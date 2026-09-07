---
name: novel-characters
description: 管理小说角色资产 —— 角色卡、关系图谱、家族 / 阵营树、动态角色状态（卷级职责 / 缺席风险 / 候选新角色）。当用户说"加角色"、"加主角"、"加反派"、"创建一个角色"、"角色关系"、"建家族树"、"add character" 时触发。每个角色一个 markdown 文件，frontmatter 维护双向关系。
---

# Novel Characters —— 角色管理

## 功能

把"小说角色"拆成可独立创建 / 维护 / 引用的实体文件：
- **角色卡**：每个角色一个 `.md` 文件，包含外貌、性格、动机、声音、弧线、关键事件
- **关系图谱**：frontmatter 中的 `relationships` 字段双向维护
- **家族 / 阵营树**：维护在 `characters/_index.md` 的对应段
- **动态角色资产**（借鉴 AI-NWA）：标注每个角色在当前卷的职责、缺席风险、候选替补

## 前置条件

- `characters/_index.md` 存在（init 已建）
- `story.md` 至少有 frontmatter（提供 genre / tone 上下文）

## 工作流

### 创建一个角色

1. **读取上下文**：
   - `story.md`：genre / sub-genre / pov / tone
   - `characters/_index.md`：已有角色，避免重名 / 保持声音差异
   - 如果角色绑定到某地点 / 体系，读对应的 `worldbuilding/` 文件

2. **问基本信息**（用 AskUserQuestion 一次问 2-3 题）：
   - 角色名（中文 / 英文）
   - 角色定位：protagonist / antagonist / supporting / minor / cameo
   - 在故事中的作用：（叙述焦点 / 推动情节 / 提供信息 / 制造冲突 / 情感锚点）

3. **对话补充细节**（按下面顺序，但允许跳跃）：

   **A. 外貌与可识别特征**
   - 不要列一堆形容词；只列 3-5 个"读者一眼记住"的特征
   - 例：身高、独特服饰、伤疤、口头禅

   **B. 性格与缺陷**
   - 性格不写"善良勇敢"这种空话
   - 写**矛盾感**：一个明确的强项 + 一个会被这个强项害到的弱点
   - 例："信任直觉到固执的程度（强项 = 决断快 / 弱点 = 容易被骗）"

   **C. 背景故事**
   - 只写跟主线相关的部分
   - 关键节点：出生 / 主要变故 / 现在为什么是这样

   **D. 动机与目标**（4 层）
   - **外在目标**（想要什么）
   - **内在需要**（实际缺少什么）—— 通常跟外在目标矛盾
   - **核心恐惧**（最怕什么）
   - **道德盲点**（不愿承认自己的什么）

   **E. 声音与说话方式**
   - 句长偏好（短 / 长）
   - 用词偏好（正式 / 口语 / 方言 / 带梗）
   - 沉默时机
   - **必填**：至少 2 句典型对话作示范

   **F. 角色弧线**
   - 起点状态（章节 X 时是什么样）
   - 转折点（哪一卷 / 哪个事件让他变）
   - 终点状态（全书结束时变成什么）

   **G. 关键时间线事件**（可少量）

4. **写文件**：
   - 使用 `references/character-template.md`
   - 文件名 = `{name-kebab}.md`
   - 路径 = `characters/{name-kebab}.md`

5. **更新 `characters/_index.md`** 的角色表 + 关系图（如果加了关系）

6. **双向链**：
   - 如果 frontmatter 中列了 `relationships: [{character: x, type: sibling}]`，去 `characters/x.md` 也加上反向关系（关系类型表见 `references/relationship-types.md`）
   - 如果列了 `locations / linked-systems / arcs`，去对应文件加反向引用

### 更新一个角色

1. 读原文件
2. 改 frontmatter / 正文
3. 关系改了 → 对方文件也要改
4. role / status 改了 → 更新 `_index.md`

### 关系管理

详见 `references/relationship-types.md`，含完整的关系类型对照表 + 反向对应。

加关系时：
1. 在 A 的 frontmatter 加 `{character: B, type: X}`
2. 在 B 的 frontmatter 加 `{character: A, type: inverse(X)}`
3. 在 `characters/_index.md` 的关系图段加一行

### 家族树 / 阵营图

维护在 `characters/_index.md` 的 `## 家族 / 阵营` 段。格式：

```markdown
### {家族 / 阵营名}
- **{角色名}** ({status}) - [[{name-kebab}]]
  - **{子辈名}** - [[{name-kebab}]]
  - **{子辈名}** - [[{name-kebab}]]
```

### 动态角色状态（v0.2+，可选）

借鉴 AI-NWA 的"动态角色资产"概念，每个角色卡可以追加：

```yaml
volume-1:
  responsibility: "推进主线 - 与反派的第一次正面冲突"
  absence-risk: low      # low / med / high (久不出场的话有什么后果)
  appearance-target: 8   # 本卷计划出场章数
  appearance-actual: 0   # 实际出场（每章更新）
```

v0.1 暂不强制，但 schema 已留好（写入 character-template.md）。

## 命名约定

- 中文小说：角色名用中文（孟九 / 江流儿 / 萧炎）
- 英文小说：kebab-case（sera-voss / kael-voss）
- 别名 / 化名：写在 `aliases:` 字段，不单独建文件

## 与其他 skill 的边界

- **不创建地点 / 体系**：那是 `novel-worldbuilding`。如对话中涉及地点 / 体系，先在角色 frontmatter 留 `linked-locations / practices` 占位 + 临时 ID。
- **不写卷纲 / 章纲 / 章节正文**
- **不评判人设好不好**：除非用户主动问"这角色立得住吗"，否则不要插嘴
- **不做"自动提取出场人物"**：那是 `novel-memory` 在 post-write 阶段的事

## 输出

每次完成创建后：
- 给用户看新写的文件内容（含 frontmatter 和正文）
- 提醒下一步可以做什么
