# Step 5-7: 创建目录结构 + 生成章节摘要

## 第五步：创建目录结构 + 生成章节摘要

**Token 预算矩阵：**

| BOOK_TYPE \ DEPTH | reference | study |
|---|---|---|
| text | 800–1200 | 1000–1800 |
| technical | 1200–1800 | 2000–3000 |

**章节文件模板：**
```markdown
# Chapter N: <完整标题>

## Core Idea
<1-2 句：本章最重要的一个洞见>

## Frameworks Introduced
- **<框架名>**: <精确表述>
  - 何时用: <场景>
  - 怎么做: <步骤或标准>

## Key Concepts
- **<术语>**: <一句话精确定义>
(本章最重要的 5-10 个术语)

## Mental Models
<2-4 个思维工具，写成"遇到 X 时用 Y"或"把 X 理解为 Y">

## Anti-patterns
- **<要避免的>**: <为什么失败>

## Code Examples *(仅 technical)*
```<language>
<本章最具启发性的代码片段>
```
- **说明**: <一句话>

## Reference Tables *(仅 technical)*
<!-- 还原本章的比较矩阵、参数表、决策表 -->

## Worked Example *(仅 DEPTH=study)*
<!-- 还原作者演示的一个具体实例 -->

## Key Takeaways
1. <可执行的洞察>
...

## Connects To
- **Ch N**: <为什么相关>
```

❌ 门禁：章节摘要超过 Token 预算 → 砍冗余，确保密度优先。
