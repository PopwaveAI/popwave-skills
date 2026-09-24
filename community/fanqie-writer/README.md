# fanqie-writer v1.29.9-fork.48（番茄小说写作技能）

番茄平台的网文连载创作技能，定位为上游 fanqie-crafter 的「补充层」——只补上游没有的能力，不重复其已覆盖内容；上游可独立使用，两者可配合。

本目录是 popwave 技能仓库的社区技能包（`community/fanqie-writer`），由技能中心按社区包分发。

## 目录结构

```
fanqie-writer/
├── SKILL.md                  # 主流程：四批交付三闸门、15 条交付前自检
├── skill.json                # 仓库清单：id / 版本 / 触发词 / 权限 / 按需加载策略
├── README.md                 # 本文件
├── THIRD_PARTY_NOTICES.md    # 来源与授权说明
├── UPSTREAM-INHERITANCE.md   # 上游资产继承清单（本仓库补写的说明件，非上游原件）
├── references/               # 31 个参考文件（题材包 / 套路库 / 情绪模板 / 文笔规则等）
├── templates/                # 8 个模板（大纲 / 细纲 / 人物 / 情绪 / 章节 / 写作规则 / 记忆 / 拆书）
├── scripts/                  # 4 个脚本（字数配额 / 字数校验 / 格式归一 / 门禁与风格画像）
└── assets/                   # 卷级规划模板
```

包根 ＝ 本目录（`SKILL.md` 所在目录）。技能内所有引用都是相对包根的路径，例如调用脚本写作
`python scripts/check_chapter_wordcount.py <章节文件>`。

## 收录说明

来源为维护者发布的 `fanqie-writer-v1.29.9-fork.48.zip`（2026-09-24 15:09）。收录时**未改动** `SKILL.md`、`references/`、`templates/`、`scripts/`、`assets/` 的任何内容，逐字节与原包一致。本仓库只新增以下 4 件：

| 文件 | 作用 |
|---|---|
| `skill.json` | 仓库清单，供技能中心识别 id、版本、触发词、权限与加载策略 |
| `README.md` | 按仓库口径重写（原版写的是「解压 zip 后上传」的交付方说明） |
| `THIRD_PARTY_NOTICES.md` | 来源与授权说明 |
| `UPSTREAM-INHERITANCE.md` | 补写说明件：`SKILL.md` 引用了该件，但来源包未随包提供 |

## 已知缺口

1. `UPSTREAM-INHERITANCE.md` 的逐文件登记表（A 类原文一字未动 / B 类已叠加 / C 类自研新增）未随包提供，需向原维护者索取。
2. `references/my-methodology.md` 是空骨架，标「待作者确认」的字段按原文设计由作者本人填，不是缺陷。
3. `references/benchmark-writing.md` 引用的 8 本文笔样本为第三方文本，按原文说明归档在项目工作区，不进技能包。

## 与 pop 管线的桥接

`references/pop-pipeline-bridge.md` 定义了本技能与 snow / 灯塔 / 涌现三条管线的路由与冲突裁决：管线管生产，本技能管番茄合规与平台节奏，冲突时番茄规则优先。仅当项目来自 pop 管线（存在 `状态.md`）或用户点名「用章纲写」时启用。

## 版本

v1.29.9-fork.48（2026-09-24）：交付节奏改为「四批 ＋ 三个闸门」；自查词表加「看上下文」判据，防误伤剧本内容。
