# 设计包格式后处理归一化

> **定位**: 在 delegate_task 并行提取全部批次完成后，对设计包文件执行一次全量格式归一化。
> **为什么需要**: 不同子 agent 使用不同 heading 格式（`# 第X章·标题 — 设计包 (v4)` vs `# 设计包 — chXXX「标题」`），3层+1区结构小节命名也不同（`事件链层` vs `骨架层` vs `情节层` 等变体）。
> **实测数据**: 149章批量提取后，44/44 抽检文件首行格式均不符合标准格式。

---

## 归一化脚本（Python）

将以下脚本放在 `_temp/` 下运行。它扫描 `写作资产/设计包v3/` 并修复两种最常见的漂移：

### 1. 首行格式归一化

```python
import os, re

DESIGN_DIR = '写作资产/设计包v4'

def normalize_heading(line: str) -> str | None:
    """将各种变体归一化为标准格式: # 设计包 — chXXX「标题」"""
    line = line.strip()
    
    # 变体1: # 第X章·标题 — 设计包 (v3)
    m = re.match(r'^#\s*第(\d+)章[·.．](.+?)\s*[—\-–]\s*设计包', line)
    if m:
        ch_num = int(m.group(1))
        title = m.group(2).strip()
        return f'# 设计包 — ch{ch_num:03d}「{title}」'
    
    # 变体2: # 第X章·标题 设计包v3
    m = re.match(r'^#\s*第(\d+)章[·.．](.+?)\s*设计包', line)
    if m:
        ch_num = int(m.group(1))
        title = m.group(2).strip()
        return f'# 设计包 — ch{ch_num:03d}「{title}」'
    
    # 变体3: # 设计包 (v3) — 第X章·标题
    m = re.match(r'^#\s*设计包.*?第(\d+)章[·.．](.+)', line)
    if m:
        ch_num = int(m.group(1))
        title = m.group(2).strip().rstrip(')）')
        return f'# 设计包 — ch{ch_num:03d}「{title}」'
    
    # 变体4: # chXXX 标题 设计包
    m = re.match(r'^#\s*ch(\d+)\s+(.+?)\s*设计包', line)
    if m:
        ch_num = int(m.group(1))
        title = m.group(2).strip()
        return f'# 设计包 — ch{ch_num:03d}「{title}」'
    
    return None  

def check_and_report():
    """扫描并报告格式问题"""
    issues = []
    for f in sorted(os.listdir(DESIGN_DIR)):
        if not f.endswith('.md'):
            continue
        path = os.path.join(DESIGN_DIR, f)
        with open(path, 'r', encoding='utf-8') as fh:
            first = fh.readline().strip()
        if not first.startswith('# 设计包 — ch'):
            issues.append((f, first[:60]))
    return issues
```

### 2. 3层+1区结构小节命名映射表

```python
SECTION_MAP = {
    # v4 标准命名（3层+1区）
    '事件链层': '事件链层', 'L1事件链层': '事件链层',
    '爽点层': '爽点层', 'L2爽点层': '爽点层',
    '角色层': '角色层', 'L3角色层': '角色层',
    '设定/物品提取区': '设定/物品提取区', 'S1设定/物品提取区': '设定/物品提取区',
    # v4 变体 → 设定/物品提取区
    '设定区': '设定/物品提取区', '设定物品区': '设定/物品提取区', '设定提取区': '设定/物品提取区',
    # v3 历史映射 → 事件链层（兼容历史文件）
    '骨架层': '事件链层', '情节层': '事件链层', '叙事层': '事件链层',
    '事件链': '事件链层', '剧情层': '事件链层',
    # v3 历史映射 → 爽点层（兼容历史文件）
    '爽点设计': '爽点层', '情绪层': '爽点层',
    # v3 历史映射 → 角色层（兼容历史文件）
    '角色与人设': '角色层', '人物层': '角色层', '人物弧层': '角色层',
    # v3 感官层映射（保留兼容历史文件，v4 已删除此层）
    '感官层': '感官层', '感官与画面': '感官层',
}

def normalize_sections(content: str) -> str:
    """将小节标题映射回标准3层+1区命名"""
    for old, new in SECTION_MAP.items():
        if old != new:
            content = content.replace(f'## {old}', f'## {new}')
            content = re.sub(
                rf'^(## \d+\.\s*){re.escape(old)}',
                rf'\1{new}',
                content,
                flags=re.MULTILINE
            )
    return content
```

### 3. 批量执行

```python
def normalize_all():
    stats = {'heading_fixed': 0, 'section_fixed': 0}
    for f in sorted(os.listdir(DESIGN_DIR)):
        if not f.endswith('.md'):
            continue
        path = os.path.join(DESIGN_DIR, f)
        with open(path, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()
        changed = False
        
        new_heading = normalize_heading(lines[0])
        if new_heading and new_heading != lines[0].strip():
            lines[0] = new_heading + '\n'
            stats['heading_fixed'] += 1
            changed = True
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('## '):
                for old, new in SECTION_MAP.items():
                    if old != new and old in stripped:
                        lines[i] = line.replace(old, new)
                        stats['section_fixed'] += 1
                        changed = True
                        break
        
        if changed:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.writelines(lines)
    return stats
```

---

## 执行时机

| 阶段 | 操作 |
|:-----|:------|
| **Step 3 验证后** | 执行 `check_and_report()` 输出格式问题清单 |
| **标记异常后** | 执行 `normalize_all()` 全量修复 |
| **修复后** | 重新执行 Step 3 验证，确认通过率 100% |

---

## ⚠️ 注意事项

- **先报告后修改**：先报告问题规模，再决定是否批量修复
- **不要正则替换 `# 设计包` 自身的正文引用**
- **3层+1区结构新增映射**：如遇到不在 SECTION_MAP 中的小节名（如「基底层」），判断其内容归属后新增映射条目
- **v4 事件表列数校验**：v4 事件表应为 **7 列**（`| # | 事件 | 类型 | scene | POV | 参与角色 | 原文证据 |`），非 v3 的 8 列（v3 多一个「字数估计」列）。归一化时检查事件表列数，若发现 8 列则删除「字数估计」列
- **执行后重跑套路归档检查**：小节名变化不影响套路文件（v4 不包含套路归档 pass）

## ★ 更好的策略：从源文件提取标题

上述脚本中的一个根本局限：它从**已经写错的第一行**中提取标题（garbage in → garbage out）。更可靠的策略是从源章节文件中读取实际标题：

1. 从 `_temp/chapters/chXXX.txt` 的第一行提取章节标题（如「第一百五十章 巫行空（月票900加）」）
2. 剥离阿拉伯数字/汉字数字的「第X章」前缀和括号后缀
3. 写入规范格式 `# 设计包 — chXXX「标题」`

**为什么更可靠：** 源文件的第一行永远不会因为子 agent 的格式漂移而写错。标题信息是直接从原文恢复的，不依赖子 agent 的任何输出格式。

**实测数据：** 本策略在 150 章拆解中成功修复了 69/150 文件的格式漂移（其中 53 个用源文件标题精确修复，16 个用正则回退）。修复率 100%。

**脚本路径：** `scripts/normalize-headlines-from-source.py`

**示例：**
```python
# 源文件第一行：第一百五十章 巫行空（月票900加）
# → 提取标题：巫行空
# → 写入： # 设计包 — ch150「巫行空」
```
