# 三层框架改造 Plan v2 — 骨架权责重组

## 核心变更

**骨架 → plot 产出，writer 去掉 Pass1**

```
当前（v10.0）：
  plot → info_release → act-XX.yaml
  writer → Director 消费 info_release
         → Pass1 骨架 Agent 从 L1 提取内容产事实骨架  ← 这个不该在 writer
         → ESM before + Pass2 渲染

目标（v11.0）：
  plot → info_release → 事实骨架 → act-XX.yaml（含骨架）
  writer → Director 消费 act-XX.yaml 中的骨架
         → ESM before（从 DNA 生成 Layer 2）
         → Pass2 渲染（直接消费骨架）
         → 去掉 Pass1 骨架 Agent
```

---

## 涉及文件清单

| # | 文件 | 操作 | 说明 |
|:-:|:----|:----|:-----|
| 1 | **NEW** `pop-novel-plot/templates/事实骨架模板.md` | 新建 | 骨架产出标准格式 |
| 2 | `pop-novel-plot/SKILL.md` | 重写 | 新增 Step 3-c + 全链路数据流图 + 质量红线 + 产出物 |
| 3 | `pop-novel-plot/CHANGELOG.md` | 追加 | v5.0.0 |
| 4 | `pop-novel-plot/skill.json` | 版本号 | 4.0.0 → 5.0.0 |
| 5 | `pop-novel-writer/SKILL.md` | 重写管线段 | 去掉 Step 2 骨架Agent、ESM 15→14项、管线图、摘要行 |
| 6 | `pop-novel-writer/prompt-templates/Director-prompt.md` | 更新 | 去掉骨架Agent引用，改为直接读act-XX.yaml骨架 |
| 7 | `pop-novel-writer/prompt-templates/Pass1-chapter-planner.md` | **删除** | 不再需要 |
| 8 | `pop-novel-writer/prompt-templates/Pass2-renderer.md` | 更新 | 输入项14项、去掉info_release实体内容项 |
| 9 | `pop-novel-writer/CHANGELOG.md` | 追加 | v11.0.0 |
| 10 | `pop-novel-writer/skill.json` | 版本号 | 9.7.0 → 11.0.0 |
| 11 | `pop-novel-writer/styles/文风锚定包模板.md` | **移动+重写** | 移到 deconstructor 下 + 更新描述 |
| 12 | `pop-novel-deconstructor/SKILL.md` | 更新 | 引用模板路径更新 |
| 13 | `pop-novel-writer/styles/default.md` | 不动 | 保持兜底 |

---

## 改动详解

### 1. 新建：`pop-novel-plot/templates/事实骨架模板.md`

骨架产出的标准化格式，类似文风锚定包模板。Agent 拿着这个填空。

**结构**：

```markdown
# {chXXX} 事实骨架

> 由 plot Step 3-c 产出。供给 writer 直接消费。

---

## 信息释放执行

- 已按 info_release 从 L1 提取设定内容
- 设定{名称}通过{实战展示}嵌入骨架事件{编号}
- 设定{名称}通过{叙事者说明}嵌入骨架插槽【插·设定说明】

---

## 事件节点

### 节点 1：[事件简述]

**事件**：[一句话描述发生了什么事]

**设定包**（挂载的 info_release）：
- {key}: {从 L1 提取的具体文本内容}
- {key}: {从 L1 提取的具体文本内容}

**密度标记**：[极高/高/中/低]

**涉及实体**：{实体名}、{实体名}、{实体名}

### 节点 2：[事件简述]
...

---

## 统计数据

- 事件节点总数：{N}
- 唯一实体计数：{N}（要求 ≥ 8）
- 设定包条目数：{N}
- 预估字数：{N}（要求 ≥ 1800）
```

**质量标准**（骨架层QC用）：
```
□ 事件链完整覆盖本章全部不可变事件
□ 每个 info_release 在骨架中有对应的嵌入位置
□ {实体名} 标记 ≥ 8
□ 预估字数 ≥ 1800
□ 无叙事结构决策（不写"这里应该紧张"、"此处为高潮"）
□ 无叙事者评价（不写"主角很愤怒地"）
```

---

### 2. `pop-novel-plot/SKILL.md` — 重写

**2a. Step 3-a 描述更新**
- 第98行"骨架Agent据此从L1文档提取" → 改为"plot Step 3-c 据此从L1提取具体内容"

**2b. Step 3-a 分配原则最后一条更新**
- 第123行"骨架 Agent 凭此从 L1 取实际内容" → 改为"plot Step 3-c 凭此从 L1 取实际内容"

**2c. Step 3-c（新增）** — 在 Step 3-b 与 Step 4 之间插入

```
### Step 3-c：产出事实骨架（新增）

在 act-XX.yaml 每章字段填充完成后执行此步骤。基于 Step 3-a 的 info_release 规划 + L1 设定文档，产出每章的事实骨架。

**输入**：
- act-XX.yaml（含 info_release 数组）
- L1 设定文档（按 info_release.source_doc 读取）

**输出**：写入 act-XX.yaml 每章切片的 `skeleton` 字段

**参考格式**：`templates/事实骨架模板.md`

**执行步骤**：

1. **按 source_doc 从 L1 提取具体内容**
   - 对每条 info_release，读取 source_doc 路径获取设定文本
   - 将设定内容挂载到事件节点作为设定包

2. **按 release_method 决定嵌入方式**
   - "实战展示" → 创建 1 个"该设定被自然验证"的事件节点
   - "角色对话" → 创建 1 个"角色通过对话带出"的节点
   - "叙事者说明" → 标记为【插·设定说明】
   - "探索发现" → 创建 1 个"主角通过观察发现"的节点

3. **按 density 决定展开程度**
   - 集中爆发 → 有独立事件节点
   - 均匀撒放 → 分散到多个节点描述中
   - 埋伏笔 → 只标记现象不标记解释

4. **按模板格式写入每章 skeleton 字段**

**骨架层 QC**：
```
□ 事件链完整覆盖本章全部不可变事件
□ 每个 info_release 在骨架中有对应的嵌入位置
□ {实体名} 标记 ≥ 8
□ 预估字数 ≥ 1800
□ 无叙事结构决策
□ 无叙事者评价
```
不通过 → 退回修改。通过 → 进 Step 4。

❌ 常见错误：
- 事件链中塞入叙事结构决策（"此处应有高潮"）→ 只写"发生了什么事"
- 设定包内容为空 → 必须从 L1 提取实际文本
- 跳过密度标记 → 每个设定包必须标记密度
```

**2d. Step 4 退回指向更新**
- 第202行"退回 → 回 Step 3" → 改为"退回 → 回 Step 3-b"

**2e. Step 5 退回指向更新**
- 第230行"回 Step 3-b" → 保持（正确）

**2f. Step 6 产出物更新**
- 第246-247行：act-XX.yaml 说明更新 → "骨架是 writer 正文渲染的直接消费入口"
- 第248行：自检报告更新 → "含骨架层 QC 结果"

**2g. 质量红线新增**
```
- [ ] ★ **事实骨架已产出** —— 每章有 skeleton 字段，事件链完整 + 设定包完整 + 密度标记完整
```

**2h. 新增「全链路数据流图」**

在核心流程之前或之后插入：

```
## 全链路数据流

plot → writer 的三层框架数据流：

```
plot（设计幕纲）：
  Step 3-a: 扫描 L1 → 分配 info_release 到各章
  Step 3-b: 设计幕纲 → emotional_goal / payoff / 情节线
  Step 3-c: 从 L1 提取内容 → 产事实骨架 → 写入 act-XX.yaml
  → act-XX.yaml（含每章 skeleton + info_release）

writer（正文写作）：
  Director: 读 act-XX.yaml（骨架+info_release）+ 文风DNA
         → 输出设计说明 + 信息释放策略
  ESM before: 从文风DNA动态生成 5 条叙事策略指令
  Pass 2 渲染: 
    Layer 1（骨架+设定包）→ 写什么
    Layer 2（叙事策略指令）→ 怎么分布
    Layer 3（文风DNA+锚定章）→ 怎么落笔
  → 正文 → 自评 → QC → 状态更新
```

各层职责：
| 层 | 谁产出 | 谁消费 | 内容 |
|:---|:------|:-------|:-----|
| Layer 1 | plot Step 3-c | writer Pass2 渲染 | 事件链+设定包+密度标记 |
| Layer 2 | ESM before（writer内） | writer Pass2 渲染 | 叙事策略指令 |
| Layer 3 | deconstructor Step 3-b | writer Director + Pass2 | 5条叙事哲学DNA+锚定章片段 |
```

**2i. WRONG 新增**：跳过 Step 3-c 直接进场景卡

---

### 3. `pop-novel-writer/SKILL.md` — 重写管线段

**3a. 第8行摘要更新**：
```
六阶段管线（三层框架驱动）：Director 设计说明+决策日志（消费 act-XX.yaml 骨架+文风DNA）→ ESM 输入包注入（含骨架+叙事策略指令）→ 正文渲染+自评 → QC → 状态更新。
```

**3b. Step 1 Director 更新**：
- 第89行"指引后续骨架Agent从L1提取" → 改为"骨架已由plot Step 3-c产出，嵌入act-XX.yaml"
- 信息释放策略中：去掉"释放方式（骨架确定嵌入方式）" → plot 已确定

**3c. Step 2：去掉骨架 Agent**：
将当前 Step 2 中的"Layer 1：骨架 Agent 产出纯事实骨架"整块（第112-144行）**删除**。

改为：

```
#### Step 2：ESM 注入（叙事策略指令生成 + 输入组装）

**从文风DNA动态生成叙事策略指令**：

读取文风锚定包中的 DNA（5条叙事哲学原则） → 按当前章节语境生成指令：

① **信息释放节奏指令**（从DNA原则1推导）
   - 根据本章 info_release 项的数量和 density 决定
   - 输出：本章信息释放的总节奏 + 每项信息的释放位置 + 遮蔽策略

② **叙事者姿态指令**（从DNA原则2推导）
   - 根据本章场景类型（战斗/对话/悬疑）决定
   - 输出：POV 距离 + 叙事者是否介入 + 本章不做什么

③ **情感表达指令**（从DNA原则3推导）
   - 根据本章 emotional_goal 决定
   - 输出：情感传达手段 + 高强度段落禁止项 + 动情时刻环境策略

④ **对话策略指令**（从DNA原则4推导）
   - 根据本章对话场景预期占比决定
   - 输出：对话功能 + 引导词频率 + 每轮对话推进维度上限

⑤ **张力控制指令**（从DNA原则5推导）
   - 根据本章在幕情绪弧线中的位置决定
   - 输出：铺垫-释放目标比例 + 章内张力峰值位置 + 章末钩子情感锚点

输出格式：YAML 或 Markdown 块，作为第 13 项注入 Pass 2 渲染。

**ESM before（零LLM）**：组装 14 项输入包：

| # | 来源 | 内容 |
|:-:|:----|:------|
| 0 | project.yaml | 读者画像 reader_profile |
| 1-5 | SQLite / 文件 | 主角/技能/物品/状态变更 |
| 6 | ★ **act-XX.yaml（plot 产出）** | **本章事实骨架（事件链+设定包+密度标记）+ info_release** |
| 7 | 全局摘要 | global-summary.md |
| 8 | 上一章结尾 | 上一章正文最后800字 |
| 9 | Director | 设计说明 + 决策日志 + 信息释放策略 |
| 10 | ★ **文风锚定包 v3.0** | **Layer 1 锚定章片段 + Layer 3 文风DNA** |
| 11 | 经验日志 | 自动匹配的经验教训 |
| 12 | QC 反馈 | 上一轮 QC 报告 |
| **13** | ★ **ESM before** | **叙事策略指令（从 DNA 按本章语境生成的 5 条策略指令）** |
```

**3d. 三层框架消费指南更新**：
- 原"Layer 1：事实骨架 + info_release 实体内容（第①+⑭项）" → 改为"Layer 1：act-XX.yaml 中的事实骨架（第⑥项）"

**3e. 渲染描述更新**：
- 原"接收 15 项输入（含 Layer 1 info_release 实体内容 + Layer 2 叙事策略指令 + Layer 3 文风DNA）" → 改为"接收 14 项输入（含 Layer 1 骨架 + Layer 2 叙事策略指令 + Layer 3 文风DNA）"

**3f. 写后自评第④问更新**：
- 原"对照 info_release（第⑭项）" → 改为"对照 act-XX.yaml 中的 info_release 和骨架"

**3g. 质量红线更新**：
- ❌5 从"事实骨架实体计数 ≥ 8" → 改为"**act-XX.yaml 中本章骨架已存在** — 骨架由 plot 产出，writer 不自行生成"

**3h. 增加全链路数据流图**（与 plot 版本一致）

---

### 4. `Director-prompt.md` 更新

**输入**：
- 去掉"★ 文风锚定包 v3.0（读取 Layer 3：5条叙事哲学DNA原则）"——这仍然是需要的，保留
- "info_release 数组" → 仍保留，但从 act-XX.yaml 直接读取

**前置检查**：
- "★ info_release 已确认" → 保留
- 新增"★ **事实骨架已确认** — 从 act-XX.yaml 读取本章 skeleton，确认事件链完整"

---

### 5. 删除 `Pass1-chapter-planner.md`

整个文件删除。内容完全被 plot Step 3-c + 事实骨架模板取代。

---

### 6. `Pass2-renderer.md` 更新

**输入（14项）**：
```
 0 读者画像
 ① 事实骨架（从 act-XX.yaml 读取：事件链+设定包+密度标记）
 ② context-bundle（实体卡）
 ③ 文风DNA（5条叙事哲学原则 + 应用规则）
 ④ 宪法红线 + 写作禁止清单
 ⑤ 全局摘要
 ⑥ 上一章结尾原文
 ⑦ 导演设计说明 + 决策日志（含信息释放策略）
 ⑧ 锚定章片段
 ⑨ 经验日志
 ⑩ 场景模板
 ⑪ 知识注入 K1-K4
 ⑫ 上一轮QC/QA反馈
 ⑬ 叙事策略指令（ESM before 生成的 5 条）
```

**三层框架消费指南**更新：
- Layer 1 改描述为"act-XX.yaml 中的事实骨架（第①项）——由 plot 产出"

**写后自评第④问**：
- 改为"对照 act-XX.yaml 中的 info_release 确认每条设定信息是否在正文中出现"

**写作后自查**：
- ★ info_release 执行检查 → 改为从 act-XX.yaml 读取

---

### 7. 移动 `文风锚定包模板.md`

**源**：`d:\popwave-skills\skills\pop-novel-writer\styles\文风锚定包模板.md`
**目标**：`d:\popwave-skills\skills\pop-novel-deconstructor\templates\文风锚定包模板.md`

模板描述文案更新：
- 开头"这是开书阶段（bootstrap）产出" → 改为"这是拆书阶段（deconstructor）产出"
- 提取流程描述更新 → "deconstructor Step 3-b 按此模板提取DNA"

deconstructor SKILL.md 中引用路径同步更新。

---

### 8. `pop-novel-deconstructor/SKILL.md` 引用更新

Step 3-b 中的"参考格式"路径从 writer 路径改为 deconstructor 内部路径：
```
**参考格式**：`templates/文风锚定包模板.md`
```

---

## 实施顺序

```
Phase 1: 事实骨架模板.md（新建，独立无阻塞）
Phase 2: plot SKILL.md（重构 Step 3 + 数据流图 + WRONG）
Phase 3: writer SKILL.md（去掉 Pass1、ESM 14项、数据流图）
Phase 4: 删除 Pass1-chapter-planner.md（独立）
Phase 5: Director-prompt.md 更新
Phase 6: Pass2-renderer.md 更新（输入14项）
Phase 7: 文风锚定包模板 → 搬移到 deconstructor
Phase 8: CHANGELOG × 3 + skill.json × 2
Phase 9: git add + commit + push
```

## 兼容性

- 旧版 act-XX.yaml（无 skeleton 字段）→ writer Director 检测后走旧路径：不读骨架，直接用 info_release 自行推断
- 新版 act-XX.yaml（含 skeleton）→ writer 正常消费
- Pass1-chapter-planner.md 删除后，旧管线不会自动调用它（ESM before 直接组装输入包，不依赖 Pass1 存在）
