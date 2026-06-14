# Step 1: ETL 数据提取

> **方向**：逆 `pop-writer-prose`。从 TXT 正文中提取结构化数据。
> **核心约束**：硬性前置步骤。Step 1 未完成，不得进入 Step 2-4。
> **覆盖级别**：前N章 / 全书

---

## I/O 注解

| 维度 | 内容 |
|:-----|:-----|
| **读什么** | TXT 原文文件（由上游 `tool-download-webnovel` 提供） |
| **做什么** | 执行 `extract.py all` 脚本，从原文提取结构化数据 |
| **产出** | `_temp/baseline-data.json` + `_temp/chapter-index.json` + `_temp/world-data.json` |
| **门禁** | 三个 JSON 必须全部生成且非空；否则退回重新跑脚本 |

---

## 操作步骤

### 1. 确认输入文件

确认 TXT 文件路径已就位。变量：`$TXT_FILE_PATH`

### 2. 执行 extract.py

```bash
python "..\_scripts\extract.py" all "{$TXT_FILE_PATH}" ".\_temp\"
```

### 3. 验证输出

确认以下三个文件存在且非空：

| 文件 | 关键字段 | 用途 |
|:-----|:---------|:-----|
| `_temp/baseline-data.json` | characters[] / places[] / levels[] / ages[] / monsters[] / events[] | 角色卡提取 |
| `_temp/chapter-index.json` | 逐章 title / charCount / firstSentence / tags | 事实骨架 |
| `_temp/world-data.json` | deity / magic / class / species / faction / item / geography 逐章条目 | 世界观提取 |

### 4. 门禁检查（通过/退回）

```
□ _temp/baseline-data.json 存在且非空
□ _temp/chapter-index.json 存在且非空
□ _temp/world-data.json 存在且非空
→ 全部通过 → 进入 Step 2
→ 未通过 → 退回重新跑脚本
```

---

## 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **ETL 脚本已执行** — `_temp/` 下三个 JSON 必须存在。未跑脚本=不准写后续任何产出 |
| ❌2 | **JSON 无数据=不写** — 若 `_temp/*.json` 中无条目，产出中不得编造数据 |

---

## 产出

```
_temp/
├── baseline-data.json      ← extract.py
├── chapter-index.json      ← extract.py
└── world-data.json         ← extract.py
```

## 下一步

Step 1 完成 → 进入 Step 2：角色卡提取
