---
name: "tool-prd-builder"
version: "1.1.0"
description: "当用户说'写PRD/生成PRD/我要做一个产品/帮我做产品原型/做个交互Demo/把想法变成PRD'时启用。从产品概念出发，经需求澄清->结构化PRD->飞书同步->反馈迭代->单HTML交互Demo的全链路交付。"
pipeline:
  upstream: []
  downstream: []
---

# PRD Builder -- 从想法到 PRD 到交互 Demo v1.1.0

> 覆盖产品从概念到可演示原型的全流程：用户想法 -> 需求澄清 -> PRD(.md) -> 飞书文档 -> 反馈迭代 -> 单HTML交互Demo。

---

## 速查表：四个阶段与步骤文件

| 用户说什么 | 触发阶段 | 步骤文件 | 前置条件 |
|:-----------|:---------|:---------|:---------|
| "我想做个X产品" / "帮我写PRD" | Phase 1 -> Phase 2 | [steps/step-01-phase1-clarify.md](steps/step-01-phase1-clarify.md) -> [steps/step-02-phase2-prd.md](steps/step-02-phase2-prd.md) | 无 |
| "看看飞书上的反馈" / "处理飞书评论" | Phase 3 | [steps/step-03-phase3-feedback.md](steps/step-03-phase3-feedback.md) | 已有飞书文档 token |
| "生成Demo" / "做个原型" | Phase 4 | [steps/step-04-phase4-demo.md](steps/step-04-phase4-demo.md) | Phase 2 PRD 已确认 |
| "改一下PRD第X章" / "根据反馈修改" | Phase 3(模式A/B) | [steps/step-03-phase3-feedback.md](steps/step-03-phase3-feedback.md) | 已有 PRD 文档 |
| 快速路由总览 | -- | [steps/step-00-quick-ref.md](steps/step-00-quick-ref.md) | -- |

---

## 执行流程

按顺序执行 Phase 1 -> Phase 2 -> Phase 3 <-> Phase 2 (迭代) -> Phase 4。每一步的详细 SOP 见对应 `steps/` 文件。

```
Phase 1 (需求澄清) -> Phase 2 (PRD+飞书) -> Phase 3 (反馈) <-> Phase 2 (迭代)
                         |
                    Phase 4 (Demo)
```

---

## 红线

| # | 红线 | 说明 |
|:-:|:-----|:-----|
| 1 | 不动手写代码/PRD 前不问清需求 | 用户提 idea 必须走 Phase 1 需求澄清，至少问 3 个问题。不问就写 -> 退回 |
| 2 | 飞书同步单批 blocks >10 | 已验证批量 >10 块会报 1770006 -> 必须逐个追加 |
| 3 | Demo 的数据含虚构/编造信息 | Demo 中使用的数据应从网络搜索获取真实信息。全部虚构 -> 退回重做 |
| 4 | 跳过用户确认直接生成 Demo | 用户未确认 PRD 前不生成 Demo。强推 -> 退回 |
| 5 | PRD 少于 8 章 | 8 章是最小必要章节结构，缺章 -> 退回补充（第 3 章可跳过或改名） |
| 6 | Demo 非单文件 HTML | 最终交付必须是单文件 HTML（Chart.js 内联），多文件 -> 退回合并 |
| 7 | 飞书反馈汇总模式未展示评论就修改 | Phase 3 模式 A 必须先分类展示评论，等用户指示。跳过 -> 退回 |
| 8 | 自动处理模式将飞书评论 is_solved=true | Phase 3 模式 B 自动回复时保持 is_solved=false。设 true -> 退回 |
| 9 | Demo 详情页缺空值保护 | showPage()/goDetail() 必须有空值保护，缺 -> 退回补充 |

---

## Drop Check

> 每阶段完成后逐项勾检，确保无遗漏。

### Phase 1 Drop Check

```
□ 产品类型/领域已记录
□ 目标受众已确认
□ Demo 深度已选定（精简版 / 标准版 / 深度版）
□ 特殊功能要求已确认
□ 全部4问已完成（或 idea 已清晰可跳过）
```

### Phase 2 Drop Check

```
□ PRD.md 已生成（>= 8 章，第 3 章可跳过或改名）
□ 第 6 章包含页面路由图（ASCII）
□ 第 6 章包含页面线稿（ASCII 网格布局）
□ 第 6 章包含组件-状态矩阵
□ 飞书文档已创建
□ blocks 逐个追加（单批 <= 10）
□ 权限已设为 anyone_can_edit
□ 用户已确认 PRD 内容
```

### Phase 3 Drop Check

```
□ 模式已判定（A / B）
□ 模式 A：评论已拉取并分类展示
□ 模式 A：用户已逐条指示处理方式
□ 模式 B：is_solved 全部保持 false
□ 修改后的 PRD.md 已生成
□ 飞书文档已同步更新
```

### Phase 4 Drop Check

```
□ 业务数据已从网络搜索获取（非虚构）
□ Demo 结构完整（Dashboard / List / Detail / Kanban / Compare）
□ 交付物为单文件 HTML
□ Chart.js 已内联
□ showPage() / goDetail() 有空值保护
□ 用户已确认 PRD 后才生成 Demo
```

---

## 错误示例

### WRONG 1：不问需求直接写 PRD

```
用户：我想做一个短视频数据分析工具
Agent：好的，开始写 PRD...
X 错误：不问产品类型、目标受众、Demo 深度就开始写，产出可能与用户预期严重偏离
O 正确：先问 3-4 个关键问题（产品类型、受众、Demo 深度、特殊功能），锁定范围再动笔
```

### WRONG 2：Demo 使用虚构/编造数据

```
用户：生成 Demo
Agent：Demo 里用户数据都是随机生成的假数据
X 错误：使用假数据无法验证产品逻辑，用户拿到 Demo 没有参考价值
O 正确：先从网络搜索真实行业数据/竞品数据/基准数据，用真实数据填充 Demo
```

### WRONG 3：飞书批量 blocks >10 导致失败

```
Agent 一次性追加了 15 个 blocks 到飞书文档
结果：API 报错 1770006，文档创建失败
X 错误：没有遵守已验证的 Block API 批量限制
O 正确：逐个追加 blocks，每批不超过 10 个
```

### WRONG 4：PRD 缺少页面交互设计章节

```
Agent 写了 7 章 PRD，跳过了第 6 章（页面交互设计）
用户：我看不到界面长什么样
X 错误：缺页面路由图、线稿，开发/设计无法评估工作量
O 正确：第 6 章必须包含页面路由图（ASCII）+ 线稿（ASCII 网格布局）+ 组件-状态矩阵
```

---

## 异常与边界条件

| 场景 | 触发条件 | 处理动作 |
|:-----|:---------|:---------|
| 飞书 token 失效/获取失败 | Phase 2 同步飞书时 feishu_token.py 崩溃或 token 过期 | 直接 POST /auth/v3/tenant_access_token/internal 重新获取，不中断流程 |
| references 目录缺失 | Phase 2/4 读取 prd_structure.md / demo_framework.md 时找不到文件 | 使用内置默认模板结构继续生成，产出标注"无 reference 文件，使用默认模板" |
| WebSearch 搜索不到真实数据 | Phase 4 搜索行业案例/竞品时返回空结果 | 使用 references 中的预置模板数据，产出标注"搜索无结果，使用模板数据" |
| 用户中途改变产品方向 | Phase 3/4 用户说"改成另一个方向" | 退回 Phase 1 重新需求澄清 + 重写 PRD。不打补丁，不局部修改 |
| Demo 详情页空值报错 | Phase 4 生成 Demo 后点击详情页时 JS 报错 | 检查 showPage()/goDetail() 的空值保护，缺啥补啥。必须全部修复后再交付 |
| 非 KOL 领域无对应模板 | Phase 4 产品领域不涉及 KOL，kol_templates.json 无法使用 | 替换为对应领域的真实案例对象，保持页面结构不变 |
| 飞书文档权限不足 | Phase 2 PATCH 权限时返回 403 | 输出手动配置指引："请手动在飞书文档->分享->设为 anyone_can_edit"，不阻塞其他流程 |
| PRD 产品无显式工作流 | Phase 2 该产品无用户操作流程（如纯信息展示页） | 第 3 章改名为「核心用户路径」或直接跳过，不强行编造流程 |
| 用户拒绝使用真实数据（要保密） | Phase 4 用户说"不要用真实公司名/人名" | 使用脱敏占位符（"某公司"/"某用户"），产出标注"数据已脱敏" |
| Demo 深度切换 | Phase 4 用户看到 Demo 后说"太简单了，想看深度的" | 退回 Phase 1 重新确认 Demo 深度，重新生成。不在当前 Demo 上打补丁 |

**原则**：异常先告知用户，再按规则处理。绝不静默跳过或编造数据。

---

## 注意事项

1. MD 文件 -> workspace；脚本 -> 临时目录
2. 飞书批量 blocks 单批 >10 可能失败 -> 逐个追加
3. feishu_token.py 崩溃 -> 直接 POST /auth/v3/tenant_access_token/internal
4. Demo 实体名用真实姓名
5. 非 KOL 领域 -> 替换为对应领域真实案例，保持页面结构不变
6. PRD 章节按需自由追加或跳过（如无工作流则跳第 3 章）
