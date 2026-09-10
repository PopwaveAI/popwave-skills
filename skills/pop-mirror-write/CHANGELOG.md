# CHANGELOG

## v1.1.0 | 2026-09-10

### 并入 pop-mirror-deai 精华（07-去AI味深化清洗规则）

老板拍板：snow 三件套替代 mirror 正文循环后，pop-mirror-deai 不再单设专家，其精华规则并入 write 去AI味节，write 生成即达标（非事后降噪）。

- **新增「深化清洗规则」子节**（Step 2 去AI味写字节后）：核心规则 5 条（删废话/破模板/变节奏/信任读者/去金句）+ 废话黑名单 15 词 + 禁止句式 6 种 + 叙事恶习 9 条 + 被动→主动/副词删除 + 反例→正例速查 11 行 + 其他 AI 模式 6 条 + 快速检查清单 5 条。
- **红线新增第 7 条**（深化清洗：黑名单命中必改，违者 review 打回），原第 7-9 条顺延为 8-10。
- **速查表加行**（深化清洗规则 07-去AI味精华）。
- 与既有「去AI味写字节」浓缩信号表互补：上表是信号、本节是完整规则；deai_gate.py 脚本检测不变（跨系列单一维护源）。

同步三件套：SKILL.md / skill.json（version 1.1.0）/ CHANGELOG。

## v1.0.0 | 2026-09-10

### 重构：自 pop-snow-write v1.12.0 复制迁移（正文循环三件套替换之二）

老板拍板：snow 三件套复制改名替代 mirror 正文循环。本 skill 为替代链第二环，**原 pop-mirror-write v1.2.0（镜界 03 章节写作 + 01 章节节奏精华保真版）整体废弃，由 snow-write 复制版顶替**。

- **复制基底**：pop-snow-write v1.12.0 全量复制——四样核心输入（章纲/全书日志/前一章正文/文风DNA）/写作包抽取/execution.mode 判定（formal/draft/trial）/语感隔离阀/文风DNA 三级（P0 纯样文原文权威）/设定按章型带进/缺口处理不自行补剧情/字数 word-count.ps1 + 去AI味 deai_gate.py 双检自收束/硬后继 review。
- **新增第 0 节 · 产出三检查**：事前沟通（对齐节奏基调/文风延续）→ 事后确认（字数/断章/钩子/新增事实确认点，确认才落盘）→ research 评估（现实细节/专业名词/历史器物不够派 pop-snow-research 补采）。
- **输入适配**：设定带进改为消费 mirror 前段（pop-mirror-world/character）产出，落盘布局 `设计/`（角色库/全书设定/卷舞台等）；章纲/全书日志/章节日志/正文路径沿用 snow 布局。
- **脚本归属**：word-count.ps1 复制进本 skill `scripts/`；deai_gate.py 仍调用 `skills/pop-snow-pipeline/scripts/deai_gate.py`（跨系列单一维护源）。
- **引用改名**：上游 pop-snow-outline → pop-mirror-outline；硬后继 pop-snow-review → pop-mirror-review。
- **红线**：四样核心必读/语感隔离/章纲必兑现/DNA必带进/爽点外显/脚本双检/交接纪律/硬后继/三检查纪律 9 条。

同步三件套：SKILL.md / skill.json（version 1.0.0）/ CHANGELOG（＋ references/文风兜底/ 24 档 + scripts/word-count.ps1 复制自 snow）。

## v1.2.0 | 2026-09-10

### 加产出三检查编排（已被 v1.0.0 复制版取代，保留作历史）

原 pop-mirror-write v1.2.0 内容：镜界 `03-章节写作` + `01-章节节奏（节奏硬尺）` 精华逐字直贴 + 14 条创作原则 + AI 禁词黑名单 + 产出三检查。v1.0.0 起整体废弃，本 skill 由 pop-snow-write 复制版承担正文写作。
