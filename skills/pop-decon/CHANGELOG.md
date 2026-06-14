# CHANGELOG — 02-pop-novel-deconstructor

## v11.0 | 2026-06-14

### 完整重构 —— 一级原则：写作端是甲方

**核心变化**：拆书端的产出格式完全对齐写作端（`.md` 对 `.md`，`.yaml` 对 `.yaml`）。产出镜像项目目录树，和 `pipeline-arch.md` 定义的规范结构完全相同。

### 三级分级体系

| 级别 | 范围 | 耗时 | 产出文件数 |
|:---|:-----|:----|:---------|
| Lv1 快速扫描 | 前20章精读 + 目录跳读 | ~25min | 6个文件（故事引擎+力量体系+角色卡+起/终点快照+拆解摘要） |
| Lv2 标准模板 | 前100章全读 | ~1-3h | ~20个文件（六件套完整+数值体系+全书架构+卷+幕+角色卡） |
| Lv3 工厂级 | 全书 + 03-pop-dna | ~3-8h | ~50+文件（Lv2全部 + 正文分章 + 设计包 + entity-snapshot） |

### 模板系统对齐写作端

14 个模板文件（`templates/*.tpl.md/.yaml`），全部从写作端对应模板克隆：

```
story-engine.tpl.md          → creative phase-0.pe.md 故事引擎.md 5区段模板
L1-01~06.tpl.md              → world phase-1.pe.md 六件套格式
character-lv4.tpl.md         → character-schema Lv4 模板（9节16维）
character-lv3.tpl.md         → character-schema Lv3 模板（6节）
volume-design.tpl.md         → plot templates/volume-design.md
act-skeleton.tpl.yaml        → plot templates/act-skeleton.yaml
combat-capability.tpl.yaml   → world phases/phase-5.pe.md
design-pack.tpl.md           → chapter-design templates/fact-skeleton.md
starting-snapshot.tpl.md     → world phases/phase-6.pe.md
```

### 产出路径对齐项目目录树

- 产出路径从 `_template_library/{skill分类}/` 改为直接镜像 `{项目根}/` 子目录
- 文件名不加 `-template` 后缀——和项目文件同名、同格式、同路径
- Lv3 产出可以直接 cp 到新项目根目录→创作端直接消费

### 相位文件重组

9 个相位文件替代旧的 4 个：

```
phase-s.lv1.pe.md            Lv1 快速扫描
phase-0.sampling.pe.md       Phase 0 分层扫描
phase-1.diagnosis.pe.md      Phase 1 自诊断
phase-2.1.engine.pe.md       Lv2 故事引擎模板
phase-2.2.world.pe.md        Lv2 世界构筑模板
phase-2.3.plot.pe.md         Lv2 剧情架构模板
phase-2.4.characters.pe.md   Lv2 角色卡模板
phase-3.lv3-full.pe.md       Lv3 工厂级深度
phase-4.validate.pe.md       Phase 4 验证+打包
```

### 清理

- 旧文件归档到 `_archive/`：`templates-old/`（T1-T7）、`templates-lv1-old/`、`fragment-pipeline/`
- 旧 `_template_library/` 归档

---

## v10.0.0 | 2026-06-14

- 模板工厂模式。Phase 2 从不带路由的子Skill改为带路由的子Skill再改为不带路由的相位文件（同天迭代3次）

## v9.0.0 | 2026-06-12

- 新增 Phase S 快速拆解（Lv1）
