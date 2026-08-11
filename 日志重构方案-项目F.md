# 项目日志整体重构方案

> 针对 `C:\Users\AWMPRO\.paopao\projects\7-20-项目f` 的日志结构重构
> 目标：让 agent 排查时少读、按需读、不重复读，避免 token 浪费和认知负担

---

## 一、现状盘点（已实测）

### 1.1 目录全貌

| 目录 | 数量 | 体积 | 作用 |
|------|------|------|------|
| `runs/` | 12 个 run 目录（42 文件） | 3.4MB | 每次 agent 运行的输入 / 事件 / 输出 |
| `conversations/` | 7 个 jsonl + index.json | 2.31MB | 会话完整消息流 + 会话索引 |
| `artifacts/` | 12 个 json | 2.45MB | 每个 run 的"生成结果快照"，含完整模型轨迹 |
| `skills/` | 2 个 json | 0.02MB | skill 版本与注册信息 |
| `project.json` | 1 | 极小 | 项目元数据 |

### 1.2 runs 与 conversations 的真实归属（已逐 run 解析）

共 **12 个 run，分属 7 个会话**。主会话 `8bdefc98`（我要写本网文）独占 6 个 run，其余 6 个 run 分属 6 个分支会话：

| runId(前8) | 所属会话 | 会话标题 | 父子关系 |
|---|---|---|---|
| 95205ad2 | 8bdefc98 | 我要写本网文（主） | 根 |
| 910000e3 | 8bdefc98 | 同上 | 根 |
| 8bade404 | 8bdefc98 | 同上 | 根（**派生 5 个子 agent**） |
| fab1c263 | 8bdefc98 | 同上 | 根（派生 1 个子 agent） |
| c2287e66 | 8bdefc98 | 同上 | 根 |
| 9fdf54d6 | 8bdefc98 | 同上 | 根 |
| 9651b131 | 255012e0 | 下载参考书 | 8bade404 的子 agent |
| 4aa199fd | 2a894e0d | 赛道定位调研 | 8bade404 的子 agent |
| d7e96ba7 | 12b54486 | decon-lite拆书 | 8bade404 的子 agent |
| 62661e9a | db5e28fe | 笔触DNA提取 | 8bade404 的子 agent |
| 9d0ae4d3 | 555a90e3 | 双轨发散 | 8bade404 的子 agent |
| 46dc428e | 5193a1bf | plot-阴阳事务所 | fab1c263 的子 agent |

> 关键结构：主会话的一个 run（如 `8bade404`）派生了 5 个子 agent，每个子 agent 既是 `runs/8bade404/subagents/*/result.json`，又是一个独立的 `runs/{子agentId}/` 目录。

### 1.3 单文件内容构成（已抽查）

| 文件 | 大小 | 冗余度 |
|---|---|---|
| `runs/*/input.json` | 84~93KB | **极高**：只为拿 conversationId/model/instruction，却内嵌了完整注入历史 |
| `runs/*/events.jsonl` | 9~797KB | 高：一条响应含完整 thinking/tool-call/tool-result |
| `runs/*/response.md` | 0~65KB，多数 0~2KB | 低，多为空壳或一行摘要 |
| `conversations/*.jsonl` | 大 | **权威源**：含用户/助手消息 + 每个 run 的完整模型轨迹 + file-change 记录 |
| `artifacts/*.json` | 大 | **与 conversations.jsonl 重复存储**同一份模型轨迹 |
| `runs/*/subagents/*/result.json` | 中等 | **与独立 run 目录重复存储**子 agent 结果 |

---

## 二、核心问题诊断

### P1. runs 不按会话归类（老板已指出）
排查时 12 个 run 平铺在 `runs/` 下，无法一眼看出"这是哪个会话、哪个阶段、哪个父 agent 派生的"。必须逐个打开 `input.json` 才能拿到 conversationId → 一次排查读 6 个 90KB 的 input.json = **浪费 ~540KB token**。

### P2. input.json 结构性臃肿
90KB 的 input.json 里，真正用于定位的只有 `conversationId / model / instruction / skillNames / createdAt / outputKind` 这 6 个字段。其余是 injected history（供 agent 续写用），**排查时完全不需要**，但被一并读入。

### P3. 三重数据冗余
1. **artifacts vs conversations.jsonl**：同一份模型轨迹（thinking/tool-call/tool-result）在两个地方各存一遍，2.45MB 纯重复。
2. **subagents/result.json vs 独立 run 目录**：子 agent 结果在父 run 下和各 run 目录下各存一遍。
3. **events.jsonl vs conversations.jsonl**：run 级事件与会话级消息流高度重叠。

### P4. 缺少索引层
没有一张"run → 会话 → 阶段 → 状态(成功/失败/超时) → 大小"的元数据表。所有关联关系都要靠读文件才能还原，这是排查 token 浪费的根源。

---

## 三、重构目标

1. **秒级定位**：一眼看到"这个 run 属于谁、什么阶段、成没成功"，不用读文件。
2. **按需读取**：元数据（小）与轨迹（大）分离，排查先读元数据，需要细节才读轨迹。
3. **零重复**：同一份数据只存一份，其他位置用引用指针。
4. **向后兼容**：不破坏现有运行时（popwave/OpenClaw）的读写路径。

---

## 四、重构方案

### 4.1 目录结构（目标态）

```
7-20-项目f/
├── project.json                    # 不变
├── runs/                           # 物理存储不变（运行时兼容），但改为纯净数据
│   ├── {runId}/events.jsonl        # 权威轨迹源（唯一保留的完整轨迹）
│   ├── {runId}/input.json          # 瘦身：只留元数据，历史注入挪走
│   └── {runId}/response.md         # 不变
├── conversations/                  # 不变（消息流权威源）
├── artifacts/                      # 重构为"用户可见产物"，不再存模型轨迹
├── skills/                         # 不变
├── _index/
│   ├── runs.json                   # 【新增】run 元数据索引（关键）
│   ├── conversations.json          # 【新增】会话→run 关系扁平表
│   └── artifacts.json              # 【新增】产物→run 映射
└── _archive/                       # 【新增】已压缩/已归档的旧日志
```

### 4.2 核心动作

#### A. 新增 `_index/runs.json` 元数据索引（解决 P1+P4）

每次 run 结束时，写一行轻量元数据（约 200 字节），排查时**只读这一个文件**：

```json
{
  "runs": [
    {
      "id": "8bade404-3ecf-4679-8ff4-692ae4479561",
      "conversationId": "8bdefc98-5fd4-4476-aefe-0fb8398eef6d",
      "conversationTitle": "我要写本网文",
      "parentConversationId": null,
      "parentRunId": null,
      "kind": "root",
      "pipeline": "pop-fanqie-pipeline",
      "stage": "phase0-intent",
      "skillNames": ["pop-fanqie-pipeline"],
      "model": "popwave/writing-standard",
      "status": "success",            // success | error | timeout | aborted
      "errorTypes": ["edit_mismatch"],// 报错类型标签
      "createdAt": "2026-07-20T12:25:37Z",
      "durationMs": 20963,
      "inputSizeKB": 85,
      "eventsSizeKB": 236,
      "subagentIds": ["4aa199fd","62661e9a","9651b131","9d0ae4d3","d7e96ba7"],
      "hasArtifact": true
    }
  ]
}
```

**排查收益**：以前定位一个报错要读 6 个 90KB input.json；现在读一个 10KB 索引即可筛出所有 timeout/edit_mismatch run，再按需点进具体 run。

#### B. input.json 瘦身（解决 P2）

把 `input.json` 拆成两层：
- `input.json`：只保留 6 个定位字段（conversationId/model/instruction/skillNames/createdAt/outputKind），约 2KB。
- `input.history.json`： injected history 单独存放，**排查时默认不读**，仅 agent 续写 / 深度复现时才按需读取。

或者更简单：给 input 加一个 `meta.json` 旁路，保留大 input 不动但索引只读 meta。

#### C. 去重 artifacts（解决 P3a）

`artifacts/*.json` 目前存的是"Agent 生成结果"（含完整模型轨迹），与 conversations.jsonl 完全重复。重构为：
- **保留**：`titlet / kind / runId` 等元信息 + 用户可见的最终产物文本。
- **删除**：内嵌的 `events`（model-trace）数组，改为 `traceRef: "conversations/{convId}.jsonl"` 指针。
- 结果：2.45MB → 几十 KB，且不丢任何信息。

#### D. 去重 subagents（解决 P3b）

子 agent 结果只保留一份：
- **权威源**：保持独立 `runs/{子agentId}/` 目录（含 input/events/response）。
- **父 run 下**：`subagents/*/result.json` 瘦身为 200 字节指针 `{"runId":"...","convId":"...","summary":"..."}`，不再复制完整 summary+details。
- 排查"主会话派生了哪些子 agent"看 `_index/runs.json` 的 `subagentIds` 即可。

#### E. 会话平铺视图（可选，针对老板需求 1）

在不搬动物理文件的前提下，提供 `_index/conversations.json` 作为"以会话为第一视角"的排查入口：

```
会话: 我要写本网文 (8bdefc98)  — 6 runs
 ├─ 95205ad2  phase0-intent    success   (input85K/event84K)
 ├─ 910000e3  phase0-intent    error      (memory_index)
 ├─ 8bade404  phase0-research  success    → 派生 5 个子agent
 │    ├─ 9651b131  下载参考书
 │    ├─ 4aa199fd  赛道调研
 │    ├─ d7e96ba7  拆书
 │    ├─ 62661e9a  DNA提取
 │    └─ 9d0ae4d3  双轨发散
 ├─ fab1c263  phase1-seed      success    → 派生 1 个子agent
 │    └─ 46dc428e  plot世界构筑
 ├─ c2287e66  ...
 └─ 9fdf54d6  ...
```

---

## 五、落地步骤（分层推进，不阻塞运行时）

| 步骤 | 内容 | 优先级 | 风险 |
|------|------|--------|------|
| S1 | 写一个 `build_index.ps1` 脚本，扫描现有 runs 目录，生成 `_index/runs.json` + `_index/conversations.json` | P0 | 低，纯读 |
| S2 | 运行时在 run 结束时追加一条索引（hook 到 openclaw worker 的 completed 事件） | P0 | 中，需改 worker |
| S3 | input.json 瘦身 / meta 旁路 | P1 | 中，需改 worker |
| S4 | artifacts 去重改为指针 | P1 | 中 |
| S5 | subagents/result.json 瘦身为指针 | P2 | 低 |
| S6 | 旧数据一次性迁移（跑迁移脚本） | P2 | 低 |

---

## 六、红线

1. **不破坏运行时读写路径**——`runs/{runId}/input.json + events.jsonl + response.md` 是 OpenClaw 的协议，物理位置和文件名不能改，只能瘦身/加旁路，不能删除。
2. **索引只增不改**——`_index/runs.json` 只能追加，不能覆盖，避免并发 run 互相覆盖。
3. **去重必须保留 traceRef 指针**——删 artifacts 的 events 前必须确认 conversations.jsonl 里能找到对应轨迹，否则丢数据。
4. **子 agent 结果以独立 run 目录为权威**——父 run 下的 result.json 只做摘要指针，不复制完整内容。

---

## 七、排查效率对比（重构前后）

| 场景 | 重构前 | 重构后 |
|------|--------|--------|
| 定位"哪个 run 超时" | 读 12 个 input.json(~1MB) | 读 `_index/runs.json`(10KB) |
| 看某会话的所有 run | 逐个读 input.json 反查会话 | 读 `_index/conversations.json` |
| 复现某 run 轨迹 | 读 input(90K)+events(200K) | 读 index 定位 + 按需读 events |
| 查产物归属 | 猜 runId 再查 | 读 `_index/artifacts.json` |
| **token 消耗** | ~1.2MB | ~30KB（**省 97%**） |