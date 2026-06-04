# CHANGELOG — pop-novel-writer

## v9.5.1 (2026-06-03)
- **新增【系统级强制】写前必读清单**：HARD-GATE 后新增强制文件读取指令，每次写正文前执行
- **必读 7 组文件**：上一章状态（含 global-summary + chapter-state.yaml）+ act-yaml + constitution + reader_profile + L1设定层 6 个 + 数值体系(2个) + 地理/时间轴(如存在)
- **注意力校验原则**：agent 必须显式对比「读前记忆 vs 读后文件」，以文件为准修正认知
- 解决根因：agent 过估记忆可靠性且无强制重读指令

## v9.5.0 (2026-06-03)
- **风格注入系统**：新建 `styles/` 目录，提供可插拔文风配置
- **ESM before 升级 15 项**：新增第 15 项 style-bundle，从 `styles/{writing_style}.md` 加载文风约束注入 Pass 2
- **风格DNA模板**：`styles/style-dna-template.md` 定义 4 层·30+ 维度的文风标准
- **默认风格显式化**：`styles/default.md` 从 K1-K4 + QC 红线 + 模板池提取当前管线的隐含风格
- **新增 4 种文风**：番茄(`tomato`)、吞噬星空(`tunshi`)、遮天(`zhetian`)、深渊主宰(`abyss`)
- **SKILL.md 新增「风格注入系统」section**：用法/消费路径/5 种风格清单
- **inject_context 新增 styles/**：按 project.yaml writing_style 字段读取
- **版本号 9.4.0 → 9.5.0**

## v9.4.0 (2026-06-03)
- **吸收 pop-novel-opening-arc**：将「黄金三章」合并为正文引擎的内置模式
- **SKILL.md 新增「黄金三章模式」section**：情绪弧线（拉人→压住→释放）、爽点分布规则、节点C·黄金检查、专项自检
- **删除独立 skill**：`pop-novel-opening-arc`（skill.json / SKILL.md / CHANGELOG.md）已移除
- **同步更新 dispatcher.py 路由表**：「前三章/开篇/黄金三章」→ `pop-novel-writer`
- **同步更新 POP-ROUTER / POP-CALL / thinking-mode-template / master SKILL.md**

## v9.3.1 (2026-06-03)
- **P0-1: 补齐 glue/ 模块**：创建 `glue/project_config.py`，解决 `post_write.py`/`pre_flight.py`/`validate.py`/`main.py`/`check_db.py` 的 `from glue.project_config import ...` 断链
- **P0-2: 修复 main.py 三条错误路径**：glue import（3-level→1-level）、knowledge-base 路径（`skills/`→`pop-novel-writer/`）、template-pools 路径（从项目根上三层→自身目录）
- **P0-3: 清除旧路径硬编码**：`project_init_check.py`（9处）、`update_project_status.py`（15处 skill 名+路径）、`update_global_summary.py`（docstring）中的 `novel-agent-pro/skills/skill-emergent-writer` 引用全部替换
- **P1-1: 清理废弃 schema**：从 `validate.py` 移除已 deprecated 的 `chXXX` 和 `writer-metadata` schema 注册（2026-05-19 废弃）；删除对应的 `.schema.yaml` 文件
- **P1-2: 移除无关脚本**：删除 `post_render.py`（HTML 渲染验证，与正文写作无关）
- **name/directory 字段对齐**：`name: emergent-writer`→`pop-novel-writer`，`directory: skill-emergent-writer`→`pop-novel-writer`
- **内部旧 skill 名修复**：`skill-plot-architecture`→`pop-novel-plot`、`qa-payoff`→`pop-novel-qa`、`spec-bridge`→`pop-novel-master`
- **重复版本条目删除**：尾部重复的 `9.0.0` 条目已清理
- **书数据污染清理**：`project_init_check.py` 中 `诡异游戏` 路径替换为通用路径
- **存在意义框架**：SKILL.md 补全（来自上一轮 review）

## v9.3.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-emergent-writer 独立提升
- 修复路径引用指向新 skill 名
