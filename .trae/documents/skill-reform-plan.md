# Plan: 剩余 15 个 Skill 批量改造

## Summary

对 `D:\popwave-skills\skills\` 中尚未改造的 15 个 skill 按 pop-skill-create 模式 B 规范批量改造。根据各 skill 当前质量和类型差异，分为三组执行：

- **组 A（3 个）**：pop-novel 系列，**完整改造**（❌ 红线 + WRONG 示例 + 扁平化 + 新目录路径 + CHANGELOG）
- **组 B（4 个）**：通用工具类，**中度改造**（精简 frontmatter + description 重写 + 基础 ❌ 红线 + CHANGELOG）
- **组 C（8 个）**：已接近规范，**轻量改造**（确认 frontmatter 合规 + CHANGELOG 补充 + 可选小修）

---

## Current State Analysis

### 已改造完成（6 个）
bootstrap, deconstructor, master, plot, writer, pop-skill-create

### 待改造（15 个）

| # | skill | 当前 frontmatter 行数 | 当前状态 | 分组 |
|:-:|:------|:---------------------:|:---------|:----:|
| 1 | pop-novel-qa | 14 行 | 长 frontmatter，无❌红线 | **A** |
| 2 | pop-novel-html-renderer | 15+ 行 | 长 frontmatter，无❌红线 | **A** |
| 3 | pop-novel-game | 10 行 | 含硬编码 API key（安全问题），无❌红线 | **A** |
| 4 | book-opinion-tracker | 10+ 行 | 长 frontmatter | **B** |
| 5 | knowledge-downloader | 10+ 行 | 长 frontmatter | **B** |
| 6 | pop-book-promo | 8 行 | 中等 frontmatter | **B** |
| 7 | pop-YouTubewebbuilder | 需要检查 | 推测较长 | **B** |
| 8 | download-webnovel-txt | 4 行 | 已接近规范 | **C** |
| 9 | cnovel-research | 5 行 | 已接近规范 | **C** |
| 10 | feishu-docs | 5 行 | 已接近规范 | **C** |
| 11 | pop-html-anything | 5 行 | 已接近规范 | **C** |
| 12 | pop-reader-making | 4 行 | **已是参考范式** | **C** |
| 13 | pop-seo-anything | 5 行 | 已接近规范 | **C** |
| 14 | prd-builder | 3 行 | **最干净** | **C** |
| 15 | web-access | 10+ 行 | metadata 类，可精简 | **C** |

---

## Proposed Changes

### 组 A：完整改造（pop-novel-qa / pop-novel-html-renderer / pop-novel-game）

每个 skill 执行模式 B 的 8 步流程。

#### 1. pop-novel-qa

**文件**：`skills/pop-novel-qa/SKILL.md` + `skills/pop-novel-qa/CHANGELOG.md` + `skills/pop-novel-qa/skill.json`

**改动**：
- frontmatter 从 14 行 → 3 行（元数据迁移至 skill.json）
- description 改为触发条件式："当用户说'审稿'/'质检'/'QA'/'审一下'时启用"
- 新增 5-6 条 ❌ 质量红线（带 [ ] 勾选）：
  - ❌1 不评价节奏/画面感/不给建议/不评分（原核心原则的禁令化）
  - ❌2 必须加载 reader_profile，否则 QC 不知道"为谁而读"
  - ❌3 必须输出纯感受报告，不做分析
  - ❌4 红线触发 → 标记退回 writer
- 流程拍平为 3 步（三层介入 → 感受报告输出 → 红线标记+追回）
- 新增 WRONG 示例（QC 给建议了/QC 评分了）
- 新增 CHANGELOG.md
- 更新 skill.json 路径（02-幕纲/ → 设计/幕/ 等）

**理由**：pop-novel-qa 的 SKILL.md 结构其实不错——核心原则明确、底线清晰。改造重点是：①禁令化已有规则 ②精简 frontmatter ③补充 CHANGELOG

#### 2. pop-novel-html-renderer

**文件**：`skills/pop-novel-html-renderer/SKILL.md` + `skills/pop-novel-html-renderer/CHANGELOG.md` + `skills/pop-novel-html-renderer/skill.json`

**改动**：
- frontmatter 从 15+ 行 → 3 行
- description 改为触发条件式
- 新增 3-4 条 ❌ 红线：
  - ❌1 HTML 产出前必须先验证（零外部 CDN/JSON 可解析/闭合标签/双击可开）
  - ❌2 上游预写 image_prompt 不得自行编造（角色肖像和名场面引用上游）
  - ❌3 设计系统选择必须有理由（不能默认选第一个）
- 流程扁平化
- 新增 CHANGELOG.md
- 更新 skill.json

**理由**：HTML 渲染引擎是执行型 skill，红线集中在"产出验证"和"上游依赖"上，不需要太多禁令。

#### 3. pop-novel-game

**文件**：`skills/pop-novel-game/SKILL.md` + `skills/pop-novel-game/CHANGELOG.md` + `skills/pop-novel-game/skill.json`

**改动**：
- **安全修复**：将硬编码的 API key (`sk-3c03febd...`) 移至环境变量或 skill.json 的配置区。SKILL.md 中只留占位符
- frontmatter 精简（api 块迁移至 skill.json 或独立 config）
- description 已合格（触发条件式），保留
- 新增 3-4 条 ❌ 红线：
  - ❌1 API key 不得硬编码在 SKILL.md 中
  - ❌2 HTML 产出前必须验证（零外部 CDN/双击可开）
  - ❌3 世界观文件必须存在才可启动文游
- 新增 CHANGELOG.md

**理由**：pop-novel-game 最突出的问题是 API key 硬编码，这属于安全红线。其他内容结构尚可。

---

### 组 B：中度改造（book-opinion-tracker / knowledge-downloader / pop-book-promo / pop-YouTubewebbuilder）

每个 skill 执行模式 B 的 Step 1-3-5-6-7-8（跳过 Step 4 深度重排正文）：

#### 4. book-opinion-tracker

**改动**：
- frontmatter 从 10+ 行 → 3 行
- description 改为触发条件式
- 新增 2-3 条 ❌ 红线（搜索覆盖度/报告模板引用）
- 确认 CHANGELOG.md 存在 + 更新格式
- 更新 skill.json

#### 5. knowledge-downloader

**改动**：
- frontmatter 从 10+ 行 → 3 行
- description 改为触发条件式
- 新增 2-3 条 ❌ 红线（下载失败的处理/Phase B 拆解标准）
- 补充 CHANGELOG.md（检查是否存在）
- 更新 skill.json

#### 6. pop-book-promo

**改动**：
- frontmatter 精简
- description 改为触发条件式
- 新增 2-3 条 ❌ 红线
- 补充 CHANGELOG.md
- 更新 skill.json

#### 7. pop-YouTubewebbuilder（待确认）

- 先读 SKILL.md 确认实际结构
- 按组 B 标准执行

---

### 组 C：轻量改造（8 个已接近规范的 skill）

每个 skill 执行：
- 确认 frontmatter ≤ 5 行 ✅/❌
- 确认 description 是触发条件式 ✅/❌
- 补充 CHANGELOG.md（如果缺失）
- 仅在有明显缺陷时做小修

重点检查的 8 个：

| skill | 已有 | 只需 |
|:------|:-----|:-----|
| pop-reader-making | 4 行 frontmatter + 纪律块 ✅ | 确认 CHANGELOG 存在即可 |
| prd-builder | 3 行 frontmatter ✅ | 补充 CHANGELOG |
| download-webnovel-txt | 4 行 frontmatter ✅ | 补充 CHANGELOG |
| feishu-docs | 5 行 frontmatter ✅ | 补充 CHANGELOG |
| cnovel-research | 5 行 frontmatter + CHANGELOG ✅ | 基本无需改动 |
| pop-html-anything | 5 行 frontmatter ✅ | 补充 CHANGELOG + 确认红线 |
| pop-seo-anything | 5 行 frontmatter + CHANGELOG ✅ | 基本无需改动 |
| web-access | 10+ 行（多为 metadata）| 精简 + 补充 CHANGELOG |

---

## Assumptions & Decisions

1. **grouping 依据**：根据 skill 的当前质量和类型分组，不是一刀切。组 A 做完整改造（和已改造的 6 个同级），组 B 做中度改造（节约 60% 时间），组 C 做轻量改造（只补缺失项）。

2. **API key 安全**：pop-novel-game 的硬编码 API key 必须移出 SKILL.md。这是所有变更中唯一的安全 P0 项。

3. **保留原有内容**：改造不删除或改写技能的核心执行逻辑，只重组表达方式（红线前置、禁令化、扁平化）。

4. **CHANGELOG.md 作为标准配置**：所有缺少 CHANGELOG.md 的 skill 都补上。

5. **新目录路径**：组 A 的 skill 需要更新产出路径（02-幕纲/ → 设计/幕/ 等），组 B/C 保持原路径不变（它们不受新目录结构影响）。

---

## Verification

1. 每个 skill 改造后，检查：
   - [ ] frontmatter ≤ 4 行（组 A）/ ≤ 5 行（组 B/C）
   - [ ] description 包含触发条件
   - [ ] ❌ 质量红线已添加（组 A ≥ 4 条，组 B ≥ 2 条）
   - [ ] CHANGELOG.md 存在且包含改造记录
   - [ ] skill.json 已同步更新（元数据迁移完成）
2. 组 A 额外检查：
   - [ ] WRONG 错误示例 ≥ 1 个
   - [ ] 验收 [ ] 勾选框已添加
   - [ ] 新目录路径已更新
3. pop-novel-game 安全检查：
   - [ ] SKILL.md 中不再有硬编码 API key
