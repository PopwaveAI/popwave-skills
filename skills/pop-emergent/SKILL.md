---
name: pop-emergent
description: 涌现式小说项目初始化/修复/审计入口。当用户说"新建涌现项目/项目跑偏/审计涌现规范/涌现式骨架"时启用。建骨架、补元数据、审计 scope/版本/current-state/soul/review 闭环，给出一次性路由建议；非每轮正文写作总控。
---

# Pop Emergent

初始化/修复/审计入口，非每轮总控。每轮正文由 pop-emergent-write 执行，中长线记忆由 pop-emergent-review 压入 current-state.md。

## 红线

1. 读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具。
2. 创建项目必须双文件齐全：SKILL.md + skill.json。
3. 版本三处一致：SKILL.md + skill.json + CHANGELOG.md。
4. 不当每轮总控；路由建议仅初始化/修复/审计时一次性给出。
5. 不让 write 全量扫库；库文件由 review 筛入 current-state。
6. 不把"本次采用 skill"当合规证据；必须检查 scope 真实存在。
7. 不调用 pop-writer-v3-create 处理涌现式写作。

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

版本：v3.5.0，变更见 `CHANGELOG.md`。
