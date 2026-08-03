# CHANGELOG

## v1.4.1 | 2026-08-04

### 出图尺寸硬上限（防止报价翻倍）

- `steps/step2-generate.md` 尺寸走共享 `seedream-prompt-guide` §八 的 236 万铁律（Seedream 5.0 Pro 计费临界，超限报价翻倍）；`generate.py` 内置 `assert_size_safe` 校验，超限报错中止

## v1.4.0 | 2026-08-04

### 参考图吸收策略重构：从"精确分离"改为"放开吸收"

基于 R14 言情封面测试定稿反馈（用户反馈"画风吸收过于保守，精确分离公式'不参考'列太多，等于没参考"），重构画风参考点的提示词公式。

**变更**：
- `steps/step2-generate.md` §2.2 策略二 + §3.3：画风参考公式从"精确分离"（排除人物/姿态/服饰/场景/构图/配色，6项不参考）改为"放开吸收"（参考画风质感+色彩系统+光影氛围+人物精致度，只排除具体场景内容+人物长相）
- §2.1 策略决策核心表：画风行"控制维度"从"画面内容+配色+构图+光影+字体"收窄为"画面内容+构图+字体"，放权维度改为"画风质感（笔触+色彩系统+光影氛围+人物精致度）"
- §6 降级机制 + §9 迭代表：画风吸收不足时改为"放开吸收范围/删掉仅排除限制"，替代"强化仅参考要素"
- `steps/step0-research.md` §3.2：参考点"画风"选项描述扩展为"笔触/质感/色彩系统/光影氛围/人物精致度"
- `SKILL.md` 铁律 ❌3：参考点放权一致性补充"画风参考=放开吸收，禁止堆'不参考'清单"

**原则**：参考图吸收采用"正向吸收 + 最小排除"——吸收要素明确列出（笔触技法/色彩倾向/光影语言/人物精致度），只排除会破坏画面主体的两样（具体场景内容/人物长相），其余姿态/服饰/构图/色彩允许参考图自然传导，才能真正吸收画风。

## v1.3.0 | 2026-08-04

### 接入共享底层资产层（瘦身清理）

- 删除本地 `scripts/generate.py` / `scripts/pinterest_search.py` / `references/seedream-prompt-guide.md`，统一引用共享层 `pop-visual-shared`
- SKILL.md 速查表 + step 文件引用路径切到 `../pop-visual-shared/...`
- 消除与 oc/style/comic 的脚本与提示词指南重复维护

## v1.2.1 | 2026-07-31

### 移除品牌签名提示词需求

水印生成不稳定，改走工程化方案。

**清除范围**：
- `references/seedream-prompt-guide.md`：删除 §1.11 品牌签名规则整节、§1.10 块3/块4/完整示例中的 popwave 引用
- `steps/step2-generate.md`：自检项移除品牌签名检查

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

接入 `pop-visual-asset` 基建 skill，两个 Step 0 均新增资产文件优先读取路径。

### 变更
- **step0-scene-understand.md** 新增 §0 视觉资产检查：场景资产表→帧解构、角色档案→角色规格、视觉符号库→环境材质、IP视觉DNA→IP背景。有资产时§1帧解构变为"从资产帧清单选取+补充"
- **step0-research.md** §1.1.1 IP视觉DNA提取新增资产优先路径：`素材/视觉资产/IP视觉DNA.md` 存在时直接读取，跳过 WebSearch
- **SKILL.md** Step 0 描述更新为资产优先+回退双路径

### 兼容性
- 无资产文件时行为与 v1.0.0 完全一致（回退路径=原流程）
- 资产文件存在时省去原文解构和WebSearch环节，加速设计流程

## v1.0.0 (2026-07-30)

从 `pop-visual-base` v2.6.0 拆分独立。专注封面图 + 场景图 + 普通素材三种视觉模式。

### 从 pop-visual-base 继承
- 三段流程（搜图选图/原文理解 → 设计方案 → 生成）
- 两个用户对齐门禁（门禁A选图+参考点 / 门禁B方案确认）
- 参考点驱动提示词策略
- 场景图原文理解管线（五层）
- 高精度提示词模板（4块结构）
- IP背景提取（同人/改编视觉DNA）
- Pinterest 3维度搜索
- 迭代模式（快速路径）

### 移除
- 人物立绘模式（已拆分到 `pop-visual-oc`）
- 视觉模式路由总览（visual-mode-guide.md，三模式无需路由表）
- 立绘相关的设计方法论和提示词结构

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-research.md, step0-scene-understand.md, step1-design.md, step2-generate.md
- references/: mode-cover.md, mode-scene.md, mode-scene-art.md, novel-visual-design.md, seedream-prompt-guide.md
- templates/: design-plan.tpl.md
- scripts/: generate.py, pinterest_search.py
