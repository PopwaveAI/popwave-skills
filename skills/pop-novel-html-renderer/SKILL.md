---
name: pop-novel-html-renderer
display_name: "HTML化发布引擎"
category: publish
scenario: publish
mode: html
recommended: 8
tags: ["HTML", "发布", "可视化", "渲染"]
fidelity: production
description: "HTML渲染引擎 v1.3。27套html-anything SKILL设计约束融合。将.md/.yaml/结构化数据→高质量单文件HTML。节点F前置决策（受众/效果/特化）。支持Swiss/Guizang/Kami/Glitch等27种设计系统。pop-novel-writer/scripts/post_render.py后置验证。"
version: v1.3
novel_agent_version: v3.3

orchestration:
  preflight: ["check_project_dir"]
  dependencies: []
  inject_context: []
  subagent_required: false

produces:
  - 单文件HTML（适配各种设计系统）
  - pop-novel-writer/scripts/post_render.py 后置验证报告
---

# html-renderer — HTML化发布引擎

> **定位声明**：本 renderer 是 **pop-novel-master 内部专用的 Python 渲染层**，服务于六阶段管线的后置 HTML 发布。
>
> 全局唯一 HTML 渲染引擎是 `pop-html-anything`（`skills/pop-html-anything/`）。两者的区别：
> - pop-html-anything → 通用 HTML 渲染引擎，消费任何上游结构化数据（拆书 YAML / 角色 JSON / 数据报告）
> - html-renderer（本模块）→ pop-novel-master 内部专用，对接六阶段管线的 glue 后置验证 / 写作项目发布

> 将.md/.yaml/结构化数据 → 高质量单文件HTML
> 基于 html-anything 27 套 SKILL 设计约束

## 使用方式

```python
from html_renderer import NodeF, HTMLRenderer

# 节点F：前置决策
intent = NodeF.decide(
    doc_type="scene_card",
    doc_name="场景卡-001-纸身",
    audience="readers",
    goal="horror_immersion",
    specialization="游戏UI切入→恐怖排版收尾"
)

# 渲染
renderer = HTMLRenderer()
html = renderer.render(intent.resolved_skill, data, output_path)
```

详见 `__init__.py`
