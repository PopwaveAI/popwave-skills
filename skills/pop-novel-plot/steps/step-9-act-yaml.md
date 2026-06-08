# Step 9：幕纲设计 · 填 act-XX.yaml

> 所属管线: pop-novel-plot v4.1+
> 模板: `templates/act-guide.md`

---

## 目的

Canvas 已就绪（人物/地图/势力/信息释放），现在编排每章的具体设计。

act-XX.yaml = 一卷大纲的**章级编排层**。每章以 emotional_goal + payoff 为第一性。

---

## 前置条件

开始填 act-XX.yaml 前，确认以下文件存在并已阅读：

- [ ] `设计/幕/act-XX-人物.md` — 知道本卷有哪些角色、各自在哪些章出场
- [ ] `设计/幕/act-XX-地图.md` — 知道本卷的关键地点和移动线路
- [ ] `设计/幕/act-XX-势力.md` — 知道势力在各章的动态
- [ ] `设计/幕/info-release-XX.md` — 知道 P0/P1 信息点的章级分配
- [ ] `设计/幕/情节线草案-XX.md` — 知道线定义和交叉节奏
- [ ] `设计/里程碑设计.md` — 知道 MK-01~MK-N 的章节段

---

## 执行

按 `templates/act-guide.md` 完整填写指南逐项填写，产出 YAML 文件。

### 幕级定义必须包含

1. `core_conflict` — 本幕核心冲突
2. `goal` + `tone_note` — 幕级目标与基调
3. `act_end_state` — 卷末状态预期（主角+世界）
4. `equipment_flow` — 装备/资源变化表（结构化）
5. `payoff_distribution` — 爽点四级分布
6. `emotional_arc` — 情绪弧线关键转折点（4-6个）
7. `plotlines` — 情节线定义（M1/M2/M3 必选+S线可选）

### 每个章级切片必须包含

**基础**：
- ch / title / word_count

**情绪**：
- emotional_goal / payoff(type+trigger+reader_feeling) / reader_emotion_path

**钩子**：
- end_hook(type+drive+content)

**情节线**：
- plotlines_active / chekhov_set / chekhov_fire

**里程碑**：
- milestone_active / milestone_progress

**信息释放**：
- info_release[](item_id+title+source_doc+release_method+density+priority+chapter_context)

**Canvas 消费**（★ NEW v4.1）：
- `characters_active` — 本章登场角色（从 act-XX-人物.md 选取）
- `locations` — 本章发生地点（从 act-XX-地图.md 选取）

### YAML 示例

参考 `templates/act-guide.md` 第 6.2 节的完整示例。

---

## 红线

- ❌ 铁律：幕内不允许连续 3 章同一情绪叠加组合
- ❌ `characters_active` 中的角色必须在 act-XX-人物.md 中存在
- ❌ `locations` 中的地点必须在 act-XX-地图.md 中存在
- ❌ 第 1 章 info_release 数量 > 2 → 退回
- ❌ 连续 2 章无 info_release，第 3 章未追加 → 退回
- ❌ end_hook 与下一章 emotional_goal 不衔接 → 标记警告

---

## 引用

- 模板: `templates/act-guide.md`
