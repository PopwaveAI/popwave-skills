# Context Manifest — 子agent上下文注入清晰化 PRD

> 创建日期: 2026-06-28
> 管线版本: v3.5
> 关联skill: expert-writer, pop-writer-v3-create, pop-writer-v3-revise

---

## 背景与问题

当前涌现式写作管线中，主会话（expert-writer）通过 dispatch step 调度子agent（create/revise）时，声明"组装精简context"并注入种子文档、活记忆、文风DNA等材料。但实际执行中，注入过程是一个黑盒：

| 应该注入 | 实际发生了什么 |
|:---------|:-------------|
| 种子文档全文 | agent可能只读了前半段 |
| 活记忆相关部分 | agent可能跳过了，因为文件太大 |
| 上章末尾800字 | agent可能读了全文，也可能只读了几行 |
| 文风DNA | 已知问题：用read limit:60只读了40KB文件的前60行 |
| info_acquired | agent可能完全忽略了 |

根本原因：主会话声明了"注入什么"，但无法验证"子agent实际接收了什么"。没有回执机制，没有完整性校验，没有失败感知。这导致两个后果：

1. 质量问题无法定位——创作质量不达标时，无法判断是子agent能力问题还是context注入缺失问题。
2. 注入规范无法执行——即使step文件写了"必须Get-Content -Raw完整加载"，子agent仍可能用read工具limit截断，主会话无从感知。

---

## 目标

建立一套 context manifest 机制，让子agent的上下文注入从黑盒变为白盒：

- **可观测**：主会话能知道每次dispatch实际注入了哪些材料、来源、大小。
- **可验证**：子agent回执确认实际接收状态，主会话对照检查一致性。
- **可定位**：创作质量出问题时，能对照manifest定位是哪个context缺失或截断导致的。
- **低成本**：manifest产出和receipt回执都是轻量YAML，不显著增加token开销。

---

## 机制设计

### 核心流程

```
主会话                          子agent
  │                               │
  ├─ 1. 组装context               │
  ├─ 2. 产出manifest ──────────→  │
  │                               ├─ 3. 接收context
  │                               ├─ 4. 执行创作/修订
  │                               ├─ 5. 产出正文 + receipt ←──
  │ ←─────────────────────────────┤
  ├─ 6. 对照manifest vs receipt   │
  ├─ 7a. 一致 → 接受产出          │
  └─ 7b. 不一致 → 触发修复        │
```

manifest 在主会话 dispatch 前产出，与context一起注入子agent。receipt 在子agent产出时附带返回。主会话收到产出后，第一件事是对照 manifest 和 receipt 做一致性检查，再决定是否接受产出。

### 注入项定义

manifest 管理以下注入项，每项有固定的标识和来源：

| 注入项标识 | 来源 | 加载方式 | 说明 |
|:-----------|:-----|:---------|:-----|
| `seed_doc` | 种子文档.md | Get-Content -Raw | 种子文档全文，含任务表+要素切片+本章聚焦 |
| `chapter_focus` | 种子文档.md#本章聚焦段 | 内联提取 | 本章导演意图，含三问 |
| `living_memory` | 活记忆/活记忆.yaml | 内联提取(投影) | 三态投影：主角状态+压力仪表盘+未了事项，非全量 |
| `prev_chapter_tail` | 正文/chXXX.md | 内联提取(末尾N字) | 上一章末尾，用于衔接 |
| `style_dna` | 写作资产/文风库/{书名}.md | Get-Content -Raw | 文风DNA全文，仅revise注入 |
| `info_acquired` | 素材库/知识沉淀/{文件名}.md | 内联提取 | 本章信息获取结果，如有 |
| `l2_card` | 卷纲/L2-{编号}.md | Get-Content -Raw | 当前L2剧情单元卡，如有 |

不同子agent接收的注入项集合不同：

| 子agent | 必须接收 | 可选接收 | 禁止接收 |
|:--------|:---------|:---------|:---------|
| create | seed_doc, chapter_focus, living_memory, prev_chapter_tail, info_acquired | l2_card | style_dna |
| revise | prev_chapter_tail(重写稿), style_dna, seed_doc(要素切片段) | — | chapter_focus(创作决策), info_acquired, l2_card |

禁止接收项的存在是为了维持 context 隔离——revise 不应该知道创作决策过程，create 不应该加载文风DNA（避免创作时模仿文风而非自然涌现后由revise统一渲染）。

---

## 数据模型

### Context Manifest（主会话产出）

每次 dispatch 子agent时，主会话产出一份 manifest。manifest 可以内嵌在 dispatch 产出中（不独立存文件），也可以存为临时文件。

```yaml
context_manifest:
  dispatch_id: ch005-create-001        # 唯一标识：章号-目标-序号
  dispatched_to: pop-writer-v3-create   # 目标子agent
  dispatch_time: 2026-06-28T10:30:00    # 时间戳
  chapter: 5                            # 目标章号

  injected:
    seed_doc:
      source: 种子文档.md
      method: Get-Content -Raw
      size_chars: 1650                  # 实际字符数
      checksum: a3f2e1                  # 内容指纹（前8位MD5）
      
    chapter_focus:
      source: 种子文档.md#本章聚焦
      method: inline                    # 内联提取
      content: |                        # 直接内联内容
        推进: 压力源A（斩杀线倒计时）
        新增: 无
        钩子方向: 即时危机型
        三问:
          - 读者必须知道系统错位机制
          - 斩杀线必须推进
          - 章末留哥布林发现尸体
      size_chars: 180
      
    living_memory:
      source: 活记忆/活记忆.yaml
      method: projection                 # 三态投影提取
      sections: [主角状态, 压力状态, 未了事项]
      size_chars: 380
      
    prev_chapter_tail:
      source: 正文/ch004.md
      method: inline_tail                 # 末尾提取
      lines_extracted: 末尾1200字
      size_chars: 1200
      checksum: b8c4d2
      
    info_acquired:
      source: 素材库/知识沉淀/西雅图流浪汉生态.md
      method: inline
      size_chars: 850
      
    l2_card:
      source: 卷纲/L2-001-穿越求生·系统觉醒.md
      method: Get-Content -Raw
      size_chars: 4500
      checksum: c7d9e3

  not_injected:                          # 负向声明
    - style_dna                           # create不加载文风DNA
    - 会话历史                             # context隔离
    - 修订记录                             # 上次revise的记录
    - 项目总控                             # 工程层文件，创作不需要
```

### Context Receipt（子agent回执）

子agent产出正文/修订稿时，在产出末尾附带一份 receipt。receipt 不是独立文件，而是附在产出文本之后的一个YAML块。

```yaml
context_receipt:
  dispatch_id: ch005-create-001          # 与manifest的dispatch_id对应
  received:
    seed_doc:
      status: full                        # full / partial / missing
      actual_read_chars: 1650             # 实际读取字符数
      key_elements_confirmed:             # 关键元素确认（子agent声明读到并理解了这些）
        - 主角引擎（驱动力+行为准则）
        - 金手指（行动驱动机制）
        - 压力聚焦（当前3个压力源）
        - 任务表（当前可执行任务5个）
        - 本章聚焦（三问）
        
    chapter_focus:
      status: full
      三问确认:
        - "读者必须知道系统错位机制: 已确认"
        - "斩杀线必须推进: 已确认"
        - "章末留哥布林发现尸体: 已确认"
        
    living_memory:
      status: full
      sections_read: [主角状态, 压力状态, 未了事项]
      # 如果某个section没读到，这里会显示 missing
      
    prev_chapter_tail:
      status: full
      actual_read_chars: 1200
      
    info_acquired:
      status: full
      applied: true                       # 是否在创作中使用
      
    l2_card:
      status: full
      actual_read_chars: 4500

  anomalies: []                           # 异常列表，空=无异常
```

如果子agent发现注入的某项有问题（截断、缺失、格式错误），在 `anomalies` 中说明：

```yaml
  anomalies:
    - item: style_dna
      issue: partial_read
      detail: "文件40700字，实际读取前60行约3000字，后续内容未读取"
    - item: info_acquired
      issue: not_applied
      detail: "信息获取结果已接收但创作中未使用"
```

---

## 一致性检查规则

主会话收到子agent产出后，对照 manifest 和 receipt 逐项检查：

| 检查维度 | 通过条件 | 不通过处理 |
|:---------|:---------|:-----------|
| **完整性** | receipt.status = full 且 actual_read ≈ manifest.size（误差<10%） | 标记为 `partial`，触发修复 |
| **关键元素** | key_elements_confirmed 覆盖 manifest 中声明的所有关键元素 | 标记为 `missing_elements`，触发修复 |
| **三问确认**（仅create） | chapter_focus 三问全部确认 | 标记为 `三问未确认`，退回重做 |
| **文风DNA完整性**（仅revise） | style_dna status=full 且 actual_read = manifest.size（精确匹配，不允许误差） | 标记为 `dna_truncated`，退回重做 |
| **异常列表** | anomalies 为空 | 有异常则按异常类型处理 |

### 修复策略

检查不通过时，主会话不直接接受产出，而是根据问题类型触发修复：

| 异常类型 | 修复动作 |
|:---------|:---------|
| `partial_read`（文件截断） | 重新注入完整文件 + 重新dispatch子agent（附带上次receipt作为参考） |
| `missing_elements`（关键元素未确认） | 重新dispatch，在prompt中强调必须读取并确认缺失的元素 |
| `三问未确认` | 退回Step0重新产出本章聚焦，三问重新确认后再dispatch |
| `dna_truncated` | 重新注入文风DNA（Get-Content -Raw强制完整加载）+ 重新dispatch |
| `not_applied`（信息获取结果未使用） | 检查是否信息获取结果确实不适用于本章（合理则接受），否则重新dispatch强调必须参考 |

连续2次同一项检查不通过，标记为 `dispatch_failure`，降级到主会话直接执行（策略B兜底）。

---

## 与现有6步循环的集成

manifest 机制嵌入现有6步循环的 Step2（dispatch-create）和 Step3（dispatch-revise），不新增步骤。

### Step2 集成（dispatch-create）

当前流程：
```
组装context → 调度create → 收集产出 → 门禁检查
```

加入manifest后：
```
组装context → 产出manifest → 调度create（注入context+manifest）→ 收集产出+receipt → 对照检查 → 通过则接受/不通过则修复
```

manifest在"组装context"之后、"调度create"之前产出。receipt在"收集产出"时一并收集。"对照检查"替代原来的简单"门禁检查"。

### Step3 集成（dispatch-revise）

同样的集成方式。revise的manifest中 `style_dna` 是必须项，且一致性检查中文风DNA完整性是精确匹配（不允许误差），因为文风DNA截断是已知的反复出现的问题。

### 不影响的步骤

Step0（本章规划）、Step1（信息获取）、Step4（记忆更新）、Step5（落盘）不受manifest机制影响。manifest只在dispatch子agent时起作用。

---

## checksum 计算

checksum用于验证文件内容完整性，防止"声明注入了但内容不一致"的情况。

计算方式：文件内容UTF-8编码后的MD5值取前8位十六进制。

主会话在产出manifest时计算checksum，子agent在产出receipt时也可以回算验证。如果主会话注入的文件内容和子agent接收到的内容一致，checksum应该相同。

checksum不一致说明传输过程中文件内容发生了变化（理论上不应该发生，但作为防御性检查存在）。

实际实现中，checksum是可选字段——如果计算成本过高，可以只用 size_chars 做粗略校验。但文风DNA（已知截断问题的高频文件）必须带checksum。

---

## 成本评估

### Token开销

每次dispatch增加的token开销：

| 项目 | 估算大小 | 说明 |
|:-----|:---------|:-----|
| manifest（主会话产出） | ~300-500 token | 取决于注入项数量 |
| receipt（子agent产出） | ~200-400 token | 取决于确认项数量 |
| 总计/dispatch | ~500-900 token | 每次create+revise各一次 |

按每章2次dispatch（create+revise）计算，每章增加约1000-1800 token。相比创作本身2500-3500字正文（约4000-6000 token），manifest+receipt的开销在15%-30%之间。

这个开销换来的是：
- 每次dispatch的注入可观测
- 质量问题可定位
- 文风DNA截断等已知问题可自动检测和修复

### 执行开销

manifest 产出是主会话在组装context时顺带完成的——它已经在读文件、提取内容，产出manifest只是把这些操作记录下来。不需要额外的文件读取操作。

receipt 产出是子agent在创作完成后顺带产出的——它需要回顾自己读到了什么，这有一定的认知开销，但这是必要的（如果子agent不知道自己读到了什么，那才是真正的问题）。

---

## 实施计划

### 改动范围

| 文件 | 改动内容 | 改动量 |
|:-----|:---------|:-------|
| `expert-writer/steps/step-2-2-dispatch-create.md` | 新增manifest产出+receipt检查逻辑 | 中 |
| `expert-writer/steps/step-2-3-dispatch-revise.md` | 同上，revise版本 | 中 |
| `expert-writer/SKILL.md` | 门禁表新增manifest相关门禁 | 小 |
| `pop-writer-v3-create/SKILL.md` | 新增receipt产出要求 | 小 |
| `pop-writer-v3-revise/SKILL.md` | 同上 | 小 |

### 版本规划

| skill | 当前版本 | 目标版本 | 变更类型 |
|:------|:---------|:---------|:---------|
| expert-writer | 9.4.0 | 9.5.0 | minor（新增机制） |
| pop-writer-v3-create | 1.2.0 | 1.3.0 | minor（新增receipt） |
| pop-writer-v3-revise | 1.1.0 | 1.2.0 | minor（新增receipt） |

### 验收标准

1. 每次 dispatch create/revise 必须产出 manifest（含dispatch_id、注入项清单、size、checksum）
2. 每次 create/revise 产出必须附带 receipt（含各项status、key_elements_confirmed、anomalies）
3. 主会话必须执行 manifest vs receipt 一致性检查，不通过时触发修复
4. 文风DNA注入必须带checksum，receipt中文风DNA必须精确匹配（0误差）
5. 连续2次同一项检查不通过必须降级到策略B
6. manifest 和 receipt 的总token开销不超过单章创作token的30%
