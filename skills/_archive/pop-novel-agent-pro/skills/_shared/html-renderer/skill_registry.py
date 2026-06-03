"""
SKILL Registry - html-anything 75套设计模板注册表
自动生成自 html-anything/next/src/lib/templates/skills/
总共注册: 27 套 SKILL
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class SkillCategory(Enum):
    DECK = "deck"
    DOC = "doc"
    POSTER = "poster"
    ARTICLE = "article"
    SOCIAL = "social"
    DASHBOARD = "dashboard"
    DATA_REPORT = "data_report"
    FRAME = "frame"
    VFX = "vfx"


@dataclass
class DesignConstraints:
    accent: str
    paper: str
    ink: str
    font_display: str
    font_body: str
    font_mono: str
    grid_columns: int = 16
    border_radius: int = 0
    forbidden: List[str] = field(default_factory=list)
    required: List[str] = field(default_factory=list)


@dataclass
class SkillTemplate:
    name: str
    zh_name: str
    en_name: str
    emoji: str
    category: SkillCategory
    description: str
    constraints: DesignConstraints
    layouts: List[Dict[str, Any]] = field(default_factory=list)
    recommended: int = 50
    tags: List[str] = field(default_factory=list)

    def to_prompt(self) -> str:
        c = self.constraints
        p = f"【模板: {self.zh_name} ({self.en_name})】\n"
        p += f"【意图】{self.description}\n"
        p += f"【调色板】Accent: {c.accent} | Paper: {c.paper} | Ink: {c.ink}\n"
        p += f"【字体】Display: {c.font_display} | Body: {c.font_body} | Mono: {c.font_mono}\n"
        if c.forbidden:
            p += "【严禁】\n" + "\n".join(f"  - {x}" for x in c.forbidden) + "\n"
        return p


class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, SkillTemplate] = {}
        self._init_skills()

    def _init_skills(self):
        """从 html-anything 提取的全部 SKILL"""

        # 杂志文章 (Magazine Article)
        self._skills["article-magazine"] = SkillTemplate(
            name="article-magazine",
            zh_name="杂志文章",
            en_name="Magazine Article",
            emoji="📖",
            category=SkillCategory.ARTICLE,
            description="Substack / Medium 高级感长文排版, 适合公众号、博客发布",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "顶部 hero: 大标题 (text-5xl/6xl) + 可选副标题 + 作者 / 阅读时间 / 日期元数据。", "desc": "顶部 hero: 大标题 (text-5xl/6xl) + 可选副标题 + 作者 / 阅读时间 / 日期元数据。"}, {"name": "正文: 单栏, 最大宽度约 700px, 居中。段落 `text-lg leading-relaxed text-n", "desc": "正文: 单栏, 最大宽度约 700px, 居中。段落 `text-lg leading-relaxed text-neutral-700 dark:text-neutral-300`。"}, {"name": "H2 / H3 标题用 serif 字体, 让正文与标题有视觉对比。", "desc": "H2 / H3 标题用 serif 字体, 让正文与标题有视觉对比。"}, {"name": "引用块使用左侧粗 accent 色边线 + 斜体。", "desc": "引用块使用左侧粗 accent 色边线 + 斜体。"}, {"name": "代码块: 圆角 + 深色背景 + 浅色文字, 显示语言标签。", "desc": "代码块: 圆角 + 深色背景 + 浅色文字, 显示语言标签。"}],
            recommended=99,
            tags=["blog", "essay", "newsletter", "公众号", "博客", "文章"]
        )

        # 博客长文 (Blog Post)
        self._skills["blog-post"] = SkillTemplate(
            name="blog-post",
            zh_name="博客长文",
            en_name="Blog Post",
            emoji="📰",
            category=SkillCategory.ARTICLE,
            description="杂志感长文, 含 masthead、hero、figures、pull quote、作者署名",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Masthead (publication name + date)", "desc": "Masthead (publication name + date)"}, {"name": "Hero (大标题 + 副标 + 作者署名 + 阅读时间)", "desc": "Hero (大标题 + 副标 + 作者署名 + 阅读时间)"}, {"name": "正文 (单栏 65ch, 含 figures, pull quotes, 行内引用)", "desc": "正文 (单栏 65ch, 含 figures, pull quotes, 行内引用)"}, {"name": "Author bio 卡片", "desc": "Author bio 卡片"}, {"name": "Related posts (3 张卡)", "desc": "Related posts (3 张卡)"}],
            recommended=99,
            tags=["blog", "essay", "case study", "长文"]
        )

        # Twitter 分享卡 (Twitter Share Card)
        self._skills["card-twitter"] = SkillTemplate(
            name="card-twitter",
            zh_name="Twitter 分享卡",
            en_name="Twitter Share Card",
            emoji="🐦",
            category=SkillCategory.SOCIAL,
            description="推特金句 / 数据卡, 适合配推文",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "容器 `w-[1600px] h-[900px]`, 暗色 / 亮色二选一根据内容情绪。", "desc": "容器 `w-[1600px] h-[900px]`, 暗色 / 亮色二选一根据内容情绪。"}, {"name": "中央一句 hero 金句 (text-6xl, font-semibold, 限 2-3 行)。", "desc": "中央一句 hero 金句 (text-6xl, font-semibold, 限 2-3 行)。"}, {"name": "下方作者署名 + 头像占位 + handle。", "desc": "下方作者署名 + 头像占位 + handle。"}, {"name": "左上角小标签 (类型: \"Insight\" / \"Data\" / \"Quote\")。", "desc": "左上角小标签 (类型: \"Insight\" / \"Data\" / \"Quote\")。"}, {"name": "右下角品牌水印。", "desc": "右下角品牌水印。"}],
            recommended=99,
            tags=["twitter", "x", "quote", "金句"]
        )

        # 小红书图文卡片 (Xiaohongshu Card)
        self._skills["card-xiaohongshu"] = SkillTemplate(
            name="card-xiaohongshu",
            zh_name="小红书图文卡片",
            en_name="Xiaohongshu Card",
            emoji="📱",
            category=SkillCategory.SOCIAL,
            description="小红书风格知识卡片, 多张联排可滑动浏览",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "输出 N 张连续卡片, 每张 `w-[1080px] h-[1440px]`, 用 flex 纵向排列方便整体截图也", "desc": "输出 N 张连续卡片, 每张 `w-[1080px] h-[1440px]`, 用 flex 纵向排列方便整体截图也方便单张截图。N 由【用户内容】信息量决定: 短内容 3-6 张起步, 长内容应更多 (小红书平台单帖最多 18 图, 通常 9 张以内最佳); 一张卡只承载一个核心观点。"}, {"name": "第一张是封面: 巨大的标题 + 1 行副标题 + 一个吸引人的标签 (类似 \"干货预警\" / \"建议收藏\")。", "desc": "第一张是封面: 巨大的标题 + 1 行副标题 + 一个吸引人的标签 (类似 \"干货预警\" / \"建议收藏\")。"}, {"name": "中间几张展开正文, 每张一个核心观点, 配 emoji + 短句 + 1-2 个例子。", "desc": "中间几张展开正文, 每张一个核心观点, 配 emoji + 短句 + 1-2 个例子。"}, {"name": "最后一张是总结 + 行动号召 (关注 / 收藏 / 评论)。", "desc": "最后一张是总结 + 行动号召 (关注 / 收藏 / 评论)。"}, {"name": "配色: 选择柔和的莫兰迪色或粉色系; 元素圆润, 大量留白。", "desc": "配色: 选择柔和的莫兰迪色或粉色系; 元素圆润, 大量留白。"}],
            recommended=99,
            tags=["xhs", "小红书", "carousel", "图文"]
        )

        # 管理后台仪表板 (Admin Dashboard)
        self._skills["dashboard"] = SkillTemplate(
            name="dashboard",
            zh_name="管理后台仪表板",
            en_name="Admin Dashboard",
            emoji="🎛️",
            category=SkillCategory.DASHBOARD,
            description="固定侧栏 + 顶栏 + KPI 网格 + 1-2 张图",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Fixed left sidebar (logo + 导航 + 用户 footer)", "desc": "Fixed left sidebar (logo + 导航 + 用户 footer)"}, {"name": "Top bar (search + 通知 + avatar)", "desc": "Top bar (search + 通知 + avatar)"}, {"name": "Main: KPI cards 网格 (3-5 个)", "desc": "Main: KPI cards 网格 (3-5 个)"}, {"name": "1-2 张主图表 (折线 / 柱 / 区域)", "desc": "1-2 张主图表 (折线 / 柱 / 区域)"}, {"name": "底部 recent activity 列表", "desc": "底部 recent activity 列表"}],
            recommended=99,
            tags=["dashboard", "admin", "analytics"]
        )

        # 数据可视化报告 (Data Visualization Report)
        self._skills["data-report"] = SkillTemplate(
            name="data-report",
            zh_name="数据可视化报告",
            en_name="Data Visualization Report",
            emoji="📊",
            category=SkillCategory.DATA_REPORT,
            description="把 CSV/Excel/JSON 数据转成漂亮的可视化报告页",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "头部: 报告标题 + 时间区间 + 数据来源说明。", "desc": "头部: 报告标题 + 时间区间 + 数据来源说明。"}, {"name": "KPI 卡片网格: 3-5 个最重要指标, 每个卡片显示数值 + 同比变化 + 微型趋势线。", "desc": "KPI 卡片网格: 3-5 个最重要指标, 每个卡片显示数值 + 同比变化 + 微型趋势线。"}, {"name": "主图表区: 至少 2 个图表 (柱状 / 折线 / 饼 / 散点), 使用 Chart.js 或 ECharts (", "desc": "主图表区: 至少 2 个图表 (柱状 / 折线 / 饼 / 散点), 使用 Chart.js 或 ECharts (jsdelivr CDN 引入), 数据从用户输入解析得到。"}, {"name": "**图表容器必须有固定高度**: 每个 `<canvas>` 外层包一个 `<div style=\"position", "desc": "**图表容器必须有固定高度**: 每个 `<canvas>` 外层包一个 `<div style=\"position:relative;height:NNNpx\">` (KPI 迷你图 ~40px, 主图表 ~240–280px)。Chart.js 用 `responsive:true, maintainAspectRatio:false` 时若父容器没有显式高度, 会陷入 ResizeObserver 死循环, 图表无限增高直至卡死浏览器。**绝对不要**直接给 canvas 写 `height=` 属性当布局, 那个只是初始值。"}, {"name": "数据表格: 用户原始数据节选, 使用 `<table>` + 现代化样式 (zebra stripe, hover,", "desc": "数据表格: 用户原始数据节选, 使用 `<table>` + 现代化样式 (zebra stripe, hover, sticky header)。"}],
            recommended=99,
            tags=["data", "report", "chart", "数据", "报告"]
        )

        # 社区 / 配对数据墙 (Dating / Community Dashboard)
        self._skills["dating-web"] = SkillTemplate(
            name="dating-web",
            zh_name="社区 / 配对数据墙",
            en_name="Dating / Community Dashboard",
            emoji="💞",
            category=SkillCategory.DASHBOARD,
            description="消费感配对仪表板: 信号 ticker + KPI + 30 天柱状 + 趋势",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Left rail 导航", "desc": "Left rail 导航"}, {"name": "Ticker bar 实时信号", "desc": "Ticker bar 实时信号"}, {"name": "Headline KPIs", "desc": "Headline KPIs"}, {"name": "30-day mutual-matches 柱状图", "desc": "30-day mutual-matches 柱状图"}, {"name": "Match-rate 趋势 block", "desc": "Match-rate 趋势 block"}],
            recommended=99,
            tags=["dating", "community", "consumer"]
        )

        # 蓝图架构 Deck (Knowledge Arch Blueprint)
        self._skills["deck-blueprint"] = SkillTemplate(
            name="deck-blueprint",
            zh_name="蓝图架构 Deck",
            en_name="Knowledge Arch Blueprint",
            emoji="📐",
            category=SkillCategory.DECK,
            description="奶油纸 + 锈红 + 蓝图网格 mask + 黑边硬卡片 + pipeline 盒",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "奶油 #F0EAE0 底 + 蓝图 48px 网格 mask", "desc": "奶油 #F0EAE0 底 + 蓝图 48px 网格 mask"}, {"name": "Pipeline 步骤盒 (其中一个抬高)", "desc": "Pipeline 步骤盒 (其中一个抬高)"}, {"name": "右侧锈红 #B5392A insight callout", "desc": "右侧锈红 #B5392A insight callout"}, {"name": "Playfair serif 大字 + SVG 虚线反馈环", "desc": "Playfair serif 大字 + SVG 虚线反馈环"}, {"name": "零渐变零软阴影", "desc": "零渐变零软阴影"}],
            recommended=99,
            tags=["blueprint", "architecture", "engineering"]
        )

        # 课程 / 培训 Deck (Course Module Deck)
        self._skills["deck-course-module"] = SkillTemplate(
            name="deck-course-module",
            zh_name="课程 / 培训 Deck",
            en_name="Course Module Deck",
            emoji="🎓",
            category=SkillCategory.DECK,
            description="暖纸背景 + Playfair, 左侧学习目标常驻, 含 MCQ 自测页",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Cover (模块名 + 讲师)", "desc": "Cover (模块名 + 讲师)"}, {"name": "Learning objectives 列表 (左侧持续显示)", "desc": "Learning objectives 列表 (左侧持续显示)"}, {"name": "正文页 (concept + 例子)", "desc": "正文页 (concept + 例子)"}, {"name": "MCQ 自测页", "desc": "MCQ 自测页"}, {"name": "Wrap-up + 下一模块预告", "desc": "Wrap-up + 下一模块预告"}],
            recommended=99,
            tags=["course", "workshop", "training", "教学"]
        )

        # 极简方向键 Keynote (Dir-Key Nav Minimal Deck)
        self._skills["deck-dir-key-nav"] = SkillTemplate(
            name="deck-dir-key-nav",
            zh_name="极简方向键 Keynote",
            en_name="Dir-Key Nav Minimal Deck",
            emoji="▶︎",
            category=SkillCategory.DECK,
            description="8 页单色背景, 160px display + 4px accent + Mono 箭头列表",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "页数由【用户内容】决定 (短内容 8 页起步, 长内容应更多); 每页单色背景, 从下列调色板里循环选取 (靛 / ", "desc": "页数由【用户内容】决定 (短内容 8 页起步, 长内容应更多); 每页单色背景, 从下列调色板里循环选取 (靛 / 奶 / 绛 / 翠 / 灰 / 紫 / 白 / 炭), 同色可复用"}, {"name": "160px display 标题 + 4px 短粗 accent 线", "desc": "160px display 标题 + 4px 短粗 accent 线"}, {"name": "箭头 → 前缀的 Mono 列表", "desc": "箭头 → 前缀的 Mono 列表"}, {"name": "左下 ← → kbd 提示 + 右下页码", "desc": "左下 ← → kbd 提示 + 右下页码"}],
            recommended=99,
            tags=["minimal", "kbd", "monocolor"]
        )

        # 暗底图谱 Deck (Graphify Dark Deck)
        self._skills["deck-graphify-dark"] = SkillTemplate(
            name="deck-graphify-dark",
            zh_name="暗底图谱 Deck",
            en_name="Graphify Dark Deck",
            emoji="🌌",
            category=SkillCategory.DECK,
            description="深夜渐变 + 漂浮 orbs + SVG 力导向图谱 + JetBrains Mono",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Cover: #06060c→#0e1020 渐变 + 浮动 blur orbs + SVG 力导向 graph", "desc": "Cover: #06060c→#0e1020 渐变 + 浮动 blur orbs + SVG 力导向 graph"}, {"name": "Section 页: 彩虹渐变标题", "desc": "Section 页: 彩虹渐变标题"}, {"name": "代码 / CLI 页: JetBrains Mono 高亮", "desc": "代码 / CLI 页: JetBrains Mono 高亮"}, {"name": "Glassmorphism 卡片页", "desc": "Glassmorphism 卡片页"}],
            recommended=99,
            tags=["graph", "dev tool", "ai", "cli"]
        )

        # 贵赞编辑墨水 Deck (Guizang Editorial E-Ink Deck)
        self._skills["deck-guizang-editorial"] = SkillTemplate(
            name="deck-guizang-editorial",
            zh_name="贵赞编辑墨水 Deck",
            en_name="Guizang Editorial E-Ink Deck",
            emoji="🖋️",
            category=SkillCategory.DECK,
            description="电子杂志 × 电子墨水; 10 个版面 + 5 套调色板 (墨水/靛蓝瓷/森林墨/牛皮纸/沙丘)",
            constraints=DesignConstraints(
                accent="#0a0a0b",
                paper="#ffffff",
                ink="#000000",
                font_display="Playfair Display, Noto Serif SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=["调色板 — 5 选 1, 严禁改 hex、严禁混用", "- **严禁**: 渐变 / drop-shadow / 圆角 / 圆形装饰 / blur / SVG 图标库 / emoji 装饰。", "- **不许**: 数据捏造、Lorem ipsum、占位图片 URL。所有图请用纯 CSS / SVG 内联描绘 (色块 + 简笔)。"],
                required=[]
            ),
            layouts=[{"name": "🖋 **墨水经典 Monocle** — ink `#0a0a0b`, paper `#f1efea`, paper", "desc": "🖋 **墨水经典 Monocle** — ink `#0a0a0b`, paper `#f1efea`, paper-tint `#e8e5de`, ink-tint `#18181a`. 默认 / 通用商业 / 科技。"}, {"name": "🌊 **靛蓝瓷 Indigo Porcelain** — ink `#0a1f3d`, paper `#f1f3f5", "desc": "🌊 **靛蓝瓷 Indigo Porcelain** — ink `#0a1f3d`, paper `#f1f3f5`, paper-tint `#e4e8ec`, ink-tint `#152a4a`. 科技 / 研究 / 数据。"}, {"name": "🌿 **森林墨 Forest Ink** — ink `#1a2e1f`, paper `#f5f1e8`, pap", "desc": "🌿 **森林墨 Forest Ink** — ink `#1a2e1f`, paper `#f5f1e8`, paper-tint `#ece7da`, ink-tint `#253d2c`. 自然 / 可持续 / 文化。"}, {"name": "🍂 **牛皮纸 Kraft Paper** — ink `#2a1e13`, paper `#eedfc7`, pa", "desc": "🍂 **牛皮纸 Kraft Paper** — ink `#2a1e13`, paper `#eedfc7`, paper-tint `#e0d0b6`, ink-tint `#3a2a1d`. 怀旧 / 人文 / 文学。"}, {"name": "🌙 **沙丘 Dune** — ink `#1f1a14`, paper `#f0e6d2`, paper-tint", "desc": "🌙 **沙丘 Dune** — ink `#1f1a14`, paper `#f0e6d2`, paper-tint `#e3d7bf`, ink-tint `#2d2620`. 艺术 / 设计 / 时尚。"}],
            recommended=1,
            tags=["editorial", "e-ink", "magazine", "narrative", "guizang"]
        )

        # Cyber Terminal Deck (Hermes Cyber Terminal Deck)
        self._skills["deck-hermes-cyber"] = SkillTemplate(
            name="deck-hermes-cyber",
            zh_name="Cyber Terminal Deck",
            en_name="Hermes Cyber Terminal Deck",
            emoji="🟢",
            category=SkillCategory.DECK,
            description="黑底 + CRT 网格扫描线 + $ 命令行标题 + 薄荷绿大字 + 三档 tag",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "#0a0c10 黑底 + 56px 赛博网格 + CRT 暗角", "desc": "#0a0c10 黑底 + 56px 赛博网格 + CRT 暗角"}, {"name": "窗口红绿灯 chrome + `$ prompt` 标题", "desc": "窗口红绿灯 chrome + `$ prompt` 标题"}, {"name": "薄荷绿 #7ed3a4 大字 + JetBrains Mono", "desc": "薄荷绿 #7ed3a4 大字 + JetBrains Mono"}, {"name": "Stroke-only 柱状图 + blinking 光标", "desc": "Stroke-only 柱状图 + blinking 光标"}, {"name": "琥珀 / 绿 / 红 三档 tag", "desc": "琥珀 / 绿 / 红 三档 tag"}],
            recommended=99,
            tags=["cyber", "terminal", "review", "cli"]
        )

        # 杂志风网页 PPT (Magazine Web Deck)
        self._skills["deck-magazine-web"] = SkillTemplate(
            name="deck-magazine-web",
            zh_name="杂志风网页 PPT",
            en_name="Magazine Web Deck",
            emoji="📰",
            category=SkillCategory.DECK,
            description="电子杂志 × 电子墨水风, WebGL 流体背景 + 衬线 display",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Playfair Display, Noto Serif SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Cover (衬线 display + WebGL 流体背景)", "desc": "Cover (衬线 display + WebGL 流体背景)"}, {"name": "章节幕封页", "desc": "章节幕封页"}, {"name": "数据大字报页 (一个巨数字 + 一句解释)", "desc": "数据大字报页 (一个巨数字 + 一句解释)"}, {"name": "图片网格页", "desc": "图片网格页"}, {"name": "金句页 (Sunday-paper 风)", "desc": "金句页 (Sunday-paper 风)"}],
            recommended=99,
            tags=["magazine", "editorial", "e-ink", "horizontal swipe"]
        )

        # GitHub Dark 紫渐变 Deck (Obsidian Claude Gradient Deck)
        self._skills["deck-obsidian-claude"] = SkillTemplate(
            name="deck-obsidian-claude",
            zh_name="GitHub Dark 紫渐变 Deck",
            en_name="Obsidian Claude Gradient Deck",
            emoji="🌃",
            category=SkillCategory.DECK,
            description="GitHub-dark + 紫蓝环境光 + 三色渐变标题 + GitHub 风代码",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "GitHub-dark #0d1117 + 紫蓝 radial 环境光 + 60px 网格 mask", "desc": "GitHub-dark #0d1117 + 紫蓝 radial 环境光 + 60px 网格 mask"}, {"name": "居中布局 + 紫色 pill tag", "desc": "居中布局 + 紫色 pill tag"}, {"name": "三色渐变标题 (#a855f7→#60a5fa→#34d399)", "desc": "三色渐变标题 (#a855f7→#60a5fa→#34d399)"}, {"name": "GitHub 风代码 palette + 紫色左边框高亮块", "desc": "GitHub 风代码 palette + 紫色左边框高亮块"}],
            recommended=99,
            tags=["github", "dark", "purple", "mcp", "agent"]
        )

        # 1920 画布自由 Deck (Open-Slide 1920 Canvas Deck)
        self._skills["deck-open-slide-canvas"] = SkillTemplate(
            name="deck-open-slide-canvas",
            zh_name="1920 画布自由 Deck",
            en_name="Open-Slide 1920 Canvas Deck",
            emoji="🎨",
            category=SkillCategory.DECK,
            description="锁死 1920×1080 画布, React 组件级自由组合, 不绑模板",
            constraints=DesignConstraints(
                accent="#f1efea",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter Tight, Noto Sans SC",
                font_body="Inter Tight, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=["- **绝对禁止 overflow**: 每页内容必须 fit in 1920×1080, 不许滚动条出现。", "- 不许塞两段平等的文字; 真要并列就上 3 列等权重网格。", "- 严禁 emoji 装饰 (内容里的允许); 严禁多色彩虹; accent 只用一个色。", "- 严禁 SVG icon 套用 lucide / feather 等通用库 (自己写 inline SVG)。", "- 必须用用户的真实内容; 严禁 lorem ipsum。"],
                required=[]
            ),
            layouts=[{"name": "画布: 每页严格 `width: 1920px; height: 1080px;` 用 `transform: sc", "desc": "画布: 每页严格 `width: 1920px; height: 1080px;` 用 `transform: scale(...)` 适配视窗 (默认 `scale(0.7)` 居中)。"}, {"name": "字号 type scale (px): `2xs:18 · xs:22 · sm:28 · md:36 · lg:4", "desc": "字号 type scale (px): `2xs:18 · xs:22 · sm:28 · md:36 · lg:48 · xl:64 · 2xl:88 · 3xl:120 · 4xl:160 · 5xl:220`。"}, {"name": "边距 padding: 96 / 128 / 160 三档之一。", "desc": "边距 padding: 96 / 128 / 160 三档之一。"}, {"name": "每页有 `<section class=\"slide\" data-slide-id=\"<n>\">`。", "desc": "每页有 `<section class=\"slide\" data-slide-id=\"<n>\">`。"}, {"name": "🌫 **Ash & Lime** — bg `#f1efea`, ink `#161616`, accent `#c", "desc": "🌫 **Ash & Lime** — bg `#f1efea`, ink `#161616`, accent `#c5e803`。"}],
            recommended=9,
            tags=["canvas", "open-slide", "freeform", "1920", "react"]
        )

        # 投资人 Pitch Deck (Investor Pitch Deck)
        self._skills["deck-pitch"] = SkillTemplate(
            name="deck-pitch",
            zh_name="投资人 Pitch Deck",
            en_name="Investor Pitch Deck",
            emoji="🚀",
            category=SkillCategory.DECK,
            description="10 页融资 deck, 白底 + 蓝紫渐变 hero, traction 柱状, $X.XM ask",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Cover (Logo + Tagline + Round/$Ask)", "desc": "Cover (Logo + Tagline + Round/$Ask)"}, {"name": "Problem · Solution · Why Now", "desc": "Problem · Solution · Why Now"}, {"name": "Product (截图占位)", "desc": "Product (截图占位)"}, {"name": "Market size (TAM/SAM/SOM)", "desc": "Market size (TAM/SAM/SOM)"}, {"name": "Traction (柱状图大数字)", "desc": "Traction (柱状图大数字)"}],
            recommended=99,
            tags=["pitch", "investor", "seed", "vc"]
        )

        # Replit Slides 风 Deck (Replit Slides Deck)
        self._skills["deck-replit"] = SkillTemplate(
            name="deck-replit",
            zh_name="Replit Slides 风 Deck",
            en_name="Replit Slides Deck",
            emoji="🟣",
            category=SkillCategory.DECK,
            description="Replit Slides 八套主题 (helix/holm/vance/bevel/world/atlas/bluehouse)",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Pick one theme: helix / holm / vance / bevel / world-dark ", "desc": "Pick one theme: helix / holm / vance / bevel / world-dark / world-mint / atlas / bluehouse"}, {"name": "Cover + agenda + N 个 content + 收尾 (N 由【用户内容】长度决定, 完整覆盖每个要点", "desc": "Cover + agenda + N 个 content + 收尾 (N 由【用户内容】长度决定, 完整覆盖每个要点; 短内容 6-10 起步, 长内容应更多)"}, {"name": "每套主题有完整调色板 + 字体 + accent, 不要混用", "desc": "每套主题有完整调色板 + 字体 + accent, 不要混用"}],
            recommended=99,
            tags=["replit", "themed", "memo"]
        )

        # 瑞士国际主义 Deck (Swiss International Deck)
        self._skills["deck-swiss-international"] = SkillTemplate(
            name="deck-swiss-international",
            zh_name="瑞士国际主义 Deck",
            en_name="Swiss International Deck",
            emoji="🟦",
            category=SkillCategory.DECK,
            description="16 列网格 + 单一饱和 accent + 22 个锁死版面 (Klein Blue / Lemon / Mint / Safety Orange)",
            constraints=DesignConstraints(
                accent="#002FA7",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter Tight, Noto Sans SC",
                font_body="Inter Tight, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=["主题**只能从下面 4 套二选一, 不许混用、不许改 hex**:", "- 🟡 **Lemon Yellow** — accent `#FFD500`, paper `#f7f5ee` (淡奶油), ink `#0a0a0a`. 年轻 / 零售 / 体育。文字必须用黑色 (不能白色)。", "布局 — 22 个可复用版式池, 不许新增或改造版式; **数量由内容决定**, 把用户内容完整覆盖完为止 (短内容 6-10 张起步, 长内容应远超此范围, 同一版式可在不同章节重复使用)", "- **1px hairline borders**, 黑色或 accent; 严禁阴影 / 渐变 / blur。", "- **字体**: Inter Tight (Latin display) / Inter (body) / Noto Sans SC (中文) / JetBrains Mono (数据); 严禁衬线、严禁装饰字体。"],
                required=[]
            ),
            layouts=[{"name": "🔵 **Klein Blue (IKB)** — accent `#002FA7`, paper `#fafaf8`", "desc": "🔵 **Klein Blue (IKB)** — accent `#002FA7`, paper `#fafaf8`, ink `#0a0a0a`. 商业 / AI / 设计场景。"}, {"name": "🟡 **Lemon Yellow** — accent `#FFD500`, paper `#f7f5ee` (淡奶", "desc": "🟡 **Lemon Yellow** — accent `#FFD500`, paper `#f7f5ee` (淡奶油), ink `#0a0a0a`. 年轻 / 零售 / 体育。文字必须用黑色 (不能白色)。"}, {"name": "🟢 **Lemon Green / Neon** — accent `#C5E803`, paper `#f7f5e", "desc": "🟢 **Lemon Green / Neon** — accent `#C5E803`, paper `#f7f5ee`, ink `#0a0a0a`. 可持续 / 科技初创 / Gen-Z 品牌。文字必须用黑色。"}, {"name": "🟠 **Safety Orange** — accent `#FF6B35`, paper `#f7f5ee`, i", "desc": "🟠 **Safety Orange** — accent `#FF6B35`, paper `#f7f5ee`, ink `#0a0a0a`. 工业 / 汽车 / 紧急消息。文字用白色 + bold ≥ 600。"}, {"name": "**S01 Cover** — 全屏 accent + ASCII 呼吸点阵 + 反白标题 + 元数据 chrome", "desc": "**S01 Cover** — 全屏 accent + ASCII 呼吸点阵 + 反白标题 + 元数据 chrome (date / № / topic)。"}],
            recommended=2,
            tags=["swiss", "grid", "international", "ikb", "editorial", "facts"]
        )

        # 马卡龙慢生活 Deck (Pastel Slow-life Deck)
        self._skills["deck-xhs-pastel"] = SkillTemplate(
            name="deck-xhs-pastel",
            zh_name="马卡龙慢生活 Deck",
            en_name="Pastel Slow-life Deck",
            emoji="🍡",
            category=SkillCategory.DECK,
            description="奶油底 + 柔光 blob + 马卡龙圆角卡片 + Playfair 斜体序号",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "奶油 #fef8f1 底 + 三个柔光 blob", "desc": "奶油 #fef8f1 底 + 三个柔光 blob"}, {"name": "Playfair 斜体衬线 display + sans 正文", "desc": "Playfair 斜体衬线 display + sans 正文"}, {"name": "28px 圆角马卡龙卡片 (桃 / 薄荷 / 天 / 紫 / 柠 / 玫)", "desc": "28px 圆角马卡龙卡片 (桃 / 薄荷 / 天 / 紫 / 柠 / 玫)"}, {"name": "Playfair 斜体 01-04 序号", "desc": "Playfair 斜体 01-04 序号"}, {"name": "SVG donut 图 + chip+page 顶栏", "desc": "SVG donut 图 + chip+page 顶栏"}],
            recommended=99,
            tags=["xhs", "pastel", "lifestyle", "lifestyle"]
        )

        # Kami 羊皮纸文档 (Kami Parchment Document)
        self._skills["doc-kami-parchment"] = SkillTemplate(
            name="doc-kami-parchment",
            zh_name="Kami 羊皮纸文档",
            en_name="Kami Parchment Document",
            emoji="📜",
            category=SkillCategory.DOC,
            description="暖羊皮纸底 (#f5f4ed) + 墨蓝单色 accent (#1B365D) + 单一衬线字体, 编辑级排印",
            constraints=DesignConstraints(
                accent="#f5f4ed",
                paper="#ffffff",
                ink="#000000",
                font_display="Charter, Noto Serif SC",
                font_body="Charter, Noto Serif SC",
                font_mono="JetBrains Mono",
                forbidden=["硬性视觉签名 — 不许改", "- **唯一色彩**: 墨蓝 `#1B365D` ——所有 accent (链接、tag 描边、重点数字、引用左 rule) 只能用这一个色, 严禁多色。"],
                required=[]
            ),
            layouts=[{"name": "**画布**: 暖羊皮纸 `#f5f4ed` (永远不用纯白 `#fff`)。次级背景 `#efeee5`。", "desc": "**画布**: 暖羊皮纸 `#f5f4ed` (永远不用纯白 `#fff`)。次级背景 `#efeee5`。"}, {"name": "**墨色**: 主文字 `#1f1d18` (近黑暖灰, 不用纯黑 `#000`)。次文字 `#6b665b`。", "desc": "**墨色**: 主文字 `#1f1d18` (近黑暖灰, 不用纯黑 `#000`)。次文字 `#6b665b`。"}, {"name": "**唯一色彩**: 墨蓝 `#1B365D` ——所有 accent (链接、tag 描边、重点数字、引用左 rul", "desc": "**唯一色彩**: 墨蓝 `#1B365D` ——所有 accent (链接、tag 描边、重点数字、引用左 rule) 只能用这一个色, 严禁多色。"}, {"name": "**字体**: 一种语言一种衬线, 全文不混用:", "desc": "**字体**: 一种语言一种衬线, 全文不混用:"}, {"name": "英文: `Charter` (fallback: `Source Serif Pro`, `Iowan Old St", "desc": "英文: `Charter` (fallback: `Source Serif Pro`, `Iowan Old Style`)"}],
            recommended=3,
            tags=["kami", "parchment", "serif", "editorial", "report", "letter", "one-pager"]
        )

        # 故障艺术标题帧 (Glitch Title Frame)
        self._skills["frame-glitch-title"] = SkillTemplate(
            name="frame-glitch-title",
            zh_name="故障艺术标题帧",
            en_name="Glitch Title Frame",
            emoji="⚡",
            category=SkillCategory.FRAME,
            description="数字故障 / 像散偏移 / 数据腐败标题, 适合视频转场 / cyberpunk hero",
            constraints=DesignConstraints(
                accent="#070708",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter Tight, Noto Sans SC",
                font_body="Inter Tight, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=["- 颜色仅用: 黑 / 白 / cyan / magenta / 一点 amber 警告色; 严禁全彩虹。", "- 严禁 lorem ipsum; 必须用用户的标题 + 副标。"],
                required=[]
            ),
            layouts=[{"name": "居中, 6-9vw, weight 800/900, 字体 `Space Grotesk Bold` / `Inte", "desc": "居中, 6-9vw, weight 800/900, 字体 `Space Grotesk Bold` / `Inter Tight Black` / `JetBrains Mono Bold`。"}, {"name": "颜色: 主层 `#f5f5f7`; 后面套 2 层伪影:", "desc": "颜色: 主层 `#f5f5f7`; 后面套 2 层伪影:"}, {"name": "cyan `#00f0ff` translate(`-3px`, `1px`)。", "desc": "cyan `#00f0ff` translate(`-3px`, `1px`)。"}, {"name": "magenta `#ff2bd6` translate(`3px`, `-1px`)。", "desc": "magenta `#ff2bd6` translate(`3px`, `-1px`)。"}, {"name": "整层加 clip-path 切片 5-8 段, 每段 `@keyframes` 随机 translateX -10p", "desc": "整层加 clip-path 切片 5-8 段, 每段 `@keyframes` 随机 translateX -10px → 10px, 持续 80-160ms, 错峰播放, 营造 \"data corruption\" 像散。"}],
            recommended=6,
            tags=["glitch", "cyberpunk", "title", "transition", "vfx", "frame"]
        )

        # 品牌 Logo 收尾帧 (Logo Outro Frame)
        self._skills["frame-logo-outro"] = SkillTemplate(
            name="frame-logo-outro",
            zh_name="品牌 Logo 收尾帧",
            en_name="Logo Outro Frame",
            emoji="🎬",
            category=SkillCategory.FRAME,
            description="Logo 分块组装入场 + glow bloom + tagline 揭示, 适合视频片尾 / 品牌闭幕",
            constraints=DesignConstraints(
                accent="#08090c",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter Tight, Noto Sans SC",
                font_body="Inter Tight, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "**中心 Logo**: 用 CSS / 内联 SVG 绘制; 由 4-8 个几何块 (圆 / 方 / 三角 / h", "desc": "**中心 Logo**: 用 CSS / 内联 SVG 绘制; 由 4-8 个几何块 (圆 / 方 / 三角 / hairline) 组成。"}, {"name": "入场动画: 每个块从屏幕外滑入 (±100px 不同方向) + scale 1.4→1.0 + opacity 0→", "desc": "入场动画: 每个块从屏幕外滑入 (±100px 不同方向) + scale 1.4→1.0 + opacity 0→1, 错峰 80ms; 总时长 1.2s。"}, {"name": "入场完成后, 整个 logo 加 glow bloom: `filter: drop-shadow(0 0 24px", "desc": "入场完成后, 整个 logo 加 glow bloom: `filter: drop-shadow(0 0 24px <accent>40)`; 同时一道 shimmer `mask-image` 横扫 logo (500ms)。"}, {"name": "**品牌名**: logo 下方 6-8% 位置, 大字 (Inter Tight / SF Pro Display", "desc": "**品牌名**: logo 下方 6-8% 位置, 大字 (Inter Tight / SF Pro Display, 48-72px, weight 700, letter-spacing -0.02em), 入场: typewriter or fade-up after logo bloom (1.4s 开始)。"}, {"name": "**Tagline**: 品牌名下方一行 (24-28px, weight 400, opacity 0.7), f", "desc": "**Tagline**: 品牌名下方一行 (24-28px, weight 400, opacity 0.7), fade in (1.8s)。"}],
            recommended=8,
            tags=["logo", "outro", "branding", "end-card", "frame"]
        )

        # macOS 通知横幅 (macOS Notification Banner)
        self._skills["frame-macos-notification"] = SkillTemplate(
            name="frame-macos-notification",
            zh_name="macOS 通知横幅",
            en_name="macOS Notification Banner",
            emoji="🔔",
            category=SkillCategory.SOCIAL,
            description="拟真 macOS 通知 banner + app icon + 标题正文, 适合 video overlay / 产品发布预告",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=["- icon 不能用外链 emoji 图片, 用 unicode emoji 或 CSS 绘制几何。"],
                required=[]
            ),
            layouts=[{"name": "视频叠加 1920×1080, 通知放右上角, 周围透明。", "desc": "视频叠加 1920×1080, 通知放右上角, 周围透明。"}, {"name": "单独 banner 480×120, 居中输出。", "desc": "单独 banner 480×120, 居中输出。"}, {"name": "外框: 圆角 14px (macOS Big Sur 标准), 480×120 (或更长 480×180 含正文),", "desc": "外框: 圆角 14px (macOS Big Sur 标准), 480×120 (或更长 480×180 含正文), 12-16px 内边距。"}, {"name": "背景: **frosted glass** 效果 — `background: rgba(245,245,247,0", "desc": "背景: **frosted glass** 效果 — `background: rgba(245,245,247,0.78)` + `backdrop-filter: blur(40px) saturate(180%)`; 暗色版 `rgba(28,28,30,0.78)`。"}, {"name": "边框: 1px `rgba(0,0,0,0.06)` (light) / `rgba(255,255,255,0.0", "desc": "边框: 1px `rgba(0,0,0,0.06)` (light) / `rgba(255,255,255,0.08)` (dark); 顶部加 1px 亮 highlight `rgba(255,255,255,0.5)`。"}],
            recommended=99,
            tags=["macos", "notification", "banner", "overlay", "frame"]
        )

        # 杂志风海报 (Magazine Poster)
        self._skills["magazine-poster"] = SkillTemplate(
            name="magazine-poster",
            zh_name="杂志风海报",
            en_name="Magazine Poster",
            emoji="🗞️",
            category=SkillCategory.POSTER,
            description="Sunday-paper 风格, 大字 serif headline + 双栏正文 + 编号 sections",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Playfair Display, Noto Serif SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "Dateline 顶栏 (publication / date / issue)", "desc": "Dateline 顶栏 (publication / date / issue)"}, {"name": "Oversized serif headline (含 strike-through 词 + 斜体 accent)", "desc": "Oversized serif headline (含 strike-through 词 + 斜体 accent)"}, {"name": "双栏 body 正文", "desc": "双栏 body 正文"}, {"name": "6 个编号 sections, 每个含小标题 + 1-2 段 + pull-quote", "desc": "6 个编号 sections, 每个含小标题 + 1-2 段 + pull-quote"}, {"name": "底部署名 + 小 ornament", "desc": "底部署名 + 小 ornament"}],
            recommended=4,
            tags=["magazine", "newsprint", "editorial", "manifesto"]
        )

        # VFX 文字光标 (VFX Text Cursor)
        self._skills["vfx-text-cursor"] = SkillTemplate(
            name="vfx-text-cursor",
            zh_name="VFX 文字光标",
            en_name="VFX Text Cursor",
            emoji="✨",
            category=SkillCategory.FRAME,
            description="光标拖光 + 彩色像散射线 + 定向光斑, 适合视频片头逐字揭示金句",
            constraints=DesignConstraints(
                accent="#06070a",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter Tight, Noto Sans SC",
                font_body="Inter Tight, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=["- 字体: 西文 `Inter Tight` Bold; 中文 `Noto Sans SC` Bold; 严禁衬线。"],
                required=[]
            ),
            layouts=[{"name": "一句金句 (中英不限), 居中, 字号 6-8vw, weight 700, 字体 `Inter Tight` / ", "desc": "一句金句 (中英不限), 居中, 字号 6-8vw, weight 700, 字体 `Inter Tight` / `Source Sans 3` / `Noto Sans SC`。"}, {"name": "逐字揭示, 每个字符 80ms 间隔; 当前字符后面跟着一个 cursor `▍` (或细 vertical bar", "desc": "逐字揭示, 每个字符 80ms 间隔; 当前字符后面跟着一个 cursor `▍` (或细 vertical bar)。"}, {"name": "已揭示文字默认白色 `#f5f5f7`, opacity 1; 即将揭示位置加 chromatic ghost: 一", "desc": "已揭示文字默认白色 `#f5f5f7`, opacity 1; 即将揭示位置加 chromatic ghost: 一份 `text-shadow: 2px 0 #ff3b6f, -2px 0 #00d4ff` 在 reveal 瞬间, 200ms 内收敛回正常。"}, {"name": "光标本身: 16px 宽矩形, 颜色 = accent (取 1: hot pink `#ff3b6f` / cya", "desc": "光标本身: 16px 宽矩形, 颜色 = accent (取 1: hot pink `#ff3b6f` / cyan `#00d4ff` / amber `#ffb547`), 闪烁 `@keyframes` 1.0s 周期; 后面拖一条 60-120px 的 motion blur trail (径向渐变到透明)。"}, {"name": "在打字位置附近随机生成 3-5 道**定向光斑** (light leak): 用 `linear-gradient", "desc": "在打字位置附近随机生成 3-5 道**定向光斑** (light leak): 用 `linear-gradient(45deg, transparent, accent20, transparent)` 的细长矩形 + `mix-blend-mode: screen`, 不规则角度。"}],
            recommended=7,
            tags=["vfx", "text", "cursor", "chromatic", "reveal", "frame"]
        )

        # Hyperframes 视频脚本 (Hyperframes Video)
        self._skills["video-hyperframes"] = SkillTemplate(
            name="video-hyperframes",
            zh_name="Hyperframes 视频脚本",
            en_name="Hyperframes Video",
            emoji="🎞️",
            category=SkillCategory.FRAME,
            description="Hyperframes / Remotion 兼容的连续帧动画, 可自动播放",
            constraints=DesignConstraints(
                accent="#000000",
                paper="#ffffff",
                ink="#000000",
                font_display="Inter, Noto Sans SC",
                font_body="Inter, Noto Sans SC",
                font_mono="JetBrains Mono",
                forbidden=[],
                required=[]
            ),
            layouts=[{"name": "输出 N 个连续 `<section class=\"frame\">`, 每个 `w-[1920px] h-[1080", "desc": "输出 N 个连续 `<section class=\"frame\">`, 每个 `w-[1920px] h-[1080px]`; N 由【用户内容】信息密度决定 (短脚本 6-10 帧起步, 长脚本应更多, 每帧只承载一个镜头/概念)。"}, {"name": "每帧表达一个镜头/概念: 文字 + 视觉构图 (中央构图 / 黄金分割 / 三分法)。", "desc": "每帧表达一个镜头/概念: 文字 + 视觉构图 (中央构图 / 黄金分割 / 三分法)。"}, {"name": "每帧底部隐藏标记 `<!-- frame:N duration:3000 transition:fade -->` ", "desc": "每帧底部隐藏标记 `<!-- frame:N duration:3000 transition:fade -->` 供后续 Remotion / Hyperframes 渲染脚本读取。"}, {"name": "顶部加一段 JavaScript 自动播放: 每 3 秒切换到下一帧, 也支持点击 / 方向键控制; 角落显示进度条", "desc": "顶部加一段 JavaScript 自动播放: 每 3 秒切换到下一帧, 也支持点击 / 方向键控制; 角落显示进度条。"}, {"name": "第 1 帧是 hook (一个数据 / 一个反常识 / 一个问题), 第 2-N 是论证, 最后是结论 + CTA。", "desc": "第 1 帧是 hook (一个数据 / 一个反常识 / 一个问题), 第 2-N 是论证, 最后是结论 + CTA。"}],
            recommended=5,
            tags=["video", "hyperframes", "remotion", "视频"]
        )


    def get(self, name: str) -> Optional[SkillTemplate]:
        return self._skills.get(name)

    def list_all(self) -> List[SkillTemplate]:
        return list(self._skills.values())

    def list_by_category(self, cat: SkillCategory) -> List[SkillTemplate]:
        return [s for s in self._skills.values() if s.category == cat]

    def get_recommended(self, limit: int = 8) -> List[SkillTemplate]:
        return sorted(self._skills.values(), key=lambda x: x.recommended)[:limit]

    def search(self, q: str) -> List[SkillTemplate]:
        q = q.lower()
        return [s for s in self._skills.values()
                if q in s.zh_name.lower() or q in s.en_name.lower()
                or q in s.description.lower() or any(q in t.lower() for t in s.tags)]

    def to_json(self) -> str:
        return json.dumps({k: {"name": v.name, "zh_name": v.zh_name,
            "category": v.category.value, "description": v.description}
            for k, v in self._skills.items()}, ensure_ascii=False, indent=2)


# 全局注册表实例
registry = SkillRegistry()


if __name__ == "__main__":
    r = SkillRegistry()
    print(f"SKILL Registry: {len(r.list_all())} skills loaded")
    from collections import Counter
    cats = Counter(s.category.value for s in r.list_all())
    print(f"Categories: {dict(cats)}")
    for c, n in cats.most_common():
        print(f"  {c}: {n}")
    print()
    print("Top 5 recommended:")
    for s in r.get_recommended(5):
        print(f"  {s.emoji} {s.zh_name} (rank: {s.recommended})")
    print()
    print("Search test: deck ->", [s.name for s in r.search("deck")])