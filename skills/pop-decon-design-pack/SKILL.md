---
name: pop-decon-design-pack
description: "Phase 1 of deconstruction: ETL → chapter splitting → 5-ch batch LLM extracting full chapter design packs (events + worldbuilding + items + entities + key info + emotional beats + hooks). Supports Chinese web novels via manual ETL reference."
version: 2.0.0
author: Popwave
license: MIT
metadata:
  hermes:
    tags: [deconstruction, design-pack, etl, novel-analysis]
    related_skills: [pop-decon, pop-decon-volume, pop-decon-setting]
---

# pop-decon-design-pack · 章节设计包 v2.0.0

> **定位：Phase 1 of deconstruction. 提取原文事件信息，产出设计包。支持两种格式：**
> - **v2 格式（5章合一 YAML）** — 传统批量输出，适合 volume/setting 消费，效率高
> - **v3 格式（单章独立 Markdown）** — 高精度逐章PRD，含4层结构（骨架+爽点+角色+感官），适合 prose-render 直接消费
> 
> **核心约束：ETL 硬性前置。格式选型规则：下游需要 precision 选 v3，需要 coverage 选 v2。**

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **ETL 未执行就写设计包** — extract.py 没跑，full_text.txt 不存在 → 退回 |
| ❌2 | **跳步拆分** — 全本 txt 没按章切 → 退回先拆分 |
| ❌3 | **凭空发明事件** — 事件链中出现了原文不存在的条目 |
| ❌4 | **5章一批覆盖不全** — 批内读了 5 章但 events 覆盖不足 5 章 → 退回 |
| ❌5 | **evidence 空** — 事件/设定/物品/人物每条必须有原文引用，null 不退库 |
| ❌6 | **设定信息蒸发** — 章内有设定/物品/重要对话释放但未提取到对应区块 |
| ❌7 | **章型误判** — 混合章型放宽检查；单章型"战斗"中交锋占比< 60% → 退回 |
| ❌8 | **广告未去** — 设计包事件中混入非正文内容 → 退回 |
| ❌9 | **产出只留摘要** — 写入后只说「已产出 {N} 份设计包。事件{M}+设定{P}+物品{Q}项」|
| ❌10 | **中文网文硬跑 extract.py** — extract.py 的章节检测只支持英文"Chapter N"和罗马数字。中文「第X章」格式必须走手动 ETL（见 `references/chinese-novel-etl.md`）|
| ❌11 | **事件缺少精度锚点字段** — 事件链中每个事件缺少 scene/POV/关键对白/感官锚点 四个字段 → prose-render 无锚点指引时会在自身语言模型中补全细节，产生"看起来合理但错了"的输出（如编造不存在的专长名和属性增益）。见 `references/precision-anchor-format.md` |
| ❌12 | **v3格式跳过4层结构** — v3格式必须包含全部4层（骨架+爽点+角色+感官），缺一层视为格式不完整 → 退回重写 |

---

## 速查表

| 步骤 | 操作 | 读什么 | 产出 | 门禁 |
|:-----|:-----|:-------|:-----|:-----|
| 1 | ETL + 拆分 | TXT/EPUB → extract.py（中文 TXT 走手动 ETL） | `_temp/chapters/ch001.txt ... chNNN.txt` | ❌ 章数不匹配退回 |
| 2a | **v2批量: 5章一批 LLM**（适合 volume/setting 消费） | 每批 ch{N~M}.txt | `写作资产/设计包v2/设计包-ch{start}-{end}.md` | ❌ 质检门禁全过才进下一批 |
| 2b | **v3单章: 逐章 LLM**（适合 prose-render 直接消费） | 单章 chXXX.txt | `写作资产/设计包v3/chXXX-设计包.md` | ❌ 4层结构完整、每事件有精度锚点 |
| 3 | 验证 | 设计包目录 | 验证报告 | ❌ 缺失设计包退回 |

> **⚠️ 核心警告：Step 2 是整条拆书管线的质量瓶颈。** 设计包质量决定 volume（Phase 2）和 setting（Phase 3）的全部产出。
>
> **⚠️ 中文重要提示：** extract.py 的 `detect_structure()` 只识别英文"Chapter N"和罗马数字，**不识别中文「第X章」**。中文网文 TXT 必须跳过 extract.py，参考 `references/chinese-novel-etl.md` 手动 ETL。

---

## 核心流程

### Step 1: ETL + 按章拆分
详见 `steps/step-1-etl-split.md`

**读什么：** TXT/EPUB 原文文件
**做什么：** 运行 extract.py → 按章正则拆分到 `_temp/chapters/chXXX.txt`
**中文 TXT 替代：** extract.py 不支持中文章节检测，需手动 ETL。参考 `references/chinese-novel-etl.md`

**产出：** `_temp/metadata.json` + `_temp/full_text.txt` + `_temp/chapters/ch001.txt ~ chNNN.txt`
**❌ 门禁：** 拆分后的文件数与 metadata.json 检测到的章节数不匹配 → 退回。

### Step 2a: 5章一批 LLM 提取设计包（v2 格式 — 批量模式）
详见 `steps/step-2-batch-process.md`

**读什么：** 按批读取 5 个章节文件（最后一批可能不足 5 章）
**做什么：** 一次 LLM 调用，完成：
1. 去广告/导航/版权声明
2. 提取每章 3-15 个原子事件（依章型，标注类型 + 参与角色 + 原文证据）
3. 聚合跨 5 章的智慧实体状态轨迹、设定信息、物品变化
4. 写入 1 份 5 章合一设计包

**批对齐规则：** ch1-5, ch6-10, ch11-15 … 固定窗口，不跨卷对齐。
**产出：** `写作资产/设计包v2/设计包-ch{start}-{end}.md`
**❌ 门禁：** 质检未通过 → 退回该批重跑。
**格式规范：** 见 `产出格式（v2 版 — 5章合一）`

### Step 2b: 逐章 LLM 提取设计包（v3 格式 — 精度模式）
详见 `references/设计包v3-格式规范.md`

**读什么：** 单章 chXXX.txt
**做什么：** 一次 LLM 调用，产出单章 v3 格式设计包（4层结构）：
1. L1 骨架层：事件链（8-12事件，含字数预算/POV/原文证据）
2. L2 爽点层：套路识别+情绪弧线+钩子强度+爽点机制
3. L3 角色层：人格特质触发+关键对白+潜台词+关系变化
4. L4 感官层：环境基线6维+动作六段式+氛围渲染要点+DNA衔接映射

**特点：**
- 单章独立，精度优先，每章5-8分钟 LLM 调用
- 标记维"事件不可替换的关键对白/数据"（prose-render 不可编造）
- 文风DNA对接：每章标注 DNA 维度→本章需求的映射
- **套路提取：每章产出时同步提取套路归档，写入写作资产/套路库/{套路名}.md**

**产出：** `写作资产/设计包v3/chXXX-设计包.md`
**产出命名强制规则：** 文件名必须为 `ch{三位数}-设计包.md` 格式（如 `ch001-设计包.md`, `ch020-设计包.md`）。严禁以下变体：
- ❌ `chXXX_v3设计包.md`（下划线）
- ❌ `chXXX-v3设计包.md`（-v3后缀）
- ❌ `v3_设计包_chXXX-chYYY.md`（批次名）
- ❌ `chXXX-设计包.md`（无三位数补零）
多批次并行时，**每批次内部的 delegate_task 指令中必须写明产出文件名的精确格式**，不能依赖子 agent 自行推断命名规则。
**❌ 门禁：** 4层结构缺一 → 退回重写。每事件至少有精度锚点字段 → 缺则退回。
**套路归档门禁：** 每章至少提取1个套路并更新 `套路库/` → 未执行退回。
**⚠️ 命名归一化（delegate_task 批量提取后强制）：** 使用 `delegate_task` 并行提取时，不同子agent可能采用不同命名约定（如 `chXXX_v3设计包.md`、`chXXX-v3设计包.md`、`v3_设计包_chXX-chYY.md`）。批量完成后必须扫描目录并将全部文件统一为 `chXXX-设计包.md`。违反 → 退回。
**格式规范：** 详见 `references/设计包v3-格式规范.md`

### Step 3: 验证
详见 `steps/step-3-verify.md`

**做什么：** 对比 `_temp/chapters/` 和 `写作资产/设计包v2/`（或 `设计包v3/`）的文件数，确保全覆盖。

**v3 批量一致性验证（新增）：** 对于通过 delegate_task 并行提取的 v3 设计包，在全部批完成后额外执行一次全量验证：

| # | 检查项 | 通过标准 | 失败处理 |
|:-:|:-------|:---------|:---------|
| 1 | **命名一致性** | 全部文件名为 `chXXX-设计包.md` 格式（无 `-v3`/`_v3`/`v3_` 变体、无批次名） | 统一重命名 |
| 2 | **首行格式** | 全部文件首行匹配 `# 设计包 — chXXX「` 模式 | 标记差异文件 |
| 3 | **4层结构完整** | 全部文件包含「## 1. 事件链」「## 2. 爽点设计」「## 3. 角色与人设」「## 4. 感官与画面」四个小节 | 标记缺层文件 |
| 4 | **事件数下限** | 晚期批次（后30%）每章事件数 ≥5 | <5 的文件标注低密度警告 |
| 5 | **覆盖率** | 设计包文件数 = 章节文件数 | 缺文件退回补充 |

**验证通过后** 通知 orchestrator（pop-decon）Phase 1 完成，可进 Phase 2。

**❌ 门禁：** 设计包文件数 < 章节文件数 → 退回 Step 2。

---

## 产出格式（v2 版 — 5章合一）

| 区块 | 内容 | 下游消费 |
|:-----|:-----|:---------|
| **智慧实体** | 跨5章状态轨迹（等级/位置/心理/性格标记），不限人类 | character + volume |
| **事件链** | 按章独立，每章3-15事件（依章型），每个含类型/内容/证据/地点/参与角色。**v2 标准另加4个精度锚点字段**：scene（映射DNA场景卡值）、POV（感知锚点角色）、关键对白/数据（不可替换的原文）、感官锚点（感觉信号）。完整格式见 `references/precision-anchor-format.md` | volume 剧情线聚类 + prose-render 精度指引 |
| **设定提取** | 按主题聚合的本批世界观信息，每项标注来源章号和原文证据 | setting 世界观归纳 |
| **物品一览** | 本批出现的物品及变化，含重要性星级 | setting 物品 + volume 关键道具 |
| **地点一览** | 本批场景及功能描述 | volume + setting |
| **重要信息/对话** | 核心信息释放——台词/笔记/系统提示，标注来源和重要性 | plot 信息节点 |
| **情绪节拍** | 按章分录的起点→推进→高潮→终点 | plot 情绪弧线 + writing 参考 |
| **钩子** | 每章末的悬念/信息/情绪钩子（原文就有，不设计） | plot 钩子追踪 |
| **批次衔接** | 上一批末尾与本批起始的衔接 | volume 情节连续性验证 |

---

## 落盘检查点

| 确认项 | 状态 |
|:-------|:----:|
| `_temp/chapters/ch001.txt ~ chNNN.txt` | All |
| `写作资产/设计包v2/设计包-ch{start}-{end}.md` **或** `写作资产/设计包v3/chXXX-设计包.md` | All |
| 每事件有原文证据 | All |
| **v3格式专检：4层结构完整 + DNA对接映射表存在** | All |
| **v3套路归档：套路库/{套路名}.md 已创建或更新** | All |
| 设计包覆盖章数 ≥ 章节文件数 | All |

---

## 边界条件

| 条件 | 处理方式 |
|:-----|:---------|
| 最后一组不足 5 章 | 按实际章数处理，不补空白章 |
| extract.py 不可用 | 对于非中文文件，提示用户确认 Python 环境和依赖 |
| **中文网文 TXT（第X章格式）** | **extract.py 不识别中文章节头。** 必须手动 ETL，详见 `references/chinese-novel-etl.md` |
| 章节标题无法正则匹配（如无编号） | 用「chX-首句前20字」作为文件名 |
| 某章只有寥寥几句 | 标注「本章过短」，仍然产出设计包 |
| 广告与正文难以区分 | 保留疑似行，标注「⚠️ 可能为广告」|
| 5章一批中某章事件密集 | 事件数可超 8，但每章仍保持独立事件链 |
| 中文 TXT 编码不确定 | 依次尝试 GBK → GB18030 → UTF-8 |
| **大规模并行提取（50+章）** | ⚠️ **事件衰减风险**：子 agent 越往后批次越倾向于简化输出。每批 delegate_task 的指令中必须明确要求事件数≥5/章，并在该批完成后立即验证密度。后1/3批次的执行指令应比前1/3更详细（对抗惰性）|
| **多batch命名一致性** | 每个 batch 的 delegate_task 指令中必须在第一行写明「产出文件名格式：ch{三位数}-设计包.md」，不得让子 agent 自行决定命名样式 |

---

## 参考文件

| 文件 | 用途 |
|:-----|:-----|
| `references/chinese-novel-etl.md` | 中文网文手动 ETL 流程（替代 extract.py） |
| `references/batch-scaling.md` | 200+ 章大规模拆解时 delegate_task 并行批处理策略 |
| `references/precision-anchor-format.md` | **v2 事件精度锚点格式**——事件链中每事件增加 scene/POV/关键对白/感官锚点 四个字段，消除渲染时的信息盲区 |
| `references/设计包v3-格式规范.md` | **v3 单章 Markdown 格式规范**——4层结构（骨架+爽点+角色+感官）+ 模板 + 质量卡尺 + v2/v3差异对照 |
| `templates/fact-skeleton.md` | 单章设计包模板（pop-writer-chapter 格式） |

---

## ❌ WRONG 示例

| 场景 | 错误做法 | 正确做法 |
|:-----|:---------|:---------|
| ETL 未运行 | 跳过 extract.py 直接写设计包 | 先执行 extract.py 得到 full_text.txt |
| 不拆分逐章 | 直接读 full_text.txt 一次 LLM 跑全书 | 按章拆分后 5 章一批处理 |
| 中文 TXT 硬跑 extract.py | extract 后 chapter_count=0 仍继续 | 走 `references/chinese-novel-etl.md` 手动 ETL |
| 广告混入 | 设计包事件包含「请下载XX APP 查看更多」| LLM 调用时指示去掉非正文内容 |
| 跨批依赖 | 在批处理中引用下一批的内容 | 每批只读自己的 5 章，不跨批 |

---

## 版本

v2.1.0 | 2026-06-16 | 新增批量一致性验证（Step 3中5项检查）、命名强制规则（4种变体禁令）、大规模提取事件衰减风险边界条件、多batch命名一致性边界条件。Step 2b 产出命名规则从建议升级为强制。