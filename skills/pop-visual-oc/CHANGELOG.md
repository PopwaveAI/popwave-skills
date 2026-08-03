# CHANGELOG

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
