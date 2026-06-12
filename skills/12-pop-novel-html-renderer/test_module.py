"""测试 html-renderer 模块"""
import sys
import os

# 添加到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skill_registry import SkillRegistry, SkillCategory
from renderer import HTMLRenderer
from integrations import NovelAgentIntegration

print("=== HTML Renderer Module Test ===\n")

# 1. 测试 Skill Registry
print("1. Skill Registry Test")
registry = SkillRegistry()
print(f"   Total skills: {len(registry.list_all())}")
print(f"   Top 3 recommended:")
for skill in registry.get_recommended(3):
    print(f"      {skill.emoji} {skill.zh_name} (rank: {skill.recommended})")

# 2. 测试 Swiss International Prompt
print("\n2. Swiss International Prompt Test")
skill = registry.get("swiss-international")
if skill:
    prompt = skill.to_prompt()
    print(f"   Prompt length: {len(prompt)} chars")
    print(f"   First 200 chars:\n   {prompt[:200]}...")

# 3. 测试 HTML Renderer
print("\n3. HTML Renderer Test")
renderer = HTMLRenderer()
test_data = {
    "title": "{project_name}",
    "subtitle": "核心角色档案",
    "characters": [
        {
            "name": "摩根·威廉",
            "role": "Protagonist",
            "avatar": "🦊",
            "description": "蒸气果实能力者·摩根海贼团船长",
            "stats": {"战力": "S", "智力": "S+", "魅力": "A"}
        }
    ]
}

html = renderer.render("swiss-international", test_data)
print(f"   Generated HTML: {len(html)} chars")

# 4. 测试集成
print("\n4. NovelAgentIntegration Test")
integration = NovelAgentIntegration(output_dir="e:\\AI小说")
output_path = integration.render_character_cards(
    test_data["characters"],
    title="海贼法典",
    subtitle="测试输出"
)
print(f"   Output saved to: {output_path}")

print("\n=== All Tests Passed ===")
