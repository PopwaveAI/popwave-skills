# 拆书管线上下文（方案B）

> 统一共享资产（canonical）。由 pop-decon 持有，所有拆书 skill（pop-decon-dimension / pop-decon-prd / pop-decon-design-pack）通过引用读取本文件理解管线位置。v1.0.0（方案B 重构后统一）

## 管线全景（方案B）

```
用户: "拆这本书"
    ↓
pop-decon (下载 → 征询维度 → 路由)
    ├── Step 0  下载txt（tool-download-webnovel）
    ├── Step 1  ★征询用户：要拆哪些维度？★（多选）
    ├── Step 2  按需路由到 pop-decon-dimension（传维度参数）
    ├── Step 3  pop-decon-dimension 直读原文产出各维度拆解
    └── Step 4  pop-decon-prd 消费各维度产出 → 全书立项设计
```

## 可选加速器

- `pop-decon-design-pack`：如需快速全书骨架/逐章白描，可作可选加速器（非必选前置）
- 方案B 默认直读原文，不产白描卡

## 产出归属

| 产出 | 归属 skill |
|:--|:--|
| 剧情线/卷纲/故事DNA | pop-decon-dimension(plot) |
| 情感线 | pop-decon-dimension(romance) |
| 人物/角色弧线/对白风格 | pop-decon-dimension(character) |
| 力量体系 | pop-decon-dimension(power) |
| 世界观/地理/势力 | pop-decon-dimension(world) |
| 爽点/名场面/读者体验 | pop-decon-dimension(beat) |
| 文风DNA | pop-decon-dimension(style) |
| 全书立项设计 | pop-decon-prd |

## 维护约定

- 本文件是唯一规范源，改动只改本文件
- 各 skill 的本地 `references/pipeline-context.md` 仅为指针桩，指向本文件，禁止各自维护内容
