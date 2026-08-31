# 拆书管线上下文（单书深度wiki拆解）

> 统一共享资产（canonical）。由 pop-decon 持有，通过引用读取理解管线位置。v26.0.0：家从 4 精简为 2，产出目标从维度证据稿升级为六模块深度wiki成品。

## 管线全景

```
用户: "拆这本书"
    ↓
pop-decon (下载 → 征询范围 → 路由)
    ├── Step 0  下载txt（tool-download-webnovel）
    ├── Step 1  ★征询范围★（全书/某一卷/前N章）
    └── Step 2  路由 pop-decon-dimension（单书深度wiki拆解）
                    ├── L1 批次拆解（联合Grep锚点池→~30章/批精读八维→批次档案，硬门禁）
                    └── L2 六模块成品整合（剧情库分卷/角色与势力库/力量与战斗/世界观/赛道特色/文风DNA + 爽点/立项/索引）
```

## 产出归属

| 产出 | 归属 |
|:--|:--|
| L1 批次档案（内部依托，硬门禁） | pop-decon-dimension |
| 剧情库（分卷叙事流+动力引擎） | pop-decon-dimension |
| 角色与势力库 | pop-decon-dimension |
| 力量与战斗 | pop-decon-dimension |
| 世界观 | pop-decon-dimension |
| 赛道特色 | pop-decon-dimension |
| 文风DNA | pop-decon-dimension |
| 爽点.md / 立项.md（消费六模块综合） | pop-decon-dimension（成品层） |

## 已删除 skill（方法论已内吸）

- **pop-decon-design-pack**：逐章白描卡 → 批次档案格式（`references/batch-format.md`，30章/批）
- **pop-decon-prd**：独立立项拆解 → 成品层 `立项.md`（`templates/立项.tpl.md`，消费六模块综合）

> 两个旧 skill 不再独立存在；其方法论分别吸收为 L1 批次档案格式与 L2 立项模板。

## 维护约定

- 本文件是唯一规范源，改动只改本文件
- 各 skill 的本地 `references/pipeline-context.md` 仅为指针桩，指向本文件，禁止各自维护内容