# step0 · 初始化视觉项目

> 本文件是 pop-visual-pipeline 第一步执行指令。state=init 且无已有文件时执行。

## 目标

创建标准目录 + 生成 `视觉项目总控.html` + 自检。只做地基，不干活。

## 执行

### 1. 项目空间探测

| 探测信号 | 项目类型 | 原文路径 | 处理 |
|:---------|:---------|:---------|:-----|
| `项目总控.html` | 写作专家·起点 | `正文/ch*.txt` | import 模式，走 step1 |
| `project-state.md` | 写作专家·番茄 | `正文/ch*.txt` | import 模式，走 step1 |
| `原料/小说原文/` | 独立小说项目 | 单个完整 txt | init 模式 |
| 用户指定路径 | 临时模式 | 指定文件 | init 模式 |

- 若检测到已有项目文件 → 转入 `steps/step1-import.md`
- 若是全新项目 → 继续本 step

### 2. 创建标准目录

在项目根目录创建以下目录（用 LS 确认，不存在则创建）：

```
{项目}/正文/
{项目}/素材/视觉资产/
{项目}/素材/风格/
{项目}/素材/视觉/
{项目}/素材/ref-cache/
{项目}/漫画/assets/characters/
```

### 3. 生成视觉项目总控.html

读取 `templates/视觉项目总控.html` 全文，复制到项目根目录 `视觉项目总控.html`。

用 SearchReplace 填充以下 STATE 字段（用 `<!--STATE:xxx -->` 标记）：

| 字段 | 初始值 |
|:-----|:-------|
| `mode` | `fresh` |
| `phase` | `init` |
| `project_name` | 项目名（用户输入或目录名） |
| `book_name` | 待指定 |
| `genre` | 待指定 |
| `created_at` | 当前时间 |
| `updated_at` | 当前时间 |
| `next_step` | `Phase 0: 读小说提取视觉资产` |

### 4. 自检

- [ ] 8 个标准目录存在
- [ ] 视觉项目总控.html 生成且 STATE 字段正确
- [ ] phase=init，next_step=Phase 0

### 5. 路由到 Phase 0

自检通过后，调度 `pop-visual-asset` 执行 Phase 0（读小说提取视觉资产），进入 `steps/step2-route.md` 的路由循环。

## 红线

- 只创建地基，不提取资产/不选画风/不设计人物（这些是 Phase 0/1/2 的事）
- 视觉项目总控.html 是唯一状态文件，禁止另建 project-state.md