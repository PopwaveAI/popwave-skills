---
name: pop-visual-pipeline
description: "当用户说'视觉管线/视觉pipeline/小说视觉化/做视觉工程/继续视觉/下一步(视觉)/出封面/出OC/出漫画/出场景图'时启用。读视觉项目总控.html→按Phase 0-6路由调度各visual子skill（asset/style/art-bible/cover/oc/comic）。像起点管线一样，总控只做路由，子skill干活。"
---

# pop-visual-pipeline

> 小说视觉化总控管线。Phase 0→6路由调度。把 7 个 visual 子 skill 串成一条工程流：**基建层（查原文→定画风→产出美术设定集）是必做地基，派生层（封面/OC/场景/漫画）按需产出**。**意图闸口前置——先确认本次目标（封面/OC/漫画），按 intent 决定基建档位，不默认推漫画**。v3.0.0：steps 全合入，SOP 全内联。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

---

## 做什么

pipeline 只做路由不干活——读视觉项目总控.html判断 phase→路由到对应子 skill→完成后更新 html（职责边界见红线2）。

输入：项目名或当前项目目录（mode=fresh/import/resume）
输出：标准化目录结构 + `视觉项目总控.html`（唯一状态文件）

**核心价值**：把"**查原文+定画风+产出美术设定集=基建**"铁律固化成工程流——visual 群原是 7 个无顺序约束的散点 skill，会"没定画风就先画封面"乱序。

---

## 怎么操作（SOP全内联）

### Step 0 初始化（state=init 且无已有文件）

只做地基：创建标准目录+生成视觉项目总控.html+自检。

**1. 项目空间探测**（LS 扫描项目根）：`项目总控.html`（起点）/`project-state.md`（番茄）=写作专家项目，原文 `正文/ch*.txt`，import 走 Step 1｜`原料/小说原文/`（单个完整 txt）=独立小说项目，init｜用户指定路径=临时模式，init。

**2. 🚪 意图闸口（前置，决定基建档位）**：`AskUserQuestion` 或书面提问确认本次目标，intent 写入总控 `<!--STATE:intent -->` 全链路按档位路由——`cover` 做封面/场景图（轻量：场景资产表+视觉符号+画风，刊物角色可跳过双角度定妆）｜`oc` 做人物OC/立绘（轻量~中：角色档案+身份卡+画风，可跳过双角度定妆）｜`comic` 做漫画/连载（完整：深度角色档案+画风定标+身份卡+双角度定妆）｜`full` 全套视觉工程（完整基建）｜`asset-only` 只提取资产（最轻，只跑 asset 不进派生层）。**未明确时不默认漫画，回问用户**——只有明确说"做漫画/连载"才走 `comic` 完整档。

**3. 创建标准目录**（LS 确认，不存在则创建；分区口径见 `references/落盘规范.md`）：

```
{项目}/正文/
{项目}/素材/视觉资产/      # 基建真源：设定档案（asset 产出）
{项目}/素材/风格/           # 基建真源：画风决策 + 冻结定标图
{项目}/素材/ref-cache/      # 基建真源：Pinterest 参考图
{项目}/漫画/assets/characters/   # 漫画工程：定妆生产参考
{项目}/成品/                # 三态-成品：用户确认的对外发布图
{项目}/测试/                # 三态-测试：未确认候选/变体/定标/定妆初稿
{项目}/_过程/               # 三态-过程：原始图/脚本/任务清单/提示词记录
```

> **禁止**再建 `素材/视觉/` 扁平目录；候选/定标/复现一律按三态落盘（见红线6）。

**4. 生成视觉项目总控.html**：读 `templates/视觉项目总控.html` 全文复制到项目根，SearchReplace 填充 STATE 字段（`<!--STATE:xxx -->`）：`mode=fresh`｜`phase=init`｜`intent=意图闸口确认值`｜`project_name=项目名（用户输入或目录名）`｜`book_name`/`genre=待指定`｜`created_at`/`updated_at=当前时间`｜`next_step=Phase 0: 按意图档位读小说提取视觉资产`。

**5. 自检+路由 Phase 0**：9 个标准目录存在｜总控.html 生成且 STATE 字段正确｜phase=init，next_step=Phase 0。通过后调度 `pop-visual-asset` 执行 Phase 0，回到「路由循环」。

### Step 1 导入/续写（检测到已有项目文件，state=import/resume）

**import 是"补跑不重做"——已有资产保留，不覆盖重建**。

**1. 资产清点**（扫描项目根）：`正文/ch*.txt`（小说原文）｜`素材/视觉资产/[角色名]角色档案.md`（资产提取已完成）｜`素材/风格/画风决策.md`（画风已定）｜`素材/美术设定集.md`（基建真源）｜`成品/` `测试/` `_过程/`（已有派生图）｜`漫画/`（已有漫画产出）。

**2. 旧目录三态迁移（存量项目必做）**：检测到旧结构目录时，按 `references/落盘规范.md` §七迁移表归位，**禁止留在旧位置**。核心映射：`generated-images/`（原始 UUID 生成图）→`_过程/原始图/`｜`归档/旧版产出/`（未确认旧版图）→`测试/{类型}/`｜`归档/中间产物/`+`归档/工作脚本/`→`_过程/脚本任务/`｜`素材/视觉/`内确认对外图→`成品/{类型}/`（加`-final`）、未确认候选→`测试/`｜`素材/视觉设计方案.md`→`_过程/提示词记录.md`｜`素材/风格/`未冻结定标图→`测试/画风定标/`、已冻结定标图→原位保留（基建真源）。迁移后更新总控 `base_*` badge 与 `outputs` 为三态路径，动作落盘 `_过程/迁移记录.md`。

**3. 生成/更新总控+意图闸口**：有散落资产无总控→读模板生成并按清点结果填充 STATE；已有总控→直接读取更新。`intent` 空或未确认→`AskUserQuestion` 询问本次目标（见 Step 0 意图闸口）；已确认沿用不重复问。

**4. 落地 Phase 决策**（按清点结果）：有正文无资产/画风/设定集→**init**（从 Phase 0 补跑）｜有资产无画风/设定集→**phase1**（补跑 Phase 1 定画风）｜有资产+画风无设定集→**phase2**（补跑 Phase 2 产美术设定集）｜有美术设定集（基建完整）→**phase3+**（基建就绪按需进派生层）｜有基建+已有派生图→按用户意图派生层路由。

**5. 基建缺口补跑**：基建层（Phase 0/1/2）有缺口必须补齐才能进派生层——缺资产→`pop-visual-asset`｜缺画风→`pop-visual-style`｜缺美术设定集→`pop-visual-art-bible`。已有资产必须归位标准目录，禁止散落。

**6. 更新总控**：按 `references/html-update-protocol.md`（导入重建字段+Phase circle）更新 `phase`/`mode`/`updated_at`/`next_step`，已完成 phase circle 标 `done`。

### Step 2 路由循环（每次对话开始时）

1. Read 项目根 `视觉项目总控.html`，从 `<!--STATE:xxx -->` 标记提取 `phase`（当前阶段）、`intent`（本次目标）、`next_step`、`mode`。**先读 intent 再路由**——intent 决定基建档位与派生层去向；为空先走意图闸口（Step 0/1）
2. 对照「Phase 路由表」路由到对应子 skill 执行：
   - **基建层（phase0-2）**：主 agent 直接执行，读子 skill 的 SKILL.md（asset/style/cover 已单文件自包含；art-bible/oc/comic 仍带分步细节文件的需一并读取），按 SOP 操作
   - **派生层（phase3-6）**：主 agent 直接执行或派发子 agent（子 agent 指令要求见「执行模式」）
3. Phase 完成后按 `references/html-update-protocol.md` 更新 html（通用字段+phase circle+badge+产出表），再回到第 1 步判断是否还有下一步：
   - **基建层**：按顺序推进到 intent 档位所需深度——`cover`/`oc` 到 phase2（美术设定集）即基建完成可派生；`comic`/`full` 到 phase2 且完整复现完成（双角度定妆/场景定妆）才派生
   - **派生层**：按 intent 路由，完成后回读总控判断是否还有派生目标（`full` 档才 loop）。**不默认推漫画**——intent 是 `cover`/`oc` 时基建完成后直接进对应派生，不自动进 phase6。用户中途改意图→更新 intent 字段后按新档位路由

### Phase 路由表

> **两段式架构**：Phase 0-2 是**基建层**（必做，顺序不可跳），Phase 3-6 是**派生层**（按需，在基建就绪后任意触发）。

| Phase | 调用Skill | 定位 | 前置检查 | 产出 |
|:--|:--|:--|:--|:--|
| **0** | `pop-visual-asset` | 查原文 | state=init/import+正文文件就绪 | `素材/视觉资产/`（角色档案+场景资产表+视觉符号库+IP视觉DNA） |
| **1** | `pop-visual-style` | 定画风 | 资产就绪 | `素材/风格/画风决策.md`（选定基准+配色+风格串）+ **画风定标图** |
| **2** | `pop-visual-art-bible` | 产美术设定集 | 资产+画风就绪 | `素材/美术设定集.md`（画风/人物/场景/符号/一致性五篇合一，全下游唯一真源）+ **复现资产（定妆图/场景图）** |
| **3** | `pop-visual-cover` | 封面图 | 基建就绪 | 候选→`测试/封面/`，确认→`成品/封面/` |
| **4** | `pop-visual-oc` | 人物OC | 基建就绪 | 候选→`测试/{类型}/`，确认→`成品/{类型}/` |
| **5** | `pop-visual-cover`(场景) | 场景图 | 基建就绪 | 候选→`测试/场景/`，确认→`成品/场景/` |
| **6** | `pop-visual-comic` | 漫画 | 基建就绪 | `漫画/`（定妆图+分镜+漫画页+HTML） |

> **派生层触发（按 intent）**：Phase 3-6 非线性，由 intent 决定去向——`cover`→Phase3/5，`oc`→Phase4，`comic`→Phase6，`full`→loop 3-6，`asset-only`→停在 phase0。

---

## 📦 可调度 Skill 清单

7 个 visual 子 skill 见「Phase 路由表」（与 `skill.json` 的 `skills` 数组一致）。视觉 group 是**小说漫画专家的一部分**而非独立专家，部分 skill 会被其他专家复用。

---

## 🚪 首次对话引导（onboarding）

首次触发视觉专家（无任何视觉项目、非续写）时，先在回复中**直接粘贴 `references/onboarding-guide.md` 全文**建立认知（声明本次为功能介绍+引导、未执行任务），用 1-2 句补充"报书名+形态就开始"；用户已明确要开做则跳过直接干活。派生层不单独引导，统一由本 pipeline 总入口。

---

## 执行模式

**主 agent 直执**。Step 0/1 初始化与路由循环均由主 agent 直接执行；子 skill 的实际干活环节由主 agent 读其 SKILL.md 后按 SOP 操作，或（派生层 phase3-6）派发子 agent 执行——子 agent 指令必须显式要求读取对应 SKILL.md，禁止凭记忆"扮演"。pipeline 自身无产出，不存在可派发的只读子任务。

---

## 红线

1. **读取协议**：每次对话第一件事读视觉项目总控.html获取当前 phase+intent→按路由表调度，禁止跳过读 html 直接干活。视觉项目总控.html 是唯一状态文件，禁止另建 project-state.md。
2. **pipeline 只做路由不干活**——所有产出由下游 skill 生成。pipeline 不直接提取资产/选画风/产出美术设定集/画图/生成漫画。
3. **基建依赖链+就绪门禁不可跳**——资产没就绪不进定画风，画风没就绪不进美术设定集；进派生层（Phase 3-6）前必须验证美术设定集（`素材/美术设定集.md`）存在且签核 ✅ 已认可、画风决策签核 ✅ 已认可。未签核=报错中止，提示先跑基建并完成设定集冻结。
4. **美术设定集是唯一真源**——派生层（cover/oc/comic）只消费美术设定集，禁止各自重建人物/场景/符号/画风。视觉事实改动必须回 art-bible 升级设定集版本。
5. **意图闸口前置，不默认推漫画**——intent 为 `cover`/`oc`/`asset-only` 时不自动进漫画；未明确意图时回问用户，禁止假设用户奔漫画去。
6. **落盘三态强制（`references/落盘规范.md`）**——所有派生产出按生命周期落盘：候选→`测试/{类型}/`，确认→`成品/{类型}/`（加 `-final`），脚本/原始图/任务清单→`_过程/`。禁止再写扁平 `素材/视觉/`、禁止 UUID dump 到 `generated-images/`、禁止 `-V1`/`--v1` 版本变体。

---

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `references/html-update-protocol.md` | phase 完成后更新 html 时（含 Step 0/1 落地） | STATE 字段 SearchReplace 规范+Phase ID 表+badge 表（单源） |
| `视觉项目总控.html`（项目空间） | 每次对话第一件事 | 唯一状态源（phase+intent+next_step+就绪状态+产出表） |
| `references/落盘规范.md` | 任何落盘/迁移/命名时 | 三态分离+统一命名+版本 final 标记+skill 映射+旧目录迁移表 |
| `references/onboarding-guide.md` | **首次触发视觉专家时输出** | 首次对话引导语（功能全景+意图闸口+引导第一步） |
