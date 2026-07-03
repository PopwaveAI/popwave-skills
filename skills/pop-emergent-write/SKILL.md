---
name: pop-emergent-write
description: Pop 涌现式 write 执行 skill。用于写、续写、重写、把X写成Y、开篇样章、单章爽文、同人片段和战斗桥段。必须读取 seed、research 写作燃料、用户认可的正文锚定和当前项目状态，产出正文与创作记录；不调用正式 pop-writer-v3-create。
---

# Pop Emergent Write

write 负责产出正文。它不重新做正式 plot，但必须消费 seed、research、正文锚定和项目状态，不能凭灵感漂写。

## 执行模式

| 模式 | 条件 |
| --- | --- |
| `formal` | seed/research/正文锚定/当前状态/用户要求齐全，且有轻量写作包 |
| `draft` | 有关键输入缺口，但能保守写草案 |
| `trial` | 用户只要快速直出，或没有项目文件/锚定正文 |

## 必读输入

按优先级读取，不要全项目乱读：

1. `涌现/seed-种子文档.md` 或本轮临时 seed。
2. `涌现/research-写作燃料.md` 或本轮轻 research。
3. 正文锚定：用户明确认可的章节/试写；没有则读取最近一章或第一章作为临时锚定。
4. 当前项目状态：最近正文、世界观/外部燃料中与本章直接相关的片段、活审美上下文。
5. review 下一章修正规则：如存在，作为写作约束。
6. 用户本轮要求：场景、字数、输出位置、禁区。

### 项目文件全文加载协议

OpenClaw 的 Read 工具对大文件有截断限制（约 2000 行），agent 以为读了全文实际只拿到 40% 内容。世界观设定、前序章节的关键内容在后半部分全部丢失。

**每次写新章节前，必须执行以下 PowerShell 脚本**，把项目内所有 .txt/.md 文件拼合成一个完整文本块，一次性注入上下文：

```powershell
# ===== 参数 =====
$projectDir = "{填入项目根目录路径}"
# ================

$supportedExt = @('.txt', '.md')
$excludeFiles = @('README.md', '涌现日志.md', 'review-沉淀.md')
$chunks = @()

# 1. 涌现资产（优先级最高：文风锚定 > 设定库/人物库/剧情线）
$assetDir = Join-Path $projectDir "涌现"
$assetFiles = @('文风锚定.md', '设定库.md', '人物库.md', '剧情线.md')
foreach ($af in $assetFiles) {
    $ap = Join-Path $assetDir $af
    if (Test-Path $ap) {
        $chunks += "=== FILE: $af ===`n$(Get-Content $ap -Raw -Encoding UTF8)`n"
    }
}

# 2. seed/燃料文件
$settingFiles = Get-ChildItem $projectDir -Recurse -File | Where-Object {
    $supportedExt -contains $_.Extension -and
    $excludeFiles -notcontains $_.Name -and
    ($_.Name -match '世界观|设定|燃料|时间线|大纲|PRD|seed|research')
}
foreach ($f in $settingFiles | Sort-Object Length -Descending) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $chunks += "=== FILE: $($f.Name) ===`n$content`n"
}

# 3. 前序章节正文（按章节号排序）
$chapterFiles = Get-ChildItem $projectDir -Recurse -File | Where-Object {
    $supportedExt -contains $_.Extension -and
    $excludeFiles -notcontains $_.Name -and
    ($_.Name -match '第.*章|chapter|ch\d')
}
foreach ($f in $chapterFiles | Sort-Object Name) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $chunks += "=== FILE: $($f.Name) ===`n$content`n"
}

# 4. 涌现日志/沉淀（最后，让 agent 看到已有沉淀）
$logFiles = @('涌现日志.md', 'review-沉淀.md')
foreach ($logName in $logFiles) {
    $logPath = Join-Path $projectDir $logName
    $logPath2 = Join-Path $assetDir $logName
    if (Test-Path $logPath) {
        $chunks += "=== FILE: $logName ===`n$(Get-Content $logPath -Raw -Encoding UTF8)`n"
    } elseif (Test-Path $logPath2) {
        $chunks += "=== FILE: $logName ===`n$(Get-Content $logPath2 -Raw -Encoding UTF8)`n"
    }
}

# 5. 压缩归档摘要（如果有）
$archiveDir = Join-Path $assetDir "压缩归档"
if (Test-Path $archiveDir) {
    $archives = Get-ChildItem $archiveDir -File | Where-Object { $supportedExt -contains $_.Extension }
    foreach ($f in $archives) {
        $chunks += "=== ARCHIVE: $($f.Name) ===`n$(Get-Content $f.FullName -Raw -Encoding UTF8)`n"
    }
}

# 输出完整上下文
$fullContext = $chunks -join "`n"
Write-Output $fullContext
Write-Output "`n=== 总计: $($chunks.Count) 个文件, $($fullContext.Length) 字符 ==="
```

执行规则：
- **每次写新章节前必须执行**。不允许"我上一轮已经读过了"作为跳过理由——对话历史里的摘要不等于全文。
- 如果项目目录为空或只有 README，跳过加载，直接进入写作。
- 如果总字符数超过 10 万，只加载：文风锚定全文 + 设定库/人物库/剧情线全文 + seed/燃料文件全文 + 最近 3 章正文全文 + 最近涌现日志全文 + 压缩归档摘要。文风锚定始终加载，不裁剪。

### Research 燃料消费

write 前必须确认 research 燃料是否就绪：

- 如果项目 `涌现/research-写作燃料.md` 存在且内容有效，直接消费。
- 如果不存在或过期（距上次 research 超过 5 章），提示 pop-emergent 先执行 research。
- 跨世界观同人、涉及真实事件/技术、新项目第一轮——这三种情况 research 是强制的。
- 用户说"直接写"时可以跳过 research，但 write 的 execution.mode 只能为 `trial`。

### 文风DNA消费

write 前必须确认文风DNA是否就绪：

- 如果项目 `涌现/文风锚定.md` 存在，全文加载协议已自动加载。涌现写作包的 `文风锚定` 字段必须填写。
- 如果不存在，提示 pop-emergent 执行文风DNA部署协议（从 library 库选择匹配的 DNA 文件部署到项目本地）。
- 用户说"不要文风"时可以跳过，但 write 的 execution.mode 只能为 `trial`。

**文风锚定字段填写规则**：
1. 在加载的文风锚定文件中，找到和本章场景最匹配的场景卡（如战斗场景找`combat_*`卡，对话场景找`dialogue_*`卡）。
2. 填写：场景卡名 + 一句话观察（从DNA的观察段提取，不贴原文）。
3. 写正文时参照该场景卡的原文笔触：句式节奏、感官顺序、叙事距离、对话方式。不是模仿内容，是感受笔触密度。

## 正文锚定切片

读取锚定正文后，只提炼活审美上下文：

```text
本项目什么算爽：
本项目什么会漂：
主角主动方式：
世界观折射方式：
压迫/位阶表达：
句子与节奏：
本次必须继承：
```

如果有文风锚定文件，这里是感受笔触密度和节奏的参考——不是模仿内容，是参照句式节奏、感官顺序、叙事距离和对话方式。如果没有文风锚定文件，至少防止新文本漂成行业评论、严肃文学、普通科技新闻或另一本书。

## 涌现写作包

写前组一个输入包，作为正文施工卡的轻量替代：

```markdown
## 涌现写作包
execution.mode: formal|draft|trial
- 把 X 写成 Y：
- seed 承诺：
- research 主燃料：
- 正文锚定：
- 文风锚定：{场景卡名} - {一句话观察}
- 当前状态：
- 场景边界：本次只写到哪里；不提前吞并什么
- 主角主动动作：
- 主爽点：
- 可见反馈/收益/损失：
- 世界观折射：
- 禁区：
```

## 正文规则

- 开场 120 字内出现目标、异常、压力、反馈或主动动作之一。
- 主角至少完成一次动作闭环：压力/诱因 -> 判断 -> 主动动作 -> 阻碍升级 -> 可见反馈 -> 收益/损失 -> 新压力。
- research 燃料必须落到动作、物件、制度、职位、权限、技术细节或神性变化里。
- 关键爽点必须外显：旁人反应、敌人误判、身份变化、资源到账、能力反馈、局势翻转至少一种。
- 氛围段必须短，写完立刻回到目标、行动、风险或收益。
- 如果是续写，优先接住锚定正文的最后动作、危险或疑问。
- 结尾必须是主动钩子或威胁逼近，不是自然停顿。

## 正文落盘规则

正文写入 txt 文件，对话回复只给摘要+钩子——防止正文全文吃满上下文窗口，导致后续章节质量断崖。

### 文件命名

```
{书名}-第{N}章-{标题}.txt
```

### 落盘流程

1. 正文写完后，写入项目目录下的 txt 文件。
2. 文件写入成功后，在对话回复中给出摘要（3-5 行）+章末钩子（1-2 行）。
3. 然后执行涌现沉淀（更新 `涌现/review-沉淀.md` 或 `涌现日志.md`）。

### 对话回复格式

```markdown
**第 N 章 - {标题}** 已写入 `{文件名}`

**摘要**：{3-5 行剧情摘要}

**章末钩子**：{1-2 行，主角下一步要做什么或威胁逼到哪}

---

## 创作记录
- execution.mode:
- 已读锚定：
- seed 承诺：
- research 采用：
- 主爽点兑现：
- 新增/变更设定风险：
- 下一段衔接：
```

禁止在对话回复中放正文全文。正文全文只存在于 txt 文件中。

只有用户明确要求纳入正式项目时，才保存到正式 `正文/`；否则保存到 `试写/` 或用户指定位置。

## 红线

- 不调用 `pop-writer-v3-create`。
- 不读正文锚定就续写已有项目；没有锚定只能标 `trial`。
- 不把 research 燃料写成背景说明，必须入场面。
- 不把下一章核心事件顺手吞并。
- **正文必须落盘到 txt 文件**：对话回复只给摘要+钩子，禁止把正文全文放进对话回复。违反此条会导致后续章节上下文被正文吃满。
- **禁止凭残缺记忆写作**：写章节前必须执行项目文件全文加载协议。不允许"我之前读过"作为跳过理由。
- **禁止单章无限重写**：同一章重写超过 2 次后，标记为"试写-独立"不再阻塞递进。无限重写会进入劣化循环——每轮推翻重来但不积累内容深度。
