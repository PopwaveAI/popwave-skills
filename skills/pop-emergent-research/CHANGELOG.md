# CHANGELOG — pop-emergent-research

## v3.5.0 — 2026-07-06

四层架构对齐 PRD v3.5 契约层（`../pop-emergent/references/v3.5-pipeline-prd.md` §4）。

### 新增（四层架构）
- `SKILL.md` 重写为路由层（≤60 行）：红线 7 条 + 速查表 + 强弱加载保障 + 版本
- `steps/step-1-find.md`：找燃料 + 题材机制分流，末尾门禁 + 下一步指引
- `steps/step-2-output.md`：落盘 research-写作燃料.md + content-mechanics.md
- `templates/fuel-doc.tpl.md`：燃料文档空模板（含元数据块）
- `templates/mechanics-doc.tpl.md`：content-mechanics 空模板（含元数据块）

### 修复（对齐 PRD §4 契约层）
- **content-mechanics.md 由"分流建议"升级为正式落盘**（owner=research，PRD §4.2）— 核心修复（问题 3）
- 删除自有 execution.mode 三档表，统一引用 PRD §4.5
- 采用 PRD §4.7 统一回复格式
- 骨架/owner/命名引用 PRD §4.1/§4.2/§4.3，不在本 skill 重复定义
- 燃料文件唯一名 `research-写作燃料.md`，禁用 `燃料库.md` 别名（PRD §4.3）

### skill.json
- 补全 displayName / entry / activation / permissions 字段
- 版本 1.1.0 → 3.5.0

### 保留
- `agents/openai.yaml` 保留不动
