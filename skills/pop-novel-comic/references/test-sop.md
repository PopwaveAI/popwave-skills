# 漫画 Skill 测试 SOP

> 两条产出路径的测试标准操作流程。Phase 1 Step 2 产出阶段，根据需求选择路径并执行对应测试。

## 两个方案总览

| 维度 | 方案A：Seedream 直出整页 | 方案B：逐帧生成 + Pillow 拼图 |
|:-----|:----------------------|:----------------------------|
| 原理 | 一次 API 调用生成整页漫画（含多格+排版） | 逐帧调用 API → Pillow 像素级拼合 |
| API 调用次数 | 1 次/页 | N 次（N=帧数） |
| 耗时 | ~30 秒/页 | ~2-3 分钟/章（8帧） |
| 排版控制 | 模型自主决定，提示词+草图引导 | 像素级精确，JSON 配置驱动 |
| 角色一致性 | 跨格一致性差（模型在同一张图里画同一角色容易漂移） | 高（每帧独立引用定妆图） |
| 文字叠加 | 模型渲染（不可控，经常乱码） | Pillow 精确叠加（caption 字段） |
| 布局精度 | 取决于模型理解，有留白/错位风险 | 零留白、严丝合缝 |
| 适用场景 | 快速验证、概念草图、不需要精确排版 | 正式产出、连载质量要求 |

> **默认方案：B（逐帧生成 + Pillow 拼图）**。方案A 仅用于快速验证画风/角色适配性，不作为正式产出路径。

## 方案A：Seedream 直出整页

### 适用场景

- Phase 0 画风验证：快速看 Seedream 能否在本赛道画出合格的漫画页
- 角色定妆图验证：看角色在漫画页中的整体效果
- 概念草图：给用户快速预览章节效果
- **不用于正式连载产出**

### 测试流程

#### 1. 准备素材

- 角色定妆图（Phase 0 产出，`assets/characters/char-{名}-v1.png`）
- 章节关键信息（从导演卡提取，3-5 条核心信息即可）

#### 2. 编写提示词

直出提示词结构：

```
[Seedream 执行串]

A complete single-page manga / comic page with {N} panels.
This is ONE whole manga page, NOT a single illustration.
{故事背景一句话}。
Reading order: left-to-right, top-to-bottom.
Clear panel borders with solid black gutters between panels.
Consistent character appearance across ALL panels: {角色锚点串}。

PANEL LAYOUT ({N} panels, {M} rows):
- Row 1: Panel 1 (left half) and Panel 2 (right half).
- Row 2: Panel 3 (FULL WIDTH, LARGEST).
...

PANEL CONTENTS:
Panel 1: {画面描述}
Panel 2: {画面描述}
...

Render full-color detailed manga art inside every panel.
Each panel must contain a distinct scene; do NOT blend panels into one image.
Keep character face and costume identical in every panel where he appears.

[风格保真约束]
```

#### 3. 草图引导（可选但推荐）

用 Pillow 生成灰度布局草图作为参考图，帮助模型理解格子分割：

- 每格标注序号 + 内容关键词
- 灰度填充 + 黑色边框
- 格子大小按重要性分配（名场面最大）

参考图顺序：`[角色定妆图, 灰度草图]`

#### 4. 调用 API

```
模型：doubao-seedream-5-0-pro-260628
尺寸：1728x2304（竖版整页）
response_format：b64_json
参考图：[角色定妆图, 草图]（草图可选）
```

#### 5. 质量评估

| 检查项 | 达标标准 | 不达标处理 |
|:-------|:---------|:-----------|
| 格子分割 | 能看出明确的格子边界和阅读顺序 | 提示词增加布局描述，或加草图 |
| 角色一致性 | 同一角色在多格中面貌可辨识 | 加角色定妆图参考，减少角色出场格数 |
| 画面质量 | 画风符合锚定串，无概念艺术漂移 | 检查风格保真约束是否在末尾 |
| 文字渲染 | 无明显乱码（允许不完美） | 文字交给方案B的 caption 处理 |
| 构图完整 | 每格有独立场景，未融为一体 | 提示词强调 distinct scene |

### 已知限制

- **格子数 ≤ 8**：超过 8 格模型容易把多格融成一张大图
- **角色一致性不保证**：同一角色在 3 格以上出现时面部漂移概率高
- **文字不可控**：模型经常生成无意义英文/乱码文字
- **布局不精确**：即使有草图引导，格子大小和位置仍有偏差

## 方案B：逐帧生成 + Pillow 拼图

### 适用场景

- 正式连载产出（默认路径）
- 需要精确排版和文字叠加
- 角色一致性要求高

### 测试流程

#### 1. 前置条件

- Phase 0 已完成：角色库 + 定妆图 + 画风冻结
- Phase 1 Step 1 已完成：导演卡含分格设计表
- 分镜脚本表已编写：每帧有提示词、定妆图版本、布局类

#### 2. 逐帧生成

使用 `generate_storyboard.py` 批量生成：

1. 配置 `FRAMES` 列表（每帧 id + prompt）
2. 配置 `FRAME_REFS`（每帧的角色定妆图+场景主镜映射）
3. 执行批量生成

```powershell
$env:ARK_API_KEY="{API_KEY}"
python "{本skill路径}/scripts/generate_storyboard.py"
```

**帧质量检查**（每帧生成后立即检查）：

| 检查项 | 达标标准 | 不达标处理 |
|:-------|:---------|:-----------|
| 格式正确 | magic bytes 为 `89 50 4E 47`（真PNG） | 脚本自动转码，检查 ensure_png_format 是否执行 |
| 角色一致 | 面部/发型/服装与定妆图可辨识 | 检查提示词是否以 Seedream 执行串开头 |
| 画风一致 | 半厚涂/赛璐璐等画风无漂移 | 检查风格保真约束是否在提示词末尾 |
| 场景一致 | 同场景多帧的空间/光源一致 | 检查场景主镜是否作为参考图传入 |
| 画面质量 | 无残肢/多指/严重变形 | 提示词加 HARD CONSTRAINTS 禁止项 |

#### 3. 编写拼图配置

创建 `第{N}章/拼图配置.json`：

```json
{
  "title": "{书名}",
  "subtitle": "第{N}章 · {章节名}",
  "frames_dir": "{漫画项目}/第{N}章/output",
  "output": "{漫画项目}/第{N}章/漫画-{章节名}.jpg",
  "output_format": "jpeg",
  "jpeg_quality": 92,
  "footer": "popwave",
  "frames": [
    {"file": "frame1.png", "layout": "full",   "position": "center 15%", "caption": "旁白文字"},
    {"file": "frame2.png", "layout": "full",   "position": "center"},
    {"separator": "line"},
    {"file": "frame3.png", "layout": "scene",  "position": "center",     "caption": "名场面旁白", "style": "feature"},
    {"file": "frame4.png", "layout": "half",   "position": "center 25%", "caption": "旁白"},
    {"file": "frame5.png", "layout": "half",   "position": "center",     "caption": "旁白"},
    {"separator": "line"},
    {"file": "frame8.png", "layout": "hook",   "position": "center 55%", "caption": "钩子文字", "style": "hook"}
  ]
}
```

**配置检查清单**：

- [ ] frames 数组覆盖分镜脚本表的全部帧
- [ ] 每帧 layout 值与分格设计表布局类对应
- [ ] half 帧成对出现（连续两个 half 自动配对）
- [ ] separator 对应页面设计表的页面边界
- [ ] caption 文字从导演卡旁白文案复制
- [ ] position 根据画面主体位置调整（人物在上→`center 20%`，在下→`center 80%`）

#### 4. 执行拼图

```powershell
python "{本skill路径}/scripts/assemble_comic.py" "{漫画项目}/第{N}章/拼图配置.json"
```

#### 5. 拼图质量评估

| 检查项 | 达标标准 | 不达标处理 |
|:-------|:---------|:-----------|
| 零留白 | 每帧完全填充目标区域，无白色/背景色缝隙 | 检查 cover_crop 是否正确执行 |
| 严丝合缝 | 帧间间距均匀（GUTTER=4px），无错位 | 检查 JSON 配置的帧顺序 |
| 布局类正确 | full 全宽 / half 并排 / scene 更大 / hook 暗角 | 检查 layout 值与分格设计表对应 |
| position 合理 | 画面主体未被裁掉 | 调整 position 值（center 15%/30%/55%等） |
| caption 可读 | 旁白文字清晰、不遮挡画面主体 | 调整 caption 文字长度，或拆为多帧 |
| 文件大小 | JPEG 100KB-2MB | 调整 jpeg_quality（默认92） |
| 标题/页脚 | 书名+章节名居中，popwave 页脚可见 | 检查 title/subtitle/footer 字段 |

#### 6. 进入 Phase 2 审核

拼图完成后，自动进入 `step3-review.md` 执行视觉审核+记忆沉淀。

## 方案选择决策树

```
需求是什么？
├─ 快速验证画风/角色 → 方案A（直出，1次调用）
├─ 给用户看概念效果 → 方案A（直出，可加草图）
├─ 正式连载产出 → 方案B（逐帧+拼图，默认）
└─ 需要精确文字/排版 → 方案B（唯一选择）
```

## 测试项目结构

```
{测试项目}/漫画/
├── assets/characters/           # 定妆图
├── 漫画角色库.md
├── 漫画快照.md
├── 漫画状态.md
├── 视觉沉淀.md
├── 第1章/
│   ├── 导演卡.md
│   ├── storyboard.md
│   ├── 拼图配置.json             # 方案B
│   ├── output/
│   │   ├── frame1~8.png         # 方案B 逐帧产出
│   │   └── test_seedream_variants.py  # 方案A 测试脚本（可选）
│   └── 漫画-{章节名}.jpg         # 最终产出
```

## 常见问题

**Q: 方案A 能否替代方案B？**
不能。方案A 的角色一致性、排版精度、文字叠加均不达标，仅适合快速验证。

**Q: 能否先方案A 验证再方案B 产出？**
可以。Phase 0 用方案A 快速验证画风，通过后切换方案B 正式产出。两方案共用角色定妆图和画风锚定串。

**Q: 方案B 的 position 怎么调？**
先生成帧后看帧画面——主体在上半部用 `center 20%`，在下半部用 `center 80%`，居中用 `center`。默认 `center` 对大多数帧够用。

**Q: half 帧必须成对吗？**
是。连续两个 `layout: "half"` 自动配对并排。单独 half 会警告并当全宽处理。

**Q: 超过 8 格怎么办？**
拼图配置的 frames 数组长度不限。用 `separator` 分隔页面边界保持阅读节奏。建议每页 6-10 格。
