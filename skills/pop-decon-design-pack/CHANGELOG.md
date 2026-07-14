# CHANGELOG

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
