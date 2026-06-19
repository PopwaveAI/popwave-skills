# 管线架构设计说明（项目B事故教训）

> 为什么不继续用 SKILL.md 里的 `upstream/downstream` 声明来推导管线顺序？

## 事故复盘

**6.18项目B** 中 Agent 跳过了 reservoir 阶段（creative 完成后直接进了 world），导致：
- reservoir 的剧情储备卡在 world 阶段不可用
- 直到用户追问才发现 pipeline 断裂
- 事后补 reservoir 注入（错过了 world 阶段的消费窗口）

## 三个直接原因

1. **world SKILL.md 声明 `upstream: [pop-writer-creative]`** — 技术上说没错（creative 确实是 world 的上游产出者），但缺少 reservoir 这个中间节点。Agent 读到此声明后认为 creative→world 是正确顺序。
2. **reservoir SKILL.md 声明 `downstream: [pop-writer-plot]`** — 没有声明自己和 world 的先后关系。可以被解读为 creative→reservoir→plot（与 world 并列）。
3. **Agent 读 expert-writer SKILL.md 时只读了前 10 行** — 管线全景图（`creative → reservoir → world → plot...`）在第 12 行以后，没读到。

## 根本原因

**管线顺序的定义权分散在各个 SKILL.md 的 pipeline 字段里，每个 skill 只声明自己的邻居关系，不声明全链路顺序。** 三个 skill 的声明拼起来是一幅矛盾/不完整的图：

```
pipeline-manifest 说：  creative → reservoir → world → plot
world 说：               creative → world                  (跳 reservoir)
reservoir 说：           creative → reservoir → plot       (跳 world)
```

Agent 无论读哪个 skill 的声明，都得不出完整顺序。

## 修复方案：管线合同 + 项目总控

### 管线合同（pipeline-manifest.md）

- 放在 `expert-writer/references/` 下，系统级只读
- 硬编码管线顺序 `creative → reservoir → world → plot → chapter → prose → qa`
- 每个阶段标注 skill 名、核心产出、前置条件、闸门
- **管线顺序不由任何 SKILL.md 的 upstream/downstream 字段推导**

### 项目总控（项目根目录的 `项目总控.md`）

- 新项目初始化时从 `references/project-master-control.tpl.md` 复制
- 人机共读：管线进度条（`[creative] ✅ → [reservoir] ⬜`）、硬约束索引、关键产出索引
- Agent 每个阶段完成后自动更新
- 管线断裂检测：比对 `completed_stages` 在 pipeline-manifest 顺序上是否连续

### 截断检测协议

- 所有文件读取后强制校验：`content.length vs (Get-Item).Length`
- 字符数 < 文件大小 × 0.9 → ⚠️ 截断警告 → 回退 `Get-Content -Raw` 重读
- 连续 2 次不通过 → 终止，告知用户

## 设计原则

1. **管线顺序是系统层的硬契约**，不是各 skill 的自我声明
2. **进度状态是项目层的可变数据**，存于项目根目录（人机共读）
3. **截断检测是读文件的必修流程**，不依赖特定工具的正确性
4. **Agent 首次加载时的第一动作是锚定位置**，不是直接执行路由
