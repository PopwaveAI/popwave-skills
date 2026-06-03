# novel-agent-pro · 初始化健壮性与硬编码全量评估报告

> 扫描日期：2026-05-26  
> 扫描范围：`e:/AI小说/_工具配置/novel-agent-pro/` — 52 个 .py 文件  
> 覆盖：硬编码路径 / 项目初始化工件 / 路径归属策略

---

## 一、硬编码路径全量清单（57 处，涉及 17 个文件）

### 严重度分级

| 级别 | 数量 | 定义 |
|:----|:----:|:-----|
| 🔴 **P0 断裂级** | 4 | 写在代码逻辑中，非注释，非 --help 示例。新项目必崩 |
| 🟠 **P1 风险级** | 9 | 默认值/fallback/注释中的项目依赖。有触发条件时才崩 |
| 🟡 **P2 污染级** | 44 | --help 示例/文档注释/测试数据。不影响运行但误导 |

---

### 🔴 P0 — 写在代码逻辑中的硬编码

| # | 文件 | 行 | 代码 | 风险 |
|:-:|:----|:--|:----|:----|
| 1 | `scripts/updater.py:170` | SQL WHERE | `"name LIKE '%诡异游戏%'"` | 新项目sqlite选不到book_id→写错表 |
| 2 | `scripts/main.py:234` | 回退路径 | `os.path.join(project_root, "..", "海贼法典", "_chapters")` | 新项目无此目录但回退失败时无害，但说明旧项目残留 |
| 3 | `glue/post_write.py:90` | 硬编码目录 | `os.path.join("03-正文", ...)`——首参不是 project_root | 函数不知道 project_root→写到错误目录 |
| 4 | `scripts/update_global_summary.py:17` | 默认值 | `--project-dir` 默认硬编码诡异游戏项目 | 不传参数直接崩 |

### 🟠 P1 — 默认值/fallback 中的硬编码

| # | 文件 | 行 | 内容 | 触发条件 |
|:-:|:----|:--|:----|:--------|
| 5 | `scripts/loader.py:11` | 示例 | `EntityLoader("E:/AI小说/诡异人生v2")` | 复制粘贴时 |
| 6 | `scripts/updater.py:11` | 示例 | `EntityUpdater("E:/AI小说/诡异人生v2")` | 同上 |
| 7 | `scripts/main.py:6-9` | 注释 | `--project E:/AI小说/海贼法典v3` | 看注释 |
| 8-9 | `scripts/project_init_check.py:11` | help | `"E:\AI小说\这诡异游戏也太真实了"` | 复制help命令时 |
| 10-11 | `scripts/update_project_status.py:6` | help | `"e:/AI小说/这个诡异游戏太真实了 V2"` | 同上 |
| 12 | `skills/_shared/html-renderer/renderer.py:35` | 默认fallback | `"title": "海贼法典"` | 无配置时 |
| 13 | `glue/pre_flight.py:94` | usage示例 | `'E:\\AI小说\\诡异游戏v2' 8` | 抄用法时 |

### 🟡 P2 — help/注释中的硬编码

44 处分布在 `regression_test.py`、`鬼游戏_integration.py`、`batch_merger.py`、`project_config.py` 等文件的 --help 文本和文档注释中。**不影响运行但给新用户埋坑。**

---

## 二、项目初始化缺失扫描

### 2.1 现有初始化检查（pre_flight.py）

```
✔ project.yaml 存在并合法
✔ global-summary.md 存在
✔ character-state-anchor.md 存在
✔ 上一章正文存在（ch001 跳过）
✔ v3.db 存在（check_v3db_exists）
✔ reader_profile 合法（platform + gender）
✔ constitution.yaml 存在
```

**整体过弱**——更多是"文件存在性"检查，没有"结构合法性"检查。

### 2.2 缺失的关键初始化检查

| 检查项 | 当前状态 | 后果 |
|:------|:--------|:-----|
| **project.yaml schema 验证** | ❌ | 缺 reader_profile/paths 任何键 → ESM 报没有意义的错误 |
| **v3.db 表结构验证** | ❌ | 表建了但缺字段（skills.category, items.brief 等）→ 运行时报错 |
| **锚定章目录** | ❌ | `01-写作资产/锚定章库/` 不存在 → _load_anchor_chapter 静默失败 |
| **01-事实骨架/ 目录** | ❌ | 骨架文件写入前不检查目录 |
| **01-写作资产/ 目录** | ❌ | bundle/QC/Director 文件写入前不检查 |
| **02-幕纲/act-XX.yaml 内容验证** | ❌ | 文件存在就行，不检查 chapters 字段格式 |
| **经验日志文件** | ❌ | `01-写作资产/experience-log.md` 不存在 → _read_experience_log 静默返回空 |
| **全局摘要格式** | ❌ | 只检查存在性，不检查是否包含章节进度表 |
| **pipeline_config.yaml 自身验证** | ❌ | pipeline_config.yaml 缺失字段（project_path）→ 跑管线直接崩 |
| **ESM scripts 目录在 sys.path 中** | ❌ | 从 pipeline 调 ESM before/after 时依赖 __pycache__ 缓存 |

### 2.3 后果链

拿一个新项目举例：

```
新建项目 → 没有 setting-index.yaml
         → 没有 reader_profile（但管线不检查）
         → 没有锚定章库 → _load_anchor_chapter 静默失败
         → 没有经验日志 → _read_experience_log 静默返回空  
         → ESM before 不报错 → bundle 缺少多个区块
         → Pass2 写正文时不知道角色锚定和诡异性格
```

**管线不报错、不警告、不觉察——假装一切正常。**

---

## 三、路径归属策略：skill 侧 vs 项目侧

### 3.1 当前分布（根因分析）

```
NOVEL_AGENT_ROOT/
├── glue/                          ← 项目侧路径解析层（正确）
│   └── project_config.py          ← 通过 project.yaml paths 解耦
├── automation/
│   └── pipeline_orchestrator.py   ← pipeline_config.yaml 中注入 project_path
├── skills/
│   ├── skill-emergent-writer/
│   │   └── scripts/main.py        ← hardcoded "海贼法典" + "诡异人生"（错误）
│   │   └── updater.py             ← hardcoded "诡异游戏%"（错误）
│   │   └── loader.py              ← hardcoded "我的诡异人生v2"（错误）
│   ├── _shared/html-renderer/
│   │   └── renderer.py            ← hardcoded "海贼法典"（错误）
│   └── _shared/pop/
│       └── dispatcher.py          ← hardcoded "诡异游戏v2"（错误）
```

**当前现状：glue层做得对，skill层做得错。**

`project_config.py` 已经是一个正确的设计——通过 `project.yaml paths` 段来解耦项目目录结构差异。但**skill 层的脚本没有使用它**，而是自己写死了路径。

### 3.2 正确的路径归属原则

```
┌─────────────────────────────────────────────┐
│  不变的部分 → 放在 skill 侧                  │
├─────────────────────────────────────────────┤
│  - prompt 模板                              │
│  - 验证规则/正则                             │
│  - K1-K4 知识库                             │
│  - ESM 逻辑（实体加载/更新）                    │
│  - 输出文件格式规范                            │
│  - DB schema（每张表的结构定义）                │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  变的部分 → 放在项目侧                        │
├─────────────────────────────────────────────┤
│  - project.yaml paths（所有文件路径定义）        │
│  - target_platform（番茄/起点）                │
│  - reader_profile（读者画像）                  │
│  - 参考书列表                                 │
│  - pipeline_config.yaml（章节数/模式开关）      │
│  - 设定文件内容（setting-index.yaml）           │
│  - 锚定章库内容                                │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  桥接模式 → resolve_path(project_dir, key)   │
├─────────────────────────────────────────────┤
│  script 从不自己拼路径                         │
│  它问 glue.project_config: "prd 在哪？"       │
│  project_config 查 project.yaml paths 回答   │
│  script 拿到绝对路径，读写                     │
└─────────────────────────────────────────────┘
```

### 3.3 具体应该怎么做

**所有 skill 脚本**需要做到这条规范：

```python
# ❌ 当前做法（硬编码）
gs_path = os.path.join(project_root, "02-幕纲", "global-summary.md")

# ✅ 正确做法（通过 glue 桥接）
from glue.project_config import resolve_path
gs_path = resolve_path(project_root, "global_summary")
```

这样项目侧可以自由定义目录结构，skill 侧不用改。

---

## 四、修复方案

按修复难度从低到高排列：

### Phase 0 — 注释层清理（10min，零风险）

清理所有 --help 和文档中的项目名示例，改为占位符 `{project_dir}`。

**涉及**: 6 个文件（`regression_test.py`, `project_init_check.py`, `update_global_summary.py`, `update_project_status.py`, `pre_flight.py`, `orchestrate.py`）

```python
# 当前
parser.add_argument("--project", default="e:/AI小说/_小说项目/我的诡异游戏v3")

# 改为
parser.add_argument("--project", required=True, help="项目根目录（包含 project.yaml）")
```

### Phase 1 — P0 断裂级修复（30min）

| Gap | 修复方式 |
|:----|:--------|
| `updater.py:170` `"name LIKE '%诡异游戏%'"` | 改为 `" WHERE id=1 OR name LIKE ?"` + 从 project.yaml 读取项目名 |
| `post_write.py:90` 硬编码 `"03-正文"` | project_root 通过参数传入，改为 `os.path.join(project_root, "03-正文", ...)` |
| `update_global_summary.py:17` 硬编码默认值 | `--project-dir` 改为 required=True |

### Phase 2 — 全量 migrate 到 resolve_path（60min）

将所有 skill 脚本中的 `os.path.join(project_root, "01-写作资产")` 类调用改为 `resolve_path(project_root, "writing_assets")`。

这样以后任何项目想改目录结构（例如"不用 03-正文/ 而用 chapters/"），改 project.yaml paths 即可。

### Phase 3 — 初始化检查增强（45min）

在 `pre_flight.py` 中新增 6 项检查：

```python
checks = {
    "v3_db_schema":         check_db_tables(db_path, EXPECTED_TABLES),
    "锚定章库":               check_dir_exists(project_root, "01-写作资产/锚定章库"),
    "事实骨架目录":            check_dir_exists(project_root, "01-事实骨架"),
    "写作资产目录":            check_dir_exists(project_root, "01-写作资产"),
    "经验日志文件":            check_file_exists(project_root, "01-写作资产/experience-log.md"),
    "pipeline_config":      check_file_exists(NOVEL_AGENT_ROOT, "automation/pipeline_config.yaml"),
}
# 任何一个失败 → 打印警告但不断流
# 3个以上失败 → 打印严重警告并建议初始化
```

### Phase 4 — 新增"project init"命令（60min）

新建 `automation/init_project.py`，取代当前需要手动创建的文件：

```bash
python automation/init_project.py --project "e:/AI小说/我的新项目"
# 自动创建:
#   - project.yaml（含 reader_profile 占位 + paths 标准配置）
#   - 00-原始设定/L1-元设定层/（目录）
#   - 01-事实骨架/（目录）
#   - 01-写作资产/锚定章库/（目录）
#   - 01-写作资产/experience-log.md（空模板）
#   - 02-幕纲/（目录）
#   - 02-章纲/global-summary.md（空模板）
#   - 03-正文/（目录）
#   - 04-数据库/（目录 + v3.db 带表结构）
#   - constitution.yaml（空模板）
#   - setting-index.yaml（空模板）
#   - .pipeline/checkpoints/（目录）
#   - pipeline_config.yaml（模板，16 个占位符）
```

### 修复工作量总览

| Phase | 文件数 | 改动行数 | 风险 | 效果 |
|:------|:------|:--------|:----|:-----|
| P0 注释清理 | 6 | ~20 | 零 | 新用户不会抄到错的命令 |
| P1 P0断裂 | 3 | ~10 | 低 | 新项目跑管线不会崩 |
| P2 resolve_path | 8 | ~30 | 中 | 路径全解耦，改目录只需改 project.yaml |
| P3 初始化检查 | 1 | ~40 | 低 | 初始化不全会被告知 |
| P4 init 命令 | 1(新建) | ~80 | 低 | 1条命令建好所有前置文件 |

---

## 五、一句话结论

> **novel-agent-pro 的 glue 层设计是正确的（通过 project.yaml paths 桥接），但 skill 层的 17 个文件从未使用这套设计——57 处硬编码路径让任何"在新项目上跑管线"都是一个赌局。**

修复路径很清晰：先用 glue 层的 `resolve_path` 替换所有 skill 脚本中的 `os.path.join(project_root, "硬编码目录")`，再补全初始化检查。不需要架构重做。
