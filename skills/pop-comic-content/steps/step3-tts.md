# Step 3: TTS 配音（火山灿灿）

> 用火山语音「豆包语音合成」按口播文案生成人声 MP3，为出片提供配音轨 + 时长。默认音色**知性灿灿 2.0**。复用 pop-video-brand 的 `scripts/tts_generate.py`。若老板只要文本三件套，本步可跳过。

## 前置

- 老板已确认 `口播脚本.md`（Step 2 产出）
- 火山语音控制台已开通「豆包语音合成大模型」，已有 **X-Api-Key**
- **Key 已固化在 skill 里**：`scripts/.env` 写入 `VOLC_ARK_API_KEY=<X-Api-Key>`（脚本自动读取，运行无需手动传 key）。若该文件不存在，复制 `scripts/.env.example` 为 `.env` 并填入真实 key
- 若老板尚未提供 key：提示到 `https://console.volcengine.com/voice` → 开通豆包语音合成大模型 → 「API Key 管理」复制 X-Api-Key，填入 `scripts/.env`

## 操作

1. **读取口播文案**：从 `口播脚本.md` 拆成逐句（每句对应一个场景/页）。

2. **逐句生成**（用 `scripts/tts_generate.py`，复用 brand 的火山方案）：
   ```bash
   python scripts/tts_generate.py \
     --text "口播句文案" \
     --out "{项目}/视频/audio/seg01.mp3" \
     --speech-rate 20
   ```
   > key 自动读取，无需传 `--api-key`。读取优先级：命令行 `--api-key` > 环境变量 `VOLC_ARK_API_KEY` > `scripts/.env`。若三种都缺，脚本会报错并提示配置方式。
   - 每句一个 `seg{N}.mp3`
   - 默认音色已是灿灿（`--speaker` 可换其他音色，如 `zh_female_zhixingnv_uranus_bigtts` 知性女声）
   - **统一 `--speech-rate +20`**（v0.8 铁律）：全批固定同一语速，避免逐句独立合成导致的语速不均/偏慢。必要时 `--loudness-rate/--pitch-rate` 微调

3. **记录每句时长**：用 imageio-ffmpeg 的 ffmpeg 或 ffprobe 读时长，产出 `时长清单.json`（seq / page / file / duration_sec / text / emotion）。

## 产出

- `{项目}/视频/audio/seg{N}.mp3`（分句配音）
- `{项目}/视频/audio/时长清单.json`

## 完成判定

- [ ] 每句文案都有对应 mp3
- [ ] 时长清单含全部句的 seq/page/file/duration_sec
- [ ] 总时长与每页场景时长偏差可接受（口播不超画面太多）

> 失败处理：某句失败只重试该句，不中断整批。重试仍失败则改用 `--speaker` 换备用音色或对文案做口语化微调。