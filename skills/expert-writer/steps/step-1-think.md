# step-1-think.md — 感知 + 意图识别 + 管道前置校验

> **读什么**：workspace-index.yaml（若存在）、project.yaml、entity-snapshot.yaml（若存在）
> **产出什么**：项目阶段判断 + 路由目标 + 前置校验报告
> **闸门**：前置条件不满足 → 告知用户，不硬跳

---

## 0. 截断检测协议（所有文件读取强制执行）

每次用 `Get-Content` 或 `Read` 工具加载文件后，先校验完整性再生产下文：

```
1. 读取结果实际字符数 → content.length
2. 文件系统大小 → (Get-Item '{path}').Length  
3. if content.length < file_size × 0.9:
     标记 ⚠️ 截断警告
     回退用 Get-Content -Encoding UTF8 -Raw 重新读取全文
     （不回退用 Read+limit，只回退 Raw 模式）
4. if 同一文件连续 2 次检查不通过:
     终止，告知用户"文件过大需要分段处理"
     绝不基于不完整内容继续执行
```

> 完整协议见 `references/pipeline-manifest.md§截断检测协议`。

---

## 1. 管线锚定与会话恢复协议（每次新会话优先执行）

1. **加载管线合同**：`Get-Content -Raw references/pipeline-manifest.md`（系统级，只读，定义管线硬顺序）
2. **加载项目总控**：检查项目根目录 `项目总控.md`
   - 存在 → 读取，获取 `current_stage` 和 `completed_stages`，与 pipeline-manifest 比对推算出 `next_stage`
   - 不存在（新项目）→ 用 `references/project-master-control.tpl.md` 模板初始化项目总控.md，标记 current_stage=creative
3. **管线断裂检测**：比对 `completed_stages` 中的阶段在 pipeline-manifest 顺序上是否连续
   - 例：completed=[creative, world] 但 reservoir 不在其中 → ⚠️ "管线断裂：reservoir 被跳过"
   - 告知用户断裂风险，询问是否回退补齐
4. 检查 workspace-index.yaml → 获取上次所在阶段和完成状态
5. 如有已完成的产出物 → 向用户展示进度摘要：
   ```
   📊 [项目] | 第N章 | 幕M，上次停在 [阶段]。继续吗？
   ```
6. **不重复提问**。优先读文件获取答案
7. workspace-index.yaml 存在 → 读取。不存在 → 初始化索引
8. 确认项目阶段（空/设定中/写作中/写作后）
9. 若文件缺失 → 告知用户缺什么，不编造

---

## 2. 意图识别

1. 从用户消息提取关键词，对照 SKILL.md 速查表定位目标子 Skill
2. 检查 pipeline 前置条件（见 §3 管道前置校验）
3. 前置条件不满足 → 告知缺什么，路由到缺失 skill
4. **需求质量检查**（写正文时）：情绪弧线位置 / 上一章终→本章始衔接 / 爽点比 / 需求与 plot 一致？

**精简模式**：用户说"直接写/快一点/跳过解释" → 少解释、多执行、保留闸门确认。

**❌ WRONG**：
```
用户说"写正文" → agent 直接开始写，没检查 plot→chapter-design→prose-render 管线
✅ CORRECT：检查上游产出物 → 缺失则路由到缺失 skill
```

---

## 3. 管道前置校验

> 依赖清单来源：`workspace-index.yaml#pipeline_deps`
> 文件分类/消费矩阵速查 → `references/pipeline-arch.md§一`

```
① 从 workspace-index.yaml#pipeline_deps 读取路由目标的 required + recommended 文件列表

② 逐项检查 required 文件是否存在（Grep/Read 验证路径可达）

③ 子 skill 文件完整性检查（全量加载）：
   → 用 Get-Content -Encoding UTF8 -Raw 加载路由目标子 skill 的完整 SKILL.md + 全部文档文件
   → 验证方法：文件字符数 ≥ (Get-Item '{path}').Length → 完整
   → 不完整（返回为空或明显偏短）→ ⚠️ 标记"子skill指令文件不完整，无法安全路由"
       退回 §0.8 协议补全后再校验

④ 逐项检查 recommended 文件（如存在则标注可用，缺失不阻止）

⑤ 输出校验报告：
   ✅ 全部 required 通过 → 进入 Execute
   ❌ 有 required 缺失 → 告知用户缺什么文件、来自哪个上游 Skill
   ⚠️ recommended 缺失 → 告知但不阻止，标注"缺少此数据可能影响质量"
```

### 大环节转换自检

> 路由目标跨越管线大环节时执行（bookstrap → plot → chapter-design → prose-render）

```
→ 用 Get-Content -Encoding UTF8 -Raw 读取上一环节的全部产出文件
   （bookstrap 产出的 L1 六件套 / plot 产出的 act-XX.yaml+角色卡 / chapter-design 产出的 chXXX-设计包.md）

→ 自检回答三个核心问题：
   □ 这些文件的深度和融合度，是否足以支撑下一个环节的工作？
     （例：plot 需要从 L1 文件中提取地理信息做地图 → 01-世界蓝图的地理描述是否足够详细？
      prose-render 需要文风DNA和设计包 → 设计包的事件链条是否完整？）

   □ 用户中途追加的所有核心设定（如有）是否被充分融合进了所有相关文件？
     （检查是否有"补丁感"——追加设定是否从结构层面融入，而非末尾段落）

   □ 当前产出物是否存在明显的数据断点，导致下游无法直接开工？
     （例：bookstrap 缺数值体系 → plot 无法做战力推演；L1 缺种族文化描写 → 角色卡缺种族背景）

→ 自检结果处理：
   ✅ 三个问题全部通过 → 正常路由
   ⚠️ 有字段/深度不足 → 先退回上一环节做深度展开（Phase 1.2 或等价的展开步骤），再路由
   ❌ 有文件缺失 → 退回上一环节补全，不直接路由
   ❓ 不确定 → 输出自检报告给用户，让用户判断"这个深度够不够进下一阶段"
```
