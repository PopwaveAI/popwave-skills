---
name: pop-recommend
description: "当用户说'推书/推书卡/读者推荐'时启用。从小说原文生成读者推书卡HTML，三阶段价值扫描100章只精读30-40章。"
---

# pop-recommend

> 推书营销专家。从小说原文→读者推书卡（给新读者的无剧透推荐）。v1.2.0

## 做什么

输入：小说原文txt文件
输出：一张可分享的推书卡HTML（9页式读者推荐卡）+ 评审JSON

推书不是拆书。目标是帮新读者判断"这本书值不值得看、适不适合我"。每个判断带原文证据+spoiler标注。

## 怎么操作（SOP骨架）

> execution.mode: 串联式 | 强保障：本SKILL.md由host层强制注入 | 弱保障：steps/references/templates需agent主动读取，设计时假设可能没读到

- **Step 1** 三阶段价值扫描（内化）→ ETL精简版(编码归一+章节分割+元数据,禁止逐章摘要)→Phase1骨架扫描(首章+每卷首尾+尾章≈15-20章,产出structure-map.json)→Phase2锚点深读(highlight/controversy/character/relationship章≈10-15章,产出anchor-pool.json+evidence-ledger.json)→Phase3阅感采样(全书均匀采样5-8章,6维度量化打分,产出reading-metrics.json) → 5个JSON落盘工作稿/
- **Step 2** 评审生成 → `steps/step2.md`（消费5个JSON生成review.json，spoiler三级控制safe/mild/major只消费safe+mild）
- **Step 3** HTML渲染 → `steps/step3.md`（9页独立设计语言：Cinematic Poster/Swiss Grid/Magazine Editorial等，产出{书名}-读者推书-v1.html）

## 红线

1. **读取协议**——读取skill文件用`Get-Content -Encoding UTF8 -Raw`，Read工具有行数限制会截断丢内容
2. **禁止逐章摘要**——必须用三阶段价值扫描，100章只精读30-40章
3. **所有判断绑定evidence_id**——每条strength/controversy/character必须引用证据台账，excerpt≥50字
4. **review.json是唯一评审输出**——禁止生成input+draft两个重复JSON
5. **Step文件链式加载**——Step1内化→step2.md→step3.md，禁止跳过

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次run强制注入 | SOP骨架+三阶段价值扫描方法论+红线 |
| `steps/step2.md` | Step1完成后读取 | 评审生成（消费5个JSON→review.json） |
| `steps/step3.md` | Step2完成后读取 | HTML渲染（9页推书卡设计语言） |
| `references/page-layout-guide.md` | Step3渲染时参考 | 9页布局设计指南 |
| `templates/*.tpl.json` | Step1-2产出时复制填充 | JSON模板（structure-map/anchor-pool/reading-metrics/review） |
| `templates/recommend-card.tpl.html` | Step3渲染时使用 | HTML推书卡模板 |

## 版本

v1.2.0 | 2026-07-22 | 按Popwave Skill设计规范重写SKILL.md结构（≤100行），红线合并为5条含读取协议 → CHANGELOG.md
