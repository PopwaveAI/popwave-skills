# 第二步：加载对应 Lv 模板 + 填写角色卡

## 加载模板

| 级别 | 模板路径 | 加载方式 |
|:----|:---------|:---------|
| Lv1 | `references/Lv1-one-shot.md` | `Get-Content -Path '{skill_path}/references/Lv1-one-shot.md' -Encoding UTF8 -Raw` |
| Lv2 | `references/Lv2-functional.md` | 同上 |
| Lv3 | `references/Lv3-important.md` | 同上 |
| Lv4 | `references/Lv4-core.md` | 同上 |

## 做什么

按维度逐项填写，严格遵循"上一级全部 + 本级新增"原则。

| 项目 | 内容 |
|:-----|:------|
| 读什么 | `references/level-selection-methodology.md` 的维度矩阵 + 对应 Lv 模板文件 |
| 做什么 | 按维度逐项填写，严格遵循"上一级全部 + 本级新增"原则 |
| 产出什么 | `设计/角色层/{角色名}-{定位}.md`（格式与模板一致） |
| 必须包含 | **设计目的** + **叙事能力**（所有级别都必须有） |

## 维度递增原则

Lv1 → Lv4 维度严格做加法。每级 = 上一级**全部维度** + 本 Lv **新增维度**。

详见 `references/level-selection-methodology.md` 维度矩阵一览表。
