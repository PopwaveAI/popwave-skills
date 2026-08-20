#!/usr/bin/env python3
"""
pop-visual-shared 固定画风测试脚本（batch_test.py）v1.4
========================================================
把画风测试固化成"固定 SOP + 任务清单导出"，杜绝每次测试全新设计、不稳定、慢的问题。

核心变化：本脚本不再直连生图 API，也不内置任何 API Key。
它只负责：解析变体 → 组装固定 6 段式提示词 → 导出 generation_tasks.json，
由主 agent 用 image_generate 工具逐条生成（图生图时传参考图保证角色一致）。

固定什么（不随测试变）：
  - 测试素材（默认用【小说次要视觉锚点】——场景/路人/NPC/战斗片段，见 style step4；
    未传时兜底用脚本内置中性素材）
  - 固定 6 段式提示词模板（[质量触发词] + Art style + 构图 + 光影 + 场景 + 角色）
  - 固定质量触发词 / 固定默认尺寸
  - 固定输出目录结构（{out_dir}/{种子}/{id}.png）
  - 固定任务清单格式（generation_tasks.json，可复现）

只随测试变（填变体即可）：
  - 画风变体列表（每个变体 = 画风 dna + constraint，或直接完整 prompt）
  - 可选 seed（固定后同 seed 复现对比）

用法：
  1) 从 DNA 库按名字批量测（推荐）：
     python batch_test.py --style-names "暗黑悬疑高对比,赛博边缘行者" \
         --out-dir 素材/测试 --seed 20260804
  2) 自定义变体（JSON 文件）：
     python batch_test.py --config test_variants.json --out-dir 素材/测试
  3) 复现验证：用同一 seed 再跑一次，输出落在同目录，对比画风是否稳定一致

生图方式：本脚本只导出任务，不调用任何 API。主 agent 读取 generation_tasks.json，
对每条任务调用 image_generate 工具（有 ref_images 时传参考图），输出到任务的 output_path。

⚠️ v1.4（画风定标素材 = 小说次要视觉锚点）：
画风定标测试素材默认用【和小说相关但无关紧要的次要元素】——某个战斗场景/地点、
路人/NPC/龙套。这类元素：和小说强相关 → 保留画风的 project 代入感；无关紧要 →
不承担角色形象验收（画风满意但形象不满的问题不会出现）。变量隔离仍成立：素材一次确定、
固定使用，唯一变量是画风。
- `--scene`：小说场景/地点/战斗场景英文描述 → 替换所有变体的场景段
- `--side`：路人/NPC/龙套英文描述 → 替换所有变体的角色段（非主角，不需一致性，纯文生图）
- 未传 --scene/--side → 兜底用脚本内置中性素材
- `--character`/`--character-image` 已废弃（主角形象归 pop-visual-art-bible/oc 环节，
  画风定标不用主角，避免混入"形象是否满意"的变量）

依赖:
  pip install Pillow (仅尺寸校验/格式校验用，可选)
"""

import argparse
import json
import os
import sys
import time

# ============ 固定配置（勿改，除非版本升级） ============

SIZE = "1125x1500"          # 画风测试默认尺寸（竖版，兼容定标）
MAX_PIXELS = 2360000        # Seedream 5.0 Pro 计费临界：超 236 万像素输出图报价翻倍，须所有出图 ≤ 上限

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


# ============ 校验工具 ============

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


def export_tasks(variants, run_dir, seed, test_mode):
    """组装并导出 generation_tasks.json。不发起任何 API 调用。"""
    os.makedirs(run_dir, exist_ok=True)

    tasks = []
    for v in variants:
        vid = v.get("id", "v")
        prompt = build_prompt(v)
        _assert_size_safe(v.get("size", SIZE))

        out_path = os.path.join(run_dir, f"{vid}.png").replace("\\", "/")
        tasks.append({
            "id": vid,
            "prompt": prompt,
            "size": v.get("size", SIZE),
            "ref_images": [],
            "output_path": out_path,
        })

    meta = {
        "total": len(tasks),
        "generator": "batch_test.py (固定画风测试 SOP)",
        "seed": seed,
        "test_mode": test_mode,
        "note": "用 image_generate 工具逐条生成，输出到每条任务的 output_path",
        "tasks": tasks,
    }
    meta_path = os.path.join(run_dir, "generation_tasks.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"已导出 {len(tasks)} 条画风测试任务 → {meta_path.replace(os.sep, '/')}")
    print("=" * 60)
    print("\n主 agent 请按以下方式用 image_generate 工具逐条生成：")
    for t in tasks:
        ref = "（图生图，参考：" + os.path.basename(t["ref_images"][0]) + "）" if t["ref_images"] else "（文生图）"
        print(f"  [{t['id']}] size={t['size']} {ref}\n    -> {t['output_path']}")
    print("\n生成完成后检查图片格式（扩展名与实际字节一致，JPEG 需转码为 PNG）。")
    return meta_path


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
    parser = argparse.ArgumentParser(description="固定画风测试 SOP（任务清单导出，不直连 API）")
    parser.add_argument("--style-names", help="逗号分隔的画风名，从 DNA 库批量取变体")
    parser.add_argument("--config", help="自定义变体 JSON 文件路径")
    parser.add_argument("--out-dir", required=True, help="输出目录（自动建 {out_dir}/{种子}）")
    parser.add_argument("--seed", type=int, default=None, help="固定随机种子（同 seed 复现对比）")
    parser.add_argument("--scene", default=None, help="[小说次要视觉锚点] 小说场景/地点/战斗场景英文描述，替换变体场景段（与小说相关、无关紧要，v1.4）")
    parser.add_argument("--side", default=None, help="[小说次要视觉锚点] 小说路人/NPC/龙套英文描述，替换变体角色段（与小说相关、无关紧要，v1.4）")
    parser.add_argument("--character", default=None, help="[已废弃] 项目角色描述（画风定标不用主角，主角形象归 art-bible/oc）")
    parser.add_argument("--character-image", default=None, help="[已废弃] 项目角色参考图路径（v1.4 起不再使用）")
    args = parser.parse_args()

    if not args.style_names and not args.config:
        parser.error("必须提供 --style-names 或 --config")

    # v1.4 起：画风定标素材用【小说次要视觉锚点】（场景/路人/NPC），不用主角、不用中性素材
    #   --scene 小说场景/地点/战斗场景描述 → 替换所有变体的场景段
    #   --side   路人/NPC/龙套描述 → 替换所有变体的角色段（非主角，不需一致性，纯文生图）
    #   --character/--character-image 已废弃（主角形象归 art-bible/oc，画风定标不用主角）
    if args.character or args.character_image:
        print("[警告] v1.4 起画风定标不用主角，--character/--character-image 已废弃，已忽略并回退到小说场景素材(或中性兜底)", file=sys.stderr)
        args.character = None
        args.character_image = None

    # 解析变体
    if args.style_names:
        template_mapping = _load_template_mapping()
        variants = variants_from_names([n for n in args.style_names.split(",") if n.strip()], template_mapping)
    else:
        variants = load_config(args.config)

    if not variants:
        print("错误：变体列表为空", file=sys.stderr)
        sys.exit(1)

    # 注入小说次要视觉锚点（场景/路人），替换所有变体对应段
    if args.scene:
        for v in variants:
            v["scene"] = args.scene
    if args.side:
        for v in variants:
            v["character"] = args.side

    # 计算测试素材模式
    if args.scene or args.side:
        asset_parts = []
        if args.scene:
            asset_parts.append("场景")
        if args.side:
            asset_parts.append("路人")
        test_mode = "小说次要视觉锚点(" + "+".join(asset_parts) + ")"
    else:
        test_mode = "中性素材(兜底)"

    # 打印固定 SOP 摘要
    print("=" * 60)
    print(f"固定画风测试 SOP (seed={args.seed})")
    print(f"尺寸: {SIZE}")
    print(f"测试素材: {test_mode}")
    print(f"变体数: {len(variants)}")
    print("=" * 60)

    # 输出目录（含种子级，便于复现对比）
    run_dir = args.out_dir if args.seed is None else os.path.join(args.out_dir, f"seed-{args.seed}")

    # 导出任务清单（唯一动作，不发起任何 API 调用）
    meta_path = export_tasks(variants, run_dir, args.seed, test_mode)

    # 固定 PE 日志（可复现的根基）
    log = {
        "sop": "固定画风测试 SOP v1.4",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "size": SIZE,
        "seed": args.seed,
        "test_mode": test_mode,
        "scene_desc": args.scene,
        "side_desc": args.side,
        "fixed_character": FIXED_CHARACTER,
        "fixed_scene": FIXED_SCENE,
        "quality_trigger": QUALITY_TRIGGER,
        "task_manifest": meta_path,
        "note": "本脚本不调用生图 API，任务清单由主 agent 用 image_generate 工具逐条生成",
    }
    log_path = os.path.join(run_dir, "pe-log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"\nPE 日志: {log_path}")


if __name__ == "__main__":
    main()