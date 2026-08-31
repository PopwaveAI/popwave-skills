# CHANGELOG

## v14.0.2 — 2026-08-31

### stage 合并，下游指向 pop-stage

- 下游列 `pop-world`→`pop-stage`（pop-world+pop-character 再合并为 pop-stage，旧 2 skill 废弃删除）
- skill.json version 14.0.1→14.0.2

## v14.0.1 — 2026-08-31

### world 三族合并，下游指向 pop-world

- 下游列 `pop-fanqie-world`→`pop-world`（旧 fanqie-world 废弃删除，三族合并为 pop-world）
- skill.json version 14.0.0→14.0.1

## v14.0.0 — 2026-08-24

### steps 3件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline（起点系）改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1.md / step2.md / step3.md 三件全部合入 SKILL.md 对应 Phase 节
- **内容合入**：Phase 1（1a七维摸底+路由表/1b底牌闸门/1b-2四路并发/1c市场调研/1c-5题材深度调研/1d-0改编策略含A/B轨prompt/1d双轨发散含好创意六标准/1e十选一）、Phase 2（2a行为引擎+行为框架碰撞/2b金手指三要素合成/2c四眼法/2e故事纲领规则差异四层+三核心质量标准+营销层+自检清单/2f创意.md落盘模板+番茄简介硬约束）、Phase 3（3a加载+笔触三态/3b黄金开篇六法则+反差画面/3c七节拍/3e爽感闭环/3f落盘+交付面板/3g确认+首章自检）全内联
- **执行模式明确**：Phase 1/2/3 用户多轮交互环节（摸底问答/策略选择/10选1/试读确认）主agent直执；1b-2 四路并发（笔触DNA/力量体系拆书/市场调研/扫榜）为只读调研类——派子agent执行回报、主agent落盘消费
- **内容精炼**：2e自检清单13项与质量标准合并（清单保留全部检查项，标准详见上文各核心）；番茄简介写法示例压缩指向 synopsis-guide.md；step3 的 3a 与 3d 笔触协议合一；1b-2 子agent指令全文压缩为派发原则+一条示例指令；速查表/知识地图 steps 引用清除
- skill.json version 13.23.0→14.0.0

---

## v13.23.0 | 2026-08-18

### step2 压缩：showcase示例库+三核心正反例下沉references（26.8KB→19.7KB）

**改动**：
- **step2.md**：2b合成示例库（6条金手指三要素示例）改为指向 references/showcase.md「三要素合成示例」（弱加载，仅2b环节读取）
- **step2.md**：2e三核心正反例（R41-B正例×3+R41反例×3+类型参考表×3）改为指向 references/showcase.md「故事纲领三核心质量对照示例」（弱加载，写各核心前对照校准）
- **references/showcase.md**：追加「三要素合成示例」+「故事纲领三核心质量对照示例」两大节
- 质量标准✓项/硬约束/自检清单/落盘模板全部保留在step2内——门禁不弱化，只沉示例
- skill.json version 13.22.0→13.23.0，版本三处一致

---

## v13.22.0 | 2026-08-13

### 世界新增"类型+风味基调"声明：seed声明、world执行、write注入

**核心改动**：创意.md 与故事纲领核心一新增"世界类型+风味基调"声明（世界类型+命名/器物/社会符号参考系）。seed 声明类型，world 据此执行命名/器物/社会符号，write 每章注入类型声明——杜绝"声明西幻却写出中式味"的类型味漂移。

**改动**：
- **steps/step2.md**：故事纲领核心一新增"世界类型+风味基调"小节（0a世界类型+0b风味基调+硬约束）；故事纲领自检清单新增"世界有世界类型+风味基调吗"检查项；创意.md 落盘模板新增"世界类型+风味基调"字段
- **SKILL.md**：Phase 2 描述新增世界类型+风味基调声明；红线15类型声明红线；版本号同步至 v13.22.0
- **skill.json**：version 13.21.0→13.22.0
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

**核心洞察**：类型味漂移的根因是"声明西幻却用中式命名/器物/社会符号"——seed声明类型+风味基调，world据此执行命名/器物/社会符号并做类型门禁，write每章注入类型声明。三层各司其职，杜绝类型味漂移。

---

## v13.21.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v13.21.0
- **CHANGELOG.md**：新增本条版本记录

---

## v13.20.0 (2026-08-11)

### 新增知识地图 + 触发锚定 + 目录名统一

**背景**：reference 是"可选读物"，agent 默认跳过。试点解法：SKILL.md 加知识地图（强注入必到），写崩级 reference 在 step 内绑触发条件。

**改动**：
- **SKILL.md**：新增「🗺️ 知识地图」区块——reference 读取索引（design-guide🔴写崩级 / synopsis/dna-example/showcase🟡提品级）；目录名 `reference/`→`references/` 统一
- **steps/step2.md**：2e 故事纲领加触发锚定（必读 design-guide.md🔴）；番茄简介加触发锚定（建议读 synopsis-guide.md🟡）
- **skill.json**：version 13.19.0→13.20.0

---

---

> 历史版本条目已归档：`_archive/changelog-history/pop-fanqie-seed/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
