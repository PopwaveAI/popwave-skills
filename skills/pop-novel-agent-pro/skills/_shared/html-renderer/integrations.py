"""
Integration Layer - 将 html-renderer 集成到 novel-agent-pro skill 管线

使用方式:
    # 在任意 SKILL.md 中:
    输出格式: HTML (swiss-international)
    
    # 在 Python skill 脚本中:
    from html_renderer.integrations import NovelAgentIntegration
    
    integration = NovelAgentIntegration()
    integration.render_character_cards(characters, output_path)
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

try:
    from .renderer import HTMLRenderer, render_html, generate_skill_prompt
    from .skill_registry import SkillRegistry, SkillCategory
except ImportError:
    from renderer import HTMLRenderer, render_html, generate_skill_prompt
    from skill_registry import SkillRegistry, SkillCategory


class NovelAgentIntegration:
    """
    novel-agent-pro 集成类
    
    提供场景化的便捷方法，让现有 skill 可以一键生成高质量 HTML
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        self.renderer = HTMLRenderer()
        self.output_dir = output_dir or os.getcwd()
    
    # ============================================
    # SKILL 名称映射（兼容新旧命名）
    # ============================================
    _SKILL_NAME_MAP = {
        "swiss-international": "deck-swiss-international",
        "kami-parchment": "doc-kami-parchment",
        "guizang-editorial": "deck-guizang-editorial",
        "glitch-title": "frame-glitch-title",
        "hermes-cyber": "deck-hermes-cyber",
        "magazine-poster": "magazine-poster",
        "article-magazine": "article-magazine",
        "data-report": "data-report",
    }
    
    @staticmethod
    def _map_skill_name(name: str) -> str:
        return NovelAgentIntegration._SKILL_NAME_MAP.get(name, name)
    
    # ============================================
    # 场景化渲染方法
    # ============================================
    
    def render_character_cards(self, 
                               characters: List[Dict],
                               title: str = "角色档案",
                               subtitle: str = "",
                               output_path: Optional[str] = None,
                               skill: str = "swiss-international") -> str:
        """
        渲染角色卡片
        
        Args:
            characters: 角色列表，每个角色包含 name, role, avatar, description, stats
            title: 页面标题
            subtitle: 副标题
            output_path: 输出路径
            skill: 使用的 SKILL 模板
        
        Returns:
            HTML 文件路径
        """
        data = {
            "title": title,
            "subtitle": subtitle or f"共 {len(characters)} 位角色",
            "characters": characters
        }
        
        if not output_path:
            output_path = os.path.join(self.output_dir, f"{title}-角色档案.html")
        
        # 兼容新旧命名: swiss-international → deck-swiss-international
        skill_name = self._map_skill_name(skill)
        html = self.renderer.render(skill_name, data, output_path)
        return output_path
    
    def render_relationship_network(self,
                                    nodes: List[Dict],
                                    edges: List[Dict],
                                    title: str = "人物关系网",
                                    output_path: Optional[str] = None) -> str:
        """
        渲染人物关系网络图
        
        Args:
            nodes: 节点列表 [{id, label, group, size}, ...]
            edges: 边列表 [{from, to, label, strength}, ...]
            title: 标题
            output_path: 输出路径
        """
        # 使用 D3.js 或 vis-network 内嵌实现
        data = {
            "title": title,
            "nodes": nodes,
            "edges": edges
        }
        
        if not output_path:
            output_path = os.path.join(self.output_dir, f"{title}-关系网.html")
        
        # 使用 glitch-title 或自定义网络图模板
        html = self._render_network_html(data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
    
    def render_chapter_report(self,
                              chapter_data: Dict,
                              output_path: Optional[str] = None) -> str:
        """
        渲染章节分析报告
        
        Args:
            chapter_data: 章节数据 {
                title: 章节标题,
                summary: 摘要,
                beats: 节拍列表,
                characters: 出场角色,
                metrics: {pace, tension, emotion}
            }
        """
        if not output_path:
            output_path = os.path.join(self.output_dir, f"{chapter_data['title']}-分析报告.html")
        
        # 使用 Kami Parchment 文档风格
        skill_name = self._map_skill_name("kami-parchment")
        html = self.renderer.render(skill_name, chapter_data, output_path)
        return output_path
    
    def render_book_deconstruction(self,
                                   book_data: Dict,
                                   output_path: Optional[str] = None) -> str:
        """
        渲染拆书报告
        
        Args:
            book_data: 书籍数据 {
                title: 书名,
                author: 作者,
                chapters: 章节列表,
                arcs: 剧情弧线,
                characters: 角色分析
            }
        """
        if not output_path:
            output_path = os.path.join(self.output_dir, f"{book_data['title']}-拆书报告.html")
        
        # 使用 Magazine Poster 风格
        skill_name = self._map_skill_name("magazine-poster")
        html = self.renderer.render(skill_name, book_data, output_path)
        return output_path
    
    def render_project_dashboard(self,
                                 project_data: Dict,
                                 output_path: Optional[str] = None) -> str:
        """
        渲染项目仪表盘
        
        Args:
            project_data: 项目数据 {
                name: 项目名称,
                progress: 进度百分比,
                chapters: 章节状态列表,
                metrics: 各种指标
            }
        """
        if not output_path:
            output_path = os.path.join(self.output_dir, f"{project_data['name']}-项目状态.html")
        
        # 使用 Swiss International 风格
        skill_name = self._map_skill_name("swiss-international")
        html = self.renderer.render(skill_name, project_data, output_path)
        return output_path
    
    # ============================================
    # LLM Prompt 生成方法
    # ============================================
    
    def generate_character_card_prompt(self, characters: List[Dict]) -> str:
        """生成角色卡片的 LLM Prompt"""
        data = {
            "title": "角色档案",
            "characters": characters
        }
        return generate_skill_prompt("deck-swiss-international", data)
    
    def generate_report_prompt(self, content: Dict) -> str:
        """生成文档报告的 LLM Prompt"""
        return generate_skill_prompt("kami-parchment", content)
    
    # ============================================
    # 内部方法
    # ============================================
    
    def _render_network_html(self, data: Dict) -> str:
        """渲染网络图 HTML (使用 vis-network)"""
        nodes_json = json.dumps(data["nodes"], ensure_ascii=False)
        edges_json = json.dumps(data["edges"], ensure_ascii=False)
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{data['title']}</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ margin: 0; background: #0a0e1a; color: white; font-family: system-ui; }}
        #network {{ width: 100vw; height: 100vh; }}
        .header {{ position: absolute; top: 20px; left: 20px; z-index: 10; }}
        h1 {{ margin: 0; font-size: 24px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{data['title']}</h1>
    </div>
    <div id="network"></div>
    <script>
        const nodes = new vis.DataSet({nodes_json});
        const edges = new vis.DataSet({edges_json});
        
        const container = document.getElementById('network');
        const data = {{ nodes: nodes, edges: edges }};
        
        const options = {{
            nodes: {{
                shape: 'dot',
                size: 20,
                font: {{ size: 14, color: '#ffffff' }},
                borderWidth: 2
            }},
            edges: {{
                width: 2,
                color: {{ color: '#4a5568', highlight: '#60a5fa' }},
                smooth: {{ type: 'continuous' }}
            }},
            physics: {{
                stabilization: false,
                barnesHut: {{
                    gravitationalConstant: -8000,
                    springConstant: 0.04,
                    springLength: 95
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200
            }}
        }};
        
        new vis.Network(container, data, options);
    </script>
</body>
</html>"""


# ============================================
# 便捷函数
# ============================================

def render_to_html(content_type: str, 
                   data: Dict,
                   output_path: str,
                   skill: str = "deck-swiss-international") -> str:
    """
    便捷函数：根据内容类型自动选择渲染方式
    
    Args:
        content_type: 内容类型 (characters, network, report, dashboard)
        data: 数据
        output_path: 输出路径
        skill: SKILL 模板名称
    """
    integration = NovelAgentIntegration()
    
    if content_type == "characters":
        return integration.render_character_cards(
            data.get("characters", []),
            data.get("title", "角色档案"),
            data.get("subtitle", ""),
            output_path,
            skill
        )
    elif content_type == "network":
        return integration.render_relationship_network(
            data.get("nodes", []),
            data.get("edges", []),
            data.get("title", "关系网"),
            output_path
        )
    elif content_type == "report":
        return integration.render_chapter_report(data, output_path)
    elif content_type == "dashboard":
        return integration.render_project_dashboard(data, output_path)
    else:
        # 通用渲染 - 先映射名称
        mapped_skill = NovelAgentIntegration._map_skill_name(skill)
        return render_html(mapped_skill, data, output_path)


# ============================================
# SKILL.md 集成示例
# ============================================

SKILL_INTEGRATION_EXAMPLE = """
# 在任意 SKILL.md 中集成 HTML 输出

## 输出格式声明

在 SKILL.md 的 frontmatter 或正文中声明：

```yaml
---
output_format: html
skill_template: swiss-international  # 可选: swiss-international, guizang-editorial, kami-parchment
---
```

## 在 Prompt 中使用

```markdown
## 输出要求

1. 使用 HTMLRenderer 生成最终输出
2. SKILL 模板: swiss-international
3. 数据格式:
   ```json
   {
     "title": "...",
     "characters": [...]
   }
   ```

或者直接生成 Prompt:

```python
from html_renderer.integrations import NovelAgentIntegration

integration = NovelAgentIntegration()
prompt = integration.generate_character_card_prompt(characters)
# 将 prompt 发给 LLM，LLM 生成 HTML
```
"""

if __name__ == "__main__":
    # 测试集成
    print("=== NovelAgentIntegration Test ===")
    
    integration = NovelAgentIntegration()
    
    # 测试角色卡片
    characters = [
        {
            "name": "摩根·威廉",
            "role": "Protagonist",
            "avatar": "🦊",
            "description": "蒸气果实能力者·摩根海贼团船长",
            "stats": {"战力": "S", "智力": "S+", "魅力": "A"}
        }
    ]
    
    output_path = integration.render_character_cards(
        characters,
        title="{project_name}",
        subtitle="核心角色档案"
    )
    print(f"Generated: {output_path}")
