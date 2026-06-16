# 管线断链排查与修补实战

> 收录于 pop-writer-chapter · 引自信: 2026-06-15 写作管线全链路根因分析

## 断链模式识别

当正文出现以下症状时，说明 pipeine 某环节断链：

| 症状 | 可能断链位置 |
|:-----|:------------|
| 正文中角色状态与剧情基线不匹配 | 断链1 — entity-snapshot 未创建/未更新 |
| 数据面板零亮相（战斗章无升级反馈） | 断链2 — 设计包 `关键对白/数据` 字段未标注面板激活场景 |
| 正文缺乏场景感，所有段落叙事距离一致 | 断链2 — 设计包 `scene` 字段缺失 → prose 不知道用哪张DNA场景卡 |
| 多角色章叙事视角混乱 | 断链2 — 设计包 `POV` 字段缺失 |
| 章节奏平，读者读完无认知变化 | 断链3 — ◆小爽点或★中爽点未标注 |
| AI观感词多（他感到/他意识到/他心想），叙事者跳出来解释设定 | 断链4 — prose step 文件未加载，解说员句式检查未执行 |

## 标准修补路径

### 断链1: entity-snapshot 缺失
```
文件路径: 00-总控/entity-snapshot.yaml
依据: pop-writer-chapter Step 1 ★ entity-snapshot 初始化分支
动作:
  ① 从 volume-XX.md §三 读角色池
  ② 从 状态/角色/{角色名}-角色卡.md 读 core_desire/人格基线/初始等级/位置
  ③ 从 起点快照.md 读世界初始状态
  ④ 组装为 entity-snapshot.yaml（含 entities/event_log/timeline/flags）
  ⑤ 标记 _meta.version=1, total_chapters=0
```

### 断链2: 设计包缺 scene/POV/关键对白/数据
```
依据: pop-writer-chapter Step 2 事件链设计 / templates/fact-skeleton.md

每个事件补全五个字段:
  - scene: (映射到文风DNA场景卡值 — combat_stealth / dialogue_intel / narration_suspense 等)
  - POV: (感知锚点角色名，留空默认主角)
  - 关键对白/数据: (不可替换的原文，多条用 | 分隔)
  - 感官锚点: (事件首句感官信号，如"雨声启动""铁锈味启动")

  ★ 升级/面板数据：必须写精确竖列，如「击杀混沌狂战士。获得杀戮经验: 45点。等级提升: Lv2。」
  ★ 日记/信件/纸条：必须写精确原文，不可概括转述
  ★ 填不出的关键对白→填空字符串""，prose 自行发挥

  - 感官锚点: (v2 已有字段，保留)
```

### 断链3: 爽点未标注
```
依据: pop-writer-chapter references/payoff-guide.md
动作:
  ◆小爽点 ≥ 5/章（干脆斩杀/升级/打脸/梗植入 — 自设计自承接）
  ★中爽点 ≥ 1/章（信息揭示/关系转折/障碍突破/情绪落地 — plot 定位置或兜底）

  在事件中标注:
    小爽点?: ◆ 小爽点
    中爽点标记: ★中爽点(信息揭示)
```

### 断链4: prose step 文件未加载
```
依据: pop-writer-prose WRONG 9 / ⚠️0 前置检查
动作:
  ① skill_view 加载 step-1-read-input / step-2-render / step-3-verify / step-4-output
  ② Step 3 中检查:
     - 文本脉冲密度（每500字一个微脉冲）
     - 解说员句式（不是...而是... = 0次✅/1次⚠️/≥2次❌退回）
     - AI观感词（他感到/他仿佛/他心想 = 0次）
     - 视角一致性（限知视角不写非锚点角色内心）
     - 设计包 关键对白/数据 原文已全部精确嵌入正文
```

## 首次运行（CH1特有）

CH1 的 entity-snapshot 不存在是**正常状态**，不应阻断。按 Step 1 初始化分支创建即可。
CH1 无上一章衔接，开幕段从穿越/苏醒直接开篇。

## 核验命令

修补完成后运行以下核验：
```bash
# 1. entity-snapshot 存在
ls -la 00-总控/entity-snapshot.yaml

# 2. 设计包字段完整性（grep 各字段数量）
grep -c "scene:" 写作资产/设计包/ch*-设计包.md
grep -c "POV:" 写作资产/设计包/ch*-设计包.md
grep -c "关键对白/数据" 写作资产/设计包/ch*-设计包.md
grep -c "◆ 小爽点" 写作资产/设计包/ch*-设计包.md
grep -c "★中爽点" 写作资产/设计包/ch*-设计包.md

# 3. 正文质量检查
grep -c "不是[^。]*而是" 正文/ch*.md       # 应为0
grep -c "他感到|他仿佛|他心想|他意识到" 正文/ch*.md   # 应为0
grep -c "他似乎|他好像" 正文/ch*.md        # 应为0
```
