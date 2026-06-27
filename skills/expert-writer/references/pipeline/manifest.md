# 写作专家全链路合同（pipeline-manifest）

> v3.5涌现式写作管线合同。expert-writer唯一调度器→5步循环+2子skill调度，L2卡驱动，context manifest白盒。
> 对齐 PRD v3.5：`prd/01-管线架构/16-v3.5涌现式写作管线重构PRD.md`
> 对齐 context-manifest PRD：`prd/01-管线架构/15-context-manifest-子agent上下文清晰化PRD.md`

---

## 管线阶段表（v3.5）

| 阶段 | skill | 产出 | 消费 | 状态 |
|:-----|:------|:-----|:-----|:-----|
| 种子设计 | pop-writer-v3-seed | 卷纲/卷N-方向锚.md + 写作参考/设定/* + 写作资产/文风库/{书名}.md + 活记忆/活记忆.yaml(baseline) | — | ✅ 已有 |
| L2卡设计 | pop-writer-v3-plot | 卷纲/L2-NNN-名称.md（含结构分析表+物理坐标段+设定引用指针） | 卷N方向锚+设定 | ✅ 已有 |
| 涌现写作环 | expert-writer（主会话5步循环） | 正文/chXXX.md + 活记忆追加 + 项目总控更新 | L2卡+写作参考+活记忆+文风DNA | ✅ 已有 |
| ↳ create | pop-writer-v3-create | 初稿+create receipt | context manifest | ✅ 已有 |
| ↳ revise | pop-writer-v3-revise | 重写稿+revise receipt | 初稿+文风DNA | ✅ 已有 |
| 弧线校准 | pop-writer-v3-arc | 弧线校准报告/arc-XX.md + L2卡更新 + L3卡 + 活记忆压缩 | 正文+活记忆+L2卡 | ✅ 已有 |
| 按需调研 | pop-research | 写作参考/知识沉淀/* | 按需 | ⏳ 预留（尚未创建） |

> **v3.5关键变化（vs v3.3）：**
> - 新增 **L2卡设计**（pop-writer-v3-plot）阶段 — 取代种子文档，L2卡为唯一运行时活文档
> - 新增 **pop-research**（按需调研）— 管线预留位置，尚未创建
> - **emerge已废弃** — 5步循环由expert-writer主会话直接执行，不再作为独立环节
> - 6步循环 → **5步循环**（导演意图→状态快照→信息获取→子agent创作→receipt检查→活记忆更新）
> - 新增 **context manifest白盒机制** — 子agent上下文可追溯
> - 素材库+设定库 → **写作参考**（合并）

---

## 管线顺序

```
种子设计(pop-writer-v3-seed) → L2卡设计(pop-writer-v3-plot) → 涌现写作环(expert-writer 5步循环) ↔ 弧线校准(pop-writer-v3-arc)
                                                                ↑ 按需：pop-research
```

### 触发规则

| 触发条件 | 路由到 | 说明 |
|:---------|:-------|:-----|
| 项目初始化 | pop-writer-v3-seed | 首次启动 |
| seed完成 | pop-writer-v3-plot | L2卡设计 |
| plot完成（L2卡已产出） | expert-writer 5步循环 | 涌现写作 |
| **L2单元最后一章Step5完成** | pop-writer-v3-arc | **每个L2单元结束时触发**（v3.5变更） |
| arc完成 | expert-writer 5步循环 | 下一L2单元 |
| 需要外部调研 | pop-research | 按需调用 |

> v3.4 arc触发：每10-20章
> v3.5 arc触发：每个L2单元结束时

---

## 5步循环（expert-writer主会话执行）

| Step | 名称 | 执行者 | 核心动作 | 人工check |
|:-----|:-----|:-------|:---------|:---------|
| Step0 | 导演意图提取 | 主会话 | 从L2卡结构分析表取本章行→组装导演意图（≤150字） | CHECK 1：用户确认 |
| Step1 | 状态快照投影 | 主会话 | 从活记忆+L2卡物理坐标投影当前状态（≤400字） | 无 |
| Step2 | 信息获取 | 主会话 | 设定指针强制读取→library按需查询→pop-research(如需) | 无 |
| Step3 | 子agent创作 | 子agent | context manifest组装→create涌现写作→revise完全重写 | CHECK 2：用户验收 |
| Step4 | receipt检查 | 主会话 | 对照manifest vs receipt→对照导演意图验证 | 无 |
| Step5 | 活记忆更新+落盘 | 主会话 | 自然语言追加活记忆→正文落盘→项目总控更新 | 无 |

> v3.4 的6步（plan→info→create→revise→memory→commit）→ v3.5 的5步
> 原 Step4（dispatch-revise）合并进 Step3（create→revise一次调度）
> 原 Step4（memory）+ Step5（commit）合并为 Step5（活记忆更新+落盘）

---

## context manifest 白盒机制

> 对齐 context-manifest PRD（`prd/01-管线架构/15-context-manifest-子agent上下文清晰化PRD.md`）

### create阶段 manifest

| 注入项 | 来源 | 说明 |
|:-------|:-----|:-----|
| 导演意图 | Step0产出 | 含三问+settings_ref |
| 状态快照 | Step1产出 | protagonist+pressures+pending |
| 上章末尾 | 正文/chXXX.md | 500-800字衔接 |
| 设定文件 | Step2强制读取 | settings_ref指向的文件 |
| info_acquired | Step2产出 | library+research结果 |

### revise阶段 manifest

| 注入项 | 来源 | 说明 |
|:-------|:-----|:-----|
| create初稿 | create阶段产出 | 全文 |
| 文风DNA | 写作资产/文风库/{书名}.md | 精确匹配目标 |
| 要素切片 | 导演意图+状态快照 | 子线+伏笔+承诺+揭示 |
| 导演意图验证清单 | Step0导演意图三问 | 5项验证 |

### receipt 检查（Step4）

6项检查：
1. 完整性：receipt.status=full 且 actual_read≈manifest.size
2. 关键元素：key_elements_confirmed覆盖所有声明元素
3. 导演意图（create）：三问全部确认
4. 设定文件读取：settings_ref全部status=full
5. 文风DNA（revise）：status=full 且精确匹配（0误差）
6. 导演意图验证（revise）：5项验证全部通过

修复策略：连续2次同一项不通过 → 降级策略B（红线5）

---

## 理想目录路由

```
{项目名}/
├── 卷纲/
│   ├── 卷N-方向锚.md                     [seed] → [plot消费]
│   ├── L2-NNN-名称.md                    [plot产出] → [emerge消费] → [arc更新]
│   └── L3-NNN-名称.md                    [arc产出] → [arc更新]
├── 写作参考/
│   ├── 索引.md                           [seed初始化] → [全管线追加]
│   ├── 设定/                             [seed产出] → [emerge Step2强制读取]
│   ├── 知识沉淀/                         [pop-research/expert-writer产出]
│   └── 已废弃/                           [arc修剪归档]
├── 写作资产/
│   └── 文风库/{书名}.md                  [seed产出] → [revise消费]
├── 活记忆/活记忆.yaml                    [seed初始化] → [emerge Step5追加] → [arc压缩]
├── 正文/chXXX.md                        [emerge Step5落盘]
├── 弧线校准报告/arc-XX.md                [arc产出]
└── 项目总控.md                           [expert-writer每章更新]
```

> v3.5变化：
> - 种子文档.md **取消** → L2卡+写作参考吸收
> - 素材库/ + 设定库/ → **写作参考/**（合并）
> - 新增卷纲/ 目录（L2卡+L3卡+卷方向锚）

---

## 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v3.5 | 2026-06-28 | 6步→5步；L2卡替代种子文档；素材库+设定库合并为写作参考；context manifest白盒；arc每L2单元触发；新增plot+pop-research |
| v3.3 | 2026-06-26 | emerge调度合并到expert-writer；7步→6步剔除qa |
| v3.1 | 2026-06-25 | 去掉v2双轨，全方面服务于v3.1 |
