# Step 3: TTS 配音（火山灿灿）

> 用火山语音「豆包语音合成」按口播文案生成人声 MP3，为出片提供配音轨 + 时长。默认音色**知性灿灿 2.0**。复用 pop-video-brand 的 `scripts/tts_generate.py`。若老板只要文本三件套，本步可跳过。

## 前置

- 老板已确认 `口播脚本.md`（Step 2 产出）
- 火山语音控制台已开通「豆包语音合成大模型」，已有 **X-Api-Key**
- **Key 已固化在 skill 里**：`scripts/.env` 写入 `VOLC_ARK_API_KEY=<X-Api-Key>`（脚本自动读取，运行无需手动传 key）。若该文件不存在，复制 `scripts/.env.example` 为 `.env` 并填入真实 key
- 若老板尚未提供 key：提示到 `https://console.volcengine.com/voice` → 开通豆包语音合成大模型 → 「API Key 管理」复制 X-Api-Key，填入 `scripts/.env`

## 操作

1. **读取口播文案**：从 `口播脚本.md` 拆成逐句（每句对应一个场景/页），并**在每句前嵌入情绪指令**（全角括号 `（低沉，恐惧地）` `（松了口气，温暖）` `（神秘，压低）` 等）。封面钩子句配 `（低沉，神秘地）`。seed-audio-1.0 是自然语言驱动的音频大模型，括号指令用于调节语气节奏且**不会被念出来**（ASR 验证过）。

2. **整段合成**（用 `scripts/tts_generate.py`，复用 brand 的火山方案），把含情绪指令的全文一次送入：
   ```bash
   python scripts/tts_generate.py \
     --text "$(cat 口播全文含情绪指令.txt)" \
     --out "{项目}/视频/audio/v{版本}/full_voice.mp3" \
     --speech-rate 5
   ```
   > key 自动读取，无需传 `--api-key`。读取优先级：命令行 `--api-key` > 环境变量 `VOLC_ARK_API_KEY` > `scripts/.env`。若三种都缺，脚本会报错并提示配置方式。
   - **整段一次合成**（含封面钩子句 + 正文全部），避免逐句拼接割裂/语速不均
   - 默认音色已是灿灿（`--speaker` 可换其他音色，如 `zh_female_zhixingnv_uranus_bigtts` 知性女声）
   - **统一 `--speech-rate +5`**（v0.11 终稿）：+8 仍偏快且抹平情绪，+5 更从容自然，让情绪指令有发挥空间。必要时 `--loudness-rate/--pitch-rate` 微调

3. **ASR 对齐**：用 faster-whisper（small, word_timestamps）对整段音频做词级时间戳，并按**纯文本（去掉情绪指令）**的汉字序列映射到每句，产出 `audio/v{版本}/对齐.json`（seq / start / end / duration / text）。封面句为 seq0，正文各段依次。
   - 对齐用纯文本，因为情绪指令不进语音、不占时长

## 产出

- `{项目}/视频/audio/v{版本}/full_voice.mp3`（整段配音，含情绪表现）
- `{项目}/视频/audio/v{版本}/对齐.json`（seq / start / end / duration / text）

## 完成判定

- [ ] 整段配音一次合成成功（无逐句拼接割裂）
- [ ] 对齐.json 含全部句（封面 seq0 + 正文各段）的 seq/start/end/duration
- [ ] 语速 +5，情绪指令生效（听感有起伏变化，无指令被念出）
- [ ] 总时长与每页场景时长偏差可接受（口播不超画面太多）

> 失败处理：整段合成失败重试整段；反复失败则改用 `--speaker` 换备用音色，或对文案情绪指令做口语化微调。