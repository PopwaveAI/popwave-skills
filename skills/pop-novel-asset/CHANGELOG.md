# CHANGELOG

## v1.0.0 (2026-07-30)

从 `pop-novel-visual` 拆分体系中新建的基建 skill。专注从小说原文提取结构化视觉资产，供下游视觉 skill 群消费。

### 核心能力
- **四种资产产出**：角色档案（10维度）、场景资产表（可定格帧清单）、视觉符号库（意象/标志色/器物/阵营符号）、IP视觉DNA（同人时）
- **两种项目空间兼容**：写作专家项目（起点/番茄，有已有设定辅助）+ 独立小说项目（纯原文采样）
- **增量更新机制**：采样范围标记 + 只提取新增章节 + 追加不覆盖
- **消费路由**：资产就绪后告知用户可调用 pop-novel-oc / pop-novel-comic / pop-novel-cover

### 设计理念
- **只提取不生成**：asset 是基建 skill，禁止调用任何图片生成 API
- **与拆书 skill 的区别**：拆书拆"怎么写的"（技法），asset 提"有什么"（素材）
- **原文采样有行号索引**：每条信息可溯源，消费方可定位原文

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-detect.md, step1-extract.md
- references/: asset-extract-guide.md
