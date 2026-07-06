# CHANGELOG

## v3.5.0 - 2026-07-06

### 重构：对齐 PRD 契约层
- 四层架构对齐：SKILL.md 引用 PRD §4 作为单一真相源，删除自有 execution.mode 三档表、自有骨架定义、自有 owner 表。
- 正文落盘路径明确为 `涌现/正文/{书名}-第{N}章-{标题}.txt`（修复问题 7）。
- "新增事实待 review" 措辞修正：write 只在对话创作记录里列清单（声明），不落盘到任何库文件；由 review 读取后落库（修复问题 10）。
- 新增 steps/ 目录：step-1-consume.md（消费 4 类输入 + 末尾门禁）、step-2-write.md（写正文 + 落盘 + 创作记录）。
- 新增 templates/chapter-record.tpl.md（统一回复模板，对齐 PRD §4.7）。
- skill.json 补全 displayName / entry / activation / permissions 字段。
- 版本从 2.3.0 升至 3.5.0，版本三处一致（SKILL.md + skill.json + CHANGELOG.md）。

## v2.3.0

- 旧版单文件 SKILL.md，自有 execution.mode 三档表、自有骨架与 owner 定义。
