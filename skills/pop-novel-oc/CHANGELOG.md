# CHANGELOG

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

接入 `pop-novel-asset` 基建 skill，Step 0 新增资产文件优先读取路径。

### 变更
- **step0-character-research.md** 新增 §0 资产文件检查：扫描 `素材/视觉资产/[角色名]角色档案.md`，存在则直接读取跳过原文采样，不存在则走原流程（回退路径）
- **SKILL.md** Step 0 描述更新为两条路径（优先路径+回退路径）
- 资产文件格式与 OC 内部10维度调研完全一致，读取后直接进入门禁A确认

### 兼容性
- 无资产文件时行为与 v1.0.0 完全一致（回退路径=原流程）
- 资产文件存在时省去原文采样环节，加速 OC 生成流程

## v1.0.0 (2026-07-30)

从 `pop-novel-visual` v2.6.0 拆分独立。专注 OC 角色立绘，新增角色调研管线和系列化输出。

### 从 pop-novel-visual 继承
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
- 封面图模式（已拆分到 `pop-novel-cover`）
- 场景图模式（已拆分到 `pop-novel-cover`）
- 普通素材模式（已拆分到 `pop-novel-cover`）
- 视觉模式路由总览（单一模式无需路由表）
- novel-visual-design.md（封面设计库，OC不需要）

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-character-research.md, step1-design.md, step2-generate.md
- references/: mode-character.md, character-research-guide.md, seedream-prompt-guide.md
- templates/: design-plan-oc.tpl.md
- scripts/: generate.py, pinterest_search.py
