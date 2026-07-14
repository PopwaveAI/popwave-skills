# CHANGELOG

## v1.0.0 - 2026-07-14

### 新建：番茄 onepiece 复制更名
- 从番茄小说创作skill群的 prose-render-onepiece 复制更名为 pop-emergent-write-onepiece。
- 新增 frontmatter（name: pop-emergent-write-onepiece）。
- 新增 execution.mode（formal/draft/trial 三档，引用 PRD §4.5）。
- Step 1 适配：加入 current-state 消费规则，读取 current-state.md 获取下一章硬推进。
- 新增正文落盘规则：正文落盘到 `涌现/正文/{书名}-第{N}章-{标题}.txt`，对话中只回摘要+钩子+创作记录。
- 保留番茄 onepiece 全部内容：三层架构/SOP/赛道定义/战斗模式/API管道注入规范等。
- 流派技法/ 目录从源完整复制。
