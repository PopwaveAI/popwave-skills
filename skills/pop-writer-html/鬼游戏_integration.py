"""
诡异游戏专属集成 - NovelAgentIntegration 子类
为《这诡异游戏也太真实了》项目定制HTML渲染
"""
import os, json
from typing import Dict, List, Optional
from pathlib import Path

# 兼容两种导入方式
try:
    from .integrations import NovelAgentIntegration
except ImportError:
    from integrations import NovelAgentIntegration


class GuiyiGameIntegration(NovelAgentIntegration):
    """
    诡异游戏项目专属集成
    
    自动映射项目文档类型→SKILL模板
    """
    
    # 诡异游戏品牌色 (从07-营销/提取)
    THEME = {
        "bg_deep": "#0a0e1a",
        "bg_card": "#1a1d27",
        "accent": "#d44",
        "accent_dim": "#8a5a5a",
        "text": "#e4e6f0",
        "text_dim": "#8b8fa3",
        "green": "#34d399",
        "blue": "#60a5fa",
    }
    
    # 文档类型→SKILL映射
    DOC_SKILL_MAP = {
        "prd": "article-magazine",
        "constitution": "kami-parchment",
        "settings": "data-report",
        "scene_card": "card-xiaohongshu",
        "chapter": "article-magazine",
        "outline": "deck-guizang-editorial",
        "director": "deck-open-slide-canvas",
        "review": "kami-parchment",
        "dashboard": "dashboard",
        "marketing": "magazine-poster",
        "power_system": "deck-graphify-dark",
        "world_map": "dashboard",
    }
    
    def render_document(self, 
                        doc_type: str,
                        data: Dict,
                        project_path: str = "") -> str:
        """
        自动根据文档类型渲染
        
        Args:
            doc_type: PRD/constitution/settings/scene_card/etc
            data: 文档数据
            project_path: 项目根路径
        
        Returns:
            输出文件路径
        """
        skill = self.DOC_SKILL_MAP.get(doc_type, "article-magazine")
        title = data.get("title", doc_type)
        
        output_dir = os.path.join(project_path, "07-营销") if project_path else self.output_dir
        output_path = os.path.join(output_dir, f"{title}.html")
        
        return self.renderer.render(skill, data, output_path)
    
    def batch_render_scene_cards(self, 
                                  cards_dir: str,
                                  output_dir: str) -> List[str]:
        """
        批量渲染场景卡为HTML
        
        Args:
            cards_dir: 场景卡目录
            output_dir: 输出目录
        
        Returns:
            生成的HTML文件路径列表
        """
        results = []
        import glob
        for card_file in sorted(glob.glob(os.path.join(cards_dir, "场景卡-*.md"))):
            basename = os.path.basename(card_file).replace(".md", "")
            
            with open(card_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析元数据
            scene_type = "未知"
            for line in content.split('\n'):
                if '场景类型' in line:
                    scene_type = line.split('：')[-1].strip() if '：' in line else line.split(':')[-1].strip()
                    break
            
            data = {
                "title": basename,
                "subtitle": scene_type,
                "content": content
            }
            
            output_path = os.path.join(output_dir, f"{basename}.html")
            self.renderer.render("article-magazine", data, output_path)
            results.append(output_path)
            print(f"  [OK] {basename}")
        
        return results
    
    def render_overview_dashboard(self, project_path: str) -> str:
        """
        渲染项目总览看板
        """
        import yaml
        
        # 收集项目统计
        stats = {"title": "诡异游戏-项目总控台"}
        
        # 章节统计
        chapter_dirs = [
            os.path.join(project_path, "04-正文", "v7"),
            os.path.join(project_path, "03-正文", "v8"),
        ]
        total_chapters = 0
        for d in chapter_dirs:
            if os.path.exists(d):
                total_chapters += len([f for f in os.listdir(d) if f.endswith(".md")])
        
        stats["chapters"] = total_chapters
        
        # 场景卡统计
        scene_dir = os.path.join(project_path, "01-写作资产", "场景卡")
        if os.path.exists(scene_dir):
            stats["scene_cards"] = len([f for f in os.listdir(scene_dir) if f.startswith("场景卡") or f.startswith("scene-card")])
        
        # 导演指令统计
        dir_dir = os.path.join(project_path, "01-写作资产", "导演指令")
        if os.path.exists(dir_dir):
            stats["directors"] = len([f for f in os.listdir(dir_dir) if f.endswith(".md")])
        
        # 营销页统计
        mkt_dir = os.path.join(project_path, "07-营销")
        if os.path.exists(mkt_dir):
            stats["marketing_pages"] = len([f for f in os.listdir(mkt_dir) if f.endswith(".html")])
        
        output_path = os.path.join(self.output_dir, "诡异游戏-项目总控台.html")
        return self.renderer.render("dashboard", {
            "title": stats["title"],
            "items": [
                {"name": "已写正文", "value": f"{total_chapters}章"},
                {"name": "场景卡", "value": f"{stats.get('scene_cards', 0)}张"},
                {"name": "导演指令", "value": f"{stats.get('directors', 0)}份"},
                {"name": "营销HTML页", "value": f"{stats.get('marketing_pages', 0)}页"},
            ]
        }, output_path)


if __name__ == "__main__":
    # 测试
    integration = GuiyiGameIntegration(output_dir="e:\\AI小说")
    print("=== GuiyiGameIntegration Test ===")
    print("Theme:", integration.THEME)
    print("Doc-Skill mapping:", len(integration.DOC_SKILL_MAP))
    
    # 测试场景卡批量渲染
    cards_dir = "e:\\AI小说\\这诡异游戏也太真实了\\01-写作资产\\场景卡"
    out_dir = "e:\\AI小说\\这诡异游戏也太真实了\\07-营销"
    if os.path.exists(cards_dir):
        print("\nBatch rendering scene cards...")
        results = integration.batch_render_scene_cards(cards_dir, out_dir)
        print(f"Rendered {len(results)} scene cards")
