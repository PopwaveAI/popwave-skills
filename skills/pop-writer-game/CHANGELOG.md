# CHANGELOG — 13-pop-novel-game

> 版本规则：主版本.次版本.修订号
> 每次调优产生一个新版本号

---

## v2.0.2 (2026-06-14)

**根因**: v5 结构化重构 — SKILL.md 过长（406行），存在重复目录 `方法/`，缺少 steps 拆分、drop check 和 pipeline 字段
**类型**: 重构

**改动**:
- **【目录清理】删除重复 `方法/` 目录** — 与 `references/` 内容完全重复，统一使用 `references/`
- **【SKILL.md 瘦身】406行 → 121行** — 详细方法论移至 steps/ 文件，SKILL.md 仅保留速查表、红线、错误示例、异常边界、drop check
- **【steps 拆分】新增两步文件**:
  - `steps/02-文游设计.md` — Phase B 完整流程（6维度设计 + 主持指令模板）
  - `steps/03-产出生成.md` — Phase C 完整流程（HTML设计规范 + API协议 + 实战陷阱 + 验证清单）
- **【SKILL.md 路径修正】所有 `方法/` 引用 → `references/`**
- **【红线下沉】保留 6 条红线于 SKILL.md，移除独立的纪律列表（纪律已分布到各 step 文件和 references）**
- **【产量验收下沉】产出物验收清单下沉到 `steps/03-产出生成.md`（验证清单章节）**
- **【新增 Drop Check 表】三个检查项：上游 skill 存在性、references 可读性、steps 可读性**
- **【skill.json 新增 pipeline 字段】**: `upstream: ["10-pop-novel-prose-render"]`, `downstream: []`
- **【版本号更新】**: v2.0.1 → v2.0.2

**效果**: 符合 v5 规范 — SKILL.md ≤150行、步骤化拆分、红线下沉、drop check 就位、pipeline 依赖声明完整、无重复内容

---

## v2.0.1 (2026-06-04)

**根因**: API key 安全泄露风险 + SKILL.md 结构缺失质量保障体系
**类型**: 安全修复 / 文档重构

**改动**:
- **【安全修复】移除硬编码 API key** — frontmatter 中 `api.key` (`sk-3c03febdfee3442193d4f5f0bd3b766a`) 已彻底删除；frontmatter 精简为仅 name + description（3 行）；新增 `### API 配置` 章节，明确要求通过 `$env:DEEPSEEK_API_KEY` 环境变量或交互式提示注入，SKILL.md 中不存储任何真实 key
- **新增「❌ 质量红线」** — 5 条 [] checkbox：不准硬编码 API key / HTML 验证 pre-delivery / Phase A 必须产出结构化 JSON / 不准编造设定 / 视觉风格匹配世界调性
- **新增「❌ 错误示例」** — 展示 WRONG 模式（API key 硬编码 frontmatter）及其问题分析 + 正确做法
- **新增「产出物验收」** — 5 条 [] checkbox 覆盖所有交付物
- **新增「异常与边界条件」表** — 8 个场景（文件缺失 / API 失败 / HTML 验证失败 / 空输入 / 指令章节为空 / 目录冲突 / 用户要求去 API / 反引号未转义）
- **纪律第 10 条重写** — 从"演示场景直接写入真实 key...注意勿提交"改为"禁止硬编码在 SKILL.md 或方法文档中"
- **产出路径更新** — AI文游.html 从根目录移至 `互动/` 子目录
- **版本号更新** — v2.0.1，底部新增版本脚注
- **skill.json 版本同步** — 1.0.0 → 2.0.1

**效果**: 消除 API key 泄露风险，建立可审计的质量红线和边界处理体系，规范文件结构

---

## v2.0.0 (2026-06-03)

**根因**: —（初始版本记录）
**类型**: —
**改动**: 当前稳定版本。小说互动游戏引擎，基于叙事分歧的 AI 文游。
**效果**: —
