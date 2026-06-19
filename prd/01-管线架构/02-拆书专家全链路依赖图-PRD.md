# 拆书专家全链路依赖图 — 文件依赖与产出全景 PRD

> 版本：v1.0 | 2026-06-19
> 说明：本文档覆盖拆书专家（pop-novel-*）全链路。写作专家见 `01-写作专家全链路依赖图-PRD.md`。

---

## 目录

- 一、拆书专家架构总览
- 二、Skill 管线流程
- 三、各 Skill 详细文件依赖表
- 四、拆书产出 → 写作专家消费协议
- 五、典型路径速查
- 六、关键架构决策
- 附录 A：拆书项目文件全貌

---

## 一、拆书专家架构总览

### 1.1 为什么拆为写作专家和拆书专家

| 维度 | 拆书专家（pop-novel-*） | 写作专家（pop-writer-*） |
|:-----|:-----------------------|:------------------------|
| **目标** | 拆解分析现有作品 | 创作一本新书 |
| **输出** | 拆书报告、文风DNA、参考数据 | 正文、设计包、世界观、剧情 |
| **独立调用** | 拆解参考书 / 提取文风DNA | 开新书 / 续写 / 注入元素 |
| **消费关系** | 独立运行，产出供写作专家消费 | 消费拆书专家的产出（Lv1/Lv2） |
| **技能前缀** | `pop-novel-*` | `pop-writer-*` |

两位专家**不耦合**——拆书专家可以独立调起（用户说"拆解这本书"），写作专家也可以在没有拆书产出时独立运行。

### 1.2 拆书专家全链路

```
┌──────────────────────────────────────────────────────────────┐
│                     拆书专家（pop-novel-*）                    │
│                                                              │
│  download-webnovel-txt                                        │
│  TXT 直链下载                                                 │
│  → 产出: {书名}.txt                                          │
└──────────────────────┬───────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-novel-deconstructor                                     │
│  拆书分析 (Phase S → Phase 0→4)                              │
│  ★ Phase S: Lv1 快速拆解（~25min，6个轻量文件）              │
│  ★ Phase 0-4: Lv2/Lv3 全量深拆（T1~T7 + 文风DNA）           │
│  → 产出: Lv1-拆解摘要 + T1~T7 + 三维拆书档案                 │
└──────────┬──────────┬───────────────────────────────────────┘
           │          │
           │          ▼
           │    ┌──────────────────────────────────────────────┐
           │    │  pop-dna                                     │
           │    │  文风DNA蒸馏 (从 ≥20 章均匀采样)              │
           │    │  → 产出: 写作资产/文风DNA/{书名}.md           │
           │    └──────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-novel-character-schema                                  │
│  角色分级标准 (Lv1~Lv4) — 静态标准定义 Skill                 │
│  产出: schema 模板 + 示例卡                                   │
│  ★ 消费方: world（写作专家）做角色卡时加载                    │
└──────────────────────────────────────────────────────────────┘

                ┌──────────────────────────────────────────────┐
                │  pop-novel-bookstrap (逆向工程)               │
                │  ★ 仅 reverse 模式保留                       │
                │  → 从已有正文逆向提取设定、还原卷纲（续写场景）│
                └──────────────────────────────────────────────┘
```

### 1.3 双专家交互关系

拆书专家为写作专家产出参考数据，但不消费写作专家任何产出：

```
拆书专家产出          →       写作专家消费
  Lv1 拆解摘要                 creative（PRD/引擎参考）
  Lv4-主角参考卡                creative（主角设计参考）
  卷1起终点快照                 creative（节奏参考）
  快速文风指纹                  prose-render（风格感知）
  T1/T2/T3/T4                 world（L1设定参考）
  char-schema Lv1~Lv4          world（角色卡标准）
```

产出存于 `_参考书/{书名}/` 下，多个写作项目可同时消费同一份拆书数据。

### 1.4 调度入口

两位专家共享 expert-writer 元 Skill 调度：

```
用户消息
  │
  ▼
expert-writer（元 Skill）
  ├─ 意图识别
  │   ├─ "开新书/续写/注入元素" → 写作专家
  │   ├─ "拆解这本书/分析文风"  → 拆书专家
  │   └─ "帮我写/检查/发布"    → 写作专家对应子Skill
  │
  ├─ 写作专家路由 → 详见写作专家 PRD
  │
  └─ 拆书专家路由:
      ├─ download → deconstructor(Phase S/0-4) → pop-dna(可选)
      └─ 产出写入 _参考书/{书名}/，更新 reference_deconstructions[]
```

---

## 二、Skill 管线流程

### 2.1 参考书拆解

```
用户说"拆解这本书"
  │
  ▼
Step 1 · download-webnovel-txt
  → 搜索直链 → 下载 → 质检 → {书名}.txt
  ↓
Step 2 · pop-novel-deconstructor
  ├─ Phase S: Lv1 快速拆解（~25min）
  │   → 6 个轻量文件（story-engine + 主角参考卡 + 快照 + 文风指纹）
  │   → "老板可以开书了"
  ├─ Phase 0: 采样日志
  ├─ Phase 1: 诊断报告
  ├─ Phase 2: T1~T7 独立产出
  ├─ Phase 3: 验证报告
  └─ Phase 4: 三维拆书档案 + 起终点快照
  ↓ (可选)
Step 3 · pop-dna（文风DNA蒸馏）
  → 均匀采样 ≥20 章 → 全书搜索验证 → 写作资产/文风DNA/{书名}.md
```

---

## 三、各 Skill 详细文件依赖表

### 3.1 pop-novel-deconstructor（拆书分析 — 拆书专家核心）

| Phase | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Phase S** ★ | {书名}.txt | `Lv1-拆解摘要.md` + `Lv4-{主角}-参考卡.md` + `卷1-起点/终点快照.md` + `快速文风指纹-top5.md` | creative、world |
| **Phase 0** | Phase S + {书名}.txt | `{书名}-Phase0-采样日志.md` | Phase 1 |
| **Phase 1** | Phase 0 | `{书名}-Phase1-诊断报告.md` | Phase 2 |
| **Phase 2** | 诊断报告 + T1~T7 模板 | `{书名}-T1~T7` × 7 | Phase 3、world |
| **Phase 3** | T1~T7 | `{书名}-Phase3-验证报告.md` | Phase 4 |
| **Phase 4** | 全部 Phase 产出 | `{书名}-三维拆书档案.md` | pop-dna、world |

### 3.2 pop-dna（文风DNA蒸馏）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 采样 | {书名}.txt（≥20 章均匀采样） | 采样样本 | 全文搜索验证 |
| 蒸馏 | 采样样本 + 全书搜索 | `写作资产/文风DNA/{书名}.md`（含叙事哲学/技法偏好/节奏模式） | prose-render |

### 3.3 pop-novel-character-schema（角色分级标准）

> 轻量标准定义 Skill，不执行具体角色设计流程。拆书专家产出，写作专家消费。

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 模板定义 | — | `schema/Lv1-one-shot.md` ~ `Lv4-core.md` | world 角色产出阶段 |
| 示例卡 | 参考小说原文 | `examples/Lv1~Lv4 案例卡` | world 角色产出阶段（对照参考） |

### 3.4 download-webnovel-txt（TXT 下载）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 搜索直链 | 书名 | — | 下载 |
| 下载 | 直链 URL | `{书名}.txt` | deconstructor |
| 质检 | 下载内容 | 质检报告 | deconstructor |

### 3.5 pop-novel-bookstrap（逆向工程）

保留 reverse 模式功能。forward 模式已迁移至 creative + world。

| Phase | 说明 |
|-|-|
| Phase r1~r6 | 从已有正文逆向提取设定、还原卷纲（续写场景） |

### 调度层私有文件

| 文件 | 读写者 | 用途 |
|-|-|-|
| **workspace-index.yaml** | expert-writer | 全局索引 — 项目列表、拆书引用、阶段追踪 |

---

## 五、典型路径速查

| 场景 | 管线路径 | 关键闸门 |
|:-|:---------|:---------|
| **拆解参考书（快速）** | download → deconstructor Phase S（~25min，6个轻量文件） | TXT 质量验证 |
| **拆解参考书（全量）** | download → deconstructor Phase S→0→1→2→3→4（T1~T7） | 阶段间验证报告 |
| **提取文风DNA** | deconstructor（≥20章）→ pop-dna → 写作资产/文风DNA/{书名}.md | 20章采样下限 |
| **逆向还原设定（续写场景）** | bookstrap REV Phase r1→r2→r3→r4→r5→r6 | 精读闸门 |
| **角色分级参考** | pop-novel-character-schema（独立调用） | — |

---

## 六、关键架构决策

### 6.1 为什么拆为双专家

| 决策 | 理由 |
|-|-|
| **独立调用** | 拆书专家不需要写作专家上下文即可独立运行。用户说"拆这本书"不与某个写作项目绑定 |
| **产出可复用** | 拆书产出存于 _参考书/{书名}/，多个写作项目可同时消费同一份拆书数据 |
| **职责隔离** | 拆书专家专注于"怎么分析"，写作专家专注于"怎么创作"。两个能力集不同 |
| **调度清晰** | expert-writer 通过意图识别路由到对应专家，不耦合两个域的执行逻辑 |

### 6.2 为什么 character-schema 在拆书专家

| 决策 | 理由 |
|-|-|
| **标准 ≠ 执行** | character-schema 定义"角色卡长什么样"（标准），world 执行"具体角色卡填写"（实现） |
| **跨专家复用** | character-schema 被 world（写作专家）消费，但标准本身由拆书专家维护——从拆书积累中提炼分级标准 |
| **拆书对齐** | 拆出的角色参考卡按 character-schema Lv1~Lv4 分级，world 产出时自动对照 |

### 6.3 为什么仅保留 bookstrap reverse 模式

| 决策 | 理由 |
|-|-|
| **forward 模式迁移** | forward（从设定→正文）已迁移至 creative + world，bookstrap 不再承担正向创作职责 |
| **reverse 保留** | 续写/恢复会话时需要从已有正文逆向提取设定。这是 bookstrap 不可替代的能力 |

---

## 附录 A：拆书项目文件全貌

```text
_参考书/{书名}/
│
├── {书名}.txt                       ← download-webnovel-txt（原始文本）
│
├── Lv1-拆解摘要.md                   ← deconstructor Phase S
├── Lv4-{主角}-参考卡.md              ← deconstructor Phase S
├── 卷1-起点快照.md                   ← deconstructor Phase S
├── 卷1-终点快照.md                   ← deconstructor Phase S
├── 快速文风指纹-top5.md              ← deconstructor Phase S
│
├── {书名}-Phase0-采样日志.md         ← deconstructor Phase 0
├── {书名}-Phase1-诊断报告.md         ← deconstructor Phase 1
├── {书名}-T1-力量体系.md             ← deconstructor Phase 2（→ world）
├── {书名}-T2-世界观展开.md           ← deconstructor Phase 2（→ world）
├── {书名}-T3-角色系统.md             ← deconstructor Phase 2（→ world）
├── {书名}-T4-剧情结构.md             ← deconstructor Phase 2
├── {书名}-T5-叙事节奏.md             ← deconstructor Phase 2
├── {书名}-T6-世界细节填充.md         ← deconstructor Phase 2
├── {书名}-T7-文风分析.md             ← deconstructor Phase 2
├── {书名}-Phase3-验证报告.md         ← deconstructor Phase 3
├── {书名}-三维拆书档案.md             ← deconstructor Phase 4（→ pop-dna、world）
│
└── 写作资产/文风DNA/{书名}.md         ← pop-dna（→ prose-render）

schema/                              ← pop-novel-character-schema
├── Lv1-one-shot.md
├── Lv2-side.md
├── Lv3-major.md
├── Lv4-core.md
└── examples/
    ├── Lv1-案例卡.md
    └── Lv4-案例卡.md
```

---

> 本文档覆盖拆书专家（pop-novel-*）全链路。写作专家见 `01-写作专家全链路依赖图-PRD.md`。