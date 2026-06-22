# Step 1：读入上下文

> 管线: pop-writer-chapter v2.2
> 模板: `templates/fact-skeleton.md`
> 参考: `references/character-scheduling.md` / `references/location-orchestration.md` / `references/emotional-beats.md` / `references/info-release.md`

## 目的

读取上游 plot 产出的幕纲 + 剧情线 + 项目状态，建立本章设计基线。所有字段读完后再开始 Step 2。

## 前置条件

- [ ] `剧情设计/幕/vol-XX/act-YY.md` 存在（幕纲：分幕/章锚点/Canvas/枪链）
- [ ] `剧情设计/剧情线/*.md` 存在（主线/支线文档）
- [ ] `状态/角色/{主角}-角色卡.md` 存在

### entity-snapshot 初始化分支（CH1 首次运行专用）

检查 `状态/entity-snapshot.yaml`：
- ✅ 已存在 → 正常读取
- ❌ 不存在（CH1）→ 执行初始化：

```
① 从 剧情设计/剧情线/*.md 提取登场角色名列表
② 对每个角色，读 状态/角色/{角色名}-角色卡.md 提取 core_desire、人格基线、初始等级/位置
③ 从 小说世界设定/起点快照.md 提取世界初始状态
④ 组装为 entity-snapshot 写入 状态/entity-snapshot.yaml
⑤ 标注：⚠️ entity-snapshot.yaml 由 CH1 初始化创建
```

## 执行

### 1. 读幕纲（act-YY.md）

定位当前章（ch = N），从幕纲的「Step5 章锚点与 Canvas」段提取本章信息：

| 从幕纲取 | 用途 |
|:---------|:-----|
| 章锚点表 → 本章的章目标/活跃线/钩子/预期 payoff | 本章核心方向和约束 |
| Canvas 矩阵 → 本章各线的铺垫/释放/空白状态 | 哪些线在动、payoff_level |
| Canvas 节奏评估 → 密度和线间平衡 | 避免过载 |
| 幕级门槛 → 力量/信息/关系/资源门槛 | 本章角色能力边界 |
| 幕定位 → 幕功能/幕起点终点 | 本章在幕中的位置 |

### 2. 读剧情线文档

从 `剧情设计/剧情线/{主线,支线}-*.md` 提取：
- 核心驱动力、数值门槛、登场人物、配套套路链、契诃夫枪链、起终点切片

### 3. 读项目状态

| 文件 | 取什么 |
|:-----|:-------|
| `状态/entity-snapshot.yaml` | 所有角色当前状态（唯一 canon） |
| `状态/角色/{角色名}-角色卡.md` | core_desire、人格基线（慢变信息） |
| `章节设计包/ch{上一章}-设计包.md` | 上章末尾未闭合的节点 |
| `pop-trope-library/套路库/{套路名}.md` | 套路公式+节奏控制段 |

### 4. 场景类型推断

从 Canvas 线摘要关键词推断：

| 暗示 | 场景类型 |
|:-----|:---------|
| 遭遇/攻击/战斗/追杀 | combat |
| 商量/谈判/质问/坦白 | dialogue |
| 发现/探索/进入/揭示 | discovery |
| 危机/压迫/紧迫/绝境 | crisis |

### 5. 确定本章活跃线和枪链

- 活跃线：Canvas 矩阵中本章非空的线
- 枪链：从剧情线文档提取本章设伏/回收的枪点（Step5 已预留 Canvas 位置）

## 产出（内存基线）

```
本章位置：幕号/章号/标题
Canvas 约束：payoff 位置/情绪目标/钩子方向/字数上限
可用资源：角色池(entity-snapshot+角色卡) / 枪链 / 套路链
衔接：上章末尾状态 / 未闭合节点
```
