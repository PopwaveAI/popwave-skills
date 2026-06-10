# typical-paths.md — 典型路径速查

> 加载时机：Think 初次路由时，对照确认当前环节上下游。
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

---

```
新书启动：            bookstrap (含拆书融合+起点+终点) → plot (含里程碑) → chapter-design → prose-render → qa
拆解参考书：           download-webnovel-txt → pop-novel-deconstructor → _参考书分析/
调研后开书：           cnovel-research → bookstrap → plot → chapter-design → prose-render → ...
已有项目续写：          plot → chapter-design → prose-render → qa
续写旧项目：            bookstrap (reverse) → chapter-design → prose-render → qa
文风分析 → 写作：       pop-dna → prose-render（携带 style 参数）
修改设定+重写受影响正文： bookstrap → plot → chapter-design → prose-render
```
