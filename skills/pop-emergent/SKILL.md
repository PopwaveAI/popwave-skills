---
name: pop-emergent
description: 涌现式小说项目初始化/修复/审计入口。当用户说"新建涌现项目/项目跑偏/审计涌现规范/涌现式骨架"时启用。建骨架、补元数据、审计 scope/版本/current-state/soul/review/DNA执行包闭环，给出一次性路由建议；非每轮正文写作总控。
---

# Pop Emergent

初始化/修复/审计入口，非每轮总控。每轮正文由 pop-emergent-write 执行，中长线记忆和下一章DNA执行包由 pop-emergent-review 压入 current-state.md。

## 骨架定义

```text
pop-emergent（初始化/审计）
├── qidian-seed（番茄seed覆盖：种子+世界展开+主角引擎+角色储备池+世界圣经）
├── pop-emergent-plot（番茄plot-design迁移：素材收集+幕纲+6门禁+施工卡）
├── pop-emergent-write（番茄prose-render覆盖：6章型+17微观技法+五层指导+current-state消费）
├── pop-emergent-write-dndlike（番茄dndlike：D&D数据面板流完整写作引擎）
├── pop-emergent-write-onepiece（番茄onepiece：海贼王世界冒险流完整写作引擎）
└── pop-emergent-review（番茄review覆盖：逐beat对比+gap分析+current-state更新+历史层）
```

## 标准流程

```text
pop-emergent 初始化骨架
→ qidian-seed 种子+世界展开
→ pop-emergent-plot 素材收集+幕纲+施工卡
→ pop-emergent-review 初始化 current-state（将施工卡+快照压缩为 current-state.md）
→ pop-emergent-write（或流派skill）写正文+落盘
→ pop-emergent-review 逐beat对比+gap分析+更新current-state+历史层
→ 循环 write ↔ review
```

## 红线

1. 读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具。
2. 创建项目必须双文件齐全：SKILL.md + skill.json。
3. 版本三处一致：SKILL.md + skill.json + CHANGELOG.md。
4. 不当每轮总控；路由建议仅初始化/修复/审计时一次性给出。
5. 不让 write 全量扫库；库文件由 review 筛入 current-state。
6. 不把"本次采用 skill"当合规证据；必须检查 scope 真实存在。
7. 不调用 pop-novel-create 处理涌现式写作。
8. 启用文风DNA时，必须检查 soul 的长期融合策略和 current-state 的本章DNA执行包是否存在。

## 速查表

| 文件 | 读取时机 |
| --- | --- |
| `steps/step-1-init-audit.md` | 初始化/审计时加载，执行骨架建立与审计报告 |
| `steps/step-2-fix-route.md` | 修复缺口时加载，补 current-state/soul 骨架并给一次性路由 |
| `templates/skeleton-init.tpl.md` | 初始化骨架时复制，提供目录树与空壳元数据块 |
| `references/v3.5-pipeline-prd.md` | 骨架/owner/命名/execution.mode/版本契约层 |

骨架、owner 表、命名规范、execution.mode、版本基线、回复格式见 PRD §4，不在本 skill 重复定义。

## 强弱加载保障

- 强加载：红线、速查表、PRD §4 契约引用（每轮必读）。
- 弱加载：step-1/step-2/templates 按 scenario 按需加载。

版本：v4.0.0，变更见 `CHANGELOG.md`。