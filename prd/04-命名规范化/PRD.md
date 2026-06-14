# Skill 命名规范化 PRD

> 版本：v1.0-draft | 日期：2026-06-14 | 状态：草案
> 依赖：[popwave-skill规范 PRD](../../prd/03-popwave-skill规范/PRD.md) §四

---

## 〇、命名公式

```
{领域前缀}-{专家归属}-{功能后缀}

领域前缀: pop | tool | expert
专家归属: writer | decon | shared
功能后缀: kebab-case，说清这 skill 干什么
```

| 位置 | 含义 | 示例 |
|:-----|:-----|:-----|
| `pop-` | 业务域 skill（写作/拆书/发布） | `pop-writer-plot` |
| `tool-` | 通用工具 skill（不属任何专家） | `tool-download-webnovel` |
| `expert-` | 元 skill（调度其他 skill） | `expert-writer` |
| `-writer-` | 服务写作专家 | `pop-writer-creative` |
| `-decon-` | 服务拆书专家 | `pop-decon-extract` |
| `-shared-` | 多专家复用的公共能力 | `pop-shared-dna` |

---

## 一、完整映射

### 1.1 写作专家管辖（11 个）

| 当前目录 | 当前 id | 目标目录 | 目标 id |
|:---------|:--------|:---------|:--------|
| `pop-writer-creative` | `pop-writer-creative` | `pop-writer-creative` | `pop-writer-creative` |
| `pop-writer-world` | `pop-writer-world` | `pop-writer-world` | `pop-writer-world` |
| `pop-writer-continue` | `pop-writer-continue` | `pop-writer-continue` | `pop-writer-continue` |
| `pop-writer-plot` | `pop-writer-plot` | `pop-writer-plot` | `pop-writer-plot` |
| `pop-writer-chapter` | `pop-writer-chapter` | `pop-writer-chapter` | `pop-writer-chapter` |
| `pop-writer-prose` | `pop-writer-prose` | `pop-writer-prose` | `pop-writer-prose` |
| `pop-writer-qa` | `pop-writer-qa` | `pop-writer-qa` | `pop-writer-qa` |
| `pop-writer-character` | `pop-writer-character` | `pop-writer-character` | `pop-writer-character` |
| `pop-writer-html` | `pop-writer-html` | `pop-writer-html` | `pop-writer-html` |
| `pop-writer-game` | `pop-writer-game` | `pop-writer-game` | `pop-writer-game` |
| `expert-writer` | `expert-writer` | `expert-writer` | `expert-writer`（保留） |

### 1.2 拆书专家管辖（2 个）

| 当前目录 | 当前 id | 目标目录 | 目标 id |
|:---------|:--------|:---------|:--------|
| `pop-decon` | `pop-decon` | `pop-decon-extract` | — |
| — | — | `pop-decon-cluster` | — |
| — | — | `pop-decon-world` | — |
| — | — | `pop-decon-engine` | — |
| — | — | `pop-decon-validate` | — |

> ⚠️ deconstructor 拆 5 个子 skill vs 保留一包 — 这是独立 PRD 的活。本次 PRD 先不动 deconstructor，只把当前 02 号映射为 `pop-decon` 站位。

| 当前 | 目标（本次） | 目标（未来拆分后） |
|:-----|:------------|:-----------------|
| `pop-decon` | `pop-decon` | 5 个子 skill 各独立包 |

### 1.3 公共能力（4 个）

| 当前目录 | 当前 id | 目标目录 | 目标 id |
|:---------|:--------|:---------|:--------|
| `pop-shared-dna` | `pop-shared-dna` | `pop-shared-dna` | `pop-shared-dna` |
| `pop-shared-skill-create` | `pop-shared-skill-create` | `pop-shared-skill-create` | `pop-shared-skill-create` |
| `pop-shared-reader` | `pop-shared-reader` | `pop-shared-reader` | `pop-shared-reader` |

### 1.4 工具 skill（保持独立）

| 当前目录 | 目标目录 | 说明 |
|:---------|:---------|:-----|
| `tool-download-webnovel` | `tool-download-webnovel` | 拆书管线前置工具 |
| `tool-opinion-tracker` | `tool-opinion-tracker` | 舆情监控工具 |
| `tool-cnovel-research` | `tool-tool-cnovel-research` | 调研工具 |
| `tool-knowledge-downloader` | `tool-tool-knowledge-downloader` | 知识下载工具 |
| `tool-web-access` | `tool-tool-web-access` | 网络访问工具 |
| `tool-fanqie` | `tool-fanqie` | 番茄小说工具 |
| `pop-shared-book-promo` | `pop-shared-book-promo` | 书宣工具 |
| `pop-shared-html` | `pop-shared-html` | 公共 HTML 渲染引擎 |
| `tool-seo-anything` | `tool-seo-anything` | SEO 工具 |
| `tool-youtube-webbuilder` | `tool-youtube-webbuilder` | YouTube 建站工具 |
| `tool-book-to-skill` | `tool-tool-book-to-skill` | 书转 skill 工具 |
| `tool-feishu-docs` | `tool-tool-feishu-docs` | 飞书文档工具 |
| `tool-prd-builder` | `tool-tool-prd-builder` | PRD 生成工具 |

---

## 二、命名规则

| # | 规则 |
|:-:|:-----|
| 1 | **域名 = 目录名 = skill.json#id**。不三套命名 |
| 2 | **kebab-case 全小写**。`pop-writer-creative`，不是 `popWriterCreative` 或 `Pop_Writer_Creative` |
| 3 | **功能后缀 ≤ 2 词**。`pop-writer-chapter` 足够，不加 `-design`（chapter 本身就意味着设计章纲）；`pop-writer-prose` 足够，不加 `-render` |
| 4 | **编号从命名中彻底移除**。`01-` ~ `13-` 全部消失 |
| 5 | **无 `novel` 中缀**。`pop-novel-` → `pop-writer-` |
| 6 | **expert- 表示元 skill**。`expert-writer`（不叫 `pop-writer-expert` — expert 是调度器，不是工具） |

---

## 三、命中范围

| 命中类型 | 估算数量 | 说明 |
|:---------|:-------:|:-----|
| 目录重命名 | 28 | 所有 skill 根目录改名 |
| skill.json `id` 字段 | 28 | 每份 `{id: "新名"}`  |
| skill.json `pipeline.upstream/downstream` | ~30 | 管线上下游引用全部指向新 id |
| frontmatter `pipeline` 字段 | ~14 | SKILL.md YAML 头 |
| SKILL.md 正文引用 | ~60 | 速查表 / 步骤详情 / 消费关系等段落 |
| expert-writer 路由文件 | 6 文件 | `_shared/pop/ROUTER.md` `POP-CALL.md` `typical-paths.md` 等 |
| validate-skills.mjs | 28 | 注册表 skill 列表 |
| npm 包/其他配置 | ≤5 | `package.json` scripts / CI 配置等 |
| **总计** | **~200** | |

---

## 四、施工方案

### 核心策略

**不手动改 200 处**。用脚本一次性重命名目录 + 全文搜索替换 + 验证。

### 脚本逻辑

```
1. 读取映射表（28 行 old→new）
2. 对每个 skill:
   a. git mv 目录
   b. 更新 skill.json#id
   c. 更新 skill.json#pipeline.upstream/downstream（如果该 id 也在映射表中）
3. 全项目 grep 搜索 28 个 old id → 替换为 new id
   （在 SKILL.md / CHANGELOG.md / _shared/ 文件 / validate-skills.mjs）
4. npm run skills:validate 验证
5. git diff --stat 输出变更清单
```

### 门禁

| # | 条件 |
|:-:|:-----|
| ❌1 | npm run skills:validate 全过 |
| ❌2 | grep 全项目确认无残留 old id |
| ❌3 | SKILL.md 逻辑内容一字不改（纯命名替换） |

---

## 五、不做的事

| 不做 | 原因 |
|:-----|:-----|
| 不动 deconstructor 内部 phase 拆分子 skill | 独立 PRD |
| 不动 creative+world+continue 合并为 bookstrap | 独立 PRD |
| 不动 SKILL.md 逻辑内容 | PRD §九 ❌1 |
| 不动 templates/ 模板文件命名 | 模板名称与 skill 名解耦 |

---

## 六、验收标准

```bash
# 1. 构建通过
npm run skills:validate  # 28/28 ok

# 2. 无残留旧名
grep -r "01-download-webnovel" skills/  # 0 results
grep -r "02-pop-novel" skills/          # 0 results
grep -r "pop-novel-" skills/            # 0 results (except CHANGELOG historical entries)

# 3. 新命名生效
ls skills/pop-writer-plot/SKILL.md      # 可读
ls skills/pop-shared-dna/SKILL.md       # 可读
ls skills/tool-download-webnovel/SKILL.md # 可读
```
