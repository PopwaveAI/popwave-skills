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
Step 1 · pop-novel-bookstrap (forward)
  ├─ Phase 0:     故事引擎 → story-engine.yaml
  ├─ Phase 0.5:   跨域素材聚合 (HARD-GATE)
  ├─ Phase 0.6:   ⬅ 消费 deconstructor 拆书成果 → deconstruct-融合摘要.md
  ├─ Phase 1:     L1 六件套 (01~06)
  ├─ Phase 1.2:   L1 深度展开
  ├─ Phase 1.3:   L1 交叉关联
  ├─ Phase 1.5:   世界稳定性检验
  ├─ Phase 3:     project.yaml + 状态/角色/角色卡
  ├─ Phase 4:     reader_profile 校对
  ├─ Phase 5:     数值体系 x4
  ├─ Phase 6:     起点快照.md → 设计/ [用户确认闸门]
  └─ Phase 7:     终点快照.md → 设计/ [用户确认闸门 → 进入 plot]
  ↓
Step 2 · pop-writer-plot
  ├─ Phase 0:  全书架构 → 设计/全书架构.md（卷拆分/地理全图/角色出场/主线全览）
  ├─ Step 1:   卷定义 → 设计/卷/volume-XX.md [用户确认闸门]
  └─ Step 2:   幕纲 → 设计/幕/vol-XX/act-YY.yaml（Canvas矩阵 + info_release_plan 内嵌）
  ↓
Step 3 · pop-writer-chapter ★
  ├─ Step 1:  读入 act-XX.yaml + volume-XX.md + entity-snapshot + 角色卡
  ├─ Step 2:  事件链设计（逐个回合，同步地点/角色/情绪/信息释放）
  └─ Step 3:  产出 → 写作资产/设计包/chXXX-设计包.md + entity-snapshot 更新
  ↓
Step 4 · pop-writer-prose ★
  ├─ Step 1:  读入设计包 + 写作资产/文风DNA/ + 锚定章
  ├─ Step 2:  正文渲染
  ├─ Step 3:  风格验证（P0禁句/视角一致性/解说员句式）
  └─ Step 4:  输出 → 正文/chXXX.md（含章末状态更新块）
  ↓
Step 5 · pop-writer-qa
  ├─ Step 1:  大纲层 QC（act-XX.yaml + reader_profile）
  ├─ Step 2:  骨架层 QC（设计包 + reader_profile）
  └─ Step 3:  正文层 QC（正文/chXXX.md + reader_profile）
```

---

## 路径二：已有项目续写

```
用户说"续写"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 检查 pre_read_status（精读闸门 — 倒数20章已精读？）
  → 检查 entity-snapshot 一致性
  ↓
Step 1 · pop-novel-bookstrap (reverse)
  ├─ Phase r1:  事件日志（逐章读正文）
  ├─ Phase r2:  L0 提取
  ├─ Phase r3:  L1 提取
  ├─ Phase r4:  卷纲/幕地图还原 → 设计/卷/volume-XX + 设计/幕/vol-XX/act-YY
  ├─ Phase r5:  卷大纲确认
  └─ Phase r6:  交接验证报告
  ↓
Step 2 → Step 3 → Step 4 → Step 5（同新书启动的 plot → chapter-design → prose-render → qa）
  ⚠️ 续写项目 plot 从当前幕续设计下一个 act-XX.yaml，不重新规划全卷
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
  ├─ Phase 3:  归纳世界观 (L1六件套 + 宪法 + 数值)
  ├─ Phase 4:  归纳故事引擎 (仅Lv3)
  └─ Phase 5:  验证打包
  ↓ (可选)
Step 3 · pop-shared-dna
  → 均匀采样 ≥20 章 → 产出 写作资产/文风DNA/{书名}.md
  ↓
→ 回到 路径一 · Step 1 bookstrap 的 Phase 0.6（融合拆书成果）
```

---

## 快速路由速查

| 用户说 | 路由目标 | 需检查 |
|:-------|:--------|:------|
| 「开书」「新书」 | bookstrap (fwd) | story-engine 未产出 → 从 Phase 0 开始 |
| 「续写」「下一章」 | 当前阶段 + 1 | progress.last_completed_skill → next_skill |
| 「拆解」「分析这本书」 | download→decon | 参考书 TXT 是否存在 |
| 「设计剧情」「规划大纲」 | plot | bookstrap 产出是否齐全 |
| 「写第N章」 | chapter-design | act-XX.yaml + volume-XX 是否就位 |
| 「渲染」「上色」 | prose-render | 设计包是否存在 |
| 「审稿」「看看」 | qa | 正文是否存在 |
| 「分析文风」 | pop-shared-dna | 原文 ≥20 章是否可用 |
| 「改设定」「改角色」 | 定位→评估→逐层更新 | 修改路由表（SKILL.md §5） |

---

## 闸门检查点

| 环节 | 闸门 | 不过则 |
|:-----|:-----|:------|
| bookstrap → plot | 终点快照 用户确认 | 回到 Phase 7 |
| plot Phase 0 → Step 1 | 全书架构 用户确认 | 回到 Step 0 |
| plot Step 1 → Step 2 | volume-XX 用户确认 | 回到 Step 1 |
| plot → chapter-design | act-XX.yaml 首幕切片就位 | 等 plot 完成当前幕 |
| chapter-design → prose-render | 设计包就位 + entity-snapshot 一致 | 回到 chapter-design |
| prose-render → qa | 正文存在 + 风格验证通过 | 回到 prose-render |
