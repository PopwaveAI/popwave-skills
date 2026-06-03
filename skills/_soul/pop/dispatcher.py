"""
pop/dispatcher.py — Harness 编排控制器

职责：pop 从"说一句话"升级为"做一套编排"
接收用户需求 → 查路由 → 解析 frontmatter → 装配依赖 → 触发 glue → 分发

使用方式（pop agent 入口）：
    from pop.dispatcher import Harness

    harness = Harness(project_dir="...")
    job = harness.route(
        user_intent="写第8章正文",
        project_dir="PROJECT_DIR"
    )
    # job.skill → 路由到的 skill
    # job.preflight → 前置检查结果
    # job.context → 装配好的上下文
    # job.prompt → 子Agent prompt
"""

import os
import sys
import re
import json
import yaml
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


# ============================================
# 路由表（与 POP-ROUTER.md 同步维护）
# ============================================

ROUTING_TABLE = [
    # (keywords, category, skill_name, display_name)
    # ★ Spec 桥接 — 排在首位，优先级最高
    (["规格", "spec", "审批", "生成规格", "先规格"], "spec", "spec-bridge", "Spec 桥接"),
    # 原有路由
    (["开书", "启动", "设计设定", "开新书"], "bootstrap", "skill-project-bootstrap", "开书启动"),
    (["幕纲", "大纲", "剧情", "幕设计"], "plot", "skill-plot-architecture", "剧情架构"),
    (["前三章", "开篇", "黄金三章"], "opening", "skill-opening-arc", "黄金三章"),
    (["写作", "正文", "第", "ch0"], "writing", "skill-emergent-writer", "正文写作"),
    (["拆书", "解构", "分析", "对标"], "deconstruct", "skill-book-deconstructor", "拆书解构"),
    (["审稿", "QA", "质检", "审一下"], "qa", "skill-qa-payoff", "爽点QA"),
    (["市场", "验证", "审市场"], "market", "skill-market-test", "市场验证"),
    (["续写", "交接", "已有正文"], "continuation", "_continuation", "续写适配"),
    (["HTML化", "发布", "渲染", "做成HTML"], "publish", "html-renderer", "HTML化发布引擎"),
    (["调研", "搜索", "研究"], "research", "cnovel-research", "网文调研"),
    (["舆情", "查一下", "书评", "口碑"], "research", "book-opinion-tracker", "网文舆情追踪"),
]


@dataclass
class SkillManifest:
    """解析后的 SKILL 清单（来自 frontmatter）"""
    name: str
    display_name: str
    category: str
    scenario: str
    mode: str
    tags: List[str]
    description: str
    version: str
    recommended: int = 99
    
    # 编排字段（新增）
    preflight: List[str] = field(default_factory=list)
    postflight: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    inject_context: List[str] = field(default_factory=list)
    subagent_required: bool = True


@dataclass
class JobOrder:
    """编排任务单 — Harness 的输出"""
    skill_name: str                     # 路由到的 skill
    display_name: str                   # 显示名
    category: str                       # 场景分类
    version: str                        # skill 版本
    project_dir: str                    # 项目路径
    manifest: SkillManifest             # 解析后的 frontmatter
    preflight_results: Dict[str, bool]  # 前置检查结果
    context: Dict[str, str]             # 装配好的上下文
    prompt: str = ""                    # 子Agent prompt
    errors: List[str] = field(default_factory=list)
    
    @property
    def pass_gate(self) -> bool:
        """是否通过所有前置检查"""
        return len(self.errors) == 0 and all(self.preflight_results.values())


class Harness:
    """
    pop 编排控制器
    
    使用流程：
        1. harness = Harness(project_dir)
        2. job = harness.route(user_intent)
        3. if job.pass_gate:  # 分发
        4. else:  # 返回缺失报告
    """
    
    def __init__(self, project_dir: str = ""):
        self.project_dir = project_dir
        self.skills_dir = self._find_skills_dir()
    
    def _find_skills_dir(self) -> str:
        """定位 skills/ 根目录（确保从任意位置都能找到）"""
        # 从 dispatcher.py 所在位置推算：_shared/pop/dispatcher.py → skills/
        own_dir = os.path.dirname(os.path.abspath(__file__))  # _shared/pop/
        shared_dir = os.path.dirname(own_dir)                  # _shared/
        skills_dir = os.path.dirname(shared_dir)               # skills/
        if os.path.isdir(skills_dir):
            return skills_dir
        return ""
    
    # ============================================
    # ① 路由匹配
    # ============================================
    
    def route(self, user_intent: str, project_dir: str = "", dry_run: bool = False) -> JobOrder:
        """
        入口：接收用户需求 → 返回编排任务单
        
        Args:
            user_intent: 用户原始的输入文本
            project_dir: 项目根路径
            dry_run: 仅路由不执行 glue
            
        Returns:
            JobOrder 任务单
        """
        if project_dir:
            self.project_dir = project_dir
            self.skills_dir = self._find_skills_dir()
        
        # Step 1: 意图匹配
        skill_name, display_name, category = self._match_intent(user_intent)
        
        # Step 2: 解析 SKILL.md frontmatter
        manifest = self._parse_manifest(skill_name)
        
        # Step 3: 前置检查
        preflight_results = {}
        errors = []
        if not dry_run:
            preflight_results, errors = self._run_preflight(manifest, project_dir)
        
        # Step 4: 装配上下文
        context = {}
        if not dry_run and manifest.inject_context:
            context = self._assemble_context(manifest.inject_context, project_dir)
        
        job = JobOrder(
            skill_name=skill_name,
            display_name=display_name,
            category=category,
            version=manifest.version,
            project_dir=project_dir,
            manifest=manifest,
            preflight_results=preflight_results,
            context=context,
            errors=errors,
        )
        
        # Step 5: 生成子Agent prompt
        job.prompt = self._build_prompt(job)
        
        return job
    
    def _match_intent(self, intent: str) -> Tuple[str, str, str]:
        """
        意图匹配逻辑（对应 POP-ROUTER.md 关键词表）
        优先级：精确匹配 > 关键词部分匹配 > 兜底
        """
        intent_lower = intent.lower()
        
        # 按关键词列表命中率排序
        best_match = None
        best_score = 0
        
        for keywords, category, skill_name, display_name in ROUTING_TABLE:
            score = 0
            for kw in keywords:
                if kw.lower() in intent_lower:
                    score += 1
            if score > best_score:
                best_score = score
                best_match = (skill_name, display_name, category)
        
        if best_match and best_score > 0:
            return best_match
        
        # 兜底
        return ("skill-emergent-writer", "正文写作", "writing")
    
    # ============================================
    # ② Frontmatter 解析
    # ============================================
    
    def _find_skill_md(self, skill_name: str) -> str:
        """定位 SKILL.md 文件路径"""
        # 先尝试常规路径：skills/{name}/SKILL.md
        skill_dir = os.path.join(self.skills_dir, skill_name)
        md_path = os.path.join(skill_dir, "SKILL.md")
        if os.path.isfile(md_path):
            return md_path
        
        # 再尝试 _shared/ 下：skills/_shared/{name}/SKILL.md
        shared_path = os.path.join(self.skills_dir, "_shared", skill_name, "SKILL.md")
        if os.path.isfile(shared_path):
            return shared_path
        
        # 最后搜索整个 skills/ 目录
        for root, dirs, files in os.walk(self.skills_dir):
            for f in files:
                if f == "SKILL.md" and skill_name in root:
                    return os.path.join(root, f)
        
        return ""
    
    def _parse_manifest(self, skill_name: str) -> SkillManifest:
        """解析 SKILL.md 的 frontmatter + 编排字段"""
        md_path = self._find_skill_md(skill_name)
        
        manifest = SkillManifest(
            name=skill_name,
            display_name=skill_name,
            category="unknown",
            scenario="unknown",
            mode="unknown",
            tags=[],
            description="",
            version="0.0",
            recommended=99,
        )
        
        if not md_path or not os.path.isfile(md_path):
            return manifest
        
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取 YAML frontmatter（跳过开头的 HTML 注释）
        fm_match = re.search(r'---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            return manifest
        
        fm_text = fm_match.group(1)
        
        # 提取编排字段（新字段）
        self._extract_field(fm_text, "name", manifest, "name")
        self._extract_field(fm_text, "display_name", manifest, "display_name")
        self._extract_field(fm_text, "category", manifest, "category")
        self._extract_field(fm_text, "scenario", manifest, "scenario")
        self._extract_field(fm_text, "mode", manifest, "mode")
        self._extract_field(fm_text, "description", manifest, "description")
        self._extract_field(fm_text, "version", manifest, "version")
        
        # recommended 数字
        rec_match = re.search(r'^recommended:\s*(\d+)', fm_text, re.MULTILINE)
        if rec_match:
            manifest.recommended = int(rec_match.group(1))
        
        # tags（特殊处理数组）
        tags_match = re.search(r'tags:\s*\[([^\]]*)\]', fm_text)
        if tags_match:
            manifest.tags = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]
        
        # 编排字段 — preflight
        preflight_match = re.search(r'preflight:\s*\[([^\]]*)\]', fm_text)
        if preflight_match:
            manifest.preflight = [p.strip().strip('"\'') for p in preflight_match.group(1).split(',')]
        
        # dependencies
        deps_match = re.search(r'dependencies:\s*\[([^\]]*)\]', fm_text)
        if deps_match:
            manifest.dependencies = [d.strip().strip('"\'') for d in deps_match.group(1).split(',')]
        
        # inject_context
        ctx_match = re.search(r'inject_context:\s*\[([^\]]*)\]', fm_text)
        if ctx_match:
            manifest.inject_context = [c.strip().strip('"\'') for c in ctx_match.group(1).split(',')]
        
        # subagent_required
        sa_match = re.search(r'subagent_required:\s*(true|false)', fm_text)
        if sa_match:
            manifest.subagent_required = sa_match.group(1) == 'true'
        
        return manifest
    
    def _extract_field(self, text: str, key: str, manifest: SkillManifest, attr: str):
        """从 YAML 文本提取字段"""
        pattern = rf'^{key}:\s*(.+?)$'
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            val = match.group(1).strip()
            # 去掉引号和尾随注释
            val = val.strip('"').strip("'")
            val = re.sub(r'\s*#.*$', '', val).strip()
            setattr(manifest, attr, val)
    
    # ============================================
    # ③ 前置检查
    # ============================================
    
    def _run_preflight(self, manifest: SkillManifest, project_dir: str) -> Tuple[Dict[str, bool], List[str]]:
        """运行前置检查（文件存在性 + HARD-GATE 语义级检查）"""
        results = {}
        errors = []
        
        # 检查项目目录
        if project_dir:
            results["project_dir"] = os.path.isdir(project_dir)
            if not results["project_dir"]:
                errors.append(f"项目目录不存在: {project_dir}")
        
        # 检查 project.yaml
        if project_dir:
            proj_yaml = os.path.join(project_dir, "project.yaml")
            results["project.yaml"] = os.path.isfile(proj_yaml)
            if not results["project.yaml"]:
                errors.append(f"缺少 project.yaml: {proj_yaml}")
        
        # 检查依赖文件
        for dep in manifest.dependencies:
            if project_dir:
                dep_path = os.path.join(project_dir, dep)
                results[dep] = os.path.exists(dep_path)
                if not results[dep]:
                    errors.append(f"依赖缺失: {dep}")
        
        # 没有项目目录时跳过文件检查
        if not project_dir:
            return {}, []
        
        # ─── HARD-GATE 语义级检查 ────────────────────────────────
        
        skill_name = manifest.name
        
        # 加载 project.yaml（供后续语义检查使用）
        config = None
        proj_yaml = os.path.join(project_dir, "project.yaml")
        if os.path.isfile(proj_yaml):
            try:
                with open(proj_yaml, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            except Exception:
                pass
        
        # 1. reader_profile 检查：需要 reader_profile 字段的 skill
        reader_skills = ["plot-architecture", "opening-arc", "market-test", "emergent-writer"]
        if any(s in skill_name for s in reader_skills):
            if config:
                project = config.get("project", {})
                rp = project.get("reader_profile", {})
                if not rp:
                    errors.append(
                        "HARD-GATE: project.yaml 缺少 reader_profile 字段。 "
                        "请先执行 开书启动(bootstrap) skill 补充读者画像配置。"
                    )
                    results["reader_profile"] = False
                elif not rp.get("platform") or not rp.get("gender"):
                    errors.append(
                        f"HARD-GATE: reader_profile 不完整（当前: {rp}），"
                        "缺少 platform 或 gender。请先执行 开书启动(bootstrap) skill。"
                    )
                    results["reader_profile"] = False
                else:
                    results["reader_profile"] = True
            else:
                errors.append(
                    "HARD-GATE: 无法加载 project.yaml 进行检查。"
                )
                results["reader_profile"] = False
        
        # 2. v3.db 检查：emergent-writer 依赖 v3.db
        if "emergent-writer" in skill_name:
            # 优先从 project.yaml paths.database 定位
            v3_found = False
            try:
                from glue.project_config import resolve_path
                db_dir = resolve_path(project_dir, "database")
            except (ImportError, KeyError, FileNotFoundError):
                db_dir = os.path.join(project_dir, "04-数据库")

            if os.path.isdir(db_dir):
                for f in os.listdir(db_dir):
                    if "v3" in f.lower() and f.endswith(".db"):
                        v3_found = True
                        break
            if not v3_found:
                errors.append(
                    "HARD-GATE: v3.db 不存在。"
                    "请先执行 拆书解构(book-deconstructor) skill 生成设定数据库。"
                )
                results["v3.db"] = False
            else:
                results["v3.db"] = True
        
        # 3. constitution.yaml 检查：opening-arc / market-test 依赖书籍宪法
        constitution_skills = ["opening-arc", "market-test"]
        if any(s in skill_name for s in constitution_skills):
            # 尝试多个可能位置
            constitution_paths = [
                os.path.join(project_dir, "00-原始设定", "constitution.yaml"),
                os.path.join(project_dir, "constitution.yaml"),
            ]
            # 如果 project.yaml 有定义则优先
            if config:
                paths = config.get("paths", {})
                if "constitution" in paths:
                    constitution_paths.insert(0, os.path.join(project_dir, paths["constitution"]))
            constitution_found = any(os.path.isfile(p) for p in constitution_paths)
            if not constitution_found:
                errors.append(
                    "HARD-GATE: constitution.yaml 不存在。"
                    "请先执行 书籍宪法生成(constitution) skill 生成书籍宪法。"
                )
                results["constitution.yaml"] = False
            else:
                results["constitution.yaml"] = True
        
        return results, errors
    
    # ============================================
    # ④ 上下文装配
    # ============================================
    
    def _assemble_context(self, inject_keys: List[str], project_dir: str) -> Dict[str, str]:
        """装配上下文"""
        context = {}
        
        if not project_dir:
            return context
        
        for key in inject_keys:
            # 尝试直接作为文件路径
            file_path = os.path.join(project_dir, key)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        context[key] = f.read()
                except:
                    context[key] = f"[无法读取: {file_path}]"
            else:
                context[key] = f"[未找到: {file_path}]"
        
        return context
    
    # ============================================
    # ⑤ 子Agent Prompt 生成
    # ============================================
    
    def _build_prompt(self, job: JobOrder) -> str:
        """生成子Agent 执行 prompt"""
        lines = []
        lines.append(f"# 编排任务单 — pop Harness")
        lines.append(f"")
        lines.append(f"## 任务")
        lines.append(f"- Skill: {job.display_name} ({job.skill_name})")
        lines.append(f"- 版本: {job.version}")
        lines.append(f"- 场景: {job.category} → {job.manifest.scenario}")
        lines.append(f"- 模式: {job.manifest.mode}")
        lines.append(f"")
        lines.append(f"## 描述")
        lines.append(f"{job.manifest.description}")
        lines.append(f"")

        # ★ 规则中枢注入（v1.0 新增）
        try:
            from glue.rule_hub.hub import load as load_rules, inject as inject_rules
            rules = load_rules(job.project_dir)
            if rules:
                # 映射 skill_name → 管线阶段
                stage_map = {
                    "spec-bridge": "director",
                    "skill-emergent-writer": "pass2",
                    "skill-qa-payoff": "qc",
                    "skill-plot-architecture": "director",
                    "skill-project-bootstrap": "director",
                    "skill-opening-arc": "pass2",
                    "skill-book-deconstructor": "director",
                    "skill-market-test": "qc",
                }
                stage = stage_map.get(job.skill_name, "")
                if stage:
                    rule_block_text = ""
                    for r in rules:
                        if stage == "director" and r.enforce.get("director_constraint"):
                            rule_block_text += f"\n- [{r.severity}] {r.enforce['director_constraint'].get('text', r.problem)}"
                        elif stage == "pass2" and r.enforce.get("redline"):
                            rule_block_text += f"\n- [{r.severity}] {r.problem}"
                        elif stage == "qc" and r.enforce.get("qc_check"):
                            qc = r.enforce["qc_check"]
                            rule_block_text += f"\n- {qc.get('id', r.rule_id)}: {qc.get('description', r.problem)}"
                    if rule_block_text:
                        lines.append(f"## ★ 历史教训约束（规则中枢 — 不可违反）")
                        lines.append(rule_block_text.strip())
                        lines.append(f"")
        except ImportError:
            pass

        lines.append(f"## 上下文")
        for key, val in job.context.items():
            lines.append(f"### {key}")
            lines.append(f"```")
            lines.append(val[:2000] if len(val) > 2000 else val)
            lines.append(f"```")
            lines.append(f"")
        lines.append(f"## 前置检查结果")
        for check, passed in job.preflight_results.items():
            icon = "✅" if passed else "❌"
            lines.append(f"- {icon} {check}")
        lines.append(f"")
        if job.errors:
            lines.append(f"## 警告")
            for e in job.errors:
                lines.append(f"- ⚠️ {e}")
            lines.append(f"")
        lines.append(f"请根据以上上下文执行 {job.display_name} 的 SOP。")
        
        return "\n".join(lines)
    
    def describe(self, job: JobOrder) -> str:
        """生成 pop agent 的声明文本"""
        gate = "✅ 门全开" if job.pass_gate else "❌ 有阻塞"
        lines = [
            f"🖋️ **pop 收到老板指示**",
            f"",
            f"任务理解：{job.manifest.description[:80]}...",
            f"场景判断：{job.category} → {job.manifest.scenario}",
            f"路由技能：{job.display_name} {job.version}（推荐 #{job.manifest.recommended}）",
        ]
        
        if job.preflight_results:
            checks = " / ".join([f"{k} → {'✅' if v else '❌'}" for k, v in job.preflight_results.items()])
            lines.append(f"前置条件：{checks}")
        
        lines.append(f"大门状态：{gate}")
        
        return "\n".join(lines)


# ============================================
# CLI 入口
# ============================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="pop Harness 编排控制器")
    parser.add_argument("user_intent", help="用户需求文本")
    parser.add_argument("--project", "-p", default="", help="项目路径")
    parser.add_argument("--dry-run", action="store_true", help="仅路由不执行")
    args = parser.parse_args()
    
    harness = Harness(args.project)
    job = harness.route(args.user_intent, args.project, args.dry_run)
    
    print("=" * 60)
    print(harness.describe(job))
    print("=" * 60)
    
    if job.manifest:
        print(f"\n📋 Frontmatter 解析:")
        print(f"  Name: {job.manifest.name}")
        print(f"  Tags: {job.manifest.tags}")
        print(f"  Preflight: {job.manifest.preflight}")
        print(f"  Dependencies: {job.manifest.dependencies}")
        print(f"  Inject Context: {job.manifest.inject_context}")
        print(f"  SubAgent: {'是' if job.manifest.subagent_required else '否'}")
    
    if args.dry_run:
        print(f"\n🔍 Dry-run: 不走 glue，仅查路由")
