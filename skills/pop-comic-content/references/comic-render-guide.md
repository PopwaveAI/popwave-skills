# 漫画页动效渲染写法（图片为主体 + Ken Burns + 字幕）

> pop-comic-content 出片动效用「JS 驱动逐帧渲染」：单页 HTML 暴露 `window.render(t)`，agent 逐帧设时间并截图。**画面主体是漫画页图片**（整页 PNG），叠加 Ken Burns 推拉 + 字幕淡入，不用 CSS keyframes（无法精确对齐帧）、不做品宣式 HTML 元素搭建。

## 与 pop-video-brand 渲染的差异

| 维度 | pop-video-brand（品宣） | pop-comic-content（漫画） |
|:--|:--|:--|
| 画面主体 | HTML 元素搭建（文字+UI截图） | **整张漫画页图片** |
| 画布 | 1920×1080 横版 | **1080×1920 竖版** |
| 动效 | 元素位移/缩放 | **Ken Burns 推拉 + 字幕淡入** |
| 分镜 | HTML 场景切换 | 每页漫画图切换 |

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

**Ken Burns 推拉**：图片从 scale 1.0 → 1.12 缓动，轻微上移（模拟镜头推进）。

```js
function kenburns(img, t, start, dur){
  var p = clamp((t-start)/dur, 0, 1);
  var s = 1.0 + 0.12 * ease(p);
  var ty = -0.15 * 1920 * (s - 1) * p;   // 轻微上移
  set(img, app(t,start,start+0.3)*out(t,start+dur-0.3,start+dur),
      'scale('+s+') translateY('+ty+'px)');
}
```

**每页场景**：`scene` 整页淡入/淡出，图片做 Ken Burns，字幕按时间点淡入淡出。**每条字幕必须带出场淡出**（`app(进场)*out(出场)`），本页第二条字幕进场前先淡出第一条，否则两条叠加重叠。

```js
// 第1页 0-5s（示例；实际每页时长=该页口播总时长+余量）
kenburns(document.querySelector('.scene[data-page="1"] img'), t, 0, 5);
set(document.querySelector('.scene[data-page="1"]'), 1, '');
// sub-1-1：0.5 进场，2.5 淡出（在 sub-1-2 进场前收起）
set(document.querySelector('[data-sub="1-1"]'), app(t,0.5,1.2)*out(t,2.3,2.7), '');
// sub-1-2：2.8 进场，4.5 淡出（页末随场景收起）
set(document.querySelector('[data-sub="1-2"]'), app(t,2.8,3.5)*out(t,4.4,4.8), '');
```

> 字幕生命周期公式：`app(进场起,进场止) * out(淡出起,淡出止)`。进场止 → 淡出起 之间为字幕驻留期（对齐配音段时长），淡出起设在下一条进场前 0.3-0.5s。

## 时间轴设计（每页时长 = 该页口播总时长 + 0.5s 余量）

- 从 `时长清单.json` 读每句口播 `duration_sec`，按页累加得到每页起止时间。
- 每页一声景，页面切换用 `out` 淡出 + 下一页 `app` 淡入（0.3s 交叉）。

## 常见坑

- 图片 `object-fit:contain` 但要 `width/height:100%` 铺满，Ken Burns 在 transform 上做，禁止改变布局尺寸。
- **渲染必须显式传 `--w 1080 --h 1920`**：`render_frames.py` 默认横版 1920×1080，漏传会把竖版 HTML 裁成横版。
- 只改 `opacity` 与 `transform`，保证 Playwright 截图即时生效。
- 图片用相对路径 `assets/page{N}.png`，与 index.html 同目录。
- 中文字体必须显式设置（`Noto Sans CJK SC` / `WenQuanYi Micro Hei`）。

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