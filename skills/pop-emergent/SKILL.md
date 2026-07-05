---
name: pop-emergent
description: Pop 涌现式小说调度入口。用于用户请求涌现式写作、seed共创、research写作燃料、正文锚定写作、质量review、AI味审稿、复盘沉淀时，按 seed -> research -> write -> review 路由到四个执行 skill：pop-emergent-seed、pop-emergent-research、pop-emergent-write、pop-emergent-review；不进入正式 world/plot/create 管线。
---

# Pop Emergent

这是涌现式小说入口 skill，只负责判断阶段、读取对应执行 skill、检查阶段边界。具体产物由四个执行 skill 完成。

## 执行 skill

| 阶段 | 执行 skill | 职责 |
| --- | --- | --- |
| seed | `skills/pop-emergent-seed/SKILL.md` | 碰撞 idea，形成全书/本轮种子文档 |
| research | `skills/pop-emergent-research/SKILL.md` | 找能进场面的本书涌现燃料和外部写作燃料 |
| write | `skills/pop-emergent-write/SKILL.md` | 读取 seed、research、正文锚定、文风DNA和项目状态，产出正文 |
| review | `skills/pop-emergent-review/SKILL.md` | 审 seed 兑现、爽文兑现、AI味，并沉淀涌现资产 |

## 路由

| 用户请求 | 路由 |
| --- | --- |
| 想 idea、做 seed、全书种子、方向碰撞 | 读取并执行 `pop-emergent-seed` |
| 找燃料、查资料、外部事件怎么入戏、世界观怎么接现实 | 读取并执行 `pop-emergent-research` |
| 写、续写、重写、把 X 写成 Y、开篇样章、单章爽文 | 读取并执行 `pop-emergent-write`；缺燃料时先执行 `pop-emergent-research` |
| 审稿、AI味、爽不爽、质量复盘、沉淀新增设定 | 读取并执行 `pop-emergent-review` |
| 提取文风、文风DNA、风格蒸馏、分析作者笔触 | 读取并执行 `pop-shared-dna/SKILL.md`；产出后部署到 library 文风库 |
| 部署文风DNA到项目本地 | 执行文风DNA部署协议（见下方） |
| 跑完整涌现式 | 顺序执行 seed -> research -> write -> review |

## 调度规则

- 写作请求必须优先进入 `pop-emergent-write`，不得因为项目里已有草稿就自动改成 review。
- review 请求不得自动重写正文；用户要求修改后再进入 write。
- research 可以在 write 前自动补一轮轻量燃料，但不要写成长调研报告。
- seed 候选需要用户确认；用户明确说自动继续时才直接进入 research。
- 四个执行 skill 都使用 `formal / draft / trial` 执行模式，入口不得替它们伪造完成状态。
- 涉及真实项目落盘时，遵守执行 skill 的产物路径和“待确认/待冻结”边界。

### Research 触发规则

以下情况 write 前必须先执行 research：

- 新项目第一轮写作（无 seed/无燃料文件）。
- 跨世界观同人（如 BG3 × 战锤40K）：需 research 确认两个世界观的设定交集和冲突点。
- 涉及真实事件/技术/行业（如 DeepSeek R1）：需 research 确认事实细节。
- 距离上次 research 超过 5 章：需补一轮轻量 research。
- 用户明确要求查资料。

research 不需要长报告。目标是给 write 提供 3-5 条能进场面的燃料，每条有入戏方式、主角操作点、可外显爽点。

### 文风DNA部署协议

文风DNA是提升正式质量的最大杠杆。pop-shared-dna 产出的 DNA 文件落在项目目录的 `写作资产/文风库/{书名}.md`，但 emergent-write 的全文加载协议需要从 library 库加载。部署流程：

1. **DNA产出后**：pop-shared-dna 把 DNA 文件写入项目目录 `写作资产/文风库/{书名}.md`（已有逻辑）。
2. **部署到library库**：把 DNA 文件复制到 `$env:APPDATA\popwave\remote-skills\pop-trope-library\文风库\{书名}.md`，并更新 `文风库/00-索引.md` 添加条目。
3. **部署到项目本地**：把 DNA 文件复制到项目目录 `涌现/文风锚定.md`（单一文件，emergent-write 全文加载协议会自动加载）。
4. **write消费**：emergent-write 全文加载协议加载 `涌现/文风锚定.md`，涌现写作包的 `文风锚定` 字段要求 agent 定位到匹配场景卡。

部署命令（PowerShell）：

```powershell
# ===== 参数 =====
$projectDir = "{填入项目根目录路径}"
$bookName = "{书名}"
# ================

# 1. 源 DNA 文件路径
$srcDna = Join-Path $projectDir "写作资产\文风库\$bookName.md"
if (-not (Test-Path $srcDna)) {
    # 尝试 library 库路径
    $libDna = Join-Path $env:APPDATA "popwave\remote-skills\pop-trope-library\文风库\$bookName.md"
    if (Test-Path $libDna) { $srcDna = $libDna }
    else { Write-Output "DNA 文件未找到"; exit }
}

# 2. 部署到项目本地（emergent-write 加载路径）
$dstDir = Join-Path $projectDir "涌现"
New-Item -Path $dstDir -ItemType Directory -Force | Out-Null
Copy-Item $srcDna (Join-Path $dstDir "文风锚定.md") -Force

# 3. 部署到 library 库（canonical 路径）
$libDir = Join-Path $env:APPDATA "popwave\remote-skills\pop-trope-library\文风库"
if (Test-Path $libDir) {
    Copy-Item $srcDna (Join-Path $libDir "$bookName.md") -Force
    Write-Output "已部署到 library 文风库"
}

# 4. 更新 library 索引
$indexPath = Join-Path $libDir "00-索引.md"
if (Test-Path $indexPath) {
    $index = Get-Content $indexPath -Raw -Encoding UTF8
    $entry = "| $bookName | 文风库/$bookName.md | ✅ |"
    if ($index -notmatch [regex]::Escape($bookName)) {
        $index = $index -replace '(\|:-----\|:---------\|:-----\|)', "`$1`n$entry"
        Set-Content $indexPath $index -Encoding UTF8
        Write-Output "已更新 library 索引"
    }
}

Write-Output "文风DNA部署完成: $bookName -> 涌现/文风锚定.md"
```

**触发时机**：
- pop-shared-dna 产出 DNA 文件后自动触发。
- 用户明确要求"部署文风DNA"时触发。
- 新项目首次写作前，如果 library 库有匹配的 DNA 文件，提示用户选择并部署。

### 涌现资产分类存储

涌现日志禁止无限膨胀。按以下分类存储到 `涌现/` 目录：

```
涌现/
  seed-种子文档.md          # 种子（pop-emergent-seed 产出）
  research-写作燃料.md      # 燃料（pop-emergent-research 产出）
  review-沉淀.md             # 审稿沉淀（pop-emergent-review 产出）
  设定库.md                  # 冻结的设定（从 review 沉淀中确认纳入的）
  人物库.md                  # 冻结的人物状态
  剧情线.md                  # 冻结的剧情线追踪
  压缩归档/                  # 每10章压缩一次的历史记录
```

**每 10 章压缩一次**：把前 10 章的涌现日志压缩为一份摘要存入 `涌现/压缩归档/第1-10章摘要.md`，然后清空主日志只保留最近 10 章的详细记录。压缩时保留：
- 设定库/人物库/剧情线不受压缩影响（这些是累积的）
- 只压缩每章的详细新增设定、角色状态变化记录、剧情线推进记录
- 章末状态只保留最近一章的

全文加载协议加载优先级：设定库 > 人物库 > 剧情线 > 最近10章涌现日志 > 压缩归档摘要 > seed/燃料文件

## 红线

- 不调用正式 `pop-writer-v3-create` 处理涌现式试写。
- 不要求正式 plot 章级施工卡、章卡边界、微beat表；write 自己使用轻量"涌现写作包"。
- 不把 review 的沉淀直接冻结成正式设定，除非用户明确确认纳入项目。
- **禁止凭记忆写作**：write 执行前必须执行项目文件全文加载协议（见 pop-emergent-write SKILL.md），确保世界观/时间线/前序章节全文进入上下文。不允许"我之前读过"作为跳过理由。
- **禁止正文进对话历史**：正文写入 txt 文件，对话回复只给摘要+钩子。违反此条会导致上下文窗口被正文吃满，后续章节质量断崖。
- **禁止单章无限重写**：同一章重写超过 2 次后，降级为"试写-独立"处理，不得阻塞章节递进。
- **禁止摘要/压缩文风DNA传递**：调度 write 执行时，文风锚定（`涌现/文风锚定.md`）必须全文注入到写正文 agent 的上下文。禁止主 agent 读取文风锚定全文后压缩成抽象要点传给子 agent——实测发现压缩成 6 条 bullet points 后，子 agent 知道规则但看不到原文摘录，文风对齐失效。文风锚定全文必须用 exec（Get-Content -Raw）读取，禁止用 Read 工具读取（Read 工具有随机截断，实测保留率 9%-80%）。
- **禁止把文风DNA当内容素材库**：文风DNA传递的是笔触（句式节奏/感官顺序/叙事距离/段落呼吸/对话引导），不是内容（战术思维/战斗复盘/击杀余韵/剧情模板）。禁止从文风DNA原文摘录里提取剧情设计作为创作要求——原文摘录是让 agent 感受"作者怎么写"，不是让 agent 抄"作者写了什么"。
