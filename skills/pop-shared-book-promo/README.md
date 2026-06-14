# pop-shared-book-promo — 多模态营销物料生成

> **原项目**: multi-modal-marketing v1.0.0
> **重构**: 2026-05-29 · 对齐 Popwave Skill 设计规范 v1.0
> **标签**: `multimodal` `image-generation` `open-router` `marketing` `html-renderer`

---

## 是什么

从拆书分析产出的结构化数据（角色/场景/金句）出发，调用 Open Router 多模态图像 API 生成配图，交付 **5 种传播级 HTML 营销物料**。

## 5 种物料

| # | 物料 | 场景 |
|:-:|:----|:-----|
| 🎨 | **名场面四格漫画** | 小红书 / 微博 |
| 📜 | **古风人物画卷** | 官网 / 推书帖 |
| 🎬 | **名场面高光帧** | 推书长图 / 公众号 |
| 💬 | **金句分享卡** | 朋友圈 / 小红书 |
| 🎭 | **角色立绘画廊** | 角色宣传页 |

## 快速开始

```bash
pip install requests
export OPEN_ROUTER_API_KEY="sk-or-v1-..."

# 先跑前置检查
python3 preflight.py

# 再生成四格漫画（输出到项目外或指定目录）
python3 scripts/generate.py --mode comic \
  --input examples/scenes.json \
  --output ../书名_四格漫画.html
```

## 工作流

```
拆书数据 (角色/场景/金句)
    ↓ (LLM 编写 image_prompt)
增强数据 JSON (含 prompt 字段)
    ↓ (preflight.py 前置检查)
    ↓ (generate.py 调 API 出图)
AI 图像 base64
    ↓ (注入 HTML 模板)
单文件 HTML ← 最终交付物
```

## 目录结构

```
pop-shared-book-promo/
├── skill.json           ← Popwave 元数据
├── SKILL.md             ← 核心 skill 定义
├── README.md            ← 本文件
├── CHANGELOG.md         ← 变更日志
├── preflight.py         ← 前置检查
├── scripts/
│   ├── generate.py      ← 统一生成引擎
│   ├── autocheck.py     ← 自检脚本
│   ├── build_heroine_card.py
│   └── demo_from_title.py
├── templates/           ← 5 个 HTML 模板
├── examples/            ← 示例数据
└── skills/
    └── novel-ip-demo/   ← 快速演示子 skill
```

## 规范合规

本技能已对齐 `_SKILL_DESIGN_STANDARD.md` v1.0：

- ✅ skill.json 使用 popwave 标准格式（id + activation + permissions）
- ✅ SKILL.md 完整 frontmatter（dependencies + inject_context + produces）
- ✅ preflight.py 前置检查
- ✅ autocheck.py 自检脚本
- ✅ CHANGELOG.md 包含改动文件记录
