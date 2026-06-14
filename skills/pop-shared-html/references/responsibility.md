# 唯一责任原则

> **pop-shared-html 是系统中唯一产出 HTML 的 skill。** 其他所有 skill 不再自行产出 HTML。

**协作流程：**
```
其他 skill（如 pop-shared-reader）
  └→ 产出结构化 Markdown + 配套 YAML 结构化数据
       └→ 调用 pop-shared-html
            └→ 本 skill 接管：Phase 0 设计简报 → 选骨架 → 应用设计核心 → 组装组件 → 硬性配图 → 质量门禁
                 └→ 输出最终 HTML
```
