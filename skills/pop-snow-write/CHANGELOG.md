# CHANGELOG

## v1.1.0 | 2026-08-31

### 意识层 + wiki 站取源

- 新增「心智前置·意识层」节（Know-Gap/Pack/Worth/Deepen + 取材预算硬上限），贯穿本 skill 与全流程。
- wiki 取源统一走网站 https://wiki.popwave.cn（替代本地 D:\popwave-wiki\docs 镜像 / sync.ps1）。

## v1.0.2 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份词"正文写作引擎"→"正文写作"，description 精简
- 引语与版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version/displayName/description）

## v1.0.1 | 2026-08-31

### 更名：pop-write → pop-snow-write

- 雪花流家族徽记：统一管线 8 件 skill 加 snow 中间名，与旧族 pop-fanqie-*/pop-qidian-* 区分（老板 2026-08-31 拍板）；test 系列 5 件（adapt/lite/plot/research/write）同批删除退役（备份 temp/_backup-test-20260831/）
- name/version/全仓引用同步；功能零变化

## v1.0.0 | 2026-08-31

由 test-write(v8.1.1) 改造为统一管线正文写作引擎首版。

**架构变化**：
- 改名 test-write → pop-write，去 test 专属（包配方/设定包/改编计划内置引用）
- X 体验层从必选项改为可选（项目存在`素材/改编计划.md`才启用）
- 设定注入表对齐 pop-stage 产出路径：加入`设计/卷舞台/卷N-舞台.md`（日常章注入）
- KB 参考从项目侧 KB/ 目录改为 library/写作技法库/（不硬编码文件名，按章型选读）
- 文风兜底继承 pop-fanqie-write `references/文风兜底/`（23份按赛道分类）

**保留资产**（test-write 核心能力）：
- 章纲读3章（叙事原子序列+线账本+锚点区）——向前推进唯一来源
- 写作包16字段 + execution.mode 三档
- 文风DNA强制注入（P0素材/文风锚定→P1执行包→P2兜底）
- 设定注入表（必选2件+按章型6类）
- DNA落地8项 + 对话落地3项
- word-count.ps1 验收门禁（纯汉字2000-2500）
- 新增事实只声明不落库（review落库）
- 硬后继 pop-review
- 6条红线

**资产来源**：
- scripts/word-count.ps1 ← test-write
- templates/chapter-record.tpl.md ← test-write
- references/文风兜底/（23份）← pop-fanqie-write
