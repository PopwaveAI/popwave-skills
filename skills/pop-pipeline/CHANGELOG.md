# CHANGELOG

## v1.1.0 | 2026-08-31

对齐 pop-seed v2.0.0 全书大纲架构：立项产物从"六要素PRD"（`01-立项PRD.md`）改为共创三层（`01-命运图.md`/`02-命运图plus.md`/`03-全书大纲.md`）。归位表、0c 就绪判定、状态.md 模板立项就绪行、Phase 1 路由说明、可调度清单同步改指。

## v1.0.0 | 2026-08-31

### 三族合并首版：pop-qidian-pipeline + pop-fanqie-pipeline + test-pipeline → pop-pipeline

> **根因**：三族 pipeline 各维护一份安装器，phase 链三套口径（起点 0/1/3/3.5/4/5/6、番茄 0-5、test 0/1/3/3.5/4/5/6），三族界限消失后需要一个统一总控。对齐老板 2026-08-31 拍板的第二轮合并路线图 P7：test-pipeline 改造为 pop-pipeline，卷循环状态机 2a-2g。

**统一 phase 链**：`init → 1(seed) → 2(stage首喷) → 卷循环 2a-2g`。

- **卷循环状态机 2a-2g**（新增，路由参照单点维护）：2a 卷需求brief（pop-plot 任务A）→ 2a+ 卷级调研（pop-research 模式2，轻量可选）→ 2b 卷舞台刷新（pop-stage 模式B，卷二起）→ 2c 卷纲+幕白描（pop-plot 任务B/C）→ 2d 章纲（pop-outline，新位入链）→ 2e 正文（pop-write）→ 2f 审核沉淀（pop-review）→ 2g 卷末盘点回 2a。幕内滚动：产幕N→拼章纲→逐章写审→产幕N+1。
- **包校验/创意X采集/改编强度选择移交 pop-seed**（原 test-pipeline Phase 0 三件套）：seed 路径C 的 C1 已内置包门禁+强度必问，pipeline 不再重复设卡。状态.md 字段 `改编强度` 改为 `seed_path`（A/B/C）。
- **状态.md 模板换新**：新增 current_volume（卷号，2g 卷末+1）；就绪态改三组（立项/舞台/卷循环），卷循环四项（需求brief/卷舞台/卷纲/幕白描）每卷清零，正文/双文件跨卷保留。
- **归位表对齐新路径**：`卷纲/`（brief/卷纲/幕白描）、`卷纲/章纲/`、`设计/卷舞台/`、`产出/白描卡/`+`产出/状态快照.md`（番茄旧路径 `审核/` 作废）；幕白描与审核白描卡的分流规则写明（含锚点段归卷纲，含关键数据🔒归产出）。
- **落地Phase决策表重写**：按新依赖链（PRD→首喷→brief→卷舞台→卷纲→幕白描→章纲→正文→双文件）逐位落地；resume 按"下一章章纲已拼/未拼"分流 2e/2d。
- **状态更新协议内联**（吸收 qidian `references/状态更新协议.md`）：谁干活谁更新、只改涉及字段、pipeline 只在初始化/导入时碰 phase；2g 卷末字段更新单列。
- **资产搬迁**：`templates/项目总控.html`（按新 phase 链与字段重写展示面板）、`references/onboarding-guide.md`（去起点专属口吻，改统一管线引导语）。
- **红线收敛**：三族 7/4/8 条合并为 6 条（只安装不生产/就绪判定查文件系统/user-original 标⚠️/状态源唯一/状态更新走协议/宿主原生读取）。原"包准入门禁""改编强度必问"随职责移交 pop-seed。
- **废弃**：pop-qidian-pipeline(v4.4.2)、pop-fanqie-pipeline(v4.3.2)、test-pipeline(v8.1.2) 三件退役，备份于 `temp/_backup-pipeline-20260831/`。
