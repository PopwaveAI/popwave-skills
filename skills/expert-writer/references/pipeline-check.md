# pipeline-check.md — 管道前置校验 + 大环节转换自检

> 加载时机：§3.1.6，路由执行前最后一道闸。
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

---

## 一、管道前置校验

> 依赖清单来源：`workspace-index.yaml#pipeline_deps`

```
① 从 workspace-index.yaml#pipeline_deps 读取路由目标的 required + recommended 文件列表

② 逐项检查 required 文件是否存在（Grep/Read 验证路径可达）：
   act-XX.yaml ................ ✅ 存在
   act-XX-人物.md .............. ❌ 缺失 → 停止路由
   constitution.yaml ........... ✅ 存在
   ... 逐项检查完毕

③ 子 skill 文件完整性检查（NEW — 全量加载）：
    → 用 `Get-Content -Encoding UTF8 -Raw` 加载当前路由目标子 skill 的完整 SKILL.md + 全部文档型文件
    → 验证方法：文件字符数 ≥ `(Get-Item '{path}').Length` → 完整
    → 不完整（返回为空或明显偏短）→ ⚠️ 标记 "子skill指令文件不完整，无法安全路由"
       退回 §0.8 协议补全后再校验

④ 逐项检查 recommended 文件（如存在则标注可用，缺失不阻止）：
   combat_capability.yaml ...... ⚠️ 未找到（战斗章建议生成）
   entity-snapshot.yaml ........ ✅ 可用（快照存在且章数一致）
   T5-叙事技法.md .............. ✅ 可用（已注入增强信息）

⑤ 输出校验报告：
   ✅ 全部 required 通过 → 进入 §3.2 Execute
   ❌ 有 required 缺失 → 告知用户缺什么文件、来自哪个上游 Skill
   ⚠️ recommended 缺失 → 告知但不阻止，标注"缺少此数据可能影响质量"
```

---

## 二、大环节转换自检

> 当路由目标跨越管线大环节时执行（bookstrap → plot → chapter-design → prose-render）

```
→ 用 Get-Content -Encoding UTF8 -Raw 读取上一环节的全部产出文件
   （bookstrap 产出的 L1 六件套 / plot 产出的 act-XX.yaml+角色卡 / chapter-design 产出的事实骨架）

→ 自检回答三个核心问题：
   □ 这些文件的深度和融合度，是否足以支撑下一个环节的工作？
     （例：plot 需要从 L1 文件中提取地理信息做地图 → 01-世界蓝图的地理描述是否足够详细？
      prose-render 需要文风DNA和设计包 → 设计包的事件链条是否完整？）

   □ 用户中途追加的所有核心设定（如有）是否被充分融合进了所有相关文件？
     （检查是否有"补丁感"——追加设定是否从结构层面融入，而非末尾段落）

   □ 当前产出物是否存在明显的数据断点，导致下游无法直接开工？
     （例：bookstrap 缺数值体系 → plot 无法做战力推演；L1 缺种族文化描写 → 角色卡缺种族背景）

→ 自检结果处理：
   - 三个问题全部通过 ✅ → 正常路由
   - 有字段/深度不足 ⚠️ → 先退回上一环节做深度展开（Phase 1.2 或等价的展开步骤），再路由
   - 有文件缺失 ❌ → 退回上一环节补全，不直接路由
   - 不确定 → 输出自检报告给用户，让用户判断"这个深度够不够进下一阶段"
```
