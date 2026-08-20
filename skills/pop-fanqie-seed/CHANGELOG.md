# CHANGELOG

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
