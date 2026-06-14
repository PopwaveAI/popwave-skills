# pop-decon-world · 管线上下文

## 在拆书管线中的位置

```
Phase 1          Phase 2           Phase 3           Phase 4          Phase 5
事实提取  ──→  聚类卷幕  ──→  归纳世界观   ──→ 归纳故事引擎 ──→  验证打包
pop-decon-extract                pop-decon-world     pop-decon-engine  pop-decon-validate
                    ↑                    ↑                    ↑
               upstream           you are here           downstream
```

## 消费说明

| 产出 | 谁消费 | 消费目的 |
|:-----|:-------|:---------|
| L1-01~06 六件套 | pop-decon-engine | 故事引擎「世界锚点」「宪法」段的归纳原料 |
| 世界宪法.md | pop-decon-engine | 故事引擎「绝对不能做的事」段的原料 |
| combat_capability.yaml | pop-decon-validate | 跨 Phase 一致性检查（vs 角色卡等级路径） |
| 起点/终点快照 | pop-decon-validate + 写作端 | 跨 Phase 一致性检查 + 项目启动包 |

## 级别映射

| 级别 | 覆盖步骤 | 产出范围 |
|:-----|:---------|:---------|
| Lv2 | Step 1-8 | L1 六件套 + 世界宪法 + 数值体系 + 起点快照 |
| Lv3 | Step 1-9 | Lv2 + 终点快照 + L1 六件套全书增补版 |
