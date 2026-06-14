---
name: pop-writer-html
description: 当用户说"发布 / HTML化 / 渲染成网页 / 小说上网页 / 把设定做成HTML / 场景卡发布 / 角色页发布 / 全文发布页"时触发。将小说正文/设定/场景卡等结构化数据 → 高质量单文件 HTML 发布页。
pipeline:
  upstream: [pop-writer-qa, pop-writer-prose]
  downstream: []
---

# html-renderer — HTML 化发布引擎 v1.3.2

> **定位声明**：本 renderer 是 **pop-novel-master 内部专用的 Python 渲染层**，服务于六阶段管线的后置 HTML 发布。
>
> 全局唯一 HTML 渲染引擎是 `pop-shared-html`（`skills/pop-shared-html/`）。两者的区别：
> - **pop-shared-html** → 通用 HTML 渲染引擎，消费任何上游结构化数据
> - **html-renderer（本模块）** → pop-novel-master 内部专用，对接六阶段管线的 glue 后置验证 / 写作项目发布

---

## 速查表

| 使用方式 | 场景 | 入口 |
|:---------|:-----|:-----|
| **Python 模块调用** | pop-novel-master glue 层在六阶段管线后置 | `from html_renderer import NodeF, HTMLRenderer` |
| **渲染通用 HTML** | 非 pop-novel-master 场景 | ❌ 不适用 — 用 `pop-shared-html` |

### 判断指引

| 场景 | 用哪个 |
|:-----|:-------|
| 拆书报告需要 HTML 发布页 | `pop-shared-html` |
| pop-novel-master 的六阶段管线需要产出发布 | **html-renderer（本模块）** |
| 创作项目发布（已通过 glue 路由） | **html-renderer（本模块）** |

---

## 执行流程 SOP

> 本模块是 Python 渲染层，三步调用即可完成一次发布。详细指令见 `steps/step-1-render.md`。

### 第一步：前置决策（NodeF.decide）

| 项目 | 内容 |
|:-----|:------|
| 读什么 | 文档类型 / 受众 / 效果目标 / 规格说明 |
| 做什么 | 调用 `NodeF.decide()` 确定设计系统（Swiss / Guizang / Kami / Glitch 等 27 种之一） |
| 产出什么 | intent 决议对象（含 resolved_skill） |
| ❌ 门禁 | `doc_type` / `audience` 任一缺失 → 抛出 `ValueError`，列出缺失字段，要求补齐后再决策 |

```python
intent = NodeF.decide(
    doc_type="scene_card",          # 文档类型：scene_card / character / outline / full_novel
    doc_name="场景卡-001-纸身",
    audience="readers",             # 受众：readers / editors / self
    goal="horror_immersion",         # 效果目标
    specialization="游戏UI切入→恐怖排版收尾"
)
```

### 第二步：执行渲染（render）

| 项目 | 内容 |
|:-----|:------|
| 读什么 | intent 决议 + 上游结构化数据（dict / YAML） |
| 做什么 | 调用 `HTMLRenderer.render()` 生成 HTML |
| 产出什么 | 单文件 HTML（写入 `宣传/` 子目录） |
| ❌ 门禁 | `pop-shared-html` 未安装 → 抛出 `ImportError`，提示安装后重试 |
| 门禁 | 传入的 data 格式不是预期的 dict/YAML → 打印校验失败详情，提示上游修复 |

```python
renderer = HTMLRenderer()
html = renderer.render(intent.resolved_skill, data, output_path)
```

### 第三步：质量验证

| 项目 | 内容 |
|:-----|:------|
| 做什么 | 逐项检查质量红线 |
| 产出什么 | 验证报告 / 修复动作 |
| ❌ 门禁 | 任一项未通过 → 阻塞修正，不跳过 |

---

## ❌ 质量红线

以下条件未满足时禁止上线，必须阻塞修正：

| # | 红线 | 确认 |
|:-:|:-----|:----:|
| ❌1 | **HTML 验证** — 生成的 HTML 必须通过 W3C 标准检查，无未闭合标签、无非法嵌套、无重复 ID | [ ] |
| ❌2 | **设计系统决策已执行** — 必须明确选择一种设计系统（Swiss / Guizang / Kami / Glitch 等 27 种）并附选择理由；禁止无依据随机挑选 | [ ] |
| ❌3 | **NodeF 前置决策已完成** — 渲染前必须经过 `NodeF.decide()` 获取决议，禁止跳过节点 F 直接硬编码设计参数 | [ ] |
| ❌4 | **输出路径合规** — 渲染产物必须写入 `宣传/` 子目录，禁止写入项目根目录或其他非约定路径 |
| ❌5 | **产出只留摘要** — HTML 生成后对话中不粘贴源码。说"已写入 {路径}。预览核心里：{首页视觉效果描述}。需调整告诉我。" | [ ] |

---

## 落盘检查点

| 产物 | 路径 | 说明 |
|:-----|:-----|:-----|
| **xxx.html** | `宣传/` 子目录 | 单文件 HTML 发布页，设计系统已通过 NodeF.decide() 决策 |

完成后告知用户："已写入 {路径}。预览核心：{首页视觉效果描述}。需调整告诉我。"

---

## ❌ 错误示例

### WRONG 1：跳过 NodeF 决策直接硬编码设计系统

```python
# ❌ 错误
renderer = HTMLRenderer()
html = renderer.render("Swiss", data, output_path)
# 没有经过 NodeF.decide()，直接硬编码设计系统
```
❌ 错误：没有做前置决策就随意选设计系统。
✅ 正确：先调用 `NodeF.decide()` 获取决议，再用 `intent.resolved_skill` 传给 render。

### WRONG 2：渲染产物写到项目根目录

```python
# ❌ 错误
renderer.render(intent.resolved_skill, data, "project_root/index.html")
```
❌ 错误：产出不放在 `宣传/` 子目录，污染项目根目录。
✅ 正确：使用 `宣传/` 子目录作为输出路径。

### WRONG 3：传入非标准 data 格式

```python
# ❌ 错误
renderer.render(intent.resolved_skill, "这是一段文本", output_path)
# 传入的是纯字符串而非 dict/YAML
```
❌ 错误：数据结构校验失败，render 无法解析。
✅ 正确：传入标准 dict/YAML 结构。

### WRONG 4：忽略 HTML 验证直接交付

```
Agent：生成的 HTML 看起来没问题 → 直接交付
```
❌ 错误：未做 W3C 标准检查，可能存在未闭合标签或非法嵌套。
✅ 正确：交付前做完整性验证：`</html>` 闭合 / 标签合法 / 无重复 ID。

### WRONG 5：没有选择理由就随机选设计系统

```
Agent：这次用 Kami 设计系统（没有附理由）
```
❌ 错误：选设计系统必须附选择理由，禁止无依据随机挑选。
✅ 正确：记录选择理由，如"场景卡需要恐怖沉浸感 → 选 Glitch（故障风 + 暗色调）"

---

## 异常与边界条件

| # | 场景 | 触发条件 | 处理动作 |
|:-:|:-----|:---------|:---------|
| 1 | pop-shared-html 未安装 | 渲染器初始化时无法导入 pop-shared-html 模块 | 抛出 `ImportError`，提示「请先安装 pop-shared-html SKILL」并中止渲染 |
| 2 | NodeF.decide() 输入不完整 | 调用时缺少 doc_type 或 audience 等必需参数 | 抛出 `ValueError`，列出缺失字段，要求补齐后再决策 |
| 3 | 渲染器运行时异常 | render() 执行过程中 Python 抛出未预期异常 | 捕获异常，记录完整 traceback 到日志文件，返回错误码并保持输出路径不写入残损文件 |
| 4 | 输出路径不存在 | output_path 指向的目录尚未创建 | 自动递归创建目标目录（os.makedirs），完成后继续渲染 |
| 5 | 上游数据格式错误 | 传入的 data 不是预期的 dict / YAML 结构 | 打印数据结构校验失败详情，提示上游（pop-novel-master glue 层）修复数据格式 |
| 6 | 设计系统名不存在于 27 套中 | NodeF.decide() 返回的 resolved_skill 匹配不到已知设计系统 | 回退到默认系统（Swiss），在日志中记录警告并追加到调度报告的「异常回退」列表 |
| 7 | pop-shared-html 版本不兼容 | 已安装但版本过低，缺少本 renderer 依赖的 API | 提示用户更新 pop-shared-html 至兼容版本，显示当前版本和最低版本要求 |
| 8 | 输出文件已存在 | output_path 对应的 HTML 文件已存在 | 覆盖写入前先创建备份（加 `.bak` 后缀），完成后标注"已覆盖旧文件" |

---

## 版本

v1.3.2 | 2026-06-14 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
