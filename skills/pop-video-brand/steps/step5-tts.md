# Step 5：TTS 配音（火山语音 · 灿灿默认）

> 用火山语音「豆包语音合成」按口播文案生成人声 MP3，为 Step 6 合成提供配音轨 + 时长。默认音色**知性灿灿 2.0**（温暖专业女声，品宣传播首选）。

## 前置

- 老板已确认 `口播文案`（Step 1 产出，或本步临时确认）
- 火山语音控制台已开通「豆包语音合成大模型」，已有 **X-Api-Key**（新版控制台单头鉴权）
- 若尚无 Key：提示老板到 `https://console.volcengine.com/voice` → 开通豆包语音合成大模型 → 「API Key 管理」复制 X-Api-Key

## 操作

1. **读取口播文案**：从 `叙事脚本.md` 或老板本地确认的文案，拆成逐句（每句对应一个画面/场景段）。

2. **逐句生成**（用 `scripts/tts_generate.py`）：
   ```bash
   python scripts/tts_generate.py \
     --api-key <X-Api-Key> \
     --text "口播句文案" \
     --out "{项目}/audio/seg01.mp3"
   ```
   - 每句一个 `seg{N}.mp3`，命名 `seg01.mp3`...
   - 默认音色已是灿灿（`--speaker` 可换其他音色，如 `zh_female_zhixingnv_uranus_bigtts` 知性女声）
   - 语速/音量/音调可用 `--speech-rate/--loudness-rate/--pitch-rate` 微调

3. **记录每句时长**：用 `imageio-ffmpeg` 的 ffmpeg 或 `ffprobe` 读时长，产出 `时长清单.json`（seq / file / duration_sec）。

## 产出

- `{项目}/audio/seg{N}.mp3`（分句配音）
- `{项目}/audio/时长清单.json`

## 完成判定

- [ ] 每句文案都有对应 mp3
- [ ] 时长清单含全部句的 seq/file/duration
- [ ] 总时长与视频场景时长偏差可接受（口播不超画面太多）

> 失败处理：某句失败只重试该句，不中断整批。重试仍失败则改用 `--speaker` 换备用音色或对文案做口语化微调。