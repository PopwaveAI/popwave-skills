> ⚠️ **废弃 — 勿引用** 本文件所属 skill 已被重构/删除。agent 不应加载此文件。
> 所有活跃 skill 位于 skills/pop-novel-*

---
name: html-renderer
display_name: "HTML鍖栧彂甯冨紩鎿?
category: publish
scenario: publish
mode: html
recommended: 8
tags: ["HTML", "鍙戝竷", "鍙鍖?, "娓叉煋"]
fidelity: production
description: "HTML娓叉煋寮曟搸 v1.3銆?7濂梙tml-anything SKILL璁捐绾︽潫铻嶅悎銆傚皢.md/.yaml/缁撴瀯鍖栨暟鎹啋楂樿川閲忓崟鏂囦欢HTML銆傝妭鐐笷鍓嶇疆鍐崇瓥锛堝彈浼?鏁堟灉/鐗瑰寲锛夈€傛敮鎸丼wiss/Guizang/Kami/Glitch绛?7绉嶈璁＄郴缁熴€俫lue/post_render.py鍚庣疆楠岃瘉銆?
version: v1.3
novel_agent_version: v3.3

orchestration:
  preflight: ["check_project_dir"]
  dependencies: []
  inject_context: []
  subagent_required: false

produces:
  - 鍗曟枃浠禜TML锛堥€傞厤鍚勭璁捐绯荤粺锛?
  - glue/post_render.py 鍚庣疆楠岃瘉鎶ュ憡
---

# html-renderer 鈥?HTML鍖栧彂甯冨紩鎿?

> **瀹氫綅澹版槑**锛氭湰 renderer 鏄?**novel-agent-pro 鍐呴儴涓撶敤鐨?Python 娓叉煋灞?*锛屾湇鍔′簬鍏樁娈电绾跨殑鍚庣疆 HTML 鍙戝竷銆?
>
> 鍏ㄥ眬鍞竴 HTML 娓叉煋寮曟搸鏄?`pop-html-anything`锛坄skills/pop-html-anything/`锛夈€備袱鑰呯殑鍖哄埆锛?
> - pop-html-anything 鈫?閫氱敤 HTML 娓叉煋寮曟搸锛屾秷璐逛换浣曚笂娓哥粨鏋勫寲鏁版嵁锛堟媶涔?YAML / 瑙掕壊 JSON / 鏁版嵁鎶ュ憡锛?
> - html-renderer锛堟湰妯″潡锛夆啋 novel-agent-pro 鍐呴儴涓撶敤锛屽鎺ュ叚闃舵绠＄嚎鐨?glue 鍚庣疆楠岃瘉 / 鍐欎綔椤圭洰鍙戝竷

> 灏?md/.yaml/缁撴瀯鍖栨暟鎹?鈫?楂樿川閲忓崟鏂囦欢HTML
> 鍩轰簬 html-anything 27 濂?SKILL 璁捐绾︽潫

## 浣跨敤鏂瑰紡

```python
from html_renderer import NodeF, HTMLRenderer

# 鑺傜偣F锛氬墠缃喅绛?
intent = NodeF.decide(
    doc_type="scene_card",
    doc_name="鍦烘櫙鍗?001-绾歌韩",
    audience="readers",
    goal="horror_immersion",
    specialization="娓告垙UI鍒囧叆鈫掓亹鎬栨帓鐗堟敹灏?
)

# 娓叉煋
renderer = HTMLRenderer()
html = renderer.render(intent.resolved_skill, data, output_path)
```

璇﹁ `_shared/html-renderer/__init__.py`

