---
name: pop-skill-create
description: Popwave Skill 编写规范和抽象原则指南。定义 Popwave Skill 的双文件结构、场景分类体系、抽象原则（通用跨场景/模板兜底/Agent验收/需求前置思考/版本迭代/产出隔离）。Invoke when user wants to create a new Popwave Skill, or when discussing Skill architecture/standards.
version: 1.0.0
---

# Popwave Skill 编写规范

> 所有 Popwave 下的工具和能力都以 **Skill** 为单位组织。本规范定义了一个合格的 Popwave Skill 应该长什么样——文件结构、抽象原则、边界划分、验收标准。

---

## 一、Skill 是什么

Popwave 的 Skill，是一个**可独立交付的能力单元**：

```
Skill = 一份 SKILL.md（人读指令） + 一个 skill.json（机器元数据）
     + 可选的 scripts/ 和 templates/ 目录（实现）
```

一个 Skill 应该回答三个问题：
- **这个能力在什么场景下该用？**（触发条件）
- **能产出什么？不能产出什么？**（边界）
- **Agent 用之前要做什么准备？**（前置思考）

---

## 二、文件规范

### 2.1 双文件结构（强制）

每个 Skill 必须包含且仅包含两个核心元文件：

```
my-skill/
├── SKILL.md          ← 人读：全部指令、上下文、方法论、模板
├── skill.json        ← 机读：平台用元数据（id/权限/斜杠命令）
├── scripts/          ← 可选：脚本实现
├── templates/        ← 可选：模板文件
└── other-assets/     ← 可选：reports / docs 等
```

**不要**：
- ❌ 不要在 `SKILL.md` 之外再放 `README.md`（功能重叠）
- ❌ 不要单独放 `CHANGELOG.md`（更新日志放 `SKILL.md` 尾部）
- ❌ 不要放 `docs/` 目录（所有说明写进 `SKILL.md`）

### 2.2 skill.json 规格

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `id` | ✅ | 唯一标识，对应目录名 | `"knowledge-downloader"` |
| `entry` | ✅ | 入口文件，固定 `"SKILL.md"` | `"SKILL.md"` |
| `activation.slashCommands` | ✅ | 触发命令数组 | `["knowledge-downloader", "download"]` |
| `permissions` | ✅ | 权限声明 | `{ "network": true }` |

**skill.json 只放机器读的字段，不要放 description / version（这些在 SKILL.md frontmatter 里维护更及时）。**

完整示例：
```json
{
  "id": "my-skill",
  "entry": "SKILL.md",
  "activation": {
    "slashCommands": ["my-skill", "ms"]
  },
  "permissions": {
    "readProjectFiles": true,
    "writeProjectFiles": true,
    "network": true,
    "shell": false
  }
}
```

### 2.3 SKILL.md 规格

#### frontmatter（强制）

```yaml
---
name: my-skill                   # 唯一标识，与目录名和 skill.json id 一致
description: 做什么 + 何时触发。   # 关键字段：Agent 靠这个决定要不要调用你
version: 1.0.0                   # 语义版本号
---
```

`description` 是**最重要的字段**。必须同时包含：
1. **做什么** — 功能的简要描述
2. **何时触发** — Agent 在什么场景下应该调用它

写法示例：
```yaml
# ❌ 差：只说做什么
description: "用户调研工具"

# ✅ 好：做什么 + 何时触发
description: "网文作者社区用户调研。Invoke when user needs to research opinions across Chinese web novel communities."
```

#### 内容组织（推荐顺序）

```
# Skill 标题

> 一句话摘要

---

## 一、概述
## 二、能力范围（矩阵/决策树）
## 三、核心指令/方法论
## 四、模板/产出物标准
## 五、环境准备/前置依赖
## 六、场景工作流
## 七、常见问题/踩坑记录
## 八、更新日志
```

---

## 三、Skill 抽象原则

### 原则 1：追求通用和跨场景能力

一个 Skill 应该覆盖一类场景的**通用能力**，而不是一个具体任务。

```
✅ 好：knowledge-downloader（通用知识获取，支持微信/B站等多种数据源）
❌ 差：wechat-article-downloader（只做微信文章下载，场景狭隘）
```

**判断标准：** 当换个数据源（微信→B站/知乎/小红书）时，Skill 的 Phase B 能否直接复用？如果能，抽象就是成功的。

### 原则 2：通过模板兜底特化场景效果

Skill 提供通用能力，模板（`templates/`）提供场景化的效果兜底。

```
Skill（通用）                        templates/（场景特化）
knowledge-downloader               report-template.md（微信拆解）
                                   subtitle-clean-prompt.md（B站清洗）

pop-write-anything                 大纲模板.md / 章纲模板.md / 人物卡模板.md
```

模板是 Skill 通用能力和场景特化之间的**桥梁**。当需要为一个新场景定制输出格式时，加模板，不改 Skill 核心逻辑。

### 原则 3：Skill 要考虑 Agent 验收部分

每个 Skill 必须定义**什么算「做完了」**的标准：

- **产出物验收** — 输出文件长什么样才算合格？放在哪里？
- **质量验收** — 拆解报告/文章/数据的质量下限是什么？
- **失败处理** — 哪些情况是 Skill 已知的、可以继续的？哪些是必须停下来的？

在 SKILL.md 中明确写出来：
```markdown
## 验收标准

- [ ] 原文 .md 存在于原文/ 目录
- [ ] 拆解报告存在于拆解文/ 目录
- [ ] 报告各章节不为空
- [ ] 如果下载失败 → 记录错误后跳过，继续下一篇
- [ ] 如果无字幕 → 输出导读而非全文
```

### 原则 4：Agent 运用之前，哪怕有 Skill，也要想清楚需求

Skill 不是万能插件。Agent 在调用 Skill 之前，必须：
1. **理解用户真正要什么** — 用户说「下载这篇文章」不一定是只需要原文，可能还要拆解报告
2. **判断 Skill 是否匹配** — 当前场景是否在 Skill 的能力范围内？
3. **确认前置条件** — 这个 Skill 依赖 Chrome/CDP/API Key 吗？都就位了吗？
4. **选择正确参数** — 用 `--no-ocr` 还是 `--album`？输出到哪个目录？

**Skill 不能替代思考。** 在 POP-CALL 阶段就要做这个判断。

### 原则 5：考虑版本迭代定位

SKILL.md 的 `version` 字段遵循语义化版本：

```
主版本.次版本.修订号

主版本：管线重构、输出格式变更、核心逻辑改变
次版本：新增数据源、新增参数、新增模板
修订号：修复、优化文档、调整参数默认值
```

**更新日志必须在 SKILL.md 尾部维护**，而不是单独的文件。每条日志写清楚：
- 改了什么
- 为什么改
- 向后兼容性

### 原则 6：产出物声明 + Skill 隔离

每个 Skill 必须明确声明：
- **产出物** — 脚本输出什么文件、放在哪里、格式是什么
- **依赖** — 运行需要什么（Chrome/CDP/网络/外部API）
- **隔离边界** — 这个 Skill 和别的 Skill 的关系

在 SKILL.md 中用 `produces` 和 `orchestration` 块声明（参考 `_knowledge-downloader`）：

```yaml
orchestration:
  preflight:
    - check Chrome remote-debugging enabled
    - check web-access skill available
  dependencies:
    - web-access
  subagent_required: false

produces:
  - Markdown格式的文章原文
  - 文章配图
  - 结构化拆解报告
```

---

## 四、场景分类规范

所有 Skill 按场景放在 `_工具配置/` 下，分为以下场景组：

| 场景 | 说明 | 示例 |
|------|------|------|
| `create场景/` | 写作/创作/素材采集 | novel-agent-pro, pop-write-anything, _knowledge-downloader |
| `office场景/` | 办公效率 | pop-feishu-office |
| `网站html场景/` | 网页/H5/SEO | pop-html-anything, pop-seo-anything |
| `基础设施/` | 跨场景支撑 | web-access, _shared, **pop-skill-create** |
| `_archive/` | 已过期/学习资料 | 不活跃，仅留存 |
| `储备方案区/` | 产品设计方案 | 非 Skill，仅文档 |

### 分类原则

- **按用户使用场景分，不按抽象层级分** — 用户想「写东西」就找 create 场景，想「处理网页」就找网站html场景
- **基础设施**放的是被其他 Skill 依赖的底层能力
- 新 Skill 加入时必须归入一个场景组，不能放到一级目录

---

## 五、编写检查清单

新建 Skill 时，逐项确认：

- [ ] **双文件结构** — 有 `SKILL.md` 和 `skill.json`
- [ ] **frontmatter** — `name` / `description` / `version` 齐全
- [ ] **description 含触发条件** — Agent 靠它判断该不该调你
- [ ] **skill.json 精简** — 只有机读字段，没有 description/version
- [ ] **无冗余文件** — 没有 README.md / CHANGELOG.md
- [ ] **有验收标准** — 什么算做完了？
- [ ] **有前置检查** — 运行前要确认什么？
- [ ] **有产出物声明** — 输出什么文件？放哪里？
- [ ] **通用跨场景** — 换个数据源/场景，核心逻辑能复用吗？
- [ ] **模板兜底** — 特化效果通过 `templates/` 解决，而非改核心逻辑
- [ ] **版本号** — 语义化版本，更新日志在 SKILL.md 尾部
- [ ] **场景归位** — 放在正确的场景组目录下

---

## 六、示例：cnovel-research（规范示范）

作为规范的本 Skill 自身也是 Popwave Skill：

```
popwave-skills/cnovel-research/
├── SKILL.md          ← ✅ 所有人读内容合并在此
├── skill.json        ← ✅ 只有机读字段
├── reports/          ← 调研报告产出物
└── tools/            ← 爬虫脚本
```

遵循的所有规范：
- ✅ 双文件结构，无 README/CHANGELOG
- ✅ frontmatter 含 description + version
- ✅ 通用跨场景（可调研任意平台话题，不限于网文作者）
- ✅ 模板兜底（`reports/` 中的报告模板）
- ✅ 验收标准（能力范围表明确标注哪些平台能/不能）

---

## 七、更新日志

### 1.0.0 — 2026-05-28

- 初版：Popwave Skill 双文件规范
- 六大抽象原则
- 场景分类体系
- 编写检查清单
- cnovel-research 作为规范示范
