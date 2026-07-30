# CHANGELOG

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

接入 `pop-novel-asset` 基建 skill，两个 Step 0 均新增资产文件优先读取路径。

### 变更
- **step0-scene-understand.md** 新增 §0 视觉资产检查：场景资产表→帧解构、角色档案→角色规格、视觉符号库→环境材质、IP视觉DNA→IP背景。有资产时§1帧解构变为"从资产帧清单选取+补充"
- **step0-research.md** §1.1.1 IP视觉DNA提取新增资产优先路径：`素材/视觉资产/IP视觉DNA.md` 存在时直接读取，跳过 WebSearch
- **SKILL.md** Step 0 描述更新为资产优先+回退双路径

### 兼容性
- 无资产文件时行为与 v1.0.0 完全一致（回退路径=原流程）
- 资产文件存在时省去原文解构和WebSearch环节，加速设计流程

## v1.0.0 (2026-07-30)

从 `pop-novel-visual` v2.6.0 拆分独立。专注封面图 + 场景图 + 普通素材三种视觉模式。

### 从 pop-novel-visual 继承
- 三段流程（搜图选图/原文理解 → 设计方案 → 生成）
- 两个用户对齐门禁（门禁A选图+参考点 / 门禁B方案确认）
- 参考点驱动提示词策略
- 场景图原文理解管线（五层）
- 高精度提示词模板（4块结构）
- IP背景提取（同人/改编视觉DNA）
- Pinterest 3维度搜索
- 迭代模式（快速路径）

### 移除
- 人物立绘模式（已拆分到 `pop-novel-oc`）
- 视觉模式路由总览（visual-mode-guide.md，三模式无需路由表）
- 立绘相关的设计方法论和提示词结构

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-research.md, step0-scene-understand.md, step1-design.md, step2-generate.md
- references/: mode-cover.md, mode-scene.md, mode-scene-art.md, novel-visual-design.md, seedream-prompt-guide.md
- templates/: design-plan.tpl.md
- scripts/: generate.py, pinterest_search.py
