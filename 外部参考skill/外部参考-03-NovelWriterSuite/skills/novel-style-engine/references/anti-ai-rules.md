# 默认反 AI 规则库（中文网文向）

> 在 `novel-init` 阶段拷贝到 `style/anti-ai.md` 作为默认值。用户可在 `novel-style-engine` 中编辑。
> 借鉴 inkos post-write-validator.ts + novel-writer SKILL.md 的禁用清单，独立整合。

---

## forbidden（绝对禁止）

最高优先级，违反一次即报 critical。

### 句式类

```yaml
- pattern: "不是.+而是"
  description: "AI 特征句式（直白对比）"
  weight: 1.0

- pattern: "并非.+而是"
  description: "AI 特征句式变体"
  weight: 1.0

- pattern: "与其说.+不如说"
  description: "AI 喜欢的强对比模板"
  weight: 1.0

- pattern: "——"
  description: "破折号在中文网文中是 AI 痕迹"
  weight: 1.0
```

### 元叙事 / 上帝视角

```yaml
- pattern: "读者(可能|会|应该|也许)"
  description: "元叙事 - 跳出叙述跟读者对话"
  weight: 1.0

- pattern: "接下来(就是|将会|即将)"
  description: "编剧旁白模式"
  weight: 1.0

- pattern: "(后面|之后)(会|将|还会)"
  description: "未来预告 - 元叙事"
  weight: 1.0

- pattern: "(故事|剧情)(发展)?到了"
  description: "编剧旁白"
  weight: 1.0

- pattern: "我们(可以|不妨|来看)"
  description: "讲解员口吻"
  weight: 1.0
```

### 学术 / 报告腔

```yaml
- pattern: "值得注意的是"
  description: "学术报告腔"
  weight: 1.0

- pattern: "(核心|关键)在于"
  description: "学术报告腔"
  weight: 1.0

- pattern: "(从某种意义上说|从某种角度来看)"
  description: "AI 模糊表达"
  weight: 1.0
```

### 说教 / 上帝判断

```yaml
- pattern: "显然"
  description: "AI 喜欢的说教词"
  weight: 1.0

- pattern: "毋庸置疑"
  description: "上帝判断"
  weight: 1.0

- pattern: "不言而喻"
  description: "上帝判断"
  weight: 1.0

- pattern: "众所周知"
  description: "强行设定"
  weight: 1.0

- pattern: "不难看出"
  description: "强行引导读者"
  weight: 1.0
```

### 分析报告术语（不应出现在正文）

```yaml
- pattern: "(核心动机|信息边界|信息落差|核心风险)"
  description: "学术分析词汇漏到正文"
  weight: 1.0

- pattern: "(锚定效应|沉没成本|认知共鸣|利益最大化)"
  description: "经济学/心理学术语漏到正文"
  weight: 1.0

- pattern: "(行为约束|性格过滤|情绪外化)"
  description: "分析报告词"
  weight: 1.0
```

### 全场震惊式

```yaml
- pattern: "(全场|众人|所有人|在场的人)([，,]?)?(都|全|齐齐|纷纷)?(震惊|惊呆|倒吸凉气|目瞪口呆|哗然|惊呼)"
  description: "集体反应模板 - 写具体某个人的反应代替"
  weight: 1.0

- pattern: "(全场|一片)([，,]?)?(寂静|哗然|沸腾|震动)"
  description: "全场反应"
  weight: 1.0
```

---

## risk（频次监控）

中等优先级，超过密度阈值即报 warning。

```yaml
- pattern: "(突然|忽然|猛然|猛地)"
  max-per-3000: 1
  description: "AI 常用突兀转折词"

- pattern: "(似乎|可能|或许|大概)"
  max-density-per-1000: 3
  description: "套话密度 - 模糊语气"

- pattern: "(然而|不过|与此同时|另一方面|尽管如此|话虽如此)"
  max-per-3000: 3
  description: "公式化转折词"

- pattern: "(此外|另外|同时|并且|因此|所以)"
  max-per-3000: 5
  description: "AI 偏爱的衔接副词"

- pattern: "(最终|最后|结局是|结果是)"
  max-per-3000: 2
  description: "过度总结词"

- pattern: "(仿佛|宛如|犹如|好像)"
  max-per-3000: 3
  description: "比喻过密"

- pattern: "(竟然|居然|没想到|原来)"
  max-per-3000: 2
  description: "AI 喜欢用的'震惊词'"

- pattern: "(不禁|不由)"
  max-per-3000: 1
  description: "陈词滥调"
```

---

## encourage（鼓励出现）

软规则，提示 writer 加入这类特征。

```yaml
- description: "感官描写（视觉/听觉/嗅觉/触觉/味觉）每场景至少出现 2 类"
  weight: 0.7

- description: "用具体细节而非抽象总结表达情绪"
  weight: 0.85
  example: "他握紧拳头，指节发白 优于 他很愤怒"

- description: "对话中夹动作和神态作打断"
  weight: 0.7
  example: |
    "你早就知道了。" 她沉默了很久才说。

- description: "段落长度有变化，长短句交替"
  weight: 0.65

- description: "章节结尾使用具体钩子（动作/对话/消息/场景转换）"
  weight: 0.8

- description: "重要场景用画面+动作呈现，不要直接说情绪"
  weight: 0.8
```

---

## 使用方式

`novel-init` 创建项目时，把这份默认值拷贝到 `style/anti-ai.md`。
用户可以在 `novel-style-engine` 中：
- 增删条目
- 调整 weight
- 改 description / example

每次修改后跑 `compile_style.py` 重新编译。
