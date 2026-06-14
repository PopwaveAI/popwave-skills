# step-2-execute.md — 加载子 Skill + 执行 + 修改路由

> **读什么**：目标子 skill SKILL.md + steps/ + templates/ + 项目 YAML + styles/
> **产出什么**：子 Skill 执行结果
> **闸门**：决策点闸门（bookstrap/plot/chapter-design/prose-render — 必须用户确认）

---

## 1. 强制加载（不可跳过）

```
Get-Content -Encoding UTF8 -Raw 子 skill SKILL.md → 验证完整
Get-Content -Encoding UTF8 -Raw steps/*.md, templates/*.md
Get-Content -Encoding UTF8 -Raw 项目 YAML (project/entity-snapshot/act-XX)
Get-Content -Encoding UTF8 -Raw styles/*
```

**动态融合**：用户追加核心设定且当前在 L1 阶段 → 加载 `references/dynamic-fusion.md`

**❌ WRONG**：
```
agent 凭记忆判断子 skill 内容 → 跳过 Get-Content → 版本不一致产出格式不匹配
✅ CORRECT：每次都 Get-Content 最新版本

entity-snapshot 最后更新 ch05，用户要写 ch08 → agent 基于 ch05 续写 → 角色状态脱节
✅ CORRECT：检查快照章号 vs 目标章号 → 脱节则提示用户
```

---

## 2. 决策点闸门（方案选择协议）

| 子 skill | 确认方式 |
|:---------|:---------|
| bookstrap | 方案A：当前设定 / 方案B：调整方向 / 4. 我重新来 |
| plot | 方案A：当前卷+幕 / 方案B：调整某卷 / 4. 我重新来 |
| chapter-design | 方案A：当前骨架 / 方案B：调整某事件 / 4. 我重新来 |
| prose-render | 方案A：当前渲染 / 方案B：调整某段 / 4. 我重新来 |

每个方案说明适用情况、优点、风险。跳过闸门 = 违规。

---

## 3. 按子 skill 的 SOP 执行

按子 skill 的分步指令执行。执行过程中保持文件写入落地，不在对话中输出完整内容。

**纪律**：
- 先问修改 → 再建议下一步 → 不催促
- QA 后只问修改
- 中文。不暴露内部 skill 名。

---

## 4. 修改路由

> 定位修改层 → 评估连锁影响 → 逐层执行

| 改什么 | 联动什么 |
|:-------|:---------|
| 修辞/措辞 | — |
| 人物性格/关系 | bookstrap（角色设定） |
| 剧情走向 | plot + prose-render |
| 世界观规则 | bookstrap → chapter-design → prose-render |
| 起点/终点状态 | bookstrap → plot → chapter-design → prose-render |

**铁律**：改设定 ≠ 重写全书。只动直接受影响的。

---

## 5. 异常与边界条件

| 场景 | 触发条件 | 动作 |
|:-----|:---------|:-----|
| 子 skill 文档读取 | 每次路由 | 统一 `Get-Content -Encoding UTF8 -Raw`。>25K 回退 Read+offset |
| SKILL.md 找不到 | 文件不存在 | 终止 + `❌ SKILL.md 不存在` |
| 子 agent 不可用 | 环境不支持 | 声明 `⚠️ master 手动执行` 在前 |
| 执行失败 | 任意异常 | 通知用户 + 原因 + 可操作建议 |
| 前置条件缺失 | 上游产物不存在 | 告知缺什么，建议调用前置 skill |
| 无法匹配路由 | 用户消息无匹配 | 回到 Think 追问补全信息 |
| 用户要跳步 | 用户明确表示 | 说清代价，给两个选项。确认后立即切换 |
| 未加载子 skill | agent 跳过加载 | 必须先加载再执行。跳过 = 退回 |
| 越界检测 | 当前阶段出现下一阶段内容 | 说"这属于 [X] 的范围，到那一步处理。先完成当前阶段。" |
