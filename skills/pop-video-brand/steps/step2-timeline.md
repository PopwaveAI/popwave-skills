# Step 2 · 搭动效时间线（Timeline）

> 目的：把叙事脚本翻译成 HTML 动效时间线（JS 驱动），为本 skill 的技术核心。
> 做完本步，产出 `index.html`，先跑 Step 3 的 preview 校验构图，再决定是否全量渲染。

## 2.1 技术模式（必读 `references/motion-timeline-guide.md`）
- 单页 `<body>` 固定 1920×1080，`overflow:hidden`。
- 所有动效元素绝对定位，用 `window.render(t)`（t 为秒）驱动，只改 `opacity` 与 `transform`。
- 提供 `seg/ease/app/out/slide/set` 辅助函数做缓动插值。
- 逐场景绝对定位坐标基于 1920×1080 网格。

## 2.2 品牌合规（铁律，用 `references/sky-bubble-palette.md`）
- 色板严格用 Sky Bubble：主蓝 `#2F64FF`、泡泡青 `#26D7E8`、波浪紫 `#7B59FF`、主墨 `#141824`、正文 `#343B4D`、画布白 `#FBFDFF`、线框 `#DCE8F2`。
- 中文字体：`"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif`。
- 文案照抄 `叙事脚本.md`，禁止自创。

## 2.3 元素与坐标
- 每场景一个 `.scene` 容器，元素用 `.el`（opacity:0 起步）。
- 产品截图装入圆角卡片（`object-fit:contain`，白底），叠加浮层标签。
- 大标题/卖点/功能矩阵用绝对定位放在右侧信息区（或母版右侧）。
- `left:50%` 居中的元素在 render 里用 `translateX(-50%)` 补正。

## 2.4 时间轴实现
- 在 `render(t)` 里按 `app(t,a,b)`（进场）与 `out(t,a,b)`（出场）组合每元素透明度与位移。
- 功能矩阵等序列元素用循环按 `a+i*step` 逐个点亮。
- 收尾标版吉祥物可加轻微 `Math.sin(t)` 浮动。

## 2.5 常见坑
- `left:50%` 且考验居中时，`translateX` 用 `calc(-50% + Npx)` 微调。
- 避免除零/NaN 变换（折算用进场的 `app()` 值，不直接除）。
- 图片用相对路径（`assets/…`），assets 与 index.html 同目录。

## 产出
`index.html`（自包含单文件）+ `assets/`（拷贝的截图/logo/吉祥物）。

## 传导
- 进入 **Step 3 渲染**：先 `--mode preview` 抓关键帧校验构图与文案，通过后 `--mode full` 全量。