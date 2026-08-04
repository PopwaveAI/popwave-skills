# Step 2: 30章合并批处理提取（双模式）

> **方向**：30章合并一次调用，逐章单文件提取。根据 execution.mode 选择 precision（v4设计包3层+1区）或 fast（瘦身白描卡4段式）。
> **核心约束**：这是拆书管线唯一的**质量瓶颈**。设计包/白描卡烂 = volume/setting 全烂。宁退不回。
> **v6.2.0 核心变化**：从「单章 1 次调用」改为「30 章合并 1 次调用」，双模式统一走 `slim_card_batch.py`，降低 API 调用成本约 30%。

---

## I/O 注解

| 维度 | precision mode | fast mode |
|:-----|:---------------|:----------|
| **读什么** | 全文 TXT（脚本自动按章分割） | 同左 |
| **做什么** | `slim_card_batch.py --mode precision` 30章合并提取 3层+1区 | `slim_card_batch.py --mode fast` 30章合并提取 4段白描卡 |
| **产出** | `写作资产/设计包v4/chXXX-设计包.md` | `写作资产/白描卡/chXXX.md` |
| **门禁** | 3层+1区结构完整 | 事件白描+关键数据+爽点钩子三段存在 |

---

## 0. 模式选择

```
execution.mode 已指定？
  ├─ precision → 走 Step 2A（下方）
  └─ fast → 走 Step 2B（下方）
  └─ 未指定 → 判断：章数 > 100 且不需要 prose-render 直接消费 → fast；否则 precision
```

---

## Step 2A: precision mode（v4 设计包）

> 以下为 precision mode 流程。使用 `slim_card_batch.py --mode precision`，30章合并批处理。

### 处理方式

**30章合并一次调用**，使用 `scripts/slim_card_batch.py`：

```bash
# 全书 precision 模式，30章合并
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision

# 指定卷
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision --volume "第一卷"

# 测试前10章
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision --max-chapters 10

# 调整每批章数（默认30）
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/设计包v4/" --mode precision --batch-size 30
```

**参数说明**：
| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| --input | （必填） | 小说 TXT 文件路径 |
| --output | 写作资产/白描卡 | 输出目录（precision 建议 `写作资产/设计包v4/`） |
| --mode | fast | `precision` = 设计包v4（3层+1区） |
| --batch-size | 30 | 每批合并章数（30章合并白描） |
| --encoding | gbk | TXT 文件编码（自动检测回退） |
| --volume | 全书 | 只处理指定卷（如 "第一卷"） |
| --workers | 3 | 并发批数（每批是30章大调用，不宜过高） |
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

每批返回后，脚本自动按 `# 设计包 — chXXX「标题」` 标记拆分写入独立文件。agent 必须抽检后 10%（至少 3 章）执行 7 项质量检查，全部通过才能视为完成。

---

## Step 2B: fast mode（瘦身白描卡）

> 以下为 fast mode 流程。使用 `slim_card_batch.py --mode fast`，30章合并批处理。

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

**30章合并一次调用**，使用 `scripts/slim_card_batch.py`：

```bash
# 基本用法（默认 fast + 30章合并）
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/"

# 指定卷
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --volume "第一卷"

# 测试前10章
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --max-chapters 10

# 自定义每批章数
python scripts/slim_card_batch.py --input "{书名}.txt" --output "写作资产/白描卡/" --batch-size 30
```

**参数说明**：
| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| --input | （必填） | 小说 TXT 文件路径 |
| --output | 写作资产/白描卡 | 输出目录 |
| --mode | fast | `fast` = 瘦身白描卡（4段式） |
| --batch-size | 30 | 每批合并章数（30章合并白描） |
| --encoding | gbk | TXT 文件编码（自动检测回退） |
| --volume | 全书 | 只处理指定卷（如 "第一卷"） |
| --workers | 3 | 并发批数（每批是30章大调用，不宜过高） |
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

### 6. 实测性能参考（30章合并）

| 量级 | 批数 | 每批章数 | 并发批 | 耗时 | 压缩比 | 实测验证 |
|:-----|:----:|:-------:|:------:|:-----|:------:|:---------|
| 10 章 | 1 | 30 | 1 | ~20s | ~11% | ✅ |
| 30 章 | 1 | 30 | 1 | ~60s | ~11% | ✅ |
| 187 章 | 7 | 30 | 3 | ~3-4 分钟 | ~11% | ✅ 深渊主宰第一卷 |
| 678 章（全书） | 23 | 30 | 3 | ~12 分钟 | ~8% | 预估 |

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
| ❌9 | **30章合并遗漏** — 单批输出缺失章节（脚本标记 missing）→ 重跑缺失批次 |

---

## 版本

v6.2.0 | 2026-08-04 | 双模式统一改为30章合并批处理：precision/fast 均走 `slim_card_batch.py --mode`，每批30章一次调用，降低 API 成本约30%

---

## ⛔ 加载门禁 + 下一步指引

> 在加载下一 step 文件前，禁止产出任何文件。
>
> 下一 step：`steps/step-3-verify.md`
> 加载指令：`Get-Content -Encoding UTF8 -Raw steps/step-3-verify.md`
> 什么时候进入下一步：所有章节的设计包/白描卡已产出