# Skill 分类表

> 依据专家配置图（2026-08-13）整理的 skill 分类索引。图中 5 位专家各自绑定一组 skill；未在图中分配、但属于某专家命名空间家族的 skill 归入「通用·子组件」区，可按需提升到对应专家。

## 一、五大专家 → Skill 对应

| # | 专家 | 消耗 | 说明 | 对应 Skill |
|:--|:--|:--|:--|:--|
| 1 | 番茄长篇网文专家 | 中 | 番茄/七猫等长篇网文创作（完整创作管线：立项→世界→剧情→正文→审核） | `pop-fanqie-seed` `pop-fanqie-plot` `pop-fanqie-write` `pop-fanqie-review` `pop-fanqie-world` `pop-fanqie-pipeline` `pop-research` `pop-dna-style` |
| 2 | 小说推书与IP化专家 | 高 | 网文→漫画/IP 化改编与视觉资产生产（跨平台视觉改编） | `pop-visual-style` `pop-visual-shared` `pop-visual-pipeline` `pop-visual-oc` `pop-visual-cover` `pop-visual-comic` `pop-visual-asset` `pop-comic-content` `pop-visual-art-bible` |
| 3 | 起点长篇网文专家 | 中 | 起点长篇网文创作（测试调整中；写作含 dnlike/海贼王类 流派专属） | `pop-qidian-seed` `pop-qidian-world` `pop-qidian-character` `pop-qidian-plot` `pop-qidian-write` `pop-qidian-review` `pop-qidian-research` `pop-qidian-pipeline` |
| 4 | 网文拆书专家 | 高 | 长篇网文解构/逆向分析（计算密集） | `pop-decon` `pop-decon-design-pack` `pop-decon-prd` `pop-decon-setting` `pop-decon-volume` |
| 5 | 短篇小说专家 | 低 | 知乎/豆瓣/每日阅读等短篇创作 | `short-body-generator` `short-idea-refiner` `short-opening-designer` `short-plot-structurer` `short-platform-orientation` `short-reviewer` `short-text-deconstructor` |

## 二、共享工具

| Skill | 作用 | 归属专家 |
|:--|:--|:--|
| `tool-download-webnovel` | 网文搜索下载 | 番茄 / 起点 / 拆书共用 |

## 三、通用 Skill（图中未分配）

按命名空间家族分组，建议归入对应专家的子组件：

### 拆书子组件（decon 家族，供「网文拆书专家」按需调用）
`pop-decon-beat` `pop-decon-character` `pop-decon-plot` `pop-decon-power` `pop-decon-romance` `pop-decon-style` `pop-decon-world`

### 番茄子组件
`pop-fanqie-character`

### 视频与物料（推书/IP 化延伸）
`pop-video-brand` `pop-video-comic` `pop-content-card` `pop-comic-test`

### 推书
`pop-recommend`

### 降AI味
`pop-ai-reduce`

### 元能力（skill 开发）
`pop-shared-skill-create`

## 四、命名空间速查

| 前缀 | 家族 | 归属 |
|:--|:--|:--|
| `pop-fanqie-*` | 番茄长篇 | 番茄专家 |
| `pop-qidian-*` | 起点长篇 | 起点专家 |
| `pop-decon-*` | 网文拆解 | 拆书专家（子组件在通用区） |
| `pop-visual-*` `pop-comic-content` | 视觉/IP | 推书与IP化专家 |
| `short-*` | 短篇 | 短篇专家 |
| `pop-video-*` `pop-content-card` `pop-comic-test` `pop-recommend` | 视频物料/推书 | 通用·视频物料 |
| `pop-ai-reduce` | 降AI味 | 通用 |
| `pop-shared-skill-create` | skill 元能力 | 通用 |
| `tool-*` | 共享工具 | 跨专家共用 |