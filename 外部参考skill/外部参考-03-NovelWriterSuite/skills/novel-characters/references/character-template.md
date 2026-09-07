# 角色文件模板

```markdown
---
name: "{角色名}"
role: {protagonist / antagonist / supporting / minor / cameo}
age: {年龄}
gender: {男 / 女 / 其他 / 不详}
status: {alive / dead / unknown / missing / sealed}
aliases:
  - "{别名 1}"
  - "{别名 2}"
relationships:
  - character: {kebab-id}
    type: {sibling / parent / child / mentor / rival / enemy / lover / friend / ...}
linked-locations:
  - {location-kebab}
practices:
  - {system-kebab}
arc: {名}
tags:
  - {tag}
# 动态角色状态（v0.2+）
# volume-N:
#   responsibility: "..."
#   absence-risk: low / med / high
#   appearance-target: N
---

# {角色名}

## 外貌

<!-- 3-5 个能让读者"一眼记住"的特征，不是面孔素描 -->
<!-- 例：身高、伤疤、独特服饰、明显年龄痕迹、口头禅 -->

## 性格与缺陷

<!-- 不写"善良勇敢"——写矛盾感 -->
<!-- 必须包含：1 个明确的强项 + 1 个会被这个强项害到的弱点 -->

**强项**: {一段}
**弱点**: {一段，跟强项有逻辑关联}
**典型行为模式**: {遇到 X 情境会做 Y}

## 背景

<!-- 只写跟主线相关的部分 -->
<!-- 关键节点：出生 / 主要变故 / 现在为什么是这样 -->

## 动机与目标

**外在目标（想要什么）**: 

**内在需要（实际缺少什么）**: 
<!-- 通常跟外在目标矛盾——这是角色成长弧的引擎 -->

**核心恐惧**: 

**道德盲点**: 
<!-- 自己不愿承认的弱点 -->

## 声音与说话方式

**句长偏好**: {短句 / 长句 / 长短交替}
**用词风格**: {正式 / 口语 / 文言 / 方言 / 带梗 / 粗鲁}
**沉默时机**: {什么时候不说话}

**典型对话**（≥ 2 句）：

> "{第一句}"

> "{第二句}"

## 角色弧线

**起点（开场状态）**: 
**中点（转折点）**: 
**终点（结尾状态）**: 

## 关键时间线

| 时间 | 事件 | 章节 |
|---|---|---|
| {时间} | {事件} | {章节号或 Backstory} |

## 注意点

<!-- 写本角色时容易出错的点（比如"他不会主动说出自己的心情"或"他从不带武器"） -->
```

## 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 完整角色名 |
| `role` | ✅ | 主要定位 |
| `age` | 推荐 | 数字或"约 30 / 未知 / 永恒" |
| `status` | ✅ | 当前生死 / 状态 |
| `aliases` | 可选 | 别名 / 称号 / 化名 |
| `relationships` | 可选 | 与其他角色的关系，必须双向维护 |
| `linked-locations` | 可选 | 跟角色绑定的地点 |
| `practices` | 可选 | 修炼 / 使用的力量体系 |
| `arc` | 可选 | 所属故事弧（对应 plot/arcs/{arc}.md）|

## 角色定位的字数建议

| role | 角色卡建议长度 |
|---|---|
| protagonist | 详尽，全部段落填满 |
| antagonist | 详尽，但 **动机 / 道德盲点** 段要特别下功夫（反派立不立得住关键看这里）|
| supporting | 中等，可省略 backstory 细节 |
| minor | 精简，重点写 voice + 1-2 个识别特征 |
| cameo | 极简，可只填 frontmatter + voice + 1 句典型对话 |
