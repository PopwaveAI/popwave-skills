# CHANGELOG

## v6.4.0 | 2026-08-06

### 执行方式从「脚本直连 DS API」改为「派发子 agent 执行」

- **核心变化**：Phase 1 白描卡/设计包提取不再依赖 `slim_card_batch.py` 脚本直连 DS API，改为由主 agent **派发子 agent** 执行。每个子 agent 读取 `_temp/chapters/` 原文章节、产出白描卡/设计包，**无需 DEEPSEEK_API_KEY**
- **删除 `scripts/slim_card_batch.py`**：彻底移除对 DS API 的依赖，管线纯子 agent 驱动
- **双模式映射为派发粒度**：
  - 质量模式（quality）= 每章 1 个子 agent 逐章精拆，精度最高、跨章不串扰
  - 性能模式（performance）= 每 30 章 1 个子 agent 合并产出，成本最低（187章=7个子agent，省约30%）
- **step-2-batch-process.md**：重写为子 agent 派发流程（Step 2A-1~5 / 2B-1~5），含子 agent 任务包模板、绝对路径写入要求、主 agent 汇总验证；新增红线❌8「子agent落盘错误目录」
- **SKILL.md**：双维度表、速查表、红线改为子 agent 方式，删除脚本引用行
- **references/batch-scaling.md**：命令示例改为派发方式说明，脚本参数改为派发参数
- **references/slim-card-format-spec.md**：v4 对照表处理方式行改为子 agent 派发
- **templates/slim-card-template.md**：生产方式说明改为子 agent
- **skill.json**：description 同步子 agent 派发说明，版本 6.3.0→6.4.0
- **版本三处一致**：SKILL.md + skill.json + CHANGELOG.md 统一为 6.4.0

## v6.3.0 | 2026-08-06

### 新增「质量模式 / 性能模式」双处理方式维度

- **核心变化**：新增第二维度 `execution.strategy`（处理方式），与 `execution.mode`（输出格式）正交——形成「质量模式（单章逐章）/ 性能模式（30章合并）」×「precision/fast」双维度矩阵
- **质量模式（quality）**：单章逐章处理，每章 1 次 API 调用，精度最高、跨章不串扰；成本高（187章=187次）、耗时 ~35-45 分钟
- **性能模式（performance）**：30章合并，1 次调用产出 30 张，成本最低（187章=7次，省约30%）、耗时 ~3-4 分钟；后段章节因长上下文质量略降
- **任务开启前强制模式确认**：`steps/step-2-batch-process.md` 新增「0. 任务开启前：模式确认」环节，必须先向用户展示两种处理方式与两种输出格式的得失表，取得用户明确选择（strategy+mode）后才能继续；新增红线❌10「未确认模式擅自执行」
- **slim_card_batch.py**：新增 `--strategy` 参数（quality/performance），quality 强制 batch_size=1 + 10并发 + 120s超时，performance 默认 batch_size=30 + 3并发批 + 300s超时
- **SKILL.md**：升级为双维度表（输出格式 × 处理方式），任务开启前先确认模式
- **skill.json**：description 同步双维度说明，版本 6.2.0→6.3.0
- **版本三处一致**：SKILL.md + skill.json + CHANGELOG.md 统一为 6.3.0

## v6.2.0 | 2026-08-04

### 双模式统一改为30章合并批处理

- **核心变化**：从「单章1次API调用」改为「30章合并1次API调用」（30张合并白描），降低API调用成本约30%
- **precision/fast 双模式统一走 `scripts/slim_card_batch.py --mode`**，废弃原「precision走delegate_task 3章/批、fast走DS API 10并发」的分离方式
- **slim_card_batch.py 重构**：
  - 新增 `--mode`（fast白描卡/precision设计包）与 `--batch-size`（默认30）
  - 30章合并一次调用，一次产出30张卡/设计包
  - 新增两套系统提示词（fast 4段式 / precision 3层+1区）
  - 按 `# chXXX「标题」`（fast）/ `# 设计包 — chXXX「标题」`（precision）标记拆分写入独立文件
  - missing 章节自动列清单供重跑
- **step-2-batch-process.md**：双模式均改为30章合并批处理，更新命令与参数、性能表、质量红线（新增❌9 30章合并遗漏）
- **batch-scaling.md**：重写为30章合并策略，新增成本对比表（187次调用→7次，~96%调用次数减少）
- **slim-card-format-spec.md**：处理方式更新为30章合并，v4对比表处理方式行同步
- **版本三处一致**：SKILL.md + skill.json + CHANGELOG.md 统一为 6.2.0

## v6.1.0 | 2026-07-22

### 按规范重写 SKILL.md

- 按pop-shared-skill-create v6.1.0规范重写SKILL.md
- 新增"做什么"输入/输出/下游表+双模式表
- 新增"怎么操作"section含execution.mode+强弱加载声明，步骤表合并step文件路径
- 红线#1改为读取协议（Get-Content -Encoding UTF8 -Raw，禁用Read工具）
- 合并双速查表为单一文件目录引导（文件+读取时机+核心内容）
- 版本只留最新一条
- skill.json版本同步至6.1.0
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v6.0.0 | 2026-07-14
- **新增 fast mode（瘦身白描卡）** — 双模式架构：precision（v4设计包）+ fast（瘦身白描卡4段式）
- 新增 `references/slim-card-format-spec.md`：瘦身白描卡格式规范，含4段式结构、字数规则、质量卡尺5项、v4对比表、下游消费说明
- 新增 `templates/slim-card-template.md`：瘦身白描卡模板
- 新增 `scripts/slim_card_batch.py`：DS API并发处理脚本，支持 --volume/--workers/--max-chapters/--encoding 参数，自动编码检测
- 更新 SKILL.md：双模式速查表、模式选择规则、红线适配双模式
- 更新 step-2：增加 fast mode 分支（DS API并发处理流程）
- 更新 step-3：增加 fast mode 验证规则（5项卡尺）
- 更新 batch-scaling.md：增加 DS API 并发实测数据（187章/3分钟/10并发/压缩比11.3%）
- **实测数据**：深渊主宰第一卷187章，原文623K→产出71K，压缩比11.3%，平均377字/章，3分钟/10并发

## v5.0.0 | 2026-07-01
- **删除"本章套路"字段** — 下游不再消费套路类型，从模板/格式规范/快查参考/step文件中全面移除
- **按 pop-shared-skill-create v6.0.0 规范重构 SKILL.md** — 从304行重写为≤60行纯路由层
- frontmatter 精简为 name+description（≤4行）
- 红线从9条精简为5条，第一条改为读取协议
- 新增强弱加载保障声明
- 速查表改为全文件目录引导（14行文件索引+4行步骤索引）
- **step文件末尾统一加加载门禁+下一步指引** — step-0/1/2 加自传导，step-3 加管线完成确认
- **修v3遗留** — post-hoc-format-normalization.md 和 normalize-headlines-from-source.py 中的 设计包v3 路径改为 设计包v4
- step-3 验证完成通知从"Step 4/5 enrichment"改为"Phase 2"
- 质量卡尺从8条改为7条（删除套路检查项）
- skill.json downstream 补充 pop-decon-prd
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md 统一为 5.0.0）

## v4.4.0 | 2026-06-30
- **新增 Step 0: 源文件获取** — Phase 1 自带获取能力，项目目录无源 TXT 时委派 tool-download-webnovel 自动下载
- 新增 `steps/step-0-source-acquire.md`：检测源文件→无则委派下载→落位校验→交付 Step 1
- 速查表新增 Step 0 行；红线 ❌1 扩展覆盖源文件获取；落盘检查点新增 `$TXT_PATH`
- 版本号三处对齐（SKILL.md/skill.json/CHANGELOG此前不一致，借本次统一为 4.4.0）

## v4.1.0 | 2026-06-24
- 删除 Step 4（套路归档批量pass）和 Step 5（价值点分流批量pass）
- 删除 `价值点采集-入库分流SOP.md`、`step-4-trope-pass.md`、`step-5-valuepoint-pass.md`
- 套路库保留但不再有自动化入库 pass
- 速查表、参考文件表、WRONG 示例同步清理

## v4.0.0 | 2026-06-23
- 章节设计包精简：4层→3层+1区(事件链+爽点+角色+设定/物品提取区)
- 套路归档/价值点分流defer到Step 4/5批量pass
- 事件表8列→7列(删除字数估计)
- 删除L4感官层(动作六段式/DNA映射/环境基线6维/氛围渲染)
- 新增设定/物品提取区(补齐Phase 3数据缺口)
- 红线19→9条
- 卡尺15→8项
- 重写step-2/step-3(修复v2过时格式)
- 同步skill.json版本

## v1.1.0 | 2026-06-15
- Merge clean into design-pack: ETL + split + 5-chapter batch LLM
- Step 1: ETL + split (no LLM)
- Step 2: 5章一批 LLM: clean + extract events + write design packs
- Step 3: verification
- Delete pop-decon-clean (absorbed)
