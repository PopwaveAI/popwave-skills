# 三层框架改造实施计划

## 摘要

将验证通过的三层框架（纯事实骨架/叙事策略指令/文风DNA）正式纳入pop-novel-plot和pop-novel-writer管线。三个核心改动点：(1) 文风锚定包模板从参数规则升级为叙事哲学DNA提取；(2) plot Step 3 新增info_release字段设计；(3) writer全面升级为三层框架。

---

## 当前管线与断层

```
bootstrap（开书） → deconstructor（拆书） → plot（设计幕纲） → writer（写正文）

断层1：DNA提取用参数规则而非叙事哲学 → 风格还原不准确
断层2：plot设计幕纲时不规划信息释放节奏 → writer不知道每章放什么设定
断层3：writer骨架只产事件链不含设定包 → 正文信息量不足
```

## DNA提取的位置

用户确认：DNA提取放在开书阶段（bootstrap/deconstructor），选锚定书（约3本参考书）时一次提取完成，不每章重复。

---

## 改动清单

### 文件1：`styles/文风锚定包模板.md` — 重写（工作量≈60%）

**当前问题**：参数式结构（复选框+下拉菜单），把风格降格为选项排列组合。
**改造目标**：从参数规则改为5条叙事哲学DNA。

**具体改动**：

1. 保留"一、锚定章片段"（实例层不变），每段新增`叙事哲学印证：{DNA原则编号}`
2. 重写"二、叙事策略"为5条叙事哲学原则，每条含：
   - 信念陈述（一句总结作者的叙事信念）
   - 证据链（来自锚定章的具体表现）
   - 应用规则（可执行的指引）
3. 删除原"三、技法偏好"（复选框式），内容融入DNA原则的应用规则
4. 保留红线清单和字数基线

**5条DNA原则结构**：
```
原则1：信息释放哲学 — 集中/分散/埋伏笔？信息在故事中的角色？
原则2：叙事者姿态哲学 — 隐身的观察者/偶尔介入的讲述者/主动引导的说书人？
原则3：情感表达哲学 — 动作后果/感官堆叠/对话潜文本/内心独白？
原则4：对话策略哲学 — 推进信息/塑造关系/控制节奏？
原则5：张力-释放哲学 — 铺垫与释放比例，张力如何建立与兑现？
```

### 文件2：`pop-novel-plot/SKILL.md` — 增量（工作量≈+80行）

**改动点**：

1. **Step 3 新增子步骤 `Step 3-a：L1 设定目录扫描与 info_release 规划`**
   - 扫描 `01-写作资产/L1设定/` 下所有文件
   - 提取"本幕必须释放的设定知识点"（P0/P1分级）
   - 分配到各章，写入每章切片的 info_release 数组
   - 分配原则：第1章≤2个新概念、连续2章无新信息则第3章追加、同设定不在3章内重复
   - 每个 info_release 标注 source_doc

2. **每章切片新增 `info_release` 字段**
   ```yaml
   info_release:
     - item_id: "力量体系.升级条件"
       title: "突破需要凝聚灵气漩涡"
       source_doc: "01-写作资产/L1设定/力量体系.md"
       release_method: "实战展示"    # 实战展示/角色对话/叙事者说明/探索发现
       density: "集中爆发"
   ```

3. **Step 5 节奏自检新增 `★ 信息释放检查`**：连续无新信息章节≤2章、P0级全部分配、第1章新概念≤2个

4. **Step 6 产出物更新**：说明 info_release 是骨架Agent消费入口

### 文件3：`pop-novel-writer/SKILL.md` — 重写+增量（工作量≈改写40%+新增150行）

**改动点**：

1. **Director 设计说明新增"信息释放策略"**：基于act-XX.yaml当前章的info_release

2. **骨架Agent升级为Layer 1产出**
   - 按 info_release.source_doc 从L1设定文件提取具体内容
   - 按 release_method 嵌入骨架（实战展示→创建事件节点，叙事者说明→标记插槽）
   - 产出格式：事件链 + 设定包 + 密度标记

3. **ESM before 新增 Layer 2 生成逻辑**
   - 从文风DNA（5条叙事哲学原则）动态生成5条叙事策略指令
   - 生成逻辑：读DNA原则 + 当前章节语境 → 输出指令
   - 指令内容：信息释放节奏/叙事者姿态/情感表达/对话策略/张力控制

4. **ESM注入包从13项扩展为15项**
   - 新增第13项：info_release实体内容（骨架Agent从L1提取）
   - 新增第14项：叙事策略指令（ESM before从DNA生成）
   - 编号调整，旧项内容不变

5. **渲染Agent新增"三层框架消费指南"**
   - 消费优先级：Layer1（写什么）→ Layer2（怎么分布）→ Layer3（怎么落笔）
   - 冲突解决规则：骨架优先、DNA其次、叙事策略可降级

6. **写前必读清单追加**：info_release确认 + 叙事策略指令确认

### 文件4：`prompt-templates/Director-prompt.md` — 增量（+20行）
- 设计说明新增"信息释放策略"区块
- 前置检查新增 info_release 确认项

### 文件5：`prompt-templates/Pass1-chapter-planner.md` — 增量（+40行）
- Step 2 新增 info_release 消费步骤（按source_doc提取、按release_method嵌入）
- 设定实体追加到{实体名}计数
- 骨架设计说明新增"信息释放执行"块

### 文件6：`prompt-templates/Pass2-renderer.md` — 增量（+60行）
- 输入表从14项扩展为15项
- 新增"三层框架消费指南"章节（消费优先级+冲突解决规则）
- 写后自评新增第④问（信息释放执行检查）

---

## 实施顺序

```
Phase 1：文风锚定包模板.md（独立，无阻塞）
Phase 2：plot SKILL.md（需Phase 1概念对齐）
Phase 3：writer SKILL.md（需Phase 1+2完成）
Phase 4：Director-prompt.md（需Phase 3）
Phase 5：Pass1-chapter-planner.md（需Phase 3+4）
Phase 6：Pass2-renderer.md（需Phase 3+5）
```

## 兼容性

- info_release 字段可选：旧版 act-XX.yaml 无此字段时骨架 Agent 按原逻辑工作
- 文风锚定包兼容 v2.0（参数式）和 v3.0（DNA式）：ESM before 检测格式后走不同分支
- Pass2 输入项扩展不破坏旧项编号映射

## 验证

1. 用深渊主宰测试用例重新跑一轮：骨架是否能按info_release从原文设定中提取信息
2. 检查ESM before是否能从v3.0文风锚定包生成叙事策略指令
3. 渲染结果是否维持v2实验的差异水平
