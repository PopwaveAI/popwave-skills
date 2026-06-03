"""
HTML Renderer - 核心渲染引擎
将数据 + SKILL 模板 → 高质量 HTML
"""

import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import asdict

# 尝试导入 jinja2，如果没有则使用简单模板
try:
    from jinja2 import Environment, BaseLoader, select_autoescape
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False
    print("[WARN] jinja2 not available, using simple template engine")

try:
    from .skill_registry import SkillRegistry, SkillTemplate, SkillCategory
except ImportError:
    from skill_registry import SkillRegistry, SkillTemplate, SkillCategory


class HTMLRenderer:
    """
    HTML 渲染器 - 融合 html-anything 设计系统
    
    使用方式:
        renderer = HTMLRenderer()
        
        # 方式1: 直接渲染
        html = renderer.render("swiss-international", {
            "title": "{project_name}",
            "characters": [...]
        })
        
        # 方式2: 生成 Prompt 给 LLM
        prompt = renderer.generate_prompt("swiss-international", {
            "title": "{project_name}",
            "characters": [...]
        })
        # LLM 生成 HTML → renderer.validate_and_fix(html)
    """
    
    def __init__(self, templates_dir: Optional[str] = None):
        self.registry = SkillRegistry()
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(__file__), "templates"
        )
        # 兼容新旧命名
        self._skill_aliases = {
            "swiss-international": "deck-swiss-international",
            "kami-parchment": "doc-kami-parchment",
            "guizang-editorial": "deck-guizang-editorial",
            "glitch-title": "frame-glitch-title",
            "hermes-cyber": "deck-hermes-cyber",
            "magazine-poster": "magazine-poster",
            "article-magazine": "article-magazine",
            "data-report": "data-report",
            "dashboard": "dashboard",
        }
        
        if JINJA_AVAILABLE:
            self.jinja = Environment(
                loader=BaseLoader(),
                autoescape=select_autoescape(['html', 'xml'])
            )
        else:
            self.jinja = None
    
    def _resolve_skill_name(self, name: str) -> str:
        """解析 SKILL 名称，兼容新旧命名"""
        return self._skill_aliases.get(name, name)
    
    def get_skill(self, name: str) -> Optional[SkillTemplate]:
        """获取 SKILL（自动兼容别名）"""
        resolved = self._resolve_skill_name(name)
        return self.registry.get(resolved)
    
    def render(self, 
               skill_name: str, 
               data: Dict[str, Any],
               output_path: Optional[str] = None) -> str:
        """
        渲染 HTML
        
        Args:
            skill_name: SKILL 名称 (如 "deck-swiss-international")
            data: 渲染数据
            output_path: 可选，输出文件路径
        
        Returns:
            HTML 字符串
        """
        # 兼容别名
        resolved_name = self._resolve_skill_name(skill_name)
        skill = self.registry.get(resolved_name)
        if not skill:
            raise ValueError(f"Unknown skill: {skill_name} (resolved: {resolved_name})")
        
        # 根据 SKILL 类型选择渲染策略
        if skill.category == SkillCategory.DECK:
            html = self._render_deck(skill, data)
        elif skill.category == SkillCategory.DOC:
            html = self._render_doc(skill, data)
        elif skill.category == SkillCategory.POSTER:
            html = self._render_poster(skill, data)
        else:
            html = self._render_generic(skill, data)
        
        # 验证并修复
        html = self.validate_and_fix(html, skill)
        
        # 保存到文件
        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[HTMLRenderer] Saved to: {output_path}")
        
        return html
    
    def generate_prompt(self, skill_name: str, data: Dict[str, Any]) -> str:
        """
        生成 LLM Prompt
        用于让 LLM 直接生成符合设计系统的 HTML
        """
        resolved_name = self._resolve_skill_name(skill_name)
        skill = self.registry.get(resolved_name)
        if not skill:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        # 基础 SKILL 约束
        prompt = skill.to_prompt()
        
        # 添加数据
        prompt += f"""
【用户数据】
{json.dumps(data, ensure_ascii=False, indent=2)}

【输出要求】
1. 生成完整、独立的单文件 HTML
2. 使用 Tailwind CSS CDN: https://cdn.tailwindcss.com
3. 使用 Google Fonts CDN 加载指定字体
4. 所有样式内联，不要外链 CSS 文件
5. 严格遵循上述【硬性约束】，违反则设计失败
6. 布局从【布局池】中选择合适的版式
7. 输出格式: ```html\n...\n```
"""
        return prompt
    
    def validate_and_fix(self, html: str, skill: SkillTemplate) -> str:
        """
        验证 HTML 是否符合 SKILL 约束，并尝试自动修复
        """
        constraints = skill.constraints
        
        # 检查禁止项
        for forbidden in constraints.forbidden:
            if "圆角" in forbidden and "border-radius" in html:
                # 自动修复: 移除 border-radius
                import re
                html = re.sub(r'border-radius:\s*[^;]+;', 'border-radius: 0;', html)
            if "阴影" in forbidden and "box-shadow" in html:
                # 警告但不自动移除，因为可能是必要的
                pass
            if "渐变" in forbidden and "gradient" in html.lower():
                pass
        
        # 确保有必要的 meta 标签
        if "<html" not in html:
            html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{skill.zh_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
{html}
</body>
</html>"""
        
        return html
    
    def _render_deck(self, skill: SkillTemplate, data: Dict[str, Any]) -> str:
        """渲染 Deck 类型 (演示稿)"""
        c = skill.constraints
        
        # Swiss International 风格
        if skill.name == "deck-swiss-international":
            return self._render_swiss_deck(skill, data)
        
        # Guizang Editorial 风格
        if skill.name == "deck-guizang-editorial":
            return self._render_guizang_deck(skill, data)
        
        # 通用 Deck
        return self._render_generic(skill, data)
    
    def _render_swiss_deck(self, skill: SkillTemplate, data: Dict[str, Any]) -> str:
        """Swiss International 风格渲染"""
        c = skill.constraints
        title = data.get("title", "Untitled")
        subtitle = data.get("subtitle", "")
        items = data.get("items", data.get("characters", []))
        
        # 生成 HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --accent: {c.accent};
            --paper: {c.paper};
            --ink: {c.ink};
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; border-radius: 0 !important; }}
        body {{ 
            font-family: 'Inter Tight', 'Noto Sans SC', sans-serif; 
            background: var(--paper); 
            color: var(--ink);
        }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .border-hairline {{ border-color: var(--ink); }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="w-full" style="background: var(--accent); color: white;">
        <div class="grid grid-cols-16 gap-0" style="display: grid; grid-template-columns: repeat(16, 1fr);">
            <div class="col-span-12 p-10">
                <div class="font-mono text-xs opacity-50 mb-3 tracking-widest">▓▓▓▓▓▓▓▓░░░░░░░░░░░ 47%</div>
                <h1 class="text-5xl font-extrabold tracking-tight leading-none mb-4">{title}</h1>
                <p class="font-mono text-sm uppercase tracking-widest opacity-80">{subtitle}</p>
            </div>
            <div class="col-span-4 p-10 border-l border-white/30 flex flex-col justify-end items-end text-right">
                <div class="font-mono text-xs opacity-60 leading-relaxed">
                    Document ID<br>HC-001<br><br>Last Updated<br>2026.01
                </div>
            </div>
        </div>
    </header>
    
    <!-- Content -->
    <main>
        <div class="flex justify-between items-center px-10 py-6 border-b border-black">
            <span class="font-mono text-xs uppercase tracking-widest opacity-50">Featured Items</span>
            <span class="font-mono text-xs opacity-50">№ 01 / {len(items):02d}</span>
        </div>
        
        <div class="grid grid-cols-3 gap-0">
"""
        
        # 渲染每个 item
        for i, item in enumerate(items[:3], 1):
            name = item.get("name", item.get("姓名", f"Item {i}"))
            role = item.get("role", item.get("角色", ""))
            desc = item.get("description", item.get("描述", ""))
            stats = item.get("stats", item.get("属性", {}))
            
            html += f"""
            <div class="border-r border-b border-black p-8 relative hover:bg-black/[0.02] transition-colors">
                <span class="absolute top-8 right-8 font-mono text-sm opacity-20">{i:02d}</span>
                <div class="flex gap-4 mb-6">
                    <div class="w-16 h-16 bg-black flex items-center justify-center text-2xl" style="box-shadow: -2px -2px 0 0 var(--accent);">
                        {item.get("avatar", item.get("头像", "◆"))}
                    </div>
                    <div>
                        <div class="font-mono text-xs uppercase tracking-wider mb-1" style="color: var(--accent);">{role}</div>
                        <h2 class="text-xl font-bold tracking-tight">{name}</h2>
                    </div>
                </div>
                <p class="text-sm opacity-70 mb-4 leading-relaxed">{desc}</p>
                <div class="space-y-3">
"""
            # 渲染 stats
            for stat_name, stat_value in list(stats.items())[:3]:
                bar_width = {"S": "95%", "S+": "98%", "A": "85%", "B": "70%", "C": "40%"}.get(stat_value, "50%")
                is_highlight = stat_value in ["S", "S+"]
                value_color = "var(--accent)" if is_highlight else "var(--ink)"
                html += f"""
                    <div class="flex items-center gap-4">
                        <span class="font-mono text-xs uppercase opacity-50 w-20">{stat_name}</span>
                        <span class="text-2xl font-extrabold" style="color: {value_color};">{stat_value}</span>
                        <div class="flex-1 h-1 bg-black/10">
                            <div class="h-full" style="width: {bar_width}; background: var(--accent);"></div>
                        </div>
                    </div>
"""
            html += """
                </div>
            </div>
"""
        
        html += """
        </div>
    </main>
    
    <!-- Footer -->
    <footer class="bg-black text-white px-10 py-6">
        <div class="flex justify-between items-center">
            <div class="flex items-center gap-8">
                <span class="font-bold tracking-tight">""" + title + """</span>
                <span class="font-mono text-xs uppercase opacity-50">Character Archive System v1.0</span>
            </div>
            <div class="flex gap-8">
                <span class="font-mono text-xs uppercase opacity-50">Data: Ch.001-388</span>
                <span class="font-mono text-xs uppercase opacity-50">2026.01</span>
            </div>
        </div>
    </footer>
</body>
</html>"""
        
        return html
    
    def _render_guizang_deck(self, skill: SkillTemplate, data: Dict[str, Any]) -> str:
        """Guizang Editorial 风格渲染"""
        # 类似实现...
        return self._render_generic(skill, data)
    
    def _render_doc(self, skill: SkillTemplate, data: Dict[str, Any]) -> str:
        """渲染 Doc 类型 (文档)"""
        c = skill.constraints
        title = data.get("title", "Untitled")
        content = data.get("content", "")
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Charter&family=Noto+Serif+SC:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Charter', 'Noto Serif SC', serif;
            background: {c.paper};
            color: {c.ink};
            line-height: 1.5;
        }}
        .accent {{ color: {c.accent}; }}
        .accent-bg {{ background: {c.accent}; }}
        .accent-border {{ border-color: {c.accent}; }}
    </style>
</head>
<body class="max-w-3xl mx-auto px-8 py-16">
    <article class="prose prose-lg max-w-none">
        {content}
    </article>
</body>
</html>"""
    
    def _render_poster(self, skill: SkillTemplate, data: Dict[str, Any]) -> str:
        """渲染 Poster 类型 (海报)"""
        return self._render_generic(skill, data)
    
    def _render_generic(self, skill: SkillTemplate, data: Dict[str, Any]) -> str:
        """通用渲染"""
        c = skill.constraints
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{skill.zh_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {{
            --accent: {c.accent};
            --paper: {c.paper};
            --ink: {c.ink};
        }}
        body {{
            background: var(--paper);
            color: var(--ink);
        }}
    </style>
</head>
<body class="p-8">
    <pre>{json.dumps(data, ensure_ascii=False, indent=2)}</pre>
</body>
</html>"""


# 便捷函数
def render_html(skill_name: str, data: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """便捷渲染函数"""
    renderer = HTMLRenderer()
    return renderer.render(skill_name, data, output_path)


def generate_skill_prompt(skill_name: str, data: Dict[str, Any]) -> str:
    """便捷 Prompt 生成函数"""
    renderer = HTMLRenderer()
    return renderer.generate_prompt(skill_name, data)


if __name__ == "__main__":
    # 测试
    print("=== HTML Renderer Test ===")
    
    renderer = HTMLRenderer()
    
    # 测试数据
    test_data = {
        "title": "{project_name}",
        "subtitle": "Based on Vol.1-4 · 388 Chapters · Character Voice Analysis",
        "characters": [
            {
                "name": "摩根·威廉",
                "role": "★ Protagonist · 七武海",
                "avatar": "🦊",
                "description": "蒸气果实能力者·纳维亚及法莱斯联合王国国王·摩根海贼团船长。",
                "stats": {"战力": "S", "智力": "S+", "魅力": "A"}
            },
            {
                "name": "丹彼尔",
                "role": "Core Member · 首席智囊",
                "avatar": "📚",
                "description": "海贼学者·武器研发者·外交使节。",
                "stats": {"战力": "C", "智力": "S", "外交": "A"}
            }
        ]
    }
    
    # 生成 Prompt
    print("\n=== Swiss International Prompt ===")
    prompt = renderer.generate_prompt("deck-swiss-international", test_data)
    print(prompt[:1000] + "...")
    
    # 直接渲染
    print("\n=== Rendering HTML ===")
    html = renderer.render("deck-swiss-international", test_data)
    print(f"Generated {len(html)} chars")
    print(html[:500] + "...")
