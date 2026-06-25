# 已封存 Skill 归档

> 封存时间：2026-06-25
> 封存操作者：pop（经老板江轩确认）

## 封存原因

本目录存放 v1 写作管线 skill（pop-writer-* 系列），因 v2 管线经 AB 测试验证后转正为默认模式而封存。

- v1 管线采用逐事件设计、文风DNA降级、8子表设计包
- v2 管线（场景流设计、DNA硬阻塞、金手指行动引擎、生态图谱）经 A/B 测试验证后转正
- v1 skill 不再被 expert-writer 调用，registry.json 已移除其条目
- 保留归档供历史对照与回溯参考，不维护、不更新

## 与未来重构的关系

v2 转正是过渡措施。未来将按《涌现+反馈环写作管线 PRD》
（`prd/01-管线架构/09-涌现反馈环写作管线-PRD.md`）全面重构。

## 封存清单

| 原 skill | 封存路径 |
|:---------|:---------|
| pop-writer-creative | `_deprecated/pop-writer-creative/` |
| pop-writer-world | `_deprecated/pop-writer-world/` |
| pop-writer-character | `_deprecated/pop-writer-character/` |
| pop-writer-plot | `_deprecated/pop-writer-plot/` |
| pop-writer-chapter | `_deprecated/pop-writer-chapter/` |
| pop-writer-prose | `_deprecated/pop-writer-prose/` |
| pop-writer-qa | `_deprecated/pop-writer-qa/` |
