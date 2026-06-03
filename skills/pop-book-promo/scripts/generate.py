#!/usr/bin/env python3
"""
pop-book-promo — 多模态营销物料图像生成引擎

生图核心（Seedream 国内直连），供 LLM 在 PRD 先行工作流中调用。

用法:
  # 模式 A（推荐）：纯生图，LLM 自行设计 HTML
  python3 generate.py --mode image --prompt "..." --output scene1.png

  # 模式 B（快捷）：旧模板注入管线（向后兼容）
  python3 generate.py --mode comic --input scenes.json --output out.html
"""

import argparse, base64, html, io, json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path
from typing import Optional, List

HERE = Path(__file__).resolve().parent.parent
TEMPLATES = HERE / "templates"

# ── 常量 ──

# Seedream（火山引擎）内嵌 API Key — 免环境变量即可生图
# 🔑 此 Key 也在 SKILL.md "# 🔑 API Key" 章节中记录，方便查找
SEEDREAM_API_KEY = "b597f4e5-2370-4bdf-875f-5ae43e43c52b"

# Kimi 2.5 API Key — 用于快照/检修/质检，在 SKILL.md 🔑 章节中也有记录
KIMI_API_KEY = "sk-9FVFhuRY5B8jvwzlNb1HseqDmUvfOa2LYvN7We9EVXPMaXxT"

# 默认后端
DEFAULT_BACKEND = "seedream"

# 模型
SEEDREAM_MODEL = "doubao-seedream-5-0-260128"
OPENROUTER_MODEL = "google/gemini-2.5-flash-image"

# API 地址
SEEDREAM_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

# 默认模型
DEFAULT_MODEL = SEEDREAM_MODEL


# ═══════════════════════════════════════════
# 1. 生图后端
# ═══════════════════════════════════════════

def generate_image(prompt: str, backend: str = DEFAULT_BACKEND, api_key: str = "",
                   model: str = "", version: str = "5.0",
                   reference_images: Optional[List[Path]] = None,
                   retries: int = 2) -> bytes:
    """路由到对应的后端生图引擎"""
    if backend == "seedream":
        return _generate_seedream(prompt, version=version, retries=retries)
    else:
        return _generate_openrouter(prompt, api_key, model or OPENROUTER_MODEL,
                                    reference_images, retries)


# ── 1a. Seedream（火山引擎，国内直连） ──

def _generate_seedream(prompt: str, version: str = "5.0", retries: int = 2) -> bytes:
    """调火山引擎 Seedream 图像生成 API，返回图片 bytes

    API Key 优先级：环境变量 ARK_API_KEY > MODEL_IMAGE_API_KEY > 内嵌 key
    """
    api_key = (os.getenv("ARK_API_KEY")
               or os.getenv("MODEL_IMAGE_API_KEY")
               or SEEDREAM_API_KEY)
    if not api_key:
        print("  ❌ 未设置 ARK_API_KEY 且无内嵌 Key")
        return _placeholder_image("请设置 ARK_API_KEY")

    model = SEEDREAM_MODEL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "size": "2048x2048",
        "response_format": "b64_json",
        "watermark": False,
    }).encode()

    timeout = 120
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                f"{SEEDREAM_API_BASE}/images/generations", data=body, headers=headers,
                method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())

            images = data.get("data", [])
            if images:
                b64 = images[0].get("b64_json")
                if b64:
                    return base64.b64decode(b64)
                url = images[0].get("url")
                if url:
                    with urllib.request.urlopen(url, timeout=90) as img_resp:
                        return img_resp.read()
            print(f"  ⚠️  Seedream 响应无图片数据")
            if attempt < retries - 1:
                time.sleep(2)
            continue

        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:300]
            print(f"  ⚠️  Seedream HTTP {e.code}: {detail}")
            if e.code in {401, 403}:
                break
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠️  Seedream 失败 (attempt {attempt+1}): {e}")
            time.sleep(2)

    return _placeholder_image("Seedream 生成失败")


# ── 1b. Open Router（海外网关） ──

def _generate_openrouter(prompt: str, api_key: str, model: str,
                         reference_images: Optional[List[Path]] = None,
                         retries: int = 3) -> bytes:
    """调 Open Router 的 chat/completions 接口生成图片"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    content = [{"type": "text", "text": f"Generate one image. Return the image in the response. Prompt: {prompt}"}]
    for ref in reference_images or []:
        if ref.exists():
            content.append({"type": "image_url", "image_url": {"url": file_to_data_url(ref)}})

    body = json.dumps({
        "model": model,
        "modalities": ["image", "text"],
        "messages": [
            {"role": "user", "content": content}
        ],
    }).encode()

    timeout = 90
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                f"{OPENROUTER_API_BASE}/chat/completions", data=body, headers=headers,
                method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:300]
            print(f"  ⚠️  API HTTP {e.code}: {detail}")
            if e.code in {401, 403, 404}:
                break
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            continue
        except Exception as e:
            print(f"  ⚠️  API 调用失败 (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            continue

        try:
            message = data["choices"][0]["message"]
        except (KeyError, IndexError):
            print(f"  ⚠️  响应格式异常: {json.dumps(data, ensure_ascii=False)[:300]}")
            continue

        img_bytes = extract_image_bytes(message)
        if img_bytes:
            return img_bytes

        print(f"  ⚠️  未能提取图片数据 (attempt {attempt+1})")
        continue

    print(f"  ❌ 所有重试均失败，使用占位图")
    return _placeholder_image("Open Router 生成失败")


def extract_image_bytes(message) -> Optional[bytes]:
    """解析 OpenRouter 多种图片响应形态，兼容 Gemini 和 OpenAI 格式。"""
    candidates = []

    for img in message.get("images") or []:
        if isinstance(img, dict):
            iu = img.get("image_url") or {}
            if isinstance(iu, dict):
                candidates.append(iu.get("url", ""))
            elif isinstance(iu, str):
                candidates.append(iu)
        elif isinstance(img, str):
            candidates.append(img)

    content = message.get("content", "")
    if isinstance(content, list):
        for part in content:
            if not isinstance(part, dict):
                continue
            if part.get("type") in {"image_url", "input_image", "inline_image"}:
                iu = part.get("image_url") or {}
                candidates.append(iu.get("url", "") if isinstance(iu, dict) else str(iu))
            txt = part.get("text", "")
            if txt and len(txt) > 100:
                candidates.append(txt)
    elif isinstance(content, str):
        candidates.append(content)
        md_urls = re.findall(r'!\[.*?\]\((https?://[^\s)]+)\)', content)
        candidates.extend(md_urls)

    candidates.append(message.get("image_str", ""))

    for value in candidates:
        img_bytes = decode_image_candidate(value)
        if img_bytes:
            return img_bytes
    return None


def decode_image_candidate(value: str) -> Optional[bytes]:
    if not value:
        return None
    data_url = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=\n\r]+)', value)
    if data_url:
        return base64.b64decode(re.sub(r'\s+', '', data_url.group(1)))
    if value.startswith(("http://", "https://")):
        try:
            req = urllib.request.Request(value, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return resp.read()
        except Exception as e:
            print(f"  ⚠️  图片 URL 下载失败: {e}")
            return None
    compact = re.sub(r'\s+', '', value.strip())
    if len(compact) > 500:
        try:
            return base64.b64decode(compact, validate=True)
        except Exception:
            return None
    return None


def _placeholder_image(msg: str = "图片生成失败") -> bytes:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="768">
      <rect width="1024" height="768" fill="#1a1a2e"/>
      <text x="512" y="384" text-anchor="middle" fill="#8b949e" font-size="24" font-family="sans-serif">{msg}</text>
      <text x="512" y="420" text-anchor="middle" fill="#484f58" font-size="14" font-family="sans-serif">请检查 API Key 或网络连接</text>
    </svg>'''
    return svg.encode()


def img_to_data_url(img_bytes: bytes) -> str:
    """将图片 bytes 转为 data URL"""
    if img_bytes[:4] == b'<svg':
        b64 = base64.b64encode(img_bytes).decode()
        return f"data:image/svg+xml;base64,{b64}"
    if img_bytes[:3] == b'\xff\xd8\xff':
        fmt = "jpeg"
    elif img_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        fmt = "png"
    elif img_bytes[:4] == b'RIFF':
        fmt = "webp"
    else:
        fmt = "png"
    b64 = base64.b64encode(img_bytes).decode()
    return f"data:image/{fmt};base64,{b64}"


def file_to_data_url(path: Path) -> str:
    data = path.read_bytes()
    return img_to_data_url(data)


def safe_filename(value: str, fallback: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|\\s]+', "_", value.strip())
    cleaned = cleaned.strip("._")
    return cleaned or fallback


def write_asset(save_assets: Optional[Path], name: str, img_bytes: bytes) -> None:
    if not save_assets:
        return
    save_assets.mkdir(parents=True, exist_ok=True)
    (save_assets / f"{safe_filename(name, 'image')}.png").write_bytes(img_bytes)


def reference_paths(reference_dir: Optional[Path], character_names: List[str]) -> List[Path]:
    if not reference_dir:
        return []
    paths = []
    for name in character_names:
        path = reference_dir / f"{safe_filename(name, name)}.png"
        if path.exists():
            paths.append(path)
    return paths


def apply_style_bible(data: dict) -> dict:
    """把同一项目的视觉规范注入所有 image prompt，提升一致性。"""
    style = data.get("style_bible")
    if not style:
        return data

    def merge_prompt(item: dict, keys: tuple[str, ...]) -> None:
        for key in keys:
            if item.get(key) and style not in item[key]:
                item[key] = f"{item[key]}, {style}"
                return

    for scene in data.get("scenes") or []:
        merge_prompt(scene, ("image_prompt", "description"))
    for quote in data.get("quotes") or []:
        merge_prompt(quote, ("image_prompt", "character_desc"))
    for character in data.get("characters") or []:
        merge_prompt(character, ("image_prompt", "appearance_prompt", "desc"))
    merge_prompt(data, ("image_prompt", "appearance", "desc"))
    return data


def _build_scene_prompt(scene: dict) -> str:
    """当 scene 缺少 image_prompt 时，从可用数据构建半合格 prompt"""
    title = scene.get("title", "")
    emotion = scene.get("emotion", "")
    chars = scene.get("characters", [])
    chars_str = ", ".join(chars) if chars else "characters"
    dialogue = scene.get("dialogue", "")

    emo_map = {
        "悲壮": "solemn and dramatic", "温馨": "warm and tender",
        "激烈": "intense and tense", "悬疑": "mysterious",
        "甜蜜": "sweet and romantic", "愤怒": "fierce with anger",
        "搞笑": "light-hearted and humorous",
    }
    emo_en = emo_map.get(emotion, "atmospheric")
    parts = ["Chinese xianxia novel scene", f"featuring {chars_str}", f"mood: {emo_en}"]
    if title:
        parts.append(f"scene: {title}")
    if dialogue:
        parts.append(f'key dialogue: "{dialogue.replace(chr(10), " ")[:60]}"')
    parts.append("traditional Chinese painting aesthetic, cinematic composition, high detail")
    return ", ".join(parts)


# ── 模式 A：纯生图（LLM 设计 HTML） — 见 main() 中实现


# ── 模式 B（旧/快捷）：模板注入（向后兼容） ──

def render_template(template_name: str, **kwargs) -> str:
    """读取模板文件，替换占位符"""
    tpl_path = TEMPLATES / template_name
    if not tpl_path.exists():
        raise FileNotFoundError(f"模板不存在: {tpl_path}")
    html_str = tpl_path.read_text(encoding="utf-8")
    for key, val in kwargs.items():
        placeholder = f"__{key.upper()}__"
        html_str = html_str.replace(placeholder, str(val))
    return html_str


def build_comic(scenes: list, novel: str, backend: str = DEFAULT_BACKEND,
                api_key: str = "", model: str = "",
                reference_dir: Optional[Path] = None,
                save_assets: Optional[Path] = None) -> str:
    """四格漫画（模板注入）"""
    panels_html = ""
    for i, scene in enumerate(scenes[:4]):
        prompt = scene.get("image_prompt") or _build_scene_prompt(scene)
        title = scene.get("title", f"场景{i+1}")
        dialogue = scene.get("dialogue", "")
        chapter = scene.get("chapter", "")
        refs = reference_paths(reference_dir, scene.get("characters", []))
        if refs and backend == "openrouter":
            prompt = (f"{prompt}. Use the provided reference image(s) as strict character anchors. "
                      "Preserve identity and visual design.")
        print(f"  [{i+1}/4] {title}")
        img_bytes = generate_image(prompt, backend=backend, api_key=api_key,
                                   model=model, reference_images=refs)
        write_asset(save_assets, f"{i+1:02d}_{title}", img_bytes)
        data_url = img_to_data_url(img_bytes)
        d_lines = "".join(f"<p>{html.escape(l)}</p>" for l in dialogue.split("\n") if l.strip())
        panels_html += f'''
        <div class="panel">
          <div class="panel-label">{html.escape(title)}<span class="ch">·{html.escape(chapter)}</span></div>
          <div class="panel-img"><img src="{data_url}" alt="{html.escape(title)}"></div>
          <div class="panel-dialogue">{d_lines}</div>
        </div>'''
    return render_template("comic.html", title=novel, panels=panels_html)


def build_scroll(profile: dict, backend: str = DEFAULT_BACKEND,
                 api_key: str = "", model: str = "",
                 reference_dir: Optional[Path] = None,
                 save_assets: Optional[Path] = None) -> str:
    """古风人物画卷（模板注入）"""
    novel = profile.get("novel", profile.get("name", "角色"))
    name = profile.get("name", "未知")
    desc = profile.get("desc", profile.get("personality", ""))
    appearance = profile.get("appearance", "")
    prompt = profile.get("image_prompt", f"Chinese fantasy novel character portrait: {appearance}")
    print(f"  生成角色画像: {name}")
    refs = reference_paths(reference_dir, [name])
    img_bytes = generate_image(prompt, backend=backend, api_key=api_key,
                               model=model, reference_images=refs)
    write_asset(save_assets, name, img_bytes)
    hero_img = img_to_data_url(img_bytes)
    timeline = profile.get("timeline", [])
    timeline_html = ""
    for i, evt in enumerate(timeline[:8]):
        evt_prompt = f"Chinese fantasy scene: {evt.get('event', '')}"
        print(f"  时间线节点 {i+1}")
        evt_img = generate_image(evt_prompt, backend=backend, api_key=api_key,
                                 model=model, reference_images=refs)
        write_asset(save_assets, f"timeline_{i+1:02d}", evt_img)
        evt_url = img_to_data_url(evt_img)
        timeline_html += f'''
        <div class="scroll-node">
          <div class="scroll-node-img"><img src="{evt_url}" alt=""></div>
          <div class="scroll-node-info">
            <span class="ch">第{evt.get('chapter','?')}章</span>
            <p>{html.escape(evt.get('event',''))}</p>
          </div>
        </div>'''
    quotes = profile.get("quotes", [])
    quotes_html = ""
    for q in quotes[:3]:
        quotes_html += f'<blockquote><p>“{html.escape(q.get("text",""))}”</p><cite>——第{html.escape(q.get("chapter","?"))}章</cite></blockquote>'
    return render_template("scroll.html",
        title=f"{novel} · {name}", name=name,
        description=html.escape(desc).replace("\n", "<br>"),
        hero_img=hero_img, timeline=timeline_html, quotes=quotes_html)


def build_scenes(scenes: list, novel: str, backend: str = DEFAULT_BACKEND,
                 api_key: str = "", model: str = "",
                 reference_dir: Optional[Path] = None,
                 save_assets: Optional[Path] = None) -> str:
    """名场面高光帧（模板注入）"""
    cards_html = ""
    for i, scene in enumerate(scenes):
        prompt = scene.get("image_prompt") or _build_scene_prompt(scene)
        title = scene.get("title", f"名场面{i+1}")
        chapter = scene.get("chapter", "")
        dialogue = scene.get("dialogue", "")
        emotion = scene.get("emotion", "")
        refs = reference_paths(reference_dir, scene.get("characters", []))
        if refs:
            prompt = f"{prompt}. Preserve identity from reference."
        print(f"  [{i+1}/{len(scenes)}] {title}")
        img_bytes = generate_image(prompt, backend=backend, api_key=api_key,
                                   model=model, reference_images=refs)
        write_asset(save_assets, f"{i+1:02d}_{title}", img_bytes)
        data_url = img_to_data_url(img_bytes)
        emoji_map = {"悲壮":"💔","温馨":"☀️","激烈":"⚡","悬疑":"🔍","甜蜜":"💕","愤怒":"🔥","感人":"😢","搞笑":"😂"}
        emoji = emoji_map.get(emotion, "✨")
        d_lines = "".join(f"<p>{html.escape(l)}</p>" for l in dialogue.split("\n") if l.strip())
        cards_html += f'''
        <div class="scene-card">
          <div class="scene-img"><img src="{data_url}" alt="{html.escape(title)}"></div>
          <div class="scene-meta">
            <span class="emotion-tag">{emoji} {html.escape(emotion)}</span>
            <span class="chapter-tag">📖 {html.escape(chapter)}</span>
          </div>
          <div class="scene-title">{html.escape(title)}</div>
          <div class="scene-dialogue">{d_lines}</div>
        </div>'''
    return render_template("scenes.html", title=f"{novel} · 名场面", cards=cards_html)


def build_quote(quotes: list, novel: str, backend: str = DEFAULT_BACKEND,
                api_key: str = "", model: str = "",
                reference_dir: Optional[Path] = None,
                save_assets: Optional[Path] = None) -> str:
    """金句分享卡（模板注入）"""
    cards_html = ""
    for i, q in enumerate(quotes):
        char_name = q.get("character", "未知")
        quote_text = q.get("quote", "")
        chapter = q.get("chapter", "")
        char_desc = q.get("character_desc", "一个小说角色")
        prompt = q.get("image_prompt") or f"Chinese fantasy novel character portrait, half body: {char_desc}"
        refs = reference_paths(reference_dir, [char_name])
        if refs:
            prompt = f"{prompt}. Preserve identity."
        print(f"  [{i+1}/{len(quotes)}] {char_name}")
        img_bytes = generate_image(prompt, backend=backend, api_key=api_key,
                                   model=model, reference_images=refs)
        write_asset(save_assets, f"{i+1:02d}_{char_name}", img_bytes)
        data_url = img_to_data_url(img_bytes)
        cards_html += f'''
        <div class="quote-card">
          <div class="quote-char-img"><img src="{data_url}" alt="{char_name}"></div>
          <div class="quote-body">
            <div class="quote-text">“{html.escape(quote_text)}”</div>
            <div class="quote-char">{html.escape(char_name)}</div>
            <div class="quote-chapter">——《{html.escape(novel)}》第{html.escape(chapter)}章</div>
          </div>
        </div>'''
    return render_template("quote.html", title=f"{novel} · 金句集", cards=cards_html)


def build_gallery(characters: list, novel: str, backend: str = DEFAULT_BACKEND,
                  api_key: str = "", model: str = "",
                  reference_dir: Optional[Path] = None,
                  save_assets: Optional[Path] = None) -> str:
    """角色立绘画廊（模板注入）"""
    cards_html = ""
    for i, ch in enumerate(characters):
        name = ch.get("name", f"角色{i+1}")
        desc = ch.get("desc", ch.get("type", ""))
        faction = ch.get("faction", "")
        prompt = ch.get("image_prompt") or ch.get("appearance_prompt",
                      f"Chinese fantasy character: {name}, {desc}")
        color = ch.get("color", "#7c5cff")
        refs = reference_paths(reference_dir, [name])
        if refs:
            prompt = f"{prompt}. Preserve identity."
        print(f"  [{i+1}/{len(characters)}] {name}")
        img_bytes = generate_image(prompt, backend=backend, api_key=api_key,
                                   model=model, reference_images=refs)
        write_asset(save_assets, name, img_bytes)
        data_url = img_to_data_url(img_bytes)
        cards_html += f'''
        <div class="gallery-card" style="--accent:{color}">
          <div class="gallery-img"><img src="{data_url}" alt="{html.escape(name)}"></div>
          <div class="gallery-info">
            <div class="gallery-name">{html.escape(name)}</div>
            {f'<div class="gallery-faction">{html.escape(faction)}</div>' if faction else ''}
            {f'<div class="gallery-desc">{html.escape(desc[:60])}</div>' if desc else ''}
          </div>
        </div>'''
    return render_template("gallery.html", title=f"{novel} · 角色画廊", cards=cards_html)


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="pop-book-promo · 营销物料生图引擎")
    parser.add_argument("--mode", required=True,
        choices=["image", "comic", "scroll", "scenes", "quote", "gallery"],
        help="运行模式：image=纯生图(推荐) | 其余=旧模板管线(向后兼容)")
    parser.add_argument("--prompt", "-p", help="出图提示词（仅 image 模式）")
    parser.add_argument("--input", "-i", type=Path, help="输入 JSON（仅模板模式）")
    parser.add_argument("--output", "-o", required=True, help="输出路径（图片或 HTML）")
    parser.add_argument("--backend", default=DEFAULT_BACKEND, choices=["seedream", "openrouter"])
    parser.add_argument("--api-key")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-items", type=int)
    parser.add_argument("--reference-dir", type=Path)
    parser.add_argument("--save-assets", type=Path)
    args = parser.parse_args()

    # API Key 校验
    if args.backend == "openrouter":
        args.api_key = args.api_key or os.getenv("OPEN_ROUTER_API_KEY")
        if not args.api_key:
            parser.error("OpenRouter 后端需要 API Key")
    else:
        args.api_key = args.api_key or ""

    # ── 模式 A：纯生图（推荐） ──
    if args.mode == "image":
        if not args.prompt:
            parser.error("image 模式需要 --prompt/-p")
        print(f"  🎨 生图: {args.prompt[:60]}...")
        img_bytes = generate_image(args.prompt, backend=args.backend, api_key=args.api_key,
                                   model=args.model)
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(img_bytes)
        print(f"  ✅ {out_path.resolve()} ({len(img_bytes)/1024:.0f} KB)")
        print(f"  🔗 Data URL: {img_to_data_url(img_bytes)[:80]}...")
        return

    # ── 模式 B：模板注入（向后兼容） ──
    if not args.input:
        parser.error("模板模式需要 --input")
    data = json.loads(args.input.read_text(encoding="utf-8"))
    data = apply_style_bible(data)
    novel = data.get("novel", data.get("title", "未命名"))
    if args.max_items:
        for key in ("scenes", "quotes", "characters"):
            if isinstance(data.get(key), list):
                data[key] = data[key][:args.max_items]
        if isinstance(data.get("timeline"), list):
            data["timeline"] = data["timeline"][:args.max_items]

    factory = {
        "comic": lambda: build_comic(data.get("scenes", []), novel, args.backend, args.api_key, args.model, args.reference_dir, args.save_assets),
        "scroll": lambda: build_scroll(data, args.backend, args.api_key, args.model, args.reference_dir, args.save_assets),
        "scenes": lambda: build_scenes(data.get("scenes", []), novel, args.backend, args.api_key, args.model, args.reference_dir, args.save_assets),
        "quote": lambda: build_quote(data.get("quotes", []), novel, args.backend, args.api_key, args.model, args.reference_dir, args.save_assets),
        "gallery": lambda: build_gallery(data.get("characters", []), novel, args.backend, args.api_key, args.model, args.reference_dir, args.save_assets),
    }
    print(f"🚀 模板模式: {args.mode} | {novel}")
    html = factory[args.mode]()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"✅ 输出: {out_path.resolve()} ({out_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
