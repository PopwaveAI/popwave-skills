# Step 3: TTS 配音

> 用 `edge-tts` 按脚本逐句生成人声，记录每句时长。为 Step 4 对齐提供时长清单。

## 前置

- 老板已确认 `口播脚本.md`（Step 2 闸门通过）
- `pip install edge-tts`（免费，无需 API Key）

## 操作

1. **读取已确认的 `口播脚本.md`**，提取所有口播句（含 seq + page 绑定）。

2. **用 `scripts/tts_generate.py` 逐句生成**：
   ```bash
   python scripts/tts_generate.py \
     --script "{项目}/视频/口播脚本.md" \
     --out "{项目}/视频/audio" \
     --voice zh-CN-YunxiNeural
   ```
   - 每句生成一个 `seg{N}.mp3`，命名 `seg01.mp3`...
   - 音色建议：男声 `zh-CN-YunxiNeural`，女声 `zh-CN-XiaoxiaoNeural`，可按章节情绪选择

3. **记录每句时长**：脚本输出 `时长清单.json`（seq / page / file / duration_sec）。

## 时长清单.json 结构

```json
[
  {"seq": 1, "page": "cover", "file": "seg01.mp3", "duration_sec": 2.1},
  {"seq": 2, "page": "page1", "file": "seg02.mp3", "duration_sec": 3.4},
  ...
]
```

## 产出

- `{项目}/视频/audio/seg{N}.mp3`（分句音频）
- `{项目}/视频/audio/时长清单.json`

## 完成判定

- [ ] 每句口播都有对应 mp3
- [ ] 时长清单.json 含全部句的 seq/page/file/duration
- [ ] 总时长 ~60s（与脚本估算偏差 <20%）

> 若某句生成失败：重试该句，不中断整批。