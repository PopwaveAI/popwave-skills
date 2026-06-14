# pop-decon-engine · 管线上下文

## 在拆书管线中的位置

```
Phase 1          Phase 2           Phase 3           Phase 4          Phase 5
事实提取  ──→  聚类卷幕  ──→  归纳世界观   ──→ 归纳故事引擎 ──→  验证打包
pop-decon-extract    pop-decon-cluster    pop-decon-world    pop-decon-engine  pop-decon-validate
                                             ↑                    ↑
                                        upstream           you are here
```

## 消费说明

| 产出 | 谁消费 | 消费目的 |
|:-----|:-------|:---------|
| 故事引擎.md | pop-decon-validate | Phase 5 可回源性审计 / 跨 Phase 一致性检查 |
| 故事引擎.md | 写作端 creative | 项目启动包核心（Phase 0 故事引擎） |

## 级别映射

| 级别 | 是否执行 | 说明 |
|:-----|:---------|:-----|
| 前N章 | 否 | 前 20 章不归纳故事引擎 |
| 前N章 | 否 | 前 100 章不足以回答"这书是什么" |
| 全书 | 是 | 全书完成后从全部数据中归纳 |
