# Project State Discovery — 当 workspace-index.yaml 不存在时

> 场景: 用户说"继续任务"或路由到 expert-writer，但项目目录下无 workspace-index.yaml
> 目的: 从文件系统自动推断项目当前阶段，初始化索引

## 阶段推断矩阵

### 1. 扫描目标文件（按优先级）

| 文件/目录 | 存在暗示 | 不存在暗示 |
|:----------|:---------|:-----------|
| `创意种子/PRD.md` | 创意阶段已启动 | 可能还没开始 |
| `创意种子/故事引擎.md` | 创意核心阶段完成 | 仍在早期方向碰撞 |
| `小说世界设定/L1-` (6+ 个文件) | 世界构建完成 | 仍在 world 阶段或之前 |
| `储备剧情池/素材储备池.md` | creative 全部完成 | 需检查缺失了哪步 |
| `设计/全书架构.md` | plot Phase 0 完成 | 可进入 plot |
| `设计/卷/volume-XX.md` | plot Phase 1 进行中 | 需检查是否已有架构 |
| `设计/幕/vol-XX/act-YY.md` | plot Phase 2 进行中 | 需检查卷设计 |
| `写作资产/设计包/chXXX-设计包.md` | chapter-design 进行中 | 仍在 plot 阶段 |
| `正文/chXXX.md` | 正文渲染进行中 | 仍在设计阶段 |
| `写作资产/文风DNA/{书名}.md` | 文风DNA 已提取 | S 文件，不强制 |

### 2. 核心启发式

```python
# 伪代码逻辑
if 存在 创意种子/PRD.md:
    if 存在 设计/全书架构.md:
        if 存在 设计/卷/volume-01.md:
            if 存在 设计/幕/vol-01/act-01.md:
                phase = "act_design_in_progress"
            else:
                phase = "volume_design_complete_waiting_user"
        else:
            phase = "architecture_complete"
    elif 存在 储备剧情池/素材储备池.md:
        phase = "creative_complete_ready_for_plot"
    elif 存在 创意种子/故事引擎.md:
        phase = "story_engine_done_world_in_progress"
    else:
        phase = "prd_done_creative_in_progress"
else:
    phase = "unknown_or_not_started"
```

### 3. 索引初始化清单

发现阶段后，写入 workspace-index.yaml 的必填字段：

```yaml
project:
  name: "{从 PRD 或目录名推断}"
  status: "{推断的阶段}"
  started: "{最早文件的 mtime}"

progress:
  current_phase: "{推断的阶段}"
  next_skill: "{根据阶段路由}"
  ready: true
  last_action: "文件系统自动发现：{简述发现结论}"
```

### 4. next_skill 路由映射

| 推断阶段 | next_skill | 说明 |
|:---------|:-----------|:------|
| `unknown_or_not_started` | pop-writer-creative | 从方向碰撞开始 |
| `prd_done` | pop-writer-creative | 继续 creative 管线 |
| `creative_complete_ready_for_plot` | pop-writer-plot | 从全书架构开始 |
| `architecture_complete` | pop-writer-plot | 从卷设计开始 |
| `volume_design_complete_waiting_user` | pop-writer-plot | 等待用户确认卷设计后进幕纲 |
| `act_design_in_progress` | pop-writer-plot | 继续当前幕的编排 |
| `chapter_design_in_progress` | pop-writer-chapter | 继续章设计包 |
| `prose_in_progress` | pop-writer-prose | 继续正文渲染 |

### 5. 注意事项

- 不读取文件内容来推断阶段——只用路径存在性判断
- 有 `写作资产/文风DNA/` 但不一定有 `正文/` — 二创/拆书场景，需区分 forward vs reverse pipeline
- `设计/` 目录空存在但无子文件 → 可能是误创建，保守判断为 phase 前状态
- 多种阶段的文件混存（如同时有 `设计/卷/` 和 `正文/`）→ 取 pipeline 中最下游的完整阶段
