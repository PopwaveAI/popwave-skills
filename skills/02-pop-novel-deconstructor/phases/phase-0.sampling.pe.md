# Phase 0：分层扫描

> 定位：Lv2/Lv3 前置。前 100 章（或全书）全量采样。

## 🔧 数据提取前置命令（硬性！先执行再写产出）

执行以下脚本提取 ch1-100 章节索引，提取结果写入 `_temp/chapter-index.json`，此 JSON 是写采样日志的基础数据。

### 执行命令
```powershell
python "..\_scripts\extract.py" index "{$TXT_FILE_PATH}" ".\_temp\"
```

### 输出文件
`.\_temp\chapter-index.json`

字段说明：
| 字段 | 内容 | 用途 |
|:-----|:-----|:-----|
| `meta.totalChapters` | 全书总章节数 | 完整性判断 |
| `meta.first100Chars` | ch1-100 总字符数 | 采样规模 |
| `chapters[].chapter` | 章号 | 逐章索引 |
| `chapters[].title` | 章节标题 | 采样日志 |
| `chapters[].charCount` | 去除空白后的字符数 | 字数统计 |
| `chapters[].firstSentence` | 正文首句（前80字） | 内容速览 |
| `chapters[].tags[]` | battle/worldbuilding/economy 标签 | 内容分类 |

### 规则
1. 采样日志中的统计数据（章号/字数/类型分布）必须来自此 JSON，不得估算
2. JSON 中不含的章节标记为未读范围，不得编造内容
3. 写采样日志时如需引用某章的具体内容，返回原文对应行数读取

---

## 速查表

| 步骤 | 操作 | 读什么 | 产出 | 门禁 |
|:-----|:-----|:-------|:-----|:-----|
| 1 | 格式识别 | .txt/.md 直接读，其他 `scripts/extract.py` | 文本就绪 | ❌ 不支持格式退回 |
| 2 | 完整性验证 | 25%/50%/75% + 结尾 | 可读性确认 | ❌ 乱码/截断退回 |
| 3 | 全量采样 | 前100章逐章 | 采样日志 | — |

## 产出

`_参考书/{书名}/Phase0-采样日志.md`：逐章统计（章号/标题/字数/行范围）。

## 格式约束

- `.md` 格式
- >500K 字符的文件用 Python 脚本切片访问
