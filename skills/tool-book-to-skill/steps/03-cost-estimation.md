# Step 2.5-2.6: 成本预估 + 大书处理

## 第三步：成本预估 + 大书处理

读取 metadata.json，在生成前展示预估：

```
📖 检测到 <N> 个源文件
📄 合并页数: ~<N> | 词数: ~<N> | Token: ~<N>K

💰 预估成本:
   输入: ~<N>K tokens  |  输出: ~<N>K tokens  |  总计: ~<N>K tokens
   Sonnet 4.5: ~$<X>  |  Haiku 4.5: ~$<X>
   ⏱ 预计耗时: ~<N> 分钟

📁 将生成: SKILL.md + 章节文件 + glossary + patterns + cheatsheet
```

等待用户确认后继续。

**大书处理（>50K tokens）：** 将 `full_text.txt` 视为可查询语料库，不要一次性全读：

```bash
wc -w full_text.txt                           # 大小检查
grep -n "^\s*(Chapter|CHAPTER)\s+[0-9]+" ...  # 找章节偏移
sed -n '<start>,<end>p' full_text.txt         # 只拉需要的章节
grep -c -i "关键词" full_text.txt             # 验证框架是否提到
```

50K tokens 以下直接 Read 即可。

❌ 门禁：**成本预估必须在生成前展示。** 跳过 Step 2.5 → 退回，让用户有知情权。
