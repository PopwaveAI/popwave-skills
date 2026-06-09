# reflection.md — 通用反思检查

> 适用时机：任何子 skill 执行完成后，审视产出。
> 不分场景，所有路由返回后执行一次。

---

## 通用检查三问

| # | 问 | 检查方式 |
|:-:|:---|:---------|
| 1 | **产出回答了用户问的问题吗？** | 对比用户原始需求和产出结果 |
| 2 | **有没有超出 scope 的多余产出？** | 用户没要求的东西写多了 = 浪费 |
| 3 | **有没有明显的盲点被忽略？** | "看起来对但站不住"的结论 |

## 质量信号

| 信号 | 行动 |
|:-----|:-----|
| 执行结果完美覆盖需求 | 直接交付，一句话总结 |
| 执行结果覆盖大部分但小细节偏了 | 标记偏差，再问用户是否接受 |
| 执行结果偏了但 agent 认为做完了 | **人工检查**：是不是 agent 偷懒了？ |
| 执行结果和需求南辕北辙 | **不退**——复盘：路由错了还是指令理解错了？ |

## 风险标记规则

发现盲点后，按优先级标记：

| 优先级 | 含义 | 行动 |
|:------|:-----|:------|
| P0 | 不改会出大问题 | 立刻退回，通知用户 |
| P1 | 影响后续写作质量 | 建议用户修，但不强制 |
| P2 | 可以放着，以后再说 | 记录到项目状态文件里 |

---

## 状态协议专项检查（v2 — Writer 执行后强制）

> 如果当前任务涉及 Writer（正文写作），在通用检查后追加此节。

### Delta→全量快照一致性校验

```
□ entity-snapshot.yaml 是否存在？
   → 不存在：WARN — "Writer 产出未生成 entity-snapshot.yaml。需执行聚合。"

□ 章文件数量 vs entity-snapshot._meta.total_chapters 是否一致？
   → 不一致：P0 — "章文件有 {N} 个，entity-snapshot 声称 {M} 章。快照过时或未正确聚合。"

□ entity-snapshot.protagonist.status 是否与最新章 delta 中的 protagonist 条目一致？
   → 不一致：P1 — "entity-snapshot 记录的主角状态与最新章末 delta 不匹配。可能未执行 Step 3.3 聚合。"

□ entity-snapshot 中各角色的 key_items 合并是否去重完整？
   → 有重复：P2 — 记录，不影响当前继续，但下次聚合时注意去重。

□ entity-snapshot.timeline 与最新章的 world_updates 是否一致？
   → 不一致：P1 — 时间线滞后于实际写作进度。"
```

### Constitution 一致性校验（新增）

```
□ entity-snapshot.protagonist.rank 是否在 constitution 允许的段位范围内？
   → 超出：P1 — 触发修正建议，不强制退回。

□ entity-snapshot 中任意角色 status=死亡 是否符合 constitution 或 plot 的规划？
   → 意外死亡：P0 — 退回 writer 确认。
```
