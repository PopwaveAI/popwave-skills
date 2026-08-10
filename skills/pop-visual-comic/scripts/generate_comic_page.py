#!/usr/bin/env python3
"""
pop-visual-comic 逐页漫画任务清单导出脚本 v5.2.0
================================================
生图改为由主 agent 调用 `image_generate` 工具完成，本脚本不再直调任何 HTTP API、不再内置 API Key。

职责：
  1. 从下方 PAGES 列表读取每页的 id + prompt + ref_images + size
  2. 做文字控制占位符（NEG<DIALOGUE>/NEG<TEXT>）替换 + 尺寸安全校验
  3. 解析角色定妆图参考路径（REF_IMAGES 字段）
  4. 导出 `generation_tasks.json`（每页一条任务：id/prompt/size/ref_images/output_path）
  5. 打印"请用 image_generate 工具逐张生成"的指引

页漫模式（唯一模式）：
  PAGES 每项 = 一页（内嵌多格），size 默认 1125x1500。
  条漫模式已剥离（v7.13.0 老板校准），本脚本不再支持切格 cut_type。

主 agent 用法：
  1. 修改下方 PAGES 列表（每项的 id + prompt + ref_images + 可选 size）
  2. 修改 OUTPUT_DIR / CHAR_ASSETS_DIR
  3. 运行: python generate_comic_page.py
  4. 读取生成的第{N}章/output/generation_tasks.json
  5. 对每条任务调用 image_generate 工具（prompt/text=任务prompt, size=任务size, output=任务output_path，参考图按工具能力传入）
  6. 生成后用 ensure_png_format 校验（本脚本已内置校验函数）

依赖:
  pip install Pillow
"""

import base64
import json
import os
import sys

# ============ 配置区（使用前修改） ============

# 页漫模式（唯一模式），每页内嵌多格
MODE = "page"

SIZE = "1125x1500"           # 页漫默认尺寸（总像素 169 万 ≤ 236 万上限）
MAX_PIXELS = 2360000         # 超 236 万像素计费翻倍，所有出图必须 ≤ 上限

# 输出目录（章节级）
OUTPUT_DIR = r"d:\popwave-skills\第3章\output"

# 定妆图根目录（跨章复用，字符图实际存放位置）
CHAR_ASSETS_DIR = r"C:\Users\AWMPRO\.openclaw-novel-buddy\media\tool-image-generation"

# 页面列表（每页是一张包含多格的完整漫画图）
PAGES = [
    {
        "id": "page1",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical manga comic page with a top section of three small compressed horizontal panels stacked tightly (each about 15% height, total 45%) and one large full-width horizontal panel at the bottom (55% height). Thin black gutters between all panels.\n"
                  "Panel 1: WIDE SHOT, eye level. rule of thirds composition. Morning dim cold sunlight filtering through an oil-paper window, a gnarled tree shadow cast on the window like a ghost, a lean 24-year-old man lying on a rough bed in a small clay-stove hut, messy black short hair, pale sickly face, worn gray-brown coarse cotton clothes.\n"
                  "Panel 2: EXTREME CLOSE-UP. extreme negative space, minimal composition. A translucent blue glowing semi-transparent system panel floating in the dark air, abstract luminous light patterns, one small brilliant cold light dot at the center, vast empty darkness around it.\n"
                  "Panel 3: CLOSE-UP, high angle looking down. vulnerable composition. The lean man's closed eyes, brows slightly furrowed in deep concentration, pale sickly face under soft morning light, subtle blue glow reflecting on his skin.\n"
                  "Panel 4: WIDE SHOT, low angle. diagonal composition. In a dark void, a straight luminous path abruptly splits into a side branch, the lean man's gray-clothed silhouette leaping into the branch, blue energy bloom, glowing particles, dynamic surging lines.\n"
                  "NEG<DIALOGUE>",
        "ref_images": ["char-李玄-v1-front.png", "char-李玄-v1-side.png"],
        "size": "1125x1500",
    },
    {
        "id": "page2",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical webtoon comic page with a large full-page background panel of a grand scene (65% height). Two smaller foreground panels overlap on top of the background: a medium square panel in the lower-left and a small panel in the lower-right. The foreground panels have distinct borders to separate them from the background. Thick framing.\n"
                  "Panel 1: EXTREME WIDE SHOT, high angle looking down. vulnerable composition. In a vast dark void, a straight luminous time-line path abruptly splits into an IF branch with a subtle warm color shift, a tiny gray silhouette of a man plunging into the branch, cold volumetric fog drifting, boundless cosmic emptiness.\n"
                  "Panel 2: MEDIUM CLOSE-UP, eye level. framing through a window. The lean gray-clothed man opening his eyes, everything unchanged, still lying on the rough bed in the clay-stove hut, soft morning light on his face.\n"
                  "Panel 3: EXTREME CLOSE-UP. extreme negative space. Steam and warmth rising from a steaming bowl of thin porridge seen through a gap in the window, warm ambient glow against the cold dim room, a few floating dust motes catching light.\n"
                  "NEG<DIALOGUE>",
        "ref_images": ["char-李玄-v1-front.png", "char-李玄-v1-side.png"],
        "size": "1125x1500",
    },
    {
        "id": "page3",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical webtoon comic page with a wide horizontal panel at the top (full width, 45% height) and a bottom section split into two panels: a tall narrow vertical panel on the left (25% width) and a large panel on the right (75% width). Thin black gutters between all panels.\n"
                  "Panel 1: WIDE SHOT, eye level. rule of thirds composition. A rough wooden table with three bowls of thin porridge; the center bowl (a lean gray-clothed man's) is thick with beans, rice and wild greens, while the two side bowls hold nearly clear broth. The lean man seated holding his bowl, a plump soft woman and a thin 6-year-old girl with two small buns seated opposite.\n"
                  "Panel 2: MEDIUM CLOSE-UP, diagonal composition. The plump soft woman with black hair in a simple bun gently scolding her daughter, warm caring earnest expression, gesturing toward the father's bowl.\n"
                  "Panel 3: EXTREME CLOSE-UP. extreme negative space. The thin 6-year-old girl with two small buns and big hungry eyes staring at the beans in her father's bowl, drooling, longing sorrowful expression, warm glow on her hollow cheeks.\n"
                  "IMPORTANT: 3 distinct characters with triple-locked features. The lean man has messy black short hair + deep dark drooping eyes + worn gray-brown coarse cotton farm clothes. The plump woman has black hair loosely tied in a simple bun + large warm eyes + plain gray-brown coarse cotton woman's clothing. The small girl has soft black hair in two small buns + big bright eyes + patched coarse cotton child's dress. Do NOT change any character's hair color or clothing color between panels.\n"
                  "NEG<DIALOGUE>",
        "ref_images": ["char-李玄-v1-front.png", "char-李玄-v1-side.png", "char-孟莹-v1-front.png", "char-孟莹-v1-side.png", "char-丫丫-v1-front.png", "char-丫丫-v1-side.png"],
        "size": "1125x1500",
    },
    {
        "id": "page4",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical webtoon comic page with only the upper half (50% height) occupied by a single full-width full-bleed comic art panel without any borders or gutters, the lower half left as empty plain blank space with no panels, no gutters, no borders, reserved purely as a clean background for text overlay.\n"
                  "Panel 1: EXTREME WIDE SHOT, high angle looking down. vulnerable composition. A vast cotton field at dusk on barren outskirts, a tiny lone figure with a hoe standing small in the field, distant dark silhouettes of a wealthy estate's cotton mill, oppressive heavy dark sky, cold volumetric haze, desolate and stifling atmosphere.\n"
                  "NEG<DIALOGUE>",
        "ref_images": [],
        "size": "1125x1500",
    },
    {
        "id": "page5",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical webtoon comic page with a left column of 3 stacked panels (60% width) and a large full-height panel on the right (40% width). Left column: top panel 60% height, middle panel 20% height, bottom panel 20% height. Right panel occupies the full page height. Inside the right panel, a small inset panel in the upper-left corner (15% of the right panel). Thin black gutters.\n"
                  "Panel 1: MEDIUM CLOSE-UP, diagonal composition. The plump woman slapping a pair of chopsticks on the table in feigned anger, the thin 6-year-old girl flinching, lowering her head in apology, family meal scene.\n"
                  "Panel 2: EXTREME CLOSE-UP. extreme negative space. The lean man's hand picking a few beans from his bowl and placing them into the girl's bowl, warm light.\n"
                  "Panel 3: EXTREME CLOSE-UP. extreme negative space. The small girl's little hand picking the beans back into her father's bowl, gentle determined gesture.\n"
                  "Panel 4: CLOSE-UP, eye level. framing, warm ambient glow. The thin 6-year-old girl breaking into a tearful bright smile, eyes shining with both sorrow and love, silvery tears on her hollow cheeks, warm halo light, emotional peak, luminous glow highlights.\n"
                  "IMPORTANT: 3 distinct characters with triple-locked features. The lean man has messy black short hair + deep dark drooping eyes + worn gray-brown coarse cotton farm clothes. The plump woman has black hair loosely tied in a simple bun + large warm eyes + plain gray-brown coarse cotton woman's clothing. The small girl has soft black hair in two small buns + big bright eyes + patched coarse cotton child's dress. Do NOT change any character's hair color or clothing color between panels.\n"
                  "NEG<DIALOGUE>",
        "ref_images": ["char-李玄-v1-front.png", "char-李玄-v1-side.png", "char-孟莹-v1-front.png", "char-孟莹-v1-side.png", "char-丫丫-v1-front.png", "char-丫丫-v1-side.png"],
        "size": "1125x1500",
    },
    {
        "id": "page6",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical webtoon comic page with one large vertical panel on the left (60% height) and two smaller panels side by side at the bottom (40% height). Thin black gutters between all panels.\n"
                  "Panel 1: SILHOUETTE SHOT, high angle looking down. A plump woman's silhouette walking toward a cotton mill in pale morning light, back view, small lonely figure, distant cotton mill, cold haze, quiet and weary.\n"
                  "Panel 2: MEDIUM CLOSE-UP, eye level. framing through a doorway. The thin 6-year-old girl with two small buns sitting in the room practicing embroidery, carefully stitching a small flower on a cloth, focused and earnest.\n"
                  "Panel 3: MEDIUM SHOT, eye level. rule of thirds. The lean gray-clothed man sitting alone in the room, thoughtful distant expression, gazing off into the light, quiet solitude.\n"
                  "IMPORTANT: 3 distinct characters with triple-locked features. The lean man has messy black short hair + deep dark drooping eyes + worn gray-brown coarse cotton farm clothes. The plump woman has black hair loosely tied in a simple bun + large warm eyes + plain gray-brown coarse cotton woman's clothing. The small girl has soft black hair in two small buns + big bright eyes + patched coarse cotton child's dress. Do NOT change any character's hair color or clothing color between panels.\n"
                  "NEG<DIALOGUE>",
        "ref_images": ["char-李玄-v1-front.png", "char-李玄-v1-side.png", "char-孟莹-v1-front.png", "char-孟莹-v1-side.png", "char-丫丫-v1-front.png", "char-丫丫-v1-side.png"],
        "size": "1125x1500",
    },
    {
        "id": "page7",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical webtoon comic page with a large full-page background panel of a grand scene (65% height). Two smaller foreground panels overlap on top of the background: a medium square panel in the lower-left and a small panel in the lower-right. The foreground panels have distinct borders to separate them from the background. Thick framing.\n"
                  "Panel 1: WIDE SHOT, eye level. extreme negative space. Night, the clay-stove hut with dim flickering candlelight, a curtain separating two beds, a small girl sleeping on the far side, cold night atmosphere, faint fog, quiet and intimate.\n"
                  "Panel 2: SILHOUETTE SHOT. foreground silhouette occluding view, layered depth. Two figures lying close together under a quilt, soft silhouettes partially hidden by the draped curtain, dim candlelight casting gentle shadows, tasteful and restrained intimacy, focus on mood not explicit content.\n"
                  "Panel 3: CLOSE-UP, eye level. warm ambient glow. In the darkness, the plump woman's face showing a delighted warm smile, eyes soft, realizing her husband has recovered, warm luminescent glow in the dark.\n"
                  "IMPORTANT: 2 distinct characters with triple-locked features. The lean man has messy black short hair + deep dark drooping eyes + worn gray-brown coarse cotton farm clothes. The plump woman has black hair loosely tied in a simple bun + large warm eyes + plain gray-brown coarse cotton woman's clothing. Do NOT change any character's hair color or clothing color between panels.\n"
                  "NEG<DIALOGUE>",
        "ref_images": ["char-李玄-v1-front.png", "char-李玄-v1-side.png", "char-孟莹-v1-front.png", "char-孟莹-v1-side.png"],
        "size": "1125x1500",
    },
    {
        "id": "page8",
        "prompt": "IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.\n"
                  "Art style: Korean webtoon dark fantasy manhwa style, professional thick painting technique. Soft or invisible linework, lineless rendering, forms defined by color and value transitions. Thick digital painting with visible brushwork, cold color palette. Deep blues, slate grays, desaturated crimsons, smooth skin rendering with realistic texture. Cinematic three-point lighting, strong rim lights, cold blue ambient with warm accent. 7.5 head proportion, semi-realistic, realistic features with subtle stylization. Gritty dark fantasy, cinematic and immersive, premium webtoon adaptation quality. Must be thick painted style with visible brushwork. No cel-shading. No anime style. No visible ink outlines. No soft watercolor. No cartoonish. Maintain cold color palette and cinematic quality. No text overlay.\n"
                  "Layout: A vertical webtoon comic page with a wide horizontal panel at the top (full width, 45% height) and a bottom section split into two panels: a tall narrow vertical panel on the left (25% width) and a large panel on the right (75% width). Thin black gutters between all panels.\n"
                  "Panel 1: WIDE SHOT, eye level. rule of thirds composition. At night, the lean man and plump woman lying close together under the quilt talking silently, window showing dark cold night, faint fog, intimate but restrained, peaceful.\n"
                  "Panel 2: MEDIUM CLOSE-UP, eye level. framing. The plump woman speaking seriously, solemn earnest expression, telling a grave matter, cold blue hint of mood.\n"
                  "Panel 3: EXTREME CLOSE-UP. visual juxtaposition, two contrasting elements side by side in frame. The plump woman's playful cunning teasing smile, a spark of girlish mischief in her eyes, subtle dark mysterious shadow looming behind her, contrast between her light teasing and the dark hint.\n"
                  "IMPORTANT: 2 distinct characters with triple-locked features. The lean man has messy black short hair + deep dark drooping eyes + worn gray-brown coarse cotton farm clothes. The plump woman has black hair loosely tied in a simple bun + large warm eyes + plain gray-brown coarse cotton woman's clothing. Do NOT change any character's hair color or clothing color between panels.\n"
                  "NEG<DIALOGUE>",
        "ref_images": ["char-李玄-v1-front.png", "char-李玄-v1-side.png", "char-孟莹-v1-front.png", "char-孟莹-v1-side.png"],
        "size": "1125x1500",
    },
]

# ===== 文字控制负面词（2026-08-03 实测锁定，见 references/content-layer.md §六）=====
# 对话场景（角色开口/对峙）：NEG_DIALOGUE —— 禁气泡，防伪对话乱字
TEXT_CONTROL_DIALOGUE = (
    "No speech bubbles, no dialogue balloons, no thought bubbles, no caption boxes, no dialogue text, "
    "no quotes, no sound effect text. The characters speak purely through their expressions and posture, "
    "NO text bubbles anywhere. No text, no letters, no numbers, no words, no typography, no labels, "
    "no captions, no inscriptions, no writing, no calligraphy, no handwriting, no glyphs, no symbols, "
    "no runes, no icons, no logos, no dial numerals, no roman numerals. Pure visual imagery only, "
    "no readable characters anywhere."
)
# 非对话场景：NEG_STRONG
TEXT_CONTROL_STRONG = (
    "No text, no letters, no numbers, no words, no typography, no labels, no captions, no inscriptions, "
    "no writing, no calligraphy, no handwriting, no glyphs, no symbols, no runes, no icons, no logos, "
    "no dial numerals, no roman numerals. Pure visual imagery only, no readable characters anywhere."
)

# ============ 通用工具 ============


def _assert_size_safe(size):
    """校验尺寸总像素 ≤ MAX_PIXELS。超限/无法解析则报错中止。"""
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
            f"（超 236 万像素计费翻倍），已中止。",
            file=sys.stderr,
        )
        sys.exit(1)


def resolve_ref_image(ref_name):
    """根据定妆图文件名查找完整路径"""
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), "assets", "characters", ref_name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path.replace("\\", "/")
    print(f"  [警告] 定妆图未找到: {ref_name}", file=sys.stderr)
    return None


def ensure_png_format(path):
    """检测文件实际格式，若以 .png 保存但实际是 JPEG 则转码为真 PNG。"""
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        header = f.read(8)
    if header[:3] == b'\xff\xd8\xff':  # JPEG magic bytes
        try:
            from PIL import Image
        except ImportError:
            print(f"  [警告] 文件为JPEG内容但Pillow未安装，无法转码: {path}", file=sys.stderr)
            return
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        tmp = path + ".tmp"
        img.save(tmp, "PNG", optimize=True)
        os.replace(tmp, path)
        print(f"  [格式修正] JPEG → PNG 转码: {os.path.basename(path)}")


def export_tasks():
    """把 PAGES 列表导出为 generation_tasks.json，供主 agent 用 image_generate 工具逐张生成。"""
    out_dir = OUTPUT_DIR
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", out_dir)
    os.makedirs(out_dir, exist_ok=True)

    tasks = []
    print("\n定妆图映射检查:")
    for page in PAGES:
        # 文字控制占位符替换
        prompt = page["prompt"]
        prompt = prompt.replace("NEG<DIALOGUE>", TEXT_CONTROL_DIALOGUE)
        prompt = prompt.replace("NEG<TEXT>", TEXT_CONTROL_STRONG)
        if len(prompt) > 2200:
            print(f"  [警告] {page['id']} 提示词过长: {len(prompt)} 字符")

        # 尺寸：页漫模式每页用 size，再回退默认 SIZE
        size = page.get("size", SIZE)
        _assert_size_safe(size)

        # 解析参考图路径
        ref_images = page.get("ref_images", [])
        resolved_refs = []
        for ref_name in ref_images:
            ref_path = resolve_ref_image(ref_name)
            if ref_path:
                resolved_refs.append(ref_path)

        output_path = os.path.join(out_dir, f"{page['id']}.png").replace("\\", "/")
        tasks.append({
            "id": page["id"],
            "prompt": prompt,
            "size": size,
            "ref_images": resolved_refs,
            "output_path": output_path,
        })
        if resolved_refs:
            print(f"  {page['id']}: refs={', '.join(os.path.basename(r) for r in resolved_refs)}  size={size}")
        else:
            print(f"  {page['id']}: 文生图  size={size}")

    # 导出任务清单
    meta = {
        "total_pages": len(PAGES),
        "mode": MODE,
        "generator": "generate_comic_page.py v5.2.0",
        "note": "用 image_generate 工具逐条生成，输出到每条任务的 output_path",
        "tasks": tasks,
    }
    meta_path = os.path.join(out_dir, "generation_tasks.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"已导出 {len(tasks)} 条生图任务 → {meta_path.replace(os.sep, '/')}")
    print("=" * 60)
    print("\n主 agent 请按以下方式用 image_generate 工具逐张生成：")
    print("  对 generation_tasks.json 中每条任务：")
    print("    image_generate(prompt=<任务prompt>, size=<任务size>, output=<任务output_path>)")
    print("  图生图（有 ref_images 时）：按 image_generate 工具能力传入参考图，保证角色一致性。")
    print("  生成完成后本脚本的 ensure_png_format 可校验格式，必要时手动转码。")
    return meta_path


if __name__ == "__main__":
    export_tasks()