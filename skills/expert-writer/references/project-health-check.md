# 项目健康检查（快速检测模式）

> **触发方式**：用户说"检查项目状态/看看进度/健康检查/查一下/看看差什么/项目总控/管线状态"
> **产出**：结构化健康报告（对话内输出，不留盘，但会按需更新项目总控.md）
> **关联文件**：`references/pipeline-manifest.md`（管线硬顺序）、`项目总控.md`（项目实际进度）
>
> 此模式不进入任何子 skill，纯检测 + 报告。

---

## 检查流程

### Step 0：加载管线合同 + 项目总控

```
Get-Content -Encoding UTF8 -Raw references/pipeline-manifest.md
  → 获取管线顺序和各阶段前置条件/产出

检查项目根目录 项目总控.md 是否存在
  → 存在：Get-Content -Raw 读取，获取 current_stage + completed_stages
  → 不存在：标记 ⚠️ "项目总控文件不存在，需要初始化"
```

### Step 1：管线进度检查

**1a — 阶段连续性**：比对 completed_stages 与 pipeline-manifest 的顺序

```
completed_stages = [creative, world]
manifest_order   = [creative, reservoir, world, plot, chapter, prose, qa]
                                 ↑
                        断裂点：reservoir 被跳过
```

输出格式：
```
[creative] ✅ → [reservoir] ❌跳过 → [world] ✅ → [plot] ⬜ → ...

    ↓
⚠️ 管线断裂：reservoir 阶段被跳过。
建议：走 reservoir 注入流程补齐剧情储备卡后再进 plot。
```

**1b — 产出物完整性**：按当前阶段倒查各阶段必备文件是否存在

```
| 阶段 | 必备产出一项 | 存在？ |
|:-----|:------------|:------|
| creative | 00-原始设定/爽点引擎.md | ✅ |
| creative | 00-原始设定/PRD.md | ✅ |
| creative | 00-原始设定/故事引擎.md | ✅ |
| creative | 00-原始设定/素材储备池.md | ✅ |
| creative | _样品试读/样品-v*.md | ✅ |
| reservoir | 素材储备池是否剧情储备卡格式? | ⚠️ 需人工判断 |
| world | 小说世界设定/L1-01.md | ✅ |
| world | 小说世界设定/L1-02.md | ✅ |
| world | 小说世界设定/L1-03.md | ✅ |
| world | 小说世界设定/L1-04.md | ✅ |
| world | 小说世界设定/L1-05.md | ✅ |
| world | 小说世界设定/L1-06.md | ✅ |
| world | 状态/角色/主角-角色卡.md | ⚠️ 需检查 |
| world | 小说世界设定/数值体系/combat_capability.md | ⚠️ 需检查 |
| world | 小说世界设定/数值体系/rank_schedule.md | ⚠️ 需检查 |
| world | 小说世界设定/数值体系/monster_rank_map.md | ⚠️ 需检查 |
| world | 小说世界设定/数值体系/collision_curve.md | ⚠️ 需检查 |
| world | 小说世界设定/起点快照.md | ⚠️ 需检查 |
| world | 00-总控/世界宪法.md | ⚠️ 需检查 |
| world | 小说世界设定/动态升级表.md | ⚠️ 需检查 |
| plot | 设计/卷/卷1-战略定位.md | ⚠️ 需检查 |
| plot | 设计/剧情线/*.md (每条线独立) | ⚠️ 需检查 |
| plot | 设计/幕/vol-1/分幕规划.md | ⚠️ 需检查 |
| plot | 设计/幕/vol-1/act-*.md | ⚠️ 需检查 |
| plot | 设计/幕/vol-1/chekhov-tracker.md | ⚠️ 需检查 |
| chapter | 章节设计包/ch*-设计包.md | ⚠️ 需检查 |
| prose | 正文/ch*.md | ⚠️ 需检查 |
```

> 实际扫描时直接 search_files 各路径确认存在性，不依赖记忆。

### Step 2：文件截断风险扫描

对已存在的关键文件，抽样检查是否存在被截断风险：

```
检查对象：各阶段产出物中最大的几个文件
检查方法：(Get-Item '{path}').Length vs 上次读取时的字符数
标记：文件 > 10KB 但未被 Get-Content -Raw 全量读取过 → ⚠️ 可能存截断历史
```

> 这一步不是重读所有文件（太贵），是**标记已知风险**：哪些文件很有可能在之前的操作中被截断了。

### Step 3：项目总控修正

```
if 项目总控.md 不存在:
    用 references/project-master-control.tpl.md 初始化
    → completed_stages 从管线进度检查推算
    → current_stage 设为第一个未完成的阶段
    → 写入关键产出索引（从 Step 1b 的扫描结果）
    
if 项目总控.md 存在但内容与文件扫描不一致:
    比如 completed_stages 说有 world 但 L1 文件缺失 → 标记不一致
    告知用户差异，询问是否修正项目总控
```

### Step 4：输出报告

报告格式（对话内输出，不留盘）：

```
## 📊 项目健康检查报告

### 管线进度
[creative] ✅ → [reservoir] ✅ → [world] ✅ → [plot] ✅ → [chapter] ⏳(ch001) → [prose] ⬜ → [qa] ⬜
当前阶段：chapter v2.0
管线连续性：✅ 连续（无跳过）

### 产出物完整性
✅ creative: 6/6 齐全
✅ reservoir: 剧情储备卡格式
✅ world: 7/8 齐全（⚠️ 缺 collision_curve.md）
✅ plot: 6/6 齐全
⚠️ chapter: 1/30 完成（已完成ch001设计包）

### 截断风险
⚠️ L1-04.md (32KB) — 未确认全量读取历史

### 待处理
- collision_curve.md 缺失 → 建议回 world 补齐
- 设计包完成度 1/30 → ch002 设计包下一步

### 推荐下一步
➡ 继续 ch002 设计包（当前阶段连续）
—或—
➡ 先补齐 collision_curve.md 再进章节设计
```

---

## 触发方式

| 用户说 | 动作 |
|--------|------|
| "检查项目状态/看看进度/健康检查" | 全量检查（Step 0→4） |
| "检查管线/看看差什么" | Step 0→1→4（跳过截断风险扫描） |
| "更新项目总控/同步一下" | Step 0→1→3→4（重扫文件，修正总控） |
