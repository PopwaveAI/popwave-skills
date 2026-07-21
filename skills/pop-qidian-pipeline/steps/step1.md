# step1 · 初始化项目目录

> 本文件是 pop-qidian-pipeline 第一步执行指令。

## 目标

创建标准化项目目录结构 + project-state.md + project-state.html，为后续Phase路由做好准备。

## 执行

### 1. 创建目录结构

```text
{项目名}/
├── project-state.md
├── README.md
├── 素材/
│   └── downloads/
├── 设计/
│   ├── 全书设定/
│   ├── 角色库/
│   └── 第一卷剧情/
├── 正文/
└── 审核/
```

### 2. 生成 project-state.md

按 SKILL.md 中的 project-state.md 模板生成，初始值：
- phase: init
- current_chapter: ch000
- 所有就绪状态：❌
- 所有阶段完成情况：未勾选

### 3. 生成 project-state.html（如有脚本）

```powershell
python skills/pop-qidian-pipeline/scripts/generate-state-html.py {项目目录}/project-state.md
```

> 如脚本不存在，跳过HTML生成，仅落盘state.md。

### 4. 生成 README.md

简述项目信息 + 管线说明 + 目录结构说明。

## 质量门

- 四个一级文件夹（素材/设计/正文/审核）已创建
- 设计/ 下三个子文件夹（全书设定/角色库/第一卷剧情）已创建
- project-state.md 已落盘，phase=init
- README.md 已落盘

## 下一步

初始化完成 → 进入 Phase 0 Stage 1 用户意图深问。

加载：`steps/step2.md`
