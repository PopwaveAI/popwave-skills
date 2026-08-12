# 管线上下文 — pop-decon-plot

## 拆书体系概览

```
拆书专家 pop-decon（入口）
    ├── Step 0 下载txt（tool-download-webnovel）
    ├── Step 1 章节白描（pop-decon-design-pack，统一底层资产）
    ├── Step 2 征询拆解维度（★强制·多选）
    └── Step 3 按需路由到被选中的维度skill
         ├── pop-decon-plot      剧情线 ★
         ├── pop-decon-romance   情感线
         ├── pop-decon-character 人物角色
         ├── pop-decon-power     力量体系
         ├── pop-decon-world     世界观
         ├── pop-decon-beat      爽点体验
         ├── pop-decon-style     文风
         └── pop-decon-prd       立项设计（消费各维度产出）
```

## 本 skill 在体系中的位置

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必） | pop-decon-design-pack | 故事机制DNA + 主线/支线/暗线 + 卷纲 | pop-decon-character、pop-decon-beat、pop-decon-prd |

## 铁律

- 前置：必须先有章节白描
- 卷纲必须从故事机制DNA逆向归纳，不得跳过
- 产出沉淀到 `项目本地/设计/`，不入库 pop-trope-library