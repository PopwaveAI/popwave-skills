# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/) 与 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 规范。

## [0.1.0] - 2026-05-20

首个公开版本，覆盖中文长篇小说从创意到校稿的完整工作流。

### 新增 - Skills (9 个)

- **novel-init** —— 项目脚手架，搭建标准 vault 目录结构（story.md / characters / worldbuilding / plot / chapters / style / .memory）
- **novel-brainstorm** —— 结构化对话式创意构思：一句话简介、核心矛盾、30 章承诺、市场定位、文风方向
- **novel-worldbuilding** —— 地点与体系（力量 / 政治 / 科技 / 宗教 / 经济 / 军事 / 社会）管理，含 9 类中文常见体系引导
- **novel-characters** —— 角色卡 + 关系图谱 + 家族树 + 8 种 voice 范式
- **novel-plot** —— 故事弧 / 时间线 / 伏笔账 (open/advance/resolve/defer) + 章节情节推进四大原则
- **novel-memory** —— 长期记忆管理（8 个 bank：chapter-briefs / scene-cards / entity-state / relationship-state / continuity-facts / decision-log / revision-notes / tool-observations）
- **novel-chapter** —— 9 步章节写作循环（outline → user_confirm → memory_load → write → self_check → fix_loop → memory_update → checkpoint → user_review），两阶段温度策略
- **novel-style-engine** —— 写法引擎：样本投喂 → 客观统计 + 主观抽取 → 5 prompt block 编译 → 3 强度档 × 5 任务模板
- **novel-review** —— 37 维校稿：4 维 Python 统计 + 33 维 LLM 评估 + 伏笔账核对（揭1埋1硬底线）+ 跨实体一致性

### 新增 - Python 工具脚本 (8 个)

- `shared/checkpoint.py` —— JSON 快照管理器（create / rollback / list / delete）
- `shared/validate_structure.py` —— vault 结构合规检查
- `skills/novel-style-engine/scripts/extract_style.py` —— 样本客观统计（句长 / 段长 / 标点密度 / 2-gram 词频 / 对话占比）
- `skills/novel-style-engine/scripts/compile_style.py` —— 5 任务模板 × 3 强度档编译器
- `skills/novel-review/scripts/check_ai_tells.py` —— 4 维统计学 AI 痕迹检测
- `skills/novel-review/scripts/check_post_write.py` —— 13 条 forbidden + 8 条 risk 硬规则违规
- `skills/novel-review/scripts/check_hook_ledger.py` —— 伏笔账核对 + CJK 2-gram 关键词回声 + 揭1埋1
- `skills/novel-review/scripts/check_consistency.py` —— 跨实体一致性 + vault 引用完整性

### 新增 - References (16 个)

各 skill 配套的模板与规则库：
- 5 大文风类型（动词驱动 / 克制典雅 / 幽默吐槽 / 热血燃向 / 悬疑压抑）
- 8 种角色 voice 范式（嘴硬主角 / 老成内敛 / 冷峻话少 / 现代吐槽 / 古板说教 / 阴柔反派 / 直率热血 / 文艺敏感）
- 9 类中文常见体系引导（修真 / 魔法 / 异能 / 科技 / 武学 / 政治 / 宗教 / 经济 / 军事）
- 5 种全书结构模型（三幕 / 英雄之旅 / 起承转合 / 救猫咪 15 拍 / 网文升级流）
- 章节情节推进四大原则、伏笔账规范、22 种文学技巧
- 37 维校稿维度详细清单
- 默认反 AI 规则库（中文网文向）

### 新增 - 文档

- `README.md` —— 用户安装 + 快速开始
- `docs/DESIGN.md` —— v2.1 完整设计图（600+ 行）
- `docs/AUDIT.md` —— 5 候选项目代码级审计依据
- `LICENSE` —— MIT
- `CHANGELOG.md` —— 本文件

### 已知限制

- 无 `novel-adapt`（小说→剧本 / 分镜转换），计划 v0.2
- 多层写法绑定（全书/卷/章/POV）仅 schema 留好，实际编译仅支持全书级，v0.2 加入
- 向量记忆层尚未引入，当前依赖文件检索 + chapter briefs（章节数 > 30 后建议引入）
- 一致性检查中的"continuity-facts 违反检测"为占位符，依赖 LLM 层处理

### 设计借鉴

本项目独立实现，借鉴以下开源项目的设计与算法（详见 `docs/AUDIT.md`）：

- [story-skills](https://github.com/danjdewhurst/story-skills) (MIT) —— vault 骨架结构、kebab-case + frontmatter 双向链
- [novel-writer](https://github.com/AI-Practical-Lab/novel-writer) —— 中文网文领域规则、检查点机制设计
- [inkos](https://github.com/Narcooo/inkos) (AGPL-3.0) —— ai-tells 4 维统计算法、post-write 硬规则表、hook-ledger 算法、多 agent 管线概念
- [AI-Novel-Writing-Assistant](https://github.com/ExplosiveCoderflome/AI-Novel-Writing-Assistant) (AGPL-3.0) —— 写法引擎完整概念架构（描述/执行分离、anti-AI 三态、多级绑定）
- [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) (MIT) —— 16 bank 记忆分类法
