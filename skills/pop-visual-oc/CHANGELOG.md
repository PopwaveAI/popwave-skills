# CHANGELOG

## v2.0.0 | 2026-08-08

### 新增：设定卡传播版档位（对标竞品主流传播形态）

对标破译 471 张竞品素材发现——**角色设定卡（Character Sheet）是社交媒体漫改赛道的主流形态**，竞品把"角色立绘 + 属性栏 + 配色板 + 表情差分 + 花语象征 + 境界徽章"做成可识别、可传播、可二创、可收藏的独立物料。我方此前只做了"生产参考（定妆图）"+"角色名片（立绘OC）"两层，本次补齐第三层**传播物料**。

- `references/mode-character.md` 新增「设定卡传播版」章节：三档位表、与立绘OC本质区别、7大模块化信息架构、模块化布局模板、花语象征库（赛道对照8组）、境界徽章、文字密度控制、AI画风做减法差异化原则
- `steps/step1-design.md` 新增 §3.0 档位选择 + §3.3 设定卡传播版模块化设计；门禁B模板新增档位与模块化信息区块
- `steps/step2-generate.md` 新增 §2.3.1 设定卡传播版模块化文字层翻译；自检新增模块完整项
- `templates/design-plan-oc.tpl.md` 档位字段更新为三档；新增模块化信息表
- `SKILL.md` 输出/流程/Step1/布局更新为三档位；新增铁律 ❌8（文字密度铁律）+ ❌9（AI画风做减法）；速查表新增传播版方法论入口
- `skill.json` 版本至 v2.0.0，描述含三档位，slashCommands 新增"设定卡/传播卡"
- 版本同步：SKILL.md / skill.json 至 v2.0.0

## v1.9.0 | 2026-08-06

### 修复：OC 提示词禁止携带 no text（身份卡冻结提示词污染）

老板发现——OC 消费身份卡冻结提示词时，把「定妆图专用」的 `no text, no letters, no characters, no watermark, no decorative elements, no border, no seal` 原样带进了 OC 提示词，压制 EXACT TYPOGRAPHY，导致立绘渲染不出文字，退化成定妆照。

- `steps/step2-generate.md` 新增 §2.2.1「消费身份卡冻结提示词：去 no text，加 EXACT TYPOGRAPHY」：剥离文字禁止词 → 保留人物本体描述 → 补回 EXACT TYPOGRAPHY 六层信息架构 → 校验无文字禁止词残留
- `steps/step2-generate.md` 自检新增 2 项：无文字禁止词残留 + EXACT TYPOGRAPHY 完整
- `SKILL.md` 新增铁律 ❌7「OC 提示词禁止携带 no text」；Step 2 描述补充剥离 no text / 补回 EXACT TYPOGRAPHY 的要求
- 版本同步：SKILL.md / skill.json 至 v1.9.0

## v1.8.0 | 2026-08-05

### 消费链路对齐：oc 意图 = 轻量~中基建

老板审视全链路发现——oc 消费链路未声明档位，需明确 oc 意图只需基建到身份卡即可派生，不强制双角度定妆：

- `SKILL.md` Step 0.5 新增档位说明：Pipeline 语境下 oc 只需身份卡（轻量~中档），**不强制双角度定妆**；如需角色参考图用 character 单张定妆图（版本一致性校验❌6 仍生效）
- 版本同步：SKILL.md / skill.json 至 v1.8.0

## v1.7.0 | 2026-08-05

### 生图改走 image_generate 工具，移除内置 API Key

老板要求所有 skill 生图环节改用 `image_generate` 工具，清理硬编码 API Key（Pinterest 搜索保持不动）：

- `steps/step2-generate.md` §4：由「执行 API 脚本」改为 `image_generate` 工具调用，移除 `generate.py` 直连与内置 key 说明
- `SKILL.md` 模型说明表：改为「静态图片走 `image_generate` 工具，无 API Key」
- `skill.json` 描述：移除「调用 Seedream API」
- 版本同步：SKILL.md / skill.json 至 v1.7.0

## v1.6.0 | 2026-08-04

### 澄清：定妆照 vs 立绘OC + 版本一致性校验

老板定调：立绘OC有图有字有各种文化元素，定妆照是纯生产参考（前后不是同一个版本所以有gap）。OC 必须与定妆照严格区分并保持一致。

- SKILL.md 新增「定妆照 vs 立绘OC」对比表：立绘OC=展示作品/角色名片（含文字+文化元素），定妆照=纯生产参考图（无文字/无装饰/无文化元素）
- SKILL.md Step 0.5 新增**版本一致性校验（防 gap）**：读取身份卡记录的最新定妆图版本，禁止沿用旧版参考图，身份卡升级后必须用最新版重新生成
- SKILL.md 铁律 ❌5 强化为"立绘必须含文字+文化元素"（增值：肖定妆照本质区别）
- SKILL.md 新增铁律 ❌6 **必须使用最新版本定妆图**（防跨版本 gap）
- 版本同步：SKILL.md / skill.json 至 v1.6.0

## v1.5.1 | 2026-08-04

### 出图尺寸硬上限（防止报价翻倍）

- `steps/step2-generate.md` 参数表 size 行明确：常用 1125x1500=3:4，总像素须 ≤ 236 万（Seedream 5.0 Pro 计费临界，超限报价翻倍）；`generate.py` 内置 `assert_size_safe` 校验

## v1.5.0 | 2026-08-04

### 参考图吸收策略重构：模式B从"精确分离"改为"放开吸收"

与封面 skill 同步 R14 画风吸收经验（用户反馈"画风吸收过于保守，精确分离公式'不参考'列太多，等于没参考"）。

**变更**：
- `steps/step2-generate.md` 模式B：画风参考公式从"精确分离"（排除人物/姿态/服饰/场景/构图/配色，堆"不参考"清单）改为"放开吸收"（参考画风质感+色彩系统+光影氛围+人物精致度，只排除具体场景内容+人物长相）
- 关键：**"人物长相"排除正好保护角色一致性**——冻结特征不受参考图影响，系列图仍保持同一人；LOCKED COMPOSITION 块锁定构图，角色站位/姿态由提示词控制
- 降级机制 + 自检 + 迭代表：模式B画风吸收不足时改为"放开吸收范围/删掉仅排除限制"
- `SKILL.md` Step 0 可选Pinterest参考：标注画风参考默认用放开吸收公式

**原则**：参考图吸收分为"画风传导"（放开吸收，默认推荐）与"内容隔离"（精确分离，仅角色一致性/完全隔离场景时用）。OC 的"人物长相"天然属于内容隔离范畴，与放开吸收的"仅排除人物长相"边界一致，二者不冲突。

## v1.4.0 | 2026-08-04

### 接入共享底层资产层（瘦身清理）

- 删除本地 `scripts/generate.py` / `scripts/pinterest_search.py` / `references/seedream-prompt-guide.md`，统一引用共享层 `pop-visual-shared`
- 高精度模板引用从 `§1.10` 更新为共享库 `§三`（节号对齐）
- SKILL.md 速查表 + step 文件引用路径切到 `../pop-visual-shared/...`

## v1.3.0 | 2026-08-03

### 接入高级角色设计方法论（解决"千篇一律/廉价感"）

- **SKILL.md 速查表**：新增高级角色设计方法论入口 `skills/pop-visual-comic/references/advanced-character-design.md`（剪影/色彩/细节三层 + 反类型化 + 符号与行为撕裂感 + 五问提取法）
- **Step 1 设计环节**：所有主角/重要配角立绘，组装规格表前必须先读该文件，用"偏科"思维写规格表，禁止落入"黑发+白T+卫衣+牛仔裤+标准网感脸"的平均值陷阱
- 版本同步：SKILL.md / skill.json 至 v1.3.0

## v1.2.1 | 2026-07-31

### 移除品牌签名提示词需求

水印生成不稳定，改走工程化方案。

**清除范围**：
- `references/seedream-prompt-guide.md`：删除 §1.11 品牌签名规则整节、§1.10 块3/块4/完整示例中的 popwave 引用
- `steps/step2-generate.md`：移除品牌签名描述行、标注、自检项

## v1.2.0 (2026-07-31)

新增品牌签名规则：所有生成图片通过提示词在画面底部中央融入 "popwave" 品牌签名。

### 变更
- **references/seedream-prompt-guide.md** 新增 §1.11 品牌签名规则（强制），覆盖 V3 公式/高精度模板/基础公式/漫画分镜帧四种提示词模板
- **references/seedream-prompt-guide.md** §1.10 高精度模板 EXACT TYPOGRAPHY 块新增 [品牌签名] 元素
- **references/seedream-prompt-guide.md** §1.10 高精度模板 HARD CONSTRAINTS 更新：允许 popwave 品牌签名为唯一品牌标识
- **references/seedream-prompt-guide.md** 完整示例追加品牌签名文字元素
- **steps/step2-generate.md** 自检项新增品牌签名检查

### 兼容性
- 不影响已有提示词结构，品牌签名作为末尾追加项

## v1.1.0 (2026-07-30)

接入 `pop-visual-asset` 基建 skill，Step 0 新增资产文件优先读取路径。

### 变更
- **step0-character-research.md** 新增 §0 资产文件检查：扫描 `素材/视觉资产/[角色名]角色档案.md`，存在则直接读取跳过原文采样，不存在则走原流程（回退路径）
- **SKILL.md** Step 0 描述更新为两条路径（优先路径+回退路径）
- 资产文件格式与 OC 内部10维度调研完全一致，读取后直接进入门禁A确认

### 兼容性
- 无资产文件时行为与 v1.0.0 完全一致（回退路径=原流程）
- 资产文件存在时省去原文采样环节，加速 OC 生成流程

## v1.0.0 (2026-07-30)

从 `pop-visual-base` v2.6.0 拆分独立。专注 OC 角色立绘，新增角色调研管线和系列化输出。

### 从 pop-visual-base 继承
- 人物立绘设计方法论（六层信息架构+五种布局模板）
- 高精度提示词模板（4块结构）
- IP背景提取（同人/改编视觉DNA）
- Pinterest 搜索（可选，角色气质参考）
- 迭代模式（快速路径）
- mode-character.md 完整保留

### 新增
- **角色调研管线**（step0-character-research.md）：原文关键词搜索→上下文采样→10维度角色档案→门禁A确认
- **调研方法论**（character-research-guide.md）：系统化角色信息采样策略，10维度档案模板
- **系列化输出**：一份角色档案驱动N张系列图（形态演变/核心场景/群像关系），冻结核心特征+变化服饰场景
- **OC专属设计方案模板**（design-plan-oc.tpl.md）

### 移除
- 封面图模式（已拆分到 `pop-visual-cover`）
- 场景图模式（已拆分到 `pop-visual-cover`）
- 普通素材模式（已拆分到 `pop-visual-cover`）
- 视觉模式路由总览（单一模式无需路由表）
- novel-visual-design.md（封面设计库，OC不需要）

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-character-research.md, step1-design.md, step2-generate.md
- references/: mode-character.md, character-research-guide.md, seedream-prompt-guide.md
- templates/: design-plan-oc.tpl.md
- scripts/: generate.py, pinterest_search.py
