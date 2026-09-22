# CHANGELOG

## v1.0.0（2026-09-22）

- 首版：补齐拆书管线「分章」环节。此前 `pop-decon-dimension` 的 L1 分批精读要求读 `_temp/chapters/chXXX.txt`，但全仓无任何代码生成该目录，属断链。
- 新增 `scripts/split_book.py` 四个子命令：`split`（分章归一）、`batch`（切批）、`validate-scope`（范围校验）、`estimate`（token 估算）。
- 产出 `合并章节索引.json`：每章带全书序号、卷内序号、字数、异常标记，供宿主与拆解层共读，避免「UI 看到的章」与「拆解读到的章」漂移。
- 新增 `references/契约说明.md`：三份契约（合并章节索引、拆解配置、批次完成标志）的 schema。
