# Skill 设计规范

> 本文件是 Popwave Skill 设计规范的完整正文。创建或改造 skill 时必读。

---

## 一、格式规范

### frontmatter

SKILL.md 开头 YAML frontmatter **不超过 4 行**：

```yaml
---
name: my-skill
description: "当用户说'做X/做Y'时启用。产出来物供给下游管线。"
---
```

❌ 不在 frontmatter 放 version/tags/category/orchestration/dependencies/produces/display_name。全部移入 skill.json 或正文。

### description 写法

```
❌ 差：description: "用户调研工具"
❌ 差：description: "五模式设计：模式A→B→C→D→E"
✅ 好：description: "当用户说'调研/社区/什么火'时启用。产出调研报告供给下游管线。"
```

必须含"当用户说…时启用"或"Invoke when…"触发条件。说明做什么 + 何时触发 + 产出给谁。

### skill.json 规格

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | ✅ | 唯一标识，与目录名一致 |
| `version` | ✅ | 语义化版本号，与 SKILL.md + CHANGELOG 一致 |
| `displayName` | ✅ | 中文显示名 |
| `description` | ✅ | 触发条件式描述 |
| `entry` | ✅ | 固定 `"SKILL.md"` |
| `activation.slashCommands` | ✅ | 触发命令数组 |
| `permissions` | ✅ | 权限声明 |

```json
{
  "id": "my-skill",
  "version": "1.0.0",
  "displayName": "我的技能",
  "description": "当用户说'做X/做Y'时启用。产出来物供给下游管线。",
  "entry": "SKILL.md",
  "activation": {
    "slashCommands": ["my-skill", "做X"]
  },
  "permissions": {
    "readProjectFiles": true,
    "writeProjectFiles": true
  }
}
```

---

## 二、内容定位（SOP 骨架 + 五类资源）

```
my-skill/
├── SKILL.md          ← 骨架层：做什么 + 怎么运作（SOP骨架）+ 红线 + 速查表，≤100行
├── skill.json        ← 机读：平台元数据
├── CHANGELOG.md      ← 变更历史
├── steps/            ← 展开层：复杂步骤的详细操作指令，50-150行/文件
├── references/       ← 知识层：读后理解，指导操作（SOP、规范）
├── templates/        ← 模板层：复制填充，直接产出（空模板）
└── scripts/          ← 代码层：可执行脚本、工具代码、批处理逻辑
```

| 层级 | 职责 | 行数目标 |
|:-----|:-----|:---------|
| 骨架层 (SKILL.md) | 告诉 agent "做什么 + 怎么运作"——SOP骨架、红线、速查表、版本 | ≤100 行 |
| 展开层 (steps/) | 复杂步骤的完整操作指令 | 50-150 行/文件 |
| 知识层 (references/) | 方法论、规范参考（读后理解） | 按需加载 |
| 模板层 (templates/) | 空模板、示例（复制填充产出） | 按需加载 |
| 代码层 (scripts/) | 可执行脚本、工具代码、批处理逻辑 | 按需执行，必要时阅读 |

**SKILL.md 是完整骨架，不是纯路由表。** 它必须自包含：这个 skill 做什么、怎么运作（step1~n 简述）、断裂级红线、全文件速查表。错误示例、详细方法论、长模板、复杂操作展开再下沉到 `steps/` 或 `references/`。

### steps/ vs references/ vs templates/ vs scripts/ 区别

| 目录 | 定位 | 使用方式 | 典型文件 |
|:-----|:-----|:---------|:---------|
| `steps/` | 展开层 — 执行细节 | 按阶段阅读，照步骤执行 | 多阶段操作、复杂门禁、长流程 |
| `references/` | 知识层 — 读后理解 | 阅读理解，指导操作 | 搜索SOP、调用规范、设计原理 |
| `templates/` | 模板层 — 复制填充 | 复制→填充→产出文件 | 空白模板、输出格式骨架 |
| `scripts/` | 代码层 — 运行或改造 | 执行、测试、必要时阅读源码 | Python/JS 脚本、CLI 工具、批量转换器 |

❌ 模板文件不放 references/。❌ SOP 文件不放 templates/。❌ 可执行代码不放 references/templates 根下。❌ 不放 README.md。

### 文件拆分原则

**references/templates/scripts**：越细越好——agent 只在需要时读或执行对应文件，不拆 = 每次全读浪费 token。

**steps/**：按独立阶段拆，不按步骤拆。

| 该拆 ✅ | 不该拆 ❌ |
|:--------|:----------|
| 有用户确认断点（天然分水岭） | 连贯推导链中间硬切 |
| 两个阶段彼此独立 | 两个阶段必须顺序执行且共享上下文 |
| 一个阶段可以反复执行 | 一次性线性流程 |

**scripts/**：只有重复性强、容易写错、需要确定性执行的逻辑才放。脚本必须有清晰入口、参数说明，新增或修改后至少跑一个代表性样例。

拆分决策：SKILL.md 骨架是否足够执行？→ 不足则补骨架 / 单步过长？→ 进 steps / 需要读后理解？→ 进 references / 需要复制填充？→ 进 templates / 需要运行代码？→ 进 scripts。

---

## 三、SKILL.md 骨架指引

### SKILL.md 内容组织（推荐顺序）

```
# 标题
> 一句话摘要

## 这个 Skill 做什么        ← 2-3句说明职责、边界、产物
## 怎么运作                 ← step1~n 简述，每步说明动作和产出
## ❌ 质量红线              ← 断裂级约束，第一条必须是读取协议
## 速查表（全文件目录引导）  ← 列出所有文件及读取/执行时机
## 强弱加载保障             ← 声明 SKILL.md 是强保障，资源文件是弱保障
## 版本（指向 CHANGELOG.md）
```

内容优先级：**做什么 → 怎么运作（SOP骨架）→ 红线 → 速查表**。如果 SKILL.md 放不下，优先压缩红线和速查表，保住 SOP 骨架。

### 速查表设计方法

速查表 = 全文件目录引导，不只是模式路由。让 agent 一看速查表就知道每个文件什么时候读、什么时候执行。

```markdown
| 我要 | 读/执行什么文件 | 什么时候用 |
|:-----|:----------|:----------|
| {操作A} | `steps/step-1-xxx.md` | {触发条件} |
| {查规范} | `references/xxx.md` | {触发条件} |
| {填模板} | `templates/xxx.md` | {触发条件} |
| {跑工具} | `scripts/xxx.py` | {触发条件} |
```

### step 文件自传导

step 文件末尾不仅加门禁，还写明"下一步做什么+怎么触发"：

```markdown
---

## ⛔ 加载门禁 + 下一步指引

> 在加载下一 step 文件前，禁止产出任何文件。
>
> 下一 step：`steps/step-{N+1}-xxx.md`
> 加载指令：`Get-Content -Encoding UTF8 -Raw steps/step-{N+1}-xxx.md`
> 什么时候进入下一步：{触发条件}
```

---

## 四、精简原则

### 红线≤7条

只有违反后会**断裂下游流程**的才是红线。格式细节、风格偏好降级为检查清单。

| 是红线 ✅ | 不是红线 ❌ |
|:---------|:-----------|
| 读取协议（截断会丢内容） | frontmatter 不超过4行（格式偏好） |
| 双文件结构（缺文件平台无法注册） | description 含触发词（写法要求） |
| 版本三处一致（不一致导致 registry 错乱） | 红线在第一屏（布局建议） |

### 注意力预算

每份文档/模板都有"最值钱的部分"。识别它，把篇幅和字段密度给它，而不是均匀分配。

- 识别核心价值：写模板前先问——下游最依赖的是哪个段？那个段就是核心
- 核心段占比 ≥ 30%：不足 → 辅助段该删的删、该并的并
- 禁止均匀分配：不要每个段都给一样多的空间——那是登记表不是设计文档

### 信息不重复

同一信息在 SKILL.md 中只出现一次。步骤总表已列"读什么/产出/门禁"，就不在加载门禁、核心流程中再各写一遍。需要强调时引用而非复制。

---

## 五、强弱加载保障

| 保障类型 | 文件 | 机制 | 可靠性 |
|:---------|:-----|:-----|:-------|
| 强保障 | 元 skill 的 SKILL.md | host 层每次 run 强制注入 | 100% |
| 弱保障 | steps/references/templates/scripts | agent 按 SKILL.md 指引主动读取或执行 | 天然弱 |

**设计原则**：

1. 设计 SKILL.md 时假设 step 文件可能没被读到
2. 关键流程必须在 SKILL.md 的 SOP 骨架中自包含——不依赖"agent 会去读 step 文件"
3. 435 runs 数据证明：3 轮对话后 skill 文件读取率降至 0-3%
4. 如果某个约束断裂后果严重，把它提升到 SKILL.md 红线中（强保障），而不是放在弱保障资源里

---

## 六、创建流程

1. 向用户确认 skill 名称和职责
2. 创建目录 `{skill-name}/`
3. 创建 `SKILL.md`（≤100 行，按内容组织顺序）
   - 必须包含"这个 Skill 做什么"和"怎么运作"两段
   - "怎么运作"写 step1~n 简述，让 agent 不读外部文件也知道完整流程
   - 红线第一条必须是读取协议
   - 速查表必须是全文件目录引导
4. 创建 `skill.json`（按规格）
5. 创建 `CHANGELOG.md`（初始 v1.0.0）
6. 如有 steps/references/templates/scripts 需求，创建对应一级目录
7. 对照检查清单逐项验证
8. 输出创建完成报告（文件路径列表）

---

## 七、改造流程

1. **先读全文** — 用 `Get-Content -Encoding UTF8 -Raw` 读取目标 skill 的 SKILL.md + skill.json + CHANGELOG
2. **输出扫描报告** — 对照检查清单标记违规项 + 证据行号，交用户确认
3. **只改结构/格式/红线位置/资源归位** — 不动核心方法论和业务逻辑；发现代码散落时归入一级 `scripts/`
4. **版本 +1** — SKILL.md + skill.json + CHANGELOG 三处同步
5. **输出 BEFORE/AFTER 对比报告** — 用户需要知道改了什么

---

## 八、检查清单

### 格式检查

- [ ] frontmatter ≤ 4 行，只保留 name + description
- [ ] description 含触发条件（"当用户说…时启用"）
- [ ] skill.json 字段完整（id/version/displayName/description/entry/activation/permissions）
- [ ] 版本三处一致（SKILL.md + skill.json + CHANGELOG）

### 结构检查

- [ ] SKILL.md ≤ 100 行，包含完整 SOP 骨架，不只是路由表
- [ ] "这个 Skill 做什么"说明职责、边界、产物
- [ ] "怎么运作"覆盖 step1~n 的动作和产出
- [ ] 红线在第一屏，第一条是读取协议
- [ ] 红线 ≤ 7 条（违反后断裂下游的才叫红线）
- [ ] 执行细节下沉到 steps/，知识层下沉到 references/
- [ ] 模板文件放 templates/，SOP 放 references/
- [ ] 可执行代码、工具脚本、批量处理逻辑放 scripts/

### 加载门禁检查

- [ ] 速查表是全文件目录引导（列出所有文件及读取/执行时机）
- [ ] 有独立 step 文件的 skill，SKILL.md 有强弱加载保障声明
- [ ] step 文件末尾有加载门禁 + 下一步指引
- [ ] scripts/ 中新增或修改的代表性脚本已实际运行验证

### 文档质量检查

- [ ] 识别核心价值段，核心段占比 ≥ 30%
- [ ] 同一信息不重复出现
- [ ] 无深层嵌套（拍平为 3-6 步扁平流程）
- [ ] 无第二人称（"You should"改为祈使句）

---

## 九、落盘检查点

| 确认项 | 状态 |
|:-------|:----:|
| `{skill-id}/SKILL.md` 已写入 | [ ] |
| `{skill-id}/skill.json` 已写入 | [ ] |
| `{skill-id}/CHANGELOG.md` 已写入 | [ ] |
| `{skill-id}/steps/` 目录存在（多步骤 skill） | [ ] |
| `{skill-id}/references/` 存在（需方法论支撑） | [ ] |
| `{skill-id}/templates/` 存在（需模板文件） | [ ] |
| `{skill-id}/scripts/` 存在（需代码工具） | [ ] |

---

## 十、异常与边界条件

| 场景 | 触发条件 | 处理动作 |
|:-----|:---------|:---------|
| 文件/依赖缺失 | 路径无效 | 告知用户，**不准编造数据** |
| 外部工具不可用 | 工具未安装 | 降级方案 |
| 用户中途改变需求 | 用户改变指令 | 暂停当前流程，确认后继续 |
| skill.json 缺失 | 新建时未创建 | 必须补建，不能只有 SKILL.md |
