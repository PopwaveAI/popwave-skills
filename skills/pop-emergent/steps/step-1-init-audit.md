# Step 1: 初始化骨架与审计

> 触发：新建涌现项目 / 项目跑偏 / 审计涌现规范
> 前置：PRD §4 契约层已就位（`../references/v3.5-pipeline-prd.md`）

## 1. 建立骨架

按 PRD §4.1 唯一真相源创建目录结构与空壳文件。骨架定义见 `../references/v3.5-pipeline-prd.md` §4.1，各文件 owner 见 §4.2。

emergent 只建结构，不填写任何文件正文内容。每个空壳文件仅含元数据块（参照 PRD §5 文档元数据协议），正文待对应 owner 填充。

目录结构：

```text
涌现/
  current-state.md          # 入口层（full-required）
  soul.md                   # 入口层（full-required）
  seed-种子文档.md          # 库层
  research-写作燃料.md      # 库层（唯一名称，禁用"燃料库.md"）
  content-mechanics.md      # 库层
  设定库.md                 # 库层
  人物库.md                 # 库层
  剧情线.md                 # 库层
  review-沉淀.md            # 历史层（append-only）
  压缩归档/                 # 历史层
  正文/                     # 产出层
```

空壳文件元数据块模板见 `../templates/skeleton-init.tpl.md`。

## 2. 审计报告

骨架建立后或对已有项目，输出以下审计报告：

```markdown
## 涌现项目审计

- **skill scope**：当前可用 scope 中是否真实存在 pop-emergent-seed/research/write/review
- **skill version**：5 skill 实现版本是否统一 3.5.0
- **current-state**：存在 / 缺失 / 过大（超 2500 字）/ 缺字段
- **soul**：存在 / 缺失 / 空泛 / 越权写事实
- **write 输入闭环**：write 是否只读 current-state + soul + 最近正文 + 用户要求
- **review 闭环**：review 是否更新 current-state 并归档旧版
- **execution.mode**：是否有过度 formal（缺 current-state 仍标 formal）
- **下一步建议**：指向 seed / research / review / write 之一
```

审计必须真实检查 scope，不得沿用历史自称采用。

## 3. 加载门禁

完成审计报告后，暂停。等待用户确认需要修复的缺口项。

## 4. 下一步指引

- 若用户确认修复 current-state / soul 缺口 → 加载 `step-2-fix-route.md`。
- 若骨架齐全无需修复 → 根据审计结果给一次性路由建议（seed / research / review / write），结束本轮。
- 若 scope 中缺少目标 skill → 明说"不可执行该 skill"，不得自称已采用。
