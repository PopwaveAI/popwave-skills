---
name: novel-worldbuilding
description: 管理小说世界观资产 —— 地点（location）和体系（system，含力量体系/政治/科技/宗教/经济/军事/社会）。当用户说"构建世界观"、"加一个地点"、"设计魔法体系"、"政治体系"、"修真体系"、"科技背景"、"加阵营"、"add location" 等时触发。每个 entity 保存为独立 markdown 文件，frontmatter 双向链到 characters 和 plot。
---

# Novel Worldbuilding —— 世界观管理

## 功能

把"世界观"拆成可独立创建、独立维护、互相引用的实体文件：
- **地点（location）**：城市、要塞、荒野、虚拟空间、洞穴...
- **体系（system）**：力量体系 / 政治体系 / 科技体系 / 宗教体系 / 经济体系 / 军事体系 / 社会习俗

每个实体一个 `.md` 文件，frontmatter 标元数据，正文按模板填。所有 entity 通过 `_index.md` 注册表汇总。

## 前置条件

- 必须有 `worldbuilding/_index.md`（说明已 init）
- 建议先跑过 `novel-brainstorm`，让 `story.md` 有题材定位（影响世界观风格）

## 工作流

### 创建一个地点

1. **读取上下文**：
   - `story.md`：拿到 genre / sub-genre / tone，决定地点的整体氛围
   - `worldbuilding/_index.md`：看已有地点，避免重复 / 保持一致
   - 如果是续作 / 同人，还要读 `parent_canon.md`（如有）

2. **问用户基本信息**（用 AskUserQuestion 一次问 2-3 题）：
   - 地点名称（中文 / 英文均可）
   - 类型（城市 / 要塞 / 荒野 / 海岛 / 虚拟空间 / 异空间 / 其他）
   - 在全书中的作用（主舞台 / 阶段性据点 / 一次性场景）

3. **对话补充细节**，覆盖以下要素（不用一次问完，按重要度展开）：
   - 物理描述与氛围
   - 历史（跟主线相关的部分）
   - 居民文化与习俗
   - 注意点（主角会怎么和它互动）
   - 当前状态（故事开始时这地方是什么样）

4. **写文件**：
   - 使用 `references/location-template.md` 作为骨架
   - 文件名 = `{name-kebab}.md`（中文直接用，英文 kebab-case）
   - 路径 = `worldbuilding/locations/{name-kebab}.md`

5. **更新 `worldbuilding/_index.md`** 的地点表

6. **反向链**：如果地点 frontmatter 中列了 `notable-characters`，检查这些角色文件是否存在；不存在则建议用户用 `novel-characters` 创建，已存在则在角色文件的 `locations` 字段加上本地点 ID。

### 创建一个体系

1. **读取上下文**（同地点）

2. **判断体系类型**，参考 `references/world-element-types.md` 中对应类型的引导问题清单：

   | 类型 | 关键问题 |
   |---|---|
   | 力量体系（修真/魔法/超能/科技力） | 来源、获取方式、等级划分、代价 / 副作用、跟世界的兼容性 |
   | 政治体系 | 政体、阶级、权力来源、合法性、内部矛盾 |
   | 科技体系 | 科技水平、突破点、限制、社会接受度 |
   | 宗教体系 | 神祇、教义、组织、与权力的关系 |
   | 经济体系 | 流通物、生产模式、贸易、阶级流动性 |
   | 军事体系 | 武装、战斗逻辑、跟力量体系的关系 |
   | 社会习俗 | 礼仪、禁忌、节日、性别 / 家族 / 年龄观 |

3. **对话补充细节**

4. **写文件**：
   - 使用 `references/system-template.md`
   - 路径 = `worldbuilding/systems/{name-kebab}.md`

5. **更新 `_index.md`** 的体系表

6. **反向链**：如果体系涉及 practitioners（如魔法用户、修真者），在对应角色文件的 `practices` 字段标上本体系。

### 更新一个 entity

1. 读原文件
2. 改 frontmatter 和正文
3. 如果改了 `notable-characters` / `practitioners` / `regions` 等关系字段，对应文件也要更新
4. 改了名字 / 类型 / 状态，更新 `_index.md`

### 跨实体一致性检查（可选，被 `novel-review` 调用）

- 地点引用的角色 → 角色必须存在
- 体系约束的关系（比如"修真只有 9 个境界"）→ 角色卡里的 `cultivation-level` 不应越界
- 力量体系内部一致（比如等级 A 能做的事，等级 B 不应该能做）

这些检查由 `check_consistency.py` 实现（在 `novel-review` 阶段），本 skill 只负责创建。

## 命名约定

- **中文名**：直接用（如 `落雁城.md` / `天枢宗.md`）
- **英文名**：kebab-case（如 `ashen-citadel.md`）
- **避免**：包含 `/`、`:`、`*`、`?` 等文件系统非法字符；如必须，转为全角字符

## 中文长篇网文专属：常见体系类型

详见 `references/world-element-types.md`，包含 9 类常见体系的具体引导问题：

- 修真体系（道术 / 灵根 / 境界）
- 魔法体系（西式 / 东式 / 科学魔法）
- 异能体系（超能力 / 觉醒 / 进化）
- 科技体系（赛博朋克 / 蒸汽朋克 / 硬科幻）
- 武学体系（武侠 / 内功 / 招式）
- 修罗 / 神魔体系
- 体制 / 阶级体系
- 经济 / 资源体系
- 宗教 / 信仰体系

## 与其他 skill 的边界

- **不创建角色**：角色由 `novel-characters` 管。如果对话中涉及角色（比如"这座城的城主是谁"），先在地点 frontmatter 里留 `notable-characters: [-tbd-城主]` 占位，由用户后续用 `novel-characters` 创建。
- **不写卷纲 / 章纲**：那些是 `novel-plot` / `novel-chapter`。
- **不评判世界观好不好**：是用户的世界，不要在创建过程中插嘴"这样设定可能会有 XXX 问题"，除非用户主动问。

## 输出

每次完成创建后：
- 给用户看新写的文件内容
- 提醒下一步可以做什么（继续加地点 / 加体系 / 加角色 / 设计卷纲）
