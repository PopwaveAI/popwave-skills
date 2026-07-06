---
name: pop-emergent-seed
description: 当用户说"碰撞idea/做种子/定主卖点/定soul/涌现式seed"时启用。碰撞 idea、做全书种子、确定主卖点/叙事魂/题材承诺和禁区；产出 seed-种子文档.md 和 soul.md 首版。
---

# Pop Emergent Seed

seed 回答"写一本什么小说"——内容、情节、卖点。soul 回答"什么味道的小说"——文风、笔触、风格。seed 不替作者锁死剧情。

## 红线

1. 读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具。
2. 创建 skill 必须双文件：SKILL.md + skill.json。
3. 版本三处一致：SKILL.md + skill.json + CHANGELOG.md。
4. 不写正文、不写章纲、不冻结世界设定。
5. soul.md 首版必须落盘带元数据（owner=seed，见 PRD §4.2）。
6. 主卖点必须一句话说清且说明主角如何主动。
7. 不把世界压迫当主角主动。

## 速查表

| 文件 | 读取时机 |
| --- | --- |
| steps/step-1-collide.md | 碰撞 idea、候选 PK、推方案时读 |
| steps/step-2-lock.md | 用户确认方案后，锁定种子并落盘时读 |
| templates/seed-doc.tpl.md | step-2 落盘 seed-种子文档.md 前读 |
| templates/soul.tpl.md | step-2 落盘 soul.md 首版前读 |

骨架/owner/命名/execution.mode/回复格式统一引用 PRD §4：`../pop-emergent/references/v3.5-pipeline-prd.md`。

## execution.mode

三档切换条件引用 PRD §4.5。本 skill 的 formal 必读输入：核心承诺、主卖点、禁区、待 research 问题齐全。

## 强弱加载保障

formal 必读输入齐全才正式落盘；有缺口降档补全后继续；快速脑暴不落盘。三档切换条件见 PRD §4.5。step-1 可不落盘，step-2 落盘必须达 formal 或 draft。

## 回复格式

引用 PRD §4.7 统一骨架；专属摘要为 seed 主卖点结论和 soul 落盘状态。

## 版本

v3.5.0
