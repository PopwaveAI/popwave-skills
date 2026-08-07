# Step 5: 混音（配音 + 可选 BGM）

> 用完整版 ffmpeg（imageio-ffmpeg）把分句配音按 **时间轴定位** 混入 `成品.mp4`，产出最终带人声的视频。复用 `scripts/mix_audio.py`（本轮实操验证）。

## 输入

- `成品.mp4`（Step 4 产出，无音轨）
- `audio/seg{N}.mp3`（Step 3 配音，逐句）
- 各段配音在视频中的**起始时间**（来自 Step 4 时间轴设计）
- 可选 `bgm.mp3`（背景音乐，无则省略）

## 操作

1. **按时间轴定位混入**（用 `scripts/mix_audio.py`，本质是 ffmpeg adelay+amix）：
   ```bash
   python scripts/mix_audio.py \
     --video 成品.mp4 \
     --audio-dir audio \
     --offsets "seg01.mp3=3.0,seg02.mp3=8.9,seg03.mp3=16.2,..." \
     --out 成品-配音.mp4 \
     [--bgm bgm.mp3 --bgm-vol 0.15 --voice-vol 1.1]
   ```
   - `--offsets` 每项 `文件名=起始秒`，逗号分隔，与配音段落一一对应
   - 每段用 `adelay=起始ms|起始ms` 延迟到对应时间点，`amix` 混合，`volume` 控制响度
   - 无 BGM 时省略 `--bgm`，脚本自动只混配音

2. **probe 校验**：分辨率仍是竖版 1080×1920、时长正确、含 AAC 音轨。

## 产出

- `{项目}/视频/成品-配音.mp4`（最终视频）

## 完成判定

- [ ] 口播清晰，每句配音落在对应画面字幕的时间点
- [ ] BGM（若有）不压人声（0.15）
- [ ] 分辨率/时长/fps 正确，有音轨
- [ ] 最终视频已交付

> 若老板只要文本三件套，本步可跳过。