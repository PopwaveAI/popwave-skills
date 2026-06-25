# 大文件写入可靠性指南

> **定位**：当 prose-render 写入章节正文时，防止因 Hermes checkpoint 系统截断导致文件不完整。
> **适用场景**：任何 >5KB 的文件写入操作。

## 问题

从对话层直接调 `write_file()` 写入大文件（~10KB+）时，Hermes checkpoint 系统可能**静默截断**输出：

- 写入 11,940 bytes → 磁盘只剩 302 bytes（~2.5% 写入）
- 写入 11,970 bytes → 磁盘只剩 400 bytes（~3.3% 写入）
- **截断边界**：约 5KB 以上时风险显著增加

**风险**：截断不会报错，对话摘要中也看不到——后续 agent 读到不完整文件时，基于部分数据产出虚假结论。

## 最佳实践

### 写入完整正文

```python
# ✅ 可靠方式：从 execute_code 内调用写入
from hermes_tools import write_file
import os

chapter_text = "# chXXX ... 完整正文 ..."
write_file("正文/chXXX.md", chapter_text)

# 立即验证
size = os.stat("正文/chXXX.md").st_size
if size < len(chapter_text) * 0.5:
    print(f"TRUNCATED: expected {len(chapter_text)}, got {size}")
    # 重试：分段写入或换用 terminal python3 -c 直接写文件
```

### 追加状态块

```python
# 先确认文件完整
import os
size = os.stat("正文/chXXX.md").st_size
print(f"Current: {size} bytes")  # 验证后决定是追加还是重写全文件

# 方法 A：全文件重写（最可靠）
with open("正文/chXXX.md", "r", encoding="utf-8") as f:
    existing = f.read()

# 方法 B：追加（仅当文件完整时可用）
# 用 terminal 执行: printf '%s' "$STATE_UPDATE" >> 正文/chXXX.md
```

### 验证三件套

每次写入后立即执行：

```bash
# 1. 文件大小对比
wc -c 正文/chXXX.md  # 确认与预期一致

# 2. 状态块存在性

# 3. 末行完整性
tail -3 正文/chXXX.md  # 确认不是截断的中间行
```

## 边界情况

| 情况 | 处理 |
|:-----|:------|
| 文件 <5KB | 对话层 write_file 安全 |
| 文件 5-15KB | 用 execute_code 的 from hermes_tools import write_file |
| 文件 15-30KB | 同上，但每 10KB 追加一次并验证 |
| 文件 >30KB | 分卷写入（多文件）或分段追加 |

## 陷阱：read_file 行号污染

> 本 session 实测事故：用 `read_file` 的输出拼接状态块后写回 → 文件中出现了 `94|` `95|--` 等行号前缀。

### 问题描述

Hermes 的 `read_file` 工具返回的文本格式为 `LINE_NUM|CONTENT`（如 `95|--`）。**但你看到的输出格式和磁盘上的实际内容不是同一回事。** 当以下操作链出现时文件会被污染：

```
read_file(ch003.md) → 获取content字段 → 拼接文本 → write_file(ch003.md)
```

如果 `content` 返回的是**带行号前缀的显示格式**（而不是纯文件内容），写回后每一行都带上 `NN|` 前缀，导致：
- 文件膨胀（约 10% 额外字节）
- 纯文本行如 `--` 变成 `95|--`
- 人眼在 `cat` 输出中几乎无法察觉（行号前缀被误认为是终端行号）
- 字数统计不变（中文字符无影响），但文件结构损坏

### 检测方法

```bash
# 检查文件前 3 行是否含行号前缀
head -3 chXXX.md | grep -E '^[0-9]+\|' && echo "CONTAMINATED" || echo "CLEAN"

# 对比预期大小与实际大小
python3 -c "
import re
with open('chXXX.md') as f: raw = f.read()
clean = re.sub(r'^\d+\|', '', raw, flags=re.MULTILINE)
print(f'Before: {len(raw)} After: {len(clean)} Ratio: {len(clean)/len(raw):.2%}')
if len(clean) < len(raw) * 0.9:
    print('CONTAMINATED')
"
```

### 预防

1. **写文件内容时，永远从你的 Python 变量/模板直接构建**，不依赖 `read_file` 输出作为文本源
2. 如需合并已有文件 + 新内容：
   - ✅ 用 `terminal` 工具执行 `python3 -c "..."` 直接读写文件（不走 Hermes read_file/write_file 工具）
   - ✅ 或在 execute_code 中用 Python 的 `open()` + `f.read()` 直接读写
3. **每次写入后立即验证**：检查文件前 3 行首字符是否为 `#`（正文文件）而非数字
4. 发现污染后修复：`python3 -c "import re; open('f.md','w').write(re.sub(r'^\d+\|', '', open('f.md').read(), flags=re.MULTILINE))"`
