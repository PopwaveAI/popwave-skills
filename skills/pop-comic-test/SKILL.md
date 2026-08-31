---
name: pop-comic-test
description: "当用户说'测画风/画风测试/三组测试/画风能不能用'时启用。对 文风DNA-library 的画风做三组固定内容测试（场景/角色/多格剧情），逐画风验证 DNA 是否被 Seedream 稳定执行，产出通过判定表。"
---

# pop-comic-test

> 画风三组测试。用固定三组模板（场景/角色/多格剧情）逐画风验证 DNA 执行力，产出"画风能不能用"的通过判定。v1.3.0

## 这个 Skill 做什么

对 `pop-visual-style` 的画风 DNA 库做**三组内容形态测试**，验证画风 DNA 在不同内容下是否稳定执行：

- **T1 场景向**：环境为主，验证画风能否撑起全景/氛围
- **T2 角色立绘向**：角色为主，验证画风能否撑起角色/主观特征
- **T3 多格剧情向**：一页多格，验证画风能否撑起最终漫画产物

**核心价值**：一个画风光"适合场景"不够，必须能在角色、分格剧情里也成立，才算真正可用。三组全过 = 画风稳定；部分过 = 画风有偏科，需标记偏科项。

**边界**：本 skill 只做**测试与判定**，不生产最终交付图。画风库维护归 `pop-visual-style`，生成脚本归 `pop-visual-shared`。

## 怎么运作

### Step 1: 选画风范围 → 读 DNA 库
- 读取 `../pop-visual-style/references/文风DNA-library.json` 的 `styles` 键
- 支持单画风（`--style-name`）或全库（`--all`）
- 每次取该画风的 `dna` + `constraint` 字段注入三组模板

### Step 2: 生成三组 config → `scripts/build_3test.py`
- 用固定三组模板（非画风部分统一中性，不含画风色彩）生成 config
- **控制变量铁律**：三组模板的 composition/lighting/scene/character 全部固定，只有 DNA+constraint 随画风变化
- 输出 config JSON 供 `batch_test.py` 消费

### Step 3: 批量生成 → `../pop-visual-shared/scripts/batch_test.py`
- 用 `--config` 指定生成的 config，`--out-dir` 指定输出，`--seed` 固定种子
- `batch_test.py` 导出三张图的任务清单（T1_scene / T2_character / T3_comic）到 `generation_tasks.json`
- 主 agent 读任务清单，用 `image_generate` 工具逐条生成（生图统一走 `image_generate`，不直连 API）
- 自动落盘 `pe-log.json`

### Step 4: 判定 + 汇总 → 结果表
- 逐画风检查三张图：画风特征是否被稳定执行
- 输出"画风通过判定表"：T1/T2/T3 各过/不过 + 偏科项标注
- 不过的画风 → 标记并回媒体库（交给 `pop-visual-style` 微调 DNA）

## ❌ 质量红线

| # | 红线 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **必须走固定脚本** — 禁止现场手写提示词或临时改三组模板，必须用 `build_3test.py` 生成 config | 变量不隔离，测试不可比 |
| ❌2 | **控制变量** — 三组模板的非画风部分（构图/光影/场景/角色）永久固定，禁止掺入画风特征 | 无法判断是画风还是模板问题 |
| ❌3 | **三组全测** — 每个画风必须跑 T1/T2/T3 三组，禁止只测一组 | 画风偏科被漏检 |
| ❌4 | **固定种子** — 用 `--seed` 固定，保证可复现对比 | 无法复现，结果不可信 |

## 速查表

| 我要 | 读/执行什么 | 什么时候用 |
|:-----|:----------|:---------|
| 生成三组 config | `scripts/build_3test.py --style-name "X" --out config.json` | Step 2 |
| 全库批量生成 config | `scripts/build_3test.py --all --out-dir 素材/测试` | Step 2 全库模式 |
| 读画风 DNA 库 | `../pop-visual-style/references/文风DNA-library.json` | Step 1 |
| 批量生成图片 | `../pop-visual-shared/scripts/batch_test.py --config ...` | Step 3 |
| 三组固定模板定义 | `scripts/build_3test.py` 内 `TEMPLATES` 常量 | Step 2 |
| 画风库变更历史 | `../pop-visual-style/CHANGELOG.md` | 画风库更新后 |

## 版本

见 `CHANGELOG.md`。画风库变更历史见 `../pop-visual-style/CHANGELOG.md`。