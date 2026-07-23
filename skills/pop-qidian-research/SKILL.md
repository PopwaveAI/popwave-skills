---
name: pop-qidian-research
description: 起点调研引擎。当用户说"找燃料""补燃料""题材机制"时启用燃料档；用户给力量体系参考书时启用decon-lite 9表拆书；pipeline Phase 0自动触发赛道定位调研；用户提供参考书时启用decon-plot剧情拆解。不写正文不排章纲。
---

# research

> 起点调研引擎。四档：燃料+题材机制 / decon-lite 9表拆书 / 赛道定位调研 / decon-plot剧情拆解。v4.3.0：新增decon-plot剧情拆解档。

---

## 做什么

四档调研，按触发条件切换：

| 档位 | 触发条件 | 产出 | 消费方 |
|:--|:--|:--|:--|
| 燃料+题材机制 | 用户说"找燃料/补燃料/题材机制" | `涌现/research-写作燃料.md` + `涌现/content-mechanics.md` | review |
| decon-lite 9表拆书 | 用户给力量体系参考书 | `素材/decon-lite-{书名}.md` | seed 1d+1e+1d-0+故事纲领 |
| 赛道定位调研 | pipeline Phase 0自动触发 | `素材/赛道调研.md` | seed 1d+plot三源合流 |
| decon-plot 剧情拆解 | 用户提供参考书 | `素材/decon-plot-{书名}.md` | seed S1+S2 / plot R2+R3+R4+R5 / character C1 |

---

## 怎么操作（SOP骨架）

> execution.mode: formal（落盘）/ draft（补全继续）/ trial（不落盘）。仅燃料档适用三档切换；decon-lite、赛道调研和decon-plot必须完整执行。
> 强弱加载：SKILL.md=完整骨架（必读），steps/下step文件=详细操作（按档位强加载全文），templates/=文档模板（落盘前加载）。

### 燃料+题材机制档
1. **分流+搜索** → `steps/step-1-find.md`：找写作燃料+题材机制分流（能进本书→燃料表；不能迁移→content-mechanics；疑似文风→禁交soul/write）
2. **落盘** → `steps/step-2-output.md`：产出燃料文档（≥3条，每条含事件形状/主角操作点/可外显爽点）+机制文档

### decon-lite 9表拆书档
1. **采样** → `steps/step-decon-lite.md` DL1.5：三阶段采样v2.0（前10章全文+11-100章关键词+100章后每25章+境界过渡期必采）
2. **9表拆解** → `steps/step-decon-lite.md` DL2：表1力量体系(规则级)+表2-5(节奏/情绪/人称/开篇)+表6-8(势力/金手指/危机,服务seed 1d-0)+表9动力引擎(服务seed 1e)
3. **质检+存盘** → `steps/step-decon-lite.md` DL3-DL4：9表完整性门禁→落盘`素材/decon-lite-{书名}.md`

### 赛道定位调研档
1. **四轮搜索** → `steps/step-track-research.md` S2：赛道格局→读者偏好→赛道演变→对标分析
2. **落盘** → `steps/step-track-research.md` S3-S4：产出`素材/赛道调研.md`+质量门禁

### decon-plot 剧情拆解档
1. **接收+采样** → `steps/step-decon-plot.md` DP1：接收参考书+采样范围声明
2. **6维度拆解** → `steps/step-decon-plot.md` DP2：
   - 力量体系对比（→seed S1）：参考书做法/优缺点/爽感差异
   - 金手指设计对比（→seed S2）：加速比/限制设计/代价平衡
   - Boss战设计（→plot R2）：铺垫时长/战斗阶段数/破局方式/临终反扑/爽感爆发点
   - 爽感场景拆解（→plot R3）：信息差铺设/面板爆发节奏/越级杀节奏
   - 分幕转折手法（→plot R4）：转折事件/节奏变化/读者冲击
   - NPC登场效果（→character C1+plot R5）：出场方式/关系建立节奏/伏笔埋设手法
3. **质检+存盘** → `steps/step-decon-plot.md` DP3-DP4：6维度完整性门禁→落盘`素材/decon-plot-{书名}.md`

---

## 红线

1. **读取协议**：执行任何档位前先读SKILL.md获取骨架，再按档位加载对应step文件（强加载全文）。templates落盘前加载。禁止跳过SKILL.md直接读step文件。
2. **不越界**：不写正文、不排章纲。本skill只做调研产出，不干涉下游创作。
3. **燃料三要素**：每条燃料必须落到事件形状+主角操作点+可外显爽点。缺要素=不合格。
4. **content-mechanics落盘**：content-mechanics.md必须落盘带元数据（owner=research）。
5. **机制不伪装文风**：不把内容机制伪装成文风特征交给soul/write。疑似文风→禁止交付。
6. **9表全拆+表1规则级**：decon-lite 9张表必须全拆。表1必须拆到规则级（主养成线+子养成线+chXX出处）。
7. **表9三组成齐全**：表9动力引擎三组成（驱动逻辑/运转机制/代价结构）必须齐全。
8. **decon-plot 6维度全拆**：6个维度（力量体系对比/金手指设计对比/Boss战设计/爽感场景拆解/分幕转折手法/NPC登场效果）必须全拆，每个维度必须标注消费方。缺维度=不合格。

---

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `steps/step-1-find.md` | 燃料档·第一步 | 燃料搜索+题材机制分流流程 |
| `steps/step-2-output.md` | 燃料档·落盘前 | 燃料+机制文档落盘流程 |
| `steps/step-decon-lite.md` | decon-lite档 | DL1.5采样v2.0+9表完整定义+质检门禁 |
| `steps/step-track-research.md` | 赛道调研档 | 四轮搜索+产出模板+质检门禁 |
| `steps/step-decon-plot.md` | decon-plot档 | DP1采样+6维度拆解+质检门禁 |
| `templates/fuel-doc.tpl.md` | 燃料档·落盘前 | 燃料文档模板（含元数据块） |
| `templates/mechanics-doc.tpl.md` | 燃料档·落盘前 | 机制文档模板（含元数据块） |
| `../_deprecated/pop-qidian/references/v3.5-pipeline-prd.md` | 对齐PRD时 | 契约层(骨架/owner/命名/mode/回复格式) |

---

## 版本

v4.3.0 | 2026-07-22 → CHANGELOG.md
- 新增decon-plot剧情拆解档（第五档）：6维度拆解（力量体系对比/金手指设计对比/Boss战设计/爽感场景拆解/分幕转折手法/NPC登场效果）
- 产出`素材/decon-plot-{书名}.md`，消费方：seed S1+S2 / plot R2+R3+R4+R5 / character C1
- 新增红线❌8：decon-plot 6维度必须全拆
- 现有四档（燃料+题材机制/decon-lite/赛道调研）内容不动
- 版本只留最新一条，历史版本见CHANGELOG.md
