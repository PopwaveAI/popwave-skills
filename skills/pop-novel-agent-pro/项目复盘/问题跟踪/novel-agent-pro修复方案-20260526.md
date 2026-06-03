# novel-agent-pro v3.2 全量修复方案

> **修复对象**: `e:/AI小说/_工具配置/novel-agent-pro`
> **来源报告**: `全量Gap曝光报告.md`（25项）
> **修复日期**: 2026-05-26
> **原则**: 每阶段只改一层，改完可独立验证，改坏可回滚

---

## 阶段总览

| 阶段 | 覆盖 Gap | 修改文件数 | 预计耗时 | 影响范围 |
|:----|:--------|:---------|:--------|:--------|
| **Phase 0** — 止血：否定句+锚定章 | GAP02, GAP11 | 1 | 10min | 全局提升 |
| **Phase 1** — 重塑注入层 | GAP01, GAP09, GAP10 | 2 | 45min | bundle 内容质量 |
| **Phase 2** — 修复数据层 | GAP07, GAP15, GAP16, GAP17, GAP18, GAP08 | 1 | 60min | DB 完整性 |
| **Phase 3** — 管线硬闸门 | GAP06, GAP12, GAP13, GAP14, GAP24 | 1 | 45min | 管线可阻断 |
| **Phase 4** — 元设计补全 | GAP20, GAP21, GAP22, GAP03 | 3 | 30min | 设计层完整 |
| **Phase 5** — 自动化测试 | GAP04, GAP05, GAP23, GAP25, GAP26 | 2 | 60min | 可回归验证 |

---

# Phase 0 · 止血修复（10min）

> **为什么先做这个**：否定句漏检和锚定章正则断裂是"改动最小、收益最大"的两个gap。修完后立即生效，所有章节的质量都有提升。

## 0.1 修复否定句检测：补全第3变体

**修改文件**: `skills/skill-emergent-writer/scripts/main.py`
**位置**: `_post_render_auto_check` 函数（第103-114行）
**覆盖**: GAP11

```python
# 当前（第103-114行）
neg_patterns = [
    r'不是[^，。]{1,30}而是',
    r'不是[^，。]+不是[^，。]+是',
]

# 修复为：
neg_patterns = [
    # 变体1: "不是A而是B"
    r'不是[^，。\n]{1,30}而是',
    # 变体2: "不是A不是B是一种C"
    r'不是[^，。\n]+不是[^，。\n]+是[一|种|某种]',
    # 变体3: "说不清(楚)的(颜色|感觉|味道|声音)"
    r'说不清[楚的]{0,2}(?:的)?\s*(?:颜色|感觉|味道|声音|情绪|恐惧)',
    # 变体4: "是某种/一种说不清的"
    r'是(?:某种|一种)\s*说不清[的楚楚]{0,4}',
    # 变体5: "直觉告诉" / "他不知道为什么"
    r'直觉告诉',
    r'不知道为什么(?:地|的)?',
]
```

**验证方式**: 修改后运行 `python main.py autocheck --chapter-path ch017.md`，应检测出"说不清楚的颜色"。

## 0.2 修复锚定章正则匹配

**修改文件**: `skills/skill-emergent-writer/scripts/main.py`
**位置**: `_load_anchor_chapter` 函数（第59-75行）
**覆盖**: GAP02

```python
def _load_anchor_chapter(project_root: str, skeleton_path: str) -> str:
    """从骨架或 Director 输出中提取锚定章引用，从锚定章库加载全文"""
    if not skeleton_path or not os.path.isfile(skeleton_path):
        return ""
    with open(skeleton_path, "r", encoding="utf-8") as f:
        text = f.read()

    anchor_file = None

    # 模式1: 骨架格式 `锚定章《filename》`
    m = re.search(r'锚定章[《\s]*([^《》\n]+)(?:\.md)?[》]?', text)
    if m:
        anchor_file = m.group(1).strip()

    # 模式2: Director 格式 `### 锚定章引用\n**主锚定**：`filename``
    if not anchor_file:
        m = re.search(r'主锚定[：:]\s*[`"\']?([^`"\'\n]+)(?:\.md)?[`"\']?', text)
        if m:
            anchor_file = m.group(1).strip()

    # 模式3: 旧格式 `锚定章引用: filename`
    if not anchor_file:
        m = re.search(r'锚定章引用[：:]\s*["\']?([^"\'\n]+)(?:\.md)?["\']?', text)
        if m:
            anchor_file = m.group(1).strip()

    if not anchor_file:
        return ""

    anchor_dir = os.path.join(project_root, "01-写作资产", "锚定章库")
    if not os.path.isdir(anchor_dir):
        return f"（锚定章库目录不存在: {anchor_dir}）"

    for fname in os.listdir(anchor_dir):
        # 模糊匹配：去除空格、书引号、扩展名后比对
        clean_fname = re.sub(r'[\s《》""\']', '', fname).replace('.md', '')
        clean_anchor = re.sub(r'[\s《》""\']', '', anchor_file).replace('.md', '')
        if clean_anchor in clean_fname or clean_fname in clean_anchor:
            path = os.path.join(anchor_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # 只取前 2000 字锚定片段
            return content[:2000] if len(content) > 2000 else content

    return f"（锚定章文件未找到: {anchor_file}）"
```

**验证方式**: 修改后运行 `python main.py before 10 --skeleton ch010-事实骨架.md --project ...`，检查 bundle 中 `## ⑧ 锚定章片段` 是否从"无锚定章引用"变成实际内容。

---

# Phase 1 · 重塑注入层（45min）

> **为什么第二做**：注入层是所有数据进入正文写作的入口。原始设定不进 → 正文 Agent 不知道大量设计约束。14项变9项 → 输入包信息量少了36%。

## 1.1 添加原始设定文件读取

**修改文件**: `skills/skill-emergent-writer/scripts/main.py`
**新增函数**（在 `_build_pass2_input` 之前）:
**覆盖**: GAP01

```python
def _read_original_settings(project_root: str) -> str:
    """读取 00-原始设定/ 下的所有关键设定文件，拼接后注入 bundle"""
    settings_dir = os.path.join(project_root, "00-原始设定")
    if not os.path.isdir(settings_dir):
        return "（原始设定目录不存在）"

    key_files = [
        # L0-产品层
        "L0-产品层/角色行为锚定.md",
        "L0-产品层/金手指设计.md",
        "L0-产品层/PRD.md",
        # L1-元设定层
        "L1-元设定层/01-世界底座.md",
        "L1-元设定层/02-对抗模型.md",
        "L1-元设定层/03-成长体系.md",
        "L1-元设定层/05-主角契约.md",
        "L1-元设定层/06-力量体系.md",
        "L1-元设定层/数值体系.md",
        "L1-元设定层/诡异行为性格.md",
    ]

    sections = []
    for rel_path in key_files:
        full_path = os.path.join(settings_dir, rel_path)
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            # 只取核心约束部分（跳过模板说明）
            if len(content) > 1500:
                content = content[:1500] + "\n...(已截断，完整设定见原始文件)"
            sections.append(f"### {os.path.basename(rel_path)}\n{content}")
        else:
            sections.append(f"### {os.path.basename(rel_path)}\n（文件缺失）")

    return "\n\n".join(sections)
```

## 1.2 补全 bundle 中缺失的 5 项输入

**修改文件**: `skills/skill-emergent-writer/scripts/main.py`
**位置**: `_build_pass2_input` 函数
**覆盖**: GAP09, GAP10

在现有函数中插入以下代码块——在 `## ⑧ 锚定章片段` 之后，`return` 之前：

```python
    # ⑨ 导演决策日志（v3.2 新增——从 Director 文件中提取）
    director_path = os.path.join(project_root, "01-写作资产", f"ch{chapter:03d}-director.md")
    lines.append("## ⑨ 导演决策日志\n")
    if os.path.isfile(director_path):
        with open(director_path, "r", encoding="utf-8") as f:
            lines.append(f.read())
    else:
        lines.append("（无 Director 文件）\n")
    lines.append("")

    # ⑩ 原始设定约束包（Gap修复——将原始设定注入正文写作）
    original_settings = _read_original_settings(project_root)
    lines.append("## ⑩ 原始设定约束包\n")
    lines.append(original_settings)
    lines.append("")

    # ⑪ 上一轮 QC 反馈
    qc_path = os.path.join(project_root, "01-写作资产", f"ch{chapter:03d}-qc-text.md")
    lines.append("## ⑪ 上一轮 QC 反馈\n")
    if os.path.isfile(qc_path):
        with open(qc_path, "r", encoding="utf-8") as f:
            qc = f.read()
        lines.append(qc[:800])  # 只取前800字
    else:
        lines.append("（无QC反馈）\n")
    lines.append("")

    # ⑫ 上一章全文（非仅结尾800字——增加上下文）
    if chapter > 1:
        prev_full = os.path.join(project_root, "03-正文", f"ch{chapter-1:03d}.md")
        lines.append("## ⑫ 上一章全文\n")
        if os.path.isfile(prev_full):
            with open(prev_full, "r", encoding="utf-8") as f:
                lines.append(f.read())
        else:
            lines.append("（上一章文件缺失）\n")
    lines.append("")

    # ⑬ 下一章钩子预告
    lines.append("## ⑬ 下一章钩子预告\n")
    # 尝试从 act-01.yaml 读取
    act_path = os.path.join(project_root, "02-幕纲", "act-01.yaml")
    if os.path.isfile(act_path) and chapter < 30:
        import yaml
        with open(act_path, "r", encoding="utf-8") as f:
            act = yaml.safe_load(f)
        chapters = act.get("chapters", [])
        if chapter < len(chapters):
            next_ch = chapters[chapter]  # 0-indexed: chapter 1 → index 0
            lines.append(f"下一章标题: {next_ch.get('title', '未知')}")
            lines.append(f"情感目标: {next_ch.get('emotional_goal', '未知')}")
            hook = next_ch.get("end_hook", {}).get("content", "")
            if hook:
                lines.append(f"本章钩子指向: {hook}")
    else:
        lines.append("（无法读取下一章信息）\n")
    lines.append("")

    return "\n".join(lines)
```

**验证方式**: 修改后运行 `python main.py before 10 --project ...`，检查输出是否包含 14 个 `## ⑨`~`## ⑬` 区块，且内容非空。

## 1.3 更新 SKILL.md 的 inject_context

**修改文件**: `skills/skill-emergent-writer/SKILL.md`
**位置**: `inject_context` 字段
**覆盖**: GAP01（声明层）

```yaml
# 当前（第16-21行）
inject_context:
  - "project.yaml#reader_profile"
  - "02-幕纲/act-XX.yaml"
  - "02-章纲/global-summary.md"
  - "01-写作资产/"
  - "01-事实骨架/"

# 修复为：
inject_context:
  - "project.yaml#reader_profile"
  - "02-幕纲/act-XX.yaml"
  - "02-章纲/global-summary.md"
  - "00-原始设定/L1-元设定层/"       # ← Phase 1 新增
  - "00-原始设定/L0-产品层/"         # ← Phase 1 新增
  - "01-写作资产/锚定章库/"           # ← 已有但未显式列出
  - "01-写作资产/"
  - "01-事实骨架/"
```

同时更新 `produces` 中 Phase 3 的描述：`"14 项输入包（完整版，已补全⑨-⑬）"`。

---

# Phase 2 · 修复数据层（60min）

> **为什么第三做**：DB 空白是系统性的——不是因为写了 bad code，是因为 EntityUpdater 的检测模式与实际骨架格式不匹配。1 个修复同时解决 6 个 gap。

## 2.1 改造 EntityUpdater 的检测逻辑

**问题根因**: `CHANGE_PATTERN` 期望 `{苏午}.心态: 冷静` 格式，但实际骨架格式是 `{林深}`（只标记，无字段赋值）。所以永远检测不到变化。

**修改文件**: `skills/skill-emergent-writer/scripts/updater.py`
**覆盖**: GAP07, GAP08, GAP15, GAP16, GAP17, GAP18

在 `EntityUpdater` 类中新增方法 `detect_entities_from_skeleton`：

```python
# 在 detect_changes 方法之后添加：

def detect_entities_from_skeleton(self, skeleton_text: str, chapter: int) -> List[dict]:
    """
    从事实骨架的 {实体名} 标记中提取实体及其隐含的状态变化。
    格式: {林深}在{客厅}打开了{诡异APP}
       → 林深: last_appearance=chapter, location="客厅"
       → 诡异APP: last_appearance=chapter
    """
    refs = EntityLoader.extract_entity_references(skeleton_text)
    if not refs:
        return []

    changes = []
    for name in refs:
        # 每个实体至少记录一次 "出现在了这章"
        changes.append({
            "entity": name,
            "field": "last_appearance", 
            "new_value": str(chapter),
        })

        # 尝试从骨架上下文中推断状态变化
        # 格式: {实体}在{地点} → 更新位置
        loc_pattern = re.compile(
            r'\{' + re.escape(name) + r'\}(?:在|来到|走到|站在|进入)(\{([^}]+)\})?'
        )
        m = loc_pattern.search(skeleton_text)
        if m and m.group(2):
            changes.append({
                "entity": name,
                "field": "位置",
                "new_value": m.group(2),
            })

    # 去重：同一实体的同字段只保留第一次
    seen = set()
    unique = []
    for c in changes:
        key = (c["entity"], c["field"])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique
```

同时修改 `apply_changes_from_skeleton`，在现有 `detect_changes` 失败时回退到 `detect_entities_from_skeleton`：

```python
def apply_changes_from_skeleton(self, skeleton_file: str, chapter: int) -> int:
    """从事实骨架文件读取并应用状态变化"""
    with open(skeleton_file, "r", encoding="utf-8") as f:
        skeleton = f.read()
    
    # 先尝试格式1: {实体}.字段: 新值
    changes = self.detect_changes(skeleton)
    
    # 如果没检测到，回退到格式2: 从 {实体} 标记推断
    if not changes:
        changes = self.detect_entities_from_skeleton(skeleton, chapter)
    
    if not changes:
        print(f"[ESM] ⚠️ 事实骨架中未检测到状态变化: {skeleton_file}")
        return 0
    
    return self.apply_changes(changes, chapter)
```

**验证方式**: 修改后运行 `python main.py after 5 --skeleton ch005-事实骨架.md --project ...`，应看到 `state_changelog` 表中有记录，而不是"检测到 0 个状态变化"。

## 2.2 修复 _auto_create_entity 的容错

**修改文件**: `skills/skill-emergent-writer/scripts/updater.py`
**位置**: `_auto_create_entity` 方法
**覆盖**: GAP17（玩家自动入库）

```python
def _auto_create_entity(self, cur, book_id: int, name: str) -> Optional[int]:
    """自动创建占位实体——自动识别实体类型"""
    try:
        # 判断实体类型
        entity_type = 'character'
        tbl = 'characters'
        
        # 玩家编号模式: 001-006
        if re.match(r'^玩家\d{3}$', name) or re.match(r'^00[1-6]$', name):
            entity_type = 'character'
            tbl = 'characters'
        # 特殊实体
        elif name in ['诡异APP', '诡异残留', '系统']:
            entity_type = 'item'
            tbl = 'items'
        elif '诡异' in name or '诡' in name or name in ['影诡', '路灯熄', '隙影', '沉默邻居', '镜中人']:
            entity_type = 'weird'
            tbl = 'weirds'
        elif '技能' in name or 'Lv' in name or '天赋' in name:
            entity_type = 'skill'
            tbl = 'skills'
        
        if tbl == 'characters':
            cur.execute("""
                INSERT OR IGNORE INTO characters 
                (book_id, name, brief, importance, first_appearance, last_appearance, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (book_id, name, f"[auto] 从骨架自动创建", 3, None, None, 'auto-created'))
        elif tbl == 'items':
            cur.execute("""
                INSERT OR IGNORE INTO items
                (book_id, name, brief, first_appearance, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (book_id, name, f"[auto] 自动创建", None, 'auto-created'))
        elif tbl == 'weirds':
            cur.execute("""
                INSERT OR IGNORE INTO weirds
                (book_id, name, brief, first_appearance, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (book_id, name, f"[auto] 自动创建", None, 'auto-created'))
        
        cur.execute(f"SELECT id FROM {tbl} WHERE name=? AND book_id=?", (name, book_id))
        row = cur.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"[ESM] ⚠️ 自动创建实体失败 ({name}): {e}")
        return None
```

---

# Phase 3 · 管线硬闸门（45min）

> **核心变更**：把"文字提示"变成"代码拦截"。Pipeline 在 pass2-render 完成后多一个真实验证步骤。

## 3.1 在管线中添加硬验证步骤

**修改文件**: `pipeline_orchestrator.py`
**覆盖**: GAP06, GAP12, GAP13, GAP24

在 `_execute_chapter` 方法中，`pass2-render` 和 `qc-text` 之间插入验证：

```python
# 在 _execute_chapter 中，pass2-render 的 checkpoint 写入之后：

if sub_step == "pass2-render":
    # 原来的 checkpoint 写入 ...
    self.cp.write(step_name, executor="pop")
    
    # ─── Phase 3 新增：硬验证 ───
    chapter_path = os.path.join(self.project, "03-正文", f"{ch_str}.md")
    if os.path.isfile(chapter_path):
        with open(chapter_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # 排除自评部分
        main_text = text.split("## 写后自评")[0] if "## 写后自评" in text else text
        wc = len(main_text.replace("\n", "").replace(" ", ""))
        
        # 硬闸门 1: 字数
        min_wc = self.config._data.get("quality", {}).get("min_chapter_word_count", 1800)
        if wc < min_wc:
            log(f"  ⛔ 质量闸门拦截: 字数 {wc} < {min_wc}")
            log(f"  ⚠️ 请扩充至 {min_wc} 字后重试。管线暂停。")
            raise RuntimeError(f"ch{ch:03d} 字数不足: {wc} < {min_wc}")
        
        # 硬闸门 2: 否定句（使用 main.py 的 _post_render_auto_check）
        from skills.skill_emergent_writer.scripts.main import _post_render_auto_check
        auto_result = _post_render_auto_check(chapter_path)
        if not auto_result["passed"]:
            failed_checks = [c for c in auto_result["checks"] if c["status"] in ("❌",)]
            log(f"  ⛔ 自动检查未通过: {failed_checks}")
            log(f"  ⚠️ 请修正后重试。管线暂停。")
            raise RuntimeError(f"ch{ch:03d} 自检不通过")
        
        log(f"  ✅ 硬验证通过: {wc}字 / 否定句0命中")
```

## 3.2 改造 _check_quality_gate 为阻断式

**修改文件**: `pipeline_orchestrator.py`
**位置**: `_check_quality_gate` 方法

```python
def _check_quality_gate(self, ch: int) -> bool:
    """返回 True 表示通过，False 表示阻断"""
    ch_str = f"ch{ch:03d}"
    qc_path = os.path.join(self.project, "01-写作资产", f"{ch_str}-qc-text.md")
    
    if not os.path.isfile(qc_path):
        log(f"  ⚠️ QC 报告不存在: {qc_path}")
        return True  # 无报告可读时放行
    
    with open(qc_path, "r", encoding="utf-8") as f:
        qc_text = f.read()
    
    # 检查 QC 是否明确标记为不通过
    if "NOT PASS" in qc_text.upper() or "不通过" in qc_text:
        log(f"  ⛔ QC 报告标记为 NOT PASS")
        log(f"  📋 QC 反馈: {qc_text[:200]}...")
        return False
    
    return True
```

然后在调用处：

```python
if sub_step == "qc-text":
    if not self._check_quality_gate(ch):
        log(f"  ⛔ 质量闸门拦截。请根据 QC 反馈修改后重试。")
        raise RuntimeError(f"ch{ch:03d} QC 不通过")
```

## 3.3 添加 checkpoint 内容验证

**修改文件**: `pipeline_orchestrator.py`
**位置**: `_wait_for_checkpoint` 方法（替换原有简单的轮询）

```python
def _wait_for_checkpoint(self, step_name: str, timeout_minutes: int = DEFAULT_TIMEOUT_MINUTES):
    """轮询等待 checkpoint 文件出现并验证其内容合法性"""
    timeout_seconds = timeout_minutes * 60
    elapsed = 0
    while elapsed < timeout_seconds:
        if self.cp.has(step_name):
            # Phase 3 新增：验证 checkpoint 内容不是空洞的
            token_data = self.cp.read(step_name)
            if token_data and token_data.get("completed_at"):
                return
            else:
                log(f"  ⚠️ checkpoint {step_name} 存在但内容为空，继续等待...")
        time.sleep(5)
        elapsed += 5
    
    raise TimeoutError(f"⏰ 等待 {step_name} 超时 ({timeout_minutes}分钟)")
```

---

# Phase 4 · 元设计补全（30min）

## 4.1 补全 act-01.yaml schema

**修改文件**: `02-幕纲/act-01.yaml`（需要手动补充）以及 `pipeline_orchestrator.py` 的 task-card 生成逻辑
**覆盖**: GAP20, GAP21, GAP22

在 `pipeline_orchestrator.py` 的 `STEP_PLOT` task-card 中，instruction 要求每个 chapter 切片必须包含：

```yaml
# 每个 chapter 切片的必填字段（在生成 task-card 时注入约束）
- number: 18
  title: "开拓者"
  emotional_goal: "凝聚→爽"
  fun_level: "大"           # ← Phase 4 强制要求：零|微|中|大|超大
  scene_time: "白天"         # ← Phase 4 强制要求：清晨|白天|黄昏|入夜|深夜|黎明
  payoff:
    type: "组织爽"
    level: "大爽点"
    cost_type: "资源消耗"    # ← Phase 4 强制要求
    trigger: "..."
  # ... 其余字段保持不变
```

同时在 quality_rules 中添加：

```python
"quality_rules": (
    "- 连续 ≤ 1 章 fun_level='零'\n"
    "- scene_time 连续 ≤ 3 章重复\n"
    "- 同一 cost_type 不重复 ≥ 2 次\n"
),
```

## 4.2 Director prompt 明确注入 reader_profile

**修改文件**: `skills/skill-emergent-writer/prompt-templates/Director-prompt.md`
**覆盖**: GAP03

在"前置检查"部分替换为：

```markdown
## 前置检查（强制执行）

在输出设计说明前，必须先完成以下步骤：

```
□ 读者画像已读入: 从 project.yaml 读取 reader_profile，输出一行确认
   例: "我知道在给谁写: 番茄男频 18-28岁，每章停留≤40秒，连续2章无爽点即弃"
□ 经验日志已加载: 上轮类似场景的教训（如有）
□ 锚定章已选: 从 01-写作资产/锚定章库/ 中匹配至少 1 个同类型片段
□ 字数目标已定: 不低于2200，不高于2500
□ 原始设定已确认: 本章涉及的力量体系/诡异行为/成长路径已在设定文件中确认
```
```

---

# Phase 5 · 自动化测试（60min）

## 5.1 集成自动化质检 Skill

**修改文件**: `pipeline_orchestrator.py`
**覆盖**: GAP23, GAP25, GAP26

在 `_execute_chapter` 循环开始和结束时，自动调用 `自动化质检` skill 的审计功能：

```python
import sys
sys.path.insert(0, os.path.join(NOVEL_AGENT_ROOT, "skills"))

def _run_qa_pipeline(self, ch: int, step_name: str):
    """调用自动化质检 skill，生成结构化审计记录"""
    from 自动化质检.scripts.qa_pipeline import run_qc_pipeline, register_function
    
    ch_str = f"ch{ch:03d}"
    chapter_path = os.path.join(self.project, "03-正文", f"{ch_str}.md")
    
    if not os.path.isfile(chapter_path):
        return
    
    with open(chapter_path, "r", encoding="utf-8") as f:
        text = f.read()
    main_text = text.split("## 写后自评")[0] if "## 写后自评" in text else text
    wc = len(main_text.replace("\n", "").replace(" ", ""))
    
    config = {
        "target_skill": "emergent-writer",
        "steps": [{
            "id": f"ch{ch:03d}_pass2",
            "name": f"第{ch}章正文",
            "executor": {"type": "function", "function_name": "load_chapter", "args": {"text": main_text}},
            "validators": [
                {"type": "word_count", "min": self.config._data.get("quality", {}).get("min_chapter_word_count", 1800), "max": 3500, "severity": "error"},
                {"type": "regex_match", "pattern": r'不是[^，。]{1,30}而是', "must_match": False, "severity": "error"},
                {"type": "regex_match", "pattern": r'说不清[楚的]{0,2}(?:的)?\s*(?:颜色|感觉|味道)', "must_match": False, "severity": "warn"},
            ]
        }],
        "global_config": {
            "output_dir": os.path.join(self.project, ".pipeline", "qc_reports")
        }
    }
    
    @register_function("load_chapter")
    def load_chapter(text="", **kwargs):
        return {"text": text, "file_paths": [chapter_path]}
    
    report = run_qc_pipeline(config)
    return report
```

## 5.2 添加回归验证脚本

**新建文件**: `automation/regression_test.py`
**覆盖**: GAP25, GAP26

```python
"""
regression_test.py — 对已完成的章节做回归验证
用法: python regression_test.py --project "e:/AI小说/_小说项目/我的诡异游戏v3" --chapters 1-30
"""
import sys, os, re, json

def run_regression(project_path: str, chapters: range):
    results = []
    body_dir = os.path.join(project_path, "03-正文")
    
    for ch in chapters:
        path = os.path.join(body_dir, f"ch{ch:03d}.md")
        if not os.path.isfile(path):
            results.append({"chapter": ch, "status": "MISSING", "issues": ["文件不存在"]})
            continue
        
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        main = text.split("## 写后自评")[0] if "## 写后自评" in text else text
        wc = len(main.replace("\n", "").replace(" ", ""))
        
        issues = []
        if wc < 1800:
            issues.append(f"字数不足: {wc}")
        
        # 否定句
        neg = len(re.findall(r'不是[^，。\n]{1,30}而是', main))
        neg += len(re.findall(r'说不清[楚的]{0,2}', main))
        if neg > 1:
            issues.append(f"否定句: {neg}处")
        
        # 章末钩子
        last_3 = "\n".join(text.strip().split("\n")[-3:])
        if not any(c in last_3 for c in ["?", "！", "但", "然而", "不知道"]):
            issues.append("章末无钩子")
        
        results.append({
            "chapter": ch,
            "status": "PASS" if not issues else "ISSUES",
            "word_count": wc,
            "negation_hits": neg,
            "issues": issues
        })
    
    # 输出汇总
    passed = [r for r in results if r["status"] == "PASS"]
    failed = [r for r in results if r["status"] != "PASS"]
    print(f"\n回归验证: {len(passed)}/{len(results)} 通过")
    print(f"失败章节: {[r['chapter'] for r in failed]}")
    if failed:
        for r in failed:
            print(f"  ch{r['chapter']:03d}: {r['word_count']}字 / {r['issues']}")
    
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--chapters", default="1-17")
    args = parser.parse_args()
    
    start, end = map(int, args.chapters.split("-"))
    run_regression(args.project, range(start, end+1))
```

---

# 实施检查清单

每个阶段完成后的验证方法：

| 阶段 | 验证命令/方法 | 预期结果 |
|:----|:------------|:--------|
| **Phase 0** | `python main.py autocheck --chapter-path ch017.md` | 应检测出"说不清楚的颜色" |
| **Phase 0** | `python main.py before 10 --skeleton ch010-事实骨架.md --project ...` | bundle ⑧ 锚定章片段非空 |
| **Phase 1** | 同上 | bundle 包含 ⑨~⑬ 共 14 个区块 |
| **Phase 1** | 检查 bundle ⑩ 原始设定约束包 | 包含诡异行为性格/数值体系内容 |
| **Phase 2** | `python main.py after 5 --project ...` | state_changelog > 0 条 |
| **Phase 2** | `sqlite3 v3.db "SELECT COUNT(*) FROM characters"` | > 1 |
| **Phase 3** | 写一个字数<1800的章节跑管线 | 管线应Rais error并暂停 |
| **Phase 4** | 检查 act-01.yaml 的 fun_level/cost_type | 字段存在且非空 |
| **Phase 5** | `python regression_test.py --project ...` | 输出所有章节的通过/失败统计 |

---

# 风险与回滚策略

| 阶段 | 改动文件 | 回滚方式 |
|:----|:--------|:--------|
| Phase 0-2 | `main.py`, `SKILL.md` | git checkout 或还原备份 |
| Phase 3 | `pipeline_orchestrator.py` | 先备份为 `pipeline_orchestrator.py.bak` |
| Phase 4 | `act-01.yaml`, `Director-prompt.md` | yaml 文件手动备份 |
| Phase 5 | `regression_test.py`（新建） | 新文件不影响现有流程 |

**最坏情况回滚**：Phase 3 的硬闸门如果误报太多，可以在 `pipeline_config.yaml` 的 `quality` 段增加一个 `hard_gate_enabled: false` 开关。
