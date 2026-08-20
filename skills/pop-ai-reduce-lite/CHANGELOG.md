# CHANGELOG

## v2.4.0 | 2026-08-14

### 脚本迁移 Node.js（Popwave 标准运行时）+ 执行效率优化

- **analyze_metrics.py → `analyze_metrics.mjs`（Node 版）** — Popwave 环境无 Python 解释器（实测 run e4ba6de3 的 agent 花了 14 轮找 Python、被迫 Node 移植脚本）。改用 Node 后直接用 openclaw-runtime 自带 node 执行
- **validate_l2.py → `validate_l2.mjs`（Node 版）** — 同上
- **新增红线 ❌7（执行效率红线）** — ①表层字符一次性批量完成防返工；②台词跨段连击 = 切分伪影直接跳过；③指标一次跑全量
- **删除 .py 脚本**（保留 .mjs 为唯一实现）

## v2.3.2 | 2026-08-14

### tags 精简

- skill.json tags 从 ["写作管线","降AI","精简版","表层降噪"] 精简为 **["降AI味"]**（与主 skill 统一）

## v2.3.1 | 2026-08-14

### 修复（基于测试4 run 实测）

- **残余AI味预估算法补全** — 新增两条深层信号："忽然/突然"类概括式内心活动（>3处 +0.10）、金句升华腔（+0.05）。lite 不处理深层 AI 味，但预估必须如实反映未动信号
- **❌6 红线补强** — 明确"所有指标数据必须来自脚本输出，禁止自写或自行估算"

### 背景

测试4 lite 自评残余 0.40（≤0.45 可不深度），但深度 run 实测朱雀 0.93→0.60，两套口径不可比。根因：lite 预估只检测表层信号（破折号/引号/句长/对仗），漏了"忽然"类内心活动与金句升华等深层信号。

---

> 历史版本条目已归档：`_archive/changelog-history/pop-ai-reduce-lite/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
