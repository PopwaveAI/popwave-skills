# 故事弧文件模板

```markdown
---
name: "{弧名}"
type: {main / subplot / character / thematic}
status: {planning / in-progress / completed}
characters:
  - {character-kebab}
  - {character-kebab}
themes:
  - {theme-1}
  - {theme-2}
acts:
  - act-1
  - act-2
  - act-3
chapter-range:
  start: ch-001
  end: ch-025
---

# {弧名}

## 一句话定位

<!-- 这一弧的核心：主角要做什么 / 解决什么 -->

## Setup（开局状态）

<!-- 这一弧开始时的情境 -->
<!-- 主角面临什么 / 世界是什么状态 / 还没解决的问题是什么 -->

## Rising Action（铺垫升级）

<!-- 主角做出的尝试 / 遇到的升级阻碍 / 每一步付出的代价 -->
<!-- 这一段最长，是这一弧的主要篇幅（占 50-60%） -->

## Climax（高潮）

<!-- 这一弧的决定性时刻 -->
<!-- 主角必须做出关键抉择，抉择有不可逆的代价 -->
<!-- 高潮通常占 15-25% 篇幅，详细展开 -->

## Resolution（解决）

<!-- 解决方式（不一定是胜利） -->
<!-- 主角变成了什么样 -->
<!-- 给下一弧 / 下一卷留下了什么（伏笔、新格局、新问题） -->

## Plot Points（情节点表）

<!-- 章节级事件追踪。每个 plot point 对应卷级章纲里的一个章节 -->

| # | 事件 | 幕 | 章节 | 状态 |
|---|---|---|---|---|
| 1 | {事件} | Act 1 | Ch 1 | Planned |
| 2 | {事件} | Act 1 | Ch 2 | Planned |
| 3 | {事件} | Act 2 | Ch 3 | Written |
| 4 | {事件} | Act 2 | Ch 4 | Written |

## Foreshadowing（本弧伏笔）

<!-- 详细规范见 references/hook-ledger-spec.md -->

| ID | Plant | Payoff | Planted | Paid Off | Priority |
|---|---|---|---|---|---|
| H001 | 主角伤疤的来历不详 | 揭开是父亲的鞭痕 | Ch 1 | Ch 18 | core |
| H012 | 胖虎家里有秘密 | 揭开胖虎是间谍 | Ch 5 | Ch 15 | supporting |

## Chapter Outline（卷级章节大纲）

<!-- 可选：如果这一弧的所有章节大纲已经设计完，写在这里 -->
<!-- 也可以单独放在 plot/arcs/{arc}-chapters.md -->

### Ch 1：{标题}
- 时间：
- POV：
- 地点：
- 权重：⭐⭐⭐
- 危机来源：（首章可以是世界状态本身）
- 核心冲突：
- 主角抉择：
- 埋下隐患：
- 推进的 hook：
- 兑现的 hook：

### Ch 2：{标题}
- ...

## 主题对应

<!-- 这一弧服务哪些主题，怎么服务 -->

| 主题 | 通过什么情节 / 角色体现 |
|---|---|
| {主题-1} | {情节} |
| {主题-2} | {情节} |
```

## 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 弧名（描述性，可中可英）|
| `type` | ✅ | main / subplot / character / thematic |
| `status` | ✅ | planning（设计中）/ in-progress（边写边推）/ completed |
| `characters` | 推荐 | 涉及角色列表 |
| `themes` | 推荐 | 服务的主题列表 |
| `acts` | 可选 | 内部分幕 ID（仅当 type=main 时常用）|
| `chapter-range` | 推荐 | 这一弧对应的章节范围 |

## 不同 type 的写法侧重

- **main**：所有段都要详细。是全书骨干。
- **subplot**：可以省略详细的 Setup / Resolution，重点写 Rising Action 和 Climax。
- **character**：聚焦某个角色的成长，可以不严格按三幕结构，按角色弧线写。
- **thematic**：聚焦某个主题（如"权力的代价"），可以不严格依附时间线。
