---
name: pop-fanqie-review
description: "当用户说'番茄review/番茄审核/审核正文'时启用。三段式审核（合规底线→番茄底线→爽感底线），每章产出审核报告。"
---

# pop-fanqie-review

> 番茄审核专家。三段式审核，通过→ch+1，打回→重写。v4.3.0

## 做什么

输入：正文/chXXX.txt+前章审核结论+current-state+角色库+笔触DNA
输出：审核/review-chXXX.md（审核报告）+ 审核/review-verdict-chXXX.md（结论PASS/REJECT）

三段式审核：合规底线（一票否决）→番茄底线（逐条检查）→爽感底线（主推爽感必触发）。

## 怎么操作（SOP骨架）

> execution.mode: 串联式 | 强保障：本SKILL.md由host层强制注入 | 弱保障：steps/需agent主动读取，设计时假设可能没读到

- **Step 1** 加载审核材料（内化）→ 正文/chXXX.txt+前章审核结论(如果有)+current-state+角色库+笔触DNA(三态协议对应的笔触约束)
- **Step 2** 三段式审核 → `steps/step2.md`
  - 2a 合规底线：政治敏感/红线词/未成年保护/价值观，命中任一=直接REJECT
  - 2b 番茄底线：章末钩子/爽感≥1/节奏密度8-12个事件/字数2000-2500/章名格式/章型7节拍/前后章衔接(回收前章钩子)/角色库一致性
  - 2c 爽感底线：主推爽感是否触发/爆发后三段式是否执行/爽感引擎5种类型是否有
- **Step 3** 产出审核报告 → `steps/step3.md`（审核/review-chXXX.md含三段式结果+问题清单+修改建议，审核/review-verdict-chXXX.md含PASS/REJECT+一句话理由+打回条目）

审核结论：全部通过→PASS→pipeline Phase 4 ch+1。任一不通过→REJECT→pipeline Phase 4重写（附打回条目+修改建议）。

## 红线

1. **读取协议**——读取skill文件用`Get-Content -Encoding UTF8 -Raw`，Read工具有行数限制会截断丢内容
2. **三段式全审**——合规→番茄→爽感，不能跳过任何一段，合规命中=直接REJECT不再审后续
3. **审核结论必须PASS/REJECT**——不能模棱两可，REJECT必须列出具体打回条目+修改建议
4. **每条问题必须标注严重等级+修改建议+证据引用**——严重等级分critical/major/minor，证据引用正文行号或片段
5. **Step文件链式加载**——Step1内化→step2.md→step3.md，禁止跳过

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次run强制注入 | SOP骨架+三段式审核方法论+红线 |
| `steps/step2.md` | Step1完成后读取 | 三段式审核执行（合规8项/番茄8项/爽感3项检查清单） |
| `steps/step3.md` | Step2完成后读取 | 审核报告+结论产出格式（review-chXXX.md+review-verdict-chXXX.md） |

## 版本

v4.3.0 | 2026-07-22 | 按Popwave Skill设计规范重写SKILL.md结构（≤100行），红线合并为5条含读取协议 → CHANGELOG.md
