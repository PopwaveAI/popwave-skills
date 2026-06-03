"""
节点F — pop agent 前置渲染决策模块（HTML化发布思考节点）

属于 pop 思考节点系列：节点A(金手指) / 节点B(幕设计) / 节点C(黄金三章) 
                               / 节点D(市场验证) / 节点E(拆书) / 节点F(HTML发布)
                              
节点F的职责：接到HTML化需求后，先决策再渲染，不是事后检查。
三步决策：①受众是谁 ②要达到什么效果 ③这份文档的特化方向

使用流程:
    # pop agent 收到"做成HTML"需求后
    from html_renderer import NodeF
    
    intent = NodeF.decide(
        doc_type="scene_card",
        doc_name="场景卡-001-纸身",
        audience="readers",
        goal="horror_immersion",
        specialization="游戏UI切入→恐怖排版收尾"
    )
    # intent.resolved_skill → 选定的SKILL
    # intent.customizations → 定制点
    # → 基于这些信息渲染
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json


class Audience(Enum):
    """文档HTML化的受众"""
    READERS = "readers"           # 读者/粉丝 - 群内传播、朋友圈
    PARTNERS = "partners"         # 合作者/投资人 - 展示
    SELF = "self"                 # 自己 - 写作复盘
    AGENTS = "agents"             # AI agent - 上下文注入


class EmotionalGoal(Enum):
    """目标读者感受"""
    WORLD_BUILDING = "world_building"     # "这世界观是认真的"
    HORROR_IMMERSION = "horror_immersion" # "头皮发麻"
    SYSTEM_DEPTH = "system_depth"         # "这体系真有深度"
    PROFESSIONAL = "professional"         # "这团队靠谱"
    WANT_TO_PLAY = "want_to_play"         # "想玩"
    TRUST = "trust"                       # "可信赖"
    LAUGHTER = "laughter"                 # "笑出声"
    SUSPENSE = "suspense"                 # "等等…不对劲"


@dataclass
class RenderIntent:
    """
    渲染意图 — pop agent 接到 HTML 化需求后的决策输出
    
    这个不是在渲染之后的检查，而是渲染之前 pop 的第一反应
    """
    
    # === 文档标识 ===
    doc_type: str                    # scene_card / constitution / settings / chapter / prd / ...
    doc_name: str                    # "场景卡-001-纸身"
    
    # === 三层思考输出 ===
    audience: Audience               # 给谁看
    emotional_goal: EmotionalGoal    # 要什么感受
    specialization: str              # 特化方向（一句话锚点）
    
    # === 决策产出 ===
    resolved_skill: str = ""         # 选定的 SKILL
    customizations: List[str] = field(default_factory=list)  # 定制点
    design_notes: str = ""           # 设计备注
    
    def describe(self) -> str:
        """输出可读的渲染意图"""
        lines = [
            f"🎯 【渲染意图】{self.doc_name}",
            f"   受众：{self.audience.value}",
            f"   效果目标：{self.emotional_goal.value}",
            f"   特化方向：{self.specialization}",
            f"   选定SKILL：{self.resolved_skill}",
        ]
        if self.customizations:
            lines.append("   定制点：")
            for c in self.customizations:
                lines.append(f"     - {c}")
        if self.design_notes:
            lines.append(f"   设计备注：{self.design_notes}")
        return "\n".join(lines)
    
    def to_markdown_comment(self) -> str:
        """输出作为 HTML 注释嵌入"""
        return f"<!-- RENDER INTENT: {self.doc_name} | audience={self.audience.value} | goal={self.emotional_goal.value} | skill={self.resolved_skill} -->"


class NodeF:
    """
    节点F — HTML化发布前置决策器
    
    pop 思考节点系列之一。
    每次收到"把这个文档HTML化"的需求，先用这个模块跑一遍。
    三层思考：受众 → 效果 → 特化方向
    """
    
    # SKILL 选型规则库
    SKILL_RULES = {
        # (doc_type, audience, goal) → (skill, customizations)
        
        # === 宪法/铁律 ===
        ("constitution", "partners", "professional"):
            ("deck-swiss-international", [
                "全屏 Klein Blue hero 封面",
                "编号规则用16列网格展示",
                "底部元数据条（版本/创建时间）",
            ]),
        ("constitution", "readers", "world_building"):
            ("deck-guizang-editorial", [
                "墨水印刷感，不用科技风",
                "章节切换用反色（ink ↔ paper）",
                "folio 页码在右下角",
            ]),
        
        # === 场景卡 ===
        ("scene_card", "readers", "horror_immersion"):
            ("custom:scene-card", [
                "以「游戏内日志UI」切入",
                "前半段保留系统感（等宽字体、信息栏）",
                "恐怖段落降低字重、增大留白",
                "文字节奏随恐怖程度收紧",
                "结尾不留游戏UI痕迹",
            ]),
        ("scene_card", "self", "system_depth"):
            ("kami-parchment", [
                "暖纸底 #f5f4ed，保留附注",
                "核心卖点用 tag 展示",
                "文风参考用引用框",
            ]),
        
        # === L1设定 ===
        ("settings", "readers", "system_depth"):
            ("kami-parchment", [
                "书卷封面页（标题+副标题+版本号）",
                "层级展开：概念→三态→境界→颜色→禁忌",
                "色板用实体色块展示",
                "境界用序列列表，不用卡片",
            ]),
        ("settings", "partners", "professional"):
            ("data-report", [
                "KPI指标卡展示关键数据",
                "境界体系用图表可视化",
            ]),
        
        # === PRD ===
        ("prd", "partners", "trust"):
            ("article-magazine", [
                "顶部 hero: 大标题 + 作者/日期元数据",
                "正文单栏 700px 最大宽度",
                "H2/H3 用 serif 字体制造对比",
                "表格用 zebra stripe 样式",
            ]),
        ("prd", "agents", "professional"):
            ("deck-swiss-international", [
                "全用结构化卡片，不要叙事段落",
                "16列网格约束",
                "数据必须从真实输入解析",
            ]),
        
        # === 章节正文 ===
        ("chapter", "readers", "horror_immersion"):
            ("custom:chapter-horror", [
                "暗底 #0a0e1a + 衬线字体",
                "无侧栏/无导航/无分心元素",
                "章节号用大号罗马数字或中文数字",
                "恐怖段落：短句/大留白/灰色渐变",
                "阅读进度条在顶部细线",
            ]),
        
        # === 复盘报告 ===
        ("review", "self", "system_depth"):
            ("kami-parchment", [
                "极简排版，去掉装饰元素",
                "信息密度优先",
                "重点用墨蓝 #1B365D 标记",
            ]),
        
        # === 力量体系 ===
        ("power_system", "readers", "system_depth"):
            ("deck-graphify-dark", [
                "暗底 + 图谱节点 + 编号路径",
                "境界用层级树展示",
                "连接线标注关系",
            ]),
        
        # === 营销/登录页 ===
        ("marketing", "readers", "want_to_play"):
            ("deck-hermes-cyber", [
                "黑底 #0a0c10 + CRT 网格",
                "薄荷绿大字 + JetBrains Mono",
                "闪烁光标 + CLI 感",
                "彩蛋交互",
            ]),
    }
    
    def decide(self,
               doc_type: str,
               doc_name: str,
               audience: str,
               goal: str,
               specialization: str = "") -> RenderIntent:
        """
        pop agent 的决策入口
        
        Args:
            doc_type: 文档类型 (constitution/scene_card/settings/...)
            doc_name: 文档名
            audience: 受众 (readers/partners/self/agents)
            goal: 效果目标 (world_building/horror_immersion/...)
            specialization: 特化方向描述
            
        Returns:
            RenderIntent 决策结果
        """
        intent = RenderIntent(
            doc_type=doc_type,
            doc_name=doc_name,
            audience=Audience(audience),
            emotional_goal=EmotionalGoal(goal),
            specialization=specialization,
        )
        
        # 查规则表
        key = (doc_type, audience, goal)
        match = self.SKILL_RULES.get(key)
        
        if match:
            intent.resolved_skill, intent.customizations = match
        else:
            # 模糊匹配：按优先级降序尝试
            for (dt, aud, gl), (skill, customs) in sorted(
                self.SKILL_RULES.items(),
                key=lambda x: {
                    "constitution": 1, "scene_card": 2, "settings": 3,
                    "prd": 4, "chapter": 5, "review": 6,
                    "power_system": 7, "marketing": 8
                }.get(x[0][0], 99)
            ):
                if dt == doc_type:
                    intent.resolved_skill = skill
                    intent.customizations = customs
                    intent.design_notes = f"模糊匹配: 目标({audience},{goal}) → 使用({aud},{gl})"
                    break
            else:
                # 兜底
                intent.resolved_skill = "article-magazine"
                intent.customizations = ["通用叙事排版"]
                intent.design_notes = "兜底选择: 无精确匹配规则"
        
        return intent
    
    def export_rules(self) -> str:
        """导出规则表为可读格式"""
        lines = ["# Pre-Render Decision Rules", ""]
        for (dt, aud, gl), (skill, customs) in sorted(self.SKILL_RULES.items()):
            lines.append(f"## {dt} + {aud} + {gl}")
            lines.append(f"- SKILL: {skill}")
            for c in customs:
                lines.append(f"  - {c}")
            lines.append("")
        return "\n".join(lines)


# ============================================
# pop agent 使用示例
# ============================================

if __name__ == "__main__":
    decider = NodeF()
    
    print("=" * 60)
    print("节点F · HTML化发布决策 测试")
    print("=" * 60)
    
    cases = [
        ("constitution", "宪法.yaml", "partners", "professional", "冷静展示20条铁律，让投资人觉得这项目靠谱"),
        ("scene_card", "场景卡-001-纸身.md", "readers", "horror_immersion", "游戏UI切入→恐怖排版收尾的文字陷阱"),
        ("settings", "L1设定-意.yaml", "readers", "system_depth", "从本质到禁忌的递进展开"),
        ("chapter", "ch001.md", "readers", "horror_immersion", "沉浸式阅读无干扰"),
        ("review", "复盘报告.md", "self", "system_depth", "信息密度优先"),
    ]
    
    for doc_type, doc_name, audience, goal, spec in cases:
        print(f"\n📄 {doc_name}")
        intent = decider.decide(doc_type, doc_name, audience, goal, spec)
        print(intent.describe())
    
    print("\n" + "=" * 60)
    print("规则表：", len(decider.SKILL_RULES), "条")
    print("=" * 60)
