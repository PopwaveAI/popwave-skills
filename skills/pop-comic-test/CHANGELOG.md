## v1.4.2 | 2026-09-21

**脚本与跨包路径改按包根解析。**

把脚本调用与跨包引用的写法从「发布源相对路径」改为「本包根相对路径」。本包根就是运行时系统提示里 `--- skill: /pop-comic-test (<包根>) ---` 括号内的路径，命令行等价于 `--skill`，逐台机器不同。原来写的 `scripts/x.py`、`../pop-visual-shared/scripts/x.py`、`skills/pop-xxx/...` 在用户机器上解析不到，模型只能全盘搜脚本。

改动：SKILL.md 增「脚本调用约定」段；跨包引用改为 `<包名 包根>` 形式；本包脚本调用补 `<包根>` 前缀。无脚本逻辑变更。

## v1.4.1 | 2026-09-20

改 description：补触发条件、删内部实现说明（原 52 字 → 72 字）。不涉及规程与产出变更。

# CHANGELOG

## v1.4.0 | 2026-09-13

### 新增 `prd/` 骨架（设计档案）

`pop-shared-skill-create` v9.0.0 把 `prd/`（设计预期／解决思路／进度／后续方向）立为 skill 标配，本 skill 先落两份骨架：`prd/PRD.md`、`prd/进度与待探索.md`。

**内容状态**：设计预期、解决思路、边界、关键取舍四节标「待补（2026-09-13）」，等下一次改到这个 skill 时填实。**不编设计预期**——编出来的比没有更坏，下一轮会拿它当依据。

## v1.3.0 | 2026-08-31

### 去AI味
- 引语身份词「画风三组测试引擎」改为「画风三组测试」
- 同步 skill.json（version）

---

## v1.2.0 — 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v1.2.0。

## v1.1.0 — 2026-08-05

### 生图改走 image_generate 工具，移除内置 API Key

老板要求所有 skill 生图环节改用 `image_generate` 工具，清理硬编码 API Key（Pinterest 搜索保持不动）：

- `SKILL.md` Step 3：由「批量生成」改为「`batch_test.py` 导出 `generation_tasks.json` + `image_generate` 工具逐条生成」
- 版本同步：SKILL.md / skill.json 至 v1.1.0

## v1.0.0 — 2026-08-04

### 新增：画风三组测试引擎

把「三组画风测试」沉淀为独立 skill，对画风库做逐画风内容形态验证：

- 三组固定模板（控制变量）：T1场景向 / T2角色立绘向 / T3多格剧情向
- 非画风部分（构图/光影/场景/角色）永久固定统一，只有 DNA+constraint 随画风变化
- `scripts/build_3test.py`：从 DNA 库批量生成三组 config，支持单画风（`--style-name`）与全库（`--all`）
- 复用 `pop-visual-shared/scripts/batch_test.py` 并发批量生成 + 自动 PE 日志
- 产出"画风通过判定表"：T1/T2/T3 各过/不过 + 偏科项标注
- 试点验证：双城之战三组全过（T1 85% / T2 100% / T3 95%），确认画风在三种内容形态下稳定执行