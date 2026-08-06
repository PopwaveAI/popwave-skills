# Step 2: 剧情白描提取（质量模式 / 性能模式）

> **方向**：逐章单文件提取。根据 execution.mode 选择输出格式（precision v4设计包3层+1区 / fast 瘦身白描卡4段式），根据 execution.strategy 选择处理方式（quality 单章逐章 / performance 30章合并）。
> **核心约束**：这是拆书管线唯一的**质量瓶颈**。设计包/白描卡烂 = volume/setting 全烂。宁退不回。
> **v6.3.0 核心变化**：新增「处理方式」维度 execution.strategy——**质量模式**（单章逐章，精度最高）与**性能模式**（30章合并一次调用，成本最低）。每次任务开启前必须先与用户确认选用哪种策略，并说明两种模式的得失。

---

## I/O 注解

| 维度 | precision mode | fast mode |
|:-----|:---------------|:----------|
| **读什么** | 全文 TXT（脚本自动按章分割） | 同左 |
| **做什么** | `slim_card_batch.py --mode precision` 提取 3层+1区 | `slim_card_batch.py --mode fast` 提取 4段白描卡 |
| **产出** | `写作资产/设计包v4/chXXX-设计包.md` | `写作资产/白描卡/chXXX.md` |
| **门禁** | 3层+1区结构完整 | 事件白描+关键数据+爽点钩子三段存在 |

---

## 0. 任务开启前：模式确认（必做）

> ⛔ **v6.3.0 强制环节**：每次拆书任务开启前，必须先与用户确认「处理方式」与「输出格式」，并如实说明两种处理方式的得失，取得用户明确选择后才能继续。禁止擅自默认。

### 0.1 向用户展示两种处理方式（execution.strategy）

| 维度 | 🎯 质量模式（quality） | ⚡ 性能模式（performance） |
|:-----|:----------------------|:--------------------------|
| **处理方式** | 单章逐章，每章 1 次 API 调用 | 30章合并，1 次调用产出 30 张 |
| **精度** | 每章独立上下文，精度最高，跨章不串扰 | 30章共享上下文，后段质量略降 |
| **成本** | 高（187章=187次调用） | 低（187章=7次调用，省约30%） |
| **耗时** | 187章 ~35-45分钟 | 187章 ~3-4分钟 |
| **适用** | 精品拆书/拆书为写/prose-render直接消费 / 关键章节精拆 | 大规模拆书/快速验证/全书骨架 / 成本敏感 |

**得失一句话**：
- 质量模式**得精度、失成本与速度**——每章独立上下文、无跨章串扰，适合需要逐章精读的场景。
- 性能模式**得成本与速度、失部分精度**——30章合并一次调用，后段章节可能因长上下文而细节略粗，适合先跑全书骨架再精修关键章。

### 0.2 向用户确认输出格式（execution.mode）

| 模式 | 格式 | 单章字数 | 压缩比 | 适用 |
|:-----|:-----|:---------|:------:|:-----|
| precision | v4 设计包（3层+1区） | 1-2K | 80-100% | 精品拆书/拆书为写/prose-render |
| fast | 瘦身白描卡（4段式） | 150-400 | ~11% | 大规模拆书/快速验证/全书骨架 |

### 0.3 确认流程

1. 向用户展示 0.1 与 0.2 两张表
2. 询问用户：**「本次拆书用质量模式还是性能模式？输出用 precision 还是 fast？」**
3. 用户明确答复后，记录 `execution.strategy` + `execution.mode`，才进入 Step 2A/2B
4. 若用户答复与默认（performance + fast）一致，确认后即可继续；若不一致，按用户指定调整

---

## Step 2A: precision mode（v4 设计包）

> 使用 `slim_card_batch.py --mode precision`。处理方式由 execution.strategy 决定（quality 单独传，performance 默认）。

### 处理方式

```bash
# 性能模式（30章合并），precision 设计包
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision --strategy performance

# 质量模式（单章逐章），precision 设计包
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision --strategy quality

# 指定卷
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision --strategy performance --volume "第一卷"

# 测试前10章
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision --strategy performance --max-chapters 10
```

**参数说明**：
| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| --input | （必填） | 小说 TXT 文件路径 |
| --output | 写作资产/白描卡 | 输出目录（precision 建议 `写作资产/设计包v4/`） |
| --mode | fast | `precision` = 设计包v4（3层+1区） |
| --strategy | performance | `quality` = 单章逐章 / `performance` = 30章合并 |
| --batch-size | performance:30 / quality:1 | 每批合并章数（quality 恒为 1） |
| --workers | performance:3 / quality:10 | 并发数 |
| --encoding | gbk | TXT 文件编码（自动检测回退） |
| --volume | 全书 | 只处理指定卷（如 "第一卷"） |
| --max-chapters | 无限制 | 最多处理章数（用于测试） |
| --api-key | 环境变量 | DeepSeek API Key |
| --model | deepseek-v4-flash | 模型名 |

### v4 格式

每份设计包为独立文件 `chXXX-设计包.md`，3层+1区结构（详见 `references/v3-format-quick-reference.md`）：

```markdown
# 设计包 — chXXX「章节标题」

## 1. beat链 (L1beat链层) - 表格格式
| # | beat | 类型 | scene | POV | 参与角色 | 原文证据 |
（至少8个beat，原文证据列只写定位指针，🔒 标记关键对白/数据）

## 2. 爽点设计 (L2爽点层)
- 情绪弧线 / 爽点机制 / 章末钩子(L1-L5)

## 3. 角色与人设 (L3角色层)
- 登场角色行为锚定 / 关键对白(语气+潜台词)

## 4. 设定/物品提取区 (S1)
- 本章新揭示的世界设定、力量体系、规则、物品
```

### 不同章型的beat粒度

同一套"5-8 个beat"不能套所有章。必须先判断章型再定粒度：

| 章型 | 特征 | 每章beat数 | beat粒度 |
|:-----|:-----|:----------|:---------|
| **战斗** | 回合制对抗、有胜负有转折 | 8-12 | 每一轮交锋 = 一个beat |
| **对话/信息** | 两人/多人交谈、信息交换 | 5-8 | 每轮信息释放 = 一个beat |
| **探索/发现** | 新地点、新发现、世界观披露 | 6-10 | 每个地点/每个发现 = 一个beat |
| **过渡/日常** | 赶路、修炼、日常 | 3-5 | 每段日常/每段修炼 = 一个beat |
| **高潮/转折** | 重大beat、多线汇合 | 10-15 | 可拆到每人每线一个beat |

### 质量检验（precision mode）

脚本自动按 `# 设计包 — chXXX「标题」` 标记拆分写入独立文件。agent 必须抽检后 10%（至少 3 章）执行 7 项质量检查，全部通过才能视为完成。

---

## Step 2B: fast mode（瘦身白描卡）

> 使用 `slim_card_batch.py --mode fast`。处理方式由 execution.strategy 决定。

### 1. 格式规范

格式规范详见 `references/slim-card-format-spec.md`。

**4 段式结构**：
```
# chXXX「标题」
POV: xxx | 章型: xxx | 原文: XXXX字
## 事件白描（3-5句，覆盖本章核心）
## 关键数据
🔒 一行式摘要+原文定位指针
## 爽点·钩子
## 人物关系变化（可选）
```

### 2. 处理方式

```bash
# 性能模式（30章合并），fast 瘦身白描卡（默认）
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --strategy performance

# 质量模式（单章逐章），fast 瘦身白描卡
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --strategy quality

# 指定卷
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --volume "第一卷"

# 测试前10章
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --max-chapters 10
```

**参数说明**：
| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| --input | （必填） | 小说 TXT 文件路径 |
| --output | 写作资产/白描卡 | 输出目录 |
| --mode | fast | `fast` = 瘦身白描卡（4段式） |
| --strategy | performance | `quality` = 单章逐章 / `performance` = 30章合并 |
| --batch-size | performance:30 / quality:1 | 每批合并章数（quality 恒为 1） |
| --workers | performance:3 / quality:10 | 并发数 |
| --encoding | gbk | TXT 文件编码（自动检测回退） |
| --volume | 全书 | 只处理指定卷（如 "第一卷"） |
| --max-chapters | 无限制 | 最多处理章数（用于测试） |
| --api-key | 环境变量 | DeepSeek API Key |
| --model | deepseek-v4-flash | 模型名 |

### 3. 失败重试

脚本内置 2 次自动重试。仍失败/缺失的章节会在汇总报告中列出，可单独重跑：

```bash
# 重跑缺失章节（降低并发数提高成功率）
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --workers 2
```

### 4. 产出目录

```
写作资产/
├── 白描卡/                    ← fast mode 产出
│   ├── ch001.md
│   ├── ch002.md
│   └── ...
├── 白描卡-汇总报告.md          ← 处理统计
├── 设计包v4/                   ← precision mode 产出（如使用）
│   ├── ch001-设计包.md
│   └── ...
└── 设计包-汇总报告.md          ← precision 处理统计
```

### 5. 质量卡尺（fast mode，5项）

| # | 检查项 | 通过标准 | 扣分规则 |
|:-:|:-------|:---------|:---------|
| 1 | 事件白描完整 | 3-5句，覆盖全部核心转折 | 缺1转折 -1 |
| 2 | 🔒关键数据 | 有🔒标记且为一行式摘要+指针 | 缺标记 -2 |
| 3 | 章型正确 | 7型之一且与内容匹配 | 错误 -1 |
| 4 | 钩子标注 | 有钩子或合理省略 | 缺钩子且无说明 -1 |
| 5 | 字数控制 | ≤500字 | >500字 -1 |

### 6. 实测性能参考

**质量模式（单章逐章，10并发）**：

| 量级 | 调用次数 | 耗时 | 压缩比 | 实测验证 |
|:-----|:--------:|:-----|:------:|:---------|
| 10 章 | 10 | ~15s | ~11% | ✅ |
| 187 章 | 187 | ~3 分钟 | ~11% | ✅ 深渊主宰第一卷 |
| 678 章（全书） | 678 | ~12 分钟 | ~8% | 预估 |

**性能模式（30章合并，3并发批）**：

| 量级 | 批数 | 调用次数 | 耗时 | 压缩比 | 实测验证 |
|:-----|:----:|:--------:|:-----|:------:|:---------|
| 30 章 | 1 | 1 | ~60s | ~11% | ✅ |
| 187 章 | 7 | 7 | ~3-4 分钟 | ~11% | ✅ 深渊主宰第一卷 |
| 678 章（全书） | 23 | 23 | ~12 分钟 | ~8% | 预估 |

---

## 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **ETL前置缺失** — 未ETL/未按章拆分 → 退回 |
| ❌2 | **凭空发明内容** — beat链/事件白描中出现原文不存在的内容 → 退回 |
| ❌3 | **证据缺失或转录** — precision: 每beat必须有原文证据指针; fast: 🔒数据必须有一行式摘要+指针 |
| ❌4 | **精度模式锚点缺失** — precision: 每beat必须有scene+POV+🔒+感官锚点 |
| ❌5 | **结构不完整** — precision: 3层+1区; fast: 事件白描+关键数据+爽点钩子三段 |
| ❌6 | **广告混入** — 设计包/白描卡中混入非正文内容 → 退回 |
| ❌7 | **多章合并或命名违规** — precision: chXXX-设计包.md; fast: chXXX.md |
| ❌8 | **API Key 缺失** — 未设置 DEEPSEEK_API_KEY 环境变量且未传 --api-key |
| ❌9 | **产出遗漏** — 单批输出缺失章节（脚本标记 missing）→ 重跑缺失批次 |
| ❌10 | **未确认模式擅自执行** — 任务开启前未与用户确认 strategy+mode 就提取 → 退回重确认 |

---

## 版本

v6.3.0 | 2026-08-06 | 新增「处理方式」维度：质量模式（quality 单章逐章）/ 性能模式（performance 30章合并），任务开启前强制模式确认

---

## ⛔ 加载门禁 + 下一步指引

> 在加载下一 step 文件前，禁止产出任何文件。
>
> 下一 step：`steps/step-3-verify.md`
> 加载指令：`Get-Content -Encoding UTF8 -Raw steps/step-3-verify.md`
> 什么时候进入下一步：已完成模式确认，所有章节的设计包/白描卡已产出