# 网文写作专家（expert-writer）

网文创作元 Skill（专家模式）。Agent 加载本 Skill 后自动识别创作意图、判断范围并路由到子 Skill。

## 📁 目录结构

```
expert-writer/
├── README.md        ← 你在这里
└── SKILL.md         ← 核心技能文件（管辖 Skill 清单 + 判断规则 + 修改路由 + 引导规则）
```

## 🚀 快速开始

### 这是什么

本 Skill 不直接产出内容，而是作为 Agent 的"操作系统"。加载后 Agent 会按以下逻辑工作：

1. **每轮判断：** 用户说的是创作/修改/质检吗？不是 → 自由回复。是 → 进入路由
2. **意图路由：** 新建？继续？修改？质检？调研？→ 自动选择最合适的子 Skill
3. **修改联动：** 改人物性格？自动联动更新角色设定。改剧情？自动联动更新幕纲和正文
4. **每轮引导：** 产出后问修改 + 建议下一步，推动用户沿创作管线前进

### 使用方式

在写作 Agent 的对话输入栏中选择「写作专家」模式，Agent 即开始按本 Skill 规则工作。

### 管辖的 Skill

| 类型 | 数量 | 说明 |
|------|------|------|
| 推荐 Skill（主场） | 10 个 | bootstrap · plot · opening-arc · writer · qa · continuation · deconstructor · reader-making · html-renderer · game |
| 延伸 Skill（可用） | 4 个 | cnovel-research · book-opinion-tracker · 01-download-webnovel-txt · knowledge-downloader |

## 核心设计

### 判断不靠记忆，靠项目状态

Agent 不靠"上一轮做了什么"来判断进度，而是读项目文件系统：有没有 bootstrap 产物？有没有 plot？写到第几章了？修改完成后自动重评估。

### 修改不推倒重来

改一个设定 ≠ 重写全书。按三步执行：定位改哪层 → 评估是否影响其他层 → 仅动受影响的层面。

### 每轮都引导

产出后必定先问修改 + 再建议下一步。引导是建议不是催促。

## 版本

v1.0.0 | 2026-06-04

> 与 PRD `06_专家模式PRD_v1.md` 配套，细节以 PRD 为准。
