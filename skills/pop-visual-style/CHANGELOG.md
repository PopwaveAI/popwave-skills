# CHANGELOG

## v1.8.0 — 2026-08-05

### 画风定标按 intent 档位分支（不默认全量门禁）

老板审视全链路发现——画风定标写死"Pipeline 语境下必做"，只想做封面/OC 的用户也被迫跑完整门禁 + 稳定复现。改造成 intent 档位分支：

- `SKILL.md` Step 4：新增档位分支——`comic`/`full` → 完整定标必做（门禁+稳定复现）；`cover`/`oc` → 降为 **agent 自检分支**（自查辨识度/配色/光影/无文字，不设强制用户门禁、不强制稳定复现，定标图达标即标记 `✅ 已认可` 供下游作画风参考）；独立纯文生图跳过
- `SKILL.md` 跨skill引用协议第6条：补 intent 档位说明
- `steps/step4-style-calibrate.md` 何时用：改为按 intent 档位分支；下一步补定妆深度档位提示
- 版本同步：SKILL.md / skill.json 至 v1.8.0

## v1.7.0 — 2026-08-05

### 生图改走 image_generate 工具，移除内置 API Key

老板要求所有 skill 生图环节改用 `image_generate` 工具，清理硬编码 API Key（Pinterest 搜索保持不动）：

- `steps/step3-generate.md`：由「执行 API 脚本」改为 `image_generate` 工具调用，移除 `generate.py` 直连与内置 key 说明
- `steps/step4-style-calibrate.md` §3：由「并发批量生成」改为「`batch_test.py` 导出 `generation_tasks.json` + `image_generate` 工具逐条生成」
- `SKILL.md` 模型说明表：改为「静态图片走 `image_generate` 工具，无 API Key；视频走 `generate.py video` 需显式设置 `ARK_API_KEY`」
- `skill.json` 描述：移除「调用 Seedream API」
- 版本同步：SKILL.md / skill.json 至 v1.7.0

## v1.6.0 — 2026-08-04

### 试点：以 IP 命名画风（新增「双城之战」独立画风）

老板提出以 IP 名命名画风、并指出「现代电影感美漫」与「英雄联盟 双城之战」差距过大。试点以「双城之战」作为 IP 命名画风，从 IP 参考图重建 DNA：

- `style-dna-library.json` 升级 v5.1：新增「双城之战（手绘厚涂电影感）」独立条目（Arcane/Fortiche），37种画风（二次元12/国漫5/韩漫3/插画概念17）
- 新 DNA 核心特征：**手绘糙边**（色块断裂不规则边界，非干净矢量线）、**色块内部渐变**（每个色块内渐变，不在边界混合）、**主观色彩分区**（额头暖黄/颧骨粉橙/眼窝紫/下颚冷蓝）、**2D/3D混合**（3D结构底+2D手绘涂感）、青橙电影对比
- 与「现代电影感美漫」(Marvel系) 并存，`ip_source` 标注 IP 来源保证可追溯
- 加入 `A_dark_cinematic` 暗黑电影系兼容性矩阵，`recommended_composition=CT1_scale_contrast`、`recommended_lighting=LT1_subtractive`
- 命名规范定为 **IP名（技术描述）** 双命名：IP 名保证可识别性，技术描述作为 Seedream 执行力锚点
- 用 `batch_test.py` 文生图复原「双城之战」对比验证，确认与「现代电影感美漫」gap 消除
- 同步更新 SKILL.md / step1 / skill.json 计数（36→37）与版本号
- 后续可扩展 IP 命名画风：哪吒3D、雾山五行、一人之下等

## v1.5.0 — 2026-08-04

### 画风DNA库 v5.0 全视觉生态重构

画风库从"漫画圈"扩到"全视觉生态"，汰换低还原传统媒介、合并重复定位、新增美漫/数字画风：

- `style-dna-library.json` 升级 v5.0：汰换7个模拟物理媒介/低还原画风（伊藤潤二/维多利亚版画/浮世绘/国风水墨/凡妮塔斯/吉卜力/圣魔之血），合并3组重复（赛博朋克霓虹+都市赛博风→赛博边缘行者、黑执事+圣魔之血、港漫武侠风+硬朗武侠历史），新增10个已验证画风（4美漫：极简线稿93.3%/电影感92%/经典漫威8/10/概念艺术78；6全生态：波普90/低多边形92/电影海报87/超现实8.7/扁平矢量4.35/极简线条84.1）
- 分类调整为二次元12/国漫5/韩漫3/插画概念16，总数保持36
- 同步清洗 `lighting-composition-templates.md` 兼容性矩阵、CT1/CT2 最佳画风、LT1/LT2/LT3 兼容画风，移除全部已汰换画风引用
- 同步更新 `step1-style-select.md` 兼容性路由（柔美→LT2、平面→LT3、暗黑→LT1）、`step4-style-calibrate.md` 光影检查、`seedream-prompt-guide.md` DNA库引用与分类计数
- 筛选原则沉淀：Seedream 保真档位优先，淘汰模拟物理媒介，鼓励数字媒介全视觉生态

## v1.4.2 — 2026-08-04

### 出图尺寸硬上限（防止报价翻倍）

- `steps/step3-generate.md` 尺寸表新增铁律：所有出图总像素 ≤ 236 万（Seedream 5.0 Pro 计费临界，超限报价翻倍），上表全部安全（最大 1500x1500=225 万）；`generate.py` 内置 `assert_size_safe` 校验，超限报错中止

## v1.4.1 — 2026-08-04

### 升级：画风定标改为"画风×项目角色联合测试"

老板实测发现固定中性素材测不出"画风能否撑起项目角色"（玄鉴仙族用中性"现代青年+木屋"测画风，测不出"黑金甲衣+金瞳"主角的适配度）。画风定标默认用项目主角做测试素材：

- `step4-style-calibrate.md` 改为画风×项目角色联合测试：用 `--character`（项目角色描述）+ `--character-image`（定妆图/OC图，图生图保证角色一致）传项目真实角色，验证"画风能否撑起这个角色"
- 仅排查"画风本身是否被执行"时才用中性素材（`--character` 不传）
- 测试素材章节新增"项目主角"缺省（Phase 0 未定角色时回退标准角色）
- 同步更新 SKILL.md Step 4 描述、铁律 ❌5（变量隔离扩展到"测试角色固定为项目主角"）

## v1.4.0 — 2026-08-04

### 新增：画风定标走固定脚本（固定 SOP + 并发批量）

把画风定标从"单张组装+单张生成+单张复现"改为"固定脚本并发批量"，杜绝每次测试全新设计、不稳定、慢：

- `step4-style-calibrate.md` 改为走固定脚本 `../pop-visual-shared/scripts/batch_test.py`：固定测试素材（变量隔离）+ 固定 6 段式模板 + 并发批量（默认 8 线程）+ 自动 `pe-log.json`
- 变体从 DNA 库按画风名批量取（`--style-names`），或 `--config` 精调（`--config` 只改一个子维度回炉）
- 稳定复现验证改为同 seed 重跑脚本，输出按 `seed-{seed}` 分级，天然复现对比
- SKILL.md 更新：Step 4 描述、铁律 ❌9、速查表（batch_test.py）
- 红线：定标必须走固定脚本，禁止现场手写提示词、单张串行

## v1.3.0 — 2026-08-04

### 新增：Pinterest 参考图单张锚定 + 稳定复现工作流

- Step 1 新增 **Pinterest 参考图搜索（单张锚定）**：选定画风后搜 1 张最符合画风的参考图，落盘 `素材/ref-cache/`，路径记决策.md（一次搜索、全程复用）
- Step 4 新增 **稳定复现验证（核心）**：同 seed + 同提示词复现对比，确认画风稳定而非单次运气，未稳定复现不冻结
- 画风冻结时记录 **seed + 参考图路径**，下游复用同 seed 保证画风不漂移
- 明确参考图是"图资产"（整图 image 参数复用），不靠精确分离公式提炼文字
- SKILL.md 更新：Step 1/4 描述、铁律 ❌7/❌8、速查表、跨skill引用协议第7条
- 参考图复用粒度：**单张锚定**（老板拍板）

## v1.2.0 — 2026-08-04

### 新增：画风定标（Pipeline 语境下必做）

- 新增 `steps/step4-style-calibrate.md`：用**固定测试素材**渲染 1 张画风定标图（变量隔离）
- 画风第一次被眼睛看到，验证 DNA 是否被 Seedream 准确执行
- 新增 🚪 **画风定标验收门禁**（辨识度/配色/光影/无文字）
- 用户认可 → **冻结画风三字段为基线资产**（`素材/风格/画风决策.md` 标 `✅ 已认可`）
- 未认可 → 回炉微调 DNA 片段，不冻结、不放行下游
- SKILL.md 更新：新增 Step 4、铁律 ❌5/❌6、速查表、跨skill引用协议第6条
- 独立纯文生图时跳过本步（Step 1→2→3 直接出图）

## v1.1.0 — 2026-08-04

### 接入共享底层资产层（瘦身清理）

- 删除本地 `scripts/generate.py` / `references/seedream-prompt-guide.md`，统一引用共享层 `pop-visual-shared`
- 6段式提示词结构迁移到共享库 `seedream-prompt-guide.md` §一（本 skill 保留 `style-dna-library.json` 与 `lighting-composition-templates.md` 域资产）
- SKILL.md 速查表 + step 文件引用路径切到 `../pop-visual-shared/...`

## v1.0.0 — 2026-08-01

### 新增
- 创建 `pop-visual-style` skill，定位为营销专家skill群的通用文生图引擎+画风DNA库共享基座
- 迁移36种画风DNA库（`references/style-dna-library.json`），含3光照模板+2构图模板+兼容性矩阵
- 创建 `references/seedream-prompt-guide.md`：6段式提示词结构（默认）+ V3结构化公式（备选）+ 高精度4块结构（商业级备选）
- 创建 `references/lighting-composition-templates.md`：3光照模板+2构图模板+三分法兼容性矩阵
- 创建3个step文件：画风选择→提示词组装→执行生成
- 复制 `scripts/generate.py`（Seedream/Seedance API调用脚本）

### 定位
- 独立执行纯文生图任务
- 作为cover/oc/comic skill的共享画风层引用源
- 不替代各skill的结构层和功能层
