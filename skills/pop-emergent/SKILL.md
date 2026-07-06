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
| write | `skills/pop-emergent-write/SKILL.md` | 读取 seed、research、正文锚定、soul/文风锚定和项目状态，产出正文 |
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

### Soul / 文风锚定部署协议

涌现式写作不把文风DNA当剧情设计器。文风资产分三层：

| 文件 | 定位 | 消费者 |
| --- | --- | --- |
| `涌现/soul.md` | 短、硬、可执行的叙事魂：叙事人格、句子气口、段落呼吸、对白方式、信息释放、情绪外化、禁区 | write 每次必读 |
| `涌现/文风锚定.md` | 完整DNA或原文样例锚定：让 agent 感受笔触密度，不当剧情素材库 | write formal 优先读；太大时可只读匹配片段+保留 soul |
| `涌现/content-mechanics.md` | 从参考书剥离出的内容机制：武学招式、系统面板、诡异规则、职业数值、战斗升级结构等，明确路由到 seed/research/设定库，不属于文风 | seed/research/review |

第一性原则：**剧情血肉来自 seed/research/正文锚定；题材机制来自 seed/research/设定库；文风只通过 soul/文风锚定影响“怎么说”。**

pop-shared-dna 产出的 DNA 文件落在项目目录的 `写作资产/文风库/{书名}.md`，但 emergent-write 需要本地涌现资产。部署流程：

1. **DNA产出后**：pop-shared-dna 把 DNA 文件写入项目目录 `写作资产/文风库/{书名}.md`（已有逻辑）。
2. **部署到library库**：把 DNA 文件复制到 `$env:APPDATA\popwave\remote-skills\pop-trope-library\文风库\{书名}.md`，并更新 `文风库/00-索引.md` 添加条目。
3. **部署到项目本地**：把 DNA 文件复制到项目目录 `涌现/文风锚定.md`。
4. **生成/更新 soul**：从 DNA 和用户目标中提炼 `涌现/soul.md`。soul 不是摘要，不得写“冷峻/史诗/克制”等空标签；每条都必须能改写句子或段落。
5. **生成/更新 content-mechanics**：把参考书里不可直接当文风迁移的内容机制写入 `涌现/content-mechanics.md`，标明应路由到 seed/research/设定库。
6. **write消费**：emergent-write 每次必读 `soul.md`；formal 写作优先读 `文风锚定.md`，但不得把其中剧情内容当创作要求。

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

# 2a. 初始化 soul / content-mechanics 占位（需由 agent 根据DNA和项目目标补写）
$soulPath = Join-Path $dstDir "soul.md"
if (-not (Test-Path $soulPath)) {
@"
# Soul

> 待从文风DNA与本项目目标中提炼。每条必须能落到句子、段落、对白或信息释放；禁止空泛风格标签。

## 叙事人格

## 句子气口

## 段落呼吸

## 对白方式

## 信息释放

## 情绪外化

## 禁区
"@ | Set-Content $soulPath -Encoding UTF8
}

$mechanicsPath = Join-Path $dstDir "content-mechanics.md"
if (-not (Test-Path $mechanicsPath)) {
@"
# Content Mechanics

> 这里记录参考书中不属于文风的内容机制。它们不能由文风迁移到正文；需要时必须进入 seed / research / 设定库。

| 机制 | 来源 | 属于哪一层 | 是否允许迁移 | 正确路由 |
| --- | --- | --- | --- | --- |
"@ | Set-Content $mechanicsPath -Encoding UTF8
}

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
  soul.md                    # 叙事魂/表达约束（短、硬、可执行）
  文风锚定.md                # 完整文风DNA或原文样例锚定
  content-mechanics.md        # 参考书内容机制分流表，不属于文风
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

全文加载协议加载优先级：soul > 设定库 > 人物库 > 剧情线 > 最近10章涌现日志 > 压缩归档摘要 > seed/燃料文件 > 文风锚定/样例

## 红线

- 不调用正式 `pop-writer-v3-create` 处理涌现式试写。
- 不要求正式 plot 章级施工卡、章卡边界、微beat表；write 自己使用轻量"涌现写作包"。
- 不把 review 的沉淀直接冻结成正式设定，除非用户明确确认纳入项目。
- **禁止凭记忆写作**：write 执行前必须执行项目文件全文加载协议（见 pop-emergent-write SKILL.md），确保世界观/时间线/前序章节全文进入上下文。不允许"我之前读过"作为跳过理由。
- **禁止正文进对话历史**：正文写入 txt 文件，对话回复只给摘要+钩子。违反此条会导致上下文窗口被正文吃满，后续章节质量断崖。
- **禁止单章无限重写**：同一章重写超过 2 次后，降级为"试写-独立"处理，不得阻塞章节递进。
- **禁止空泛 soul**：`soul.md` 不能只有“冷峻、克制、史诗、爽、诡异”等形容词。每条必须说明如何影响句子、段落、对白、信息释放或情绪外化。
- **禁止把文风DNA当内容素材库**：文风锚定传递的是笔触（句式节奏/感官顺序/叙事距离/段落呼吸/对话引导），不是内容（武学招式、系统面板、战术复盘、剧情模板）。内容机制必须进入 `content-mechanics.md` 并路由到 seed/research/设定库。
