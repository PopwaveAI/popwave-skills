# Step 3 · HTML渲染（自包含）

> 生成一个完整的独立 HTML 推书卡文件。本文件包含全部 CSS+JS 渲染逻辑+SVG 装饰，**agent 读完本文件即可完整产出，不需要再读取任何模板文件。**

---

## 输入

读取 `工作稿/review.json`。

---

## 产出

`{书名}-读者推书-v1.html` — 自包含文件，双击浏览器直接打开。

---

## 渲染流程

1. 读取 review.json → 序列化为 JS 变量 `window.__BOOK_DATA__ = {...};`
2. 读取下面的完整 HTML 骨架（从 `<!doctype html>` 到 `</html>`）
3. 将 `{{TITLE}}` 替换为书名
4. 将 `{{REVIEW_DATA}}` 替换为第1步的 JS 变量内容
5. 落盘到项目根目录

---

## 强制执行：完整 HTML 骨架

⚠️ **下面的完整 HTML 代码就是最终产出。逐字写入 `{书名}-读者推书-v1.html`，不要修改任何 CSS 类名、不要删除任何 SVG 装饰块、不要自己手写渲染函数替代。**

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLE}}｜读者推书卡</title>
<style>
:root{--bg:#1a1a1e;--white:#fff;--black:#111;--grey1:#f8f8f8;--grey2:#eee;--grey3:#ccc;--grey4:#999;--grey5:#555;--grey6:#333;--red:#c0392b;--gold:#b8860b;--blue:#1a5276;--teal:#117a65;--orange:#d35400;--ink:#1a1a1e;--soft:#666;--accent:#b8860b;--accent2:#8b6914;--paper:#faf8f2;--cover1:#1a1410;--cover2:#3d2817}
body[data-theme="ink-blue"]{--ink:#0d1b2a;--soft:#5a7a9a;--accent:#1b6b8f;--accent2:#2e86ab;--paper:#f2f7fa;--cover1:#0a1628;--cover2:#1a3a5c;--red:#8b0000;--gold:#b8860b}
body[data-theme="warm-paper"]{--ink:#2d1f14;--soft:#8b7355;--accent:#c0392b;--accent2:#d35400;--paper:#fef9f0;--cover1:#1a0f08;--cover2:#5c2a0e;--gold:#d4a017}
body[data-theme="dark-modern"]{--bg:#0a0a0c;--ink:#e8e8ec;--soft:#888;--accent:#ff6b6b;--accent2:#ffa500;--paper:#141418;--cover1:#050508;--cover2:#1a1020;--gold:#ffa500;--white:#e8e8ec;--grey1:#1a1a20;--grey2:#222;--grey3:#333;--grey4:#666;--grey5:#999;--grey6:#bbb;--black:#000}
body[data-theme="diary-orange"]{--ink:#1e2d3a;--soft:#5a7a8a;--accent:#d35400;--accent2:#e67e22;--paper:#faf6f0;--cover1:#1a2530;--cover2:#6b3000;--gold:#d35400}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;display:flex;flex-direction:column;align-items:center;gap:40px;padding:40px 0}
.page{position:relative;width:720px;height:960px;overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,.45);flex-shrink:0}

/* P1 COVER */
.page-cover{background:linear-gradient(160deg,var(--cover1) 0%,var(--cover2) 60%,var(--cover1) 100%);color:var(--white);padding:0;display:flex;flex-direction:column}
.page-cover:before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.04),transparent 60%);pointer-events:none;z-index:0}
.page-cover .cover-inner{position:relative;z-index:1;flex:1;display:flex;flex-direction:column;justify-content:center;padding:60px 70px}
.page-cover .cover-eyebrow{font:600 13px/1.2 -apple-system,sans-serif;letter-spacing:.35em;color:var(--gold);margin-bottom:40px}
.page-cover h1{font:900 72px/1.05 "Songti SC","STSong","Noto Serif SC",serif;letter-spacing:-.03em;color:var(--white);max-width:560px}
.page-cover h1 em{color:var(--gold);font-style:normal}
.page-cover .cover-quote{margin-top:32px;font:500 22px/1.5 "Songti SC",serif;color:rgba(255,255,255,.75);max-width:500px;padding-left:24px;border-left:3px solid var(--gold)}
.page-cover .cover-lede{margin-top:16px;font:400 14px/1.7 -apple-system,sans-serif;color:rgba(255,255,255,.5);max-width:480px}
.page-cover .cover-footer{position:absolute;bottom:40px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid rgba(255,255,255,.12);padding-top:16px}
.page-cover .cover-tags{display:flex;gap:8px;flex-wrap:wrap}
.page-cover .cover-tags span{font:500 11px/1 -apple-system,sans-serif;color:rgba(255,255,255,.5);letter-spacing:.1em;padding:4px 0}
.page-cover .cover-tags span+span:before{content:"·";margin:0 6px;color:rgba(255,255,255,.25)}
.page-cover .cover-num{font:600 12px/1 -apple-system,sans-serif;color:rgba(255,255,255,.35);letter-spacing:.15em}
.page-cover .cover-overlay{position:absolute;right:-60px;bottom:-60px;width:320px;height:320px;border:1px solid rgba(255,255,255,.06);border-radius:50%;pointer-events:none;z-index:0}

/* SVG ICONS */
.deco-icon{pointer-events:none;z-index:0;overflow:visible}.deco-icon svg{width:100%;height:100%;display:block}
.cover-deco-book{position:absolute;left:58px;bottom:52px;width:72px;height:72px;opacity:.08}
.dash-deco-chart{position:absolute;right:16px;top:16px;width:48px;height:48px;opacity:.12}
.back-deco-star{width:100px;height:20px;opacity:.5;margin:0 auto 8px}
.show-deco-grid{position:absolute;right:0;top:0;width:180px;height:180px;opacity:.05;pointer-events:none;z-index:0}

/* P2 SWISS GRID */
.page-swiss{background:var(--paper);padding:52px 60px 52px 70px;display:flex;flex-direction:column}
.page-swiss:before{content:"";position:absolute;left:0;top:0;width:6px;height:100%;background:var(--black)}
.page-swiss .swiss-header{margin-bottom:44px}
.page-swiss .swiss-eyebrow{font:600 11px/1 -apple-system,sans-serif;letter-spacing:.25em;color:var(--soft);margin-bottom:18px}
.page-swiss h2{font:700 42px/1.1 -apple-system,sans-serif;letter-spacing:-.02em;color:var(--ink);max-width:520px}
.page-swiss h2 em{color:var(--accent);font-style:normal}
.page-swiss .swiss-grid{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:0;flex:1}
.page-swiss .swiss-cell{padding:28px 32px 28px 0;display:flex;flex-direction:column;justify-content:flex-start;border-bottom:1px solid var(--grey3)}
.page-swiss .swiss-cell:nth-child(odd){padding-right:28px;border-right:1px solid var(--grey3)}
.page-swiss .swiss-cell:nth-child(3),.page-swiss .swiss-cell:nth-child(4){border-bottom:none}
.page-swiss .swiss-num{font:900 48px/1 -apple-system,sans-serif;color:var(--grey3);margin-bottom:8px}
.page-swiss .swiss-cell h3{font:700 16px/1.3 -apple-system,sans-serif;color:var(--ink);margin-bottom:6px}
.page-swiss .swiss-cell p{font:400 13px/1.55 -apple-system,sans-serif;color:var(--soft);max-width:240px}
.page-swiss .swiss-panel{margin-top:28px;padding:20px 0 0;border-top:2px solid var(--black)}
.page-swiss .swiss-panel h3{font:700 14px/1.3 -apple-system,sans-serif;color:var(--ink);margin-bottom:6px}
.page-swiss .swiss-panel p{font:400 13px/1.6 -apple-system,sans-serif;color:var(--soft);max-width:500px}
.page-swiss .swiss-footer{position:absolute;bottom:28px;left:70px;right:60px;display:flex;justify-content:space-between;font:500 10px/1 -apple-system,sans-serif;color:var(--grey4);letter-spacing:.12em}

/* P3 MAGAZINE */
.page-magazine{background:var(--paper);padding:0;display:flex}
.page-magazine .mag-left{width:180px;background:var(--ink);color:var(--white);padding:52px 32px;display:flex;flex-direction:column;justify-content:space-between}
.page-magazine .mag-left .mag-eyebrow{font:600 10px/1.4 -apple-system,sans-serif;letter-spacing:.3em;writing-mode:vertical-rl;color:var(--gold);margin:0 auto}
.page-magazine .mag-left .mag-section{font:900 72px/1 -apple-system,sans-serif;color:rgba(255,255,255,.08);text-align:center}
.page-magazine .mag-right{flex:1;padding:52px 48px 52px 40px;overflow-y:auto;display:flex;flex-direction:column}
.page-magazine h2{font:700 36px/1.15 "Songti SC",serif;color:var(--ink);margin-bottom:32px;letter-spacing:-.01em}
.page-magazine h2 em{color:var(--accent);font-style:normal}
.page-magazine .mag-steps{flex:1;display:flex;flex-direction:column;gap:0;position:relative}
.page-magazine .mag-steps:before{content:"";position:absolute;left:7px;top:8px;bottom:8px;width:1px;background:var(--grey2)}
.page-magazine .mag-step{position:relative;padding:0 0 28px 32px}
.page-magazine .mag-step:last-child{padding-bottom:0}
.page-magazine .mag-step:before{content:"";position:absolute;left:0;top:6px;width:15px;height:15px;border:2px solid var(--accent);border-radius:50%;background:var(--paper);z-index:1}
.page-magazine .mag-step:first-child:before{background:var(--accent)}
.page-magazine .mag-step h3{font:700 18px/1.3 "Songti SC",serif;color:var(--ink);margin-bottom:4px}
.page-magazine .mag-step p{font:400 13px/1.6 -apple-system,sans-serif;color:var(--soft)}
.page-magazine .mag-panel{margin-top:24px;padding:20px 24px;background:var(--grey1);border-left:3px solid var(--accent)}
.page-magazine .mag-panel h3{font:700 14px/1.3 -apple-system,sans-serif;color:var(--ink);margin-bottom:6px}
.page-magazine .mag-panel p{font:400 12.5px/1.6 -apple-system,sans-serif;color:var(--soft)}
.page-magazine .mag-footer{display:flex;justify-content:space-between;margin-top:28px;padding-top:16px;border-top:1px solid var(--grey2);font:500 10px/1 -apple-system,sans-serif;color:var(--grey4);letter-spacing:.1em}

/* P4 PROFILES */
.page-profiles{background:var(--paper);padding:52px 60px;display:flex;flex-direction:column}
.page-profiles .prof-header{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:36px;border-bottom:2px solid var(--black);padding-bottom:20px}
.page-profiles .prof-eyebrow{font:600 10px/1 -apple-system,sans-serif;letter-spacing:.25em;color:var(--soft)}
.page-profiles h2{font:700 40px/1.1 -apple-system,sans-serif;color:var(--ink);letter-spacing:-.02em}
.page-profiles .prof-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;flex:1}
.page-profiles .prof-card{padding:0;border:none;background:none}
.page-profiles .prof-card .prof-name{font:700 22px/1.2 "Songti SC",serif;color:var(--ink);margin-bottom:4px;padding-bottom:8px;border-bottom:2px solid var(--accent);display:inline-block}
.page-profiles .prof-card .prof-identity{font:500 12px/1 -apple-system,sans-serif;color:var(--accent);letter-spacing:.08em;margin-bottom:12px}
.page-profiles .prof-card .prof-drive{font:400 12.5px/1.55 -apple-system,sans-serif;color:var(--soft)}
.page-profiles .prof-panel{margin-top:24px;padding:20px 0 0;border-top:1px solid var(--grey3);display:flex;gap:32px}
.page-profiles .prof-panel h3{font:600 13px/1.3 -apple-system,sans-serif;color:var(--ink);min-width:80px}
.page-profiles .prof-panel p{font:400 12.5px/1.6 -apple-system,sans-serif;color:var(--soft)}
.page-profiles .prof-footer{display:flex;justify-content:space-between;margin-top:auto;padding-top:16px;border-top:1px solid var(--grey3);font:500 10px/1 -apple-system,sans-serif;color:var(--grey4);letter-spacing:.1em}

/* P5 INFOGRAPHIC */
.page-infographic{background:var(--paper);padding:52px 60px;display:flex;flex-direction:column}
.page-infographic .info-header{text-align:center;margin-bottom:36px}
.page-infographic .info-eyebrow{font:600 11px/1 -apple-system,sans-serif;letter-spacing:.3em;color:var(--soft);margin-bottom:14px}
.page-infographic h2{font:700 34px/1.15 -apple-system,sans-serif;color:var(--ink);letter-spacing:-.02em}
.page-infographic .info-diagram{flex:1;display:flex;align-items:center;justify-content:center;position:relative}
.page-infographic .info-center{text-align:center;z-index:1}
.page-infographic .info-formula{display:inline-flex;align-items:center;gap:16px;padding:24px 32px;border:2px solid var(--black);background:var(--white)}
.page-infographic .info-formula span{font:700 20px/1 "Songti SC",serif;color:var(--ink)}
.page-infographic .info-formula i{font:300 28px/1 serif;color:var(--accent)}
.page-infographic .info-cards{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:24px}
.page-infographic .info-card{padding:20px 24px;border:1px solid var(--grey3);background:var(--white)}
.page-infographic .info-card h3{font:700 15px/1.3 -apple-system,sans-serif;color:var(--ink);margin-bottom:6px}
.page-infographic .info-card p{font:400 12px/1.55 -apple-system,sans-serif;color:var(--soft)}
.page-infographic .info-panel{margin-top:20px;text-align:center;padding:16px 0;border-top:1px solid var(--grey3)}
.page-infographic .info-panel h3{font:600 13px/1.3 -apple-system,sans-serif;color:var(--ink);margin-bottom:4px}
.page-infographic .info-panel p{font:400 12.5px/1.5 -apple-system,sans-serif;color:var(--soft)}
.page-infographic .info-footer{display:flex;justify-content:space-between;margin-top:auto;padding-top:16px;border-top:1px solid var(--grey3);font:500 10px/1 -apple-system,sans-serif;color:var(--grey4);letter-spacing:.1em}

/* P6 TIMELINE */
.page-timeline{background:var(--paper);padding:52px 60px;display:flex;flex-direction:column}
.page-timeline .tl-header{margin-bottom:48px}
.page-timeline .tl-eyebrow{font:600 11px/1 -apple-system,sans-serif;letter-spacing:.25em;color:var(--soft);margin-bottom:14px}
.page-timeline h2{font:700 36px/1.15 -apple-system,sans-serif;color:var(--ink);letter-spacing:-.02em}
.page-timeline .tl-track{flex:1;display:flex;align-items:flex-start;position:relative;padding:20px 20px 0}
.page-timeline .tl-track:before{content:"";position:absolute;left:20px;right:20px;top:26px;height:2px;background:var(--black)}
.page-timeline .tl-cards{display:flex;gap:0;width:100%;position:relative;z-index:1}
.page-timeline .tl-card{flex:1;text-align:center;padding:0 12px;position:relative}
.page-timeline .tl-card:before{content:"";display:block;width:14px;height:14px;border:3px solid var(--black);border-radius:50%;background:var(--paper);margin:0 auto 20px}
.page-timeline .tl-card:first-child:before{background:var(--accent);border-color:var(--accent)}
.page-timeline .tl-card h3{font:700 14px/1.3 -apple-system,sans-serif;color:var(--ink);margin-bottom:4px}
.page-timeline .tl-card p{font:400 11px/1.5 -apple-system,sans-serif;color:var(--soft)}
.page-timeline .tl-route{display:flex;justify-content:center;align-items:center;gap:12px;margin-top:32px;padding:16px 24px;border:2px solid var(--black)}
.page-timeline .tl-route span{font:700 14px/1 -apple-system,sans-serif;color:var(--ink);letter-spacing:.04em}
.page-timeline .tl-route i{font:300 18px/1 serif;color:var(--accent)}
.page-timeline .tl-footer{display:flex;justify-content:space-between;margin-top:auto;padding-top:16px;border-top:1px solid var(--grey3);font:500 10px/1 -apple-system,sans-serif;color:var(--grey4);letter-spacing:.1em}

/* P7 SHOWCASE */
.page-showcase{background:var(--ink);color:var(--white);padding:52px 60px;display:flex;flex-direction:column}
.page-showcase .show-header{margin-bottom:40px}
.page-showcase .show-eyebrow{font:600 11px/1 -apple-system,sans-serif;letter-spacing:.3em;color:var(--gold);margin-bottom:14px}
.page-showcase h2{font:700 38px/1.1 -apple-system,sans-serif;color:var(--white);letter-spacing:-.02em}
.page-showcase h2 em{color:var(--gold);font-style:normal}
.page-showcase .show-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(255,255,255,.08);flex:1;margin-bottom:24px}
.page-showcase .show-card{padding:28px 28px;background:var(--ink);display:flex;flex-direction:column}
.page-showcase .show-card .show-num{font:900 40px/1 -apple-system,sans-serif;color:rgba(255,255,255,.1);margin-bottom:12px}
.page-showcase .show-card h3{font:700 15px/1.3 -apple-system,sans-serif;color:var(--white);margin-bottom:6px}
.page-showcase .show-card p{font:400 12px/1.55 -apple-system,sans-serif;color:rgba(255,255,255,.55)}
.page-showcase .show-panel{padding:20px 0 0;border-top:1px solid rgba(255,255,255,.1)}
.page-showcase .show-panel h3{font:600 12px/1.3 -apple-system,sans-serif;color:var(--gold);margin-bottom:4px}
.page-showcase .show-panel p{font:400 12px/1.55 -apple-system,sans-serif;color:rgba(255,255,255,.45)}
.page-showcase .show-footer{display:flex;justify-content:space-between;margin-top:auto;padding-top:16px;border-top:1px solid rgba(255,255,255,.08);font:500 10px/1 -apple-system,sans-serif;color:rgba(255,255,255,.25);letter-spacing:.1em}

/* P8 DASHBOARD */
.page-dashboard{background:var(--paper);padding:52px 60px;display:flex;flex-direction:column}
.page-dashboard .dash-header{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:32px}
.page-dashboard .dash-eyebrow{font:600 11px/1 -apple-system,sans-serif;letter-spacing:.25em;color:var(--soft)}
.page-dashboard h2{font:700 34px/1.1 -apple-system,sans-serif;color:var(--ink);letter-spacing:-.02em;margin-top:10px}
.page-dashboard .dash-warning-tag{font:700 10px/1 -apple-system,sans-serif;color:var(--white);background:var(--red);padding:8px 14px;letter-spacing:.15em}
.page-dashboard .dash-body{display:flex;gap:24px;flex:1}
.page-dashboard .dash-radar{flex:1;padding:24px;border:2px solid var(--black);display:flex;flex-direction:column;gap:16px;justify-content:center;position:relative}
.page-dashboard .dash-radar-row{display:flex;align-items:center;gap:12px}
.page-dashboard .dash-radar-row .dash-label{width:70px;font:600 11px/1 -apple-system,sans-serif;color:var(--soft);text-align:right}
.page-dashboard .dash-radar-row .dash-track{flex:1;height:8px;background:var(--grey2);position:relative}
.page-dashboard .dash-radar-row .dash-fill{position:absolute;left:0;top:0;height:100%;background:var(--accent)}
.page-dashboard .dash-radar-row .dash-val{width:28px;font:700 14px/1 -apple-system,sans-serif;color:var(--ink);text-align:right}
.page-dashboard .dash-right{flex:1;display:flex;flex-direction:column;gap:16px}
.page-dashboard .dash-warning{padding:20px;border:2px solid var(--red);background:rgba(192,57,43,.04);flex:1}
.page-dashboard .dash-warning h3{font:700 14px/1.3 -apple-system,sans-serif;color:var(--red);margin-bottom:12px}
.page-dashboard .dash-warning ul{list-style:none;padding:0}
.page-dashboard .dash-warning li{font:400 11.5px/1.5 -apple-system,sans-serif;color:var(--soft);padding:4px 0 4px 16px;position:relative}
.page-dashboard .dash-warning li:before{content:"—";position:absolute;left:0;color:var(--red)}
.page-dashboard .dash-panel{padding:16px;border:1px solid var(--grey3);background:var(--white)}
.page-dashboard .dash-panel h3{font:600 12px/1.3 -apple-system,sans-serif;color:var(--ink);margin-bottom:4px}
.page-dashboard .dash-panel p{font:400 11.5px/1.5 -apple-system,sans-serif;color:var(--soft)}
.page-dashboard .dash-footer{display:flex;justify-content:space-between;margin-top:auto;padding-top:16px;border-top:1px solid var(--grey3);font:500 10px/1 -apple-system,sans-serif;color:var(--grey4);letter-spacing:.1em}

/* P9 BACK COVER */
.page-backcover{background:linear-gradient(160deg,var(--cover2) 0%,var(--cover1) 40%,var(--cover1) 100%);color:var(--white);padding:0;display:flex;flex-direction:column}
.page-backcover:before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 70% 80%,rgba(255,255,255,.03),transparent 60%);pointer-events:none;z-index:0}
.page-backcover .back-inner{position:relative;z-index:1;flex:1;display:flex;flex-direction:column;padding:52px 60px}
.page-backcover .back-eyebrow{font:600 12px/1 -apple-system,sans-serif;letter-spacing:.35em;color:var(--gold);margin-bottom:28px;text-align:center}
.page-backcover .back-title{text-align:center;margin-bottom:40px}
.page-backcover .back-title h2{font:700 32px/1.15 "Songti SC",serif;color:var(--white)}
.page-backcover .back-title h2 em{color:var(--gold);font-style:normal}
.page-backcover .back-verdict{text-align:center;padding:32px 40px;margin-bottom:24px;border:2px solid rgba(255,255,255,.15);background:rgba(0,0,0,.3)}
.page-backcover .back-verdict .back-score{font:900 64px/1 "Songti SC",serif;color:var(--gold);margin-bottom:8px}
.page-backcover .back-verdict .back-grade{font:600 14px/1 -apple-system,sans-serif;color:rgba(255,255,255,.7);letter-spacing:.15em;margin-bottom:16px}
.page-backcover .back-verdict .back-text{font:400 13px/1.6 -apple-system,sans-serif;color:rgba(255,255,255,.6);max-width:480px;margin:0 auto}
.page-backcover .back-audience{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}
.page-backcover .back-audience>div{padding:20px 24px;border:1px solid rgba(255,255,255,.1)}
.page-backcover .back-audience h3{font:700 12px/1 -apple-system,sans-serif;color:var(--gold);letter-spacing:.1em;margin-bottom:10px}
.page-backcover .back-audience ul{list-style:none;padding:0}
.page-backcover .back-audience li{font:400 11px/1.5 -apple-system,sans-serif;color:rgba(255,255,255,.5);padding:3px 0}
.page-backcover .back-why{padding:20px 24px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.03)}
.page-backcover .back-why h3{font:600 12px/1 -apple-system,sans-serif;color:var(--gold);letter-spacing:.1em;margin-bottom:8px}
.page-backcover .back-why p{font:400 12px/1.55 -apple-system,sans-serif;color:rgba(255,255,255,.45)}
.page-backcover .back-footer{display:flex;justify-content:space-between;margin-top:auto;padding-top:16px;border-top:1px solid rgba(255,255,255,.1);font:500 10px/1 -apple-system,sans-serif;color:rgba(255,255,255,.25);letter-spacing:.1em}

/* BRAND */
.brand{font-weight:400;color:var(--grey4);margin-left:3px;letter-spacing:.04em}
.page-cover .brand{color:rgba(255,255,255,.35)}
.page-backcover .brand{color:rgba(255,255,255,.3)}
</style></head>
<body>
<script>{{REVIEW_DATA}}</script>
<script>
(function(){
  var D=window.__BOOK_DATA__;
  if(!D){var s=document.createElement('script');s.src='review.js';s.onload=function(){if(window.__BOOK_DATA__)init(window.__BOOK_DATA__)};s.onerror=function(){document.body.innerHTML='<p style="color:#fff;padding:40px;font-family:sans-serif">review.js 未加载。<br>请将 review.js 与此 HTML 放在同一目录后刷新。</p>'};document.head.appendChild(s);return}
  init(D)
})();
function init(D){
  document.body.dataset.theme=D.theme||'literary-red';
  var E=function(s){return String(s||'').replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
  var MT=function(p){var r=String(p.title||''),m=String(p.highlight||'');if(!m||r.indexOf(m)<0)return E(r);return r.split(m).map(E).join('<em>'+E(m)+'</em>')};
  var SV=function(x){return typeof x==='string'?x:(x.label||x.title||x.text||x.value||'')};
  var T=D.pages.length;

  function P1(p){
    var tags=(p.blocks||[]).filter(function(b){return b.kind==='tags'}).reduce(function(a,b){return a.concat(b.items||[])},[]);
    var q=(p.blocks||[]).find(function(b){return b.kind==='quote'});
    var l=(p.blocks||[]).find(function(b){return b.kind==='lede'});
    return '<div class="page page-cover"><div class="cover-inner">'+
      '<div class="cover-eyebrow">'+E(p.eyebrow||'')+'</div>'+
      '<h1>'+MT(p)+'</h1>'+
      (q?'<div class="cover-quote">'+E(q.text)+'</div>':'')+
      (l?'<div class="cover-lede">'+E(l.text)+'</div>':'')+
      '</div>'+
      '<div class="cover-footer"><div class="cover-tags">'+tags.map(function(t){return'<span>'+E(SV(t))+'</span>'}).join('')+'</div><span class="cover-num">1 / '+T+'<span class="brand">popwave</span></span></div>'+
      '<div class="cover-deco-book deco-icon"><svg viewBox="0 0 48 48"><rect x="4" y="6" width="18" height="34" rx="1" fill="none" stroke="var(--gold)" stroke-width="1.5" opacity=".6"/><rect x="26" y="6" width="18" height="34" rx="1" fill="none" stroke="var(--gold)" stroke-width="1.5" opacity=".3"/><line x1="13" y1="16" x2="22" y2="14" stroke="var(--gold)" stroke-width=".8" opacity=".4"/><line x1="13" y1="24" x2="22" y2="22" stroke="var(--gold)" stroke-width=".8" opacity=".4"/><line x1="30" y1="16" x2="39" y2="14" stroke="var(--gold)" stroke-width=".8" opacity=".25"/><line x1="30" y1="24" x2="39" y2="22" stroke="var(--gold)" stroke-width=".8" opacity=".25"/></svg></div>'+
      '<div class="cover-overlay"></div></div>'
  }

  function P2(p){
    var cards=(p.blocks||[]).filter(function(b){return b.kind==='cards'}).reduce(function(a,b){return a.concat(b.items||[])},[]).slice(0,4);
    var panel=(p.blocks||[]).find(function(b){return b.kind==='panel'});
    var cells='';for(var i=0;i<4;i++){var c=cards[i]||{};cells+='<div class="swiss-cell"><div class="swiss-num">0'+(i+1)+'</div><h3>'+E(c.title||'')+'</h3><p>'+E(c.text||'')+'</p></div>'}
    return '<div class="page page-swiss">'+
      '<div class="swiss-header"><div class="swiss-eyebrow">'+E(p.eyebrow||'')+'</div><h2>'+MT(p)+'</h2></div>'+
      '<div class="swiss-grid">'+cells+'</div>'+
      (panel?'<div class="swiss-panel"><h3>'+E(panel.title)+'</h3><p>'+E(panel.text)+'</p></div>':'')+
      '<div class="swiss-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div>'
  }

  function P3(p){
    var steps=(p.blocks||[]).filter(function(b){return b.kind==='steps'}).reduce(function(a,b){return a.concat(b.items||[])},[]);
    var panel=(p.blocks||[]).find(function(b){return b.kind==='panel'});
    var stepsHtml=steps.map(function(s,i){return'<div class="mag-step"><h3>'+E(s.title)+'</h3><p>'+E(s.text||'')+'</p></div>'}).join('');
    return '<div class="page page-magazine">'+
      '<div class="mag-left"><div class="mag-eyebrow">'+E(p.eyebrow||'')+'</div><div class="mag-section">'+('0'+p.page_no).slice(-2)+'</div></div>'+
      '<div class="mag-right"><h2>'+MT(p)+'</h2><div class="mag-steps">'+stepsHtml+'</div>'+
      (panel?'<div class="mag-panel"><h3>'+E(panel.title)+'</h3><p>'+E(panel.text)+'</p></div>':'')+
      '<div class="mag-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div></div>'
  }

  function P4(p){
    var cards=(p.blocks||[]).filter(function(b){return b.kind==='cards'}).reduce(function(a,b){return a.concat(b.items||[])},[]).slice(0,4);
    var panel=(p.blocks||[]).find(function(b){return b.kind==='panel'});
    var cardsHtml=cards.map(function(c){
      var id=c.title||'';var text=c.text||'';
      var parts=text.split('。');var identity=parts[0]||'';var rest=parts.slice(1).join('。');
      return'<div class="prof-card"><div class="prof-name">'+E(id)+'</div><div class="prof-identity">'+E(identity)+'</div><div class="prof-drive">'+E(rest)+'</div></div>'
    }).join('');
    return '<div class="page page-profiles">'+
      '<div class="prof-header"><div><div class="prof-eyebrow">'+E(p.eyebrow||'')+'</div><h2>'+MT(p)+'</h2></div></div>'+
      '<div class="prof-grid">'+cardsHtml+'</div>'+
      (panel?'<div class="prof-panel"><h3>'+E(panel.title)+'</h3><p>'+E(panel.text)+'</p></div>':'')+
      '<div class="prof-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div>'
  }

  function P5(p){
    var formula=(p.blocks||[]).find(function(b){return b.kind==='formula'});
    var cards=(p.blocks||[]).filter(function(b){return b.kind==='cards'}).reduce(function(a,b){return a.concat(b.items||[])},[]).slice(0,2);
    var panel=(p.blocks||[]).find(function(b){return b.kind==='panel'});
    var f=(formula&&formula.items||[]);
    var fHtml=f.length?f.map(function(x,i){return(i?'<i>×</i>':'')+'<span>'+E(SV(x))+'</span>'}).join(''):'';
    return '<div class="page page-infographic">'+
      '<div class="info-header"><div class="info-eyebrow">'+E(p.eyebrow||'')+'</div><h2>'+MT(p)+'</h2></div>'+
      '<div class="info-diagram"><div class="info-center">'+(fHtml?'<div class="info-formula">'+fHtml+'</div>':'')+'</div></div>'+
      (cards.length?'<div class="info-cards">'+cards.map(function(c){return'<div class="info-card"><h3>'+E(c.title)+'</h3><p>'+E(c.text||'')+'</p></div>'}).join('')+'</div>':'')+
      (panel?'<div class="info-panel"><h3>'+E(panel.title)+'</h3><p>'+E(panel.text)+'</p></div>':'')+
      '<div class="info-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div>'
  }

  function P6(p){
    var cards=(p.blocks||[]).filter(function(b){return b.kind==='cards'}).reduce(function(a,b){return a.concat(b.items||[])},[]).slice(0,4);
    var route=(p.blocks||[]).find(function(b){return b.kind==='route'});
    var r=(route&&route.items||[]);
    return '<div class="page page-timeline">'+
      '<div class="tl-header"><div class="tl-eyebrow">'+E(p.eyebrow||'')+'</div><h2>'+MT(p)+'</h2></div>'+
      '<div class="tl-track"><div class="tl-cards">'+cards.map(function(c){return'<div class="tl-card"><h3>'+E(c.title)+'</h3><p>'+E(c.text||'')+'</p></div>'}).join('')+'</div></div>'+
      (r.length?'<div class="tl-route">'+r.map(function(x,i){return(i?'<i>→</i>':'')+'<span>'+E(SV(x))+'</span>'}).join('')+'</div>':'')+
      '<div class="tl-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div>'
  }

  function P7(p){
    var cards=(p.blocks||[]).filter(function(b){return b.kind==='cards'}).reduce(function(a,b){return a.concat(b.items||[])},[]);
    var panel=(p.blocks||[]).find(function(b){return b.kind==='panel'});
    return '<div class="page page-showcase">'+
      '<div class="show-deco-grid deco-icon"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="none" stroke="var(--gold)" stroke-width=".5" opacity=".5"/><circle cx="20" cy="20" r="14" fill="none" stroke="var(--gold)" stroke-width=".5" opacity=".35"/><circle cx="20" cy="20" r="9" fill="none" stroke="var(--gold)" stroke-width=".5" opacity=".2"/><line x1="20" y1="1" x2="20" y2="39" stroke="var(--gold)" stroke-width=".3" opacity=".15"/><line x1="1" y1="20" x2="39" y2="20" stroke="var(--gold)" stroke-width=".3" opacity=".15"/></svg></div>'+
      '<div class="show-header"><div class="show-eyebrow">'+E(p.eyebrow||'')+'</div><h2>'+MT(p)+'</h2></div>'+
      '<div class="show-grid">'+cards.map(function(c,i){return'<div class="show-card"><div class="show-num">'+('0'+(i+1)).slice(-2)+'</div><h3>'+E(c.title)+'</h3><p>'+E(c.text||'')+'</p></div>'}).join('')+'</div>'+
      (panel?'<div class="show-panel"><h3>'+E(panel.title)+'</h3><p>'+E(panel.text)+'</p></div>':'')+
      '<div class="show-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div>'
  }

  function P8(p){
    var radar=(p.blocks||[]).find(function(b){return b.kind==='radar'});
    var warning=(p.blocks||[]).find(function(b){return b.kind==='warning'});
    var panel=(p.blocks||[]).find(function(b){return b.kind==='panel'});
    var ri=(radar&&radar.items||[]);
    var wi=(warning&&warning.items||[]);
    return '<div class="page page-dashboard">'+
      '<div class="dash-header"><div><div class="dash-eyebrow">'+E(p.eyebrow||'')+'</div><h2>'+MT(p)+'</h2></div><div class="dash-warning-tag">'+E((warning||{}).title||'阅读门槛')+'</div></div>'+
      '<div class="dash-body"><div class="dash-radar">'+ri.map(function(x){var v=Math.max(0,Math.min(10,Number(x.value)||0));return'<div class="dash-radar-row"><span class="dash-label">'+E(x.label)+'</span><div class="dash-track"><div class="dash-fill" style="width:'+(v*10)+'%"></div></div><span class="dash-val">'+v+'</span></div>'}).join('')+
      '<div class="dash-deco-chart deco-icon"><svg viewBox="0 0 24 24"><polyline points="2,20 8,14 12,16 18,6 22,10" fill="none" stroke="var(--soft)" stroke-width="1.2" stroke-linejoin="round"/><circle cx="8" cy="14" r="2" fill="var(--soft)" opacity=".3"/><circle cx="18" cy="6" r="2" fill="var(--soft)" opacity=".3"/></svg></div></div>'+
      '<div class="dash-right"><div class="dash-warning"><h3>⚠ 明确阅读门槛</h3><ul>'+wi.map(function(x){return'<li>'+E(SV(x))+'</li>'}).join('')+'</ul></div>'+
      (panel?'<div class="dash-panel"><h3>'+E(panel.title)+'</h3><p>'+E(panel.text)+'</p></div>':'')+'</div></div>'+
      '<div class="dash-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div>'
  }

  function P9(p){
    var audience=(p.blocks||[]).find(function(b){return b.kind==='audience'});
    var verdict=(p.blocks||[]).find(function(b){return b.kind==='verdict'});
    var panel=(p.blocks||[]).find(function(b){return b.kind==='panel'});
    var aud=audience&&audience.items||{};
    var rec=aud.recommended||[];var avo=aud.avoid||[];
    var vTitle=verdict?verdict.title:'';var vText=verdict?verdict.text:'';
    var scoreMatch=vTitle.match(/[\d.]+/g);
    return '<div class="page page-backcover"><div class="back-inner">'+
      '<div class="back-eyebrow">'+E(p.eyebrow||'')+'</div>'+
      '<div class="back-title"><h2>'+MT(p)+'</h2></div>'+
      '<div class="back-verdict">'+
      '<div class="back-deco-star deco-icon"><svg viewBox="0 0 100 20">'+
        (function(){var s='';for(var i=0;i<5;i++)s+='<polygon points="'+(10+i*20)+',1 '+(13+i*20)+',6.5 '+(19+i*20)+',8.5 '+(14+i*20)+',13.5 '+(15+i*20)+',19.5 '+(10+i*20)+',16.8 '+(5+i*20)+',19.5 '+(6+i*20)+',13.5 '+(1+i*20)+',8.5 '+(7+i*20)+',6.5" fill="var(--gold)" opacity=".8"/>';return s})()+
      '</svg></div>'+
      (scoreMatch?'<div class="back-score">'+scoreMatch.join('–')+'</div>':'')+'<div class="back-grade">'+E(p.footer||'')+'</div><div class="back-text">'+E(vText)+'</div></div>'+
      '<div class="back-audience"><div><h3>✓ 推荐给</h3><ul>'+rec.map(function(x){return'<li>'+E(x)+'</li>'}).join('')+'</ul></div><div><h3>✗ 不推荐给</h3><ul>'+avo.map(function(x){return'<li>'+E(x)+'</li>'}).join('')+'</ul></div></div>'+
      (panel?'<div class="back-why"><h3>'+E(panel.title)+'</h3><p>'+E(panel.text)+'</p></div>':'')+
      '<div class="back-footer"><span>'+E(p.footer||'')+'</span><span>'+p.page_no+' / '+T+'<span class="brand">popwave</span></span></div></div></div>'
  }

  var renderers={cover:P1,hook:P2,synopsis:P3,characters:P4,chemistry:P5,structure:P6,selling_points:P7,risks:P8,verdict:P9};
  document.body.insertAdjacentHTML('beforeend',D.pages.map(function(p){var fn=renderers[p.type];return fn?fn(p):P2(p)}).join(''))
}
</script>
</body>
</html>
```

---

## 完成

HTML 落盘后直接打开验证。链式管线结束。
