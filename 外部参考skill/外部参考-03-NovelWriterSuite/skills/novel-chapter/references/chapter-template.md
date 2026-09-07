# 章节文件模板

```markdown
---
chapter: {N}
title: "{章节标题}"
pov: {character-kebab}
location: {primary-location-kebab}
arc: {arc-kebab}
weight: ⭐⭐⭐  # 节奏权重：⭐ 过渡 / ⭐⭐ 铺垫 / ⭐⭐⭐ 转折 / ⭐⭐⭐⭐ 高潮前奏 / ⭐⭐⭐⭐⭐ 大高潮
word-count: 0  # write 后由 self_check 填
word-target: 3000-4000
status: outlined  # outlined / outline-confirmed / written / needs-manual-fix / reviewed
created: {YYYY-MM-DD}
appeared:  # write 后由 memory_update 填
  - {character-kebab}
locations-used:  # 本章涉及的地点
  - {location-kebab}
systems-invoked:  # 本章涉及的力量体系动作
  - {system-kebab}
---

## 本章章纲

- **时间**：
- **危机来源**：
- **核心冲突**：
- **主角抉择**：
- **抉择代价**：
- **埋下隐患**：
- **预定场景**：
  1. {场景 1}（约 X 字）
  2. {场景 2}（约 X 字）
  3. {场景 3}（约 X 字）

## hook-账（预定）

### open（本章新埋）
- [new] {hook description}

### advance（本章推进）
- H001 {description}

### resolve（本章回收）
- H007 {description}

### defer（本章暂搁）
- H003 {description} - 原因：{...}

---

## 正文

<!-- write 步骤填充。保留 章纲 + hook-账 在前，正文在 --- 后 -->
<!-- 直接是小说正文，无任何 markdown 标题 -->

{章节正文}

## hook-账（实际）

<!-- write 后的真实操作，可能跟预定不同。memory_update 以此为准 -->

### open
- ...

### advance
- ...

### resolve
- ...

### defer
- ...
```

## 字段说明

### frontmatter

| 字段 | 必填 | 说明 |
|---|---|---|
| `chapter` | ✅ | 全书章节号（不分卷） |
| `title` | ✅ | 章节标题 |
| `pov` | ✅ | POV 角色的 kebab-id |
| `location` | ✅ | 本章主要地点 |
| `arc` | ✅ | 所属故事弧 |
| `weight` | ✅ | 节奏权重（详见 pacing-principles.md） |
| `word-count` | 自动 | 由 self_check 计算填入 |
| `word-target` | 推荐 | 字数目标范围 |
| `status` | ✅ | 当前状态 |
| `appeared` | 自动 | memory_update 自动维护 |

### 章纲段

- **本章章纲** 在 user_confirm 阶段必须填完整
- **hook-账（预定）** 是 outline 阶段写的预期
- **hook-账（实际）** 是 write 完成后的实际，可能跟预定有出入
- `memory_update` 以"实际"为准更新全书 hook ledger

## 多卷小说的命名

- 跨卷连续编号：`ch-001.md` 到 `ch-NNN.md`（推荐，简单）
- 按卷分子目录：`chapters/vol-1/ch-001.md`（适合超长篇）

v0.1 推荐第一种。

## 写作字数控制

| 题材 | 推荐每章字数 |
|---|---|
| 网文（玄幻/都市/修真） | 3000-4000 字 |
| 传统小说 | 不限，但单章 6000+ 字读者疲劳 |
| 短篇集 | 1000-2000 字 / 短篇 |

word-target 字段决定 writer 的字数控制，self_check 会检测越界。
