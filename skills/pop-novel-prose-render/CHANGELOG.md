# CHANGELOG — pop-novel-prose-render

## v1.1.0 — 2026-06-11

### 路径对齐 PRD v1.4 + constitution 移除

- **constitution.yaml 移除**：不再独立读取，约束已由设计包事件链覆盖
- **路径重构**：
  - `03-正文/chXXX.md` → `正文/chXXX.md`
  - `03-写作资产/chXXX-设计包.md` → `写作资产/设计包/chXXX-设计包.md`

### 微爽点密度验证（★ 爽点体系对齐）

- **step-3-verify.md**：新增 §3.1b 微爽点密度检查
  - 逐 500 字块扫描：是否至少有一次小反转/信息碎片/微表情/环境锐化/节奏剪刀？
  - 全章累计 ≥ 5 个微爽点？
  - 章末倒数 500 字密度最高？
  - 不通过 → 回最平淡段落插入微爽点（不改剧情，只加文本技艺）
- **微爽点定义基准** → `pop-novel-plot/templates/payoff-guide.md` §二
- **文风DNA 路径统一**：`00-原始设定/文风DNA/` → `写作资产/文风DNA/`
- **step-1-read-input.md 精简**：去 constitution 前置条件 + 禁止读表去 act-文件 + "读宪法"段落替换为"约束已由设计包覆盖"
- **SKILL.md**：文风DNA 全路径 + 正文路径 + 禁止读表同步更新

## v1.0.0 — 2026-06-09

### 初始版本：从 pop-novel-writer 拆出 Render 层

- **核心定位**：正文渲染阶段——只做风格表达，不验证剧情
- **输入**：事实骨架 + 登场人物卡 + 文风DNA + 锚定章
- **产出**：chXXX.md 完成正文
- **三阶段渲染**：风格锚定 → 逐事件渲染 → 风格验证
- **与 writer 的根本差异**：不读 Canvas/L1，不判断剧情逻辑是否合理
- **子 agent 架构**：由 expert-writer 派子 agent 独立执行
