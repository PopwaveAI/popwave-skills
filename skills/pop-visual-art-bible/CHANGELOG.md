# CHANGELOG — pop-visual-art-bible

## v2.0.0 | 2026-08-08

### 升级为 Art Bible · 美术设定集（由原 pop-visual-character 改名重构）

老板定调：L1 基建层从"character 只设计人物身份"升级为"Art Bible 产出整部美术设定集"。原体系下画风归 style、人物归 character、场景和符号散在 asset，**没有统一 owner 裁决"这个 IP 宇宙看起来整体是什么样"**，三处各画各的必然漂移。Art Bible 成为那个权威 owner——消费 asset（查原文）+ style（定画风），产出统一美术设定集，做跨实体一致性仲裁，冻结为派生层唯一消费的真源。

- **改名**：`pop-visual-character` → `pop-visual-art-bible`，displayName「Art Bible · 美术设定集」
- **产出升级**：从"每角色一张视觉身份卡"升级为"一部美术设定集 `素材/美术设定集.md`"（画风/人物/场景/视觉符号/一致性复现五篇合一，文+图）
- **消费扩展**：原只消费角色档案+画风，现消费 asset 全部资产（角色档案/场景资产表/视觉符号库/IP视觉DNA）+ style 画风
- **新增场景篇**：asset 场景资产表 → 场景形象（意象/氛围/光/构图/可定格帧）
- **新增符号篇**：asset 视觉符号库 → 标志符/器物/阵营符号
- **新增一致性仲裁**：`references/bible-arbitration-guide.md`，三把锁全局互查 + 跨实体冲突裁决
- **步骤重构**：`step0-read-input` / `step1-design-bible`（新）/ `step2-confirm-freeze`（原 confirm-save）/ `step3-reproduce-assets`（原 character-tuning）
- **新增美术设定集模板**：`templates/art-bible.tpl.md`（五篇合一）；保留 `templates/visual-identity-card.tpl.md` 作为人物篇附属
- **铁律升级**：保留原 8 条人物相关，新增 ❌9 画风引用 style 冻结、❌10 场景/符号来自 asset 原文
- **版本同步**：SKILL.md / skill.json 至 v2.0.0

---

# CHANGELOG — pop-visual-character（v1.x 历史，已并入 art-bible）

## v1.5.0 | 2026-08-05

### 定妆按 intent 档位精简（不默认全量双角度）

老板审视全链路发现——对象定妆写死"Pipeline 语境下必做"，只想做封面/OC 的用户也被迫跑双角度定妆 + 完整门禁。改造成 intent 档位分支：

- `SKILL.md` Step 3：新增档位分支——`comic`/`full` → 完整定妆必做（正/侧双角度 + 门禁）；`cover`/`oc` → 轻量定妆可选（基建到身份卡即可派生，不强制双角度；如需参考图渲染单张，agent 自查达标标 `✅ 已认可`）；只做身份设计跳过
- 版本同步：SKILL.md / skill.json 至 v1.5.0

## v1.4.0 | 2026-08-05

### 生图改走 image_generate 工具，移除内置 API Key

老板要求所有 skill 生图环节改用 `image_generate` 工具，清理硬编码 API Key（Pinterest 搜索保持不动）。

## v1.3.0 | 2026-08-04

### 澄清：定妆照 vs 立绘OC（角色生产参考 vs 展示作品）

老板定调：定妆照和立绘OC是两回事——立绘OC有图有字有各种文化元素，定妆照是纯生产参考。新增铁律 ❌8 定妆照是纯生产材料。

## v1.2.0 | 2026-08-04

### 新增：三把锁差异化纪律（角色差异化核心方法）

老板定调：网文角色辨识度低、跨书也低，根因是设计层没建立差异化。差异化不是"加更多细节"，是**在全局让每个角色占一个"唯一"的视觉位置**。新增三把锁差异化纪律（剪影签名/签名色/记忆锚点+分级）、置换测试。

## v1.1.0 | 2026-08-04

### 新增：角色定妆（Pipeline 语境下必做）

新增 `steps/step3-character-tuning.md`：用选定画风 + 身份卡冻结提示词渲染定妆图，身份设计第一次被眼睛看到，用户认可后冻结身份卡为基线资产。

## v1.0.0 | 2026-08-03

**新建 skill：人物形象设计（营销专家基建层）**

填补营销专家管线"人物形象设计"空白。定位：把"这个角色长什么样"这个身份设计一次性做对，产出「角色视觉身份卡」，作为 oc/cover/comic 全下游共用的视觉真源。