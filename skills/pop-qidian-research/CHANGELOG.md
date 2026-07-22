# CHANGELOG — pop-qidian-research

## v4.3.0 — 2026-07-22

### 新增 decon-plot 剧情拆解档（第五档）

**核心改动**：在现有四档基础上新增第五档"剧情拆解档"（decon-plot），针对参考书进行6维度剧情结构拆解，服务下游 seed 和 plot 模块。

### 新增内容

- **SKILL.md 新增 decon-plot 剧情拆解档**：
  - 触发条件：用户提供参考书
  - 产出路径：`素材/decon-plot-{书名}.md`
  - 消费方：seed S1+S2 / plot R2+R3+R4+R5 / character C1
  - SOP骨架：DP1接收+采样 → DP2 6维度拆解 → DP3-DP4质检+存盘
  - 6个拆解维度：
    1. 力量体系对比（→seed S1）：参考书做法/优缺点/爽感差异
    2. 金手指设计对比（→seed S2）：加速比/限制设计/代价平衡
    3. Boss战设计（→plot R2）：铺垫时长/战斗阶段数/破局方式/临终反扑/爽感爆发点
    4. 爽感场景拆解（→plot R3）：信息差铺设/面板爆发节奏/越级杀节奏
    5. 分幕转折手法（→plot R4）：转折事件/节奏变化/读者冲击
    6. NPC登场效果（→character C1+plot R5）：出场方式/关系建立节奏/伏笔埋设手法
- **红线新增❌8**：decon-plot 6维度必须全拆，每个维度必须标注消费方。缺维度=不合格
- **速查表新增**：`steps/step-decon-plot.md`（decon-plot档·DP1采样+6维度拆解+质检门禁）
- **frontmatter description 更新**：新增"用户提供参考书时启用decon-plot剧情拆解"触发条件
- **header 更新**：三档→四档，版本标注 v4.3.0
- **execution.mode 更新**：decon-plot 加入"必须完整执行"列表

### 保留不动

- 现有四档（燃料+题材机制/decon-lite 9表拆书/赛道定位调研）的所有内容不动
- 红线1-7保留不动（仅新增红线8）
- step文件（step-1-find.md / step-2-output.md / step-decon-lite.md / step-track-research.md）未改
- templates/（fuel-doc.tpl.md / mechanics-doc.tpl.md）未改
- agents/openai.yaml 未改
- `steps/step-decon-plot.md` 待创建（SKILL.md已引用，详细执行指令后续补充）

### 版本

- SKILL.md + skill.json + CHANGELOG.md 三处版本号同步为 4.3.0

## v4.2.0 — 2026-07-22

### SKILL.md规范重写

- 按skill-create规范重写SKILL.md（≤100行/读取协议红线/文件目录速查表/强弱加载声明）
- frontmatter description确认含触发条件（燃料/decon-lite/赛道调研三档触发词）
- 红线从10条合并为7条（删除meta红线：双文件/版本一致/Get-Content读取，新增读取协议为第一条；保留全部业务红线：不越界/燃料三要素/content-mechanics落盘/机制不伪装文风/9表全拆+表1规则级/表9三组成齐全）
- SOP从315行大幅压缩为档位引导（9表完整定义和四轮搜索详情留在step文件）
- 速查表保留文件目录格式（已有，确认合规）
- 强弱加载声明保留
- 版本只留最新一条，历史版本见CHANGELOG.md
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

### 保留不动

- step文件（step-1-find.md / step-2-output.md / step-decon-lite.md / step-track-research.md）未改
- templates/（fuel-doc.tpl.md / mechanics-doc.tpl.md）未改
- agents/openai.yaml 未改
- v4.0.0-v4.1.0全部业务设计保留

## v4.1.0 — 2026-07-22

### DL1.5采样算法升级v2.0 + 表1新增子养成线境界涌现字段

**核心改动**：三阶段采样算法从v1.0升级到v2.0，解决长篇后期子系统遗漏问题。表1新增"子养成线境界涌现"必填字段。

### 修改

- **DL1.5 三阶段采样算法 v2.0**：阶段3从"100章后每50章"改为"100章后每25章+境界过渡期必采"。新增境界过渡期信号词检测（突破/进阶/升阶/新境界/解锁/开启/获得等），该章及前后1章强制采样
- **关键词库扩展**：新增40+后期子系统关键词（道种/法骸/阵法/链法图/金丹跑分/碎丹/傀儡/版权/气运/仙门功法/元婴进化/空间技术/仙人后裔/妖裔化身/传人/真灵根/三眼神通/法宝工厂/道统/法条/宗务员/万法管家/借贷/元神/魂修/化神道体/崑仑/仙气/法条评估/道种谱/建造世界等）
- **表1新增"子养成线境界涌现"字段**：长篇(300+章)必填，按境界分组列出新涌子养成线+涌现逻辑+证据章
- **拆解要点新增子养成线境界涌现条目**：说明300+章长篇每个大境界突破都会涌现新子养成系
- **DL3质检采样范围已声明更新**：从"每50章抽样"更新为"每25章+境界过渡期必采"

### 验证来源

- 没钱修什么仙全量拆解：原v1.0"每50章"采样只覆盖到炼气境4条子养成线，完全漏掉后期37条
- v2.0"每25章+境界过渡期必采"：70章采样命中222991字符，成功覆盖全部41条子养成线
- 核心教训：长篇力量体系是动态演进的，采样必须覆盖每个大境界过渡期

## v4.0.0 — 2026-07-21

在原有燃料+题材机制档位基础上，引入 decon-lite 9表拆书 + 赛道定位调研两档位（从番茄research v2.2.0完整移植9表定义）。保留现有燃料+机制功能不动。

### 新增（decon-lite 9表拆书档位）
- `SKILL.md` 新增"流程·decon-lite"章节：完整移植番茄research v2.2.0的9表定义
  - 表1：力量体系结构（规则级深度）——主养成线+子养成线抽象，子养成线数量由书决定不固定字段
  - 表2：剧情节奏
  - 表3：情绪弧线
  - 表4：人称与视角策略
  - 表5：开篇解剖
  - 表6：势力格局（服务seed 1d-0改编策略层"势力替换"维度）
  - 表7：金手指深度（服务seed 1d-0改编策略层"金手指形式"维度）
  - 表8：世界危机引擎（服务seed 1d-0改编策略层"世界危机"维度）
  - 表9：动力引擎提取表（服务seed 1e动力引擎设计，基于24本男频小说验证，五种范式：飞轮型/探索型/混合型/压迫型/对抗型）
- `steps/step-decon-lite.md`：DL1接收需求→DL2九表拆解→DL3质量门禁→DL4存盘返回
- 产出路径：`素材/decon-lite-{书名}.md`
- 消费方：seed 1d 力量体系设计 + seed 1e 动力引擎设计 + seed 1d-0 改编策略层 + seed 故事纲领（节奏参考）

### 新增（赛道定位调研档位）
- `SKILL.md` 新增"流程·赛道定位调研"章节：移植番茄research的4轮搜索流程
  - 第1轮：赛道格局（top作品核心卖点）
  - 第2轮：读者偏好（借鉴点+避雷点）
  - 第3轮：赛道演变（细分赛道格局）
  - 第4轮：对标分析（如有用户指定对标书）
- `steps/step-track-research.md`：S1接收需求→S2四轮搜索→S3产出落盘→S4质量门禁
- 产出路径：`素材/赛道调研.md`
- 消费方：seed 1d 双轨发散（王道赛道借鉴+避雷）+ plot 三源合流（赛道参考第一源）

### 红线更新
- 保留现有7条红线不动
- 新增❌8：decon-lite 9张表必须全拆，不能只拆部分表
- 新增❌9：decon-lite 表1必须拆到规则级（主养成线+子养成线+chXX出处）
- 新增❌10：decon-lite 表9动力引擎三组成（驱动逻辑/运转机制/代价结构）必须齐全

### 速查表更新
- 新增 decon-lite 档位的文件读取指引（`steps/step-decon-lite.md`）
- 新增 赛道定位调研 档位的文件读取指引（`steps/step-track-research.md`）

### 版本
- SKILL.md + skill.json + CHANGELOG.md 三处版本号同步为 4.0.0

### 保留（未修改）
- `steps/step-1-find.md`：燃料+题材机制分流流程，保留不动
- `steps/step-2-output.md`：燃料+机制文档落盘流程，保留不动
- `templates/fuel-doc.tpl.md`：燃料文档模板，保留不动
- `templates/mechanics-doc.tpl.md`：机制文档模板，保留不动
- `agents/openai.yaml`：保留不动
- 现有燃料+题材机制功能完全保留，不受 v4.0.0 升级影响

---

## v3.5.0 — 2026-07-06

四层架构对齐 PRD v3.5 契约层（`../pop-qidian/references/v3.5-pipeline-prd.md` §4）。

### 新增（四层架构）
- `SKILL.md` 重写为路由层（≤60 行）：红线 7 条 + 速查表 + 强弱加载保障 + 版本
- `steps/step-1-find.md`：找燃料 + 题材机制分流，末尾门禁 + 下一步指引
- `steps/step-2-output.md`：落盘 research-写作燃料.md + content-mechanics.md
- `templates/fuel-doc.tpl.md`：燃料文档空模板（含元数据块）
- `templates/mechanics-doc.tpl.md`：content-mechanics 空模板（含元数据块）

### 修复（对齐 PRD §4 契约层）
- **content-mechanics.md 由"分流建议"升级为正式落盘**（owner=research，PRD §4.2）— 核心修复（问题 3）
- 删除自有 execution.mode 三档表，统一引用 PRD §4.5
- 采用 PRD §4.7 统一回复格式
- 骨架/owner/命名引用 PRD §4.1/§4.2/§4.3，不在本 skill 重复定义
- 燃料文件唯一名 `research-写作燃料.md`，禁用 `燃料库.md` 别名（PRD §4.3）

### skill.json
- 补全 displayName / entry / activation / permissions 字段
- 版本 1.1.0 → 3.5.0

### 保留
- `agents/openai.yaml` 保留不动
