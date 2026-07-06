# 初始化 + 一次性路由

> 本文件是 pop-decon 拆书专家入口的操作指令。执行拆书时必读。
> decon 只做初始化和一次性路由，不常驻调度。agent 按 skill description 自主判断调用子 skill。

---

## Step 1：源文件检查

确认用户是否有待拆源文件（TXT/EPUB/PDF）。

| 情况 | 动作 |
|:-----|:-----|
| 用户已提供文件路径 | 确认文件存在 → 进 Step 2 |
| 用户未提供文件 | 路由 `tool-download-webnovel` 下载 → 下载完成 → 进 Step 2 |
| 用户说"网上有"但无 URL | agent 用 popwave-search 搜索 `{书名} txt 下载`，找到 URL 后交 tool-download-webnovel |

**门禁：** 无源文件且未完成下载 → 不得进入 Step 2。

---

## Step 2：判断量级 + 语言

### 量级

询问用户需要拆多少章。默认前 100 章，用户说"全本/全书/全部"= 全书。

### 语言

| 语言 | 处理 |
|:-----|:-----|
| 中文 | 手动 ETL（extract.py 不识别中文「第X章」格式） |
| 英文 | extract.py 自动拆分 |

**门禁：** 用户未确认量级 → 退回询问。

---

## Step 3：一次性路由建议

向用户输出路由建议，然后退出。后续子 skill 调度由 agent 按 description 自主判断，decon 不常驻。

```text
路由建议（一次性）：

1. Phase 1 — pop-decon-design-pack
   手动 ETL 拆章 → 逐章 v4 设计包提取
   产出：写作资产/设计包v4/
   门禁：覆盖率≥95%、命名一致、事件密度≥5/章

2. Phase 2 — pop-decon-volume（≥100章时推荐）
   从设计包提取 L2 单元卡 + 卷纲（含溯源燃料台）
   产出：剧情库/{标签}/

3. Phase 3 — pop-decon-setting
   归纳 L1 六件套 + 世界宪法 + 数值体系
   产出：设定库/{书名}/

4. Phase 4 — pop-decon-prd
   消费 L1+L2+卷纲，产出全书立项 PRD
   产出：立项库/

5. 入库确认
   逐模块确认产出已写入 pop-trope-library 四库
```

**门禁：** 路由建议输出后，decon 退出。不得在后续 Phase 间反复介入调度。

---

## 质量门禁速查

每个 Phase 完成后，agent 自行对照质量标准自检。详细标准见 `references/output-quality-standards.md`。

| Phase | 关键门禁 | 失败处理 |
|:------|:---------|:---------|
| Phase 1 | 覆盖率≥95%、命名一致、事件密度≥5/章、首行格式匹配 | 退回补充 |
| Phase 1→2 | 跨卷格式审计（多卷时） | 见 `references/format-consistency-audit.md` |
| Phase 2 | L2单元卡≥3条 + 卷纲≥1份 | 退回 Phase 1 |
| Phase 3 | L1 六件套齐全 | 退回 Phase 2 |
| Phase 4 | PRD 文件存在 | 退回 Phase 3 |

---

## 入库确认（强制）

全管线 Phase 1→4 完成后，逐模块确认产出已写入 pop-trope-library 四库并更新索引。

| Phase | 入库模块 | 通过标准 |
|:------|:---------|:---------|
| Phase 2 | `剧情库/{标签}/` | L2单元卡 ≥ 3条 + 卷纲 ≥ 1份 |
| Phase 3 | `设定库/{书名}/` | L1 六件套齐全 |
| Phase 4 | `立项库/` | PRD文件存在 |
| pop-shared-dna | `文风库/{书名}.md` | 文风档案存在 |

**入库速查：** `pop-trope-library/references/deconstruction-intake-quickref.md`

完成后告知用户："拆书完成，已入库 pop-trope-library。写作管线可直接从 library 消费。"

---

## 边界条件

| 场景 | 处理 |
|:-----|:-----|
| 前N章跑完后用户要求升级全书 | 重新跑全书 design-pack → Phase 2-3 |
| extract.py 脚本不可用 | 中文 TXT 走手动 ETL；英文终止并提示环境 |
| 子 skill SKILL.md 不可读 | 终止，输出具体哪个子 skill 缺失 |
| 用户中途改变量级 | 保存当前阶段产出，用户确认后再切 |
| 源文件编码不确定 | 中文 TXT 优先 GBK → GB18030 → UTF-8 |
| 多卷同目录拆解 | 每卷置于独立子目录 `vol1/` `vol2/`，各自含完整目录结构 |

---

## ⛔ 管线完成确认

> 全管线 Phase 1→4 + 入库确认全部完成后，输出摘要告知用户各模块入库状态。
> 询问是否需要转换为写作项目或仅保留为分析。
