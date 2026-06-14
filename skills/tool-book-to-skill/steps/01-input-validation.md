# Step 0-1: 范围检查与输入验证

## 第一步：范围检查与输入验证

1. 无参数 → 停止，提示用法：`tool-book-to-skill <路径> [skill名称]`
2. 识别输入路径和可选的 Skill 名称
   - 最后一个参数若不是文件/文件夹/glob，且看起来像 slug（小写连字符）→ 视为 `SKILL_NAME`
   - 其余参数视为 `INPUT_PATHS`
   - 若输入路径是已有 Skill 目录（含 SKILL.md + chapters/）→ 标记为模式 4
3. 验证至少有一个支持的文件（`.pdf` / `.epub` / `.docx` / `.txt` / `.md` / `.rst` / `.adoc` / `.html` / `.rtf` / `.mobi` / `.azw` / `.azw3`）
4. 对目录和 glob 展开匹配

❌ 门禁：无支持文件 → 退回，告知用户"未找到支持的文档格式"，列出支持格式清单。
