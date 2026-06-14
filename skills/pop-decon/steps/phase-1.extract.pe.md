# Phase 1：事实提取

> **方向**：逆 `prose-render` + `chapter-design`。从正文中提取逐章事实骨架——事件/角色出场/状态变化/信息披露。
> **级别覆盖**：Lv1(ch1-20) / Lv2(ch1-100) / Lv3(全书)
> **前置条件**：TXT 文件已就位

---

## 🔧 数据提取前置命令（硬性！先执行再写产出）

执行以下脚本提取原文结构化数据。提取结果写入 `_temp/` 作为本 Phase 唯一数据来源。

```bash
python "..\_scripts\extract.py" all "{$TXT_FILE_PATH}" ".\_temp\"
```

产出三个 JSON：
| 文件 | 字段 | 
|:-----|:-----|
| `_temp/baseline-data.json` | characters[] / places[] / levels[] / ages[] / monsters[] / events[] |
| `_temp/chapter-index.json` | 逐章 title / charCount / firstSentence / tags |
| `_temp/world-data.json` | deity / magic / class / species / faction / item / geography 逐章条目 |

---

## 速查表

| 步骤 | 操作 | 读什么 | 产出 |
|:-----|:-----|:-------|:-----|
| 1 | 跑 extract.py all | TXT 原文 | `_temp/` 三个 JSON |
| 2 | 提取角色卡 | JSON + 逐章精读原文 | 状态/角色/{主角}-角色卡-Lv4.md、配角卡、龙套池 |
| 3 | 提取逐章事实骨架 | JSON + 逐章原文 | `写作资产/事实骨架/ch001-050-事实骨架.md`（Lv2/Lv3） |
| 4 | 落盘检查 | — | 所有产出文件确存 |

---

## 产出结构

```
项目根/
├── _temp/
│   ├── baseline-data.json      ← extract.py
│   ├── chapter-index.json      ← extract.py
│   └── world-data.json         ← extract.py
├── 状态/角色/
│   ├── {主角}-角色卡-Lv4.md     ← 从 JSON 提取，逐条标注 @chXX
│   ├── {配角}-角色卡-Lv3.md     ← 主要配角
│   └── 龙套池.md                ← 所有命名角色清单
├── 写作资产/事实骨架/
│   └── ch001-050-事实骨架.md    ← Lv2/Lv3：逐章事件链+角色状态变化（每章5-8个事件）
└── _参考书/{书名}/Phase1-事实提取摘要.md
```

---

## ❌ 质量红线

| # | 标准 |
|:-:|:-----|
| ❌1 | **ETL 脚本已执行** — `\_temp/` 下三个 JSON 必须存在。未跑脚本=不准写 |
| ❌2 | **不准凭空编造** — 每个硬数据（年龄/等级/职业/地名）必须能从 JSON 中找到。找不到=留空标注"原文未显式说明" |
| ❌3 | **推断必须标注** — 任何来自间接证据而非显式声明的数据，标注「推断」 |
| ❌4 | **chXX 标注完整** — 角色卡中每个事实字段必须标注原文章节 |
| ❌5 | **不产出故事引擎** — Phase 1 不做任何"全书是什么"的归纳。只提取事实 |

---

## 原文验证写前自查

```
1. 写角色卡前 → baseline-data.json#characters[] / ages[] 确认角色名和年龄
2. 写等级/职业 → world-data.json#class.entries[] 确认等级路径
3. 写地名 → baseline-data.json#places[] / world-data.json#geography.entries[] 确认
4. 找不到 → 标注"（前 N 章未显露）"或"（原文未显式说明，推断约X）"
```

---

## 落盘检查点

| Lv | 文件 | 状态 |
|:---|:-----|:-----|
| Lv1 | `_temp/baseline-data.json` | [ ] |
| Lv1 | `_temp/chapter-index.json` | [ ] |
| Lv1 | `_temp/world-data.json` | [ ] |
| Lv1 | `状态/角色/{主角}-角色卡-Lv4.md` | [ ] |
| Lv1 | `状态/角色/{配角}-角色卡-Lv3.md` | [ ] |
| Lv1 | `状态/角色/龙套池.md` | [ ] |
| Lv1 | `_参考书/{书名}/Phase1-事实提取摘要.md` | [ ] |
| Lv2 | `写作资产/事实骨架/ch001-050-事实骨架.md` | [ ] |
| Lv3 | `写作资产/事实骨架/ch051-100-事实骨架.md` + … | [ ] |

---

## 下一步

Lv1 完成 → 止步开书，或进入 Phase 2（聚类卷幕）
Lv2/Lv3 完成 → 进入 Phase 2（聚类卷幕边界 + Canvas 反推）
