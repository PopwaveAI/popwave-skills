# CHANGELOG

## v1.0.0 | 2026-09-10

### 初始化：自 pop-snow-outline v1.8.0 复制迁移（正文循环三件套替换之一）

老板拍板：snow 的 outline/write/review 复制改名替代 mirror 正文循环（评估结论：snow 三件套工程化更成熟——脚本化检查/文风DNA/全书日志状态管理）。本 skill 为替代链第一环。

- **复制基底**：pop-snow-outline v1.8.0 全量复制（描述约束版四块章纲格式 v5.1/容量红线 4-6 场/A-B 双路径/事实抽查 8 项/资料门/存档后去AI味 doc 检查/章末钩 6 类轮换/80-20 断章提示/沉睡伏笔预警）。
- **新增第 0 节 · 产出三检查**：事前沟通（对齐节奏基调/文风延续）→ 事后确认（章纲确认点报用户，确认才落盘）→ research 评估（新场景/职业/地域/材料资料不够派 pop-snow-research 补采）。
- **输入适配**：上游"白描卡"改为消费 mirror-plot 卷纲对应章（核心剧情点+落点+爽点标签），态源仍为全书日志，衔接仍读上一章章日志。
- **引用改名**：下游 pop-snow-write → pop-mirror-write；去AI味脚本仍调用 `skills/pop-snow-pipeline/scripts/deai_gate.py`（跨系列脚本，单一维护源，不复制）。
- **红线**：描述约束/容量红线/上游优先/事实抽查/伏笔纪律/三检查纪律 6 条。

同步三件套：SKILL.md / skill.json（version 1.0.0）/ CHANGELOG（＋ templates/章纲.tpl.md 复制自 snow）。
