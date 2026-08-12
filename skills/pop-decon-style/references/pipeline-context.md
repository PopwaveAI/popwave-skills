# 管线上下文 — pop-decon-style

## 拆书体系概览

```
拆书专家 pop-decon（入口）
    ├── Step 0 下载txt（tool-download-webnovel）
    ├── Step 1 章节白描（pop-decon-design-pack，统一底层资产）
    ├── Step 2 征询拆解维度（★强制·多选）
    └── Step 3 按需路由到被选中的维度skill
         ├── pop-decon-plot      剧情线
         ├── pop-decon-romance   情感线
         ├── pop-decon-character 人物角色
         ├── pop-decon-power     力量体系
         ├── pop-decon-world     世界观
         ├── pop-decon-beat      爽点体验
         ├── pop-decon-style     文风 ★
         └── pop-decon-prd       立项设计（消费各维度产出）
```

## 本 skill 在体系中的位置

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必）+ 原文采样 | pop-decon-design-pack / `_temp/chapters/` | 文风采样 + 文风DNA档案 + 对白风格 | pop-decon-prd |

## 铁律

- 前置：必须先有章节白描，且原文采样前必须验证原文存在
- 文风DNA必须基于≥500字原文引用，不得凭空描述
- 只摘笔触层（句法/叙事距离/感官序列/信息释放），丢弃世界观专属要素
- 产出沉淀到 `项目本地/设计/`，不入库 pop-trope-library