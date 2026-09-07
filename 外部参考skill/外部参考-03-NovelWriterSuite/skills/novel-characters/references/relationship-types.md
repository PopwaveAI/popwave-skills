# 关系类型清单 + 反向对应

> 加关系时必须双向维护。下表给出每个关系类型的"反向类型"。

---

## 家族 / 血缘类

| 类型 | 反向 | 说明 |
|---|---|---|
| `parent` | `child` | 父母 - 子女 |
| `child` | `parent` | |
| `sibling` | `sibling` | 兄弟姐妹（对称） |
| `spouse` | `spouse` | 夫妻（对称） |
| `lover` | `lover` | 恋人 / 情人（对称） |
| `ex-lover` | `ex-lover` | 前任（对称） |
| `cousin` | `cousin` | 表 / 堂兄弟姐妹（对称） |
| `relative-by-marriage` | `relative-by-marriage` | 姻亲（对称） |
| `adopted-parent` | `adopted-child` | 收养关系 |

## 师承 / 教导类

| 类型 | 反向 | 说明 |
|---|---|---|
| `mentor` | `apprentice` | 师 - 徒 |
| `apprentice` | `mentor` | |
| `senior-disciple` | `junior-disciple` | 师兄 - 师弟 |
| `junior-disciple` | `senior-disciple` | |
| `master` | `servant` | 主 - 仆 |
| `servant` | `master` | |

## 友敌 / 政治类

| 类型 | 反向 | 说明 |
|---|---|---|
| `friend` | `friend` | 朋友（对称） |
| `ally` | `ally` | 盟友（对称） |
| `rival` | `rival` | 对手（对称，竞争但未必敌对） |
| `enemy` | `enemy` | 敌人（对称） |
| `sworn-brother` | `sworn-brother` | 义兄弟（对称） |
| `superior` | `subordinate` | 上下级 |
| `subordinate` | `superior` | |
| `colleague` | `colleague` | 同事 / 同僚（对称） |

## 复杂 / 暧昧类

| 类型 | 反向 | 说明 |
|---|---|---|
| `crush` | `crushed-on` | 单恋（A 喜欢 B，B 未必知） |
| `crushed-on` | `crush` | |
| `protector` | `protected` | 保护者 - 被保护者 |
| `protected` | `protector` | |
| `creditor` | `debtor` | 债主 - 欠债人 |
| `debtor` | `creditor` | |
| `target` | `assassin` | 暗杀目标 - 刺客 |
| `assassin` | `target` | |
| `idol` | `fan` | 偶像 - 仰慕者 |
| `fan` | `idol` | |
| `creator` | `creation` | 创造者 - 被创造者（如造神 / 转世 / 复制）|
| `creation` | `creator` | |

## 一次性 / 临时类

| 类型 | 反向 | 说明 |
|---|---|---|
| `met-briefly` | `met-briefly` | 一面之缘（对称） |
| `saved-life` | `was-saved-by` | A 救过 B |
| `was-saved-by` | `saved-life` | |
| `killed` | `killed-by` | A 杀了 B |
| `killed-by` | `killed` | |

---

## frontmatter 写法示例

```yaml
relationships:
  - character: kael-voss
    type: sibling
    note: "两人相依为命 12 年"   # 可选注释
  - character: lord-maren
    type: enemy
    note: "杀父仇人，亲手处决了父母"
```

对方文件应该有：

```yaml
relationships:
  - character: sera-voss
    type: sibling
    note: "见 sera-voss 文件"
  - character: sera-voss
    type: enemy
    note: "(maren 视角) 反叛者，威胁我的统治"
```

注意：**`note` 是可以从双方视角不同的**——比如 maren 把 sera 看作"反叛者"，sera 把 maren 看作"杀父仇人"。这种视差是好故事的重要元素。

---

## 关系的状态变化

关系不是静态的。可以通过 `## 关键时间线` 标注关系的演变：

```markdown
## 关键时间线

| 时间 | 事件 | 章节 |
|---|---|---|
| 卷一前 | 与 lord-maren 是世交 | Backstory |
| 卷一第 3 章 | maren 政变，关系破裂 | Ch 3 |
| 卷二第 8 章 | 关系从 enemy 转为 reluctant-ally（共同对抗更大敌人） | Ch 38 |
```

frontmatter 始终保留**当前**的关系状态。**历史**关系写在 timeline。

---

## 自定义关系类型

如果上表没覆盖你的情况，可以自定义。建议遵守：
- 用 `kebab-case`
- 反向类型必须明确（即使是 `unknown`）
- 在角色卡的"注意点"段说明这个自定义类型的语义
