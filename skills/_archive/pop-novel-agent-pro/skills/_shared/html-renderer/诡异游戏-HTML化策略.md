# 《这诡异游戏也太真实了》文档HTML化策略方案 v1.0

> 基于 html-anything 27 套 SKILL 模板的设计约束
> 目标：项目内所有文档类型均可一键生成高质量HTML，方便传播/分享

---

## 一、文档类型→SKILL 映射

### 📖 长篇叙事/设定

| 文档 | 内容特征 | 推荐 SKILL | 设计要点 |
|------|----------|-----------|----------|
| PRD.md | 产品级文档，结构化的表格/列表 | `article-magazine` | 左hero+大标题+副标题+作者元数据 |
| constitution.yaml | 宪法铁律，编号规则 | `kami-parchment` | 暖羊皮纸 #f5f4ed，墨蓝 #1B365D，sticky index |
| l1-settings.yaml | 世界观规范，层级分明 | `data-report` | KPI卡片网格+层级树+可折叠 |
| 场景卡(.md) | 1400字短叙事，视听沉浸 | `card-xiaohongshu` | 竖版长图，场景元数据+正文+标签 |
| 章节正文(.md) | 2000-6000字连载 | `article-magazine` | serif排版，章号+字数标签+阅读进度 |
| 复盘报告(.md) | 分析类，分层级 | `kami-parchment` | 书卷风格+侧边栏锚点导航 |

### 🎬 创作管线文档

| 文档 | 内容特征 | 推荐 SKILL | 设计要点 |
|------|----------|-----------|----------|
| 章纲(character-state-anchor.md) | 角色状态区块 | `deck-swiss-international` | Klein Blue #002FA7，16列网格 |
| 大纲(段落/*.md) | 剧情分幕，编号 | `deck-guizang-editorial` | 墨水经典调色板+章节封页 |
| 导演指令(director-*.md) | 写作约束+要求 | `deck-open-slide-canvas` | 画布1920×1080，整洁图文分页 |
| 战斗体系参考池(v5.md) | 数据表格+分类 | `data-report` | KPI卡+Chart.js+多层级表 |
| 设定语料库 | 关键词+解释 | `deck-blueprint` | 架构图谱+编号节点+连接线 |
| 玩家底层逻辑 | 规则系统 | `deck-swiss-international` | ASCII点阵+反色封面 |

### 🎯 营销/分享用

| 文档 | 内容特征 | 推荐 SKILL | 设计要点 |
|------|----------|-----------|----------|
| 设定集 | 读物级世界观 | `magazine-poster` | 新闻纸+双栏+编号sections |
| 力量体系图解 | 层级关系 | `deck-graphify-dark` | 暗底+图谱节点+编号路径 |
| 管理员日志 | 叙事型 | `frame-glitch-title` | 故障艺术+CRT扫描线+ASCII噪点 |
| 第一卷地图 | 交互式 | `dashboard` | SVG图+筛选+点击详情卡 |
| 诡异OL登录页 | 游戏化 | `deck-hermes-cyber` | 黑底#0a0c10+薄荷绿+CLI风格 |
| 铁律/规则页 | 硬规条 | `deck-swiss-international` | S01全屏cover+反白标题 |

---

## 二、设计系统统一

### 配色体系

诡异游戏品牌色（从现有营销页提取）：

```
--bg-deep:     #0a0e1a  (深空蓝黑)
--bg-card:     #1a1d27  (暗灰蓝)
--accent:      #d44      (铁锈红/民俗红)
--accent-dim:  #8a5a5a   (暗红)
--text:        #e4e6f0   (银白)
--text-dim:    #8b8fa3   (灰蓝)
--green:       #34d399   (系统/安全)
--blue:        #60a5fa   (信息)
```

### 字体栈

```css
/* 正文 */
font-family: -apple-system, "PingFang SC", "Noto Sans SC", sans-serif;

/* 标题/展示 */
font-family: "Noto Serif SC", "Source Han Serif SC", serif;

/* 代码/数据 */
font-family: "JetBrains Mono", "Fira Code", monospace;
```

### 通用组件

1. **Hero Section**: 暗色径向渐变背景+大字标题+badge
2. **Rule/Section Card**: 1px边框+圆角8-10px+暗底+hover光晕
3. **Tag/Badge**: 6-8px圆角，小字，背景10%透明度
4. **Divider**: 1px rgba(255,255,255,0.04)细线
5. **Quote**: 左边框accent色+10%背景

---

## 三、技术实现

### 方式A: 直接渲染 (适用于结构化数据)

```python
from html_renderer import HTMLRenderer

renderer = HTMLRenderer()

# PRD → Magazine Article
renderer.render("article-magazine", {
    "title": "PRD - 产品需求文档",
    "author": "江轩",
    "content": "..."  # Markdown body
})

# 宪法 → Kami Parchment
renderer.render("kami-parchment", {
    "title": "诡异游戏项目宪法",
    "rules": [...]
})

# 战斗体系 → Data Report
renderer.render("data-report", {
    "title": "战斗体系参考池 v5",
    "metrics": {"境界": 5, "流派": 9, "武器": 23}
})
```

### 方式B: LLM Prompt (适用于非结构化文档)

```python
from html_renderer import generate_skill_prompt

# 生成Prompt→发给LLM→LLM产出HTML
prompt = generate_skill_prompt("article-magazine", {
    "title": "场景卡001：纸身",
    "scene_type": "纯恐怖遭遇",
    "body": open("场景卡-001-纸身.md").read()
})
```

### 方式C: 目录级批量生成

```python
from html_renderer.integrations import NovelAgentIntegration

integration = NovelAgentIntegration(output_dir="e:\\AI小说\\...")

# 一键生成全部设定集HTML
doc_map = {
    "00-原始设定/l1-settings.yaml": "data-report",
    "00-原始设定/constitution.yaml": "kami-parchment",
    "01-写作资产/场景卡/scene-card-001.md": "card-xiaohongshu",
}
for doc_path, skill in doc_map.items():
    html = integration.render_to_html(skill, data, output_path)
```

---

## 四、现有营销页质量分析

当前 `07-营销/` 下已有 10 个 HTML 文件：
- ✅ **设计统一**：暗色主题、民俗红 accent、径向渐变 hero
- ✅ **信息层级清晰**：badge-h2-p 三级体系
- ⚠️ **可改进**：暂无统一 CSS 变量系统，每个页面独立写样式
- ⚠️ **缺少**：响应式布局、动效、跨页面导航

**升级路线**：
1. 提取公共 CSS 变量 → `_theme.css`
2. 页面间增加导航条
3. 按 SKILL 体系重新组织（每个页面绑定一个 SKILL 模板）
