# Step 1：读入 Canvas + 状态

> 管线: pop-novel-chapter-design v1.0

---

## 目的

读取上游 Plot 产出的全部 Canvas 文件 + 当前项目状态，建立本章设计基线。

---

## 前置条件

- [ ] act-XX.yaml 存在（含 characters_active / locations / info_release 等字段）
- [ ] act-XX-人物.md 存在
- [ ] act-XX-地图.md 存在
- [ ] info-release-XX.md 存在
- [ ] 里程碑设计.md 存在
- [ ] entity-snapshot.yaml 存在

---

## 执行

### 1. 读幕纲（act-XX.yaml）

定位本章的章级切片，提取：

| 字段 | 作用 |
|:-----|:-----|
| `chapters[].emotional_goal` | 本章情绪目标 |
| `chapters[].payoff` | 爽点类型、等级、触发方式 |
| `chapters[].end_hook` | 钩子设计 |
| `chapters[].plotlines_active` | 本章推进的情节线 |
| `chapters[].characters_active` | 本章可出场的角色（必须对齐） |
| `chapters[].locations` | 本章可用的地点（必须对齐） |
| `chapters[].info_release` | 本章应释放的设定信息（item_id/source_doc/release_method/priority/chapter_context） |
| `chapters[].milestone_active` | 本章对应的 MK |
| `chapters[].milestone_progress` | start/mid/complete |

### 2. 读 Canvas 文件

**人物** — `act-XX-人物.md`：
- 读取 `characters_active` 中列出的角色条目
- 记录每个角色的卷初→卷末状态、叙事功能、容易写崩的点

**地图** — `act-XX-地图.md`：
- 读取 `locations` 中列出的地点条目
- 记录每个地点的视觉印象、叙事功能、位置关系

**势力** — `act-XX-势力.md`（如有）：
- 读取各势力在当前章段的活动

### 3. 读里程碑和信息释放

- `里程碑设计.md`：确认本章 MK 的成就标准
- `info-release-XX.md`：确认本章 P0/P1 信息释放的具体内容和释放方式

### 4. 读项目状态

- `entity-snapshot.yaml`：所有角色的当前状态（**唯一 canon**）
- `03-正文/ch{上一章}.md` 末尾：上一章的未闭合节点 + 语感衔接
- `上一章 design 文件`：检查未闭合节点

### 5. 读宪法

- `constitution.yaml`：红线检查

---

## 产出

本章设计基线（内存，不落盘）：
- 本章在幕情绪弧线中的位置
- 本章的 info_release 清单（P0/P1，含 source_doc）
- 本章可用的角色池和地点池
- 所有角色的当前状态（from entity-snapshot）
- 上章未被闭合的节点
