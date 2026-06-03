#!/usr/bin/env python3
"""
spec_to_prompt.py — Spec 桥接脚本

职责：
  1. --mode generate: 读取项目上下文 → 创建 .trae/specs/<change-id>/ 目录
     → 写入模板预填文件（spec.md + tasks.md + checklist.md）
     → 输出 Agent 生成提示（由 Agent 完成 LLM 依赖的占位符填充）
  2. --mode inject:   将 spec.md 注入到目标阶段的 Agent Prompt 中
  3. --mode verify:   对照 checklist.md 执行自动化验证
  4. --mode status:   显示当前 spec 状态

调用方式：
  python spec-bridge/scripts/spec_to_prompt.py --mode generate --project <dir> --change-id <id>
  python spec-bridge/scripts/spec_to_prompt.py --mode inject --project <dir> --target director|pass1|pass2|qc
  python spec-bridge/scripts/spec_to_prompt.py --mode verify --project <dir> --check <check_name>
  python spec-bridge/scripts/spec_to_prompt.py --mode status --project <dir>

退出码：
  0 = 全部通过
  1 = 有 WARN
  2 = 有 FAIL
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path

# ─── Spec 路径 ─────────────────────────────

SPEC_BASE = ".trae/specs"


def get_spec_dir(project_dir: str, change_id: str = None) -> str:
    """获取 spec 目录路径。如果未指定 change_id，查找最新"""
    base = os.path.join(project_dir, SPEC_BASE)
    if change_id:
        return os.path.join(base, change_id)
    # 查找最新的 spec 目录
    if not os.path.isdir(base):
        return None
    dirs = sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])
    return os.path.join(base, dirs[-1]) if dirs else None


def read_spec_file(spec_dir: str, filename: str) -> str:
    """读取 spec 文件"""
    path = os.path.join(spec_dir, filename)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ─── 模式：verify（自动化验证）────────────

def verify_word_count(text: str, target_min: int, target_max: int) -> dict:
    """验证字数"""
    # 中文字数（去除空格和标点后的中文字符数）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    status = "PASS"
    issues = []
    if chinese_chars < target_min:
        status = "FAIL"
        issues.append(f"字数不足: {chinese_chars} (目标≥{target_min})")
    elif chinese_chars > target_max:
        status = "WARN"
        issues.append(f"字数超限: {chinese_chars} (目标≤{target_max})")
    return {"status": status, "count": chinese_chars, "issues": issues}


def verify_non_goals(text: str, non_goals: list) -> dict:
    """检查是否涉及 Non-Goals 排除的内容"""
    issues = []
    for ng in non_goals:
        if ng and ng.strip():
            # 简单的关键词匹配（实际场景中可用更精确的语义匹配）
            keywords = ng.split("不")[-1] if "不" in ng else ng
            if len(keywords) > 2 and keywords[:4] in text:
                issues.append(f"可能涉及 Non-Goal: {ng[:30]}")
    status = "WARN" if issues else "PASS"
    return {"status": status, "issues": issues}


def verify_forbidden_patterns(text: str) -> dict:
    """检查违禁句式"""
    patterns = [
        (r"不是.*而是", "否定式描写: 不是...而是"),
        (r"不是.*不是.*是", "三重否定结构"),
        (r"^不是", "以'不是'开段"),
        (r"他感到|她感到|他意识到|她意识到|仿佛", "冗余前缀"),
    ]
    issues = []
    for pattern, desc in patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            issues.append(f"{desc} (发现 {len(matches)} 处)")
    status = "WARN" if issues else "PASS"
    return {"status": status, "issues": issues}


def verify_dialogue_ratio(text: str, min_ratio: float = 0.25) -> dict:
    """检查对话占比"""
    # 中文引号
    dialogue_chars = 0
    in_dialogue = False
    for char in text:
        if char in '""「」『』':
            in_dialogue = not in_dialogue
        elif in_dialogue:
            dialogue_chars += 1
    total_chars = len(text.replace(" ", "").replace("\n", ""))
    ratio = dialogue_chars / max(total_chars, 1)
    status = "PASS"
    issues = []
    if ratio < min_ratio:
        status = "WARN"
        issues.append(f"对话占比偏低: {ratio:.1%} (目标≥{min_ratio:.0%})")
    return {"status": status, "ratio": ratio, "issues": issues}


def verify_hook(text: str, hook_type: str = None) -> dict:
    """检查章末钩子"""
    last_500 = text[-500:] if len(text) > 500 else text
    indicators = r"[？！……——]|但|然而|不知道|还没|没有|不是|难道"
    has_hook = bool(re.search(indicators, last_500))
    status = "PASS" if has_hook else "FAIL"
    issues = []
    if not has_hook:
        issues.append("章末未检测到钩子")
    return {"status": status, "issues": issues}


def verify_entities(skeleton_text: str, min_count: int = 8) -> dict:
    """检查实体计数"""
    entities = set(re.findall(r'\{([^}]+)\}', skeleton_text))
    count = len(entities)
    issues = []
    status = "PASS"
    if count < min_count:
        status = "FAIL"
        issues.append(f"唯一实体数不足: {count} (目标≥{min_count})")
    return {"status": status, "count": count, "entities": list(entities), "issues": issues}


# ─── 验证调度 ─────────────────────────────

VERIFY_CHECKS = {
    "word_count": verify_word_count,
    "forbidden_patterns": verify_forbidden_patterns,
    "dialogue_ratio": verify_dialogue_ratio,
    "hook": verify_hook,
    "entities": verify_entities,
    "non_goals": verify_non_goals,
}


def run_verify(project_dir: str, check: str = None) -> dict:
    """执行验证"""
    results = {}
    spec_dir = get_spec_dir(project_dir)
    if not spec_dir:
        return {"error": "未找到 spec 目录，请先生成 spec.md"}

    spec_md = read_spec_file(spec_dir, "spec.md")
    if not spec_md:
        return {"error": "未找到 spec.md"}

    # 解析 spec.md 中的目标字数
    target_match = re.search(r"目标字数[：:]\s*(\d+)[-~到]?(\d*)", spec_md)
    target_min = int(target_match.group(1)) if target_match else 1800
    target_max = int(target_match.group(2)) if target_match and target_match.group(2) else target_min + 500

    # 读取正文
    ch_dir = os.path.join(project_dir, "03-正文")
    if os.path.isdir(ch_dir):
        ch_files = sorted([f for f in os.listdir(ch_dir) if f.endswith(".md")])
        if ch_files:
            latest_ch = os.path.join(ch_dir, ch_files[-1])
            with open(latest_ch, "r", encoding="utf-8") as f:
                ch_text = f.read()
        else:
            ch_text = ""
    else:
        ch_text = ""

    if check and check in VERIFY_CHECKS:
        if check == "word_count":
            results[check] = verify_word_count(ch_text, target_min, target_max)
        elif check == "forbidden_patterns":
            results[check] = verify_forbidden_patterns(ch_text)
        elif check == "dialogue_ratio":
            results[check] = verify_dialogue_ratio(ch_text)
        elif check == "hook":
            results[check] = verify_hook(ch_text)
        elif check == "entities":
            results[check] = verify_entities(ch_text)
        elif check == "non_goals":
            # 读取 Non-Goals 列表
            ngs = re.findall(r"## Non-Goals.*?\n(.*?)(?=\n##|\Z)", spec_md, re.DOTALL)
            non_goals = [ng.strip() for ng in ngs[0].split("\n") if ng.strip().startswith("-")] if ngs else []
            results[check] = verify_non_goals(ch_text, non_goals)
    else:
        # 执行全部检查
        for check_name in VERIFY_CHECKS:
            if check_name == "word_count":
                results[check_name] = verify_word_count(ch_text, target_min, target_max)
            elif check_name == "forbidden_patterns":
                results[check_name] = verify_forbidden_patterns(ch_text)
            elif check_name == "dialogue_ratio":
                results[check_name] = verify_dialogue_ratio(ch_text)
            elif check_name == "hook":
                results[check_name] = verify_hook(ch_text)
            elif check_name == "entities":
                results[check_name] = verify_entities(ch_text)
            elif check_name == "non_goals":
                ngs = re.findall(r"## Non-Goals.*?\n(.*?)(?=\n##|\Z)", spec_md, re.DOTALL)
                non_goals = [ng.strip() for ng in ngs[0].split("\n") if ng.strip().startswith("-")] if ngs else []
                results[check_name] = verify_non_goals(ch_text, non_goals)

    return results


# ─── 模式：status ────────────────────────

def show_status(project_dir: str) -> list:
    """显示 spec 状态"""
    base = os.path.join(project_dir, SPEC_BASE)
    if not os.path.isdir(base):
        print("❌ 未找到 .trae/specs/ 目录")
        return []

    status_lines = []
    spec_dirs = sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])

    for d in spec_dirs:
        spec_dir = os.path.join(base, d)
        has_spec = os.path.isfile(os.path.join(spec_dir, "spec.md"))
        has_tasks = os.path.isfile(os.path.join(spec_dir, "tasks.md"))
        has_checklist = os.path.isfile(os.path.join(spec_dir, "checklist.md"))

        # 解析 checklist 状态
        checklist_status = {}
        if has_checklist:
            with open(os.path.join(spec_dir, "checklist.md"), "r", encoding="utf-8") as f:
                cl_text = f.read()
            done = len(re.findall(r'\[x\]', cl_text))
            total = len(re.findall(r'\[ \]|\[x\]', cl_text))
            checklist_status = {"done": done, "total": total}

        line = f"  {d}: spec={'✅' if has_spec else '❌'} tasks={'✅' if has_tasks else '❌'} checklist={'✅' if has_checklist else '❌'}"
        if checklist_status:
            line += f" ({checklist_status['done']}/{checklist_status['total']} 通过)"
        status_lines.append(line)
        print(line)

    return status_lines


# ─── 模式：inject ────────────────────────

def inject_context(project_dir: str, target: str) -> dict:
    """将 spec.md 注入到 Agent Prompt (返回注入内容供 Agent 使用)"""
    spec_dir = get_spec_dir(project_dir)
    if not spec_dir:
        return {"error": "未找到 spec 目录"}

    spec_md = read_spec_file(spec_dir, "spec.md")
    if not spec_md:
        return {"error": "未找到 spec.md"}

    # 从 spec.md 提取关键段落
    sections = {}
    current_section = None
    for line in spec_md.split("\n"):
        h2_match = re.match(r"^##\s+(.+)", line)
        if h2_match:
            current_section = h2_match.group(1).strip()
            sections[current_section] = ""
        elif current_section and current_section in sections:
            sections[current_section] += line + "\n"

    inject_content = {
        "overview": sections.get("Overview", "").strip(),
        "goals": sections.get("Goals", "").strip(),
        "non_goals": sections.get("Non-Goals", "").strip(),
        "requirements": sections.get("Requirements", sections.get("Functional Requirements", "")).strip(),
        "constraints": sections.get("Constraints", "").strip(),
        "acceptance_criteria": sections.get("Acceptance Criteria", "").strip(),
    }

    # 输出注入格式
    print(f"=== Spec Injection for: {target} ===")
    print()
    print("## ★ Spec 约束（来自 spec.md — 不可违反）")
    print()
    if inject_content["overview"]:
        print("### Overview")
        print(inject_content["overview"])
        print()
    if inject_content["goals"]:
        print("### Goals（必须达成）")
        print(inject_content["goals"])
        print()
    if inject_content["non_goals"]:
        print("### Non-Goals（边界 — 不要碰）")
        print(inject_content["non_goals"])
        print()
    if inject_content["requirements"]:
        print("### Requirements（必须覆盖）")
        print(inject_content["requirements"])
        print()
    if inject_content["constraints"]:
        print("### Constraints（硬约束）")
        print(inject_content["constraints"])
        print()
    if inject_content["acceptance_criteria"]:
        print("### Acceptance Criteria（最终验收标准）")
        print(inject_content["acceptance_criteria"])

    return inject_content


# ─── 模板路径 ─────────────────────────────

_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")


def _read_template(name: str) -> str:
    """读取模板文件内容"""
    path = os.path.join(_TEMPLATES_DIR, name)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ─── 模式：generate（上下文装配 + 结构生成）──

def _detect_spec_level(change_id: str) -> str:
    """根据 change-id 判断 spec 层级"""
    if not change_id:
        return "micro"
    if "book-bootstrap" in change_id or "continuation" in change_id:
        return "macro"
    if "-ch" in change_id and change_id.count("-") >= 1:
        # ch001-ch003 → macro（批量）
        return "macro"
    # ch008 → micro
    return "micro"


def _read_project_context(project_dir: str) -> dict:
    """读取项目上下文，供模板填充和 Agent 使用"""
    ctx = {
        "project_name": os.path.basename(project_dir),
        "reader_profile": "",
        "constitution": "",
        "act_data": None,
        "last_chapter": "",
        "chapter_count": 0,
    }

    # 1. project.yaml / reader_profile
    proj_file = os.path.join(project_dir, "project.yaml")
    if os.path.isfile(proj_file):
        try:
            import yaml
            with open(proj_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            project = config.get("project", {})
            ctx["project_name"] = project.get("name", ctx["project_name"])
            rp = project.get("reader_profile", {})
            if rp:
                ctx["reader_profile"] = yaml.dump(rp, allow_unicode=True, default_flow_style=False).strip()
            paths = config.get("paths", {})
            ctx["_paths"] = paths
        except Exception as e:
            ctx["_yaml_error"] = str(e)

    # 2. constitution.yaml
    for candidates in [
        os.path.join(project_dir, "00-原始设定", "constitution.yaml"),
        os.path.join(project_dir, "constitution.yaml"),
    ]:
        if os.path.isfile(candidates):
            with open(candidates, "r", encoding="utf-8") as f:
                ctx["constitution"] = f.read()[:2000]  # 截取前 2000 字符
            break

    # 3. 查找 act-XX.yaml（支持多种路径）
    act_dirs = [
        os.path.join(project_dir, "02-幕纲"),
        os.path.join(project_dir, "02-大纲"),
        os.path.join(project_dir, "大纲"),
    ]
    if "_paths" in ctx:
        try:
            act_dirs.insert(0, os.path.join(project_dir, ctx["_paths"].get("act_outline", "")))
        except:
            pass

    for ad in act_dirs:
        if not os.path.isdir(ad):
            continue
        for f in sorted(os.listdir(ad)):
            if f.endswith(".yaml") and "act" in f:
                try:
                    with open(os.path.join(ad, f), "r", encoding="utf-8") as fh:
                        ctx["act_data"] = yaml.safe_load(fh)
                    break
                except:
                    continue
        if ctx["act_data"]:
            break

    # 4. 上一章正文
    ch_dir = os.path.join(project_dir, "03-正文")
    if os.path.isdir(ch_dir):
        ch_files = sorted([f for f in os.listdir(ch_dir) if f.endswith(".md") and f.startswith("ch")])
        ctx["chapter_count"] = len(ch_files)
        if ch_files:
            last_ch = os.path.join(ch_dir, ch_files[-1])
            with open(last_ch, "r", encoding="utf-8") as f:
                content = f.read()
            # 取末尾 1000 字符作为钩子上下文
            ctx["last_chapter"] = content[-1000:] if len(content) > 1000 else content

    return ctx


def generate_spec(project_dir: str, change_id: str = None) -> dict:
    """
    --mode generate 核心逻辑

    职责：
      1. 读取项目上下文（project.yaml / act-XX / constitution / 上一章）
      2. 确定 Spec 层级（macro / micro）
      3. 创建 .trae/specs/<change-id>/ 目录
      4. 将模板写入目标目录（预填可自动化部分）
      5. 返回结构化结果 + Agent 生成提示

    返回:
      dict: {
        "status": "ok" | "error",
        "project_name": "...",
        "level": "macro" | "micro",
        "change_id": "...",
        "spec_dir": "...",
        "files_created": [...],
        "agent_prompt": "..."
      }
    """
    from datetime import date

    # ── 确定 change-id ──
    if not change_id:
        # 自动推断：如果有 act 数据，按章节号生成；否则用时间戳
        ctx = _read_project_context(project_dir)
        if ctx.get("chapter_count", 0) > 0:
            next_ch = ctx["chapter_count"] + 1
            change_id = f"ch{next_ch:03d}"
        else:
            change_id = "01-book-bootstrap"

    spec_dir = os.path.join(project_dir, SPEC_BASE, change_id)
    level = _detect_spec_level(change_id)

    # ── 读取上下文 ──
    context = _read_project_context(project_dir)

    # ── 创建目录 ──
    os.makedirs(spec_dir, exist_ok=True)
    files_created = []

    # ── 读取模板 ──
    if level == "macro":
        spec_template = _read_template("spec-macro-template.md")
    else:
        spec_template = _read_template("spec-micro-template.md")
    tasks_template = _read_template("tasks-template.md")
    checklist_template = _read_template("checklist-template.md")

    today_str = date.today().strftime("%Y-%m-%d")
    project_name = context.get("project_name", os.path.basename(project_dir))

    # ── 写入 spec.md 模板 ──
    if spec_template:
        # 预填可自动化的头部元数据
        filled = spec_template.replace("[XXX]", change_id.lstrip("ch").rstrip("0123456789") or "1")
        filled = filled.replace("[书名/项目名]", project_name)
        filled = filled.replace("[任务名称]", f"{project_name} - {change_id}")
        filled = filled.replace("YYYY-MM-DD", today_str)
        filled = filled.replace("[change-id]", change_id)

        # micro spec 额外预填
        if level == "micro":
            # 填入章节号
            ch_num = change_id.replace("ch", "")
            filled = filled.replace("[XXX]", ch_num)
            filled = filled.replace("[N]", ch_num)
            filled = filled.replace("[Y]", "1")  # 默认第一幕

            # 如果有 act 数据，尝试填入章节上下文
            act_data = context.get("act_data")
            if act_data and isinstance(act_data, dict):
                chapters = act_data.get("chapters", [])
                if chapters:
                    try:
                        target_ch = int(ch_num)
                        for ch in chapters:
                            if ch.get("number") == target_ch:
                                title = ch.get("title", "")
                                purpose = ch.get("purpose", "")
                                if title:
                                    filled = filled.replace("[章节临时标题]", title)
                                if purpose:
                                    filled = filled.replace(
                                        "读者读完本章后，应该感受到什么。一句话。",
                                        purpose,
                                    )
                                break
                    except ValueError:
                        pass

            # 填入字数基线
            if "ch" in change_id:
                ch_num_only = change_id.replace("ch", "")
                try:
                    ci = int(ch_num_only)
                    if ci <= 3:
                        word_range = "2000-2500"
                    elif ci <= 10:
                        word_range = "2200-2600"
                    else:
                        word_range = "2000-2400"
                    filled = filled.replace("2200-2500", word_range)
                    filled = filled.replace("[如 2200-2500]", word_range)
                except ValueError:
                    pass

            # 填入上一章钩子上下文
            if context.get("last_chapter"):
                last_200 = context["last_chapter"][-200:].strip()
                filled = filled.replace(
                    "[上一章章末钩子/情绪落点]",
                    f"上一章结尾（末200字）:\n  「{last_200}」",
                )

        spec_path = os.path.join(spec_dir, "spec.md")
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(filled)
        files_created.append("spec.md")

    # ── 写入 tasks.md 模板 ──
    if tasks_template:
        filled = tasks_template.replace("[任务名称]", f"{project_name} - {change_id}")
        filled = filled.replace("[change-id]", change_id)
        filled = filled.replace("YYYY-MM-DD", today_str)
        tasks_path = os.path.join(spec_dir, "tasks.md")
        with open(tasks_path, "w", encoding="utf-8") as f:
            f.write(filled)
        files_created.append("tasks.md")

    # ── 写入 checklist.md 模板 ──
    if checklist_template:
        filled = checklist_template.replace("[任务名称]", f"{project_name} - {change_id}")
        filled = filled.replace("[change-id]", change_id)
        filled = filled.replace("YYYY-MM-DD", today_str)
        checklist_path = os.path.join(spec_dir, "checklist.md")
        with open(checklist_path, "w", encoding="utf-8") as f:
            f.write(filled)
        files_created.append("checklist.md")

    # ── 构造 Agent 生成提示 ──
    agent_prompt = f"""请按以下上下文，完成 spec.md 的内容填充。

## 项目信息
- 项目名称: {project_name}
- Spec 层级: {level}
- change-id: {change_id}
- 目录: {spec_dir}

## 项目上下文
- 已有章节数: {context.get('chapter_count', 0)}
- reader_profile: {context.get('reader_profile', '（未获取到）')}

## act 数据摘要
{str(context.get('act_data', '（无）'))[:1500]}

## 宪法约束摘要
{context.get('constitution', '（无）')[:1000]}

## 上一章末尾（钩子上下文）
{context.get('last_chapter', '（无）')[:800]}

---

### 请按以下步骤操作：

1. **读取 spec.md 模板**（已写入 {spec_dir}/spec.md）
2. 根据上述上下文，填充所有 `[占位符]` 为具体内容
3. 同时更新 tasks.md 和 checklist.md，确保：
   - tasks.md 的任务与 spec.md 的 Requirements 对应
   - checklist.md 的检查项与 spec.md 的 Acceptance Criteria 对应
4. 覆盖写入完成后的文件

### 填充原则：
- Goals 必须可量化
- Non-Goals 必须具体，防止 AI 自由发挥
- Acceptance Criteria 使用 Given/When/Then 三段式
- Constraints 引用项目 constitution.yaml 中的硬约束"""

    return {
        "status": "ok",
        "project_name": project_name,
        "level": level,
        "change_id": change_id,
        "spec_dir": spec_dir,
        "files_created": files_created,
        "agent_prompt": agent_prompt,
    }


# ─── 主入口 ────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Spec 桥接脚本")
    parser.add_argument("--mode", choices=["generate", "inject", "verify", "status"],
                        default="status", help="操作模式")
    parser.add_argument("--project", "-p", default=os.getcwd(), help="项目根目录")
    parser.add_argument("--change-id", help="Spec change ID")
    parser.add_argument("--target", choices=["director", "pass1", "pass2", "qc", "esm_before", "esm_after"],
                        help="注入目标阶段")
    parser.add_argument("--check", choices=list(VERIFY_CHECKS.keys()) + ["all"],
                        default="all", help="验证项")

    args = parser.parse_args()

    if args.mode == "inject":
        if not args.target:
            print("❌ --mode inject 需要 --target 参数")
            sys.exit(1)
        inject_context(args.project, args.target)

    elif args.mode == "verify":
        results = run_verify(args.project, args.check if args.check != "all" else None)
        if "error" in results:
            print(f"❌ {results['error']}")
            sys.exit(1)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        has_fail = any(r.get("status") == "FAIL" for r in results.values())
        has_warn = any(r.get("status") == "WARN" for r in results.values())
        if has_fail:
            sys.exit(2)
        if has_warn:
            sys.exit(1)

    elif args.mode == "status":
        show_status(args.project)

    elif args.mode == "generate":
        result = generate_spec(args.project, args.change_id)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        print("\n" + "=" * 60)
        print("✅ Spec 生成准备完成")
        print(f"   项目:      {result['project_name']}")
        print(f"   层级:      {result['level']}")
        print(f"   change-id: {result['change_id']}")
        print(f"   目录:      {result['spec_dir']}")
        print(f"   文件已创建:")
        for f in result.get("files_created", []):
            print(f"     ✅ {f}")
        print(f"\n--- 以下为 Agent 需要自行完成的 LLM 生成任务 ---")
        print(result['agent_prompt'])


if __name__ == "__main__":
    main()
