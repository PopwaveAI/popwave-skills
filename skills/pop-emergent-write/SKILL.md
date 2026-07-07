---
name: pop-emergent-write
description: "当用户说'写正文/续写/重写/把X写成Y/开篇样章/单章爽文/涌现式write'时启用。只负责成文，消费 current-state、soul、最近正文和用户本轮要求；正文落盘到 涌现/正文/；不调用正式 create，不全量扫描项目库。"
---

# Pop Emergent Write

write 只负责成文：消费 `current-state.md` + `soul.md` + 最近正文 + 用户本轮要求，产出正文与创作记录。骨架、owner、命名、execution.mode、回复格式统一引用 PRD §4（`../pop-emergent/references/v3.5-pipeline-prd.md`），本文件不自定义。

版本：v3.5.0（PRD 契约层对齐）

## execution.mode

引用 PRD §4.5。本 skill 的 formal 必读输入：current-state.md + soul.md + 最近正文 + 用户本轮要求 齐全且达标。缺 current-state 或 soul 不得标 formal。三档切换条件见 PRD §4.5，不在此重复。

## 速查表

| 文件 | 读取时机 |
| --- | --- |
| steps/step-1-consume.md | 开始消费 4 类输入时 |
| steps/step-2-write.md | 消费完成、开始写正文时 |
| templates/chapter-record.tpl.md | 写完正文、准备回复时 |

强弱加载保障：SKILL.md 为强加载主文件，steps/ 与 templates/ 为弱加载按需读取；agent 必须在对应时机读取对应文件，不得跳过。

## 回复格式

引用 PRD §4.7 统一回复骨架，专属产出摘要见 templates/chapter-record.tpl.md。

## 红线

1. 读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具。
2. 创建必须双文件：SKILL.md + skill.json。
3. 版本三处一致：SKILL.md + skill.json + CHANGELOG.md。
4. 不调用 `pop-novel-create`。
5. 正文落盘到 `涌现/正文/`，不全文进对话。
6. 不自称读库除非用户指定或缺口处理。
7. 不在 write 内维护库文件；新增事实只列清单不落库，由 review 落库。
