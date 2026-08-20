#!/usr/bin/env python3
"""三组画风测试 config 生成器（build_3test.py）v1.0.0
====================================================
控制变量铁律：三组模板的非画风部分（scene/character/composition/lighting）全部固定统一，
只有画风 DNA+constraint 段是变量。跨画风复用：换 --style-name 画风名即可。

三组测试（内容形态）：
  T1_scene      场景向（style 定标思路）：环境为主，角色做尺度参照
  T2_character  角色立绘向（OC 思路）：角色居中，客观特征
  T3_comic      漫画多格向（最终产物思路）：一页多格带剧情

用法：
  单画风：
    python build_3test.py --style-name "双城之战（手绘厚涂电影感）" --out config.json
  全库：
    python build_3test.py --all --out-dir 素材/测试
生成 config 供 batch_test.py 消费：
    python ../pop-visual-shared/scripts/batch_test.py --config config.json --out-dir 素材/测试 --seed 20260804
"""
import argparse
import json
import os
import sys

# 定位 DNA 库（绝对路径优先，兼容任意 cwd）
DNA_LIB = r"D:\popwave-skills\skills\pop-visual-style\references\style-dna-library.json"


def find_dna_library():
    candidates = [
        DNA_LIB,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pop-visual-style", "references", "style-dna-library.json"),
        os.path.join(os.getcwd(), "..", "pop-visual-style", "references", "style-dna-library.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


# ============ 三组固定模板（非画风相关，全部统一中性，禁止掺画风特征） ============
TEMPLATES = {
    "T1_scene": {
        "composition": "Composition: Vast environment dominates the frame, character is small in the lower third as a scale reference. Extreme wide shot, environment as primary subject, figure as narrative anchor.",
        "lighting": "Lighting: Subtle directional lighting, clear readable shadows, atmospheric depth, balanced exposure.",
        "scene": "A broad cityscape at dusk, layered buildings receding into the distance, a wide street with scattered details, atmospheric haze, cinematic wide establishing shot, no text.",
        "character": "A tiny distant figure standing in the lower third of frame, facing away, small against the environment."
    },
    "T2_character": {
        "composition": "Composition: Character centered in the frame, three-quarter front half-body portrait, tight framing from waist up, face as the focal point.",
        "lighting": "Lighting: Subtle directional lighting, clear readable shadows, soft background falloff, balanced exposure.",
        "scene": "A simple plain interior background, soft-focus, muted tones, no text.",
        "character": "A young adult, half-body portrait, short dark hair, calm determined expression, wearing a simple jacket, facing camera, hands relaxed."
    },
    "T3_comic": {
        "composition": "Composition: A comic page with multiple panels arranged in a grid, one large establishing panel on top and two smaller panels below, dynamic panel borders, storyboard layout.",
        "lighting": "Lighting: Subtle directional lighting consistent across panels, clear readable shadows, balanced exposure.",
        "scene": "A city street scene divided into comic panels, a short dramatic sequence, no text, no speech bubbles.",
        "character": "Two characters in a tense confrontation, one facing the other, expressive poses, dynamic angles, divided across the panels."
    },
}


def build_variants(style):
    """为一个画风条目生成三组变体。"""
    dna = style.get("dna", "")
    constraint = style.get("constraint", "")
    variants = []
    for key in ["T1_scene", "T2_character", "T3_comic"]:
        t = TEMPLATES[key]
        variants.append({
            "id": key,
            "dna": dna,
            "constraint": constraint,
            "composition": t["composition"],
            "lighting": t["lighting"],
            "scene": t["scene"],
            "character": t["character"],
        })
    return variants


def main():
    parser = argparse.ArgumentParser(description="三组画风测试 config 生成器")
    parser.add_argument("--style-name", help="单个画风名")
    parser.add_argument("--all", action="store_true", help="全库模式：为所有画风生成 config")
    parser.add_argument("--out", help="单画风输出 config JSON 路径")
    parser.add_argument("--out-dir", help="全库模式输出目录（每画风一个 config）")
    args = parser.parse_args()

    if not args.style_name and not args.all:
        parser.error("必须提供 --style-name 或 --all")

    lib_path = find_dna_library()
    if not lib_path:
        print("错误：无法定位 style-dna-library.json", file=sys.stderr)
        sys.exit(1)
    with open(lib_path, "r", encoding="utf-8") as f:
        lib = json.load(f)
    styles = lib.get("styles", {})

    if args.style_name:
        if args.style_name not in styles:
            print(f"错误：DNA 库中无画风 [{args.style_name}]", file=sys.stderr)
            sys.exit(1)
        if not args.out:
            parser.error("单画风模式必须提供 --out")
        variants = build_variants(styles[args.style_name])
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump({"variants": variants}, f, ensure_ascii=False, indent=2)
        print(f"生成 {args.out}：画风 [{args.style_name}]，三组变体（T1_scene/T2_character/T3_comic）")

    elif args.all:
        if not args.out_dir:
            parser.error("全库模式必须提供 --out-dir")
        os.makedirs(args.out_dir, exist_ok=True)
        total = 0
        for name, style in styles.items():
            variants = build_variants(style)
            # 安全文件名：去掉如 "（手绘厚涂电影感）" 括号，保留主名
            safe = name.split("（")[0].strip()
            out = os.path.join(args.out_dir, f"{safe}.json")
            with open(out, "w", encoding="utf-8") as f:
                json.dump({"variants": variants}, f, ensure_ascii=False, indent=2)
            total += 1
        print(f"全库生成 {total} 个画风 config → {args.out_dir}/")

    print("非画风部分（composition/lighting/scene/character）已统一固定，仅 DNA+constraint 为变量。")


if __name__ == "__main__":
    main()