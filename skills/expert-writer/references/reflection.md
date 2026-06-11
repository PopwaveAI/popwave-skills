# reflection.md — 四层递进审视

> 适用时机：任何子 skill 执行完成后，审视产出。不分场景，所有路由返回后执行一次。
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

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

| 优先级 | 含义 | 行动 |
|:------|:-----|:------|
| P0 | 不改会出大问题 | 立刻退回，通知用户 |
| P1 | 影响后续写作质量 | 建议用户修，但不强制 |
| P2 | 可以放着，以后再说 | 记录到项目状态文件里 |

---

## L1 ─ 产出基础检查 + 索引回写 + 状态协议校验

```
□ 产出物文件是否在正确位置？
□ 文件名格式合规？
□ 越界写入 → 移至正确位置
□ **索引回写（写 workspace-index.yaml）**：
  - 新产出文件 → 注册到 file_registry[项目].active（含 type/version）
  - 版本变更 → 旧版本移至 deprecated，填写 replaced_by
  - 依赖关系 → 填写 depends_on 字段
□ **运行时状态更新**：
  - runtime.last_session → 更新为 {项目, 任务, 完成状态, 时间戳}
  - 本轮触发的新经验教训 → 追加到 cross_project_lessons
□ **项目状态更新**（如有变化）：
  - projects[].current_chapter / current_act 按实际情况更新
  - 如果有副本章节（v1/v2/v3）→ 标记各版本的 status
  - pre_read_status.verified → 本轮若执行了精读流程，设为 true
□ **★ 项目首次配置完备化（NEW v2.7 — 项目启动时执行一次）**：
  - 触发时机：bookstrap Phase 3 产出 project.yaml 后（项目具备独立身份）
  - 检查 requirements[{项目}] 是否已存在：
    - 不存在 → 创建空列表，仅含一条初始条目
    - 已存在 → 跳过（只初始化一次）
  - 检查 change_log[{项目}] 是否已存在：
    - 不存在 → 创建初始记录
    - 已存在 → 跳过
  - 检查 file_registry[{项目}] 是否已存在：
    - 不存在 → 注册 project.yaml + 角色卡 到 confirmed
□ **状态协议校验**：
  - entity-snapshot.yaml 是否存在？→ 不存在则 WARN
  - entity-snapshot._meta.total_chapters == ch*.md 文件数？→ 不等则 P0 警告
  - entity-snapshot.protagonist.status 与最新章 delta 一致？→ 不一致则 P1
  - （详细规则见 §状态协议专项检查）
□ **文件加载完整性检查**：
  - 回顾本轮 conversation 中是否用 `Get-Content -Encoding UTF8 -Raw` 加载过子 skill 的文档型文件
  - 如果没有但本轮任务涉及写正文/修改设定等需要子 skill 指令的操作 → P2 警告
□ **管线进度更新**：
  - 子 skill 完成最后一 phase 后 → 回写 workspace-index.yaml#progress
□ **★ 变更日志回写（v2.7）**：
  - 每次子 skill 执行完成后追加 workspace-index.yaml#change_log 记录
  - 格式：id/at/skill/type/summary
  - 不追加重复条目
□ **★ 需求状态更新（v2.7）**：
  - pending 需求被本轮解决 → status="implemented"
  - 用户追加新需求 → 追加 requirements 条目
```

## L2 ─ 一致性检查

```
□ 产出与上游设定/幕纲一致？
  - chapter-design 设计包事件链是否符合 act-XX.yaml 幕纲字段约束？
  - bookstrap L1 设定是否和 story-engine.yaml 的 core_premise 一致？
□ entity-snapshot ↔ 角色卡一致性？
  - entity-snapshot 中角色状态是否与角色卡快照一致？
  - 参考 pipeline-arch.md§三 的校验对应表检查各字段
  - 例：角色卡说"主角在 Act 1 结束时不超过 3阶"，entity-snapshot 显示 4阶 → P1
□ 文件完整性 vs 管线阶段？
  - 参考 pipeline-arch.md§三「pipeline 阶段 → 应有文件」速查表检查缺失
  - 如果状态/目录为空 → WARN（角色卡未产出）
□ 如果有偏离 → 记录偏离项和严重程度，返回用户判断
```

> 详细文件分类/消费矩阵/路径规范见 `pipeline-arch.md`。

## L3 ─ 质量检查（QA 报告判断）

```
□ 如果子 skill 是 prose-render → 过 pop-novel-qa 质检
□ 读取 QA 报告结论：
  - "想跳过"≥2 或 "会弃书" → 标记 P0，退回 prose-render 重写
  - 无红线 → 通过
```

## L4 ─ 活人感检查（可选，高优章节启用）

```
读一段产出正文，判断：
□ 读起来像人在讲故事，还是 AI 在汇报剧情？
□ 有没有"他感到/他仿佛/他意识到"等 AI 观感词？
□ 有没有"首先其次""总结来说"等套话句式？
□ 对话听起来像真人在说话，还是像角色在念设定？

不通过 → 标注问题段落，退回 prose-render 局部重写。
```

---

## 状态协议专项检查（v2 — Writer 执行后强制）

### Delta→全量快照一致性校验

```
□ entity-snapshot.yaml 是否存在？
   → 不存在：WARN

□ 章文件数量 vs entity-snapshot._meta.total_chapters 是否一致？
   → 不一致：P0

□ entity-snapshot.protagonist.status 是否与最新章 delta 一致？
   → 不一致：P1

□ entity-snapshot 中各角色的 key_items 合并是否去重完整？
   → 有重复：P2
```

### 角色卡 一致性校验

```
□ 索伦状态是否与角色卡快照一致？
   → 不一致：P1

□ entity-snapshot 中任意角色 status=死亡 是否符合角色卡或 plot 的规划？
   → 意外死亡：P0 — 退回 writer 确认。
```
