# Step 4: 漫画页出片（逐格阅读 + 渲染合成）

> 把老板确认的口播脚本 + 漫画页图片组装成竖版短视频。**v0.8 起走「逐格阅读」相机系统**：按`分镜标注.json`把分享成品图按格裁剪，相机在格间纯平移滚动，一格一格"读"过去。**禁止 Ken Burns 放大/缩小**（漫画是分格叙事，缩放破坏格子与阅读节奏）。出片用「浏览器自播 + 录屏」（`scripts/record_video.py`），逐帧方案（`render_frames.py`）仅用于预览校验构图。

## 输入

- 老板确认的 `口播脚本.md`（Step 2 产出）
- **漫画页图片（优先 `分享/` 成品图，无则回退 `output/` 生图）**——按 Step 0 素材清单的来源记录取图
- `时长清单.json`（Step 3 配音产出，含每句口播时长）——**建议统一 `--speech-rate +20` 重合成，去除语速不均/偏慢**
- `分镜标注.json`（格子边界，`references/scene-template.md` 定义格式）

## 操作

### 1. 标注分镜框

逐页 Read 漫画图，给每页格子标注归一化 bbox 写入 `分镜标注.json`（格式见 `references/scene-template.md`）：
- 每格 `id`（如 `P1-1`）、`bbox`（`[x0,y0,x1,y1]`，0~1）、`label`
- **bbox 底部 ≤0.88**，向内收缩 gutter，避开分享成品图底部的 popwave 水印条
- `seq` 标该页口播段序号（决定该页时长与口播时间窗）

### 2. 裁剪格子 + 排 HTML

用 `gen_v3.py` 类似逻辑（见 `scripts/` 或历史工作区模板）：每格从分享成品图按 bbox 裁出，`cover` 填满 1080×1920，排成横向胶片 strip；`render(t)` 用 `translateX` 在格间平移（ease 缓动，过渡 0.45s），字幕按口播时间窗淡入淡出。产出 `index.html` + `panels/`。

> **字幕按 `SUBS[j].start/end` 时间窗显示**，禁止用格子 id 匹配字幕 id（v0.8 修过此坑，匹配永远不中导致字幕永不显示）。

### 3. 抓预览帧校验（铁律，逐帧模式抓关键帧）

```bash
python scripts/render_frames.py --html index.html --out preview --mode preview --times <关键帧时间...> --w 1080 --h 1920
```

> ⚠️ **必须显式传 `--w 1080 --h 1920`**：`render_frames.py` 默认视口是横版 1920×1080，不传会把竖版 HTML 裁成横版（画面被砍、字幕错位）。

逐张 Read 审查：每格取景完整、无黑边、无水印残留、字幕正常显示且不重叠、格间是平移过渡。发现问题回改 HTML 再抓预览，直到通过。

### 4. 全量出片（方案 B：录屏，主路径）

```bash
python scripts/record_video.py --html index.html --out 第{N}章-v{版本}.mp4 --duration <总时长> --w 1080 --h 1920 --preset veryfast
```

- `--duration` = 动画总时长（`时长清单.json` 累加出的总秒数）
- 录屏时长 ≈ 动画时长（57s 视频全程 ~86s 出片），不落中间 PNG
- 转码 `--preset veryfast`（快）/ `fast` / `medium`（质量更好），`--crf 18` 保画质
- 产物 `第{N}章-v{版本}.mp4` 为无音轨 H.264 竖版中间候选（Step 5 混音后产出 `第{N}章-配音-v{版本}-final.mp4`，命名遵循落盘规范 §3.1b）

## 产出

- `{项目}/视频/index.html` + `panels/`
- `{项目}/视频/preview/`（预览校验帧，过程）
- `{项目}/视频/第{N}章-v{版本}.mp4`（无音轨中间候选）

## 完成判定

- [ ] 预览帧逐张校验通过（取景/字幕/无水印/无黑边）
- [ ] 每格平移过渡连续，无 scale 缩放
- [ ] 字幕正常显示且与配音时间轴对齐
- [ ] 录屏出片成功，`第{N}章-v{版本}.mp4` 已生成（probe 校验分辨率 1080×1920 / 时长 / fps 30）

> 出片是确定性渲染（HTML+Playwright+ffmpeg），不走 AI 视频。若老板只要文本三件套，本步可跳过。录屏方案只在 HTML 注入自播时钟，不改 `render(t)` 逻辑，与逐帧方案产出画面一致。