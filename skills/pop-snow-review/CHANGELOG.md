# CHANGELOG

## v1.1.2 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份词"章节审核引擎"→"章节审核"，description 精简
- 引语与版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 正文"改编引擎"→"改编机制"
- 同步 skill.json（version/displayName/description）

## v1.1.1 | 2026-08-31

### 更名：pop-review → pop-snow-review

- 雪花流家族徽记：统一管线 8 件 skill 加 snow 中间名，与旧族 pop-fanqie-*/pop-qidian-* 区分（老板 2026-08-31 拍板）；test 系列 5 件（adapt/lite/plot/research/write）同批删除退役（备份 temp/_backup-test-20260831/）
- name/version/全仓引用同步；功能零变化

## v1.1.0 | 2026-08-31

### 统一管线对齐

- 对照物表加入「统一管线」行：本章章纲（pop-outline 产出）作为 Step 1 正向符合性基准，旧三范式保留标注「旧管线」
- 字数脚本路径 `pop-qidian-write/scripts/word-count.ps1` → `pop-write/scripts/word-count.ps1`（2d + 速查表两处）
- skill.json version 1.0.0→1.1.0

## v1.0.0 | 2026-08-31

### 三族合并首版：pop-qidian-review + pop-fanqie-review + test-review → pop-review

> **根因**：三族 review 骨架同构（四步审核+双文件沉淀+子agent审计/主agent落盘+reconstruct采样策略逐字一致），AI味检测体系（15项patterns+疲劳词3级+结构性4项）三件完全重复维护；差异全部收为范式门禁分支。对齐 pop-world/pop-character 合并范式（老板 2026-08-31 拍板的第二轮合并路线图第一棒）。

**公共内核（单点维护）**：Step 0 范式判定 / 四步审核骨架（正向符合性 1a-1e→正文质量 2a-2d→反向充足性 4 维度→沉淀双文件）/ AI味检测全套 / 对话质量6项 / 好看度4问 / 字数脚本实测 / 双文件职责（存"发生"只增不改 + 存"状态"replace）/ 执行模式（Step1-3 子agent审计+Step4 主agent落盘）/ reconstruct 批量回溯（采样策略统一+>8章拆批）/ PASS-REJECT 明确判定。

**范式分支**：
- 番茄追加五项卡口：1e' 番茄底线检查（含合规底线）/ 1f 6章型7节拍对齐 / 1g 战斗可写性 / 1h 主角主动性（连续2章C级=REJECT）/ 1i 多视角覆盖；双文件路径=审核/剧情白描流水账.md(append)+审核/状态快照.md(replace)
- test 前置双门禁：第0审配方符合性（<90%打回）+ 第0.5审X符合性（改编专属）；白描卡追加本章DNA执行包节
- 起点追加：按需更新库文件（设定库/角色库/卷纲/写作燃料）

**模板**：templates/chapter-card.tpl.md（起点/test 通用，新增 test 可选 DNA执行包节）+ templates/state-snapshot.tpl.md（三族通用；番茄流水账格式保持 SKILL.md 内联）。

**废弃**：pop-qidian-review(v4.1.0)、pop-fanqie-review(v5.0.0)、test-review(v7.0.0) 3 件 skill 删除；旧版历史见 `_archive/changelog-history/`。
