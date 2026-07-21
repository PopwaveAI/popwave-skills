# CHANGELOG — pop-qidian-research

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
