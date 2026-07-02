# CHANGELOG — pop-decon-volume

## v5.0.0 | 2026-07-01

### 删除套路聚合步骤 + 按v6.0.0规范重构

- 删除 step-4-tropes.md（套路聚合步骤），原因：design-pack已删除套路字段，无数据来源。原 step-5-intake 重命名为 step-4-intake。
- 修复 step-4（原step-5）中的 L3 残留引用。
- SKILL.md 从283行精简到≤60行。frontmatter从8行精简到2行（删除pipeline metadata）。红线从15条精简到4条。
- 新增强弱加载保障声明。速查表改为全文件目录引导。
- 所有step文件末尾添加加载门禁+下一步指引（自传导）。
- pipeline-context.md 修过时技能名引用。

## v4.0.0 | 2026-07-01

### 架构重构：L2+卷纲双轨产出

从「L2 单元卡 + L3 剧情线 + L4 全书事件」三级产出改为「L2 单元卡 + 卷纲（含溯源燃料台）」双轨产出。

**核心变更：**
- **删除 L3 剧情线**：全部层级定义、模板（L3-剧情线.tpl.md）、步骤（step-2 原 L3 追踪）和红线（❌3/❌8/❌11）均已移除
- **删除 L4 全书事件**：全部层级定义、模板（L4-全书事件.tpl.md）、步骤（step-3 原 L4 识别）和红线（❌5）均已移除
- **新增卷纲（拆书版）**：从 L2 单元卡逆向归纳卷级结构，含溯源燃料台（4类溯源：剧情/设定/创意/质感）
- **溯源燃料台**：只在卷纲级产出，格式为 `| 原文段落 | 猜测来源 | 置信度 |`

**步骤变更（8步→5步）：**
- Step 1a/1b：L2 边界预扫描 + L2 单元卡生产（不变）
- Step 2：从「L3 剧情线追踪」改为「卷纲归纳（含溯源燃料台）」
- Step 3：从「L4 全书事件识别」改为「跨卷主题线追踪」（YAML 极简格式）
- Step 4：套路聚合（不变，产出关联到卷纲）
- Step 5：从「L2/L3 双轨入库」改为「L2卡+卷纲双轨入库」

**模板变更：**
- 新建 `templates/卷纲-拆书版.tpl.md`（对齐 plot 卷纲模板，删除涌现燃料扫描，燃料台改为溯源燃料台，幕序列新增L2卡映射列，舞台人物7列）
- 删除 `templates/L3-剧情线.tpl.md`
- 删除 `templates/L4-全书事件.tpl.md`
- 修改 `templates/L2-剧情单元卡.tpl.md`（删除「不可迁移部分」区块）

**入库路径变更：**
- L2 卡：`写作资产/剧情库/{标签}/{书}-L2-{编号}-{名称}.md`（不变）
- 卷纲：`写作资产/剧情库/{标签}/{书}-卷纲-{卷号}.md`（新路径，替代原 L3 路径）

**红线变更：**
- 删除：❌3（L3引用L2）、❌5（L4候选/确认）、❌8（L3阶段推进表）、❌11（L2/L3/L4层级混淆）
- 新增：❌18（卷纲无溯源燃料台）

## v1.0.0 | 2026-06-14

### 初始发布

从 pop-decon 拆书元 Skill Phase 2 独立为专用技能。

**核心职责**：聚类卷幕。从 `chapter-index.json` 的逐章标签/首句/字数中识别卷边界、幕边界、反推剧情线 Canvas、追踪契诃夫枪链。

**管线定位**：pop-decon-extract (Phase 1) → **pop-decon-cluster (Phase 2)** → pop-decon-world (Phase 3) → pop-decon-engine (Phase 4)

**文件结构**：
- `SKILL.md` — 技能定义、前置检查、质量红线、步骤速查
- `steps/step-1-volume.md` — 识别卷边界
- `steps/step-2-act.md` — 识别幕边界
- `steps/step-3-plotlines.md` — 反推剧情线
- `steps/step-4-chekhov.md` — 契诃夫枪追踪
- `templates/` — 从 pop-decon 复制的 3 个模板文件
- `references/pipeline-context.md` — 管线上下文引用
