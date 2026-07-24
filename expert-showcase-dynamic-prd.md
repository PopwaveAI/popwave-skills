# PRD · 专家展示页动态更新系统

## 一、核心命题

### 问题
专家展示页（当前 `expert-showcase.html`）的三个信息板块——应用场景、工作流程、技能清单——目前全部硬编码在 HTML 中。但实际运行中：

| 信息源 | 更新频率 | 当前状态 |
|:--|:--|:--|
| skill 文件（SKILL.md + skill.json） | git 持续迭代 | 版本号/描述变了，页面不知道 |
| 专家配置（后台管理） | 用户随时改 | 专家增删/skill范围变了，页面不知道 |
| workflow 定义 | 随 skill 变化 | 步骤变多/变少，页面不知道 |

### 目标
skill 文件 git 更新或专家配置变更后，展示页**自动反映最新状态**，无需手动编辑 HTML。

---

## 二、数据架构

### 三层数据模型

```
┌─────────────────────────────────────────────┐
│  第一层：skill 元数据仓库（自动提取）         │
│  数据源：skills/*/skill.json + SKILL.md       │
│  产出：skill-registry.json（全量skill索引）   │
├─────────────────────────────────────────────┤
│  第二层：专家配置（后台管理产出）              │
│  数据源：popwave 后台"专家管理"页              │
│  产出：expert-config.json（专家→skill映射）    │
├─────────────────────────────────────────────┤
│  第三层：展示页渲染（运行时生成）              │
│  数据源：skill-registry.json + expert-config   │
│  产出：动态渲染的专家展示页                    │
└─────────────────────────────────────────────┘
```

### 第一层：skill-registry.json（自动提取）

每次 git pull / 文件变更后，扫描 `skills/*/skill.json`，提取每个 skill 的结构化元数据：

```json
{
  "skills": [
    {
      "id": "pop-qidian-seed",
      "version": "v8.2.0",
      "name": "pop-qidian-seed",
      "description": "起点立项引擎。骨架（力量体系+动力引擎）→主角...",
      "tags": ["骨架", "力量体系", "引擎六组成"],
      "capabilities": ["坐标系五层", "金手指=梗×机制×限制"],
      "phase": 1,
      "expert": "qidian",
      "path": "skills/pop-qidian-seed/",
      "last_updated": "2026-07-22T10:30:00Z"
    }
  ],
  "generated_at": "2026-07-23T14:00:00Z",
  "total": 28
}
```

**提取规则**：
- `id` / `version` / `description`：直接从 `skill.json` 的 `id` / `version` / `description` 字段读取
- `tags` / `capabilities`：从 `skill.json` 新增 `tags` 和 `capabilities` 字段读取（需 skill 作者维护）
- `phase` / `expert`：从 `skill.json` 新增 `phase` 和 `expert` 字段读取
- `last_updated`：取 git log 最后一次修改时间

### 第二层：expert-config.json（后台产出）

后台"专家管理"页保存时生成，描述专家的展示层信息：

```json
{
  "experts": [
    {
      "id": "qidian",
      "name": "起点写作专家",
      "badge": "测试中",
      "description": "面向起点男频小说的全链路涌现式写作引擎",
      "tagline": "创意 → 骨架 → 世界 → 剧情 → 正文 → 审核",
      "skill_ids": [
        "pop-qidian", "pop-qidian-pipeline", "pop-qidian-research",
        "pop-dna-style", "pop-shared-dna", "pop-qidian-seed",
        "pop-qidian-world", "pop-qidian-character", "pop-qidian-plot",
        "pop-qidian-write", "pop-qidian-write-dndlike",
        "pop-qidian-write-onepiece", "pop-qidian-review"
      ],
      "scenarios": [
        { "icon": "A", "label": "新书立项：七维底牌摸底→骨架+首章" },
        { "icon": "B", "label": "连载创作：逐章渲染+write↔review循环" }
      ],
      "workflow": {
        "title": "工作流程 · 步骤 0→6",
        "phases": [
          { "step": "0", "name": "意图深问", "desc": "四层递进+并发前置", "skills": ["pipeline", "research", "dna"] },
          { "step": "1", "name": "骨架+首章", "desc": "力量体系+引擎+创意", "skills": ["seed"] }
        ],
        "loop_text": "↻ write ↔ review 循环：未通过→重写 · 通过→下一章"
      },
      "stats": [
        { "value": "13", "label": "技能", "dynamic": "skill_count" },
        { "value": "7", "label": "步骤", "dynamic": "phase_count" }
      ],
      "theme_color": "#4A6CF7"
    }
  ]
}
```

**关键字段说明**：

| 字段 | 来源 | 更新方式 |
|:--|:--|:--|
| `skill_ids` | 后台"可用 Skill 范围" | 用户在后台增删 skill 时更新 |
| `scenarios` | 后台编辑 | 用户手动维护（场景描述是人工写的） |
| `workflow` | 后台编辑 | 用户手动维护步骤+关联 skill |
| `stats` 中的 `dynamic: skill_count` | 运行时计算 | 从 `skill_ids` 数组长度自动算出 |
| `stats` 中的 `dynamic: phase_count` | 运行时计算 | 从 `workflow.phases` 数组长度自动算出 |

### 第三层：运行时渲染

客户端打开"选择专家"页面时：
1. 读取 `expert-config.json` → 获取专家列表和展示配置
2. 读取 `skill-registry.json` → 获取每个 skill 的最新版本/描述/特性
3. 用 `expert.skill_ids` 做 join → 动态拼装每个专家的技能卡片
4. 渲染 HTML

---

## 三、更新机制

### 场景 1：skill 文件 git 更新

```
git pull → skill.json 变更
    ↓
触发 skill-registry.json 重新生成（扫描 skills/ 目录）
    ↓
客户端下次打开展示页 → 读取新 registry → 版本号/描述自动更新
```

**实现方式（两种可选）**：

| 方案 | 机制 | 优点 | 缺点 |
|:--|:--|:--|:--|
| A. git hook | post-merge hook 触发扫描脚本 | 实时 | 依赖 git 环境 |
| B. 客户端启动时扫描 | popwave 启动时扫描 skills/ 目录 | 不依赖 git | 启动稍慢（<1s） |

**推荐方案 B**：popwave 启动时扫描 `skills/*/skill.json`，生成 `skill-registry.json` 缓存到本地。理由：
- popwave 作为客户端，不保证用户有 git 环境
- 扫描 28 个 json 文件 <500ms
- 避免文件监听的复杂性

### 场景 2：专家配置后台变更

```
用户在后台编辑专家（增删skill/改描述/改workflow）
    ↓
后台保存 → 更新 expert-config.json
    ↓
客户端同步配置（随用户登录/刷新拉取）
    ↓
展示页重新渲染
```

### 场景 3：skill 新增/删除

```
git pull 引入新 skill（如 pop-qidian-write-xianxia）
    ↓
客户端启动扫描 → skill-registry.json 自动包含新 skill
    ↓
用户在后台将新 skill 添加到某专家的 skill_ids
    ↓
展示页自动显示新 skill 卡片
```

---

## 四、skill.json 字段扩展

当前 `skill.json` 只有 `id` / `version` / `description`。为支撑动态渲染，需新增字段：

```json
{
  "id": "pop-qidian-seed",
  "version": "v8.2.0",
  "description": "起点立项引擎。骨架（力量体系+动力引擎）→主角...",
  
  "tags": ["骨架", "力量体系", "引擎六组成", "金手指=梗×机制×限制"],
  "capabilities": ["坐标系五层", "引擎六组成", "金手指=梗×机制×限制"],
  "phase": 1,
  "expert": "qidian",
  "layer": "设计"
}
```

| 新增字段 | 类型 | 用途 | 是否必填 |
|:--|:--|:--|:--|
| `tags` | string[] | 技能卡片的能力标签 | 是 |
| `capabilities` | string[] | 卡片 feature pills（与 tags 可合并） | 否 |
| `phase` | number | 所属步骤号 | 是 |
| `expert` | string | 所属专家 ID | 是 |
| `layer` | string | 功能层分组名 | 是 |

**迁移策略**：现有 skill.json 不强制立即补充。渲染时遇到字段缺失则显示"—"或从 SKILL.md 首行提取 fallback。

---

## 五、客户端渲染流程

### 5.1 页面加载时序

```
用户点击"技能&专家" → 选择"专家"tab
    ↓
Step 1: 读取 expert-config.json → 渲染顶部 tab 卡片（专家名/描述/badge）
    ↓
Step 2: 默认选中第一个专家 → 读取 skill-registry.json
    ↓
Step 3: 用 expert.skill_ids join registry → 渲染三个板块：
        ① 应用场景（从 expert-config.scenarios 读取）
        ② 工作流程（从 expert-config.workflow 读取）
        ③ 技能清单（join registry 动态拼装 skill 卡片）
    ↓
Step 4: 统计数据自动计算（skill_count / phase_count）
```

### 5.2 技能卡片动态拼装伪代码

```javascript
function renderSkillCards(expert) {
  const skills = expert.skill_ids.map(id => {
    const skill = skillRegistry.skills.find(s => s.id === id);
    if (!skill) return null; // skill 文件不存在则跳过
    return {
      name: skill.id,
      version: skill.version,
      desc: skill.description,
      features: skill.tags || [],
      layer: skill.layer || '未分类'
    };
  }).filter(Boolean); // 过滤掉不存在的 skill

  // 按 layer 分组
  const grouped = groupBy(skills, 'layer');
  
  // 渲染分组卡片
  return Object.entries(grouped).map(([layer, items]) => {
    return `<div class="sk-group">...${items.map(renderCard).join('')}...</div>`;
  }).join('');
}
```

### 5.3 skill 不存在的降级处理

| 情况 | 处理 |
|:--|:--|
| skill_ids 中的 id 在 registry 找不到 | 跳过，不渲染卡片 |
| registry 中的 skill 不属于任何专家 | 不显示在展示页（可在"技能"tab 单独查看） |
| skill.json 缺少 tags 字段 | 卡片特性标签区显示"—" |
| skill.json 缺少 phase 字段 | 工作流程图中不标注该 skill |

---

## 六、数据流全图

```
┌──────────────┐     git pull      ┌──────────────────┐
│  git 仓库    │ ───────────────→ │  skills/ 目录    │
│ (skill文件)  │                  │  (本地文件)       │
└──────────────┘                  └────────┬─────────┘
                                           │ popwave启动时扫描
                                           ↓
┌──────────────┐    后台保存      ┌──────────────────┐
│  popwave     │ ───────────────→ │ expert-config    │
│  后台管理     │                  │ .json            │
│ (专家管理页)  │ ←─── 用户编辑 ── │ (专家→skill映射)  │
└──────────────┘                  └────────┬─────────┘
                                           │
                              ┌────────────┴────────────┐
                              ↓                         ↓
                    ┌──────────────────┐    ┌──────────────────┐
                    │ skill-registry   │    │ expert-config    │
                    │ .json            │    │ .json            │
                    │ (自动生成缓存)    │    │ (后台产出)        │
                    └────────┬─────────┘    └────────┬─────────┘
                             │                       │
                             └───────────┬───────────┘
                                         ↓
                              ┌──────────────────┐
                              │ 展示页运行时      │
                              │ join 两数据源     │
                              │ 动态渲染 HTML     │
                              └──────────────────┘
```

---

## 七、与后台管理页的对接

### 7.1 后台需要新增的字段

当前后台"专家管理"表格有：专家名称、描述、可用Skill范围、提示词、排序、启用。

需新增展示配置编辑区（编辑专家时展开）：

| 配置项 | 类型 | 说明 |
|:--|:--|:--|
| 专家标语 | text | hero 下方的一行描述（tagline） |
| 主题色 | color picker | 卡片配色 |
| 应用场景 | array[{icon,label}] | 场景标签列表，可增删 |
| 工作流程标题 | text | 如"工作流程 · 步骤 0→6" |
| 工作流程步骤 | array[{step,name,desc,skills}] | 步骤节点列表 |
| 循环提示 | text | 如"↻ write ↔ review 循环" |
| 统计数据 | array[{label,dynamic}] | 如"技能"=skill_count（自动计算） |

### 7.2 后台保存逻辑

```
用户编辑专家 → 填写展示配置 → 保存
    ↓
后台将配置写入 expert-config.json
    ↓
同时更新 expert-config.json 的 updated_at 时间戳
    ↓
客户端下次同步时拉取最新配置
```

---

## 八、迁移路径

### Phase 1：静态→半动态（当前→短期）

1. 将 `expert-showcase.html` 的硬编码数据提取为 `expert-config.json`
2. skill.json 补充 `tags` / `phase` / `expert` / `layer` 字段
3. 写一个扫描脚本 `generate-registry.py`：扫描 `skills/*/skill.json` → 生成 `skill-registry.json`
4. 展示页改为 JS 动态渲染：读取两个 json → 生成 HTML

**此阶段产出**：展示页不再硬编码，skill 版本更新后只需重新运行扫描脚本。

### Phase 2：半动态→全动态（上机 popwave）

1. popwave 启动时自动运行 `generate-registry`（内嵌，非独立脚本）
2. 后台"专家管理"页新增展示配置编辑区
3. 客户端实时读取 `expert-config.json` + `skill-registry.json` 渲染

**此阶段产出**：用户无感更新——git pull 新 skill 后，下次打开展示页自动反映。

### Phase 3：增量更新（长期优化）

1. 文件监听：skill.json 变更时增量更新 registry（非全量扫描）
2. 热更新：展示页不重启即刷新（WebSocket 推送）
3. 版本对比：skill 版本变化时在卡片上标注"已更新"

---

## 九、风险与约束

| 风险 | 应对 |
|:--|:--|
| skill.json 字段未补充 → 卡片信息缺失 | 渲染层 fallback：缺 tags 显示"—"，缺 phase 不标注 |
| 后台配置与 registry 不同步 | 展示页 join 时过滤无效 skill_id，不影响其他卡片 |
| skill 文件过多导致扫描慢 | 28 个 json <500ms，暂无性能问题；>100 个时改增量更新 |
| 专家配置格式变更 | expert-config.json 加版本号字段，客户端按版本兼容渲染 |

---

## 十、验收标准

1. **skill 版本更新**：修改某 skill.json 的 version 字段 → 重新生成 registry → 展示页该卡片版本号自动更新
2. **skill 新增**：新增 skill.json + 在后台专家配置的 skill_ids 中添加 → 展示页自动出现新卡片
3. **skill 删除**：skill_ids 中移除某 skill → 展示页该卡片消失
4. **专家新增**：后台新建专家 + 配置 skill_ids → 展示页顶部出现新 tab
5. **专家禁用**：后台关闭"启用"开关 → 展示页隐藏该专家 tab
6. **workflow 变更**：后台编辑工作流程步骤 → 展示页流程图自动更新
7. **统计数据**：skill_ids 增删后，hero 区"技能"数字自动变化
