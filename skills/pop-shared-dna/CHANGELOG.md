# CHANGELOG — 03-pop-dna

## v4.2.0 | 2026-07-22

### SKILL.md按设计规范重写

- frontmatter补触发条件（'提取文风''文风DNA''风格蒸馏''分析作者笔触'时启用）
- 红线重构为6条（首条为读取协议/强弱加载规则）
- 速查表从合格/不合格对照表改为文件目录引导（文件+读取时机+核心内容）
- 版本历史只留最新一条，其余移至CHANGELOG
- 新增强弱加载保障声明（SOP骨架区块）
- 业务方法论不变，只改结构/格式/规范
- skill.json版本号4.1.0→4.2.0

## v4.1.1 | 2026-06-26
- **产出路径修正**：`pop-trope-library/文风库/` → `写作资产/文风库/`（对齐 PRD v3.3 与 revise 子skill，涉及 SKILL.md 5处 + step-3-write.md 1处）
- **文风DNA定位修正**：删除"种子第七要素"表述，改为"项目资产（非种子要素，种子为六要素）"（对齐 PRD v3.3）
- **消费方修正**：`pop-writer-v3-emerge` → `pop-writer-v3-revise`（emerge 已废弃，硬阻塞消费方为 revise 子skill），涉及 SKILL.md + skill.json + CHANGELOG
- 同步修正 v4.1.0 条目中的上述错误表述

## v4.1.0 | 2026-06-26
- v3 管线消费支持：文风DNA 降为项目资产（非种子要素，种子为六要素），pop-writer-v3-revise 子skill 硬阻塞消费（缺失=终止）
- downstream 新增 pop-writer-v3-seed + pop-writer-v3-revise
- v2 管线的 pop-writer-prose 消费方式不变

## v4.0.0 | 2026-06-11

- **场景卡矩阵**："战斗"不再是一个维度——拆为早期遭遇战/中坚 boss 战/后期大规模/暗杀偷袭 4 个独立场景卡。对话拆为日常兄妹/情感高潮/信息交换 3 卡。描写/叙述各 2 卡。共 11 个可选场景卡。
- **500+ 字原文/卡**：每个场景卡必须配 ≥500 字原始摘录。不是分析，不是观测——是原始笔触，供 prose-render 直接感受。
- **设计包 scene 字段 1:1 映射**：DNA 场景卡名对齐设计包的 `scene` 字段值，prose-render 读设计包即可定位。
- **全量加载确认**：prose-render 保持全量加载 DNA（~20-25K，Get-Content 安全，不触发截断）。
- **旧 v1 DNA 清理**：删除龙符/遮天/吞噬星空 v1 量化统计型 DNA + examples/ 旧版示例。

## v3.1.0 | 2026-06-11

- **产出路径更新**：styles/ → 写作资产/文风DNA/（对齐 PRD v1.4，文风DNA 与设计包同目录供 prose-render 消费）

## v3.0.0 | 2026-06-09

- **方法论升级**：不统计、不浸泡、不写禁令——从原文中提取作者在每个维度上的模式，配原文证据，标注全周期变化
- **产出变化**：style/ 目录产出文风DNA档案，供 prose-render Phase 1 风格锚定消费

## v2.0.0 | 2026-05

- **初始版本**：从 writer skill 拆出独立文风分析链路
