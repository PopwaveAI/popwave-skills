# Phase 2.3：剧情架构模板提取（Lv2）

> 对齐写作端：08-pop-novel-plot Step 0~2 → `设计/全书架构.md` + `设计/卷/volume-01.md` + `设计/幕/vol-01/act-01.yaml`
> 使用模板：`templates/volume-design.tpl.md` + `templates/act-skeleton.tpl.yaml`
> 前置条件：Phase 2.1 + Phase 2.2 已完成


## 🔧 数据提取前置命令（硬性！先执行再写产出）

剧情架构需要从 ch1-100 中提取章节事件链、卷幕边界、支线线索。

### 第一步：执行章节索引提取（ch1-100 标题/首句/类型标签）
```powershell
python "..\_scripts\extract.py" index "{$TXT_FILE_PATH}" ".\_temp\"
```
输出：`_temp/chapter-index.json`

### 第二步：手动提取剧情数据（写入 `_temp/plot-data.json`）

读完 ch1-100 后，手动提取以下数据：

| 字段 | 提取什么 | 方法 |
|:-----|:---------|:-----|
| `actBoundaries[]` | 每幕起止章号 + 判断依据 | 按情绪曲线找低谷→高潮边界 |
| `majorEvents[]` | 每章的核心事件（<=20字） | 逐章阅读提炼 |
| `chekhovGuns[]` | 伏笔/未回收线索 + 设伏章 | 通读标记 |
| `tensionCurve[]` | 每章情绪值 1-10 + 类型(动作/文戏/过渡) | 阅读判断 |

### 规则
1. **卷边界必须有原文证据**：卷末高潮事件 + 后续新章有明显时空跳跃
2. **主要事件不能跳过**：每章至少记录一个核心事件
3. **契诃夫枪链中每个条目必须标注设伏 chXX**
4. 写一半发现缺数据 → 返回读原文对应章 → 补录到 plot-data.json → 再写

---

## 速查表
|:-----|:-----|:-------|:-----|:-----|
| 1 | 全书架构 | 全书章节分布 | `设计/全书架构.md`（卷拆分+主线全览） | ❌ 缺卷拆分退回 |
| 2 | 卷1设计 | 卷1逐章 | `设计/卷/volume-01.md`（核心命题+剧情线+快照） | ❌ 缺剧情线退回 |
| 3 | 幕1编排 | 幕1逐章 | `设计/幕/vol-01/act-01.yaml`（Canvas矩阵+情绪+钩子+节奏自检） | ❌ canvas空白退回 |


## 产出结构

```
设计/
├── 全书架构.md                ← 按 plot step-0-architecture.md 格式（卷拆分+地理全景+角色出场+主线全览）
├── 卷/volume-01.md            ← 按 templates/volume-design.tpl.md（5区段）
└── 幕/vol-01/
    ├── act-01.yaml            ← 按 templates/act-skeleton.tpl.yaml（完整Canvas矩阵+rhythm_check+首卷黄金窗口）
    └── chekhov-tracker.yaml   ← 契诃夫枪链（每条线的设伏→回收）
```

## 格式规则

- **全书架构 .md** — 卷拆分/地理全图/角色出场节奏/主线全览/卷间钩子
- **volume-01 .md** — 按 `templates/volume-design.tpl.md` 5区段：〇全书隶属/一/卷级定义/二/快照/三/背景/四/剧情线/五/设定披露线
- **act-01 .yaml** — 按 `templates/act-skeleton.tpl.yaml` 完整骨架（含所有21字段/章）

## 提取方法

### 卷边界识别
```
M1（世界危机）密度 + M2（主角成长）密度 → 确定 Act 边界
每章标注哪些线推进 → 识别卷的起止
卷末特征：高潮+情绪释放+新悬念建立
```

### Canvas 矩阵填写
```
逐章反推：
  - 主线1（世界危机）：本章推进了什么 → payoff_level
  - 主线2（主角成长）：本章推进了什么 → payoff_level  
  - 主线3（主角行动）：本章推进了什么 → payoff_level
  - 支线1/2：本章推进了什么 → payoff_level
  - 设线负载：本章释放了什么新设定
```

## 落盘检查点

| 路径 | 状态 |
|:-----|:-----|
| `设计/全书架构.md` | [ ] |
| `设计/卷/volume-01.md` | [ ] |
| `设计/幕/vol-01/act-01.yaml` | [ ] |
| `设计/幕/vol-01/chekhov-tracker.yaml` | [ ] |


## 下一步

完成 → 进入 Phase 2.4 (decon-characters)
