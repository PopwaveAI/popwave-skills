# Phase B: 拆解报告生成

## 第一步：准备上下文

```powershell
py scripts/report_agent.py "原文/{标题}.md" -o "拆解文/"
```

脚本自动加载 `report-prompt.md` + `report-template.md`。

## 第二步：AI 执行拆解

按 `report-prompt.md` 规范撰写拆解报告，核心原则：
1. **不摘抄原文** — 提炼观点，不是复制粘贴
2. **pop 视角** — 对标写作管线，给出行动项
3. **长短适度** — 短文 3-5 段，长文 6-8 段
4. **模板不死板** — 根据文章类型灵活调整

**门禁：** 报告必须有 `一句话定性` + 至少 3 个核心部分。

## 第三步：保存报告

→ `{标题}_拆解报告.md`

```markdown
---
title: "[标题] 拆解报告"
source: "原文标题"
author: "公众号名"
source_url: "原文链接"
created: "YYYY-MM-DD"
type: "文章拆解"
tags: []
---

# [标题] 拆解报告
> 一句话定性
...
```
