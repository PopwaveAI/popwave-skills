# Changelog

## 3.1.0 — 2026-06-02

**根因**: 模板有外部 CDN 依赖（离线无法加载）；CHANGELOG 缺失 v3.0.0 记录；模式 A 定制 HTML 缺乏产出规范约束
**类型**: enhancement
**改动**:
- **修复**: 5 个 HTML 模板移除 Google Fonts `@import`，全部替换为系统字体栈（`-apple-system/PingFang SC/Microsoft YaHei`），实现零外部依赖、离线可开
- **修复**: CHANGELOG 补齐 v3.0.0 条目（原内容）
- **新增**: SKILL.md 模式 A 第⑤步新增「定制 HTML 产出规范」，覆盖零外部依赖/文件完整性/设计体系一致性 3 类检查项

### 改动文件
- `templates/comic.html` — 移除 Google Fonts @import，字体栈改为系统字体
- `templates/scroll.html` — 同上
- `templates/scenes.html` — 同上
- `templates/quote.html` — 同上
- `templates/gallery.html` — 同上
- `SKILL.md` — 新增模式 A HTML 产出规范章节
- `CHANGELOG.md` — 本文件新增

---

## 3.0.0 — 2026-06-01

**根因**: 旧版强制模板注入 → 设计自由度不足，不适合品牌级物料
**类型**: architecture
**改动**:
- **路线变更**: 从强制模板注入 → PRD 先行 + 设计哲学驱动（模式 A）
- generate.py 新增 `--mode image` 纯生图模式
- SKILL.md 新增完整设计哲学体系（4 视觉方向 / 颜色体系 / 间距体系 / 字体层级 / 排版规则）
- 新增 PRD 文档模板
- 旧模板管线保留为模式 B（向后兼容）

---

### 破坏性变更
- 项目重命名：`multi-modal-marketing` → `pop-book-promo`
- 项目根目录变更：`_工具配置/create场景/多模态推书/` → `_工具配置/create场景/pop-book-promo/`

### 新增
- `preflight.py` — 前置检查（API Key / Python 依赖 / 输入 JSON 校验）
- `scripts/autocheck.py` — 自检脚本（语法检查 / 模板完整性 / 示例数据验证）
- SKILL.md frontmatter 补齐 7 个必填字段（dependencies / inject_context / produces）
- skill.json 改为 popwave 标准格式（id / activation / permissions / loadPolicy）
- README.md 重写，新增规范合规说明

### 修复
- skil.json 字段名修正：`name` → `id`（popwave 规范要求）
- CHANGELOG.md 新增"改动文件"记录

### 改动文件
- `skill.json` — 完全重写为 popwave 标准格式
- `SKILL.md` — 补齐 frontmatter + 重写文档结构
- `README.md` — 重写
- `CHANGELOG.md` — 本文件新增
- `preflight.py` — 新建
- `scripts/autocheck.py` — 新建
- `skills/novel-ip-demo/SKILL.md` — 补齐 frontmatter
- `skills/novel-ip-demo/agents/openai.yaml` — 新增 display_name

---

## 1.0.0 — 2026-05-25

### 新增
- 5 种多模态物料：名场面四格漫画 / 古风人物画卷 / 名场面高光帧 / 金句分享卡 / 角色立绘画廊
- 统一生成引擎 `scripts/generate.py`：调 Open Router 图像 API → base64 注入 → 单文件 HTML
- 5 套 HTML 模板：深色主题，移动端适配，中文排版
- 4 组示例数据：基于《千屿》角色体系
- 支持模型：`google/gemini-2.5-flash-image`（低成本）、`openai/gpt-5-image`（高质量）
- 失败自动降级为占位图，保证始终输出可查看的 HTML

### 改动文件
- `skill.json` — 初始创建
- `SKILL.md` — 初始创建
- `README.md` — 初始创建
- `scripts/generate.py` — 初始创建
- `scripts/build_heroine_card.py` — 初始创建
- `scripts/demo_from_title.py` — 初始创建
- `templates/comic.html` — 初始创建
- `templates/scroll.html` — 初始创建
- `templates/scenes.html` — 初始创建
- `templates/quote.html` — 初始创建
- `templates/gallery.html` — 初始创建
- `examples/scenes.json` — 初始创建
- `examples/profile.json` — 初始创建
- `examples/quotes.json` — 初始创建
- `examples/characters.json` — 初始创建
- `skills/novel-ip-demo/SKILL.md` — 初始创建
- `skills/novel-ip-demo/agents/openai.yaml` — 初始创建
