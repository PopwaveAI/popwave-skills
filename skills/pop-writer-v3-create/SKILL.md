---
name: pop-writer-v3-create
description: 涌现写作创作子skill。v3.5：输入改为导演意图（从L2卡结构分析表提取），context隔离，在导演意图框架内自由涌现——网文风格基准+世界观卖点传递+场景流渲染+压力源逼近+章末钩子+主角行为一致性。不加载文风DNA（文风渲染由revise负责）。
pipeline:
  upstream: [expert-writer]
  downstream: [pop-writer-v3-revise]
version: 1.5.0
---

# 创作子skill

> 由 expert-writer Step 3 调度，context隔离。

v3.5涌现写作管线的创作子skill。专注故事结构层：在导演意图框架内自由涌现——**网文风格基准（直接易懂、世界观卖点前置）**+场景流渲染+压力源逼近+章末钩子+主角行为一致性。导演意图说"这章要达到什么效果"，create决定"怎么写"。不做文风对齐（→修订层）、不做8020比例（→修订层）、不做AI观感词清理（→修订层）。文风从创作端拆出到修订层，创作子skill只管故事涌现。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 必须在导演意图框架内创作——叙事功能/事件链/情绪曲线/章末钩子必须覆盖 | 创作前确认导演意图已加载，创作后逐项核对覆盖 |
| ❌2 | 不加载文风DNA（文风渲染由revise负责） | 注入项白名单不含style_dna |
| ❌3 | 仅可更新L2卡的"本章聚焦"相关内容（如有微调），不得修改L2卡结构分析表/嵌套子线/物理坐标 | 写入权限白名单 |
| ❌4 | 正文≥2500字（下限门禁） | 字数统计（不含markdown标记） |
| ❌5 | 网文风格基准必须满足——直接易懂、事件推进不拖拉、世界观卖点按导演意图传递 | 创作后对照网文风格基准自检4问 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-create.md | 涌现写作（导演意图框架内场景流+压力源+钩子+行为一致性检查+context receipt预留） |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 创作执行 | `references/创作指南.md` | 场景流渲染+压力源逼近+章末钩子+主角行为一致性检查 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 创作产出 | `templates/创作-模板.md` | 上下文确认表+正文涌现结构+创作决策记录YAML+门禁表+context receipt预留格式 |

## 输入/输出契约

### 输入

> v3.5 取消种子文档。create 的输入从"种子文档全文"改为导演意图+状态快照+设定文件。种子文档原功能被 L2卡+写作参考吸收。

| 输入项 | 来源 | 内容 | 必须/可选 |
|:-------|:-----|:-----|:---------|
| 导演意图（director_intent） | L2卡结构分析表本章行（主会话Step0提取） | 叙事功能/事件链/情感曲线/节奏/子线推进/章末钩子/三问/设定引用 | 必须 |
| 状态快照（state_snapshot） | 活记忆+L2卡物理坐标投影（主会话Step1产出） | 主角当前状态/压力仪表盘/未了事项（≤400字） | 必须 |
| 上章末尾（prev_chapter_tail） | 正文/chXXX.md末尾1200字 | 语感衔接+悬念承接 | 必须（首章除外） |
| 设定文件（settings_ref） | L2卡设定引用指针指向的文件（主会话Step2强制读取后注入） | 主角引擎/金手指/压力矩阵等设定内容 | 必须（指针指向的全读） |
| info_acquired | 写作参考/知识沉淀/（主会话Step2按需获取） | 增量信息（制度细节/场景技法/伏笔回收线索） | 可选 |
| L2卡（l2_card） | 卷纲/L2-NNN.md | 整体参考（结构分析表/嵌套子线/物理坐标） | 可选 |
| 创作模板 | templates/创作-模板.md | 正文涌现结构+创作决策记录格式 | 必须 |

**禁止注入的内容：** 文风DNA（style_dna）——文风渲染由revise负责（红线❌2）。主会话历史、Step0-2的执行过程。

### 输出

| 输出项 | 格式 | 传递给 |
|:-------|:-----|:-------|
| 正文初稿 | markdown | expert-writer主会话→调度revise |
| 创作决策记录 | YAML | expert-writer主会话→Step4 receipt检查 |
| context receipt | YAML | expert-writer主会话→Step4 receipt检查（批次1预留格式，批次2完整实现） |
| L2卡本章聚焦微调记录（如有） | YAML（并入创作决策记录） | expert-writer主会话→Step5；同步回写L2卡 |

## L2卡写入权限

create在涌现写作过程中，仅可更新L2卡中与"本章聚焦"相关的内容（如导演意图对应的结构分析表本章行微调）。不得修改L2卡结构分析表其他行、嵌套子线、物理坐标（红线❌3）。

| L2卡段 | create权限 | 维护者 |
|:-----------|:-----------|:-------|
| 结构分析表本章行（导演意图来源） | 可微调（如事件brief与实际偏差） | plot设计（初版）+ create（写作中微调本章行）+ arc（单元结束时更新） |
| 结构分析表其他行 | 只读 | plot设计 |
| 嵌套子线 | 只读 | plot设计 + arc更新 |
| 物理坐标 | 只读 | plot设计 + arc更新 |
| 子线咬合 | 只读 | plot设计 + arc更新 |

## context receipt 预留（批次2完整实现）

create产出时附带 context receipt，确认实际接收了哪些注入项。主会话产出 manifest 声明注入了什么，create产出 receipt 确认实际接收了什么，主会话Step4对照检查一致性。

本次（批次1）先预留格式说明，批次2完整实现receipt产出与一致性检查。

receipt格式：

```yaml
context_receipt:
  chapter: {章号}
  manifest_id: "{主会话manifest ID}"
  received:
    - item: "director_intent"
      status: "full" | "partial" | "missing"
      actual_read: "{实际读取字数}"
      key_elements_confirmed: ["narrative_function", "event_chain", "emotion_curve", "chapter_hook"]
    - item: "state_snapshot"
      status: "full" | "partial" | "missing"
      actual_read: "{实际读取字数}"
    - item: "prev_chapter_tail"
      status: "full" | "partial" | "missing"
      actual_read: "{实际读取字数}"
    - item: "settings_ref"
      status: "full" | "partial" | "missing"
      files_read: ["{实际读取的设定文件路径列表}"]
    - item: "info_acquired"
      status: "full" | "partial" | "missing" | "not_applicable"
    - item: "l2_card"
      status: "full" | "partial" | "missing" | "not_applicable"
  excluded:
    - item: "style_dna"
      status: "excluded_by_design"
      reason: "文风渲染由revise负责（红线❌2）"
  anomalies: []
```

## 路由

upstream `expert-writer`（调度器，Step 3组装精简context调用本skill） → **本skill** → downstream `pop-writer-v3-revise`（修订子skill，接收正文初稿）

**调度架构：** 本skill由expert-writer主会话Step 3调用，context隔离——只接收精简context，不接收会话历史。创作完成后返回正文初稿+创作决策记录+context receipt给expert-writer主会话，由主会话Step4进行receipt检查+导演意图验证，然后调度revise。

---

v1.0.0 | 2026-06-26 | 从pop-writer-v3-emerge v1.2.0拆分出创作子skill；新增主角行为一致性检查（红线❌2）；context隔离红线（红线❌1）
v1.1.0 | 2026-06-27 | v3.4：输入context从场景list改为任务list（释放涌现空间）；新增字数下限门禁；upstream改为expert-writer
v1.2.0 | 2026-06-27 | v3.5批次1预备：输入适配为种子文档.md（统一活文档，含任务表+要素切片+本章聚焦）；新增种子文档本章聚焦写入权限
v1.3.0 | 2026-06-28 | v3.5正式：种子文档取消，输入改为导演意图（从L2卡结构分析表提取）+状态快照+设定文件（指针强制读取后注入）；涌现写作在导演意图框架内；不加载文风DNA；新增context receipt格式预留；L2卡本章聚焦写入权限；红线更新为4条
v1.4.0 | 2026-06-28 | 新增网文风格基准红线（❌5）；创作指南新增「网文风格基准」章节（零号章节，最高优先级）+世界观卖点传递机制+章末收束纪律；导演意图从三问扩展为五问（新增worldview+clarity）
