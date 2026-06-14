---
name: novel-ip-demo
display_name: 小说 IP 演示 Skill
description: 输入书名，快速生成演示用女主角 IP 卡 HTML。不现场调用慢速图像模型。版本 1.1.0
version: 1.1.0
scenario: multimodal-demo
pipeline:
  upstream: [pop-shared-reader]
  downstream: []
dependencies:
  required:
---
    - "scripts/demo_from_title.py"
    - "scripts/build_heroine_card.py"
    - "qianyu/heroine_card.json"
  optional:
    - "qianyu/refs/ — 角色参考图目录"
inject_context:
  - "heroine_card.json — 女主角 IP 卡数据"
  - "qianyu/refs/ — 角色参考图"
produces:
  - "女主角 IP 卡 HTML (.html)"
---

# Novel IP Demo

## Use When

Use this skill when the user asks to generate a demo-ready novel IP card from a book title, especially:

- "生成《千屿》的女主角 IP 卡"
- "用多模态衍生 demo 做一个角色卡"
- "给投资人演示，输入书名生成女主角卡"
- "小说 IP 卡 / 主角卡 / 角色宣发卡"

## Core Rule

For live demos, do **not** call image generation unless the user explicitly asks for a new image. Use cached/prebuilt assets so the result appears quickly and consistently.

## Preflight

```bash
# 验证前置条件
ls qianyu/heroine_card.json
ls qianyu/refs/
```

## Workflow

1. Identify the requested book title.
2. Run the local demo entrypoint from the pop-shared-book-promo root:

```bash
python3 -B scripts/demo_from_title.py --title 千屿
```

3. Return the generated HTML path relative to the skill root.

## Supported Books

Currently supported:

- `千屿`

If the requested title is not supported, say the demo currently has only `千屿` wired in, then offer to create a new `heroine_card.json` for the new book if the TXT or structured assets are available.

## Output Style

Keep the response demo-friendly:

- Say it is generated.
- Provide the clickable local HTML link.
- Avoid explaining internal file structure unless asked.
