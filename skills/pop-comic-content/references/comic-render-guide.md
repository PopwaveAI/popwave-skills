# 漫画页动效渲染写法（逐格阅读 + 字幕）

> pop-comic-content 出片动效用「JS 驱动逐帧渲染」：单页 HTML 暴露 `window.render(t)`，agent 逐帧设时间渲染。**v0.8 起画面主体是漫画分格裁剪**（按`分镜标注.json`裁剪格子，横向胶片 + 相机平移），叠加字幕淡入，**不用 scale 缩放**（漫画是分格叙事，缩放破坏格子与阅读节奏）。具体逐格阅读相机写法见 `references/scene-template.md`，本文件讲通用辅助函数、时间轴与命令。

## 与 pop-video-brand 渲染的差异

| 维度 | pop-video-brand（品宣） | pop-comic-content（漫画） |
|:--|:--|:--|
| 画面主体 | HTML 元素搭建（文字+UI截图） | **漫画分格裁剪（panel）** |
| 画布 | 1920×1080 横版 | **1080×1920 竖版** |
| 动效 | 元素位移/缩放 | **格间平移滚动 + 字幕淡入** |
| 分镜 | HTML 场景切换 | 逐格阅读相机（translateX） |

## 页面骨架（竖版 1080×1920）

```html
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:1080px;height:1920px;overflow:hidden;background:#000;
    font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif;}
  .scene{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
    opacity:0;will-change:transform,opacity;}
  .scene img.page{position:absolute;width:100%;height:100%;object-fit:contain;
    will-change:transform;}
  .sub{position:absolute;left:60px;right:60px;bottom:120px;text-align:center;
    font-size:44px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,0.9);
    opacity:0;will-change:transform,opacity;}
</style>
<body>
  <div class="scene" data-page="1">
    <img class="page" src="assets/page1.png">
    <div class="sub" data-sub="1-1">深夜，一个男人从剧痛中惊醒。</div>
    <div class="sub" data-sub="1-2">他睁不开眼，身体像被钉在床上。</div>
  </div>
  <!-- 每页一个 .scene，字幕用 data-sub 标记 -->
  <script>...render(t)...</script>
</body>
```

## 辅助函数（直接复用 brand 的）

```js
function clamp(x,a,b){return x<a?a:(x>b?b:x);}
function seg(t,a,b){return clamp((t-a)/(b-a),0,1);}
function ease(x){return x<0.5?2*x*x:1-Math.pow(-2*x+2,2)/2;}
function app(t,a,b){return ease(seg(t,a,b));}   // 进场 0→1
function out(t,a,b){return 1-app(t,a,b);}       // 出场 1→0
function set(el,o,tr){if(el){el.style.opacity=o;el.style.transform=tr;}}
```

## render(t) 状态赋值

**逐格阅读相机**：见 `references/scene-template.md`——横向胶片 strip + `translateX` 格间平移过渡（ease 缓动 0.45s），**不用 scale**。字幕按口播时间窗淡入淡出，**每条字幕必须带出场淡出**（`app(进场)*out(出场)`），本页第二条字幕进场前先淡出第一条，否则两条叠加重叠。

```js
// 字幕生命周期（模板无关，统一规则）
// sub-a：进场 app(t,0.5,1.2) * 出场 out(t,2.3,2.7)，驻留期责对齐配音段
set(document.querySelector('[data-sub="a"]'), app(t,0.5,1.2)*out(t,2.3,2.7), '');
// sub-b：在 sub-a 出场后进场，避免重叠
set(document.querySelector('[data-sub="b"]'), app(t,2.8,3.5)*out(t,4.4,4.8), '');
```

> 字幕生命周期公式：`app(进场起,进场止) * out(淡出起,淡出止)`。进场止 → 淡出起 之间为字幕驻留期（对齐配音段时长），淡出起设在下一条进场前 0.3s。**v0.8 起字幕按时间窗显示**（`t>=start && t<=end`），禁止用格子 id 匹配字幕 id（两者本就不同）。

## 时间轴设计（每页时长 = 该页口播总时长 + 0.5s 余量）

- 从 `时长清单.json` 读每句口播 `duration_sec`，按页累加得到每页起止时间。
- 每页一声景，页面切换用 `out` 淡出 + 下一页 `app` 淡入（0.3s 交叉）。

## 常见坑

- 分格裁剪用 `object-fit:cover` 填满，禁止改变布局尺寸；相机在 strip 的 `translateX` 上做，**禁用 scale**。
- **渲染必须显式传 `--w 1080 --h 1920`**：`render_frames.py` 默认横版 1920×1080，漏传会把竖版 HTML 裁成横版。
- 只改 `opacity` 与 `transform`，保证 Playwright 截图即时生效。
- 格子截图用相对路径 `panels/{格id}.png`，与 index.html 同目录。
- 中文字体必须显式设置（`Noto Sans CJK SC` / `WenQuanYi Micro Hei`）。
- **字幕按时间窗显示，勿用格子 id 匹配字幕 id**（v0.8 修过此坑，匹配永远不中导致字幕永不显示）。

## 渲染与混音命令

**出片默认走「浏览器自播 + 录屏」（方案 B，`scripts/record_video.py`）**：HTML 编排稿按真实时间自播，Playwright 录成 WebM 再转 MP4，不落千张 PNG，快一个数量级。逐帧方案（`render_frames.py`）仅用于预览校验构图。

```bash
# 预览校验（必须带 --w/--h 竖版，逐帧模式抓关键帧）
python scripts/render_frames.py --html index.html --out preview --mode preview --times 0.5,2.0,4.0,7.0 --w 1080 --h 1920
# 全量出片（方案 B：录屏，主路径）
python scripts/record_video.py --html index.html --out 成品.mp4 --duration <总时长> --w 1080 --h 1920 --preset veryfast
# 混入配音（按时间轴定位，时间来自时间轴设计）
python scripts/mix_audio.py --video 成品.mp4 --audio-dir audio \
  --offsets "seg01.mp3=3.0,seg02.mp3=8.9,..." --out 成品-配音.mp4
```

> 录屏方案通过注入自播时钟驱动已有的 `window.render(t)`，不改动画逻辑，画面与逐帧方案一致。`--preset veryfast` 最快 / `fast` / `medium` 质量更好，`--crf 18` 保画质。实测 57s 竖版视频全程 ~86s 出片（逐帧方案光渲染就 7-10 分钟）。