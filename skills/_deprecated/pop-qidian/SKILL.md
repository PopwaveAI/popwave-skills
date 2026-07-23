---
name: pop-qidian
description: 涌现式小说项目入口。当用户说'新建涌现项目''项目跑偏''审计涌现规范'时启用。初始化/修复/审计项目骨架，给出一次性路由建议；非每轮总控。
---
# pop-qidian
> 涌现式小说项目初始化/修复/审计入口 v4.1.0。非每轮总控，每轮正文由write执行。

## 做什么
| 输入 | 输出 | 下游 |
|------|------|------|
| 用户需求(新建/修复/审计) | 项目骨架+审计报告+一次性路由 | seed→plot→review→write循环 |

骨架7 skill：pop-qidian-seed/plot/write/write-dndlike/write-onepiece/review。

## 怎么操作（SOP骨架）
> execution.mode: 初始化/修复/审计时一次性执行，非常规每轮调度。
> 强加载：红线+速查表+PRD §4契约引用（每轮必读）；弱加载：steps/templates/references按scenario按需加载。

### Step 1: 初始化/审计 → `steps/step-1-init-audit.md`
- 建立骨架（7 skill目录树+空壳元数据）或审计现有项目（scope/版本/current-state/soul/review/DNA执行包闭环）

### Step 2: 修复+路由 → `steps/step-2-fix-route.md`
- 补current-state/soul骨架缺口，给出一次性路由建议

## 红线
1. **读取协议**：skill文件用`Get-Content -Encoding UTF8 -Raw`读取。强加载=红线+速查表+PRD §4契约（每轮必读）；弱加载=steps/templates/references按scenario按需加载。
2. **创建项目必须双文件齐全** — SKILL.md + skill.json
3. **版本三处一致** — SKILL.md + skill.json + CHANGELOG.md
4. **不当每轮总控** — 路由建议仅初始化/修复/审计时一次性给出
5. **不让write全量扫库** — 库文件由review筛入current-state
6. **不把'本次采用skill'当合规证据** — 必须检查scope真实存在
7. **不调用pop-novel-create** — 涌现式写作不走novel-create；启用文风DNA时必须检查soul融合策略和current-state的DNA执行包

## 速查表
| 文件 | 读取时机 | 核心内容 |
|------|----------|----------|
| SKILL.md | 每轮必读 | 红线+SOP骨架+速查表 |
| steps/step-1-init-audit.md | 初始化/审计时 | 骨架建立+审计报告 |
| steps/step-2-fix-route.md | 修复缺口时 | 补current-state/soul+一次性路由 |
| templates/skeleton-init.tpl.md | 初始化骨架时 | 目录树+空壳元数据块 |
| references/v3.5-pipeline-prd.md | 需要契约层时 | 骨架/owner/命名/execution.mode/版本基线 |
| agents/openai.yaml | 需要agent配置时 | OpenAI agent配置 |

## 版本
v4.1.0 | 2026-07-22 | SKILL.md按设计规范重写：frontmatter补触发条件、红线重构为7条(首条读取协议)、速查表改为文件目录引导、版本历史移至CHANGELOG。
