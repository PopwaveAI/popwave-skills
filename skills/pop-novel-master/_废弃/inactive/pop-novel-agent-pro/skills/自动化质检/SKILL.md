> ⚠️ **废弃 — 勿引用** 本文件所属 skill 已被重构/删除。agent 不应加载此文件。
> 所有活跃 skill 位于 skills/pop-novel-*

---
name: "鑷姩鍖栬川妫€"
description: "鑷姩鍖栬川妫€鍏冩妧鑳解€斺€斿浠讳綍Skill鐨勬墽琛岃繃绋嬪拰鏂囦欢杈撳嚭鍋氱粨鏋勫寲璐ㄩ噺妫€娴嬨€傛敮鎸佹楠よ皟搴?瀹¤杩芥函+LLM API楠岃瘉+璐ㄩ噺闂搁棬鎷︽埅銆傜敤浜庢祴璇曟墍鏈塻kill鐨勪骇鍑鸿川閲忓拰绠＄嚎绾緥銆傚綋闇€瑕侀獙璇佹煇涓猻kill鐨勮緭鍑烘槸鍚﹁揪鏍囨椂璋冪敤銆?
---

# 鑷姩鍖栬川妫€ Skill

杩欐槸涓€涓?*鍏冩妧鑳斤紙Meta-Skill锛?*鈥斺€斾笉鐩存帴鍒涗綔鍐呭锛岃€屾槸瀵瑰叾浠?Skill 鐨勬墽琛岃繃绋嬪拰杈撳嚭杩涜缁撴瀯鍖栬川閲忔娴嬨€?

**閫傜敤鎵€鏈?skill銆?* 閫氳繃涓嶅悓鐨?`PipelineConfig` 閫傞厤涓嶅悓绫诲瀷鐨勮緭鍑哄拰楠岃瘉闇€姹傘€?

---

## 鏍稿績鑳藉姏

| 鑳藉姏 | 璇存槑 |
|:----|:-----|
| **姝ラ璋冨害** | 鎸?PipelineConfig 瀹氫箟鐨勬楠ゅ簭鍒楅『搴忔墽琛岋紝3绉嶆墽琛屾ā寮?|
| **瀹¤杩芥函** | 姣忔鐢熸垚缁撴瀯鍖朖SON瀹¤璁板綍锛氳€楁椂/瀛楁暟/楠岃瘉缁撴灉/寮傚父鏍囪/鏂囦欢璁块棶 |
| **璐ㄩ噺闂搁棬** | 7绉嶅唴缃獙璇佽鍒?+ 鍙敞鍐岃嚜瀹氫箟瑙勫垯 |
| **LLM 鐙珛楠岃瘉** | 璋冪敤澶栭儴API瀵规楠や骇鍑虹嫭绔嬭瘎鍒嗭紝涓庤嚜璇勪氦鍙夋瘮瀵?|
| **闃诲鍗℃帶** | 涓婁竴姝ユ湁璇椂鑷姩闃诲涓嬩竴姝ワ紝绛夊緟浜哄伐纭鎴栬秴鏃跺鐞?|

---

## 蹇€熶笂鎵嬶細5绉嶅吀鍨媠kill鐨勯厤缃ā鏉?

### 1. 姝ｆ枃鍐欎綔绫?鈥?emergent-writer / horror-game-writer / opening-arc

**浜у嚭**: `03-姝ｆ枃/chXXX.md` 灏忚绔犺妭 + QC鎶ュ憡  
**闇€楠岃瘉**: 瀛楁暟鈮?000 / 杩濈鍙ュ紡0 / 鍓?00瀛楁湁閽╁瓙 / 瀹炰綋瑕嗙洊鐜?

```jsonc
{
  "target_skill": "emergent-writer",
  "steps": [{
    "id": "ch001_render",
    "name": "绗竴绔犳鏂?,
    "executor": { "type": "skill", "skill_name": "emergent-writer" },
    "validators": [
      { "type": "word_count", "min": 1800, "max": 3500, "severity": "error" },
      { "type": "regex_match", "pattern": "涓嶆槸[^銆傦紝锛沒*鑰屾槸", "must_match": false, "severity": "error" },
      { "type": "regex_match", "pattern": "璇翠笉娓匸^銆傦紝锛沒*(棰滆壊|鎰熻|鍛抽亾)", "must_match": false, "severity": "warn" },
      { "type": "entity_coverage", "required_entities": ["鏋楁繁", "璇″紓APP", "鐜╁"], "min_coverage": 0.7, "severity": "error" }
    ],
    "llm_verify": { "enabled": true, "template_name": "chapter_review", "scoring_dimensions": ["鍓?00瀛楅挬瀛?, "鎯呮劅寮х嚎"], "pass_threshold": 0.6 }
  }]
}
```

### 2. 鎷嗕功/璁惧畾绫?鈥?book-deconstructor / project-bootstrap / plot-architecture

**浜у嚭**: .md鍒嗘瀽鎶ュ憡 / .yaml閰嶇疆鏂囦欢 / 澶氭枃浠剁洰褰? 
**闇€楠岃瘉**: 鏂囦欢瀛樺湪 / 鏂囦欢澶у皬 / 缁撴瀯瀹屾暣鎬?/ yaml鍚堟硶

```jsonc
{
  "target_skill": "book-deconstructor",
  "steps": [{
    "id": "modeA_structure",
    "name": "缁撴瀯鎷嗚В浜у嚭",
    "executor": { "type": "command", "command": "cat output/modeA-report.md" },
    "validators": [
      { "type": "file_exists", "required_paths": ["output/modeA-report.md"], "severity": "error" },
      { "type": "file_size", "min_bytes": 1024, "severity": "error" },
      { "type": "regex_match", "pattern": "鑺傚鍦板浘|鑺傛媿搴忓垪", "must_match": true, "severity": "error" }
    ]
  }]
}
```

### 3. 璋冪爺/鑸嗘儏绫?鈥?cnovel-research / book-opinion-tracker

**浜у嚭**: .md璋冪爺鎶ュ憡 / 鐖櫕鏁版嵁鏂囦欢 / 澶氬钩鍙扮粨鏋滄眹鎬? 
**闇€楠岃瘉**: 鑷冲皯N涓钩鍙版湁鏁版嵁 / 鎶ュ憡瀹屾暣鎬?/ 鍏抽敭瀛楁瀛樺湪

```jsonc
{
  "target_skill": "book-opinion-tracker",
  "steps": [{
    "id": "platform_report",
    "name": "鑸嗘儏鎶ュ憡",
    "executor": { "type": "command", "command": "cat reports/opinion_report.md" },
    "validators": [
      { "type": "file_exists", "required_paths": ["reports/opinion_report.md"], "severity": "error" },
      { "type": "regex_match", "pattern": "## (璞嗙摚|寰崥|璐村惂|鐭ヤ箮)", "must_match": true, "severity": "warn" },
      { "type": "word_count", "min": 500, "severity": "error" }
    ]
  }]
}
```

### 4. HTML娓叉煋绫?鈥?html-renderer

**浜у嚭**: .html鍗曟枃浠? 
**闇€楠岃瘉**: 鏂囦欢澶у皬 / HTML缁撴瀯瀹屾暣 / 璁捐绯荤粺鍖归厤

```jsonc
{
  "target_skill": "html-renderer",
  "steps": [{
    "id": "html_output",
    "name": "HTML娓叉煋浜у嚭",
    "executor": { "type": "skill", "skill_name": "html-renderer" },
    "validators": [
      { "type": "file_exists", "required_paths": ["output/index.html"], "severity": "error" },
      { "type": "file_size", "min_bytes": 5120, "severity": "error" },
      { "type": "regex_match", "pattern": "<!DOCTYPE html>", "must_match": true, "severity": "error" },
      { "type": "regex_match", "pattern": "<html[^>]*>", "must_match": true, "severity": "error" }
    ],
    "llm_verify": { "enabled": true, "template_name": "content_review", "scoring_dimensions": ["瑙嗚瀹屾暣鎬?, "鍝嶅簲寮忛€傞厤"] }
  }]
}
```

### 5. 缃戠粶閲囬泦绫?鈥?web-access

**浜у嚭**: 缃戦〉鎶撳彇鍐呭锛堟枃浠舵垨stdout鏂囨湰锛? 
**闇€楠岃瘉**: 鍐呭闈炵┖ / 鏈夊叧閿瘝鍛戒腑 / 鏃犳姤閿欎俊鎭?

```jsonc
{
  "target_skill": "web-access",
  "steps": [{
    "id": "scrape_result",
    "name": "缃戦〉閲囬泦缁撴灉",
    "executor": { "type": "command", "command": "node web-access/scripts/check-deps.mjs" },
    "validators": [
      { "type": "word_count", "min": 50, "severity": "error" },
      { "type": "regex_match", "pattern": "Error|ERROR|澶辫触", "must_match": false, "severity": "error" }
    ]
  }]
}
```

---

## 鎶€鑳界被鍨嬮€熸煡琛?

| 绫诲瀷 | 浠ｈ〃skill | 鍏稿瀷浜у嚭 | 鍏抽敭楠岃瘉瑙勫垯 |
|:----|:---------|:--------|:------------|
| **姝ｆ枃鍐欎綔** | emergent-writer, horror-game-writer, opening-arc | .md灏忚绔犺妭 | 瀛楁暟/杩濈鍙ュ紡/瀹炰綋瑕嗙洊鐜?|
| **璁捐瑙勫垝** | project-bootstrap, plot-architecture | .md, .yaml, 澶氱洰褰?| 鏂囦欢瀛樺湪/澶у皬/yaml鍚堟硶鎬?|
| **鎷嗚В鍒嗘瀽** | book-deconstructor | .md鍒嗘瀽鎶ュ憡 | 鏂囦欢瀛樺湪/鍏抽敭璇嶅懡涓?|
| **璐ㄦ璇勫** | skill-qa-payoff, market-test | .md璇勫鎶ュ憡 | 瀛楁暟/鍏抽敭璇嶅懡涓?|
| **璋冪爺閲囬泦** | cnovel-research, book-opinion-tracker | .md鎶ュ憡 | 鏂囦欢瀛樺湪/骞冲彴瑕嗙洊鐜?|
| **娓叉煋鍙戝竷** | html-renderer | .html鏂囦欢 | DOCTYPE/鏂囦欢澶у皬/璁捐绯荤粺鍖归厤 |
| **缃戠粶浜や簰** | web-access | stdout鏂囨湰 | 瀛楁暟/閿欒鍏抽敭璇?|

---

## PipelineConfig 瀹屾暣鏍煎紡

```jsonc
{
  "run_id": "qc_20260526_001",          // 鍙€夛紝鑷姩鐢熸垚
  "target_skill": "emergent-writer",    // 琚娴嬬殑 Skill 鍚嶇О
  
  "steps": [
    {
      "id": "step_01",                  // 姝ラ鍞竴鏍囪瘑
      "name": "姝ｆ枃娓叉煋妫€鏌?,            // 姝ラ鍙鍚嶇О
      
      "executor": {                     // 鎵ц鍣ㄩ厤缃?
        "type": "skill",                // skill | command | function
        "skill_name": "emergent-writer",
        "action": "render_chapter",
        "params": {},                    // type=skill鏃讹紝鐢卞閮╝gent鎵ц
        "cwd": null                      // type=command鏃剁殑宸ヤ綔鐩綍
      },
      
      "validators": [                   // 璐ㄩ噺闂搁棬瑙勫垯
        {
          "type": "word_count",         // 瑙佷笅琛?
          "min": 1800,
          "max": 3500,
          "severity": "error"           // error(纭嫤鎴? | warn(浠呮爣璁?
        }
      ],
      
      "llm_verify": {                   // LLM鐙珛楠岃瘉锛堝彲閫夛級
        "enabled": true,
        "template_name": "chapter_review",   // content_review | chapter_review
        "scoring_dimensions": ["瀹屾暣鎬?, "閫昏緫鎬?, "鍒涙剰搴?],
        "pass_threshold": 0.6
      },
      
      "block_on_failure": true          // error绾у埆寮傚父鏃跺崱浣忎笅涓€姝?
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

### 楠岃瘉瑙勫垯绫诲瀷

| type | 楠岃瘉鍐呭 | 蹇呰鍙傛暟 | 閫傜敤鍦烘櫙 |
|:----|:--------|:--------|:--------|
| `word_count` | 瀛楁暟鑼冨洿 | `min`, `max` | 鍐欎綔鏂囨湰绫?|
| `timeout` | 鎵ц鑰楁椂 | `max_seconds` | 閲囬泦/娓叉煋绫?|
| `entity_coverage` | 瀹炰綋瑕嗙洊鐜?| `required_entities`, `min_coverage` | 灏忚/璁惧畾绫?|
| `file_exists` | 鏂囦欢瀛樺湪 | `required_paths` | 鎵€鏈変骇鍑虹被 |
| `file_size` | 鏂囦欢澶у皬 | `min_bytes`, `max_bytes` | 娓叉煋/鍙戝竷绫?|
| `regex_match` | 姝ｅ垯鍖归厤 | `pattern`, `must_match` | 鏍煎紡/鍏抽敭璇嶆鏌?|
| `custom` | 鑷畾涔夊嚱鏁?| `function_name`, `args` | 鐗瑰畾棰嗗煙妫€鏌?|

---

## 瀹¤鏃ュ織缁撴瀯

姣忔鎵ц鎸?run_id 缁勭粐鐩綍锛?

```
.qc_reports/
  鈹斺攢鈹€ qc_20260526_001/
      鈹溾攢鈹€ meta.json                      # run 鍏冧俊鎭?(target_skill, started_at绛?
      鈹溾攢鈹€ steps/
      鈹?  鈹溾攢鈹€ step_01_ch001.json         # 姣忔鐨勫畬鏁村璁¤褰?
      鈹?  鈹斺攢鈹€ step_02_html.json
      鈹溾攢鈹€ audit_trail.jsonl              # 杩藉姞寮忎簨浠舵祦姘达紙涓嶅彲鍙橈級
      鈹斺攢鈹€ summary.json                   # 姹囨€绘姤鍛?
```

### 瀹¤璁板綍瀛楁

```jsonc
{
  "run_id": "qc_20260526_001",
  "step_id": "step_01",
  "step_name": "姝ｆ枃娓叉煋妫€鏌?,
  "status": "COMPLETED",            // COMPLETED | FAILED | BLOCKED | COMPLETED_WITH_ANOMALIES

  "timing": {
    "started_at": "2026-05-26T10:00:00.000Z",
    "completed_at": "2026-05-26T10:02:35.000Z",
    "duration_ms": 155000
  },

  "output": {
    "word_count": 2150,
    "file_paths": ["03-姝ｆ枃/ch001.md"]
  },

  "validation_results": [
    { "rule": "word_count", "passed": true, "actual": 2150, "threshold": {"min": 1800, "max": 3500}, "severity": "error" }
  ],

  "llm_verification": {
    "enabled": true,
    "api_called": true,
    "api_latency_ms": 3200,
    "scores": {"瀹屾暣鎬?: 0.85, "閫昏緫鎬?: 0.78, "鍒涙剰搴?: 0.92},
    "average_score": 0.85,
    "pass_threshold": 0.6,
    "passed": true,
    "self_check_consistency": 0.88
  },

  "anomalies": [                     // 闈炵┖鏃惰Е鍙戦樆濉烇紙鍙栧喅浜巗everity鍜宐lock_on_failure锛?
    {"rule": "regex_match", "severity": "warn", "message": "鍙戠幇杩濈鍙ュ紡: '璇翠笉娓呮鐨勯鑹?"}
  ],

  "blocked_next": false,
  "file_access_log": [
    {"action": "read", "path": "03-姝ｆ枃/ch001.md", "size_bytes": 12500}
  ]
}
```

---

## Python API

```python
from 鑷姩鍖栬川妫€.scripts.qa_pipeline import run_qc_pipeline, confirm_step, get_pipeline_status

# 鎵ц涓€娆¤川妫€绠＄嚎
config = {
    "target_skill": "emergent-writer",
    "steps": [
        {"id": "ch001", "name": "绗竴绔?,
         "validators": [{"type": "word_count", "min": 1800, "severity": "error"}],
         "llm_verify": {"enabled": true, "template_name": "chapter_review"}}
    ],
    "global_config": {"output_dir": ".qc_reports", "api": {"api_key_env": "QC_LLM_API_KEY"}}
}
report = run_qc_pipeline(config)
print(report["overall_status"])     # PASSED | FAILED | COMPLETED_WITH_WARNINGS | BLOCKED

# 浜哄伐瑙ｉ櫎闃诲
confirm_step(report["run_id"], "ch001")

# 鏌ヨ绠＄嚎鐘舵€?
status = get_pipeline_status(report["run_id"])
```

---

## 鑴氭湰鏂囦欢

| 鑴氭湰 | 鍔熻兘 |
|:----|:-----|
| `qa_pipeline.py` | 涓诲叆鍙ｂ€斺€旇皟搴?楠岃瘉+闃绘柇+姹囨€绘姤鍛?|
| `validators.py` | 7绉嶅唴缃獙璇佸櫒 + 鑷畾涔夋墿灞曠偣 |
| `audit_logger.py` | 瀹¤杩芥函JSON鏃ュ織 + audit_trail浜嬩欢娴佹按 |
| `qc_api_check.py` | LLM API鐙珛楠岃瘉锛?濂梡rompt妯℃澘锛?|

---

## 鑷畾涔夐獙璇佸櫒鎵╁睍

褰撳唴缃?绉嶈鍒欎笉澶熺敤鏃讹紙姣斿闇€瑕侀獙璇亂aml鍚堟硶鎬?html鍙覆鏌撴€э級锛屾敞鍐岃嚜瀹氫箟鍑芥暟锛?

```python
from 鑷姩鍖栬川妫€.scripts.validators import register_custom

@register_custom("check_yaml_valid")
def check_yaml_valid(output, args):
    import yaml
    text = output.get("text", "")
    try:
        yaml.safe_load(text)
        return {"rule": "custom:check_yaml_valid", "passed": True, "severity": "error", "message": "yaml鍚堟硶"}
    except yaml.YAMLError as e:
        return {"rule": "custom:check_yaml_valid", "passed": False, "severity": "error", "message": f"yaml瑙ｆ瀽澶辫触: {e}"}
```

鐒跺悗鍦?PipelineConfig 涓紩鐢細

```jsonc
{"type": "custom", "function_name": "check_yaml_valid", "severity": "error"}
```

