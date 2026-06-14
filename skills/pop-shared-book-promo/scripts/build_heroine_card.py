#!/usr/bin/env python3
import argparse
import base64
import html
import json
from pathlib import Path


def data_url(path: Path) -> str:
    raw = path.read_bytes()
    suffix = path.suffix.lower()
    mime = "image/png"
    if suffix in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif suffix == ".webp":
        mime = "image/webp"
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def e(value) -> str:
    return html.escape(str(value or ""))


def render(data: dict, base_dir: Path) -> str:
    book = data["book"]
    author = data.get("author", "")
    h = data["heroine"]
    portrait_path = base_dir / h["portrait"]
    portrait = data_url(portrait_path)

    traits = "".join(f"<span>{e(t)}</span>" for t in h.get("traits", []))
    selling = "".join(f"<li>{e(item)}</li>" for item in h.get("selling_points", []))
    selling_section = ""
    if selling:
        selling_section = f'<div class="section"><h2>传播卖点</h2><ul>{selling}</ul></div>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(book)} · 女主角IP卡</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#101114;color:#f4efe8;font-family:-apple-system,BlinkMacSystemFont,"Noto Sans SC","PingFang SC",sans-serif}}
.page{{min-height:100vh;display:grid;place-items:center;padding:28px;background:
radial-gradient(circle at 18% 14%,rgba(185,63,82,.22),transparent 28%),
linear-gradient(135deg,#101114 0%,#1e2229 52%,#16100f 100%)}}
.card{{width:min(1180px,100%);min-height:720px;display:grid;grid-template-columns:.9fr 1.1fr;overflow:hidden;border:1px solid rgba(255,255,255,.12);background:rgba(18,18,20,.82);box-shadow:0 30px 90px rgba(0,0,0,.45)}}
.visual{{position:relative;background:#d8d4cf;min-height:720px;overflow:hidden}}
.visual img{{width:100%;height:100%;object-fit:cover;object-position:center top;display:block;filter:saturate(.96) contrast(1.02)}}
.visual:after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 60%,rgba(18,18,20,.84)),linear-gradient(0deg,rgba(0,0,0,.22),transparent 34%)}}
.badge{{position:absolute;left:28px;top:28px;z-index:2;padding:10px 14px;border:1px solid rgba(255,255,255,.22);background:rgba(16,17,20,.58);backdrop-filter:blur(10px);font-size:13px;color:#e9d7c7}}
.content{{padding:42px 48px 40px;display:flex;flex-direction:column;gap:20px}}
.kicker{{font-size:13px;color:#c89a8f;letter-spacing:.14em;text-transform:uppercase}}
h1{{font-size:76px;line-height:.95;margin:0;letter-spacing:0;font-weight:800}}
.role{{font-size:18px;color:#d5c3b6;margin-top:-8px}}
.tagline{{font-size:28px;line-height:1.35;color:#fff7ef;font-weight:700;max-width:720px}}
.traits{{display:flex;gap:10px;flex-wrap:wrap}}
.traits span{{padding:8px 12px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.06);font-size:14px;color:#eadbd1}}
.section{{display:grid;grid-template-columns:86px 1fr;gap:18px;border-top:1px solid rgba(255,255,255,.1);padding-top:18px}}
.section h2{{margin:0;font-size:14px;color:#c89a8f;font-weight:700}}
.section p,.section li{{margin:0;color:#d8d2ca;line-height:1.72;font-size:15px}}
ul{{padding-left:18px;margin:0;display:grid;gap:6px}}
.hook{{margin-top:auto;border:1px solid rgba(200,154,143,.34);padding:16px 18px;background:rgba(200,154,143,.08);color:#ffe6dc;font-weight:650}}
@media(max-width:860px){{.card{{grid-template-columns:1fr}}.visual{{min-height:520px}}h1{{font-size:54px}}.content{{padding:30px 24px}}.section{{grid-template-columns:1fr;gap:8px}}}}
</style>
</head>
<body>
<main class="page">
  <article class="card">
    <section class="visual">
      <div class="badge">《{e(book)}》 · {e(author)}</div>
      <img src="{portrait}" alt="{e(h['name'])}">
    </section>
    <section class="content">
      <div class="kicker">Heroine IP Card</div>
      <h1>{e(h['name'])}</h1>
      <div class="role">{e(h['role'])}</div>
      <div class="tagline">{e(h['tagline'])}</div>
      <div class="traits">{traits}</div>

      <div class="section"><h2>人物钩子</h2><p>{e(h['intro'])}</p></div>
      <div class="section"><h2>视觉记忆</h2><p>{e(h['appearance'])}</p></div>
      <div class="section"><h2>成长弧</h2><p>{e(h['arc'])}</p></div>
      <div class="section"><h2>关系张力</h2><p><strong>{e(h['relationship']['name'])}</strong>：{e(h['relationship']['dynamic'])}</p></div>
      {selling_section}
      <div class="hook">{e(h['commercial_hook'])}</div>
    </section>
  </article>
</main>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    base_dir = Path.cwd()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(data, base_dir), encoding="utf-8")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
