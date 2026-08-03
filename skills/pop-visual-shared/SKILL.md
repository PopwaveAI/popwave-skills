---
name: pop-visual-shared
description: "视觉 skill 群的共享底层资产层。不直接生成图片，而是提供被 cover / oc / style / comic 等视觉 skill 复用的统一组件：Seedream 生成脚本、Pinterest 参考搜索脚本、统一提示词指南、画风DNA库引用协议。消除多 skill 间的重复维护与版本分化。"
---

# pop-visual-shared

> 视觉 skill 群的**共享底层资产层**。v1.3.0。本 skill 不独立落地运行，而是被其他视觉 skill 以"引用共享组件"方式调用，保证全链路视觉产出使用同一套脚本与提示词标准。

## 这个 Skill 做什么

把散落在 cover / oc / style / comic 中**重复、分化、过时**的底层资产收敛到一处，作为唯一权威源：

- `scripts/generate.py`：Seedream 图片生成脚本（原 4 份字节相同副本去重）
- `scripts/batch_test.py`：**固定画风测试脚本**（固定测试素材+固定6段式模板+并发批量+自动PE日志，画风测试唯一标准入口；v1.2.0 支持画风×项目角色联合测试 `--character` + `--character-image`）
- `scripts/pinterest_search.py`：Pinterest 参考图搜索脚本（原 3 份字节相同副本去重）
- `references/seedream-prompt-guide.md`：统一提示词指南（合并 6 段式 + V3 + 高精度 4 块 + Seedance，消除 4 份分化副本）
- 画风 DNA 库引用协议：`style-dna-library.json` 与 `lighting-composition-templates.md` 仍归属 `pop-visual-style`（其域资产），本 skill 定义跨 skill 引用协议

## 共享组件清单

| 组件 | 路径 | 归属 |
|:-----|:-----|:-----|
| Seedream 生成脚本 | `scripts/generate.py` | 本 skill（共享） |
| **固定画风测试脚本** | `scripts/batch_test.py` | 本 skill（共享） |
| Pinterest 参考搜索脚本 | `scripts/pinterest_search.py` | 本 skill（共享） |
| 统一提示词指南 | `references/seedream-prompt-guide.md` | 本 skill（共享） |
| 画风 DNA 库 | `pop-visual-style/references/style-dna-library.json` | pop-visual-style（域资产） |
| 构图/光影模板库 | `pop-visual-style/references/lighting-composition-templates.md` | pop-visual-style（域资产） |

## 引用方式（跨 skill 协议）

其他视觉 skill 需要共享组件时，**禁止复制文件到本地**，统一引用本 skill 路径：

```
生成脚本：   skills/pop-visual-shared/scripts/generate.py
固定测试脚本：skills/pop-visual-shared/scripts/batch_test.py
搜索脚本：   skills/pop-visual-shared/scripts/pinterest_search.py
提示词指南： skills/pop-visual-shared/references/seedream-prompt-guide.md
```

调用时按实际 skills 根目录解析上述相对路径。需要画风 DNA 时，读取 `pop-visual-style/references/style-dna-library.json`。

## 核心约束（红线）

1. **禁止复制共享组件到本地 skill**。任何视觉 skill 需要 generate.py / pinterest_search.py / seedream-prompt-guide.md 时，必须引用本 skill 路径，不得在本地重建副本（重建即回退到重复分化）。
2. **提示词指南以本文件为唯一权威源**。`seedream-prompt-guide.md` 的分化副本已在 cover/oc/style 中删除，任何 skill 不得再各自维护一份。
3. **本 skill 不落地生成**。它只被引用，不发起图片生成，不承载业务逻辑。
4. **画风 DNA 归属不迁移**。`style-dna-library.json` 是 pop-visual-style 的域资产，本 skill 只定义引用协议，不复制内容。