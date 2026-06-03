---
name: "pop-reader-making"
version: "0.14.1"
description: "拆解长篇小说为结构化参考文件。Phase A 产出双格式：叙事笔记(MD) + 结构化数据(YAML含章节标注/实体共现/卷统计/角色image_prompt/名场面image_prompt)，供 pop-html-anything 直接消费渲染。与 book-deconstructor（拆书为写）协作。"
---

# pop-reader-making · 网文拆书技能

## 定位
帮读者拆解长篇小说。**产出双格式：人类可读的叙事笔记 + 机器可消费的结构化 YAML。**

## 协作边界

> ⚠️ **拆书定位声明：** 本 skill（pop-reader-making）面向"拆书为读"——产出供读者查阅的叙事笔记和供 pop-html-anything 渲染的结构化 YAML（含 image_prompt）。
>
> 同级 skill `book-deconstructor`（位于 `pop-novel-agent-pro` 内部）面向"拆书为写"——产出供给 emergent-writer 的 14 项输入包和 scene_fragments.db。
>
> **分工：**
> - pop-reader-making → 消费方：读者 / pop-html-anything → 产出：叙事笔记.md + 结构化YAML（含 image_prompt）
> - book-deconstructor → 消费方：emergent-writer / project-bootstrap → 产出：scene_fragments.db + 节奏地图 + 对标规则

---

## 核心流程：五段式

```
Phase 0 ─ 书稿预检（先定分卷，再定拆法）
  ├─ Step 0.1 通读目录定分卷
  ├─ Step 0.2 密集抽样验证分卷
  ├─ Step 0.3 产拆书方案（核心：分卷定界表）
  └─ Step 0.4 用户确认方向     ← 第一道门禁

Phase A ─ 按卷深度阅读 + 结构化标注（双格式产出）
  ├─ Step A.1：逐章阅读 → 产出叙事笔记（保持节奏，可读）
  ├─ Step A.1.5：逐章产出 YAML 结构化标注 ← ★ 新增
  ├─ Step A.2：读完一卷后，产出关键实体列表（含 image_prompt + 共现矩阵 + 卷统计 + 名场面）
  └─ Step A.3：用户确认本卷质量后，进入下一卷

Phase B ─ 跨卷关联（打通整书的理解）
Phase B+ ─ 方案复盘验证
Phase C ─ 按需结构化（只在需要时做）
```

---

## 拆分阶段详解

### Phase A — 按卷深度阅读 + 结构化标注

#### 核心原则

保持叙事完整性 + 同步产出结构化数据。**两条线并行，互不替代。**

叙事线（给人读）→ 保持章节顺序、叙事节奏、阅读判断
结构线（给机器）→ 每章的 entities/events/metrics/signals/tone + 角色/名场面/共现

---

#### Step A.1：产出分卷阅读笔记（叙事线）

每卷读完后产出 `{书名}_卷{序号}_{卷名}_笔记.md`。

笔记包含四个部分：

##### 一、魔改对照（IP衍生/无限流/诸天流类小说必做）

回答三个问题：
1. 这卷借用了什么原作？
2. 作者改了什么？
3. 改得怎么样？

##### 二、章节叙事流（★ 核心）

按章节顺序写。每3-5章为一节，每节包含【摘要】+【执行观察】。

执行观察类型：节奏判断 / 魔改效果 / 信息密度 / 结构评价 / 作者意图 / 阅读体验

##### 三、本卷关键实体（精简版）

只记重要角色和设定。详见下方 Step A.2。

##### 四、本卷质量判断

```
阅读体验：[流畅/拖沓/起伏大]
魔改质量：[精彩/一般/生硬]
最佳段落：____
最弱段落：____
一句话总结：____
```

---

#### Step A.1.5：逐章结构化标注（★ 结构线）

读完叙事流后，为每一章产出结构化元数据。这份数据与叙事流并存。

**每章的标注模板：**

```yaml
ch1:
  title: "大脑超频"
  entities: ["陈昂", "露西", "理查德"]
  events:
    - type: "穿越"
      summary: "陈昂自永无止境世界返回现实"
      participants: []
    - type: "对话"
      summary: "拦截露西和理查德，夺取CPH4"
      participants: ["陈昂", "露西", "理查德"]
  metrics:
    出场角色数: 3
    事件数: 2
    信息密度: 高
  signals: ["NZT副作用未提及—陈昂已适应"]
  tone: "兴奋好奇"
  key_entities: ["陈昂"]
```

**产出说明：**
- 放在叙事流之后，顺序一致
- 每章1-5条 events
- `events.type` 从以下取：`战斗 / 对话 / 探索 / 设定揭示 / 伏笔 / 转折 / 日常 / 穿越`

---

#### Step A.2：读完一卷后，产出关键实体列表（增强版）

除了基础的角色/势力/设定表，**额外产出一份结构化数据**：

##### 角色表（含 image_prompt）

| 角色 | 身份 | 本卷关键事件 | 章节 | 出场章节数 | 角色重要性 | 肖像 prompt |
|:----|:----|:-----------|:----:|:---------:|:---------:|:------------|
| 陈昂 | 主角 | 获得NZT、CPH4、进入笑傲 | 1-26 | 26 | ⭐⭐⭐主角 | Chinese xianxia novel protagonist portrait: ... |

> **image_prompt 必须写。** 这是 pop-html-anything 生图的直接输入。prompt 结构：`[内容类型]: [视觉描述], [氛围], high quality digital illustration, cinematic lighting`

##### 本卷名场面

选取本卷 3-8 个最具画面感/叙事转折意义的名场面：

| 场景 | 章节 | 类型 | 画面描述 | image_prompt |
|:----|:----:|:----:|:---------|:------------|
| 场景名 | 章节 | 类型 | 画面简述 | Chinese novel cinematic scene: ... |

**名场面判断标准：** ①有强烈视觉画面感 ②推动关键剧情转折 ③角色情感高潮点

##### 实体共现矩阵

| 共现对 | 共同出场章节数 | 关系强度 |
|:------|:-------------:|:--------|
| 陈昂 ↔ 丁勉 | 8 | ⭐⭐⭐ 大量 |

##### 本卷关键数据统计

```
卷统计：
  总章节数: 26
  总出场角色数: 18
  核心角色(出场>50%章): 4
  事件总数: 62
  战斗事件: 18
  对话事件: 15
  情绪曲线: 兴奋好奇 → 试探布局 → ... → 从容收官
```

---

#### Step A.3：用户确认后进入下一卷

---

### 产出文件

```
小说项目/<书名>/
├── 拆书方案.md                     ← Phase 0
├── {书名}_卷{序号}_笔记.md          ← Phase A（叙事线）
├── {书名}_卷{序号}_结构化数据.yaml   ← Phase A（★ 结构线，供 pop-html-anything 消费）
├── {书名}_跨卷关联笔记.md            ← Phase B
```

> `*_结构化数据.yaml` 是纯结构化版本，包含 volume_stats + chapters[]（含 entities/events/metrics/signals/tone）+ characters[]（含 image_prompt）+ scenes[]（含 image_prompt）+ entity_cooccurrence[]。pop-html-anything 直接读取此文件渲染。

---

## 方法/ 工具索引

| 文件 | 用途 | 所属阶段 |
|:----|:----|:-------:|
| `phase_b_分析协议.md` | 因果链/伏笔线/剧情线/书特有机制的结构化产出模板 | Phase B |
| `gen_html_knowledge_graph.py` | 从 novel.db 生成知识图谱 HTML（力导向图） | Phase C（可选） |

> 所有工具位于 `方法/` 目录下。

---

## 更新日志

### v0.13.1 — 2026-05-31
- **新增 Step A.1.5：逐章 YAML 结构化标注**
  - 每章产出 entities/events/metrics/signals/tone
  - 与叙事流并存，不替代原有阅读笔记
- **Step A.2 角色表新增 image_prompt 列**
  - 每个重要角色产出肖像级 image_prompt
  - 固定尾部：`high quality digital illustration, cinematic lighting`
- **Step A.2 新增「本卷名场面」表**
  - 每卷 3-8 个，含场景级 image_prompt
- **Step A.2 新增实体共现矩阵 + 卷统计**
- **新增产出文件：`*_结构化数据.yaml`**
- **产出管线双格式化**：叙事笔记(MD) + 结构化数据(YAML)
- **pop-html-anything v2.4 配套**：Step 4.5 直接读取 YAML 中预写的 image_prompt 生图
