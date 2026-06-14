# pop-decon 拆分计划

## 目标
将一包五步的 `pop-decon` 拆为 1 个 orchestrator + 5 个 domain sub-skill。

## 新结构

```
skills/
├── pop-decon/                          ← 保留，改为 orchestrator（~80行）
│   ├── SKILL.md                        ← 路由逻辑（Lv1→extract, Lv2→extract+cluster+world, Lv3→+engine+validate）
│   ├── skill.json                      ← id: pop-decon, pipeline { expert: "expert-writer" }
│   ├── CHANGELOG.md
│   └── scripts/extract.py             ← ETL 脚本（被 pop-decon-extract 消费）
│
├── pop-decon-extract/                  ← Phase 1: 事实提取
│   ├── SKILL.md                        ← 4 步：ETL → 角色卡 → 事实骨架 → 摘要
│   ├── steps/step-1-etl.md, step-2-characters.md, step-3-skeleton.md, step-4-summary.md
│   ├── templates/character-lv3.tpl.md, character-lv4.tpl.md, dragon-pool.tpl.md
│   └── references/pipeline-context.md  ← Phase 1 在管线中的位置
│
├── pop-decon-cluster/                  ← Phase 2: 聚类卷幕
│   ├── SKILL.md                        ← 4 步：卷边界→幕边界→剧情线→契诃夫枪
│   ├── steps/step-1-volume.md, step-2-act.md, step-3-plotlines.md, step-4-chekhov.md
│   ├── templates/volume-design.tpl.md, act-skeleton.tpl.yaml, chekhov-tracker.tpl.yaml, book-arch.tpl.md, starting-snapshot.tpl.md
│   └── references/
│
├── pop-decon-world/                    ← Phase 3: 归纳世界观
│   ├── SKILL.md                        ← 9 步：L1六件套→宪法→数值→快照
│   ├── steps/step-{1..9}.md
│   ├── templates/L1-01~06.tpl.md, combat-capability.tpl.yaml, constitution.tpl.md
│   └── references/
│
├── pop-decon-engine/                   ← Phase 4: 归纳故事引擎（仅 Lv3）
│   ├── SKILL.md                        ← 5 步：核心假说→卖点→宪法→开篇→结构
│   ├── steps/step-{1..5}.md
│   └── templates/story-engine.tpl.md
│
└── pop-decon-validate/                 ← Phase 5: 验证打包
    ├── SKILL.md                        ← 3 步：可回源性审计→一致性→索引
    └── steps/step-{1..3}.md
```

## 模板归属

| 当前模板 | 去哪个 skill | 备注 |
|:---------|:------------|:-----|
| character-lv3.tpl.md | pop-decon-extract | 角色卡是事实提取的产出 |
| character-lv4.tpl.md | pop-decon-extract | 同上 |
| volume-design.tpl.md | pop-decon-cluster | 卷设计是卷幕聚类的产出 |
| act-skeleton.tpl.yaml | pop-decon-cluster | 幕骨架 |
| starting-snapshot.tpl.md | pop-decon-cluster | 快照 |
| L1-01~06.tpl.md | pop-decon-world | L1 六件套 |
| combat-capability.tpl.yaml | pop-decon-world | 战力数值 |
| story-engine.tpl.md | pop-decon-engine | 故事引擎 |
| design-pack.tpl.md | pop-decon-cluster | 设计包（plot 消费格式） |

## 施工顺序

1. 创建 5 个 sub-skill 目录 + 文件
2. 从 `pop-decon/steps/` 分拆内容到各 sub-skill
3. 从 `pop-decon/templates/` 分拆模板到各 sub-skill
4. 重写 `pop-decon/SKILL.md` 为 orchestrator（~80行）
5. 清理 `pop-decon/` 中不再属于它的文件
6. npm run skills:validate

## 不做的事
- 不重写 extract.py（共享脚本不动）
- 不合并 Lv1/Lv2/Lv3 的逻辑（保持原有三级分级）
