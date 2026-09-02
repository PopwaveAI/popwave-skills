# CHANGE

## v1.1.1 | 2026-09-02

### 修复 wiki URL 反斜杠死链

- `写作技法库\元素卡库\00-索引.md` / `写作技法库\剧情周期表\00-周期表索引.md`（Step 1 + 速查表两处）统一为 `/写作技法库/元素卡库/00-索引` 与 `/写作技法库/剧情周期表/00-周期表索引`（正斜杠 + 无扩展 slug）。
- 同步 skill.json（version）。

## v1.1.0 | 2026-08-31

### 意识层 + wiki 站取源

- 新增「心智前置·意识层」节（Know-Gap/Pack/Worth/Deepen + 取材预算硬上限），贯穿本 skill 与全流程。
- wiki 取源统一走网站 https://wiki.popwave.cn（替代本地 D:\popwave-wiki\docs 镜像 / sync.ps1）。

## v1.0.3 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份词"章纲拼接器"→"章纲拼接"，description 精简
- 引语与版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version/displayName/description）

## v1.0.2 | 2026-08-31

### library 迁移回收：本地库删除，数据源改指 wiki 镜像

- 根因：library（179MB）已解耦迁至 D:\popwave-wiki（wiki.popwave.cn），本地重复一份易干扰；skill 对 library/ 的运行时引用改为指向本地 wiki 镜像 D:\popwave-wiki\docs\（出厂即备，离线可用）
- 职责：数据只从 wiki 镜像消费/回写，不再以本地 library 为单一数据源
- 全仓 library/ 活引用已清零，本地 library 目录已删除（内容经 sync.ps1 全量入 wiki，阔 _temp 过程产物与源书txt 不发布）

## v1.0.1 | 2026-08-31

### 更名：pop-outline → pop-snow-outline

- 雪花流家族徽记：统一管线 8 件 skill 加 snow 中间名，与旧族 pop-fanqie-*/pop-qidian-* 区分（老板 2026-08-31 拍板）；test 系列 5 件（adapt/lite/plot/research/write）同批删除退役（备份 temp/_backup-test-20260831/）
- name/version/全仓引用同步；功能零变化

## v1.0.0 | 2026-08-31

由 test-plot Step2.5（章纲组装）拆出独立首版。

**架构变化**：
- 章纲组装从 plot 层拆出，独立为 pop-outline skill
- 章纲组装协议（原 `library/写作技法库/章型与场景/章纲组装协议.md`）核心内容全内联进 SKILL.md
- 选卡源双轨：元素卡库54卡（主力）+ 剧情周期表（并轨迁移中）

**保留资产**：
- 章纲格式 v3.1（叙事原子+线账本+plot锚点区）
- 章型统一表（6枚举英文ID）
- 拼装五步（读下发→选卡→填槽→现编→记账+门禁）
- 现编三道关（一致/审美/密度）
- 出口门禁7项
- 四条红线（物理闭合/判定链内联/出章面板必锁/事实校验链）

**术语对齐**：去AI味红线第4条——"节拍"统一改"先后手"。

**模板**：章纲.tpl.md
