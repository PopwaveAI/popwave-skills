---
name: pop-novel-character-schema
description: 角色卡分级标准定义（Lv1~Lv4）。统一角色模板供写作管线消费。可独立触发用户设计角色储备。跨赛道复用。
pipeline:
  upstream: [pop-novel-bookstrap, pop-novel-plot, pop-novel-chapter-design, pop-novel-prose-render]
  downstream: []
---

# 角色分级模板

> 定位：**标准定义 Skill** — 不执行具体角色设计流程，只定义角色卡的格式标准、分级体系和字段规范。
> 对标：pop-dna（轻量、不注册全管线、作为 reference 被其他 skill 消费）

---

## 一、定位与使用方式

### 当它被路由调用时（自主触发）

用户说"帮我设计几个角色储备"、"创建一批角色"、"设计一个配角" → expert-writer 路由到此 skill → 本 skill 按分级标准引导用户创建角色卡，产出到 `设计/角色层/`。

### 当它被其他 skill 引用时（被动消费）

bookstrap/plot/chapter-design 在产角色卡时，**推荐先加载本 skill 的 schema 模板**，按对应级别标准填写。不强制，但不加载可能导致角色卡颗粒度不足。

**加载方式参考**：
```
Get-Content -Path '{skill_path}/schema/Lv1-core.md' -Encoding UTF8 -Raw
Get-Content -Path '{skill_path}/schema/Lv2-important.md' -Encoding UTF8 -Raw
Get-Content -Path '{skill_path}/references/character-arc.md' -Encoding UTF8 -Raw
```

### 消费方产出物归属

| 消费 Skill | 产出位置 | 使用级别 |
|:----------|:---------|:---------|
| bookstrap (Phase 3) | `设计/角色层/{角色名}-主角卡.md` | Lv1 |
| plot | `设计/角色层/{角色名}-{定位}.md` | Lv2/Lv3 |
| chapter-design | 登场人物卡（临时，不独立存档） | Lv3/Lv4 |
| 本 skill 独立触发 | `设计/角色层/{角色名}-{定位}.md` | Lv1~Lv4 |

---

## 二、分级体系总览

```
Lv1 ─ 主角/核心对立 ──── 6 维全量 ──── 贯穿全文的灵魂
  ├─ 身份（Identity）
  ├─ 心理（Psychology）
  ├─ 驱力（Drive）
  ├─ 能力（Capability）
  ├─ 演化（Evolution）
  └─ 网络（Network）

Lv2 ─ 重要配角 ──────── 4 维 ──────── 有自己的弧线，跨幕存在
  ├─ 身份
  ├─ 心理/驱力
  ├─ 叙事功能
  └─ 弧线

Lv3 ─ 功能角色 ──────── 3 维 ──────── 为特定叙事功能服务，出现 1-3 幕
  ├─ 身份
  ├─ 标签
  └─ 驱动/功能

Lv4 ─ 一次性角色 ────── 1 维 ──────── 路人/背景板，一句话概括
  └─ 一句话摘要
```

### 选择指南

| 该角色 | 用级别 |
|:-------|:------|
| 是故事的主角 | Lv1 |
| 是主要反派/最终对手 | Lv1 |
| 是主角最亲密的伙伴/恋人/宿敌 | Lv2 |
| 贯穿 2+ 幕且有独立动机 | Lv2 |
| 为特定事件出现，完成后不再有独立弧线 | Lv3 |
| 只出现 1 个场景，作用是传递信息/营造氛围 | Lv4 |

### 降级与升级规则

- **没想清楚** → 先按当前级别写，后续可升级补全（Lv3 → Lv2 需补弧线维）
- **写着写着发现重要了** → 升级后补全缺失维度的回溯填写（不重写已有信息）
- **降级几乎不发生** — 如果角色已有多维信息，降级没有意义

---

## 三、跨赛道复用说明

本 skill 的模板使用**通用写作术语**，不绑定任何题材特定概念：

- Lv1 通用动词模板可用：`Lv1-core.md`
- 如需题材特定字段（如 网文的"境界/修为"、西幻的"职业/神性"、科幻的"改造/植入体"），由消费方 skill 自行在 `能力` 维度的子字段中按需扩展
- **不改模板本身** — 模板只保留跨赛道通用字段

---

## 四、版本

v1.0.0 | 2026-06-10 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
