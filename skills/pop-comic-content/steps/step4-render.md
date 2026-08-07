# Step 4: 漫画页出片（渲染 + 合成）

> 把老板确认的口播脚本 + 漫画页图片组装成竖版短视频：图片为主体 + Ken Burns 推拉 + 字幕淡入。先预览校验构图，再全量渲染合成。复用 pop-video-brand 的 `render_frames.py` + `encode.py`。

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

### 2. 抓预览帧校验（铁律，复用 brand 思路）

```bash
python scripts/render_frames.py --html index.html --out preview --mode preview --times <每页中途帧时间> --w 1080 --h 1920
```

> ⚠️ **必须显式传 `--w 1080 --h 1920`**：`render_frames.py` 默认视口是横版 1920×1080，不传会把竖版 HTML 裁成横版（画面被砍、字幕错位）。本轮实操曾因漏传此参数产出了错误的横版视频。

逐张 Read 审查：画面完整、**字幕不重叠**、无溢出/错位、Ken Burns 正常。发现问题回改 HTML 再抓预览，直到通过。

### 3. 全量渲染

```bash
python scripts/render_frames.py --html index.html --out frames --mode full --fps 30 --start 0 --end <总时长> --w 1080 --h 1920
```

### 4. 合成无音轨视频（复用 brand `encode.py`）

```bash
python scripts/encode.py --frames frames --out 成品.mp4 --fps 30
```

## 产出

- `{项目}/视频/index.html` + `assets/`
- `{项目}/视频/preview/`（校验帧）
- `{项目}/视频/frames/`（全量帧）
- `{项目}/视频/成品.mp4`（无音轨）

## 完成判定

- [ ] 预览帧逐张校验通过（构图/字幕/无溢出）
- [ ] 全量帧渲染完成
- [ ] 成品.mp4 合成成功（probe 校验分辨率/时长/fps）

> 出片是确定性渲染（HTML+Playwright+ffmpeg），不走 AI 视频。若老板只要文本三件套，本步可跳过。