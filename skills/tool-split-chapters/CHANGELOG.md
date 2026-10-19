## 0.1.1 - 2026-10-19

- 补充市场卡面 summary 与精选元数据。

## v0.1.0 | 2026-10-12

**确定性分章脚本迁入技能仓库，与桌面端解耦。**

- 从桌面端内置目录（`apps/desktop/skills/tool-split-chapters/`）迁入本仓库 `skills/tool-split-chapters/`，含 `scripts/split-chapters.mjs`，此后只在本仓库维护。
- 桌面端改为按 skill id 解析本 skill 的脚本路径后再调用（带 `--clean` / `--clean-out` / `--dry-run` 参数），不再依赖应用内副本。
- 纯 Node ESM、零模型调用；输出契约（manifest / 章节索引 / 合并章节索引 / 指纹 / 批次计划）未变。
