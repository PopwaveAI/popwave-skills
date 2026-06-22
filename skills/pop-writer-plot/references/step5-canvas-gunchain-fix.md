# step5-canvas-gunchain-fix

> 修正背景：pop-writer-plot v7.2.0 → v7.3.0
> 触发：用户追问"契诃夫枪链在最后一步是否合理"

## 问题

6 步流程中，Step 3（剧情线成文）产出枪链，但 Step 5（Canvas 设计）完全忽略枪链，到 Step 6 才对照——此时 Canvas 已设计完成，枪链回收窗口经常找不到可用 payoff 章，导致退回 Step 5 重做。

```
Step 3: 枪链出炉 ✓
Step 5: Canvas 盲排 ✗  ← 不知道枪点在哪
Step 6: 对照 → 对不上 → 退回 Step 5  ← 恶性循环
```

## 修正

Step 5 的"做什么"新增第 2-3 条：
- 从剧情线提取枪点清单
- Canvas 中枪点回收章预留 ≥ 中 payoff，同章枪点回收 ≤ 2 个

Step 6 角色从"设计+对照"退化为"纯验证"：
- 主线无枪链 → 退回 Step 3（剧情线漏了）
- 枪点无回收窗口 → 退回 Step 5（Canvas 漏了）
- 无此两类问题 → 验证通过，不阻塞

## 信息流变化

```
修正前：Step3 枪链 → Step5 Canvas（盲） → Step6 对照（补救）
修正后：Step3 枪链 → Step5 Canvas（含枪链输入）→ Step6 验证（安全网）
```

Canvas 设计和枪链部署变回同一屏决策，Step 6 只抓漏网之鱼。
