"""
HTML Renderer - html-anything 设计系统融合模块
将 html-anything 的 75 套 SKILL 设计约束集成到 novel-agent-pro 管线

使用方式:
    # 方式0: 节点F·前置决策（pop agent 第一反应）
    from html_renderer import NodeF
    intent = NodeF.decide(
        doc_type="scene_card", doc_name="纸身",
        audience="readers", goal="horror_immersion",
        specialization="游戏UI切入→恐怖排版"
    )
    
    # 方式1: 直接渲染
    from html_renderer import HTMLRenderer
    renderer = HTMLRenderer()
    html = renderer.render(intent.resolved_skill, {"characters": [...]})
    
    # 方式2: 场景化集成
    from html_renderer import NovelAgentIntegration
    integration = NovelAgentIntegration()
    integration.render_character_cards(characters, output_path="...")
"""

from .renderer import HTMLRenderer, render_html, generate_skill_prompt
from .skill_registry import SkillRegistry, SkillTemplate, SkillCategory, DesignConstraints
from .integrations import NovelAgentIntegration, render_to_html
from .pre_render_intent import NodeF, RenderIntent, Audience, EmotionalGoal

__version__ = "1.3.0"
__all__ = [
    "HTMLRenderer", 
    "SkillRegistry", 
    "SkillTemplate", 
    "SkillCategory",
    "DesignConstraints",
    "NovelAgentIntegration",
    "NodeF",
    "RenderIntent",
    "Audience",
    "EmotionalGoal",
    "render_html",
    "generate_skill_prompt",
    "render_to_html"
]
