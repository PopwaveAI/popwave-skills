# CHANGELOG

## v2.0.0 - 2026-07-14

### 版本升级：番茄 prose-render 覆盖
- 用番茄小说创作skill群的 prose-render 完整覆盖替换 pop-emergent-write 的 SKILL.md。
- 新增 frontmatter（name: pop-emergent-write）。
- 新增 execution.mode（formal/draft/trial 三档，引用 PRD §4.5）。
- Step 1 适配：将"读取施工卡"改为"读取 current-state.md（含下一章硬推进+人物状态+燃料队列+伏笔债务）+ dna/ 目录下的笔触DNA文件"。
- 新增正文落盘规则：正文落盘到 `涌现/正文/{书名}-第{N}章-{标题}.txt`，对话中只回摘要+钩子+创作记录。
- 保留番茄 prose-render 全部内容：6章型骨架/17微观技法/五层指导/章意图思考/微观技法选择/验收表等。
- references/ 目录从番茄 prose-render 源完整复制（含情境技法/流派专属/通用技法子目录 + 8个根文件）。
- dna/ 目录从番茄 prose-render 源完整复制（4个笔触DNA文件）。
- 保留现有 templates/chapter-record.tpl.md 和 steps/ 目录。

## v3.7.0 - 2026-07-09

### 调整：章内文风DNA消费
- `文风DNA执行` 从 scene 卡、层1/2/3约束改为 DNA源、模式、章型、笔触目标、章内套路、可见反馈和禁止误用。
- 正文门禁改为检查章内笔触和单章套路是否参与生成，强嫁接只迁移章内套路和笔触手感。
- 创作记录模板同步为章内DNA字段。

## v3.6.0 - 2026-07-08

### 新增：文风DNA三层消费
- 当 soul/current-state/用户要求启用 DNA 时，write 必须消费 `本章DNA执行包` 和对应 DNA 源片段。
- 本章写作包新增 `文风DNA执行` 字段，要求列出 DNA源、模式、scene 卡序列、层1/2/3约束和禁止误用。
- 正文规则新增 DNA 落地门禁：不能只替换形容词，必须影响场景组织和商业反馈。
- 创作记录模板新增"执行的文风DNA约束"。

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
