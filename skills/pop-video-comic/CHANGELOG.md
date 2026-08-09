# CHANGELOG

## v0.1.0 | 2026-08-06

首版发布：漫画转 PPT 放映式短视频 skill。

### 新增
- 五步管线：Step 0 收集 → Step 1 读图理解 → Step 2 脚本创作【确认闸门】→ Step 3 TTS 配音 → Step 4 渲染合成
- 读图自理解：模型直接读漫画页，图片为主，`页面配置.json` 文字兜底（审查拦截时补全）
- 先脚本后出片：Step 2 产出 `口播脚本.md` 后停下来等老板确认，确认后才配音合成
- 每句口播绑定 page{N}，保证画面与口播/字幕同步
- TTS：edge-tts 免费配音（`scripts/tts_generate.py`），输出分句 mp3 + 时长清单
- 渲染：HTML 排版 + Playwright 截图 + ffmpeg 合成（`scripts/render_video.py`），Ken Burns 推拉 + 字幕 + 可选 BGM

### 铁律
- ❌1 先脚本后出片（Step 2 确认闸门）
- ❌2 读图为主、配置文字兜底
- ❌3 每句口播绑定具体页
- ❌4 视频合成走确定性渲染，不走 AI 视频（Seedance/GenerateVideo）