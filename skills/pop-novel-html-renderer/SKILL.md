---
name: pop-novel-html-renderer
description: "当用户要求「发布/HTML化/渲染成网页」内容时触发。将小说正文/设定/场景卡等结构化数据 → 高质量单文件 HTML 发布页。"
---

# html-renderer — HTML 化发布引擎

> **定位声明**：本 renderer 是 **pop-novel-master 内部专用的 Python 渲染层**，服务于六阶段管线的后置 HTML 发布。
>
> 全局唯一 HTML 渲染引擎是 `pop-html-anything`（`skills/pop-html-anything/`）。两者的区别：
> - **pop-html-anything** → 通用 HTML 渲染引擎，消费任何上游结构化数据（拆书 YAML / 角色 JSON / 数据报告）
> - **html-renderer（本模块）** → pop-novel-master 内部专用，对接六阶段管线的 glue 后置验证 / 写作项目发布。**通用 HTML 渲染 → pop-html-anything**

## ❌ 质量红线

以下条件未满足时禁止上线，必须阻塞修正：

- [ ] **HTML 验证**：生成的 HTML 必须通过 W3C 标准检查，无未闭合标签、无非法嵌套、无重复 ID。
- [ ] **设计系统决策**：必须明确选择一种设计系统（Swiss / Guizang / Kami / Glitch 等 27 种）并附选择理由；禁止无依据随机挑选。
- [ ] **NodeF 前置决策**：渲染前必须经过 `NodeF.decide()` 获取决议，禁止跳过节点 F 直接硬编码设计参数。
- [ ] **输出路径合规**：渲染产物必须写入 `宣传/` 子目录，禁止写入项目根目录或其他非约定路径。

## 使用方式

```python
from html_renderer import NodeF, HTMLRenderer

# 节点 F：前置决策 — 根据文档类型/受众/效果目标确定设计系统
intent = NodeF.decide(
    doc_type="scene_card",          # 文档类型：scene_card / character / outline / full_novel
    doc_name="场景卡-001-纸身",
    audience="readers",             # 受众：readers / editors / self
    goal="horror_immersion",         # 效果目标
    specialization="游戏UI切入→恐怖排版收尾"
)

# 渲染：传入决策决议 + 上游结构化数据 + 输出路径
renderer = HTMLRenderer()
html = renderer.render(intent.resolved_skill, data, output_path)
```

详见 `__init__.py`。

## 异常与边界条件

| 异常场景 | 触发条件 | 预期行为 |
|---|---|---|
| `pop-html-anything` 未安装/未找到 | 渲染器初始化时无法导入 `pop-html-anything` 模块 | 抛出 `ImportError`，提示「请先安装 pop-html-anything SKILL」并中止渲染 |
| `NodeF.decide()` 输入不完整 | 调用 `NodeF.decide()` 时缺少 `doc_type` 或 `audience` 等必需参数 | 抛出 `ValueError`，列出缺失字段，要求补齐后再决策 |
| 渲染器运行时异常 | `render()` 执行过程中 Python 抛出未预期异常 | 捕获异常，记录完整 traceback 到日志文件，返回错误码并保持输出路径不写入残损文件 |
| 输出路径不存在 | `output_path` 指向的目录尚未创建 | 自动递归创建目标目录（`os.makedirs`），完成后继续渲染 |
| 上游数据格式错误 | 传入的 `data` 不是预期的 dict / YAML 结构 | 打印数据结构校验失败详情，提示上游（pop-novel-master glue 层）修复数据格式 |
| 设计系统名不存在于 27 套列表中 | `NodeF.decide()` 返回的 `resolved_skill` 匹配不到已知设计系统 | 回退到默认系统（`Swiss`），在日志中记录警告并追加到调度报告的「异常回退」列表 |

## 版本 v1.3.1 | 2026-06-04 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
