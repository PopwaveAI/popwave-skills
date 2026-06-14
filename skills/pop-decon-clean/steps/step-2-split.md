# Step 2: 按章拆分

> **方向**：从 `full_text.txt` 切分为逐章独立 `.txt` 文件。
> **核心约束**：拆分后文件数量必须与 `metadata.json` 的章节数一致。
> **重要**：仅切分，不做任何内容修改。

---

## I/O 注解

| 维度 | 内容 |
|:-----|:-----|
| **读什么** | `_temp/full_text.txt` + `_temp/metadata.json` |
| **做什么** | 按章节标题正则匹配切分，每章保存为独立文件 |
| **产出** | `_temp/chapters/ch001.txt` ... `_temp/chapters/chNNN.txt` |
| **门禁** | 拆分后文件数 ≠ metadata.json 章节数 → 退回 |

---

## 操作步骤

### 1. 读取元数据

从 `_temp/metadata.json` 获取：
- `total_chapters`：总章数
- `chapters[]`：每章的 `number` + `title`

### 2. 正则切分

使用以下正则模式匹配章节标题：

```regex
# 常见章节标题模式（按优先级匹配）
1. ^第[一二三四五六七八九十百千万\d]+章\s*.*$
2. ^Chapter\s+\d+\s*.*$
3. ^第[一二三四五六七八九十百千万\d]+节\s*.*$
4. ^第[一二三四五六七八九十百千万\d]+卷\s*.*$
5. ^序章|尾声|后记|番外\s*.*$
```

> 如上述正则均无法匹配，按段落数均匀切分（4000 字 / 段 ≈ 一章），并在 metadata 中标注 `split_method: "paragraph_estimate"`。

### 3. 保存逐章文件

每章保存为独立文件，命名规则：

```
_temp/chapters/
├── ch001.txt    ← 第 1 章
├── ch002.txt    ← 第 2 章
├── ...
└── chNNN.txt    ← 第 N 章
```

### 4. 门禁检查（通过/退回）

```
□ 拆分后的 .txt 文件数量 == metadata.json 的 total_chapters
□ 每章文件非空（字数 > 0）
□ 文件名按顺序编号（ch001 → chNNN，连续无跳跃）
□ 建立 chXXX → 原文章号的映射表（记录在 metadata.json 中）
→ 全部通过 → 进入 Step 3（逐章清洗）
→ 未通过 → 退回，检查正则或 metadata
```

---

## 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **章序混乱** — ch001 对应原文第 3 章 | 在 metadata.json 中维护 `chapter_mapping: { "ch001": {"original": 3, "title": "..."}, ... }` |
| ❌2 | **跳号** — 文件编号不连续（如从 ch005 直接跳到 ch007）| 确保编号连续，如果原文确实跳号，在映射表中标注 |

---

## 产出

```
_temp/chapters/
├── ch001.txt
├── ch002.txt
├── ...
└── chNNN.txt
```

## 下一步

Step 2 完成 → 进入 Step 3：LLM 逐章清洗
