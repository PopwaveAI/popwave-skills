# CHANGELOG — pop-decon-cluster

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
