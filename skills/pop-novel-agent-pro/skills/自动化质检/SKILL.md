---
name: "自动化质检"
description: "自动化质检元技能——对任何Skill的执行过程和文件输出做结构化质量检测。支持步骤调度+审计追溯+LLM API验证+质量闸门拦截。用于测试所有skill的产出质量和管线纪律。当需要验证某个skill的输出是否达标时调用。"
---

# 自动化质检 Skill

这是一个**元技能（Meta-Skill）**——不直接创作内容，而是对其他 Skill 的执行过程和输出进行结构化质量检测。

**适用所有 skill。** 通过不同的 `PipelineConfig` 适配不同类型的输出和验证需求。

---

## 核心能力

| 能力 | 说明 |
|:----|:-----|
| **步骤调度** | 按 PipelineConfig 定义的步骤序列顺序执行，3种执行模式 |
| **审计追溯** | 每步生成结构化JSON审计记录：耗时/字数/验证结果/异常标记/文件访问 |
| **质量闸门** | 7种内置验证规则 + 可注册自定义规则 |
| **LLM 独立验证** | 调用外部API对步骤产出独立评分，与自评交叉比对 |
| **阻塞卡控** | 上一步有误时自动阻塞下一步，等待人工确认或超时处理 |

---

## 快速上手：5种典型skill的配置模板

### 1. 正文写作类 — emergent-writer / horror-game-writer / opening-arc

**产出**: `03-正文/chXXX.md` 小说章节 + QC报告  
**需验证**: 字数≥2000 / 违禁句式0 / 前300字有钩子 / 实体覆盖率

```jsonc
{
  "target_skill": "emergent-writer",
  "steps": [{
    "id": "ch001_render",
    "name": "第一章正文",
    "executor": { "type": "skill", "skill_name": "emergent-writer" },
    "validators": [
      { "type": "word_count", "min": 1800, "max": 3500, "severity": "error" },
      { "type": "regex_match", "pattern": "不是[^。，；]*而是", "must_match": false, "severity": "error" },
      { "type": "regex_match", "pattern": "说不清[^。，；]*(颜色|感觉|味道)", "must_match": false, "severity": "warn" },
      { "type": "entity_coverage", "required_entities": ["林深", "诡异APP", "玩家"], "min_coverage": 0.7, "severity": "error" }
    ],
    "llm_verify": { "enabled": true, "template_name": "chapter_review", "scoring_dimensions": ["前300字钩子", "情感弧线"], "pass_threshold": 0.6 }
  }]
}
```

### 2. 拆书/设定类 — book-deconstructor / project-bootstrap / plot-architecture

**产出**: .md分析报告 / .yaml配置文件 / 多文件目录  
**需验证**: 文件存在 / 文件大小 / 结构完整性 / yaml合法

```jsonc
{
  "target_skill": "book-deconstructor",
  "steps": [{
    "id": "modeA_structure",
    "name": "结构拆解产出",
    "executor": { "type": "command", "command": "cat output/modeA-report.md" },
    "validators": [
      { "type": "file_exists", "required_paths": ["output/modeA-report.md"], "severity": "error" },
      { "type": "file_size", "min_bytes": 1024, "severity": "error" },
      { "type": "regex_match", "pattern": "节奏地图|节拍序列", "must_match": true, "severity": "error" }
    ]
  }]
}
```

### 3. 调研/舆情类 — cnovel-research / book-opinion-tracker

**产出**: .md调研报告 / 爬虫数据文件 / 多平台结果汇总  
**需验证**: 至少N个平台有数据 / 报告完整性 / 关键字段存在

```jsonc
{
  "target_skill": "book-opinion-tracker",
  "steps": [{
    "id": "platform_report",
    "name": "舆情报告",
    "executor": { "type": "command", "command": "cat reports/opinion_report.md" },
    "validators": [
      { "type": "file_exists", "required_paths": ["reports/opinion_report.md"], "severity": "error" },
      { "type": "regex_match", "pattern": "## (豆瓣|微博|贴吧|知乎)", "must_match": true, "severity": "warn" },
      { "type": "word_count", "min": 500, "severity": "error" }
    ]
  }]
}
```

### 4. HTML渲染类 — html-renderer

**产出**: .html单文件  
**需验证**: 文件大小 / HTML结构完整 / 设计系统匹配

```jsonc
{
  "target_skill": "html-renderer",
  "steps": [{
    "id": "html_output",
    "name": "HTML渲染产出",
    "executor": { "type": "skill", "skill_name": "html-renderer" },
    "validators": [
      { "type": "file_exists", "required_paths": ["output/index.html"], "severity": "error" },
      { "type": "file_size", "min_bytes": 5120, "severity": "error" },
      { "type": "regex_match", "pattern": "<!DOCTYPE html>", "must_match": true, "severity": "error" },
      { "type": "regex_match", "pattern": "<html[^>]*>", "must_match": true, "severity": "error" }
    ],
    "llm_verify": { "enabled": true, "template_name": "content_review", "scoring_dimensions": ["视觉完整性", "响应式适配"] }
  }]
}
```

### 5. 网络采集类 — web-access

**产出**: 网页抓取内容（文件或stdout文本）  
**需验证**: 内容非空 / 有关键词命中 / 无报错信息

```jsonc
{
  "target_skill": "web-access",
  "steps": [{
    "id": "scrape_result",
    "name": "网页采集结果",
    "executor": { "type": "command", "command": "node web-access/scripts/check-deps.mjs" },
    "validators": [
      { "type": "word_count", "min": 50, "severity": "error" },
      { "type": "regex_match", "pattern": "Error|ERROR|失败", "must_match": false, "severity": "error" }
    ]
  }]
}
```

---

## 技能类型速查表

| 类型 | 代表skill | 典型产出 | 关键验证规则 |
|:----|:---------|:--------|:------------|
| **正文写作** | emergent-writer, horror-game-writer, opening-arc | .md小说章节 | 字数/违禁句式/实体覆盖率 |
| **设计规划** | project-bootstrap, plot-architecture | .md, .yaml, 多目录 | 文件存在/大小/yaml合法性 |
| **拆解分析** | book-deconstructor | .md分析报告 | 文件存在/关键词命中 |
| **质检评审** | skill-qa-payoff, market-test | .md评审报告 | 字数/关键词命中 |
| **调研采集** | cnovel-research, book-opinion-tracker | .md报告 | 文件存在/平台覆盖率 |
| **渲染发布** | html-renderer | .html文件 | DOCTYPE/文件大小/设计系统匹配 |
| **网络交互** | web-access | stdout文本 | 字数/错误关键词 |

---

## PipelineConfig 完整格式

```jsonc
{
  "run_id": "qc_20260526_001",          // 可选，自动生成
  "target_skill": "emergent-writer",    // 被检测的 Skill 名称
  
  "steps": [
    {
      "id": "step_01",                  // 步骤唯一标识
      "name": "正文渲染检查",            // 步骤可读名称
      
      "executor": {                     // 执行器配置
        "type": "skill",                // skill | command | function
        "skill_name": "emergent-writer",
        "action": "render_chapter",
        "params": {},                    // type=skill时，由外部agent执行
        "cwd": null                      // type=command时的工作目录
      },
      
      "validators": [                   // 质量闸门规则
        {
          "type": "word_count",         // 见下表
          "min": 1800,
          "max": 3500,
          "severity": "error"           // error(硬拦截) | warn(仅标记)
        }
      ],
      
      "llm_verify": {                   // LLM独立验证（可选）
        "enabled": true,
        "template_name": "chapter_review",   // content_review | chapter_review
        "scoring_dimensions": ["完整性", "逻辑性", "创意度"],
        "pass_threshold": 0.6
      },
      
      "block_on_failure": true          // error级别异常时卡住下一步
    }
  ],

  "global_config": {
    "output_dir": ".qc_reports",
    "api": {
      "llm_provider": "openai",
      "endpoint": "https://api.openai.com/v1",
      "model": "gpt-4o",
      "api_key_env": "QC_LLM_API_KEY"
    },
    "block_timeout_minutes": 30,
    "block_timeout_action": "skip"      // skip | fail | continue
  }
}
```

### 验证规则类型

| type | 验证内容 | 必要参数 | 适用场景 |
|:----|:--------|:--------|:--------|
| `word_count` | 字数范围 | `min`, `max` | 写作文本类 |
| `timeout` | 执行耗时 | `max_seconds` | 采集/渲染类 |
| `entity_coverage` | 实体覆盖率 | `required_entities`, `min_coverage` | 小说/设定类 |
| `file_exists` | 文件存在 | `required_paths` | 所有产出类 |
| `file_size` | 文件大小 | `min_bytes`, `max_bytes` | 渲染/发布类 |
| `regex_match` | 正则匹配 | `pattern`, `must_match` | 格式/关键词检查 |
| `custom` | 自定义函数 | `function_name`, `args` | 特定领域检查 |

---

## 审计日志结构

每次执行按 run_id 组织目录：

```
.qc_reports/
  └── qc_20260526_001/
      ├── meta.json                      # run 元信息 (target_skill, started_at等)
      ├── steps/
      │   ├── step_01_ch001.json         # 每步的完整审计记录
      │   └── step_02_html.json
      ├── audit_trail.jsonl              # 追加式事件流水（不可变）
      └── summary.json                   # 汇总报告
```

### 审计记录字段

```jsonc
{
  "run_id": "qc_20260526_001",
  "step_id": "step_01",
  "step_name": "正文渲染检查",
  "status": "COMPLETED",            // COMPLETED | FAILED | BLOCKED | COMPLETED_WITH_ANOMALIES

  "timing": {
    "started_at": "2026-05-26T10:00:00.000Z",
    "completed_at": "2026-05-26T10:02:35.000Z",
    "duration_ms": 155000
  },

  "output": {
    "word_count": 2150,
    "file_paths": ["03-正文/ch001.md"]
  },

  "validation_results": [
    { "rule": "word_count", "passed": true, "actual": 2150, "threshold": {"min": 1800, "max": 3500}, "severity": "error" }
  ],

  "llm_verification": {
    "enabled": true,
    "api_called": true,
    "api_latency_ms": 3200,
    "scores": {"完整性": 0.85, "逻辑性": 0.78, "创意度": 0.92},
    "average_score": 0.85,
    "pass_threshold": 0.6,
    "passed": true,
    "self_check_consistency": 0.88
  },

  "anomalies": [                     // 非空时触发阻塞（取决于severity和block_on_failure）
    {"rule": "regex_match", "severity": "warn", "message": "发现违禁句式: '说不清楚的颜色'"}
  ],

  "blocked_next": false,
  "file_access_log": [
    {"action": "read", "path": "03-正文/ch001.md", "size_bytes": 12500}
  ]
}
```

---

## Python API

```python
from 自动化质检.scripts.qa_pipeline import run_qc_pipeline, confirm_step, get_pipeline_status

# 执行一次质检管线
config = {
    "target_skill": "emergent-writer",
    "steps": [
        {"id": "ch001", "name": "第一章",
         "validators": [{"type": "word_count", "min": 1800, "severity": "error"}],
         "llm_verify": {"enabled": true, "template_name": "chapter_review"}}
    ],
    "global_config": {"output_dir": ".qc_reports", "api": {"api_key_env": "QC_LLM_API_KEY"}}
}
report = run_qc_pipeline(config)
print(report["overall_status"])     # PASSED | FAILED | COMPLETED_WITH_WARNINGS | BLOCKED

# 人工解除阻塞
confirm_step(report["run_id"], "ch001")

# 查询管线状态
status = get_pipeline_status(report["run_id"])
```

---

## 脚本文件

| 脚本 | 功能 |
|:----|:-----|
| `qa_pipeline.py` | 主入口——调度+验证+阻断+汇总报告 |
| `validators.py` | 7种内置验证器 + 自定义扩展点 |
| `audit_logger.py` | 审计追溯JSON日志 + audit_trail事件流水 |
| `qc_api_check.py` | LLM API独立验证（2套prompt模板） |

---

## 自定义验证器扩展

当内置7种规则不够用时（比如需要验证yaml合法性/html可渲染性），注册自定义函数：

```python
from 自动化质检.scripts.validators import register_custom

@register_custom("check_yaml_valid")
def check_yaml_valid(output, args):
    import yaml
    text = output.get("text", "")
    try:
        yaml.safe_load(text)
        return {"rule": "custom:check_yaml_valid", "passed": True, "severity": "error", "message": "yaml合法"}
    except yaml.YAMLError as e:
        return {"rule": "custom:check_yaml_valid", "passed": False, "severity": "error", "message": f"yaml解析失败: {e}"}
```

然后在 PipelineConfig 中引用：

```jsonc
{"type": "custom", "function_name": "check_yaml_valid", "severity": "error"}
```
