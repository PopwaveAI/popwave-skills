# Step 5: 混音（配音 + BGM 选曲植入）

> 用完整版 ffmpeg（imageio-ffmpeg）把分句配音按 **时间轴定位** 混入 `成品.mp4`，并按 `references/bgm-guide.md` **挑选并植入 BGM**，产出最终带人声的视频。复用 `scripts/mix_audio.py`（本轮实操验证）。

## 输入

- `成品.mp4`（Step 4 产出，无音轨）
- `audio/seg{N}.mp3`（Step 3 配音，逐句）
- 各段配音在视频中的**起始时间**（来自 Step 4 时间轴设计）
- 可选 `bgm.mp3`（背景音乐，无则省略）

## 操作

> 落盘命名遵循 `pop-visual-pipeline/references/落盘规范.md` §3.1b：成品视频版本化+`-final`。

1. **选曲（BGM 能力）**：按漫画**赛道** + 主要**情绪段**，从 `references/bgm-guide.md` 的「赛道 × 情绪 → 参考曲目」表选定 BGM。示例：悬疑赛道钩子段可配 `青衣`（国风戏腔悬疑感），紧张/高潮段可配 `fever pitch`（电子狂热感）。把 BGM 文件放到 `{项目}/视频/bgm/bgm-*.mp3`。

2. **按时间轴定位混入**（用 `scripts/mix_audio.py`，本质是 ffmpeg adelay+amix）：
   ```bash
   python scripts/mix_audio.py \
     --video 第{N}章-v1.mp4 \
     --audio-dir audio \
     --offsets "seg01.mp3=3.0,seg02.mp3=8.9,seg03.mp3=16.2,..." \
     --out 第{N}章-配音-v1-final.mp4 \
     [--bgm {项目}/视频/bgm/bgm-悬疑-青衣.mp3 --bgm-vol 0.15 --voice-vol 1.1]
   ```
   - `--offsets` 每项 `文件名=起始秒`，逗号分隔，与配音段落一一对应
   - 每段用 `adelay=起始ms|起始ms` 延迟到对应时间点，`amix` 混合，`volume` 控制响度
   - 有 BGM 时传 `--bgm`（音量 0.15 循环铺满全程、不盖人声）；无 BGM 时省略，脚本自动只混配音

3. **probe 校验**：分辨率仍是竖版 1080×1920、时长正确、含 AAC 音轨。

## 产出

- `{项目}/视频/第{N}章-配音-v{版本}-final.mp4`（最终视频，确认后交付）
- `{项目}/视频/第{N}章-v{版本}.mp4`（Step 4 无音轨中间版，进 `_过程/` 或保留为候选）
- `{项目}/视频/bgm/bgm-*.mp3`（选定的 BGM）

## 完成判定

- [ ] 已按赛道 × 情绪选定 BGM（若需要），曲目与漫画风格匹配
- [ ] 口播清晰，每句配音落在对应画面字幕的时间点
- [ ] BGM（若有）不压人声（0.15），强弱贴合情绪段
- [ ] 分辨率/时长/fps 正确，有音轨
- [ ] 最终视频已交付

> 若老板只要文本三件套，本步可跳过。若老板已指定 BGM，直接用老板给的曲目，不重新选。