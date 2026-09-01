# CHANGELOG · pop-stage

## v1.3.0 | 2026-08-31

### 意识层 + wiki 站取源

- 新增「心智前置·意识层」节（Know-Gap/Pack/Worth/Deepen + 取材预算硬上限），贯穿本 skill 与全流程。
- wiki 取源统一走网站 https://wiki.popwave.cn（替代本地 D:\popwave-wiki\docs 镜像 / sync.ps1）。

## v1.2.0 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份词"舞台引擎"→"舞台设定"，description 精简
- 引语与版本节版本历史解耦，仅留当前版本+指向 CHANGELOG
- 正文装饰性"引擎"→"机制/类型"（引擎类型→类型、引擎是全世界的→机制是全世界的）
- 同步 skill.json（version/displayName/description）

## v1.1.1 | 2026-08-31

### 更名：pop-stage → pop-snow-stage

- 雪花流家族徽记：统一管线 8 件 skill 加 snow 中间名，与旧族 pop-fanqie-*/pop-qidian-* 区分（老板 2026-08-31 拍板）；test 系列 5 件（adapt/lite/plot/research/write）同批删除退役（备份 temp/_backup-test-20260831/）
- name/version/全仓引用同步；功能零变化

## v1.1.0 | 2026-08-31

对齐 pop-seed v2.0.0 全书大纲架构：首喷输入从 `立项/01-立项PRD.md` 改为 `立项/03-全书大纲.md`（取力量体系刻度表/世界骨架/人物生态三块展开）+ `立项/01-命运图.md`（起点终点反转落差定调）。Step 0 输入加载、速查表、frontmatter description 同步改指。

## v1.0.0 | 2026-08-31

- **合并首版**：由 pop-world(v1.0.0) + pop-character(v1.0.0) 合并为舞台引擎，按喷漆模型重构，旧两 skill 废弃删除。
- **分层**：贯穿层（慢变量：力量体系/动力引擎/全书设定10件/金手指/角色库/主线）首喷建、之后只 append 演化；卷级层（快变量：`设计/卷舞台/卷N-舞台.md`）每卷一档，旧档封存。
- **双模式**：首喷（项目无主线.md，新书一次走 Step 0-6）/ 卷级刷新（有主线.md+卷需求brief，走 Step R0-R4）。
- **新增**：卷级刷新模式（盘账→喷卷舞台→角色库增量回写→贯穿层 append）；`生长-新编资产.md` 登记处（plot/write 现编即登，stage 刷新回编）；卷舞台档模板取代各卷切片.md。
- **吸收旧件智慧**：起点五轮交互压缩为 W/C/R 三轮（世界格局/危机体系/角色阵容）；金手指三约束、三问自检、语言指纹、攀登方式标注、战斗可写性、类型风味基线全保留。
- **移交**：拆解/融合模式移交 pop-research，stage 不再做拆书。
- **templates**：力量体系/动力引擎/全书设定9件/金手指/角色库 直接复制自旧两 skill；新建 生长-新编资产/主线/卷舞台 三件 tpl。
