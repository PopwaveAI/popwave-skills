# step1 · 初始化项目目录

> 本文件是 pop-qidian-pipeline 第一步执行指令。

## ⚠️ 前置检测：是否需要走导入/续写模式

**在执行任何创建操作前，先LS扫描项目目录**：

1. 如果 `正文/` 有 ch*.txt/ch*.md 文件，或 `设计/` 有 .md 文件 → **说明用户已有历史资料**，跳转 `steps/step0-import.md` 执行导入/续写模式
2. 如果项目目录为空或仅有 `项目总控.html` → 继续执行下面的正常初始化流程

## 目标

创建标准化项目目录结构 + 项目总控.html，为后续Phase路由做好准备。

**v1.2.0核心变化**：删除project-state.md，项目总控.html是唯一状态文件。agent直接用SearchReplace更新html中的`<!--STATE:xxx -->`标记字段。

## 执行

### 1. 创建完整目录结构（全部一次性创建，含审核/）

用PowerShell一次性创建所有目录（`-Force`确保已存在也不报错）：

```powershell
$dirs = @(
  "素材", "素材/downloads", "素材/知识沉淀",
  "设计", "设计/全书设定", "设计/角色库", "设计/第一卷剧情",
  "正文",
  "审核"
)
foreach ($d in $dirs) {
  New-Item -ItemType Directory -Force -Path $d | Out-Null
}
```

**必须创建的目录清单（8个）**：
- `素材/` + `素材/downloads/` + `素材/知识沉淀/`
- `设计/` + `设计/全书设定/` + `设计/角色库/` + `设计/第一卷剧情/`
- `正文/`
- `审核/`（初始化时就创建，不等Phase 6）

### 2. 创建项目总控.html

读取模板文件 `skills/pop-qidian-pipeline/templates/项目总控.html`，将其内容写入项目根目录的 `项目总控.html`。

然后用SearchReplace更新以下字段：

| 标记 | 替换值 |
|:--|:--|
| `<!--STATE:project_name -->未命名项目<!--/STATE:project_name -->` | `<!--STATE:project_name -->{用户给的项目名}<!--/STATE:project_name -->` |
| `<!--STATE:created_at -->--<!--/STATE:created_at -->` | `<!--STATE:created_at -->{YYYY-MM-DD HH:mm}<!--/STATE:created_at -->` |
| `<!--STATE:updated_at -->--<!--/STATE:updated_at -->` | `<!--STATE:updated_at -->{YYYY-MM-DD HH:mm}<!--/STATE:updated_at -->` |
| `<!--STATE:genre -->待指定<!--/STATE:genre -->` | `<!--STATE:genre -->{用户赛道方向}<!--/STATE:genre -->`（如用户未指定则保留"待指定"） |

### 3. 创建 README.md

简述项目信息 + 管线说明 + 目录结构说明 + 指向项目总控.html。

### 4. 初始化自检（强制执行）

创建完目录和文件后，**必须执行自检**——用LS工具确认以下全部存在：

```
✅ 素材/
✅ 素材/downloads/
✅ 素材/知识沉淀/
✅ 设计/
✅ 设计/全书设定/
✅ 设计/角色库/
✅ 设计/第一卷剧情/
✅ 正文/
✅ 审核/
✅ 项目总控.html
✅ README.md
```

**任何一项缺失=初始化失败**，必须补创后才能进入Phase 0。

## 质量门

- [x] 8个目录全部创建（含审核/和知识沉淀/）
- [x] 项目总控.html已落盘，project_name和timestamp已更新
- [x] README.md已落盘
- [x] 自检通过（11项全部✅）

## 下一步

初始化完成 → 进入 Phase 0 Stage 1 用户意图深问。

加载：`steps/step2.md`
