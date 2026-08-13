---
id: motion-timeline-guide
lib: 知识库
cat: 视觉
version: 1.0.0
tags: [视觉]
---
# HTML 动效时间线写法（render(t) 模式）

> 本 skill 的动效用"JS 驱动逐帧渲染"实现：单页 HTML 暴露 `window.render(t)`，agent 逐帧设时间并截图。**不用 CSS keyframes**（无法精确对齐帧）。

## 页面骨架
```html
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:1920px;height:1080px;overflow:hidden;background:#FBFDFF;
    font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif;}
  .el{position:absolute;opacity:0;will-change:transform,opacity;}
</style>
<body>
  <div id="s1"><div class="el" id="e1" style="left:..;top:..">..</div></div>
  <script>...render(t)...</script>
</body>
```

## 辅助函数（直接复用）
```js
function clamp(x,a,b){return x<a?a:(x>b?b:x);}
function seg(t,a,b){return clamp((t-a)/(b-a),0,1);}   // 0→1 over [a,b]
function ease(x){return x<0.5?2*x*x:1-Math.pow(-2*x+2,2)/2;} // easeInOutQuad
function app(t,a,b){return ease(seg(t,a,b));}          // 进场透明度 0→1
function out(t,a,b){return 1-app(t,a,b);}              // 出场透明度 1→0
function slide(t,a,b,from){return from*(1-app(t,a,b));}// 位移 from→0
function set(id,o,tr){var e=document.getElementById(id);if(e){e.style.opacity=o;e.style.transform=tr;}}
```

## render(t) 状态赋值
- 每元素透明度和 transform 用 `app/out/slide` 组合：
  ```js
  set('e1', app(t,0.5,1.5)*out(t,4.4,5.0), 'translateY('+(-slide(t,0.5,1.5,26))+'px)');
  ```
- 生命周期：`进场透明度 × 出场透明度`，位移用 `-slide(...)`（从下方/侧方滑入）。
- 序列元素（功能矩阵等）用循环按 `a+i*step` 逐个点亮。

## 背景光晕
```css
.glow{position:absolute;border-radius:50%;filter:blur(90px);opacity:0;pointer-events:none;}
```
- render 里 `set('glow1', clamp(app(t,0,0.6)+0.25*Math.sin(t*0.8),0,1), '')` 做轻微呼吸。

## 居中元素
- `left:50%` 元素在 render 里补 `translateX(-50%)`；需要微调时用 `translateX(calc(-50% + Npx))`。

## 常见坑
- 变换里禁止除零（折算位移用进场的 `app()` 结果，不直接除以其它值）。
- 图片用相对路径（`assets/…`），与 index.html 同目录。
- 产品截图卡片：`img{object-fit:contain}`，白底，避免拉伸。
- 只改 `opacity` 与 `transform`，保证 Playwright 截图即时生效。

## 渲染脚本
- `scripts/render_frames.py --html index.html --out preview --mode preview --times ...`
- `scripts/render_frames.py --html index.html --out frames --mode full --fps 30 --start 0 --end 33`
- `scripts/encode.py --frames frames --out 成品.mp4 --fps 30`