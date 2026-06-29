---
name: pop-writer-v3-revise
description: 按用户要求修订小说正文。用于“修改/润色/审稿/重写/检查正文问题”。只处理已有正文的质量、衔接、设定一致性和文风贴合，不承担正向剧情设计。
---

# Pop Writer V3 Revise

revise 是按需修订 skill，不是 create 后的默认流水线。

## 输入

- 待修正文。
- 用户明确的修改目标。
- 原章节运行日志或幕纲。
- 设定账本与状态快照。
- 文风DNA。

## 执行

读 `steps/step-1-revise.md`，按 `templates/修订checklist-模板.md` 输出。

## 红线

- 不改核心事实，除非用户明确要求。
- 不新增硬设定修补漏洞。
- 不把文风修订变成抽象润色，必须落在句子、节奏、动作和信息密度上。
- 不做剧情大改；剧情大改应回到 plot 或 arc。
