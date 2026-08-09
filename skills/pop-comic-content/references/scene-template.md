# 逐格阅读相机系统（scene-template / v0.8）

> pop-comic-content 出片专用。**v0.8 起废弃 Ken Burns 缩放模板，改走「逐格阅读」**：按`分镜标注.json`把分享成品图按格裁剪，相机在格与格之间做**纯平移（translate）滚动**，一格一格把漫画"读"过去。**禁止放大/缩小（scale）**——漫画是分格叙事，缩放会破坏格子与阅读节奏（插画才适合推镜）。

## 为什么改掉缩放模板

老板实测 v0.7 的缩放模板（T1~T5 Ken Burns）后否掉：漫画是分格阅读顺序，缩放推拉既不尊重格子边界、又制造"剪映拼图"式的生硬跳切。逐格阅读用**切格 + 平移过渡**还原漫画本身的阅读节奏，画面连续、无生硬 gap。

## 核心结构

1. **分镜标注**：`分镜标注.json` 定义每页的格子 `bbox`（归一化 0~1，`[x0,y0,x1,y1]`）。**bbox 底部 ≤0.88**，向内收缩 gutter，避开分享成品图底部的 popwave 水印条。
2. **裁剪适配**：每格从分享成品图按 bbox 裁出，再 `cover` 填满 1080×1920（`resize` 到能覆盖再居中裁切，保证无黑边）。
3. **横向胶片 strip**：所有格子截图按阅读顺序排成一条横向 strip（每格一个满屏 1080×1920 单元）。
4. **相机平移**：`strip` 用 `translateX` 在格与格之间滑动，`ease` 缓动，格间过渡 0.45s。
5. **字幕按时间窗**：口播 seq 时间轴对齐，字幕在对应口播窗口内淡入淡出（**不靠格子 id 匹配**，否则永不显示——v0.8 已修此坑）。

## 分镜标注格式（`分镜标注.json`）

```json
{
  "canvas": {"w": 1080, "h": 1920},
  "pages": [
    {
      "page": 1,
      "seq": [1, 2],
      "img": "page01.png",
      "panels": [
        {"id": "P1-1", "bbox": [0.02, 0.09, 0.98, 0.56], "label": "上大横格"},
        {"id": "P1-2", "bbox": [0.02, 0.60, 0.45, 0.88], "label": "左下竖格"}
      ]
    }
  ]
}
```

- `seq`：该页口播 seq（Step 3 配音段序号），决定该页时长与口播时间窗。
- `bbox`：格子归一化坐标，**底部 ≤0.88**（水印条之上），向内留 gutter 避免裁到相邻格。

## 裁剪适配算法（PIL，cover 填满无黑边）

```python
scale = max(C_W/bw, C_H/bh)          # 按短边放大到覆盖
box = box.resize((nw, nh), LANCZOS)
cl = (nw-C_W)//2; ct = (nh-C_H)//2    # 居中裁切
box = box.crop((cl, ct, cl+C_W, ct+C_H))
```

## HTML 骨架（横向胶片 + translateX 相机）

```html
<style>
  html,body{width:1080px;height:1920px;overflow:hidden;background:#000;
    font-family:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif;}
  .stage{position:absolute;inset:0;overflow:hidden;}
  .strip{position:absolute;top:0;left:0;width:N*1080px;height:1920px;display:flex;will-change:transform;}
  .cell{flex:0 0 1080px;width:1080px;height:1920px;}
  .cell img{width:100%;height:100%;object-fit:cover;display:block;}
  .mask{position:absolute;left:0;right:0;bottom:150px;height:260px;
    background:linear-gradient(to top,rgba(0,0,0,.75),rgba(0,0,0,0));pointer-events:none;}
  .sub{position:absolute;left:70px;right:70px;bottom:200px;text-align:center;
    font-size:42px;line-height:1.5;color:#fff;text-shadow:0 3px 10px rgba(0,0,0,.95);opacity:0;}
</style>
```

## render(t) 相机 + 字幕（锁死写法）

```js
var CELLS=[...格id]; var STARTS=[...每格起始秒]; var SUBS=[...{id,start,end}];
var STRIP=document.getElementById('strip');
function clamp(x,a,b){return x<a?a:(x>b?b:x);}
function ease(x){return x<0.5?2*x*x:1-Math.pow(-2*x+2,2)/2;}
function seg(t,a,b){return clamp((t-a)/(b-a),0,1);}
function app(t,a,b){return ease(seg(t,a,b));}
function out(t,a,b){return 1-app(t,a,b);}
var TRANS=0.45;
function render(t){
  var idx=0; for(var i=0;i<STARTS.length;i++){ if(t>=STARTS[i]) idx=i; }
  var next=idx+1, x=-idx*1080;
  if(next<STARTS.length && t>=STARTS[next]-TRANS && t<STARTS[next]){
    x=-(idx+ease(seg(t,STARTS[next]-TRANS,STARTS[next])))*1080;   // 格间平移过渡
  }
  STRIP.style.transform='translateX('+x+'px)';
  // 字幕：按口播时间窗显示（与配音对齐，不依赖格子 id）
  for(var j=0;j<SUBS.length;j++){
    var el=document.querySelector('[data-sub="'+SUBS[j].id+'"]'); if(!el) continue;
    var on=(t>=SUBS[j].start && t<=SUBS[j].end);
    el.style.opacity=on?(app(t,SUBS[j].start,SUBS[j].start+0.3)*out(t,SUBS[j].end-0.3,SUBS[j].end)):0;
  }
}
window.render=render;
```

> **字幕按 `SUBS[j].start/end` 时间窗显示**，禁止用格子 id 匹配字幕 id（两者本就不同，匹配永远不中，字幕永不显示——v0.8 已修）。

## 时间轴设计

- 每页时长 = 该页 `seq` 口播时长之和 + 0.5s 呼吸；页内每格展示时长 = 页时长 / 格数（视觉均匀）。
- 口播 seq 时间窗：从页首起，按各 seq 实际配音时长累加。
- 字幕窗口 = 口播窗口 ±0.2s 起止。

## 验收标准（出片前逐页核对）

- 每格取景完整、格子边界正确、无黑边、无水印残留（bbox 底部 ≤0.88）。
- 字幕在每个口播窗口内正常显示、不重叠、不压主体（落在底部渐隐 mask 区）。
- 格与格之间是平移过渡（无 scale），连续不跳切。
- 语速统一（TTS `--speech-rate +20`），字幕与配音对齐。