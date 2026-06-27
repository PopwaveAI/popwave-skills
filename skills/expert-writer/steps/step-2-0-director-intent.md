# Step0：导演意图提取 — 从L2卡结构分析表组装单章约束

> **执行者**：主会话
> **输入**：L2卡（`卷纲/L2-NNN-名称.md`）结构分析表 + 活记忆最新状态
> **产出**：导演意图 YAML（≤150字核心 + 三问 + settings_ref）
> **人工check**：**【CHECK 1】用户确认** → 确认后才进Step1
> **红线**：❌3 每章Step0开始前必须重新读取门禁表 | ❌4 导演意图未经用户确认禁止进入Step1

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
```

---

## 1. 前置：重新读取门禁表

> 红线3：每章Step0开始前必须重新读取SKILL.md的5步循环核心门禁表。

1. `Get-Content -Encoding UTF8 -Raw` 读取 expert-writer SKILL.md
2. 确认当前在5步循环的 Step0
3. 确认门禁表 Step0 的硬门禁：导演意图含三问+settings_ref+用户确认

---

## 2. 读取L2卡

1. `Get-Content -Encoding UTF8 -Raw` 读取 `卷纲/L2-NNN-名称.md`
2. 定位 **结构分析表**（L2卡内的跨章结构表）
3. 找到本章对应的行

> L2卡是唯一运行时活文档（种子文档已取消）。L2卡结构分析表包含每个章节的结构约束：
> - 章号 / 叙事功能 / 事件链 / 情绪曲线 / 节奏 / 子线推进 / 章末钩子

---

## 3. 组装导演意图

从L2卡结构分析表本章行提取以下字段，组装为导演意图 YAML：

```yaml
director_intent:
  chapter: 3                                    # 本章章号
  source: 卷纲/L2-001-街头之种.md#结构分析表      # 来源
  narrative_function: "首次猎杀+战力跃升"         # 叙事功能（一句话）
  event_chain: "搜索圈逼近→决定反杀→废弃厂房双杀→系统升级→街头感知解锁→第二次猎杀→发现命运迷宫纹→灵能警告"
                                                # 事件链（→分隔）
  emotion_curve: "紧迫→冷酷执行→满足升级→警觉"    # 情绪曲线（→分隔）
  pacing: "快→极快→中→快→极快→冷(双重钩子)"      # 节奏（→分隔）
  sublines_advance:                             # 子线推进（列表）
    - "铁钳帮搜索圈：逼近→触发反杀"
    - "系统：升级+街头感知解锁"
    - "超自然线：命运迷宫纹首次出现"
  chapter_hook: "灵能警告+灰色注释（超自然悬念）"  # 章末钩子
  three_questions:                              # 三问（核心约束）
    info: "读者必须知道系统升级机制"              # 读者必须知道什么？
    pressure: "搜索圈逼近必须推进到触发反杀"      # 压力必须推进到什么程度？
    hook: "章末留灵能警告"                       # 章末留什么钩子？
  settings_ref:                                 # 设定引用指针（Step2强制读取）
    - "写作参考/设定/金手指.md#升级机制"
    - "写作参考/设定/主角引擎.md#行为准则"
```

### 导演意图组装规则

1. **narrative_function**：从L2卡结构分析表本章行的"叙事功能"列取值
2. **event_chain**：从"事件链"列取值，保持→分隔格式
3. **emotion_curve**：从"情绪曲线"列取值
4. **pacing**：从"节奏"列取值
5. **sublines_advance**：从"子线推进"列取值，拆分为列表
6. **chapter_hook**：从"章末钩子"列取值
7. **three_questions**：从L2卡结构分析表本章行推导：
   - info：读者读完本章必须知道什么信息？
   - pressure：哪条压力线必须推进到什么程度？
   - hook：章末留什么钩子？
8. **settings_ref**：从L2卡本章行的"设定引用"列取值，指向 `写作参考/设定/` 下的具体文件+锚点

### 导演意图约束

- 核心部分（narrative_function + event_chain + emotion_curve + pacing）≤150字
- three_questions 是硬约束：create阶段必须回答全部三问
- settings_ref 是硬指针：Step2必须强制读取（不靠agent判断）

---

## 4. 【CHECK 1】用户确认

> 红线4：导演意图未经用户确认禁止进入Step1。

1. 将导演意图 YAML 交付用户
2. 用引导语：
   > 本章导演意图已提取。核心叙事功能是「{narrative_function}」。
   > 三问约束：info={info} / pressure={pressure} / hook={hook}。
   > 设定引用：{settings_ref列表}。
   > 请确认导演意图，确认后开始状态快照投影。
3. 等待用户确认
   - 用户确认 → 进入 Step1（状态快照投影）
   - 用户要求修改 → 修改导演意图 → 重新确认
   - 用户拒绝 → 暂停，等待用户指示

---

## 5. 完成条件

- [x] 门禁表已重新读取（红线3）
- [x] L2卡已完整读取
- [x] 导演意图 YAML 已组装（含三问+settings_ref）
- [x] 导演意图已交付用户确认（红线4）
- [x] 用户已确认 → 进入 Step1
