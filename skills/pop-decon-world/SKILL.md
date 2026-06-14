# pop-decon-world · 归纳世界观 v1.0.0

> **定位**：Phase 3 of deconstruction. 从 world-data.json 归纳 L1 六件套 + 世界宪法 + 数值体系。
> **级别覆盖**：Lv2(ch1-100) / Lv3(全书) | **前置**：Phase 1 + Phase 2 已完成（Lv1 跳过）

## 管线位置

```
正文 → 事实提取 → 聚类卷幕 → 归纳世界观 → 归纳故事引擎 → 验证打包
       Phase 1    Phase 2    Phase 3      Phase 4        Phase 5
                                          ↑
                               这是你在这里 ← Phase 3
```

**upstream**: pop-decon-cluster | **downstream**: pop-decon-engine | **expert**: pop-decon

---

## 速查表

| 步骤 | 操作 | 读什么 | 数据来源 | 产出 | 门禁 |
|:-----|:-----|:-------|:---------|:-----|:-----|
| 1 | 地理蓝图 | world-data.json#geography | Phase 2 卷地理范围 | `L1-01-世界蓝图.md` | — |
| 2 | 力量体系 | world-data.json#class/#magic | Phase 1 角色卡 | `L1-02-力量体系.md` | — |
| 3 | 历史驱动力 | world-data.json#deity/#faction | Phase 2 主线 | `L1-03-历史与驱动力.md` | — |
| 4 | 物种与天赋 | world-data.json#species | Phase 1 怪物数据 | `L1-04-物种与天赋.md` | — |
| 5 | 势力格局 | world-data.json#faction | Phase 2 卷势力动机 | `L1-05-势力格局.md` | — |
| 6 | 资源与物品 | world-data.json#item | — | `L1-06-资源与物品.md` | — |
| 7 | 世界宪法 | L1 六件套 | 叙事规律 | `世界宪法.md` | ≥3 原文证据 |
| 8 | 数值体系 | world-data.json#class | 战斗章数据 | `combat_capability.yaml` | — |
| 9 | 起点/终点快照 | Phase 1 角色状态 | Phase 2 卷边界 | `起点/终点快照.md` | — |

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **Phase 2 未完成就归纳** — 全书架构.md 不存在 → 退回 Phase 2 |
| ❌2 | **凭空发明设定** — world-data.json 无条目且未标注「数据极少」的名称 |
| ❌3 | **编造境界链** — 原文从未出现的分级体系（如「凡人→超凡→破格」） |
| ❌4 | **Lv2 产出 Lv3 文件** — Lv2 不产出故事引擎/设计包反推 |
| ❌5 | **归纳=编造** — JSON 有条目=归纳，没有且未标注=编造 |

## ❌ WRONG 示例

| 错误做法 | 问题 |
|:---------|:-----|
| 凭空发明「凡人→超凡→破格→神话」境界链，原文未出现 | 编造设定，违反红线 3 |
| Lv2 产出 `故事引擎.md` 文件 | Lv2 数据不足，违反红线 4 |
| 力量体系分类无 world-data.json 条目支撑 | 无 JSON 条目=编造，违反红线 5 |

## 边界条件

| # | 场景 | 处理 |
|:-:|:-----|:-----|
| 1 | world-data.json 某分类为空数组 | 注明「前 N 章此维度数据极少」，跳过该模板 |
| 2 | 原文设定前后矛盾（ch10 vs ch80） | 取最新版本，标注矛盾点及出现章节 |
| 3 | Lv2 止步不执行 Phase 4 | 跳过故事引擎，直接进入 Phase 5 |
| 4 | 起点/终点快照角色状态缺失 | 标注「数据不足」，引用最近可用章 |
| 5 | 数值体系数据不足（战斗章 <3） | 产出可用数据，标注「样本不足」 |
| 6 | 第一人称视角局限 | 注明视角局限，区分「原文明确」和「角色推断」 |

---

## 前置数据确认

```
[ ] _temp/world-data.json（7 大类） [ ] _temp/baseline-data.json
[ ] Phase 2 — 全书架构.md + 卷/幕       [ ] Phase 1 — 角色卡
```

> **核心理念**：归纳≠编造。写作是引擎→设定→正文，拆书是正文→设定→引擎。每件套回答「走到第 N 章积累了什么原文证据」。填写前：打开 entries[] → 浏览 → 高频模式 → 每模式标注 ≥2 个 chXX 出处。

---

## 落盘检查点

```
Lv2: L1-01~06 + 世界宪法 + combat_capability + 起点快照
Lv3: + 终点快照 + L1 全书版
```

## 完成 → Phase 4（Lv3）或 Phase 5（Lv2 止步）

---

> v5.0
