# Phase 0.6：拆书成果融合（NEW v4.0）

> 该文件同时作为执行指令和参考指南。

## 前置条件
- Phase 0.5 跨域素材聚合已完成
- deconstructor 已对锚点书产出至少 T1-T10 + 卷1起点快照 + 卷1终点快照

## 目的
将 deconstructor 对锚点书的产出物进行结构化融合，提取可复用的规则注入 L1 设定。
**不是照搬**——是提取参考值，标注"可以是这个幅度""这个结构的原理在此"等。

## 执行步骤

### 1. 定位 deconstructor 产出
读取 `素材库/拆解报告/` 目录下对应锚点书的文件，确认存在：
- {书名}-T1-力量体系规则手册.md
- {书名}-T2-世界观展开.md
- {书名}-T4-剧情全貌.md（含卷1起点/终点快照）
- {书名}-T5-人物阵营.md
- {书名}-T6-叙事设计技法.md
- {书名}-T10-文风DNA指纹.md

### 2. 逐 T 提取参考值

对 T1 (力量体系): 提取阶层差/通胀幅度/瓶颈设计 → 作为 L1 力量体系的参考幅度
对 T2 (世界观展开): 提取信息释放节奏/世界观展开速度 → 标注在 L1 世界观展开策略
对 T4 (剧情全貌): 提取卷1的起点/终点快照作为参考锚点 → 帮助理解"卷边界怎么设"
对 T5 (人物阵营): 提取角色密度/阵营分裂方式
对 T6 (叙事设计): 提取节奏模板/悬念链路
对 T10 (文风DNA): 提取叙事哲学原则

### 3. 产出融合摘要

输出 `00-原始设定/L0-产品层/deconstruct-融合摘要.md`：

```yaml
# deconstruct 融合摘要
source: "{书名}"       # deconstructor 产出的锚点书
fusion_date: "YYYY-MM-DD"
extraced_rules:
  power_system:
    reference: "阶层差2阶可用装备弥补，越3阶不成立"
    note: "非照搬，是幅度参考"
  world_building:
    reference: "前30章只展现城市尺度的社会结构，30章后展开区域级"
  act_boundary:
    vol1_start: "摘要 deconstructor 的起点快照关键点"
    vol1_end: "摘要 deconstructor 的终点快照关键点"
  narrative_design:
    reference: "每3-5章一个小高潮，每8-10章一个爆发点"
  character_density:
    reference: "第一卷出场核心角色≤5人，配角≤15人"
```

### 4. 红线
❌ 拆书成果存在但不读取 → 退回 Phase 0.6
