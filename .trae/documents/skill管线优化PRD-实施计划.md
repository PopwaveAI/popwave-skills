# Skill 管线优化 — 实施计划

> 基于 `E:\AI小说\.trae\documents\skill管线优化PRD.md` v1.1
> 计划日期：2026-06-07

---

## 概览

改造 5 个 skill：deconstructor / bookstrap / plot / writer / expert-writer
总改动量：3个新文件 + 17个修改文件 = 20个文件

---

## 实施顺序（按上下游依赖）

```
Phase 1（并行）
├── deconstructor P0：拆书缩至第一卷 + 采样固化 + T4新增起点/终点快照
└── writer P1：Design包新增里程碑对齐检查

Phase 2
└── bookstrap P0+P1：新增 Phase 0.6 + 6 + 7 + 全局改名 bootstrap→bookstrap

Phase 3
└── plot P0：主线拆M1/M2/M3 + 新增锚点确认 + 里程碑设计

Phase 4
└── expert-writer P2：路由路径更新 + 修改路由扩展
```

---

## 详细改动清单

### 一、pop-novel-deconstructor (v6.2.0 → v7.0.0) — P0

| # | 文件 | 改动 |
|---|------|------|
| 1 | SKILL.md frontmatter | description 改为「默认拆解第一卷/前100章」 |
| 2 | SKILL.md 开头段落 | 追加范围说明 |
| 3 | SKILL.md Phase 0 采样策略表 | 整表替换为固定策略：开篇10章全读+结尾5章全读+间隔每10章采1章 |
| 4 | SKILL.md 质量红线 ❌5 | 改为固定采样规则描述 |
| 5 | SKILL.md Phase 4 产出清单 | 追加卷1起点快照/卷1终点快照 |
| 6 | SKILL.md 版本行 | v6.3.0 → v7.0.0 |
| 7 | skill.json | version → 7.0.0 |
| 8 | templates/T4-剧情全貌模板.md | 末尾追加「第一卷起点快照」「第一卷终点快照」两个产出块 |
| 9 | templates/T4、T5、T6 模板 | 顶部追加 📌 消费管线标记 |

### 二、pop-novel-bootstrap → pop-novel-bookstrap — P0+P1

| # | 文件 | 改动 |
|---|------|------|
| 1 | **新建** phases/phase-0.6.pe.md | 拆书成果融合（读deconstructor产出→提取参考值→产出融合摘要） |
| 2 | **新建** phases/phase-6.pe.md | 起点状态设计（产出design/起点快照.md，需用户确认） |
| 3 | **新建** phases/phase-7.pe.md | 终点展望（产出design/终点快照.md，需用户确认） |
| 4 | SKILL.md Forward 质量红线 | 追加 ❌9(拆书消费)/❌10(起点锁定)/❌11(终点锁定) |
| 5 | SKILL.md Forward 执行顺序 | 插入 Phase 0.6 + Step 4(锚点设计) |
| 6 | SKILL.md 路径注册表 | 追加 Phase 0.6/6/7 三个新行 |
| 7 | phases/phase-5.pe.md | act_rank_schedule.yaml 追加注释供Phase 7消费 |
| 8 | P1：全局改名 | skill.json id→bookstrap / SKILL.md name→bookstrap / 所有文档bootstrap→bookstrap |

### 三、pop-novel-plot (→ v4.0.0) — P0

| # | 文件 | 改动 |
|---|------|------|
| 1 | SKILL.md Step 2 情节线定义 | 主线拆为M1(世界危机)/M2(战斗行动)/M3(成长) |
| 2 | SKILL.md act-XX.yaml plotlines 模板 | id:主线 → id:M1/M2/M3，每章plotlines_active对应改 |
| 3 | SKILL.md 新增 Step 1.5 | Phase 0锚点确认（读起点/终点快照） |
| 4 | SKILL.md 新增 Step 1.6 | Phase 1里程碑设计（从终点反推必经节点） |
| 5 | SKILL.md Step 2 追加 | 里程碑-线映射 |
| 6 | SKILL.md Step 3-b 每章字段 | 新增milestone_active + milestone_progress |
| 7 | SKILL.md Step 5 自检 | 新增里程碑覆盖率检查 + 线-里程碑交叉检查 |
| 8 | skill.json + SKILL.md | version → 4.0.0 |

### 四、pop-novel-writer (→ v12.0.0) — P1

| # | 文件 | 改动 |
|---|------|------|
| 1 | steps/step-1-design.md 读入上下文 | 追加里程碑设计+终点快照读取 |
| 2 | steps/step-1-design.md 设计说明 | 新增★里程碑对齐块 |
| 3 | steps/step-2-render.md 写后自评 | 新增★写后自评里程碑感知检查 |
| 4 | SKILL.md 写前必读清单 | 追加milestone文件 |
| 5 | skill.json | version → 12.0.0 |

### 五、expert-writer (→ v2.2.0) — P2

| # | 文件 | 改动 |
|---|------|------|
| 1 | SKILL.md 推荐Skill清单 | pop-novel-bootstrap → pop-novel-bookstrap，触发场景追加 |
| 2 | SKILL.md 路由路径 | bootstrap→bookstrap + 追加(含拆书融合+起点+终点)(含里程碑) |
| 3 | SKILL.md 修改路由扩展 | 追加起点/终点变更的评估规则 |
| 4 | _shared/pop/POP-ROUTER.md | bootstrap→bookstrap 全局替换 |
| 5 | references/think-开书设定.md | bootstrap→bookstrap + 追加起点/终点里程碑审视项 |
| 6 | skill.json | version → 2.2.0 |

---

## 验证方案

### 自测一轮

1. **deconstructor**：对 `铸星者（完整版）` 跑一次默认范围拆解，验证只拆第一卷/前100章 + 产出起点/终点快照
2. **bookstrap**：用 deconstructor 的深渊主宰数据跑一次 bookstrap forward，验证 Phase 0.6 融合 + Phase 6/7 产出
3. **plot**：基于 bookstrap 产出跑一次 plot，验证 M1/M2/M3 三条主线 + 里程碑设计
4. **writer**：基于 plot 产出跑一次 writer Step 1，验证 Design 包含里程碑对齐信息
5. **expert-writer**：验证路由路径显示正确的 bookstrap 名称

### 回归检查
- deconstructor：确认「用户明确要求全书拆解」时仍能走原动态密度表
- bookstrap：确认 reverse 模式不受影响（起点/终点快照仅 forward 模式消费）
- plot：确认原有情绪驱动+爽点分布+幕纲逻辑不被破坏
