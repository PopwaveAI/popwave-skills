# Step 4: 创作 HTML — SOP

> **前提：** Step 3 PRD 已通过用户确认。

## 第一步：学习设计参考

读取 `DESIGN_GUIDE.md`（完整设计参考），确认视觉选型：
- 10 个常规设计方向 + 5 个极端风格
- 严禁连续两次使用同一方向

## 第二步：创作单文件 HTML

**铁律：**

| # | 规则 | 具体要求 |
|:-:|:-----|:---------|
| 1 | **零 Emoji** | HTML 可见内容禁止 Emoji Unicode。用 ISO 代码（JP/SG/ID）、纯文字、SVG 替代 |
| 2 | **人物驱动** | 从"读懂这个人"出发，不套模板 |
| 3 | **自包含单文件** | CSS/JS 全内联，零外部依赖，双击可打开 |
| 4 | **响应式** | mobile-first，三档：≥1024px / 768-1023px / <768px |
| 5 | **数据驱动 HTML** | 视频 ID/标题/播放量/时长等所有数据从 `data.json` 动态生成。禁止手动抄写 |
| 6 | **禁止内容** | Services/Testimonials/Blog/Case Studies/Team → 一律禁止 |
| 7 | **视觉缺口处理** | 缺头像/banner → 先用缩略图 → GenerateImage → CSS 质感，禁止 emoji/占位符 |

**Section 规范：**

| Section | 最低要求 |
|:--------|:---------|
| Hero | 至少 4-5 层视觉层次 |
| Stats | 必须有数字动画（requestAnimationFrame） |
| About | 至少 3 段正文 |
| Videos | 至少 6 个，缩略图用 `maxresdefault` |
| Footer | 版权+社交 SVG 图标+订阅 CTA |
