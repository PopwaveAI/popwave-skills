# 典型错误防范（调度层）

> 只列 expert-writer 调度层面的错误。子 skill 内部的错误由各子 skill 自管。

---

## 错误 1：不读子 SKILL.md 就路由

```
❌ WRONG: 用户说"写正文"→ 直接跳到 pop-writer-prose，不读 prose 的 SKILL.md
✅ CORRECT: 先 Get-Content -Encoding UTF8 -Raw 加载 prose/SKILL.md 全文，再按其 SOP 执行
```

## 错误 2：用 Read 工具读取 skill 文件被截断

```
❌ WRONG: 用 Read 工具读 SKILL.md，文件超过 2000 行被截断
✅ CORRECT: 用 skill_view 或 Get-Content -Encoding UTF8 -Raw，读取后做截断检测
```

## 错误 3：决策点跳过用户确认

```
❌ WRONG: creative 闸门未等用户确认就继续推进到 reservoir
✅ CORRECT: 4 个闸门（creative/plot/chapter/prose）必须等待用户点头
```

## 错误 4：管线跳步

```
❌ WRONG: creative 完成后直接跳到 world，跳过 reservoir
✅ CORRECT: creative → reservoir → world → character → plot → chapter → prose → qa，硬性不可跳跃
```

## 错误 5：长文全量贴入对话

```
❌ WRONG: 写完 3000 字正文后全量贴入对话窗口
✅ CORRECT: 文件写入后对话只留摘要（≤200字）+ 文件路径
```

## 错误 6：不更新项目总控.md

```
❌ WRONG: 阶段完成后不更新项目总控的进度条和产出物清单
✅ CORRECT: 每次阶段完成后更新项目总控.md 的 current_stage + 产出物状态 + 执行顺序日志
```

## 错误 7：引导语不基于项目实际状态

```
❌ WRONG: Reflect 末尾给固定模板引导语，不检查项目实际进度
✅ CORRECT: 读项目总控.md + entity-snapshot，基于实际状态给引导
```

## 错误 8：expert-writer 自己做详细质检

```
❌ WRONG: prose 产出后 expert-writer 自己做 L1-L4 详细检查
✅ CORRECT: expert-writer 只做通用三问，详细质检退回 pop-writer-qa
```
