# CHANGELOG

## v1.0.0 - 2026-07-14

### 新建：番茄 onepiece 复制更名
- 从番茄小说创作skill群的 prose-render-onepiece 复制更名为 pop-qidian-write-onepiece。
- 新增 frontmatter（name: pop-qidian-write-onepiece）。
- 新增 execution.mode（formal/draft/trial 三档，引用 PRD §4.5）。
- Step 1 适配：加入 current-state 消费规则，读取 current-state.md 获取下一章硬推进。
- 新增正文落盘规则：正文落盘到 `涌现/正文/{书名}-第{N}章-{标题}.txt`，对话中只回摘要+钩子+创作记录。
- 保留番茄 onepiece 全部内容：三层架构/SOP/赛道定义/战斗模式/API管道注入规范等。
- 流派技法/ 目录从源完整复制。

## v1.1.0 - 2026-07-21

### 对齐：三层骨架重构
- Step 1 新增加载 `设计/主角设计.md`（爽感矛盾公式：坐标系门槛×天赋加速×代价约束）和 `设计/角色库/角色库.md`（角色唯一源）。
- Step 6 爽感层新增坐标系跃迁锚定约束：爽感爆发必须锚定坐标系位置跃迁，体现天赋加速 vs 代价约束的张力，禁止脱离坐标系的纯情感爽感。
- 流派技法（战斗模式×3阶段/海上战斗/场景卡/多线叙事）保持不动。
- 顶部新增版本说明；skill.json 版本号同步升至 1.1.0。
