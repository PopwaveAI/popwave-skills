# 管线全链路合同模式

## 动机

6.18项目B事故：Agent creative完成后跳过了reservoir直接进了world。根因是**子skill的pipeline字段只声明相邻关系（"我的上游是谁"），不声明全链顺序（"我在全链第几步"）**。Agent从world的`upstream: [creative]`推断出"creative→world"是正确顺序——语义上对，顺序上错。

## 模式

### 核心思想

全链顺序不由子skill各自声明，而由**编排者（orchestrator）持有单一的真相源**。编排者就是expert-writer itself。

编排者首次加载时，先把全链stage顺序表灌入Agent上下文。之后每次阶段交接，Agent查此表确定下一步，不依赖下一阶段的SKILL.md声明的upstream/downstream。

```yaml
# 编排者中存在一张表
Stage 1: skill-A → 产出X
Stage 2: skill-B → 产出Y  (前置: X已存在)
Stage 3: skill-C → 产出Z  (前置: X+Y已存在)
```

### 个体skill的pipeline字段设计原则

每个子skill的pipeline字段仍然保留`upstream`和`downstream`，但含义变为：
- `upstream`: "我消费谁的产出"（知识依赖，非执行顺序）
- `downstream`: "谁消费我的产出"（产出流向，非执行顺序）

加上`note`字段解释顺序约束（因为YAML frontmatter没有标准的"先后"字段）。

### 从manifest推断当前位置

编排者首次加载时（或会话恢复时），遍历项目目录检查每个stage的典型产出物是否存在，从manifest表中定位当前进度。这比依赖workspace-index.yaml更鲁棒（文件系统从不撒谎）。

```
如果 L1-01~06.md 存在 → world已完成
如果 剧情线/主线-01.md 存在 → plot已完成
如果 ch001-设计包.md 存在 → chapter已完成
以此类推。以最后修改时间戳为准判断"最新阶段"。
```

## 适用场景

此模式适用于任何**多步骤流水线**（不只是网文创作）。核心判断标准：流水线的步骤顺序是否对产出质量有硬性影响。如果是（如creative→reservoir→world的顺序错了会导致world产出缺失素材储备），就应使用此模式。

## 反模式

- **让子skill自己声明顺序**：子skill的pipeline字段理论上可以加`order: 3`，但这要求所有skill维持同一个数字序列——维护成本高，且不同编排者的实例会有冲突。
- **在workspace-index.yaml里硬编码**：这也是一个方案，但index是运行时状态（可能丢失/过期），manifest是skill的静态定义（始终在）。
