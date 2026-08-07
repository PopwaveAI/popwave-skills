# Step 3 · 逐帧渲染（Render）

> 目的：用 Playwright 把 `index.html` 的动效时间线截成 PNG 帧序列。
> 先 preview 校验，通过后再 full 全量。

## 3.1 抓预览帧（`--mode preview`，铁律）
- 在关键时间点（每场景中途帧 + 收尾定格）抓 8-12 张预览帧。
- 命令：
  ```
  python scripts/render_frames.py --html index.html --out preview \
      --mode preview --times 0.5,2.0,3.5,7.0,9.6,15.0,22.0,28.0,30.0
  ```
- 逐张 Read 审查：构图是否完整协调、文案是否合规对齐、有无元素重叠/溢出/错位。
- 发现布局问题 → 回 Step 2 改 `index.html` 再抓预览，直到通过。

## 3.2 全量渲染（`--mode full`）
- 通过后按总时长×fps 逐帧渲染：
  ```
  python scripts/render_frames.py --html index.html --out frames \
      --mode full --fps 30 --start 0 --end 33
  ```

## 3.3 渲染规范
- 视口 1920×1080，`device_scale_factor=1`。
- fps 默认 30；时长以 `叙事脚本.md` 为准。
- 中间帧放本项目的 `frames/`，不污染素材包。

## 产出
`preview/`（校验帧）+ `frames/f_%05d.png`（全量帧序列）。

## 传导
- 进入 **Step 4 合成**：用 `encode.py` 把帧序列合成 MP4，并校验参数。