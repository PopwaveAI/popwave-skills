# Step 1: ETL + 按章拆分

> **方向**：逆 pop-writer-prose。从 TXT 正文提取原始文本 + 按章拆分。
> **核心约束**：机器操作，不用 LLM。仅 extract.py + 正则拆分。

---

## I/O 注解

| 维度 | 内容 |
|:-----|:------|
| **读什么** | TXT/EPUB/PDF 原文文件 |
| **做什么** | extract.py → 正则按章拆分 → 单章文件 |
| **产出** | `_temp/full_text.txt` + `_temp/metadata.json` + `_temp/chapters/ch001.txt ~ chNNN.txt` |
| **门禁** | 拆分后文件数 ≠ metadata.json 检测的章节数 → 退回 |

---

## 操作步骤

### 1. 运行 extract.py

```bash
python "skills/pop-decon/_scripts/extract.py" all "{$TXT_PATH}" ".\_temp\"
```

验证产出：
- [ ] `_temp/full_text.txt` — 非空
- [ ] `_temp/metadata.json` — 含 chapter_count / word_count

### 2. 按章拆分

从 full_text.txt 中按正则 `^(第[零一二三四五六七八九十百千]+章|Chapter\s+\d+|第\d+章|ch\d+)|第\d+节` 拆分章节。

产出：`_temp/chapters/ch001.txt` ~ `chNNN.txt`

### 3. 验证

- [ ] 章节文件数 == metadata.json.chapter_count
- [ ] 每文件非空

未通过 → 退回重新执行拆分。

---

## 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | ETL 脚本已执行 — `_temp/full_text.txt` 必须存在 |
| ❌2 | 章序号匹配 — 文件号与正文标题号必须一致 |

---

## 产出

```
_temp/
├── full_text.txt
├── metadata.json
└── chapters/
    ├── ch001.txt
    ├── ch002.txt
    └── ...
```

---

## ⛔ 加载门禁 + 下一步指引

> 在加载下一 step 文件前，禁止产出任何文件。
>
> 下一 step：`steps/step-2-batch-process.md`
> 加载指令：`Get-Content -Encoding UTF8 -Raw steps/step-2-batch-process.md`
> 什么时候进入下一步：_temp/chapters/ 下有按章拆分的独立文件