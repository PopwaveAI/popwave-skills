# Step 4.5：多模态配图（执行阶段）

> **铁律：此步骤不可跳过、不可绕行、不可用任何理由豁免。**
> 如果 Phase 0 规划了配图但 Step 4.5 未执行 → **整次任务不合格。**

**读什么：** Phase 0 设计简报中的配图规划 + 上游 YAML 数据。

**执行步骤：**
1. 读取上游输入的 YAML 结构化数据
2. 从 YAML 中提取角色的 image_prompt + 名场面的 image_prompt + Hero prompt
3. 创建 `assets/` 目录
4. 遍历 prompt 列表，逐张生图：`python3 scripts/generate_image.py --prompt "[prompt]" --output "assets/{name}.png"`
5. 每张图生成后，转 Base64 Data URL
6. 嵌入 HTML 的 `<img>` 标签
7. 验证所有配图已嵌入（无 `file://` 或相对路径）
8. 删除 `assets/` 目录

**Prompt 来源规则：**
| 配图用途 | prompt 来源 | 谁写的 |
|:---------|:-----------|:-------|
| 角色肖像 | YAML 中该角色的 image_prompt 字段 | **上游 skill** |
| 名场面插图 | YAML 中该场景的 image_prompt 字段 | **上游 skill** |
| Hero 背景 | 从素材标题/描述/情绪自动合成 | **本 skill** |
| 装饰性配图 | 从素材整体氛围自动合成 | **本 skill** |

**图片嵌入规则：**
```html
<!-- 错误：文件路径引用（双击无法看到图片） -->
<img src="assets/hero.png" alt="">

<!-- 正确：Base64 Data URL 嵌入 -->
<img src="data:image/png;base64,iVBORw0KGgo..." alt="英雄形象">
```

**Hero 图三层叠图法（必须使用）：**
```html
<div class="banner" style="--bg-img: url('data:image/png;base64,...')">
  <!-- Layer 0：同图放大+blur 做兜底背景 -->
  <!-- Layer 1：正图，radial-gradient mask 让边缘消散 -->
  <img src="data:image/png;base64,..." alt="...">
  <!-- Layer 2：底部渐变到背景色，文字可读 -->
  <div class="banner-overlay">
    <h1>标题</h1>
    <p>副标题</p>
  </div>
</div>
```

**铁律：**
1. 数量不达标 → 不合格
2. 用 GenerateImage 工具/placeholder SVG/纯色块代替 → 不合格
3. 生图失败跳过不嵌入 → 不合格（用脚本内置 SVG 占位图兜底）
4. 引用 `src="assets/..."` 文件路径 → 不合格
5. Step 4.5 新增/删除 Phase 0 规划的配图 → 不合格

**产出：** 所有配图的 Base64 Data URL + 嵌入 HTML。

**门禁：** 见上方铁律 5 条，任一条不通过 → 整次不合格。
