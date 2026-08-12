# Step 4: 渲染合成

> HTML/CSS 排版（复用漫画美学）+ Playwright 截图 + 图/字幕/人声/Ken Burns/BGM → ffmpeg 合成 MP4。

## 前置

- 老板已确认脚本（Step 2 闸门）
- 配音已生成（Step 3，`时长清单.json`）
- `pip install playwright && playwright install chromium`
- ffmpeg 已安装

## 操作

1. **生成逐帧 HTML**：按 `时长清单.json`，每句口播对应一帧（图片 + 字幕 + Ken Burns 起始/结束缩放位移）。
   - 画布：竖屏 1080x1920（短视频）或 16:9 1920x1080，按目标平台选
   - 中文字体：`Noto Sans CJK SC` / `WenQuanYi Micro Hei`（必须显式设置，禁止默认字体）
   - 字幕叠加在图片下方或底部，不遮挡画面关键信息

2. **Playwright 截图**：`scripts/render_video.py` 逐帧截图到 `frames/`。

3. **ffmpeg 合成**（`scripts/render_video.py` 内置）：
   - 每帧图片按对应口播时长定格（Ken Burns 推拉）
   - 拼接所有帧 → 视频流
   - 混入人声（按 `时长清单.json` 对齐）+ 可选 BGM
   - 输出 `{章节名}.mp4`

## Ken Burns（推拉）规则

- 每帧从"起始缩放/位移"缓动到"结束缩放/位移"
- 竖屏图：缓慢推近（zoom in）或平移（pan），避免静止僵化
- 缩放范围 1.0→1.15 以内，避免观感怪异

## 产出

- `{项目}/视频/frames/frame{N}.png`（中间帧）
- `{项目}/视频/{章节名}.mp4`（最终视频）

## 完成判定

- [ ] 无黑边（图填满画面，`object-fit: cover`）
- [ ] 字幕字体为 CJK 字体，无乱码
- [ ] 每句口播与对应页面对齐
- [ ] 视频可播放，`{章节名}.mp4` 已生成

## 可选

- BGM：默认无，如需加在 `scripts/render_video.py` 用 `--bgm` 参数混入（音量压低，不盖人声）
- 加水印/片头（OC/封面作为开场帧）