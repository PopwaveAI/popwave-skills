# Third-Party Notices

本目录是社区技能包 `fanqie-writer`，非 popwave 自研技能。

## 来源

| 项 | 内容 |
| --- | --- |
| 上游 | SkillHub `@laoxi/fanqiexiaoshuoxiezuo` v1.0.1（fanqie-crafter by davtime） |
| 本包定位 | 上游的 fork 与「补充层」，只补上游没有的能力 |
| 来源物 | `fanqie-writer-v1.29.9-fork.48.zip`（维护者发布，2026-09-24 15:09，45 个文件） |
| 收录版本 | v1.29.9-fork.48 |

## 收录时做了什么

- `SKILL.md`、`references/`（31 件）、`templates/`（8 件）、`scripts/`（4 件）、`assets/`（1 件）逐字节按原样收录，未做任何内容改动。
- 新增 `skill.json`、重写 `README.md`、新增本文件、补写 `UPSTREAM-INHERITANCE.md`（来源包引用了该件但未随包提供）。

## 授权状态

来源包内**未见 LICENSE 文件**，本仓库无从确认授权条款。本文件是工程清单，不是法律结论。对外分发前需向原维护者与上游作者确认授权与再分发条件。

## 运行依赖

- 4 个 `scripts/*.py` 为本地 Python 脚本，由运行技能的 agent 以相对包根的路径调用，需要 shell 权限。
- 技能内的平台硬信息（`references/fanqie-platform-facts.md`）为 2026-09-20 至 2026-09-23 的查证口径，会过期；`references/market-trends.md` 说明最新风向由 AI 联网查证后回写，故清单声明了 network 权限。
