# CHANGELOG — short-plot-structurer
## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

## v1.0.0 | 2026-08-04
### 新建 skill：短篇剧情结构器
- 初始版本。4种结构模板（知乎反转体/番茄单元剧体/经典三幕式/情绪爆发体）
- Step 1 平台×题材×卖点自动推荐结构模板
- Step 2 剧情弧线设计，按免费/付费分段+情绪走向+钩子嵌入
- Step 3 角色设计（≤5人），主角四维+配角功能分类，角色服务于剧情
- Step 4 输出骨架卡片+流转上下文
- 按Popwave Skill设计规范重构：SKILL.md压缩至50行，执行细节拆分至steps/
- 5条红线，角色上限+功能合并为核心约束
- 模板 `skeleton-card.tpl.md` 含6个区块+弧线循环表+流转上下文
