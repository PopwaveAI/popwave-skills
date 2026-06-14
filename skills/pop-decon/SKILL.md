# pop-decon · 拆书管线调度 v12.0.0

> **定位：拆书管线的元 skill。执行管线调度（Phase 1→5），不直接产出文件。**
> **核心约束：不走捷径。Lv1 只跑 Phase 1，Lv2 跑 Phase 1→2→3，Lv3 跑 Phase 1→2→3→4→5。**

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **故事引擎是终点不是起点** — Phase 1/2/3 完成前不准调用 pop-decon-engine |
| ❌2 | **不跳过 Phase** — Lv2 先 Phase 1 再 2 再 3，不得跳号 |
| ❌3 | **跳过提取脚本直接写产出** — Phase 1 执行前必须先运行 extract.py |
| ❌4 | **Lv2 产出 Lv3 文件** — Lv2 不做故事引擎，不产出 L0-故事引擎/ |
| ❌5 | **子 skill 不可用时静默跳过** — 找不到子 skill → 终止，告知用户 |

---

## 速查表

| 级别 | 范围 | 执行管线 | 触发子 skill | 预期耗时 |
|:-----|:-----|:---------|:------------|:--------|
| **Lv1** | ch1-20 | Phase 1 | pop-decon-extract | ~25min |
| **Lv2** | ch1-100 | Phase 1 → 2 → 3 | extract → cluster → world | ~1-3h |
| **Lv3** | 全书 | Phase 1 → 2 → 3 → 4 → 5 | extract → cluster → world → engine → validate | ~3-8h |

---

## 管线地图

```
用户: "拆这本书"
    ↓
pop-decon (orchestrator)
    ├── 判断级别 (Lv1/Lv2/Lv3)
    ├── 判断文件存在: TXT? _temp/?
    │
    ├── Lv1 → Phase 1: pop-decon-extract    → 角色卡
    ├── Lv2 → Phase 1: pop-decon-extract    → 角色卡
    │      → Phase 2: pop-decon-cluster     → 卷幕
    │      → Phase 3: pop-decon-world       → L1+宪法+数值
    └── Lv3 → Phase 1-3 (同上)
           → Phase 4: pop-decon-engine      → 故事引擎
           → Phase 5: pop-decon-validate    → 产出索引
```

每 Phase 产出 → 消费关系见各子 skill 的 `references/pipeline-context.md`。

---

## 核心流程

### Step 1：判断级别
**做什么：** 判断用户需要的拆解深度。默认 Lv1（ch1-20），用户说"深拆/深度对标"=Lv2，"完整模板/全本"=Lv3。
**产出：** Lv{N}。**❌ 门禁：** 用户未确认级别 → 退回询问。

### Step 2：执行 Phase 1（强制前置）
**做什么：** 运行 extract.py → 调用 `pop-decon-extract`。所有级别必须跑。
**❌ 门禁：** extract.py 执行失败或 _temp/ 三个 JSON 不全 → 终止，退回修复脚本。

### Step 3：Phase 2-3（Lv2+）
**做什么：** 依次调用 pop-decon-cluster → pop-decon-world。
**❌ 门禁：** 前一 Phase 产出文件不存在 → 终止退回。

### Step 4：Phase 4-5（仅 Lv3）
**做什么：** 依次调用 pop-decon-engine → pop-decon-validate。
**❌ 门禁：** Phase 1-3 产出不全 → 退回。

### Step 5：完成后引导
输出摘要，告知用户产出位置，询问是否需要转换为写作项目。

---

## 边界条件

| 场景 | 处理 |
|:-----|:-----|
| Lv2 跑完后用户要求升级 Lv3 | 重新跑 ch1-全书 extract → Phase 2-5 |
| extract.py 脚本不可用 | 终止，提示用户确认 Python 环境和依赖 |
| 子 skill SKILL.md 不可读 | 终止，输出具体哪个子 skill 缺失 |
| 用户中途改变要求 | 保存当前阶段产出，用户确认后再切 |

---

## 版本

v12.0.1 | 2026-06-14 | 拆分为 orchestrator + 5 sub-skills → [CHANGELOG.md](CHANGELOG.md)
