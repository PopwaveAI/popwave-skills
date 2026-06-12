# Agent和skill迭代记录

本知识库收录 Agent 调优和 Skill 迭代的全部 PRD/复盘文档。

---

## 文档索引

| # | 文档 | 链接 | 摘要 |
|-|-|-|-|
| 1 | Paopao上下文管理问题-PRD | [打开](https://n0mqbh938qa.feishu.cn/wiki/LaJMwaNk4iwwWVke3sgcGZiDnDf) | 7 个系统级问题分析（Read截断/历史冻结/无压缩/泄露等），4 个已修复 |
| 2 | 全链路优化PRD-2026-06-10 | [打开](https://n0mqbh938qa.feishu.cn/wiki/UQxkwZZW5iaIRJkuamscQLLPnwh) | 管线产出模板 + 消费链路优化，5 个结构性病灶诊断 |
| 3 | 子agent隔离机制失效分析 | [打开](https://n0mqbh938qa.feishu.cn/wiki/K31XwNFLhiloF8kuakOcy3SznLf) | 6 次失败 100% 失败率，5 个负面后果 |
| 4 | PRD-Skill调用机制失效 | [打开](https://n0mqbh938qa.feishu.cn/wiki/BYPwwxC8HilzWGkeKrWcoGucntc) | 47 次 run 全量审计，3 个真实根因 |
| 5 | 外部知识注入分析-PRD | [打开](https://n0mqbh938qa.feishu.cn/wiki/I3RKw3PcqiAnORkjdzTcJtJbnIf) | 14 条外部知识 → 仅 4 条通过过滤纳入管线 |
| 6 | 复盘问题清单-2026-06-08 | [打开](https://n0mqbh938qa.feishu.cn/wiki/KL9xwz3w2i8eMwkANwpcYB21nE9) | 7 个问题 P0/P1/P2 分级，含证据链与会话引用 |
| 7 | 正文引擎拆分方案 v1 | [打开](https://n0mqbh938qa.feishu.cn/wiki/MDa4wniati2nH6kv6iWcosAhnRf) | pop-novel-writer 拆分为 chapter-design + prose-render 框架 |
| 8 | 正文引擎拆分方案 v2 | [打开](https://n0mqbh938qa.feishu.cn/wiki/XG7mwBPUCiyx3nk1VTdcU8bhnZf) | 子 agent 架构合理性论证 + 完整 SKILL.md 草案 |
| 9 | 排查技巧手册 | [打开](https://n0mqbh938qa.feishu.cn/wiki/TBCTw6CtFiQW3ukwrubcySJund2) | 运行时审计、Read 截断检测、工具链使用 |
| 10 | 写作专家全链路文件依赖图-PRD v2.0 | [打开](https://n0mqbh938qa.feishu.cn/wiki/QdXSwE2ZAiAog6kz2bsc35rXnof) | 管线重构：bookstrap→creative+world，character-schema入链，宪法审计回路 |
| 11 | 全链路匹配_Hermes vs OpenClaw | [打开](https://n0mqbh938qa.feishu.cn/wiki/YbU7w9Vc0iCLuukDBqIcAeN0nQf) | Hermes Agent 与 OpenClaw 全链路能力对比评估 |
| 12 | OpenClaw-首次Auth-401问题报告 | [打开](https://n0mqbh938qa.feishu.cn/wiki/VnSow6IhiiJpLqkF7uMcGH0jndb) | 401 鉴权失败的技术根因与修复记录 |
| 13 | 为什么选择Hermes作为Popwave技术底层 | [打开](https://n0mqbh938qa.feishu.cn/wiki/UjJQw0rm5isl1jki39FcUixUnCh) | Hermes Agent 架构优势分析与选型决策 |
| 14 | 拆书v3.0-分级拆解PRD | [打开](https://n0mqbh938qa.feishu.cn/wiki/RMn9wLli6iFLeUksobycRU7Vn1f) | 全链路图谱驱动的三级拆解体系。Lv1已落地(Phase S)，Lv2/Lv3的格式对齐+消费协议待命 |

---

## 版本

| 日期 | 变更 |
|-|-|
| 2026-06-12 | 新增 05-储备方案 子目录，记录PRD backlog |
| 2026-06-11 | 新增 Hermes/OpenClaw 相关 3 篇文档 |
| 2026-06-11 | 初始建库，收录 10 篇 PRD/复盘文档 |
