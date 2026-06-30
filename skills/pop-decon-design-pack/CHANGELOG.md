# CHANGELOG

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
