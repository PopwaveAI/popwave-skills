# CHANGELOG

## v1.6.0 | 2026-09-08

### 全面对齐 snow 四 skill 新版产物结构（seed 14维/stage 七长档/plot 卷进度表）

> **背景**：老板发现 pipeline v1.5.3 的 状态.md 模板、资产归位表、就绪判定、Phase 1 路由仍引用旧三件（01-命运图/02-命运图plus/03-全书大纲）——四 skill 重推演后 pipeline 没跟上。

- **立项位**：就绪判定 `01/02/03 三件齐` → `00-融合立项稿14维.md`（旧三件齐也可，调度 seed 转写）；Phase 1 路由 "三输入路径A/B/C→共创三层" → 六步流水线共创《融合立项稿14维》；状态.md 模板 `立项就绪: 命运图/命运图plus/全书大纲` → `融合立项稿14维`；seed_path 字段删除（A/B/C 路径已废）。
- **舞台位**：就绪判定旧七件（力量体系/动力引擎/全书设定/金手指/角色库/主线/卷一舞台）→ stage v2.0.0 七长档八件（世界全书/力量体系/位阶坐标谱/势力格局/基调母题/主角/角色库/类型风味）；归位表按七长档平铺重排（金手指并入主角.md、动力引擎归素材/、世界设定→世界全书.md）；Step 1 目录创建去掉 `全书设定/`、`角色库/` 子目录。
- **剧情位**：`主线.md` → `卷纲/00-全书卷进度表.md`（plot 任务P）；落地Phase "正文无+主线有" → "正文无+卷进度表有"；补跑顺序 plot 链前插卷进度表；速查表 plot 行加进度表。
- **展示面板（项目总控.html）同步**：立项字段"立项PRD（六要素）"→"融合立项稿14维"；舞台 7 项→8 项七长档（stg_0-7）；"白描卡+状态快照"→"章日志+全书日志"；目录树整块重画（旧的"01-立项PRD/产出/白描卡/状态快照"是三代前结构）。
- **doc profile 服务对象**：`seed L0-L3` → `seed 融合立项稿`，plot 产物加卷进度表。
- 同步 skill.json version 1.6.0。

## v1.5.3 | 2026-09-08

### deai_gate 升 v3.4：中文AI味词库广泛搜索轮（v3.3）+ Humanizer 35条军规比对补漏（v3.4）+ wiki 语境校准（v3.4.1）+ 兜底同步审计（v3.4.2）

老板发来微信扒源文（Humanizer 开源项目，35 条 patterns 源自维基百科「Signs of AI writing」清单）："中文AI味的词库需要你广泛搜索和获取"。本轮把该文逐条比对 + 多源搜索一次做完：

- **v3.3 广泛搜索轮**（此前代码已改未记录，本条补账）：doc buzz_hard +34（企业黑话 全方位/一站式/顶层设计/降本增效/新质生产力…+ 宣传腔 亮眼/硕果累累/日新月异/如火如荼…+ 万能收尾 让我们拭目以待/未来可期/前景广阔/站在新的起点上…）；buzz_soft +35（流量腔 深耕/聚焦/飞轮/中台/突围/重构/拉齐…+ 拆书降级词 见证了/标志着/充满活力…）；formulaic +6（意义拔高链 标志着新篇章/开创先河/为…注入活力/奠定基础/树立标杆…+ 硬造对立再否定/从X到Y双从结构/尽管挑战但）；PAT_CONN +11 换词链（此外/不仅如此/更重要的是/归根结底…）；PAT_AI_META +13（知识截止免责/谄媚语气 好问题！您说得完全正确/客服短语 以上供参考敬请指正）；**body 新增 2 检测**：quote_mixed 引号体系混用 + md_hr 分割线残留（番茄拒签16万本实测七破绽之3/4）。
- **v3.4 Humanizer 军规逐条比对补漏**（35 条对照现有词库后的真实缺口）：hard +1 令人惊叹（军规4销售语言）；soft +5 象征着/折射出/映射出/印证了/坐拥（军规3浅层象征分析+军规8回避be动词）；formulaic +4 模糊来源（专家/观察人士认为）/假坦率开头（坦白说/平心而论）/虚假替代方案（一个诱人的选择）/公式化谚语（时代的注脚/缩影）；PAT_CONN +归根到底。**英文专属项不入库**（Title Case/弯直引号方向/加粗密度——wiki 工程文档加粗系约定俗成，检测即全量误报），此决策记录于脚本头注释。
- **v3.4.1 wiki 语境抽样校准**（扩容后 wiki 警报曾冲到 634，拆解发现专有名词碰撞）：封神→封神之作（961 命中全是封神演义知识库专有名词）；版图→题材/商业版图（569 命中全是"地理版图/势力版图"世界观字面义）；生态→内容生态；格局→格局宏大；矩阵→IP/产品矩阵（"爽点矩阵"是管线自身文件名）；删 破局/天花板/打通（剧情行话/力量体系术语/修仙字面义，slop 场景由 重新定义/全链路 兜住）。
- **回归三层全绿**：①负面样例 100% 召回（v3.3 六类+v3.4 十项+校准词全中）；②人书 A/B（v2.1 vs v3.4，8本×3段×2600字 seed42 对齐 _cal4 方法论）：23/24 样本 FAIL 集完全一致，唯一差异是 quote_mixed 抓到遮天源 txt 抓取损坏（「 顶替标点混入""体系）——真检测非误伤，v3.3+v3.4 对 body 老检查零漂移；③wiki/skills 复扫：wiki 293→311（+6%）、skills 93→99（+6%），校准前曾达 634/103，专有名词碰撞清零后增量全部为真实 AI 味报告信号。
- **v3.4.2 兜底同步审计**（老板提交前指令"检查脚本里有没有硬编码"）：本地路径/argparse 默认值零命中；抓出**兜底 DEFAULT_DOC_CFG 与 JSON 漂移 3 处**——①skip 缺 emoji_res（v1.5.2 决策"emoji_res 移出 doc 检测面"只落了 JSON 没同步兜底，A/B 实测证伪：JSON 在场 doc 跳过 emoji，JSON 丢失则 733 文件 ⚠️✅ 工程标记误报复活）；②doc.checks.emoji_res 死配置双清（skip 与 checks 自相矛盾）；③buzz_soft/ai_meta 两处 advice 文案对齐。修复后双向全字段比对一致，emoji 三路径 A/B（JSON-doc 跳过/兜底-doc 跳过/body 仍必改）+ 负面样例 6 项全中，零回归。
- 验证产物：`测试/doc-profile-验证/负面样例-词库扩充.md`（v3.4 段）+ `wiki-scan-v341.json`/`skills-scan-v341.json` + `temp/deai-v34-regression/`（人书回归脚本与 v2.1 基线抽取）。
- 同步三件套：SKILL.md（词库蓝本行）/ skill.json（version 1.5.3）/ CHANGELOG。

## v1.5.2 | 2026-09-07

### deai_gate 升 v3.2：词库盲区补齐——吸收 pop-ai-reduce-lite 全量禁用词资产

老板问"词库会不会漏了很多真正有AI味的但你不知道？参考 skill 里是不是有点查AI味的，都看看"。翻遍全库找到三座金矿：`pop-ai-reduce-lite`（李白润色专家 v2.0 整包，banned-words.md 21 节禁用词表+zh_rules.json 规则库）、`short-reviewer`（writing-styles.md 去味清单）。对比发现 doc 词库只吸收了 banned-words 的 2/21 节，盲区确实大。本轮补齐：

- **doc buzz_hard +6**：具有里程碑意义/划时代/蓬勃发展/欣欣向荣/举世瞩目/千行百业（体制夸大腔；"不可估量/举足轻重/压倒性"因剧情复述易误伤降 soft）。
- **doc buzz_soft +14**：不可估量/举足轻重/压倒性/彰显/凸显/展现了/高光/历史性/颠覆性/革命性/本质上/这意味着/独具匠心/引领。
- **formulaic +6**：首先…其次三段式/对于…而言/通过…的方式/以…的形式/值得深思式总结/万能感受（一阵莫名·说不出）。
- **PAT_CONN +6**（body/doc 共享）：需要指出的是/需要强调的是/不难看出/简而言之/客观来说/可以预见。
- **PAT_AI_META +13**（实锤级）：chatbot 签名档（希望以上内容/感谢您的阅读/以上就是…全部/如需进一步/欢迎随时提问/如有任何问题）+ 生成器引用残留（oaicite/turn0search/contentReference/utm_source=chatgpt/[citation）。
- **兜底对齐**：代码内 DEFAULT_DOC_CFG 与 JSON 同步（v3.1 时打法/认知差等降 soft 未同步兜底，JSON 丢失时行为会漂移）；词库蓝本注释更新为全量吸收。
- **回归四层全绿**：负面样例 35 项新增特征 100% 召回；body 人书回归 22 档 ai_meta/connectives 零命中（改动项零误伤）；wiki 重扫 with_warn 276→293（+6%，全为 soft/formulaic 报告级）、skills 89→93（+4.5%）；"以上就是"正文误报（"跨两境以上就是碾压"）收紧正则后清零。
- **自指豁免说明**：词库类文档（pop-ai-reduce-lite 词表/write 检测面说明）讨论特征词属合法引用，SKILL.md 边界三条注明。
- 同步三件套：SKILL.md / skill.json（version 1.5.2）/ CHANGELOG。

## v1.5.1 | 2026-09-07

### deai_gate 升 v3.1：目录级扫描+聚合热点，doc 报告闸接满 9 skill，wiki/技能文档全量实测校准

老板问"plot 是不是也要调，应该都要调吧；脚本本身值得优化吗，拿 wiki 资料包和 skill 文档试试，看是脚本问题还是文档本身重 AI 味"。本轮一次做完：

- **脚本 v3.0→v3.1**：新增目录递归扫描（`-r`，按扩展名过滤）+ 聚合 JSON 输出（`summary.by_check` 按检测项统计 / `top_files` 前15热点文件 / `top_buzz_words` 前30高频黑话词）；hits 逐条带 `match` 命中原文片段，word_freq 记词频。
- **词库校准**（`deai_profiles.json`，依据 wiki 1750 文件+skills 227 文件实测）："信息差/认知差/打法/方法论/链路"由 hard 降 soft（管线惯用语、正常使用不算装腔）；`emoji_res` 加入 doc skip（⚠️/✅ 工程标记不算 AI 残留）；`formulaic` warn 阈值 1→2（单处套路句式不报警）。
- **doc 报告闸接满 9 skill**：v1.5.0 已接 seed/stage/research，本轮补 plot（brief/卷纲/幕白描）、outline（章纲）、review（章日志/全书日志）、decon（沉淀提醒）、decon-dimension（L2 成品）、dna-style（文风锚定说明文字）红线。工程标签（幕功能位/卷末边界/不能抢的收益等精确技术名）不在消毒范围。
- **全量实测**（`测试/doc-profile-验证/`）：wiki 1750 文件警报 1025→276（-73%），skills 227 文件警报 148→89；负面样例（黑话装腔）buzz_hard/soft+formulaic+hollow 全命中不漏检；doc profile 下"维度=454/张力=169/锚定=144"等高频命中多为拆书术语与正常文学批评词汇，属 soft 报告级，由 agent 自查放行——结论：脚本召回完好，剩余警报主要是真实风格分层而非误报。
- **SKILL.md**：doc profile 行更新（9 skill 服务对象 + `-r` 递归用法）。
- 同步三件套：SKILL.md / skill.json（version 1.5.1）/ CHANGELOG。

## v1.5.0 | 2026-09-07

### 去AI味门禁 deai_gate.py 迁入：本包统一管理，双 profile 服务全管线

老板拍板："门禁是跨 skill 的（research/seed/stage 也产文档都要闸），不该绑死 write 一家，挂 pipeline 统一管线总控"。本轮迁移+扩容：

- **脚本迁入**：`scripts/deai_gate.py` 从 pop-snow-write（v2.1）迁入并升 v3.0——新增 `--profile doc` 非正文向（报告闸：只 WARN+定位，不打回；分号/破折号/括号/列举行/0%对话放行），重点检黑话（hard 实锤/soft 风格分层）+套路句式+空腔段；阈值与词库外置 `scripts/deai_profiles.json`。
- **body 行为零变化**：正文向检测/修复面与 v2.1 一致（8本人书×3段回归零差异），write 仅换调用路径（配套 write v1.9.0）。
- **SKILL.md 新增「落盘质量闸」节**：双 profile 规范表+边界三条（工程标签不消毒/自动修仅机械项/doc 由 agent 判断放行）+阈值调校入口；红线加第7条"门禁归本包，各 skill 只调用不复制"；速查表加行。
- **下游接线**（配套 seed v4.1.0 / stage v1.5.0 / research v3.2.0）：三者红线各加"落盘后自跑 doc 消毒报告"。
- **验证**：负面样例（黑话装腔）buzz_hard/soft+formulaic+hollow 全命中；干净叙事样例（测试/深渊主宰-全链路重造验证 01-03）零误杀；doc `--fix` 最小清理不伤 markdown 结构与工程标签。

## v1.4.0 | 2026-09-04

### 账本命名对齐「章日志/全书日志」（配合 review v1.4.1 / write v1.5.1）

review 侧已把"白描卡/状态快照"统一为「章日志/全书日志/退出档案」，pipeline 的资产归位表/缺口分析/状态机仍挂旧名，消费会对不上。本轮全量对齐：

- **归位表**：`产出/白描卡/`（审核沉淀）→ `章节日志/`；`产出/状态快照.md` → 项目根 `全书日志.md`；"幕白描与审核白描卡易混"→"幕白描与章日志易混"。
- **缺口分析/落地Phase**：2f 就绪判定改 `章节日志/`+`全书日志.md`；"正文有+白描卡有+状态快照有"→"章日志有+全书日志有"；"双文件缺"→"账本缺（章日志/全书日志）"。
- **0f 补跑**：reconstruct 产出改 `章节日志/ch{NNN}.md`+`全书日志.md`；降级模式"在状态快照手动指定"→"在全书日志手动指定"。
- **目录创建**：`产出/`（含 `白描卡/`）→ `章节日志/`。
- **状态.md 模板**：就绪态"双文件[ ]"→"章日志[ ] 全书日志[ ]"。
- **状态机 2f 行 + 红线2 依赖链**：同步改章日志/全书日志。

同步三件套：SKILL.md / skill.json（version 1.4.0）/ CHANGELOG。

## v1.3.0 | 2026-09-03

### 固化"每章闭环"（防止路由绕错）

在卷循环状态机顶部新增「每章闭环」小节，显式固化每章五步循环，修正 review→next write 直读日志的误路由：

- `outline 章纲 → write 正文 → review 三件事（①定稿 ②章日志 ③全书日志） → 回到 outline 写 ch{NNN+1} 章纲 → …`
- 明确：review 产物（章日志/全书日志/退出档案）喂给**下一章的 outline**当章纲依据，**不是直接喂 write**；write 永远跟在章纲之后，不得跳过 outline。
- 对应位：`2d(outline)→2e(write)→2f(review)→回 2d`；本卷末章→2g。
- 与 pop-snow-review v1.4.0（收敛为三件事·章节验收归档）对齐。
- 同步三件套：SKILL.md / skill.json（version 1.3.0）/ CHANGELOG。

## v1.2.0 | 2026-08-31

### 意识层 + wiki 站取源

- 新增「心智前置·意识层」节（Know-Gap/Pack/Worth/Deepen + 取材预算硬上限），贯穿本 skill 与全流程。
- wiki 取源统一走网站 https://wiki.popwave.cn（替代本地 D:\popwave-wiki\docs 镜像 / sync.ps1）。

## v1.1.2 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份定位"一次性安装器"→"一次性搭建"，description 精简
- 引语与版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version/description）

## v1.1.1 | 2026-08-31

### 更名：pop-pipeline → pop-snow-pipeline

- 雪花流家族徽记：统一管线 8 件 skill 加 snow 中间名，与旧族 pop-fanqie-*/pop-qidian-* 区分（老板 2026-08-31 拍板）；test 系列 5 件（adapt/lite/plot/research/write）同批删除退役（备份 temp/_backup-test-20260831/）
- name/version/全仓引用同步；功能零变化

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
