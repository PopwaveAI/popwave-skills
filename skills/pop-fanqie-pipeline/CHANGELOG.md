# CHANGELOG

## v3.1.0 (2026-07-21)

### 新增Phase 3.5 Character + Phase 4子agent红线

- 新增Phase 3.5 Character：plot完成后、write之前，调pop-fanqie-character建角色库。消费分幕设计出场角色清单+骨架敌人梯度+创意主角轮廓，产出设计/角色库.md
- Phase 4 Write改为必须子agent执行：主agent只做路由，子agent指令模板含"必须加载角色库.md，战斗/升级场景必须使用DNA面板格式"
- 红线新增第5条"Phase 4必须用子agent调write"+第7条"Phase 3.5 Character必须执行"
- state模板/调度表/路由表/step2.md全部对齐Phase 3.5
- Skill调度表Phase 4标注"子agent"，Phase 3.5新增行

## v3.0.0 (2026-07-21)

### 项目空间重构 + project-state.html可视化

**根因**：老板在agent环境测试后发现项目空间文件夹分级不合理——0/1/2数字编号和downloads/写作参考/涌现功能名混用，1-骨架文件夹混了骨架+剧情白描两个phase的产出，Phase 0产出散落三处。同时project-state.md只有agent能读，人看进度不直观。

**改动**：

- **项目空间重构为四文件夹**：
  - 素材/ = Phase 0产出（调研+DNA+拆书+原书，合并旧写作参考/+涌现/+downloads/）
  - 设计/ = Phase 1-3产出（创意+骨架+剧情白描，合并旧0-立项/+1-骨架/）
  - 正文/ = Phase 4产出（逐章渲染，旧2-正文/改名）
  - 审核/ = Phase 5产出（审核记录，保持不变）
- **project-state.html可视化**（v3.0.0新增）：
  - 每次更新project-state.md时同步生成project-state.html
  - 自包含单文件（内联CSS+JS），浏览器直接打开
  - 内容板块：项目名+时间戳 → Phase进度条(6个phase可视化) → 下一步操作 → 底牌就绪卡片 → 创意摘要卡片 → 最近产出表格
  - 模板文件：templates/project-state.html.tpl（占位符替换方式生成）
- **路径映射表**：SKILL.md新增旧→新路径映射表，所有路径引用统一更新
- **step1.md**：初始化目录改为四文件夹（素材/素材/downloads + 素材/知识沉淀 + 设计 + 正文 + 审核）+ 1d新增生成project-state.html
- **step2.md**：路由分流对齐6 phase结构 + 新路径 + 每次更新state.md后同步生成state.html的规则
- **SKILL.md红线**：新增红线2"每次更新state.md必须同步生成state.html"
- **批量路径替换**：番茄skill群15个文件共89处路径引用统一更新（seed/world/plot/write/review/research/dna-style）
- **Skill调度表**：新增"产出路径"列，每个phase的产出文件路径一目了然

## v2.1.0 (2026-07-21)

### Phase 2拆分为World+Plot，设定设计与叙事创作分离

**根因**：原Phase 2=Plot聚合了设定设计（力量体系→地图→势力→危机→弧线）和叙事创作（剧情白描+章锚点表）两个能力域。混在一个skill里压力太大，设定设计的质量瓶颈会拖累叙事创作。

**改动**：
- **Phase拆分**：原Phase 2(Plot)拆为Phase 2(World)+Phase 3(Plot)
  - Phase 2: World → 调pop-fanqie-world，产出骨架.md
  - Phase 3: Plot → 调pop-fanqie-plot，消费骨架.md，产出剧情白描.md+章锚点表.md
- **后续phase重编号**：原Phase 3(Write)→Phase 4，原Phase 4(Review)→Phase 5
- **project-state.md模板**：phase枚举增加phase5，阶段完成情况拆分为6项
- **速查表**：启动判断表+Skill调度表同步更新
- **skill.json**：v2.0.0→v2.1.0

**关联改动**：
- 新建 pop-fanqie-world v1.0.0
- pop-fanqie-plot v2.1.1→v3.0.0（瘦身）

## v1.0.0 (2026-07-20)

### 新建pop-fanqie-pipeline skill

**根因**：R41全链路测试+7-20项目a实际运行诊断发现管线三大结构性缺口：
1. 没有"我在哪"的文件——agent启动时没有任何落盘文件告诉它当前在管线的哪个阶段
2. skill之间盲调度——每个skill只知道自己的SOP，不知道何时该调下游
3. 参考书是"用户提了才触发"的可选项——seed 1a不问参考书，用户不提就永远跳过

**设计**：
- SKILL.md：项目初始化+project-state.md模板+5个phase路由规则+红线5条+速查表
- step1.md：初始化。创建标准目录结构（8个子目录）+ 落盘project-state.md（phase=init）
- step2.md：路由。读project-state.md → 按phase值分流到5个phase执行，每个phase完成后更新state
- skill.json：v1.0.0

**Phase 0参考书闸门**（最关键的改动）：
- 进入Phase 1 Seed前，必须先通过Phase 0参考书摸底
- 三条路径：用户给书名→download+dna-style / 用户没想好→research推荐→download+dna-style / 用户明确拒绝→标注风险
- 不完成参考书摸底，不进入Phase 1

**项目目录结构**：
```
项目/
├── project-state.md        ← 管线状态追踪
├── 0-立项/
├── 1-骨架/
├── 2-正文/
├── 审核/
├── 涌现/
├── downloads/
└── 写作参考/知识沉淀/
```
