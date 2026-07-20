# 推书卡9页布局指南

> 参考 `暗恋橘生淮南-读者推书-v1.5.3.html` 的成熟布局，提炼为可复用的页面设计规范

---

## 页面规格

- 尺寸：720 × 960 px
- 内边距：58px 64px
- 内框线：inset 18px
- 字体：Songti SC / STSong（正文），PingFang SC（标注）

---

## 9页设计

### Page 1 · cover（封面）
- **layout**: editorial（cover样式）
- **eyebrow**: "一本书值不值得看？"
- **title**: 书名（highlight标红核心词）
- **subtitle**: 作者 · 题材 · 风格
- **blocks**:
  - quote: 一句话定位（从 positioning.one_liner）
  - lede: 核心钩子（从 positioning.core_hook）
  - tags: 标签（从 positioning.tags）
- **footer**: 题材标签

### Page 2 · hook（核心梗）
- **layout**: editorial
- **eyebrow**: "核心梗"
- **title**: "它与同类X故事有什么不同"（highlight"不同"）
- **blocks**:
  - cards(4): 4张差异卡（身份落差/表层目标/核心阻力/差异机制）
  - panel: "真正的故事问题"
- **footer**: 核心梗

### Page 3 · synopsis（无剧透梗概）
- **layout**: timeline
- **eyebrow**: "故事梗概"
- **title**: "无剧透地讲清故事方向"
- **blocks**:
  - steps(4): 开局/靠近/失衡/方向
  - panel: "故事推进的轴心"
- **footer**: 无剧透梗概

### Page 4 · characters（人物角色卡）
- **layout**: grid
- **eyebrow**: "人物角色卡"
- **title**: "谁值得关注"
- **blocks**:
  - cards(4): 4张人物卡
  - panel: "群像功能"
- **footer**: 人物角色卡

### Page 5 · chemistry（关系化学）
- **layout**: relationship
- **eyebrow**: "关系化学"
- **title**: "X如何成为故事的引擎"
- **blocks**:
  - formula: 双方驱动力
  - cards(2): 2张关系动态卡
  - panel: "关系向前的标志"
- **footer**: 关系化学
- **省略条件**: 无关系锚点时改为 selling_points 延伸页

### Page 6 · structure（故事结构）
- **layout**: editorial
- **eyebrow**: "世界与结构"
- **title**: "读者需要知道的故事结构"
- **blocks**:
  - cards(4): 4张结构卡
  - route: 故事路线
- **footer**: 故事结构

### Page 7 · selling_points（具体卖点）
- **layout**: grid
- **eyebrow**: "具体卖点"
- **title**: "好看具体发生在哪里"
- **blocks**:
  - cards(4): 4张卖点卡
  - panel: "强项边界"
- **footer**: 卖点

### Page 8 · risks（阅感与避雷）
- **layout**: warning
- **eyebrow**: "阅感与避雷"
- **title**: "哪些人可能会弃书"
- **blocks**:
  - radar(6): 6维雷达图（characters/plot/relationships/prose/world/pacing）
  - warning: 避雷项列表
  - panel: "争议如何理解"
- **footer**: 避雷

### Page 9 · verdict（最终结论）
- **layout**: verdict
- **eyebrow**: "最终结论"
- **title**: "它到底适合谁"
- **blocks**:
  - audience: 推荐/不推荐双栏
  - verdict: 评分区间 + 结论
  - panel: "为什么值得试读"
- **footer**: 最终推荐

---

## 主题选择规则

| 主题 | 适用 | 主色 | 封面色 |
|:--|:--|:--|:--|
| literary-red | 文学/言情（默认） | 暗红 #8c3039 | #1d1919→#4b1d24 |
| ink-blue | 仙侠/玄幻 | 墨蓝 #295c72 | #15252d→#244d5c |
| warm-paper | 都市/现实 | 暖棕 #9d5937 | #33251d→#75513a |
| dark-modern | 悬疑/科幻 | 橙红 #df6f60 | #111214→#34383d |
| diary-orange | 青春/校园 | 橙 #c26837 | #203039→#9a5634 |

---

## block 类型速查

| 类型 | 用途 | 关键字段 |
|:--|:--|:--|
| quote | 引用强调 | text |
| lede | 引导段 | text |
| paragraph | 普通段 | text |
| panel | 带标题面板 | title + text |
| cards | 2列卡片 | items[{title,text}] |
| steps | 编号步骤 | items[{title,text}] |
| tags | 标签云 | items[] |
| route | 路径流 | items[] |
| formula | 公式流 | items[] |
| bullets | 双列列表 | items[] |
| warning | 警告框 | title + items[] |
| metrics | 3列指标 | items[{value,label}] |
| radar | 雷达条 | items[{label,value}] |
| audience | 双栏推荐 | items{recommended[],avoid[]} |
| verdict | 结论框 | title + text |
