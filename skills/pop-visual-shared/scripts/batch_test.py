#!/usr/bin/env python3
"""
pop-visual-shared 固定画风测试脚本（batch_test.py）v1.0
========================================================
把画风测试固化成"固定 SOP + 并发批量"，杜绝每次测试全新设计、不稳定、慢的问题。

固定什么（不随测试变）：
  - 默认测试素材（标准角色 + 标准场景，变量隔离，见 style step4）
  - 固定 6 段式提示词模板（[质量触发词] + Art style + 构图 + 光影 + 场景 + 角色）
  - 固定质量触发词 / 固定模型 / 固定默认尺寸
  - 固定输出目录结构（{out_dir}/{种子}/{id}.png）
  - 固定 PE 日志格式（自动落盘，可复现）

只随测试变（填变体即可）：
  - 画风变体列表（每个变体 = 画风 dna + constraint，或直接完整 prompt）
  - 可选 seed（固定后同 seed 复现对比）
  - **可选项目角色（--character 文字 / --character-image 参考图）**：画风×项目角色联合测试

用法：
  1) 从 DNA 库按名字批量测（推荐）：
     python batch_test.py --style-names "暗黑悬疑高对比,赛博边缘行者" \
         --out-dir 素材/测试 --seed 20260804
  2) 自定义变体（JSON 文件）：
     python batch_test.py --config test_variants.json --out-dir 素材/测试
  3) 复现验证：用同一 seed 再跑一次，对比画风是否稳定一致
  4) **画风×项目角色联合测试（推荐，验证画风能否撑起角色）**：
     python batch_test.py --style-names "国漫玄幻厚涂" \
         --character "李周巍, 黑金玄纹甲衣, 紫羽王氅, 金瞳, 持长戟" \
         --character-image "素材/李周巍OC-v1.png" \
         --out-dir 素材/风格测试 --seed 20260804

环境变量:
  ARK_API_KEY - 火山引擎方舟 API Key（默认值已内置）

依赖:
  pip install requests Pillow
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO

# ============ 固定配置（勿改，除非版本升级） ============

API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
API_KEY = os.environ.get("ARK_API_KEY", "b597f4e5-2370-4bdf-875f-5ae43e43c52b")
MODEL = "doubao-seedream-5-0-pro-260628"
SIZE = "1125x1500"          # 画风测试默认尺寸（竖版，兼容定标）
MAX_PIXELS = 2360000        # Seedream 5.0 Pro 计费临界：超 236 万像素输出图报价翻倍，须所有出图 ≤ 上限
CONCURRENCY = 8              # 并发线程数（Seedream 500 图/分钟，8 线程安全）
MAX_RETRIES = 3              # 指数退避重试次数
API_TIMEOUT = int(os.environ.get("SEEDREAM_TIMEOUT", "300"))  # 单次生成超时(秒)，Seedream 5.0 Pro 单图可达80s+，并发排队更久，120s 易误判超时

# 固定质量触发词（画风测试用，非写实词——写实词会推高厚涂倾向）
QUALITY_TRIGGER = "High quality anime comic illustration, highly detailed, professional manga art, clean lineart, crisp colors."

# 固定测试素材（变量隔离铁律：画风测试唯一变量是画风，素材永不换）
FIXED_CHARACTER = ("a young adult standing half-body portrait, neutral calm expression, "
                   "simple dark hair, plain white inner shirt under a muted earthy jacket, "
                   "natural skin texture, facing camera, no accessories, no text")
FIXED_SCENE = ("a simple quiet interior, warm wooden room, soft window light from the left, "
               "a wooden table and a potted plant, calm atmosphere, no people, no text")

# 固定 6 段式提示词模板（占位符 {dna} {constraint} {composition} {lighting}）
PROMPT_TEMPLATE = (
    "{quality_trigger} "
    "Art style: {dna} {constraint} "
    "{composition} "
    "{lighting} "
    "{scene} "
    "{character}"
)

# 默认构图/光影占位（若变体未指定，用中性默认，避免引入额外变量）
DEFAULT_COMPOSITION = "Character centered in frame, balanced composition."
DEFAULT_LIGHTING = "Soft even lighting, clear readable shadows."

# ============ 构图/光照模板解析（代码 → 英文描述） ============
# 画风 DNA 库的 recommended_composition/recommended_lighting 存的是代码标识
# （如 CT2_silhouette_back / LT1_subtractive），真正的英文描述在
# style 的 lighting-composition-templates.md。本函数解析该文件，把代码映射成英文。

COMPOSITION_CODES = {
    "CT1": "CT1 尺度操控（Scale Contrast）",
    "CT2": "CT2 剪影悬念（Silhouette Suspense）",
}
LIGHTING_CODES = {
    "LT1": "LT1 减法照明（Subtractive Lighting）",
    "LT2": "LT2 柔光通透（Soft Luminous Lighting）",
    "LT3": "LT3 平光漫射（Flat Atmospheric Lighting）",
}


def _extract_template_md(path):
    """从 lighting-composition-templates.md 提取 代码→英文描述 映射。"""
    mapping = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return mapping
    # 按 "### {CODE} {名称}" 分块，取块内第一段英文描述（紧跟在 "**英文描述**（直接拼入提示词）：" 后的代码块）
    import re
    for code in set(COMPOSITION_CODES) | set(LIGHTING_CODES):
        # 匹配 "### CT1 尺度操控（Scale Contrast）" 这样的标题
        pat = re.compile(r"###\s*" + re.escape(code) + r"\b.*?\n```\n(.*?)\n```", re.S)
        m = pat.search(content)
        if m:
            mapping[code] = m.group(1).strip()
    return mapping


def _load_template_mapping():
    """加载模板描述映射，优先从 style 的 lighting-composition-templates.md 解析。"""
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pop-visual-style", "references", "lighting-composition-templates.md"),
        os.path.join(os.getcwd(), "..", "pop-visual-style", "references", "lighting-composition-templates.md"),
    ]
    for p in candidates:
        if os.path.exists(p):
            mapping = _extract_template_md(p)
            if mapping:
                return mapping
    return {}


def resolve_template(code, mapping):
    """把代码标识（CT2_silhouette_back / LT1_subtractive）映射为英文描述。
    解析失败时返回空白，避免把代码标识拼进提示词污染画风。"""
    if not code:
        return ""
    base = code.split("_")[0]  # 取 CT2 / LT1 前缀
    return mapping.get(base, "")


# ============ 引力工具 ============

def ensure_png_bytes(img_bytes):
    """检测字节流实际格式，JPEG 则转码为 PNG 字节流。"""
    if img_bytes[:2] == b'\xff\xd8':
        try:
            from PIL import Image
        except ImportError:
            return img_bytes
        img = Image.open(BytesIO(img_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    return img_bytes


def build_prompt(variant):
    """按固定 6 段式模板组装单变体提示词。variant 可含 dna/constraint/composition/lighting/character/scene。"""
    return PROMPT_TEMPLATE.format(
        quality_trigger=variant.get("quality_trigger", QUALITY_TRIGGER),
        dna=variant.get("dna", ""),
        constraint=variant.get("constraint", ""),
        composition=variant.get("composition", DEFAULT_COMPOSITION),
        lighting=variant.get("lighting", DEFAULT_LIGHTING),
        scene=variant.get("scene", FIXED_SCENE),
        character=variant.get("character", FIXED_CHARACTER),
    ).strip()


def resolve_character_image(path):
    """把本地角色参考图转为 data URI（图生图参考，保证角色一致）。支持 .png/.jpg/.jpeg。"""
    if not path or not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext.lstrip("."), "image/png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _assert_size_safe(size):
    """校验尺寸总像素 ≤ MAX_PIXELS。超限直接报错中止。"""
    if not size:
        return
    s = str(size).strip().lower()
    if "x" in s:
        try:
            w, h = s.split("x")
            pixels = int(w) * int(h)
        except Exception:
            print(f"  [错误] 无法解析尺寸: {size}", file=sys.stderr)
            sys.exit(1)
    else:
        rating = {"1k": 1024, "2k": 2048, "4k": 4096}.get(s)
        if rating is None:
            print(f"  [错误] 未知尺寸档位: {size}", file=sys.stderr)
            sys.exit(1)
        pixels = rating * rating
    if pixels > MAX_PIXELS:
        print(
            f"  [错误] 尺寸 {size} = {pixels} 像素，超过上限 {MAX_PIXELS} 像素"
            f"（Seedream 5.0 Pro 超 236 万像素报价翻倍），已中止。",
            file=sys.stderr,
        )
        sys.exit(1)


def generate_one(variant, output_path, seed):
    """并发生成单张。返回 {id, success, path, prompt}。"""
    prompt = build_prompt(variant)
    size = variant.get("size", SIZE)
    _assert_size_safe(size)
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "size": size,
        "watermark": False,
        "response_format": "b64_json",
    }
    if seed is not None:
        payload["seed"] = seed
    # 角色参考图（图生图，保证角色一致性）
    ref = variant.get("character_image")
    if ref:
        payload["image"] = ref

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    data = json.dumps(payload).encode("utf-8")

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=API_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            data_list = result.get("data", [])
            if not data_list:
                raise RuntimeError("未返回图片数据")
            item = data_list[0]
            if "error" in item:
                raise RuntimeError(f"API error: {item['error']}")
            b64 = item.get("b64_json")
            if not b64:
                raise RuntimeError("未返回 b64_json")
            img_bytes = ensure_png_bytes(base64.b64decode(b64))
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            size = len(img_bytes) // 1024
            print(f"  [OK] {variant['id']} ({size}KB, seed={seed})")
            return {"id": variant["id"], "success": True, "path": output_path, "prompt": prompt}
        except Exception as e:
            print(f"  [错误] {variant['id']} 尝试{attempt+1}: {str(e)[:120]}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                time.sleep(3 * (attempt + 1))
    print(f"  [失败] {variant['id']} 全部重试失败", file=sys.stderr)
    return {"id": variant.get("id", "?"), "success": False, "path": output_path, "prompt": prompt}


# ============ 变体解析 ============

def load_dna_library():
    """读取 style skill 的 DNA 库。"""
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pop-visual-style", "references", "style-dna-library.json"),
        os.path.join(os.getcwd(), "..", "pop-visual-style", "references", "style-dna-library.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return None


def variants_from_names(names, template_mapping=None):
    """按画风名从 DNA 库批量取变体。找不到的报错。"""
    lib = load_dna_library()
    if not lib:
        print("错误：无法定位 style-dna-library.json，请用 --config 传自定义变体", file=sys.stderr)
        sys.exit(1)
    styles = lib.get("styles", {})
    if template_mapping is None:
        template_mapping = _load_template_mapping()
    variants = []
    for name in names:
        name = name.strip()
        if name not in styles:
            print(f"错误：DNA 库中无画风 [{name}]", file=sys.stderr)
            sys.exit(1)
        s = styles[name]
        variants.append({
            "id": name,
            "dna": s.get("dna", ""),
            "constraint": s.get("constraint", ""),
            "composition": resolve_template(s.get("recommended_composition", ""), template_mapping),
            "lighting": resolve_template(s.get("recommended_lighting", ""), template_mapping),
        })
    return variants


def load_config(path):
    """读取 JSON 变体配置文件。支持 {out_dir} 与 list 两种结构。"""
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if isinstance(cfg, list):
        return cfg
    return cfg.get("variants", [])


# ============ 主流程 ============

def main():
    parser = argparse.ArgumentParser(description="固定画风测试 SOP（并发批量）")
    parser.add_argument("--style-names", help="逗号分隔的画风名，从 DNA 库批量取变体")
    parser.add_argument("--config", help="自定义变体 JSON 文件路径")
    parser.add_argument("--out-dir", required=True, help="输出目录（自动建 {out_dir}/{种子}）")
    parser.add_argument("--seed", type=int, default=None, help="固定随机种子（同 seed 复现对比）")
    parser.add_argument("--concurrency", type=int, default=CONCURRENCY, help="并发线程数")
    parser.add_argument("--character", default=None, help="项目角色描述（英文或中文，替换标准测试角色，用于画风×角色联合测试）")
    parser.add_argument("--character-image", default=None, help="项目角色参考图路径（图生图，保证角色一致性）")
    args = parser.parse_args()

    if not args.style_names and not args.config:
        parser.error("必须提供 --style-names 或 --config")

    # 解析变体
    if args.style_names:
        template_mapping = _load_template_mapping()
        variants = variants_from_names([n for n in args.style_names.split(",") if n.strip()], template_mapping)
    else:
        variants = load_config(args.config)

    if not variants:
        print("错误：变体列表为空", file=sys.stderr)
        sys.exit(1)

    # 注入项目角色（画风×角色联合测试）
    # 若传了 --character，用项目角色替换全部变体的角色段；若传了 --character-image，作图生图参考
    character_ref = resolve_character_image(args.character_image) if args.character_image else None
    if args.character or character_ref:
        for v in variants:
            if args.character:
                v["character"] = args.character
            if character_ref:
                v["character_image"] = character_ref

    # 打印固定 SOP 摘要
    print("=" * 60)
    print(f"固定画风测试 SOP (并发={args.concurrency}, seed={args.seed})")
    print(f"模型: {MODEL} | 尺寸: {SIZE}")
    if args.character or character_ref:
        print(f"测试素材: 项目角色{'(参考图)' if character_ref else ''} + 标准场景（画风×角色联合测试）")
    else:
        print(f"测试素材: 标准角色 + 标准场景（变量隔离）")
    print(f"变体数: {len(variants)}")
    print("=" * 60)

    # 输出目录（含种子级，便于复现对比）
    run_dir = args.out_dir if args.seed is None else os.path.join(args.out_dir, f"seed-{args.seed}")
    os.makedirs(run_dir, exist_ok=True)

    start = time.time()

    # 并发批量生成
    results = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {}
        for v in variants:
            vid = v.get("id", "v")
            out_path = os.path.join(run_dir, f"{vid}.png")
            fut = ex.submit(generate_one, v, out_path, args.seed)
            futures[fut] = v
        for fut in as_completed(futures):
            try:
                results.append(fut.result())
            except Exception as e:
                vid = futures[fut].get("id", "?")
                print(f"  [崩溃] {vid}: {e}", file=sys.stderr)
                results.append({"id": vid, "success": False, "path": None, "prompt": ""})

    elapsed = time.time() - start

    # 汇总
    ok = sum(1 for r in results if r["success"])
    print("\n" + "=" * 60)
    print(f"汇总: 成功 {ok}/{len(results)} | 耗时 {elapsed:.1f}s (串行约 {elapsed*args.concurrency:.0f}s)")
    for r in results:
        print(f"  [{'OK' if r['success'] else 'FAIL'}] {r['id']} -> {r.get('path')}")

    # 固定 PE 日志（可复现的根基）
    log = {
        "sop": "固定画风测试 SOP v1.1",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": MODEL,
        "size": SIZE,
        "concurrency": args.concurrency,
        "seed": args.seed,
        "test_mode": "画风×项目角色联合测试" if (args.character or character_ref) else "标准素材(变量隔离)",
        "character_desc": args.character,
        "character_image": args.character_image,
        "fixed_character": FIXED_CHARACTER,
        "fixed_scene": FIXED_SCENE,
        "quality_trigger": QUALITY_TRIGGER,
        "variants": results,
    }
    log_path = os.path.join(run_dir, "pe-log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"\nPE 日志: {log_path}")


if __name__ == "__main__":
    main()