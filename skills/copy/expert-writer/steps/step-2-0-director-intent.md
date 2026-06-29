# Step0：导演意图提取 — 从幕纲创作节拍表组装单章约束

> **执行者**：主会话
> **输入**：幕纲（`卷纲/幕NNN-名称.md`）创作节拍表 + 活记忆最新状态
> **产出**：导演意图 YAML（≤150字核心 + 五问 + settings_ref）
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
3. 确认门禁表 Step0 的硬门禁：导演意图含五问+settings_ref+用户确认

---

## 2. 读取幕纲 + 推演

1. `Get-Content -Encoding UTF8 -Raw` 读取 `卷纲/幕NNN-名称.md`（正式幕纲）
2. 定位 **创作节拍表**（幕纲内每章一张的节拍表）
3. 找到本章对应的节拍表
4. `Get-Content -Encoding UTF8 -Raw` 读取 `卷纲/推演/幕NNN-名称-推演.md`（推演过程文件）
5. 找到本章对应的推演段，感受故事流动

> 幕纲是正式活文档（节拍表/子线/红线），推演是过程性参考文件（故事流动/画面/对白锚点）。
> 导演意图的event_chain从节拍表提取结构，从推演段感受故事流动。

---

## 3. 组装导演意图

从幕纲创作节拍表本章表提取字段，组装为导演意图 YAML：

```yaml
director_intent:
  chapter: 3                                    # 本章章号
  source: 卷纲/幕NNN-名称.md#创作节拍表          # 来源
  narrative_function: "首次猎杀+战力跃升"         # 情绪目标（一句话）
  event_chain: "搜索圈逼近→决定反杀→废弃厂房双杀→系统升级→街头感知解锁→第二次猎杀→发现命运迷宫纹→灵能警告"
                                                # 从节拍表各字数段的动作链合并
  emotion_curve: "紧迫→冷酷执行→满足升级→警觉"    # 情绪目标+字数段情绪的合并
  pacing: "快→极快→中→快→极快→冷(双重钩子)"      # 从字数段情绪推导
  sublines_advance:                             # 子线推进（从幕纲嵌套子线表取值）
    - "铁钳帮搜索圈：逼近→触发反杀"
    - "系统：升级+街头感知解锁"
    - "超自然线：命运迷宫纹首次出现"
  chapter_hook: "灵能警告+灰色注释（超自然悬念）"  # 章末钩子
  unit_redlines:                                # 单元红线（v1.4新增）
    - "ch001必须完成：系统觉醒+第一次战斗+第一次击杀反馈"
  worldview_delivery:                           # 世界观传递（v9.6新增）
    core_selling_point: "邪神渗透美国+超凡复苏+大选博弈"  # 本书核心卖点
    chapter_must_deliver: "通过索伦回忆/系统面板/薇薇安对话让读者感知邪神渗透现实"  # 本章必须传递什么
    method: "回忆闪回+系统面板注释"               # 传递方式
  five_questions:                                # 五问（核心约束，v9.6从三问扩展）
    info: "读者必须知道系统升级机制"              # 读者必须知道什么？
    pressure: "搜索圈逼近必须推进到触发反杀"      # 压力必须推进到什么程度？
    hook: "章末留灵能警告"                       # 章末留什么钩子？
    worldview: "读者必须感知到邪神渗透这个世界"   # 本章传递了什么世界观？
    clarity: "小学生能直接看懂这章发生了什么"     # 读者读完是否清晰知道发生了什么？
  settings_ref:                                 # 设定引用指针（Step2强制读取）
    - "写作参考/设定/金手指.md#升级机制"
    - "写作参考/设定/主角引擎.md#行为准则"
```

### 导演意图组装规则

1. **narrative_function**：从幕纲创作节拍表本章的"情绪目标"字段取值
2. **event_chain**：从节拍表各字数段的"场景/动作"列合并，保持事件顺序
3. **emotion_curve**：从"情绪目标"+各字数段"读者情绪"合并
4. **pacing**：从字数段节奏推导（0-300快→300-700快→700-1200极快→1200-1800中→1800-2500钩子）
5. **sublines_advance**：从幕纲"嵌套子线"部分取值，拆分为列表
6. **chapter_hook**：从创作节拍表"章末钩子"字段取值
7. **unit_redlines**（v1.4新增）：从幕纲"单元红线"段取值，作为本章额外硬约束
8. **worldview_delivery**（v9.6新增）：从 `写作参考/设定/核心卖点.md` 提取本书核心卖点，判断本章需要传递什么世界观信息、用什么方式传递。前三章尤其重要——读者前三章没get到卖点就会弃书
9. **five_questions**（v9.6从三问扩展为五问）：
   - info：读者读完本章必须知道什么信息？
   - pressure：哪条压力线必须推进到什么程度？
   - hook：章末留什么钩子？
   - worldview：本章传递了什么世界观？（从worldview_delivery推导）
   - clarity：小学生能直接看懂这章发生了什么？（检查是否过于含蓄/文学化）
10. **settings_ref**：从幕纲节拍表"设定引用"列取值，指向 `写作参考/设定/` 下的具体文件+锚点

### 导演意图约束

- 核心部分（narrative_function + event_chain + emotion_curve + pacing）≤150字
- worldview_delivery 是硬约束：create阶段必须通过正文传递本章指定的世界观信息
- five_questions 是硬约束：create阶段必须回答全部五问
- unit_redlines 是硬约束（v1.4新增）：create阶段必须满足本单元红线
- settings_ref 是硬指针：Step2必须强制读取（不靠agent判断）

---

## 4. 【CHECK 1】用户确认

> 红线4：导演意图未经用户确认禁止进入Step1。

1. 将导演意图 YAML 交付用户
2. 用引导语：
   > 本章导演意图已提取。核心叙事功能是「{narrative_function}」。
   > 五问约束：info={info} / pressure={pressure} / hook={hook} / worldview={worldview} / clarity={clarity}。
   > 单元红线：{unit_redlines列表}。
   > 世界观传递：{worldview_delivery.chapter_must_deliver}（方式：{worldview_delivery.method}）。
   > 设定引用：{settings_ref列表}。
   > 请确认导演意图，确认后开始状态快照投影。
3. 等待用户确认
   - 用户确认 → 进入 Step1（状态快照投影）
   - 用户要求修改 → 修改导演意图 → 重新确认
   - 用户拒绝 → 暂停，等待用户指示

---

## 5. 完成条件

- [x] 门禁表已重新读取（红线3）
- [x] 幕纲已完整读取
- [x] 导演意图 YAML 已组装（含五问+settings_ref+worldview_delivery+unit_redlines）
- [x] 导演意图已交付用户确认（红线4）
- [x] 用户已确认 → 进入 Step1
