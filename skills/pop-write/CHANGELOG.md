# CHANGELOG

## v1.0.0 | 2026-09-11

### 建包：三线 write 收敛为中性名 pop-write（老板拍板）

三线 write 骨架已高度同质（都是"读章纲日志→注入文风DNA→去AI味"三件事），维护三份副本反复出问题（同一改动改三遍；snow 打分表/文风兜底副本陈旧）。收敛为**一份共用 skill**，中性名不带系列中缀。

- **蓝本＝灯塔**（进度最完整）：`pop-lantern-write` v1.17.0 的 SKILL.md 三件事结构原样承接。
- **线间差异全部收进 §0 系列适配表**（3 行）：怎么认线（看项目里存在哪个上游文件：`单元N-编排.md`→灯塔／`卷N-幕M-白描.md`→雪花／`涌现账本.md`→涌现）＋ 上游输入源 ＋ 章纲/日志路径 ＋ 文风资源 ＋ 线内纪律。SOP 主干三线共用，适配表之外不分叉。
- **文风资源合并进本包**：`references/夜无疆.md`（灯塔·单份新格式）＋ `references/文风兜底/`（雪花 22 赛道档 ＋ 涌现写死档 `辰东.md`）。哪份照适配表取。
- **脚本**：`scripts/word-count.ps1` 随本包；去AI味脚本沿用全仓共用宿主 `pop-snow-pipeline/scripts/deai_gate.py`（脚本必须落在具体 skill 包里，应用按 skill 为单位下载）。
- **涌现三条线内纪律**显式写进适配表与 Step 2：章纲可偏离（起跳板非锁链）／设定从内容模板库选／情绪坐标（峰值）不可偏离。
- **替代并删除**：`pop-lantern-write`（v1.17.0）／`pop-snow-write`（v1.16.0）／`pop-emergent-write`（v1.3.0）三包并入本包后删除；三线 pipeline 的 `skills` 依赖清单、三线 seed/outline 的指针同步改指 `pop-write`。
- 同步四件套：SKILL.md / skill.json（1.0.0）/ CHANGELOG ＋ references＋scripts。
