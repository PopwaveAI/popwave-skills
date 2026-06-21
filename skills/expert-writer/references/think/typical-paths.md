# typical-paths.md — 典型路径速查

> 加载时机：Think 初次路由时，对照确认当前环节上下游。
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

---

## 路径一：新书启动

```
用户说"开书"
  │
  ▼
Step 0 · expert-writer 全局感知
  │
  ▼
Step 1 · creative (forward)
  ├─ Phase 0:     全书立项 → 全书立项PRD.md
  ├─ Phase 0.5:   跨域素材聚合 (HARD-GATE)
  ├─ Phase 0.6:   ⬅ 消费 deconstructor 拆书成果 → 素材储备池/融合摘要.md
  ↓
Step 2 · reservoir
  ├─ 素材储备池/{素材}.md
  ↓
Step 3 · world
  ├─ L1 设定 → 小说世界设定/L1-01~06.md
  ├─ L1 深度展开
  ├─ L1 交叉关联
  ├─ 世界稳定性检验
  ├─ 数值体系 → 小说世界设定/数值体系/*.md
  ├─ 起点快照 → 小说世界设定/起点快照.md [用户确认闸门]
  └─ 终点快照 → 小说世界设定/终点快照.md [用户确认闸门 → 进入 character]
  ↓
Step 4 · character
  ├─ 角色卡 → 状态/角色/{主角,配角}-角色卡.md
  ├─ 动态升级表 → 小说世界设定/动态升级表.md
  ↓
Step 5 · plot
  ├─ Phase 0:  全书架构 → 剧情设计/（卷拆分/地理全图/角色出场/主线全览）
  ├─ Step 1:   卷定义 → 剧情设计/卷/卷{N}-战略定位.md [用户确认闸门]
  ├─ Step 2:   剧情线 → 剧情设计/剧情线/{主线,支线}-{名称}.md
  └─ Step 3:   分幕规划 → 剧情设计/幕/vol-XX/分幕规划.md + act-YY.md + chekhov-tracker.md
  ↓
Step 6 · chapter ★
  ├─ Step 1:  读入 act-YY.md + 卷{N}-战略定位.md + 状态/entity-snapshot.yaml + 角色卡
  ├─ Step 2:  事件链设计（逐个回合，同步地点/角色/情绪/信息释放）
  └─ Step 3:  产出 → 章节设计包/chXXX-设计包.md + entity-snapshot 更新
  ↓
Step 7 · prose ★
  ├─ Step 1:  读入章节设计包 + 写作资产/文风DNA/ + 锚定章
  ├─ Step 2:  正文渲染
  ├─ Step 3:  风格验证（P0禁句/视角一致性/解说员句式）
  └─ Step 4:  输出 → 正文/chXXX.md（含章末状态更新块）
  ↓
Step 8 · qa
  ├─ Step 1:  大纲层 QC（act-YY.md + reader_profile）
  ├─ Step 2:  骨架层 QC（章节设计包 + reader_profile）
  └─ Step 3:  正文层 QC（正文/chXXX.md + reader_profile）
```

---

## 路径二：已有项目续写

```
用户说"续写"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 检查精读闸门（倒数20章已精读？）
  → 检查 状态/entity-snapshot.yaml 一致性
  ↓
Step 1 · creative (reverse)
  ├─ Phase r1:  事件日志（逐章读正文）
  ├─ Phase r2:  L0 提取
  ├─ Phase r3:  L1 提取
  ├─ Phase r4:  卷纲/幕地图还原 → 剧情设计/卷/卷{N}-战略定位.md + 剧情设计/幕/vol-XX/act-YY.md
  ├─ Phase r5:  卷大纲确认
  └─ Phase r6:  交接验证报告
  ↓
Step 5 → Step 6 → Step 7 → Step 8（同新书启动的 plot → chapter → prose → qa）
  ⚠️ 续写项目 plot 从当前幕续设计下一个 act-YY.md，不重新规划全卷
```

---

## 路径三：参考书拆解 → 融入写作

```
用户说"拆解这本书"
  │
  ▼
Step 1 · tool-download-webnovel → {书名}.txt
  ↓
Step 2 · pop-decon (v12 雪花倒推)
  ├─ Phase 1:  事实提取 (角色卡 + ETL数据)
  ├─ Phase 2:  聚类卷幕 (全书架构 + Canvas矩阵)
  ├─ Phase 3:  归纳世界观 (L1-01~06 + 数值体系)
  ├─ Phase 4:  归纳故事引擎 (仅Lv3)
  └─ Phase 5:  验证打包
  ↓ (可选)
Step 3 · pop-shared-dna
  → 均匀采样 ≥20 章 → 产出 写作资产/文风DNA/{书名}.md
  ↓
 回到 路径一 · Step 1 creative 的 Phase 0.6（融合拆书成果）
```

---

## 快速路由速查

| 用户说 | 路由目标 | 需检查 |
|:-------|:--------|:------|
| 「开书」「新书」 | creative (fwd) | 全书立项PRD.md 未产出 → 从 Phase 0 开始 |
| 「续写」「下一章」 | 当前阶段 + 1 | 项目总控.md 管线进度 → next_skill |
| 「拆解」「分析这本书」 | download→decon | 参考书 TXT 是否存在 |
| 「设计剧情」「规划大纲」 | plot | world 产出是否齐全 |
| 「写第N章」 | chapter | act-YY.md + 卷{N}-战略定位.md 是否就位 |
| 「渲染」「上色」 | prose | 章节设计包是否存在 |
| 「审稿」「看看」 | qa | 正文是否存在 |
| 「分析文风」 | pop-shared-dna | 原文 ≥20 章是否可用 |
| 「改设定」「改角色」 | 定位→评估→逐层更新 | 修改路由表（SKILL.md §5） |

---

## 闸门检查点

| 环节 | 闸门 | 不过则 |
|:-----|:-----|:------|
| world → character | 终点快照 用户确认 | 回到 world 终点快照 |
| plot Phase 0 → Step 1 | 全书架构 用户确认 | 回到 Step 0 |
| plot Step 1 → Step 2 | 卷{N}-战略定位 用户确认 | 回到 Step 1 |
| plot → chapter | act-YY.md 首幕切片就位 | 等 plot 完成当前幕 |
| chapter → prose | 章节设计包就位 + entity-snapshot 一致 | 回到 chapter |
| prose → qa | 正文存在 + 风格验证通过 | 回到 prose |
