# CHANGELOG

## v2.1.0 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份词"L1 基建第三引擎"→"L1 基建层"，description 精简
- 引语版本信息解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version）

## v2.0.0 — 2026-08-24

### steps 两件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step0-detect / step1-extract 两件全合入 SKILL.md 对应 SOP 节（Step 0 探测+定位+规划 / Step 1 资产提取+门禁+落盘+消费路由）
- **执行模式明确**：原文采样提取（Grep/Read 只读）可派子 agent 执行并回报采样结果、主 agent 整理落盘；角色名单确认与资产确认门禁需用户多轮交互，主 agent 直执
- **内容精炼**：step0 探测信号表与 SKILL.md「两种项目空间」合并去重；写作专家辅助设定表并入「两种项目空间」；§4.0 intent 定深表与 §4.1 产出组合表合并为一张；增量检查/资产索引/资产确认摘要/落盘头部标记压缩为要点；5轮搜索示例表、10维度表、符号扫描表、势力/地理/规则档案三禁止全保留；step1 消费路由表与 SKILL.md art-bible 路由表合并（保留"asset 不调用消费 skill 只告知"注）
- skill.json version 1.2.0→2.0.0

## v1.2.0 | 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v1.2.0。

## v1.1.0 (2026-08-05)

### 资产提取按 intent 档位定深（不默认全量）

老板审视全链路发现——asset 无档位意识，任何意图都全量提取，只想做封面的用户也白白跑深度角色档案。改造成 intent 定深：

- `SKILL.md`：Step 0 产出规划改「按 intent 档位定深」；消费路由表改为按 intent（cover/oc/comic/full/asset-only）+ 基建档位标注
- `steps/step0-detect.md` §4：新增 §4.0 读取 intent 档位定深表；§4.1 产出组合表对齐 intent；§4.2 角色名单按 intent 划定（cover 只提封面角色精简版）
- `steps/step1-extract.md` §7：消费路由对齐 intent 档位
- 规则统一：`comic`/`full` 全量深度；`cover` 场景+符号为主、角色精简；`oc` 角色档案深度、场景精简；`asset-only` 只提指定资产不进派生层
- 版本同步：SKILL.md / skill.json 至 v1.1.0

## v1.0.0 (2026-07-30)

从 `pop-visual-base` 拆分体系中新建的基建 skill。专注从小说原文提取结构化视觉资产，供下游视觉 skill 群消费。

### 核心能力
- **四种资产产出**：角色档案（10维度）、场景资产表（可定格帧清单）、视觉符号库（意象/标志色/器物/阵营符号）、IP视觉DNA（同人时）
- **两种项目空间兼容**：写作专家项目（起点/番茄，有已有设定辅助）+ 独立小说项目（纯原文采样）
- **增量更新机制**：采样范围标记 + 只提取新增章节 + 追加不覆盖
- **消费路由**：资产就绪后告知用户可调用 pop-visual-oc / pop-visual-comic / pop-visual-cover

### 设计理念
- **只提取不生成**：asset 是基建 skill，禁止调用任何图片生成 API
- **与拆书 skill 的区别**：拆书拆"怎么写的"（技法），asset 提"有什么"（素材）
- **原文采样有行号索引**：每条信息可溯源，消费方可定位原文

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-detect.md, step1-extract.md
- references/: asset-extract-guide.md
