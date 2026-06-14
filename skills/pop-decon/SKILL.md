# pop-decon · 拆书管线调度 v12.1.0

> **定位：拆书管线的元 skill。执行管线调度（Phase 1→5），不直接产出文件。**
> **核心约束：按章节量级决定管线长度。前N章跑 Phase 1→2→3，全书跑 Phase 1→2→3→4→5。**

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **故事引擎是终点不是起点** — Phase 1/2/3 完成前不准调用 pop-decon-engine |
| ❌2 | **不跳过 Phase** — 只能顺次推进 Phase 1→2→3→4→5，不得跳号 |
| ❌3 | **跳过提取脚本直接写产出** — Phase 1 执行前必须先运行 extract.py |
| ❌4 | **前N章产出全书文件** — 只拆前100章就不产出 L0-故事引擎/ |
| ❌5 | **子 skill 不可用时静默跳过** — 找不到子 skill → 终止，告知用户 |

---

## 速查表

| 量级 | 范围 | 执行管线 | 触发子 skill | 预期耗时 |
|:-----|:-----|:---------|:------------|:--------|
| **前N章** | 用户指定（默认前100章） | Phase 1 → 2 → 3 | extract → cluster → world | ~1-3h |
| **全书** | 全部章节 | Phase 1 → 2 → 3 → 4 → 5 | extract → cluster → world → engine → validate | ~3-8h |

---

## 管线地图

```
用户: "拆这本书"
    ↓
pop-decon (orchestrator)
    ├── 判断量级: 前N章 or 全书
    ├── 判断文件存在: TXT? _temp/?
    │
    ├── 前N章 → Phase 1: pop-decon-extract    → 角色卡+事实骨架
    │         → Phase 2: pop-decon-cluster     → 卷幕
    │         → Phase 3: pop-decon-world       → L1+宪法+数值
    │
    └── 全书 → Phase 1-3 (同上)
           → Phase 4: pop-decon-engine      → 故事引擎
           → Phase 5: pop-decon-validate    → 产出索引
```

每 Phase 产出 → 消费关系见各子 skill 的 `references/pipeline-context.md`。

---

## 核心流程

### Step 1：判断量级
**做什么：** 询问用户需要拆多少章。默认前100章，用户说"全本/全书/全部/完整"=全书。
**产出：** 前N章 或 全书。**❌ 门禁：** 用户未确认量级 → 退回询问。

### Step 2：执行 Phase 1（强制前置）
**做什么：** 运行 extract.py → 调用 `pop-decon-extract`。所有量级必须跑。
**❌ 门禁：** extract.py 执行失败或 _temp/ 三个 JSON 不全 → 终止，退回修复脚本。

### Step 3：Phase 2-3（前N章+全书）
**做什么：** 依次调用 pop-decon-cluster → pop-decon-world。
**❌ 门禁：** 前一 Phase 产出文件不存在 → 终止退回。

### Step 4：Phase 4-5（仅全书）
**做什么：** 依次调用 pop-decon-engine → pop-decon-validate。
**❌ 门禁：** Phase 1-3 产出不全 → 退回。

### Step 5：完成后引导
输出摘要，告知用户产出位置，询问是否需要转换为写作项目。

---

## 边界条件

| 场景 | 处理 |
|:-----|:-----|
| 前N章跑完后用户要求升级全书 | 重新跑全书 extract → Phase 2-5 |
| extract.py 脚本不可用 | 终止，提示用户确认 Python 环境和依赖 |
| 子 skill SKILL.md 不可读 | 终止，输出具体哪个子 skill 缺失 |
| 用户中途改变量级 | 保存当前阶段产出，用户确认后再切 |

---

## 版本

v12.1.0 | 2026-06-14 | 简化级别体系：Lv1/前N章/全书 → 前N章/全书 → [CHANGELOG.md](CHANGELOG.md)
