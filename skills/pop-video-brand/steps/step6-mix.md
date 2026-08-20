# Step 6：混音合成（配音 + 可选 BGM + 视频）

> 把 Step 5 的配音轨（+可选 BGM）混入 Step 4 合成的视频，输出带人声的最终 MP4。用完整版 ffmpeg（imageio-ffmpeg）做多路音频混流。

## 前置

- Step 4 已产出 `成品.mp4`（无音轨或纯 BGM 版）
- Step 5 已产出 `audio/seg{N}.mp3` + `时长清单.json`
- 可选 BGM 文件（老板已选定，否则跳过 BGM 只配音）

## 操作

1. **拼接配音轨**：按 `时长清单.json` 顺序，用 ffmpeg `concat` 把 `seg*.mp3` 拼成一条完整 `narration.wav`（句间可加 0.2-0.4s 静音呼吸）。

2. **混音**（用完整版 ffmpeg）：
   ```
   ffmpeg -y \
     -i 成品.mp4 -i narration.wav [-i bgm.mp3] \
     -filter_complex [三路音量/淡入淡出/叠加] \
     -map 0:v -map [mix] -c:v copy -c:a aac -b:a 192k \
     -shortest 成品-配音.mp4
   ```
   - 口播音量 1.0，BGM 音量 0.3-0.5（不盖人声）
   - BGM 做淡入淡出（开头 0.8s 淡入，结尾 2.5s 淡出）
   - 口播按场景时间轴对齐画面（若需要精确对齐，用 `adelay`/`amix` 逐句定位）

## 产出

- `{项目}/成品-配音.mp4`（最终交付）

## 完成判定

- [ ] 视频 + 口播 + BGM 三轨混音正常
- [ ] probe 校验：分辨率 1920×1080、时长正常、有音轨
- [ ] 试听确认口播清晰、BGM 不压人声

> 精确对齐技巧：若口播需卡特定画面，用 `adelay=ms|ms` 为每句配音设置起始偏移，再 `amix` 合成。品宣口播通常整段铺在画面上即可，不必逐字卡点。