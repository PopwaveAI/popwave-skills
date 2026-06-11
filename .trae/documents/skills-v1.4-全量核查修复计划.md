# Skills v1.4 全量核查修复计划

## 摘要

全量扫描 25 个 skill 的 SKILL.md / steps/ / templates/ / references/ / phases/，比对 PRD v1.4 定义的路径规范，找出"以为修了实际没修"的残留引用并修复。

## 当前状态分析

### 已确认的问题文件（非 CHANGELOG，非 deprecated）

| # | 文件 | 问题 | 行 |
|:--|:-----|:-----|:--|
| 1 | `pop-novel-bookstrap/phases/phase-r4.pe.md` | `02-大纲/volume-XX.md` → 应为 `设计/卷/` | 18,19,25,26 |
| 2 | `pop-novel-bookstrap/phases/phase-3.pe.md` | project.yaml 模板中 `outline: "02-大纲/"` | 23 |
| 3 | `pop-novel-bookstrap/phases/phase-r5.pe.md` | `02-大纲/卷XX/剧情脉络.md` / `02-大纲/伏笔追踪.md` → 旧路径 | 17,18,24,25 |
| 4 | `pop-novel-chapter-design/steps/step-1-read-canvas.md` | 注释中仍提 `constitution.yaml` | 142 |

### 已确认干净的 Skill（零命中旧路径）

| Skill | 状态 |
|:------|:----|
| pop-novel-qa | ✅ 干净 |
| pop-novel-character-schema | ✅ 干净 |
| pop-novel-game | ✅ 干净 |
| pop-reader-making | ✅ 干净 |
| pop-book-promo | ✅ 干净 |
| pop-html-anything | ✅ 干净 |
| download-webnovel-txt | ✅ 干净 |
| cnovel-research | ✅ 干净 |
| book-opinion-tracker | ✅ 干净 |
| knowledge-downloader | ✅ 干净 |
| feishu-docs | ✅ 干净 |
| prd-builder | ✅ 干净 |
| pop-skill-create | ✅ 干净 |
| web-access | ✅ 干净 |
| book-to-skill | ✅ 干净 |
| pop-YouTubewebbuilder | ✅ 干净 |
| pop-seo-anything | ✅ 干净 |

### 项目特定代码（不做修改）

| 文件 | 内容 | 原因 |
|:-----|:-----|:-----|
| pop-novel-html-renderer/*.py | constitution.yaml 硬编码引用 | 属于具体项目的集成代码（鬼游戏/诡异游戏），不是 skill 规范层 |

## 修改计划

### Pass 1: pop-novel-bookstrap/phases/phase-r4.pe.md

**问题**：逆向提取步骤引用 `02-大纲/volume-XX.md` 和 `02-大纲/act-XX.yaml`  
**改为**：`设计/卷/volume-XX.md` 和 `设计/幕/vol-XX/act-YY.yaml`

| 行 | 旧值 | 新值 |
|:--|:-----|:-----|
| 18 | `02-大纲/volume-XX.md`：每卷的地理总览+时空规则 | `设计/卷/volume-XX.md`：每卷的地理总览+时空规则 |
| 19 | `02-大纲/act-XX.yaml`：每卷内的幕结构还原 | `设计/幕/vol-XX/act-YY.yaml`：每卷内的幕结构还原 |
| 25 | `02-大纲/volume-XX.md` | `设计/卷/volume-XX.md` |
| 26 | `02-大纲/act-XX.yaml` | `设计/幕/vol-XX/act-YY.yaml` |

### Pass 2: pop-novel-bookstrap/phases/phase-3.pe.md

**问题**：project.yaml 模板中 `outline: "02-大纲/"`  
**改为**：去掉 `outline` 行——新目录结构中没有单独的"大纲"目录，设计文件在 `设计/卷/` + `设计/幕/`，角色在 `状态/`。或者改为 `outline: "设计/"`。

| 行 | 旧值 | 新值 |
|:--|:-----|:-----|
| 23 | `outline: "02-大纲/"` | `outline: "设计/"` |

### Pass 3: pop-novel-bookstrap/phases/phase-r5.pe.md

**问题**：卷大纲确认步骤引用 `02-大纲/` 路径  
**改为**：对齐新目录结构

| 行 | 旧值 | 新值 |
|:--|:-----|:-----|
| 17 | `02-大纲/卷XX/剧情脉络.md` | `设计/全书架构.md` + `设计/卷/volume-XX.md` |
| 18 | `02-大纲/伏笔追踪.md`（从事件日志汇总） | `状态/`目录下角色卡快照 + `entity-snapshot.yaml` event_log |
| 24 | `02-大纲/卷XX/剧情脉络.md` | `设计/全书架构.md` + `设计/卷/volume-XX.md` |
| 25 | `02-大纲/伏笔追踪.md` | `状态/`目录 角色卡快照段 |

### Pass 4: pop-novel-chapter-design/steps/step-1-read-canvas.md

**问题**：注释说"无需另读 constitution.yaml"  
**改为**：去掉这句话——constitution 已经不存在了，提它反而让人疑惑

| 行 | 旧值 | 新值 |
|:--|:-----|:-----|
| 142 | `已隐含所有约束——无需另读 constitution.yaml` | `已隐含所有约束` |

## 假设与决策

- CHANGELOG.md 中的旧路径引用是有意保留的历史记录，不修改
- `deprecated/` 目录下的文件标注"已废弃"是正确的，不修改
- `优化PRD.md`（bookstrap）是纯历史文档，不修改
- pop-novel-html-renderer 中的 constitution 引用属于具体项目的业务代码，不在此次修复范围

## 验证步骤

1. Pass 1-4 逐文件修改
2. 对每个修改文件执行 `git diff` 确认仅变更预期行
3. 全文搜索 `02-大纲|constitution.yaml`（排除 CHANGELOG/优化PRD/deprecated）确认清零
4. `git commit` + `git push`
