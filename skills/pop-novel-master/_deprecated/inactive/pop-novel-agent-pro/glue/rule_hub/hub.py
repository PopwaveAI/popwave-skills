"""
hub.py — 规则中枢引擎（Rule Hub）

职责：
  1. load(project_dir, scene_type=None) → List[Rule]
     加载当前适用的所有 'active' 规则（可选按 scene_type 过滤）
     
  2. inject(rules, stage, prompt_text) → str
     按管线阶段将约束注入到 Prompt 中
     
  3. scan(project_dir, latest_qc_report=None) → ScanReport
     扫描经验日志 → 识别需升级的条目 → 标记通知
     
  4. seed() → int
     从问题池文档初始化规则库（仅首次运行）

调用方式：
  from glue.rule_hub import hub
  rules = hub.load(project_dir)
  annotated = hub.inject(rules, "pass2", prompt_text)
  report = hub.scan(project_dir)

数据存储：
  规则文件：_shared/rule-hub/rules/ 目录下的 *.yaml 文件
  每条规则一个文件，文件名 = rule_id.yaml
"""

import os
import sys
import yaml
import re
import glob
from datetime import date
from pathlib import Path
from typing import List, Dict, Optional, Any

# ─── 路径常量 ────────────────────────────────────

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_GLUE_DIR = os.path.dirname(_SCRIPT_DIR)
_SKILLS_SHARED = os.path.normpath(
    os.path.join(_GLUE_DIR, "..", "skills", "_shared")
)
_RULE_HUB_DIR = os.path.join(_SKILLS_SHARED, "rule-hub")
_RULES_DIR = os.path.join(_RULE_HUB_DIR, "rules")
_SCHEMA_PATH = os.path.join(_RULE_HUB_DIR, "rule-schema.yaml")
_SEED_TARGET = _RULES_DIR

# ─── 数据结构 ────────────────────────────────────


class Rule:
    """单条规则的运行时对象"""
    def __init__(self, data: dict):
        self.rule_id: str = data.get("rule_id", "R-000")
        self.source: str = data.get("source", "manual")
        self.status: str = data.get("status", "active")
        self.severity: str = data.get("severity", "P2")
        self.problem: str = data.get("problem", "")
        self.root_cause: str = data.get("root_cause", "")
        self.enforce: dict = data.get("enforce", {})
        self.lifecycle: dict = data.get("lifecycle", {})
        self.tags: list = data.get("tags", [])


class ScanReport:
    """scan() 的返回结果"""
    def __init__(self):
        self.new_issues: int = 0
        self.elevated_count: int = 0
        self.warnings: List[str] = []
        self.detail: List[dict] = []


# ─── 核心函数 ────────────────────────────────────


def load(project_dir: str = "", scene_type: str = None) -> List[Rule]:
    """
    加载所有 'active' 状态的规则。
    
    参数:
      project_dir: 项目目录（用于加载项目级自定义规则，预留）
      scene_type:  scene_type 过滤（经验日志匹配用），None=不过滤
    
    返回:
      Rule 列表，按 severity 降序排列（P0 在前）
    """
    rules = []

    # 扫描 rules 目录下的所有 yaml 文件
    pattern = os.path.join(_RULES_DIR, "*.yaml")
    for filepath in sorted(glob.glob(pattern)):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"[rule-hub] ⚠️ 规则文件读取失败: {filepath} — {e}")
            continue

        if not data:
            continue

        # 单文件可能包含多条规则（用 rule_id 区分），也可能是一条
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]

        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("status") != "active":
                continue
            rule = Rule(entry)

            # scene_type 过滤
            if scene_type and rule.tags:
                if scene_type not in rule.tags:
                    continue

            rules.append(rule)

    # 按 severity 降序（P0 > P1 > P2 > P3）
    _SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    rules.sort(key=lambda r: _SEVERITY_ORDER.get(r.severity, 99))

    return rules


def inject(rules: List[Rule], stage: str, prompt_text: str) -> str:
    """
    将规则约束注入到指定管线阶段的 Prompt 中。
    
    参数:
      rules:  需要注入的规则列表
      stage:  管线阶段（director / pass1 / pass2 / qc）
      prompt: 原始 Prompt 文本
    
    返回:
      注入约束后的 Prompt 文本
    """
    if not rules:
        return prompt_text

    # --- 注入块 ---
    sections = []

    # Director 阶段：注入 director_constraint
    if stage == "director":
        constraints = [r for r in rules if r.enforce.get("director_constraint")]
        if constraints:
            lines = ["\n## ⚠️ 历史教训约束（自动注入 — 不可违反）\n"]
            for r in constraints:
                text = r.enforce["director_constraint"].get("text", "")
                if text:
                    lines.append(f"- [{r.severity}] {text}")
            lines.append("")
            sections.append("\n".join(lines))

    # Pass 2 渲染阶段：注入 REDLINE 规则摘要 + 约束
    elif stage == "pass2":
        redlines = [r for r in rules if r.enforce.get("redline")]
        if redlines:
            lines = ["\n## ⚠️ 历史教训 · REDLINE 约束（自动注入）\n"]
            for r in redlines:
                patterns = r.enforce["redline"].get("patterns", [])
                if patterns:
                    lines.append(f"- [{r.severity}] {r.problem}")
                    lines.append(f"  禁用语: {' / '.join(patterns[:4])}")
            lines.append("")
            sections.append("\n".join(lines))

        # 也注入 director constraints 到 pass2
        dc_rules = [r for r in rules if r.enforce.get("director_constraint")]
        if dc_rules:
            lines = ["\n## ⚠️ 写作约束（自动注入）\n"]
            for r in dc_rules:
                text = r.enforce["director_constraint"].get("text", "")
                if text:
                    lines.append(f"- [{r.severity}] {text}")
            lines.append("")
            sections.append("\n".join(lines))

    # QC 阶段：注入 QC 检查项
    elif stage == "qc":
        qc_rules = [r for r in rules if r.enforce.get("qc_check")]
        if qc_rules:
            lines = ["\n## ⚠️ 历史教训 QC 检查项（自动注入）\n"]
            for r in qc_rules:
                qc = r.enforce["qc_check"]
                lines.append(f"- {qc.get('id', r.rule_id)}: {qc.get('description', r.problem)}")
                lines.append(f"  方法: {qc.get('method', 'regex')} | 来源: {r.rule_id}")
            lines.append("")
            sections.append("\n".join(lines))

    if not sections:
        return prompt_text

    # 查找 prompt 中合适的插入点
    marker = "## ★ Spec 约束"
    if marker in prompt_text:
        # 插入在 spec 约束之后
        idx = prompt_text.index(marker) + len(marker)
        insert_point = prompt_text.index("\n", idx) + 1
        inject_block = "\n" + "\n".join(sections) + "\n"
        return prompt_text[:insert_point] + inject_block + prompt_text[insert_point:]

    # 没有 spec 约束标记 → 追加到 prompt 末尾
    return prompt_text + "\n" + "\n".join(sections)


def scan(project_dir: str = "") -> ScanReport:
    """
    扫描当前规则库状态，识别需要关注的问题。
    
    检查项：
      1. 有多少条未 verified 的规则
      2. 是否有超过阈值的堆积
      3. 返回扫描报告
    
    返回:
      ScanReport 对象
    """
    report = ScanReport()

    all_rules = load(project_dir)
    active_count = 0
    unverified = 0
    unverified_p0 = 0

    for rule in all_rules:
        if rule.status == "active":
            active_count += 1
            lc = rule.lifecycle or {}
            if not lc.get("verified_at"):
                unverified += 1
                if rule.severity == "P0":
                    unverified_p0 += 1

    # 加载阈值
    thresholds = {"max_unverified_gate": 10}
    try:
        with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = yaml.safe_load(f)
            thresholds.update(schema.get("elevation_thresholds", {}))
    except Exception:
        pass

    report.detail.append({
        "active_rules": active_count,
        "unverified": unverified,
        "unverified_p0": unverified_p0,
    })

    if unverified >= thresholds.get("max_unverified_gate", 10):
        report.warnings.append(
            f"未验证规则已达 {unverified} 条（阈值 {thresholds['max_unverified_gate']}），"
            f"建议审阅后标记 verified。"
        )

    if unverified_p0 > 3:
        report.warnings.append(
            f"有 {unverified_p0} 条 P0 规则未验证，建议优先审阅。"
        )

    return report


def _get_next_rule_id() -> str:
    """自动生成下一个规则编号"""
    existing = []
    pattern = os.path.join(_RULES_DIR, "*.yaml")
    for filepath in glob.glob(pattern):
        basename = os.path.basename(filepath)
        m = re.match(r"^R-(\d{3})", basename)
        if m:
            existing.append(int(m.group(1)))
    if existing:
        next_num = max(existing) + 1
    else:
        next_num = 1
    return f"R-{next_num:03d}"


def add_rule(data: dict) -> str:
    """
    从经验日志或其他来源手动/自动新增一条规则。
    
    参数:
      data: 符合 rule-schema.yaml 的规则字典
    
    返回:
      rule_id
    """
    rule_id = data.get("rule_id") or _get_next_rule_id()
    data["rule_id"] = rule_id

    filepath = os.path.join(_SEED_TARGET, f"{rule_id}.yaml")
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"[rule-hub] ✅ 规则已创建: {rule_id} → {filepath}")
    return rule_id


# ─── 初次初始化：从问题池文档种子规则库 ─────────────


def seed() -> int:
    """
    从预定义的初始规则种子创建规则文件。
    只在 rules/ 目录为空时执行。
    
    返回:
      创建的规则数量
    """
    target_dir = _SEED_TARGET
    os.makedirs(target_dir, exist_ok=True)

    # 初始规则种子（从问题池与根因库 + 遗漏问题清单 + 对话暴露问题提炼）
    seed_rules = _get_seed_rules()

    count = 0
    for data in seed_rules:
        data["rule_id"] = _get_next_rule_id() if not data.get("rule_id") else data["rule_id"]
        filepath = os.path.join(target_dir, f"{data['rule_id']}.yaml")
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        count += 1

    print(f"[rule-hub] ✅ 初始规则库已创建: {count} 条规则 → {target_dir}")
    return count


def _get_seed_rules() -> List[dict]:
    """返回初始规则种子列表"""
    today = "2026-06-02"
    return [
        # ════════════════════════════════════════════════════════════
        # P0 规则（来自问题池+遗漏清单+对话暴露）
        # ════════════════════════════════════════════════════════════
        {
            "rule_id": "R-001",
            "source": "qa-review",
            "status": "active",
            "severity": "P0",
            "problem": "章末以'旁白总结'收束，非事件断裂",
            "root_cause": "QC 层未检查章末钩子类型；跨项目共同问题",
            "enforce": {
                "redline": {
                    "patterns": ["本章说明了|本章揭示了|这就是为什么|就这样"],
                    "target": "chapter_end"
                },
                "qc_check": {
                    "id": "QC-R001",
                    "description": "章末钩子必须为事件断裂/悬念收束/代价提示之一，不允许纯旁白总结",
                    "method": "llm_judgment"
                },
                "director_constraint": {
                    "text": "本章结尾必须在事件断裂或悬念上，不要用'旁白总结'收束。连续 2 章以总结收尾=读者流失风险。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 3},
            "tags": ["过渡推进", "章末钩子", "正文写作"]
        },
        {
            "rule_id": "R-002",
            "source": "retrospective",
            "status": "active",
            "severity": "P0",
            "problem": "否定式描写多发：'不是A而是B'及变体未完全覆盖",
            "root_cause": "REDLINE 规则只覆盖了'不是A而是B'，未覆盖变体",
            "enforce": {
                "redline": {
                    "patterns": [
                        "不是[^，。\\n]{1,30}而是",
                        "不是[^，。\\n]+不是[^，。\\n]+是[一|种|某种]",
                        "说不清[楚的]{0,2}(?:的)?\\s*(?:颜色|感觉|味道|声音|情绪|恐惧)",
                        "是(?:某种|一种)\\s*说不清",
                        "直觉告诉",
                        "他没有问|她没有问"
                    ],
                    "target": "full_text"
                },
                "qc_check": {
                    "id": "QC-R002",
                    "description": "否定式描写检测：'不是A而是B'/'说不清'/'直觉告诉'/'他没有问'",
                    "method": "regex"
                },
                "director_constraint": {
                    "text": "禁止使用否定式描写结构：'不是A而是B'、'说不清的颜色/感觉'、'直觉告诉'、'他没有/她没有问'。直接用肯定句呈现。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 5},
            "tags": ["正文写作", "否定句式"]
        },
        {
            "rule_id": "R-003",
            "source": "retrospective",
            "status": "active",
            "severity": "P0",
            "problem": "连续 2+ 章零爽点 / 填充章，导致读者流失",
            "root_cause": "act-01.yaml 缺少爽点等级字段；骨架无'信息量不足'截断判断",
            "enforce": {
                "redline": {
                    "patterns": [],
                    "target": "full_text"
                },
                "qc_check": {
                    "id": "QC-R003",
                    "description": "爽点密度检查：本章是否至少有一个微爽点落地？连续 2 章零爽点→标记",
                    "method": "llm_judgment"
                },
                "director_constraint": {
                    "text": "每章至少包含 1 个微爽点落地。连续零爽点章数 ≥ 2 = 读者弃书风险。如果本章信息量不足以撑满一章，压缩场景而非注水。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 4},
            "tags": ["过渡推进", "爽点释放", "节奏控制"]
        },
        {
            "rule_id": "R-004",
            "source": "retrospective",
            "status": "active",
            "severity": "P0",
            "problem": "战斗场景无锚定章参考，画面感全靠 LLM 默认语感",
            "root_cause": "Pass 2 的输入包中缺少锚定章片段注入环节",
            "enforce": {
                "director_constraint": {
                    "text": "本章包含战斗/对抗场景时，必须从锚定章库选取至少 1 个同类型战斗片段作为参考。如果锚定章库无匹配战斗片段，标注缺失并在场景设计中补充视觉细节要求。",
                    "trigger_scene_types": ["战斗对抗"]
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 3},
            "tags": ["战斗对抗", "战斗描写", "正文写作"]
        },
        {
            "rule_id": "R-005",
            "source": "qa-review",
            "status": "active",
            "severity": "P0",
            "problem": "主角/角色缺少性格辨识度，无法通过台词区分",
            "root_cause": "开书阶段 L0 角色人设契约太薄——只有关键词，没有行为锚定",
            "enforce": {
                "director_constraint": {
                    "text": "本章涉及的核心角色必须有可区分的说话方式/行为模式。每个角色在压力下的反应不能趋同。如果某角色只有出场没有性格表现，标注「该角色缺乏行为锚定」。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 2},
            "tags": ["对话博弈", "角色人设", "开书设定"]
        },
        {
            "rule_id": "R-006",
            "source": "user-feedback",
            "status": "active",
            "severity": "P0",
            "problem": "HTML 展示站发布前未明确需求规格，反复返工",
            "root_cause": "缺少前置 spec 需求规范——Agent 靠猜用户需求",
            "enforce": {
                "director_constraint": {
                    "text": "在创建/修改任何用户可见的 HTML 输出前，必须先输出一个简短的需求确认清单（目标用户/核心功能/外部依赖/单文件或多页面/视觉参考），用户确认后再动手。"
                }
            },
            "lifecycle": {"discovered_at": "2026-06-02", "elevated_at": today, "occurrences": 2},
            "tags": ["发布/HTML"]
        },
        {
            "rule_id": "R-007",
            "source": "retrospective",
            "status": "active",
            "severity": "P0",
            "problem": "信息密度失衡——前期过密（单章 13 概念）、中期过稀（纯填充章）",
            "root_cause": "无章级信息量配额；骨架未做'信息量是否够撑一章'的截断判断",
            "enforce": {
                "qc_check": {
                    "id": "QC-R004",
                    "description": "信息密度检查：本章引入的新概念/实体数。过渡章 ≤ 2 个，核心章 ≤ 4 个",
                    "method": "entity_count"
                },
                "director_constraint": {
                    "text": "每章引入的新概念/实体数：过渡章 ≤ 2 个，核心章 ≤ 4 个。如果当前场景的信息量不够撑满一章，压缩到单场景而非拉成多场景。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 3},
            "tags": ["正文写作", "信息密度"]
        },
        {
            "rule_id": "R-008",
            "source": "retrospective",
            "status": "active",
            "severity": "P0",
            "problem": "对话占比长期偏低（<25%），旁白叙事占比过高",
            "root_cause": "无对话比例强制约束；对话型场景卡存量不足",
            "enforce": {
                "qc_check": {
                    "id": "QC-R005",
                    "description": "对话占比检查：对话字符 ≥ 全文字数的 25%。连续 3 章 < 25% 触发告警",
                    "method": "dialogue_ratio"
                },
                "director_constraint": {
                    "text": "本章对话占比需 ≥ 25%。如果一个场景超过 500 字没有一句直接对话（含角色内心独白），需要考虑插入对话或角色互动来打破叙事密度。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 4},
            "tags": ["正文写作", "对话占比", "对话博弈"]
        },

        # ════════════════════════════════════════════════════════════
        # P1 规则
        # ════════════════════════════════════════════════════════════
        {
            "rule_id": "R-009",
            "source": "retrospective",
            "status": "active",
            "severity": "P1",
            "problem": "抽象描写代替具象画面——绕圈内心描写无信息量",
            "root_cause": "Pass 2 渲染时抽象与具象判断倾向未被约束",
            "enforce": {
                "redline": {
                    "patterns": ["不是语言不是画面|某种频率|说不清道不明"],
                    "target": "full_text"
                },
                "director_constraint": {
                    "text": "避免用抽象描述（'一种说不清的感觉'/'某种频率'）代替感官呈现。用动作、对话、环境细节来传递氛围。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 3},
            "tags": ["正文写作", "战斗描写"]
        },
        {
            "rule_id": "R-010",
            "source": "retrospective",
            "status": "active",
            "severity": "P1",
            "problem": "'天黑=危险要来'公式化触发，场景时间设定单一",
            "root_cause": "幕纲设计时场景时间连续 ≥ 3 章使用同一模式",
            "enforce": {
                "director_constraint": {
                    "text": "本章场景时间需与前一章差异化。连续 ≤ 3 章使用同一时间模式（如全部天黑触发）。过半数事件在夜间→调整部分事件发生时间。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 2},
            "tags": ["幕纲设计", "节奏控制"]
        },
        {
            "rule_id": "R-011",
            "source": "user-feedback",
            "status": "active",
            "severity": "P1",
            "problem": "WebSearch 不可用时直接跳过管线环节，无降级策略",
            "root_cause": "skill 没有为外部工具不可用设计降级路径",
            "enforce": {
                "director_constraint": {
                    "text": "当 WebSearch/WebFetch 不可用时：用本地知识库/已有设定文件替代搜索。在项目沉淀中标记为'搜索跳过'并注明替代来源。不要直接跳过管线环节。"
                }
            },
            "lifecycle": {"discovered_at": "2026-06-02", "elevated_at": today, "occurrences": 1},
            "tags": ["开书设定", "正文写作"]
        },
        {
            "rule_id": "R-012",
            "source": "qa-review",
            "status": "active",
            "severity": "P1",
            "problem": "同一代价类型/钩子类型重复使用（如纸人被撕碎多次）",
            "root_cause": "无跨章代价类型差异化检查；骨架无去重机制",
            "enforce": {
                "director_constraint": {
                    "text": "本章的代价/钩子类型与最近 3 章对比，避免重复使用同一种呈现方式（如连续多次'低头看印→纹路变多'）。如果重复 → 换一种呈现方式或调整场景编排。"
                }
            },
            "lifecycle": {"discovered_at": "2026-05-25", "elevated_at": today, "occurrences": 2},
            "tags": ["正文写作", "爽点释放"]
        },
    ]


# ─── CLI 入口 ────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rule Hub — 规则中枢引擎")
    parser.add_argument("action", choices=["load", "inject", "scan", "seed", "add"],
                        help="操作类型")
    parser.add_argument("--project", "-p", default="", help="项目路径")
    parser.add_argument("--stage", choices=["director", "pass1", "pass2", "qc", "esm_before"],
                        help="注入目标阶段(inject模式)")
    parser.add_argument("--prompt", help="Prompt 文件路径(inject模式)")
    parser.add_argument("--scene-type", help="场景类型过滤(load模式)")
    parser.add_argument("--rule-data", help="规则数据 JSON 文件路径(add模式)")

    args = parser.parse_args()

    if args.action == "seed":
        count = seed()
        print(f"✅ 已创建 {count} 条初始规则")

    elif args.action == "load":
        rules = load(args.project, args.scene_type)
        print(f"\n📋 规则中枢 — 当前 active 规则: {len(rules)} 条\n")
        for r in rules:
            lc = r.lifecycle or {}
            verified = lc.get("verified_at", "未验证")
            print(f"  {r.rule_id} [{r.severity}] {r.problem}")
            print(f"    状态: {r.status} | 来源: {r.source} | 验证: {verified}")
            print()

    elif args.action == "inject":
        if not args.stage or not args.prompt:
            print("❌ inject 需要 --stage 和 --prompt")
            sys.exit(1)
        rules = load(args.project)
        with open(args.prompt, "r", encoding="utf-8") as f:
            prompt_text = f.read()
        result = inject(rules, args.stage, prompt_text)
        print(result)

    elif args.action == "scan":
        report = scan(args.project)
        print(f"\n📋 规则扫描报告")
        print(f"  Active 规则: {report.detail[0]['active_rules'] if report.detail else 0}")
        print(f"  未验证: {report.detail[0]['unverified'] if report.detail else 0}")
        print(f"  未验证 P0: {report.detail[0]['unverified_p0'] if report.detail else 0}")
        if report.warnings:
            print(f"  ⚠️ 警告:")
            for w in report.warnings:
                print(f"    - {w}")

    elif args.action == "add":
        if not args.rule_data:
            print("❌ add 需要 --rule-data (JSON 文件路径)")
            sys.exit(1)
        with open(args.rule_data, "r", encoding="utf-8") as f:
            data = json.load(f) if args.rule_data.endswith(".json") else yaml.safe_load(f)
        rid = add_rule(data)
        print(f"✅ 规则已创建: {rid}")
