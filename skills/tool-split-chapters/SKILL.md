# tool-split-chapters

> 拆书源文本预处理：把整册 TXT 切成可寻址章节、生成合并章节索引、按档位切批、校验范围、估算 token。v1.0.0：首版，补齐拆书管线「分章」这一环（此前 `_temp/chapters/` 无人生成）。完整版本历史见 CHANGELOG.md。

## 这个 Skill 做什么

| 输入 | 输出 | 下游 |
|:--|:--|:--|
| 整册 TXT（爬取产物或用户自带） | `chapters/chNNNN.txt`、`合并章节索引.json`、批次清单、范围校验结果、token 估算 | pop-decon（拆书入口，消费合并章节索引） |

它是确定性脚本，不是 AI 判断：同一输入必须产出逐字节一致的输出。不下载（那是 `tool-download-webnovel` 的活），不拆解（那是 `pop-decon-dimension` 的活），只做「把一坨文本变成可寻址的章」。

## 怎么操作

> execution.mode: 脚本执行。强加载：红线与速查表。弱加载：scripts 按需调用、references 按需读。

### 子命令

| 子命令 | 做什么 | 何时用 |
|:--|:--|:--|
| `split` | 分章归一，产出 `chapters/`、`章节索引/`、`合并章节索引.json`、`book.json` | 拿到整册 TXT 后第一步 |
| `batch` | 按档位切批，产出批次清单 JSON | 分章后、拆解前 |
| `validate-scope` | 校验拆解配置的 scope 是否合法，判定是否试拆 | 启动拆解前 |
| `estimate` | 按字数估算 token 区间 | 展示预估时 |

统一入口：

```
python scripts/split_book.py <子命令> ...
```

### split 分章

```
python scripts/split_book.py split 某书.txt -o 输出目录 --name 书名 --author 作者
```

规则（确定性，不猜测）：

- 编码嗅探：UTF-8 / UTF-8 BOM / UTF-16 / GB18030 / GBK，统一转为 UTF-8、LF。
- 章标题识别：行首 `第X章/回/节`（阿拉伯或中文数字）、`X章`、`Chapter X`、`序章/楔子/尾声/后记/番外`。行长度超过 80 字符视为正文，不判标题。
- 卷标题识别：行首 `第X卷/部/集`、`X卷`、`卷X`。只认数字卷号，不改卷号的特殊章节（序章/尾声）归章级。
- 章号以分章后的序号为准（`globalNo` 从 1 连续），不用标题里写的数字——站点普遍缺号重号。
- 卷内序号（`volumeLocalNo`）按卷单独从 1 编号。
- 防盗标记 `[ANTILEECH:xxx]` 写进该章 `flags`，并从字数统计里剔除。
- 无章节标题的连续文本：脚本报错退出，不做 AI 切分。这类书要人工或 AI 预处理后才能拆。

### batch 切批

```
python scripts/split_book.py batch 合并章节索引.json --profile standard -o 批次清单.json
```

档位（`--profile`）：`standard` ~30章/批（上限40）、`deep` 20章/批（质量优先）、`skeleton` 40章/批（全书骨架）。切批按卷内进行，跨卷不合并。可用 `--volume N` 或 `--chapters FROM TO` 限定范围。

### validate-scope 校验范围

```
python scripts/split_book.py validate-scope 合并章节索引.json 拆解配置.json
```

校验 `scope` 合法（越界、from>to 直接报错）。范围章节数小于 20 判定为试拆，退出码 2（试拆需专用质量规则，见 `pop-decon-dimension` 的 L1 门禁）。

### estimate 估算 token

```
python scripts/split_book.py estimate 合并章节索引.json -o 估算.json
```

按范围字数 × 系数区间 [0.6, 1.0]（每字符 token 数）估算，系数可用 `--ratio MIN MAX` 覆盖。

## 红线

1. **读取协议**：读 skill 文件用 `Get-Content -Encoding UTF8 -Raw` 或直接执行脚本，禁用 Read 工具（有行数限制会截断）。
2. **不得用 AI 猜切点** — 无章节标题的文本报错退出，不做推测分章；推测分章必须由用户确认，脚本只产出确定性结果。
3. **章号以分章序号为准** — 不用标题内嵌数字做章节定位，站点缺号重号会导致锚点池整体错位。
4. **章内分页不得切断** — 分章作用在合并后的整章文本上，分页内容归入同章，不得拆成多段。
5. **分章结果必须人工抽检边界** — 正则识别是启发式，正文中独立成行且以「第X章/卷」开头的短行可能误判，交付前抽检首末章与卷边界。

## 速查表

| 文件 | 读取/执行时机 | 核心内容 |
|:--|:--|:--|
| `scripts/split_book.py` | 执行分章/切批/校验/估算时 | 统一入口，含全部子命令 |
| `references/契约说明.md` | 需要理解合并章节索引与拆解配置字段时 | 三份契约的 schema 与字段含义 |

## 执行模式

由主 agent 直接执行脚本，无适合子 agent 的环节（确定性文本处理）。

## 版本

当前版本 v1.0.0（首版：补齐拆书管线「分章」环节，产出合并章节索引）。完整版本历史见 CHANGELOG.md。
