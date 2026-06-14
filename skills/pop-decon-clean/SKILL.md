# pop-decon-clean · 章节清洗 v1.0.0

> **定位：Phase 1 of deconstruction. 原始 TXT → 逐章清洗 → 逐章 JSON.**
> **核心约束：extract.py 硬性前置。每章必须独立文件。**

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **ETL 未执行就清洗** — extract.py 还没跑，full_text.txt 不存在 → 退回 |
| ❌2 | **跳步拆分** — 全本 txt 没按章切 → 退回先拆分 |
| ❌3 | **广告混入产出** — 未去广告/导航/版权声明 → 退回清洗 |
| ❌4 | **章序号混乱** — 拆分后的文件序号与原文章号不匹配 → 退回 |
| ❌5 | **JSON 无源数据** — chapter-data/chXXX.json 中无条目仍产出 → 退回 |
| ❌6 | **产出只留摘要** — 写完说「已清洗 {N} 章。产出在 _temp/chapters/。」|

---

## 速查表

| 步骤 | 操作 | 读什么 | 产出 | 门禁 |
|:-----|:-----|:-------|:-----|:-----|
| 1 | 运行 extract.py | TXT/EPUB 文件 | `_temp/full_text.txt` + `_temp/metadata.json` | ❌ 脚本失败退回 |
| 2 | 按章拆分 | `full_text.txt` | `_temp/chapters/ch001.txt` ... `chNNN.txt` | ❌ 章数不匹配退回 |
| 3 | LLM 逐章清洗 | `chapters/chXXX.txt` | `_temp/chapters/ch001.txt (clean)` ... | ❌ 广告未去退回 |
| 4 | 逐章结构化 JSON | 清洗后的 `chXXX.txt` | `_temp/chapter-data/ch001.json` ... | ❌ JSON 空退回 |

---

## 核心流程

### Step 1: ETL — 运行 extract.py
详见 `steps/step-1-etl.md`
- **读什么**: 原始 TXT/EPUB
- **做什么**: 运行 extract.py → `full_text.txt` + `metadata.json`
- **产出**: `_temp/full_text.txt` + `_temp/metadata.json`
- **门禁**: 任一缺失 → 退回

### Step 2: 按章拆分
详见 `steps/step-2-split.md`
- **读什么**: `_temp/full_text.txt`
- **做什么**: 按章节标题正则切分 → 独立 txt 文件
- **产出**: `_temp/chapters/ch001.txt` ... `chNNN.txt`
- **门禁**: 拆分后数量与 `metadata.json` 的章节数不一致 → 退回

### Step 3: LLM 逐章清洗
详见 `steps/step-3-clean.md`
- **读什么**: `_temp/chapters/chXXX.txt`
- **做什么**: LLM 逐章去除广告/导航/版权声明 → 仅保留正文
- **产出**: 清洗后的 `_temp/chapters/chXXX.txt`
- **门禁**: 广告未去净 → 退回

### Step 4: 逐章结构化 JSON
详见 `steps/step-4-json.md`
- **读什么**: 清洗后的 `_temp/chapters/chXXX.txt`
- **做什么**: 提取事件摘要、角色出场、关键对话 → JSON
- **产出**: `_temp/chapter-data/ch001.json` ... `chNNN.json`
- **门禁**: JSON 中 event_summaries 为空 → 退回

---

## 落盘检查点

| 确认项 | 级别 |
|:-------|:----:|
| `_temp/full_text.txt` | All |
| `_temp/metadata.json` | All |
| `_temp/chapters/ch001.txt` ... `chNNN.txt` | All |
| `_temp/chapter-data/ch001.json` ... `chNNN.json` | All |

---

## 边界条件

| 条件 | 处理方式 |
|:-----|:---------|
| TXT 为空 / 0 字节 | 终止，报「输入文件为空」|
| 章节标题无规律 | 按段落数 / 章节标记（第X章 / 第X卷 / 序章）兜底识别 |
| 文件名含非法字符 | 统一用 `chXXX` 格式命名 |
| 单章内容过长（>8000 字）| 章内再拆为 segment_a / segment_b，JSON 中标注 `split: true` |
| 原始文件非 TXT（EPUB/PDF）| 先用 extract.py 统一转为 `full_text.txt` |

---

## ❌ WRONG 示例

| 场景 | 错误做法 | 正确做法 |
|:-----|:---------|:---------|
| ETL 未运行 | 跳过 extract.py 直接拆章 | 必须先跑 extract.py 得到 full_text.txt |
| 广告未去净 | 保留网站导航和版权声明 | 逐行扫描，标记并移除所有非正文段落 |
| 章序号混乱 | ch001 对应原文第 3 章 | 按原文实际章号命名，metadata 中建立映射表 |
| JSON 空仍产出 | `chapter-data/ch001.json` event_summaries 为空 | 退回，重跑 LLM 提取 |

---

## 版本

v1.0.0 | 2026-06-15 → [CHANGELOG.md](CHANGELOG.md)
