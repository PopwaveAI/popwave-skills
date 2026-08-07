# Step 4: 漫画页出片（渲染 + 合成）

> 把老板确认的口播脚本 + 漫画页图片组装成竖版短视频：图片为主体 + Ken Burns 推拉 + 字幕淡入。**出片走「浏览器自播 + 录屏」方案（方案 B，`scripts/record_video.py`）**：HTML 编排稿按真实时间自播，Playwright 直接录成 WebM 再转 MP4，不落千张 PNG，出片快一个数量级。逐帧方案（`render_frames.py`）仅用于**预览校验构图**。

## 输入

- 老板确认的 `口播脚本.md`（Step 2 产出）
- **漫画页图片（优先 `分享/` 成品图，无则回退 `output/` 生图）**——按 Step 0 素材清单的来源记录取图
- `时长清单.json`（Step 3 配音产出，含每句口播时长）

## 操作

### 1. 排 HTML 动效时间线

> **图片用 `分享/` 成品图**（含对白/水印，正式素材），把 `page01~N.png` 拷到 `assets/`。若分享缺页，用 `output/` 对应生图补齐，并在画面理解里标注「生图回退」。

按 `references/comic-render-guide.md` 写单页 HTML（1080×1920 竖版）：
- 每页一个 `.scene`，画面主体是漫画页图片
- Ken Burns 推拉 + 字幕淡入淡出（用 `references/comic-render-guide.md` 的辅助函数）
- **每条字幕必须有出场淡出**（`app(进场)*out(出场)`，本页第二条字幕进场前先淡出第一条），禁止只写进场——否则同页两条字幕重叠
- 每页时长 = 该页口播总时长 + 0.5s 余量（从 `时长清单.json` 累加）
- 产出 `index.html` + `assets/`（拷贝漫画页）

### 2. 抓预览帧校验（铁律，用逐帧模式抓关键帧）

```bash
python scripts/render_frames.py --html index.html --out preview --mode preview --times <每页中途帧时间> --w 1080 --h 1920
```

> ⚠️ **必须显式传 `--w 1080 --h 1920`**：`render_frames.py` 默认视口是横版 1920×1080，不传会把竖版 HTML 裁成横版（画面被砍、字幕错位）。本轮实操曾因漏传此参数产出了错误的横版视频。

逐张 Read 审查：画面完整、**字幕不重叠**、无溢出/错位、Ken Burns 正常。发现问题回改 HTML 再抓预览，直到通过。

### 3. 全量出片（方案 B：录屏，主路径）

```bash
python scripts/record_video.py --html index.html --out 成品.mp4 --duration <总时长> --w 1080 --h 1920 --preset veryfast
```

- `--duration` = 动画总时长（`时长清单.json` 累加出的总秒数）
- 录屏时长 ≈ 动画时长（57s 视频全程 ~86s 出片），不落中间 PNG
- 转码 `--preset veryfast`（快）/ `fast` / `medium`（质量更好），`--crf 18` 保画质
- 产物 `成品.mp4` 为无音轨 H.264 竖版视频（Step 5 混音）

## 产出

- `{项目}/视频/index.html` + `assets/`
- `{项目}/视频/preview/`（预览校验帧）
- `{项目}/视频/成品.mp4`（无音轨）

## 完成判定

- [ ] 预览帧逐张校验通过（构图/字幕/无溢出）
- [ ] 录屏出片成功，成品.mp4 已生成（probe 校验分辨率 1080×1920 / 时长 / fps 30）
- [ ] 画面与预览帧一致（字幕不重叠、无溢出）

> 出片是确定性渲染（HTML+Playwright+ffmpeg），不走 AI 视频。若老板只要文本三件套，本步可跳过。录屏方案只在 HTML 注入自播时钟，不改 `render(t)` 逻辑，与逐帧方案产出画面一致。