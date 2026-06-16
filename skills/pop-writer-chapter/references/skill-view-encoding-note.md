# skill_view 文件读取与 UTF-8 编码说明

> 排查背景：2026-06-15 会话 `20260615_113419_c9b495` 中报告 L1-06.tpl.md 被截断（210 bytes vs 98 chars），经调查为误报。

## 核心结论

**skill_view 和 read_file 均未截断。** 文件完整，问题出在 bytes 与 characters 的混淆。

## 成因

| 量纲 | 含义 | 示例 |
|:-----|:-----|:------|
| **bytes** | 文件在磁盘上的大小（字节数） | `wc -c` 或 `ls -la` |
| **chars** | Unicode 字符数（人类可读的字符） | `wc -m` 或 `skill_view`/`read_file` 返回的内容 |

UTF-8 编码下：
- ASCII 字符（英文字母、数字、标点）= 1 byte/char
- 中文字符 = **3 bytes/char**
- 混合文件中，bytes 大约是 chars 的 2-3 倍是正常的

## 验证方法

当怀疑文件被截断时，用两种方式交叉验证：

```bash
# 方法1：终端查看原始 hex 头（确认无 BOM）
xxd -l 32 "<file>"
# 正常 UTF-8 without BOM：以文件内容的第一个字节开头
# 如有 BOM：开头三个字节为 EF BB BF

# 方法2：对比 bytes 和 chars
wc -c -m "<file>"
# bytes ÷ chars ≈ 2-3 说明是 UTF-8 中文文件的正常值
# bytes ÷ chars ≈ 1 说明文件只有 ASCII

# 方法3：read_file 确认全量内容
# read_file 返回 total_lines 和 file_size，如果 file_size 与 wc -c 一致则完整
```

## 红线

- ❌ 不要仅因为 `bytes > chars` 就判定截断——对于中文 UTF-8 文件这是正常现象
- ✅ 用 `read_file` 或终端 `cat` 确认实际内容完整性
- ✅ 检查文件是否带有 UTF-8 BOM（`xxd` 开头三字节为 `EF BB BF`）——BOM 可能导致部分工具读入时出现偏差，如有则建议去掉
