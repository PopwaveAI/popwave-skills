# Step1：状态快照投影 — 从活记忆+L2卡物理坐标实时投影当前状态

> **执行者**：主会话
> **输入**：活记忆（`活记忆/活记忆.yaml`）最新events + L2卡物理坐标段
> **产出**：状态快照 YAML（≤400字，不持久化，每章实时投影）
> **人工check**：无（自动进入Step2）
> **红线**：无（本步无人工check，自动连贯）

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
```

---

## 1. 读取活记忆

1. `Get-Content -Encoding UTF8 -Raw` 读取 `活记忆/活记忆.yaml`
2. 提取最新 events（最近2-3章的状态变化记录）
3. 提取 baseline（项目初始化时的基线状态）

> 活记忆格式（v3.5）：自然语言段落，每章一段话概括状态变化。
> 不再是7组件结构化YAML，而是按时间顺序追加的自然语言日志。

---

## 2. 读取L2卡物理坐标段

1. `Get-Content -Encoding UTF8 -Raw` 读取 `卷纲/L2-NNN-名称.md`
2. 定位 **物理坐标段**（L2卡中记录当前物理状态的段落）：
   - 主角当前能力/属性
   - 主角当前心理状态
   - 当前所处环境/位置
   - 当前可用资源
   - 当前活跃压力源

> L2卡物理坐标段是结构化的状态记录，与活记忆的自然语言日志互补。
> 活记忆提供叙事状态变化，L2卡物理坐标提供精确数值/状态。

---

## 3. 投影状态快照

从活记忆最新events + L2卡物理坐标段，实时投影当前状态（≤400字）：

```yaml
state_snapshot:
  protagonist:
    ability: "街斗生存者Lv1 | 属性12/17/14/16/15/13"   # 当前能力+属性
    psychology: "警觉、压抑、保护欲驱动"                  # 当前心理状态
    situation: "铁钳帮搜索圈逼近，活动空间收紧"            # 当前处境
    resources: "无武器，有系统面板"                        # 当前资源
    current_goal: "解除铁钳帮追查威胁"                    # 当前目标
  pressures:                                             # 活跃压力源
    - source: "铁钳帮搜索圈"
      countdown: "2章内必须解决"                          # 倒计时
      must_advance: true                                 # 本章必须推进？
    - source: "教团学校渗透"
      countdown: "5章窗口"
      must_advance: false                                # 本章不必须推进
  pending:                                                # 待兑现要素
    foreshadowing: ["灰色注释的来源", "命运迷宫纹的含义"]  # 伏笔
    promises: ["系统升级的后续影响"]                       # 承诺
    reveals: ["铁钳帮背后的势力"]                           # 待揭示
```

### 状态快照投影规则

1. **protagonist**：
   - ability：从L2卡物理坐标段取当前能力等级+属性值
   - psychology：从活记忆最近1-2章的心理变化推导
   - situation：从活记忆最近events的处境描述推导
   - resources：从L2卡物理坐标段取当前持有资源
   - current_goal：从导演意图的narrative_function + pressure推导

2. **pressures**：
   - 从L2卡结构分析表的压力源列表 + 活记忆的推进记录推导
   - countdown：从L2卡物理坐标段的倒计时记录取值
   - must_advance：导演意图的three_questions.pressure指向的压力源 = true

3. **pending**：
   - foreshadowing：从活记忆累积的未兑现伏笔
   - promises：从活记忆累积的未兑现承诺
   - reveals：从L2卡结构分析表的待揭示要素

### 状态快照约束

- 总字数 ≤400字（紧凑、精确）
- 不持久化：每章实时投影，不写入文件
- 传递给Step3作为context manifest的一部分

---

## 4. 完成条件

- [x] 活记忆已读取
- [x] L2卡物理坐标段已读取
- [x] 状态快照 YAML 已投影（≤400字）
- [x] 自动进入 Step2（信息获取）
