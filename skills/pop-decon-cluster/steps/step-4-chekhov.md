# Step 4：契诃夫枪追踪

> **方向**：扫描全文识别「设伏→回收」对，追踪每把契诃夫枪的完整生命周期。
> **级别覆盖**：前N章 / 全书

---

## 数据来源

- `_temp/baseline-data.json` → `events[]` + `characters[]` + `items[]`
- `_temp/plot-data.json` → `majorEvents[]`
- Phase 1 事实骨架（写作资产/事实骨架/）

## 采集范围

从事实骨架中采集以下类型的「首次出现但未回收」元素：

| 类型 | 示例 |
|:-----|:-----|
| **物品** | 神秘道具/武器/信件 | 
| **角色** | 提及但未登场的幕后角色/组织 |
| **设定伏笔** | 预言的暗示/隐藏身份/未解的谜团 |
| **事件前置** | "看似偶然"的事件/未完成的对话线索 |

## 契诃夫枪标注格式

```yaml
chekhov_guns:
  - id: "gun-001"
    type: "物品"
    name: "琥珀吊坠"
    description: "ch3 主角在废墟中发现"
    set_in: { ch: 3, context: "废墟寻宝场景" }
    fired_at: { ch: 45, context: "吊坠发光抵御诅咒" }  # 或 null（未回收）
    status: "fired"  # 或 "pending"
    notes: ""
```

> **核心约束**：每把枪必须有 set_in 的章节证据。不得凭空编造未在原文中看到的伏笔。
> 未回收的枪标注 `status: "pending"`「Lv3 可能回收」。

---

## 产出

| 文件 | 内容 |
|:-----|:-----|
| `设计/幕/vol-01/chekhov-tracker.yaml` | 本卷内契诃夫枪链（设伏→回收） |

---

## 落盘检查

- [ ] 每把枪标注了 set_in chXX 证据
- [ ] 已回收的枪标注了 fired chXX 证据
- [ ] 未回收的枪标注 `pending`
- [ ] 没有从外部知识编造的契诃夫枪
