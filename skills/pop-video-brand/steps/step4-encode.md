# Step 4 · 合成 MP4（Encode）

> 目的：用完整版 ffmpeg 把帧序列合成 H.264 MP4，并校验成片参数。

## 4.1 编码
- 用 `imageio-ffmpeg` 自带的完整版 ffmpeg（含 libx264，能处理标准 PNG）。
- 命令：
  ```
  python scripts/encode.py --frames frames --out 成品.mp4 --fps 30 --crf 18
  ```

## 4.2 校验成片（铁律）
- 用完整版 ffmpeg probe 成片，核对：
  - 分辨率 1920×1080、fps 30、时长 = 总时长、H.264 + yuv420p、movflags faststart。
- 用 `ffmpeg -i 成品.mp4` 读 Duration / Stream 行确认。
- 时长对不上（帧数=时长×fps ±1）说明 timeline 边界有误，回查 Step 2。

## 4.3 交付
- 成片放到用户指定目录（默认 `d:\popwave-skills\`）。
- 提供本地预览页（`<video controls>` 内嵌成片）便于老板直接看。

## 产出
`成品.mp4`。全流程结束。