# CHANGELOG

## v2.1.0 | 2026-07-30

### 新增（IP背景检查 + 高精度模板集成）

**IP背景检查**（`steps/step0-init.md` §1.1）：
- 画风推导前必执行IP背景判断：同人/改编/原创三分类
- 同人小说需WebSearch搜索源IP官方画风，提取视觉DNA后决定锚定或偏离
- 引用 pop-novel-visual 的IP背景理解方法论

**高精度模板集成**：
- `steps/step0-init.md` 定妆图提示词新增高精度写法（主角定妆图建议使用4块结构）
- `steps/step1-chapter.md` 新增关键帧高精度模板指引（高潮帧/变身帧/名场面升级为高精度，普通帧速度优先）
- `references/storyboard-guide.md` 新增关键帧升级段落

## v2.0.0 | 2026-07-29

### 重构（Pipeline 化 — 漫画连载管线）

**核心升级**：从单章生成器升级为漫画连载 pipeline，解决 DeepSeek 无视觉能力下的跨章人设/画风一致性问题。

**新增 Phase 0: 项目初始化**（`steps/step0-init.md`）：
- 读取小说项目设定 → 提取角色视觉规格表 → 生成定妆图 → 冻结提示词
- 定妆图持久化到 `assets/characters/`（跨章复用，版本递增）
- 创建四个记忆文件：漫画角色库.md / 漫画快照.md / 漫画状态.md / 视觉沉淀.md
- 门禁0：角色定妆确认

**新增 Phase 2: 视觉审核+记忆沉淀**（`steps/step2-review.md`）：
- 产出完整性检查 + 视觉决策记录 + append 视觉沉淀.md
- 更新漫画快照.md + 漫画状态.md（为下章准备入口包）
- 对齐起点 pipeline 的"不得连续两章不审核"原则

**冻结提示词机制**（核心创新）：
- 角色定妆图生成后，提示词原文冻结到漫画角色库.md
- 后续章节直接引用冻结版，禁止重新从规格表组装
- 消除"规格表→提示词"的翻译 gap，解决跨章角色漂移
- 角色变化时基于冻结版+变化描述生成新版本，新提示词同样冻结

**四层角色结构**：
- 层1 规格表（人读）→ 层2 冻结提示词（API读，真相源）→ 层3 定妆图资产（版本管理）→ 层4 决策日志（append-only）

**分层记忆机制**（对齐起点 pipeline）：
- 长期：漫画角色库.md（增量更新）
- 中期：漫画快照.md（replace）
- 短期：漫画状态.md（replace）
- 审稿：视觉沉淀.md（append-only）

**脚本改造**：
- `generate_storyboard.py` v2.0：`CHAR_IMG` → `FRAME_REFS`（按帧映射角色定妆图，支持无角色帧文生图）
- 新增 `init_project.py`：初始化漫画项目目录+记忆文件
- 新增 `update_char_asset.py`：增量定妆图生成（角色外观变化时）
- `inline_html.py`：不变（v1.2.0 已有）

**新增文件**：
- `references/char-consistency-guide.md`：角色一致性管理指南
- `templates/漫画角色库.md.tpl` / `漫画快照.md.tpl` / `漫画状态.md.tpl`

**铁律精简**：6条 → 4条（冻结提示词真相源 / HTML内联 / 每章必审核 / 定妆图持久化）

**删除**：旧 `steps/step1-deconstruct.md` 和 `steps/step2-generate.md`（被新 step 文件替代）

## v1.2.0 | 2026-07-29

### 修复（HTML 图片内联化）
- **根因**：popwave webview 安全策略禁止加载外部资源（相对路径、绝对路径、file:// 协议均被阻止），HTML 中 `<img src="output/frame1.png">` 在 popwave 中显示为图片损坏
- **验证过程**：相对路径 ❌ → 绝对路径 file:// ❌ → base64 内联 472KB ✅ → base64 内联 6.5MB ❌（文件过大无法打开）→ 压缩 base64 内联 ✅
- **修复**：新增 `scripts/inline_html.py` 脚本，将 HTML 中所有本地图片引用压缩为 base64 data URI（默认 800px 宽 + JPEG quality 65），使 HTML 完全自包含
- **新增铁律6**：HTML 必须内联图片，禁止交付含外部图片路径的 HTML
- **step2-generate.md** 新增 §4 HTML 图片内联化步骤（必须执行）和质量检查项

## v1.1.0 | 2026-07-29

### 修复（格式保真）
- **根因**：Seedream API 返回的 URL 资源实际为 JPEG（magic bytes `FF D8 FF`），但 `generate_storyboard.py` 以 `.png` 命名保存，导致扩展名与实际格式不符
- **现象**：浏览器做 MIME sniffing 能兼容显示，但 popwave webview（nosniff 模式）按扩展名校验 MIME，判定为图片损坏
- **修复**：新增 `ensure_png_format()` 函数，在图片下载后自动检测 magic bytes，若为 JPEG 内容则用 Pillow 转码为真 PNG
- **同步修复**：`pop-novel-visual/scripts/generate.py` 的 `download_file` 和 `save_base64_image` 两条路径（新增 `ensure_format_integrity()` 函数）
- **新增铁律5**：下载后格式保真

## v1.0.0 | 2026-07-29

### 新增
- 初始版本，基于 R15 测试验证的网文章节转漫画管线
- 2 步结构：Step 1 章节解构+分镜脚本+门禁A，Step 2 角色定妆+分镜生成+HTML组装
- 复用 pop-novel-visual 的 Seedream API 脚本（`scripts/generate.py`）和提示词指南（`references/seedream-prompt-guide.md`）
- 新增 `scripts/generate_storyboard.py` 批量分镜生成脚本
- 新增 `templates/comic-page.tpl.html` HTML 漫画页模板
- 新增 `references/storyboard-guide.md` 分镜脚本指南

### 验证数据（R15 测试）
- 9 次 API 调用（1 角色定妆 + 8 分镜），100% 成功率
- 单格画面质量 9/10，角色一致性 75%，风格统一 9/10
- 总耗时 ~3 分钟（串行），并行可压缩到 ~30 秒
