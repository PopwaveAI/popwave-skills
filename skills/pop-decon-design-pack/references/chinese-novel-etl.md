# 中文网文 ETL 指南

> 补充 Step 1（步骤 1）。当源文件是中文 TXT（编码 GBK/GB18030）时替代 extract.py 流程。

## 为什么 extract.py 不能用

`extract.py`（位于 `pop-decon/scripts/`）的 `detect_structure()` 只识别：
- 英文 "Chapter N" / "Capítulo N"
- 罗马数字章节头 ("I: Loomings")

它**不识别**中文「第X章」格式，因此中文网文的 chapter_count 始终为 0。

## 手动 ETL 步骤

### 1. 确定编码

```python
with open('file.txt', 'rb') as f:
    raw = f.read(100000)
# 优先 GBK → GB18030 → UTF-8
for enc in ['gbk', 'gb18030', 'utf-8']:
    try:
        s = raw.decode(enc)
        print(f'OK: {enc}')
        break
    except:
        continue
```

### 2. 识别章节和卷边界

```python
import re

# 章标题正则
CH_PATTERN = re.compile(r'^(第[\d零一二三四五六七八九十百千万]+章[\s　]+.*)')
# 卷标题正则
VOL_PATTERN = re.compile(r'^(第[\d零一二三四五六七八九十百千万]+卷[\s　]+.*)')

with open('file.txt', 'r', encoding='gbk') as f:
    lines = f.readlines()

chapters = []
current_ch = None
current_lines = []

for i, line in enumerate(lines):
    m = CH_PATTERN.match(line.strip())
    if m:
        if current_ch is not None:
            chapters.append((current_ch['num'], current_ch['title'], current_lines))
        # Parse chapter number
        num_str = re.search(r'第([一二三四五六七八九十百千万\d]+)章', line)
        # Convert Chinese number to int if needed
        cn_map = {'一':'1','二':'2','三':'3','四':'4','五':'5','六':'6','七':'7','八':'8','九':'9','十':'10'}
        current_ch = {'num': None, 'title': line.strip()}
        current_lines = [line]
    else:
        if current_ch is not None:
            current_lines.append(line)

if current_ch is not None:
    chapters.append((current_ch['num'], current_ch['title'], current_lines))
```

### 3. 关键注意事项

| 问题 | 处理方式 |
|:-----|:---------|
| **每卷重新编号** | 第一卷有第1~N章，第二卷又从第1章开始。文件编号用全局序号 ch001~chNNN |
| **卷号跳跃** | 原文可能缺少某卷（如直接从第八卷跳到第十卷），照实记录 |
| **章节标题格式不一致** | 有的卷用"第1章"，有的用"第一章"。两种都要匹配 |
| **章标题后有冒号/空格** | 匹配 `第X章[\\s　]+` 范围包括空格和全角空格 |
| **正文中没有广告** | 校对版通常已去广告，但保留去广告流程以兼容网络版 |
| **原文证据引用** | events 的 evidence 字段引用本章原文，不是全局行号 |

### 4. metadata.json 结构（中文网文版）

```json
{
  "source_book": "书名",
  "author": "作者",
  "chapter_count": 20,
  "volume_count": 1,
  "volumes": [
    {"name": "第一卷 贫民区", "start_line": 18, "chapters": 187}
  ],
  "chapters": [
    {"num": 1, "original_num": "1", "title": "夜雨（上）", "chars": 3473}
  ],
  "total_chars": 68483
}
```
