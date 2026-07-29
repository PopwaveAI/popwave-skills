# Step 1: 单章生成

> 读状态+角色库 → 拆分镜 → 门禁A → 按帧映射定妆图生成 → HTML组装+内联化

## 设计哲学

Phase 1 是循环执行的核心环节。每章生成都从读取记忆文件开始——漫画状态.md 告诉 Agent"上一章画到哪、角色有什么变化"，漫画角色库.md 提供"定妆图路径+冻结提示词"。

**角色一致性靠引用冻结提示词保证**，不靠重新组装。每帧的角色描述部分直接从角色库复制冻结提示词，加上场景动作描述和风格锚定串即可。

## 1. 读取记忆文件

### 必读文件

| 文件 | 读什么 |
|:-----|:-------|
| 漫画状态.md | 当前章位、角色外观变化、上一章视觉问题、本章注意事项 |
| 漫画角色库.md | 所有角色的定妆图路径（`assets/characters/char-{名}-v{N}.png`）和冻结提示词 |
| 漫画快照.md | 风格锚定串（全系列冻结）、已生成章节清单 |

### 角色定妆图版本选择

读角色库的定妆图资产表，选择每个角色的**最新版本**。如果状态文件标注了角色在本章有外观变化，需在步骤 4 处理增量定妆图。

## 2. 读取章节原文

读取用户指定的章节文件：
- `正文/ch{NNN}.txt` 或 `正文/ch{NNN}.md`

## 3. 拆分镜脚本

从章节中拆出 6-8 个关键帧。**参考 `references/storyboard-guide.md`** 了解选帧方法论。

### 分镜脚本表格式

每帧必须标注出场角色和对应的定妆图版本：

| 帧号 | 场景 | 角色动作 | 机位 | 情绪 | 出场角色 | 定妆图版本 | 对白/文字 | 画面提示词 |
|:-----|:-----|:---------|:-----|:-----|:---------|:-----------|:---------|:-----------|
| 1 | 破屋，雨夜 | 薇薇安从米袋抓米 | 全景 | 压抑 | 薇薇安 | char-vivian-v1 | 旁白:没有食物了 | [提示词] |
| 2 | 破屋灶台 | 薇薇安抱老狗 | 中近景 | 温暖 | 薇薇安 | char-vivian-v1 | 对白:又不会偷东西 | [提示词] |

### 提示词组装规则

每格提示词结构：

```
[冻结提示词中的角色描述部分] + [角色动作描述] + [场景环境描述] + [风格锚定串]
```

**关键**：角色描述部分**从角色库的冻结提示词直接复制**，不重新组装。只追加场景和动作描述。

示例（索伦醒来帧）：
```
# 从角色库复制的冻结提示词角色描述：
一个18岁的瘦削男性角色，病后初愈的虚弱体态，亚麻色短发微乱，黑色眼眸，穿破旧亚麻衬衫赤脚，苍白面色，锁骨突出。
# 追加的场景和动作：
年轻男子在床上缓缓睁开眼睛，黑色眼眸初见光明。床边小女孩泪水决堤扑入他怀中。晨曦般的微光从门缝透入。
# 追加的风格锚定串：
暗黑奇幻半写实日式漫画风格，水彩质感笔触，灰暗色调转为暖色光晕，希望温暖的情绪氛围。
```

> 无角色帧（纯环境/特写）不需要参考图和角色描述，直接写场景提示词 + 风格锚定串。

## 4. 🚪 门禁A：分镜确认

向用户呈现分镜脚本表（含每帧的出场角色+定妆图版本）。用户确认后继续。

## 5. 角色外观变化检查

检查本章是否有角色外观变化（换装/受伤/变身等）：

- **无变化** → 使用现有最新版本定妆图
- **有变化** → 执行增量定妆图生成：
  1. 基于角色的冻结提示词 + 变化描述，组装新提示词
  2. 调用 `scripts/update_char_asset.py` 生成新版本定妆图
  3. 新定妆图保存到 `assets/characters/char-{名}-v{N+1}.png`
  4. **新提示词冻结到角色库**（作为 v{N+1} 的冻结提示词）
  5. 记录到角色库的增量定妆表和决策日志

```powershell
python "{本skill路径}/scripts/update_char_asset.py" `
  --char-name "{角色名}" `
  --version {N+1} `
  --base-prompt "{冻结提示词}" `
  --change-desc "{变化描述}" `
  --output "{漫画项目}/assets/characters/char-{名}-v{N+1}.png"
```

## 6. 逐格分镜生成

### 批量生成（推荐）

配置 `generate_storyboard.py` 的 `FRAMES` 列表和 `FRAME_REFS`（按帧映射角色参考图）：

```python
# 按帧映射角色定妆图（支持多角色同帧选主要角色）
FRAME_REFS = {
    "frame1": "assets/characters/char-vivian-v1.png",
    "frame2": "assets/characters/char-vivian-v1.png",
    "frame3": "assets/characters/char-vivian-v1.png",
    "frame4": "assets/characters/char-vivian-v1.png",  # 索伦昏迷，用薇薇安参考
    "frame5": "assets/characters/char-vivian-v1.png",
    "frame6": None,  # 无角色帧
    "frame7": "assets/characters/char-vivian-v1.png",
    "frame8": "assets/characters/char-soren-v1.png",   # 索伦醒来，用索伦参考
}
```

```powershell
$env:ARK_API_KEY="{API_KEY}"
python "{本skill路径}/scripts/generate_storyboard.py"
```

### 单格生成

```powershell
python "{pop-novel-visual路径}/scripts/generate.py" image `
  --prompt '{分镜提示词}' `
  --model doubao-seedream-5-0-lite-260128 `
  --size 1728x2304 `
  --image "data:image/png;base64,{角色定妆图base64}" `
  --output "第{N}章/output/frame{N}.png"
```

## 7. HTML 漫画页组装

读取 `templates/comic-page.tpl.html`，替换占位符，组装漫画页面。

详见模板文件中的占位符说明。布局原则：Grid 2列，全宽格和半宽格交替。对白气泡用 CSS 定位叠加。

输出到 `{漫画项目}/第{N}章/漫画-{章节名}.html`

## 8. HTML 图片内联化（必须执行）

```powershell
python "{本skill路径}/scripts/inline_html.py" "{漫画项目}/第{N}章/漫画-{章节名}.html"
```

> 内联化后 HTML 在浏览器和 popwave 中均能正常显示。

## 9. 进入 Phase 2

单章生成完成后，自动进入 Phase 2（读取 `steps/step2-review.md`）执行视觉审核和记忆沉淀。
