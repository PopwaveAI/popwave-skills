---
name: pop-novel-master
description: 网文创作技能集群的总控入口。挂载角色后自动路由到对应的子skill完成任务。当前角色：网文作者专家。
version: 1.0.0
---

# pop-novel-master — 网文创作技能集群

> 版本：v1.0 | 2026-06-03
> 职责：路由 + 角色管理 + 编排

---

## 角色系统

当前已挂载角色：

```
roles/pop-novel-author-expert/  ← 网文作者专家（默认角色）
```

每个角色定义了：persona + skill 群索引 + 任务→skill 路由映射。

---

## 路由表

收到用户任务时，匹配到角色后按以下规则路由：

| 任务类型 | 子skill | 路径 |
|:---------|:--------|:-----|
| 开新书/设世界观 | pop-novel-bootstrap | `skills/pop-novel-bootstrap/` |
| 拆书/分析参考书 | pop-novel-deconstructor | `skills/pop-novel-deconstructor/` |
| 剧情设计/幕纲 | pop-novel-plot | `skills/pop-novel-plot/` |
| 黄金三章/开篇 | pop-novel-opening-arc | `skills/pop-novel-opening-arc/` |
| 写正文/章节 | pop-novel-writer | `skills/pop-novel-writer/` |
| 质检/审稿/QA | pop-novel-qa | `skills/pop-novel-qa/` |
| 续写/交接已有项目 | pop-novel-continuation | `skills/pop-novel-continuation/` |
| HTML化/发布 | pop-novel-html-renderer | `skills/pop-novel-html-renderer/` |

## 共享模块

```
_shared/  ← 全局共用（pop身份系统、thinking-mode、工具函数）
```
