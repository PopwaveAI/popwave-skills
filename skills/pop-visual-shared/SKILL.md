# pop-visual-shared

> **脚本调用约定**：本包脚本都在**本包根目录**下的 `scripts/`。本包根目录 = 本 skill 的 SKILL.md 所在目录，即你读取本 SKILL.md 时那个绝对路径的父目录（系统提示 `<available_skills>` 里该 skill 的 `<location>` 也是它），命令行等价于 `--skill` 的取值，逐台机器不同。所以调用一律写成 `python "<包根>\scripts\<脚本>" ...`：不要把 `scripts/...` 当成相对当前工作目录的路径，不要写绝对路径，也不要到磁盘上搜脚本。
>
> **跨包路径**：要用别的包的脚本或资源，用**那个包自己的包根**，写成 `<包名 包根>`，对端包根 = 该 skill 的 SKILL.md 所在目录，从其 `<location>` 或你读取它的绝对路径取父目录。不要写 `../其它包/...`，也不要写 `skills/<包名>/...`。
>
> **参数**：以脚本自身 `--help` 为准。脚本报错时会打印实际用法，照提示改一次即可，不要猜参数。

> 视觉 skill 群的**共享底层资产层**。v1.8.1。本 skill 不独立运行，而是被其他视觉 skill 以"引用共享组件"的方式调用。**生图不直连 API、不内置任何 API Key**，统一由脚本导出 `generation_tasks.json`，再由主 agent 用 `image_generate` 工具逐条生成。

## 职责范围

本 skill 把散落在 cover / oc / style / comic 中**重复、分化、过时**的底层资产收敛到一处，作为唯一权威源：

- `<包根>\scripts\generate.py`：生图任务导出脚本（image 子命令只导出任务，不直连 API；video 子命令需显式设置 `ARK_API_KEY`）
- `<包根>\scripts\batch_test.py`：**固定画风测试脚本**（默认使用小说次要视觉锚点素材，即 `--scene` 场景、`--side` 路人，和小说强相关但无关紧要，只验证画风；不传则兜底使用内置中性素材。固定6段式模板、导出任务清单、自动 PE 日志，是画风测试的唯一标准入口；v1.4 起 `--character`/`--character-image` 已废弃，主角形象归 art-bible、oc）
- `<包根>\scripts\pinterest_search.py`：Pinterest 参考图搜索脚本（原 3 份字节相同副本去重）
- `<包根>\scripts\watermark.py`：**品牌水印脚本**（在图片像素层直接写入，生图完成后叠加半透明 `popwave.cn`；作为工程化后处理，不进提示词，避免污染 Seedream 文生图；幂等）
- `references/seedream-prompt-guide.md`：统一提示词指南（合并 6 段式、V3、高精度 4 块、Seedance 四类内容，消除 4 份分化副本）
- 画风 DNA 库引用协议：`style-dna-library.json` 与 `lighting-composition-templates.md` 仍归属 `pop-visual-style`（其域资产），本 skill 定义跨 skill 引用协议

## 共享组件清单

| 组件 | 路径 | 归属 |
|:-----|:-----|:-----|
| 生图任务导出脚本 | `<包根>\scripts\generate.py` | 本 skill（共享） |
| **固定画风测试脚本** | `<包根>\scripts\batch_test.py` | 本 skill（共享） |
| Pinterest 参考搜索脚本 | `<包根>\scripts\pinterest_search.py` | 本 skill（共享） |
| **品牌水印脚本** | `<包根>\scripts\watermark.py` | 本 skill（共享） |
| 统一提示词指南 | `references/seedream-prompt-guide.md` | 本 skill（共享） |
| 画风 DNA 库 | `<pop-visual-style 包根>/references/style-dna-library.json` | pop-visual-style（域资产） |
| 构图/光影模板库 | `<pop-visual-style 包根>/references/lighting-composition-templates.md` | pop-visual-style（域资产） |

## 引用方式（跨 skill 协议）

其他视觉 skill 需要共享组件时，**禁止复制文件到本地**，统一引用本 skill 路径：

```
生成脚本：  <pop-visual-shared 包根>/scripts/generate.py
固定测试脚本：<pop-visual-shared 包根>/scripts/batch_test.py
搜索脚本：  <pop-visual-shared 包根>/scripts/pinterest_search.py
水印脚本：  <pop-visual-shared 包根>/scripts/watermark.py
提示词指南：<pop-visual-shared 包根>/references/seedream-prompt-guide.md
```

调用时按实际 skills 根目录解析上述相对路径。需要画风 DNA 时，读取 `<pop-visual-style 包根>/references/style-dna-library.json`。

## 生图协议（image_generate 工具）

**所有静态生图统一走 `image_generate` 工具，本 skill 脚本不直连生图 API、不内置任何 API Key。**

- `generate.py image` 与 `batch_test.py` 只负责解析提示词、校验尺寸、导出 `generation_tasks.json`（含每任务 id、prompt、size、ref_images、output_path）
- 主 agent 读取任务清单，对每条任务调用 `image_generate` 工具（有 ref_images 时传参考图路径），输出到任务 output_path
- 视频生成（Seedance）不在 `image_generate` 工具范围，走 `generate.py video`，需显式设置 `ARK_API_KEY` 环境变量（不内置 key）

## 核心约束（红线）

1. **禁止复制共享组件到本地 skill**。任何视觉 skill 需要 generate.py / pinterest_search.py / seedream-prompt-guide.md 时，必须引用本 skill 路径，不得在本地重建副本（重建即回退到重复分化）。
2. **提示词指南以本文件为唯一权威源**。`seedream-prompt-guide.md` 的分化副本已在 cover/oc/style 中删除，任何 skill 不得再各自维护一份。
3. **本 skill 不直接执行生成，也不内置生图 API Key**。它只被引用，脚本只导出任务清单，静态生图由主 agent 用 `image_generate` 工具完成。
4. **画风 DNA 归属不迁移**。`style-dna-library.json` 是 pop-visual-style 的域资产，本 skill 只定义引用协议，不复制内容。
