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
  → 存在：Get-Content -Raw 读取，获取 管线身份（专家/版本/启动版本）和 执行顺序日志
  → 不存在：自动初始化
    1. 从 references/project-master-control.tpl.md 复制模板到 项目总控.md
    2. 填入项目身份（书名从 project.yaml 或目录名推断）
    3. **扫描实际文件系统**，填充 📊 项目现状 全部字段（首屏仪表盘/阶段执行/产出物清单/目录结构/进度锚点）
    4. 从文件修改时间戳推算出已有阶段的执行顺序，写入执行顺序日志
    5. 写入管线版本戳（当前 expert-writer SKILL.md 的 version → 管线版本 + 本项目启动时版本）
    6. 从 pipeline-manifest.md 填充 🗺️ 所属管线（理想全流程 + 理想目录路由）
    7. 生成管线差异映射（理想 vs 实际）
    8. 输出 ⚠️ "项目总控.md 已自动初始化（基于文件扫描推断，请确认准确性）"
```

> 初始化后，Agent 和人类打开 项目总控.md 直接看到完整项目全貌 + 差距。

---

### Step 1：管线进度检查

**1a — 阶段连续性检测**

检测依据优先级：
1. **优先**：`项目总控.md` 的「执行顺序日志」（有时间戳的顺序记录）
2. **次优**：各阶段核心文件的最早修改时间戳（存量项目无执行日志时推断）
3. **兜底**：直接询问用户（时间戳推断矛盾时）

---
**模式1：有执行顺序日志**

```yaml
执行顺序日志:
  #1: creative  @ 2026-06-18 10:08
  #2: world     @ 2026-06-18 10:26   ← 本应是 #3
  #3: reservoir @ 2026-06-18 10:44   ← 本应是 #2
  #4: plot      @ 2026-06-18 10:50
  #5: chapter   @ 2026-06-18 10:56

pipeline-manifest 理想顺序: [creative, reservoir, world, plot, chapter, prose, qa]
```

比对方法：在理想顺序中取 completed_stages 的最小和最大索引，检查中间是否有缺失。

```python
ideal = [creative, reservoir, world, plot, chapter, prose, qa]
actual_order = [creative, world, reservoir, plot, chapter]  # 从执行日志提取

# 方法：对 actual_order 遍历，检查每个阶段在 ideal 中的前一个阶段是否已完成
for i, stage in enumerate(actual_order):
    prev_in_ideal = ideal[ideal.index(stage) - 1] if ideal.index(stage) > 0 else None
    if prev_in_ideal and prev_in_ideal not in actual_order[:i]:
        ⚠️ 管线断裂：执行到 {stage} 时，应有前置阶段 {prev_in_ideal} 尚未完成

# 示例输出：
⚠️ 管线断裂：执行到 world（#2）时，应有前置阶段 reservoir 尚未完成
  顺序日志：creative(1st) → world(2nd) → reservoir(3rd) → ...
  修复建议：如果项目尚未出 plot 阶段，可以考虑重新执行 reservoir 补齐剧情储备卡。
  如果已出 plot（当前状态），检查素材储备池是否已升级为剧情储备卡格式。
```

---
**模式2：无执行顺序日志（存量项目首次健康检查）**

```yaml
1. 按 pipeline-manifest 的每个阶段，找该阶段的核心产出文件
2. 取每个阶段最早文件的修改时间戳
3. 按时间戳排序推算出执行顺序
4. 输出 ⚠️ "基于文件时间戳推断，可能不精确"
5. 生成初始执行顺序日志 → 写入项目总控.md → 以后基于日志检测
6. 如果时间戳推断显示断裂 → 明确告知用户"请确认实际执行顺序"
```

---
**输出格式（统一）：**

```text
[creative] ✅ → [reservoir] ⚠️ 顺序异常 → [world] ✅ → [plot] ✅ → [chapter] ✅ → [prose] ⬜ → [qa] ⬜

⚠️ 管线断裂：reservoir 在 world 之后执行
  实际顺序: creative(1st) → world(2nd) → reservoir(3rd) → plot(4th) → chapter(5th)
  理想顺序: creative → reservoir → world → plot → chapter → prose → qa
  影响评估: world 阶段没有吃到 reservoir 的剧情储备卡，L1设定可能不够丰富
  修复建议: 检查素材储备池是否已升级为剧情储备卡格式，如果已升级则断裂影响有限
           如果尚未升级，走 reservoir 注入流程补齐
```

**1b — 产出物完整性（产出物清单双比对）**

扫描实际文件系统，更新项目总控.md 的 📊 项目现状 块。对话只输出摘要。

```
执行方式：
1. 按 项目总控.md §产出物清单 的每条记录搜索对应文件
   文件存在 → 标记 ✅ | 不存在且阶段已完成 → ❌ | 不存在且阶段未开始 → ⬜
2. 更新 项目总控.md §📊 项目现状 → 产出物清单 的状态列
3. 扫描实际目录结构，更新 §📊 项目现状 → 目录结构
4. 更新 §📊 项目现状 → 首屏仪表盘 的统计数字
5. 如产出文件缺失但其所有输入文件都存在（说明产出者跳票）→ ⚠️ 标记

对话输出格式（摘要，不留盘全部内容）：
```

```
📂 项目全貌
├─ 创意宪法层    ✅ 5/5  (爽点引擎/PRD/故事引擎/素材储备池/样品)
├─ 世界设定层    ⚠️ 6/10 (缺: monster_rank_map, collision_curve, 配角角色卡, 世界状态)
├─ 储备剧情池    ✅ 1/1
├─ 剧情设计层    ✅ 8/8
├─ 章节设计包    ⬜ 1/30 (ch001 设计包就绪, 缺 ch002~ch030)
└─ 正文          ⬜ 0/30

📊 总体完成度: 21/84 = 25%（含预期章节数）
```

> 详细文件树见 `项目总控.md → 📊 项目现状 → 目录结构`。

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
    → 执行顺序日志从管线进度检查推算
    → 📊 项目现状 从 Step 1b 的扫描结果填充
    
if 项目总控.md 存在但内容与文件扫描不一致:
    比如 产出物清单 标记某文件 ✅ 但实际扫描找不到 → 标记不一致
    告知用户差异，询问是否修正项目总控（刷新 📊 项目现状）
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
