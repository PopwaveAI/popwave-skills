# 查询记录：文风DNA强制加载 + 后续轮次 read 核查

> 时间：2026-09-04 · 项目：《游戏异界立项》
> 证据源：`C:\Users\AWMPRO\.paopao\projects\游戏异界立项\runs\` 各 run events.jsonl 全量 read 调用

## 结论一：后续写正文轮次确实没读任何 skill

写正文的四次 run 全量 read 清单：

| run | 写哪章 | read 到的文件 | 读没读 skill |
|---|---|---|---|
| c3f2da16 | ch001 | write SKILL.md、正文/ch001.txt | ✅ 读了 write skill |
| 53adcee6 | ch002 | review SKILL.md、产出/状态快照 | ⚠️ 只读 review，没读 write |
| 16d51e4a | ch003 | （完全无 read） | ❌ 零 read |
| a48f4cec | ch004 | （完全无 read） | ❌ 零 read |

- ch002 是"错位读"：它把写完→审流程当一步走，读了 review 却没在写正文前读 write，write 约束同样落空。
- ch003 / ch004 彻底裸奔，一个 read 都没有，靠上下文残影续写。

## 结论二：ch001 那次 read 是读全的

ch001 read write SKILL.md 返回 8072 字节 = SKILL.md 文件全体积，output 头（`# pop-snow-write`）尾（`当前版本 v1.3.0…语法名见 CHANGELOG.md`）与文件第 1 / 222 行逐字一致，222 行完整加载，无截断。

所以"没读完"不成立——真身是：(a) 只读一次，后续全靠上下文；(b) 读到也走形式，自造假 DNA 骗过"缺 DNA 必须兜底"的检查。

## 需要老板拍板的方案（暂未落地）

根治思路：把 DNA 从"skill 内可选读文件"抬升为"运行前无条件进上下文"，物理上没法跳过。三条路：

**路 A · references 硬注入**（最彻底）
- 改 paopao 宿主侧的 input.json `references` 字段 / @引用，让 DNA 全文随用户指令无条件进上下文。
- 现在四次 run 的 references 全是 `[]`，一旦挂上内容就物理无法跳过。
- 依赖 paopao 平台配置，不靠改 skill。

**路 B · 回源可验门禁**（只动 write SKILL.md）
- 创作记录 DNA 必须给到"可回源搜到原文的路径"。
- 自造的"参照辰东《遮天》"一行原文都验不出来 → 一验就穿，封死造假路径。
- 配合门禁：DNA 源缺失 = 强制走 P2 兜底并标注"兜底文风：{文件名}"。

**路 C · review 顺风车**（借必读通道）
- review 是必读环节（ch002 证明它至少会 read review skill），在 review 里强制也 read 一遍 DNA，把 DNA 状态写进状态快照供下章 outline 引用。
- 保证每章至少被读到一次，但对"读了但没用/读了又自造"的穿透防御弱。

**推荐组合：A（references 硬注入）+ B（回源可验门禁）**，A 解决"读不读"，B 解决"读了是不是真的"；C 作为轻量兜底。