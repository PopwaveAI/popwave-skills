# CHANGELOG — short-idea-refiner
## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

## v1.0.0 | 2026-08-04
### 新建 skill：短篇脑洞提炼器
- 初始版本。支持3条路径（A有模糊想法/B只有方向/C带例文）
- Step 1 收集输入+路径判断
- Step 2 热点拉取+提炼2-3个脑洞方向
- Step 3 3项检验+补强+输出脑洞卡片
- 按Popwave Skill设计规范重构：SKILL.md压缩至42行，执行细节拆分至steps/
- 4条红线，热点数据仅作参考
- 模板 `idea-card.tpl.md` 含7个区块+流转上下文
