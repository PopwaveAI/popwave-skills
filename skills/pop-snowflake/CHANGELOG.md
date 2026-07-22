# Changelog

## v1.1.0 (2026-07-22)

### 按规范重写 SKILL.md

- 按pop-shared-skill-create v6.1.0规范重写SKILL.md
- 新增frontmatter（name+description含触发条件"当用户说'雪花写作/雪花法/snowflake'时启用"）
- 新增"做什么"输入/输出/下游表
- 新增"怎么操作"section含execution.mode+强弱加载声明
- 红线#1新增读取协议（Get-Content -Encoding UTF8 -Raw，禁用Read工具）
- 速查表改为文件目录引导（文件+读取时机+核心内容）
- 新增版本section（此前SKILL.md无版本区）
- 版本只留最新一条
- skill.json版本同步至1.1.0，description更新为含触发条件
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v1.0.0 (2026-07-16)

- 初始版本
- 基于兰迪·英格曼森雪花写作法10步流程
- 2-step架构：Step 1设计阶段（预备→四页纸大纲）+ Step 2执行阶段（人物宝典→写小说）
- 5个模板：一句话概括、一段式概括、人物介绍卡、人物宝典、场景清单
- 核心方法论：迭代式扩展 + 双轨并行 + 冲突驱动 + 场景循环
