# Changelog

## v1.1.0 (2026-07-22)

### 按规范重写 SKILL.md

- 按pop-shared-skill-create v6.1.0规范重写SKILL.md
- 新增frontmatter（name+description含触发条件"当用户说'章纲/写正文/章纲流'时启用"）
- 新增"做什么"输入/输出/下游表
- 新增"怎么操作"section含execution.mode+强弱加载声明
- 红线#1新增读取协议（Get-Content -Encoding UTF8 -Raw，禁用Read工具）
- 速查表改为文件目录引导（文件+读取时机+核心内容）
- 新增版本section（此前SKILL.md无版本区）
- 版本只留最新一条
- skill.json版本同步至1.1.0，description更新为含触发条件
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v1.0.0 (2026-07-18)

- 初始版本
- 基于用户提供章纲创作网文正文的专用skill
- 2-step架构：Step 1前文分析（文风/矛盾/主线/关键信息/衔接点）+ Step 2拆解框架→填充细节→节奏收尾→写正文
- 4段式骨架（开篇650-750/发展950-1050/高潮850-950/结尾650-750），总字数3100-3500字
- 2个模板：前文分析卡、4段式骨架
- 核心特色：章末期待感对话钩子、描写控制3-8个/每个≤30字、章节名10字+带噱头/反差
