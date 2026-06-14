# Step 1: ETL — 运行 extract.py

> **方向**：从原始 TXT/EPUB 提取全文 + 元数据。
> **核心约束**：硬性前置步骤。Step 1 未完成，不得进入 Step 2-4。

---

## I/O 注解

| 维度 | 内容 |
|:-----|:-----|
| **读什么** | 原始 TXT/EPUB 文件（由上游 `tool-download-webnovel` 提供） |
| **做什么** | 运行 extract.py，将原始文件转换为标准化的 `full_text.txt` + `metadata.json` |
| **产出** | `_temp/full_text.txt` + `_temp/metadata.json` |
| **门禁** | 两个文件必须全部生成且非空；否则退回重新跑脚本 |

---

## 操作步骤

### 1. 确认输入文件

确认原始文件路径已就位。变量：`$INPUT_FILE`

支持格式：`.txt` / `.epub` / `.pdf` / `.docx` / `.rtf` / `.html`

### 2. 运行 extract.py

```powershell
python "skills\pop-decon\scripts\extract.py" all "$INPUT_FILE" ".\_temp\"
```

> 如 extract.py 路径有变化，以实际部署路径为准。

### 3. 验证输出

确认以下两个文件存在且非空：

| 文件 | 用途 |
|:-----|:-----|
| `_temp/full_text.txt` | 全文合并，作为 Step 2 拆分输入 |
| `_temp/metadata.json` | 章节数量、标题列表、原始格式信息 |

### 4. 门禁检查（通过/退回）

```
□ _temp/full_text.txt 存在且非空
□ _temp/metadata.json 存在且非空
→ 全部通过 → 进入 Step 2（按章拆分）
→ 未通过 → 退回重新跑脚本
```

---

## 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **脚本已执行** — 两个产出文件必须存在。未跑脚本=不准进入后续任何步骤 |
| ❌2 | **不编造数据** — 若脚本输出的 `metadata.json` 中章节列表为空，不准虚拟章节名 |

---

## 产出

```
_temp/
├── full_text.txt      ← extract.py 产出（全文合并）
└── metadata.json      ← extract.py 产出（章节元数据）
```

## 下一步

Step 1 完成 → 进入 Step 2：按章拆分
