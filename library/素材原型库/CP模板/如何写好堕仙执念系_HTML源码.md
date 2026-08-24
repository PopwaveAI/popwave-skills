# 如何写好堕仙执念系｜HTML 源码

原始文件：v38_如何写好堕仙执念系_新版交付包.html

````html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>如何写好堕仙执念系｜硬核结构融合版｜猫的咪 v38｜新版交付包</title>
  <style>
    :root{--ink:#302729;--sub:#6f6261;--rose:#d77786;--deep:#ad4a60;--line:rgba(201,116,126,.25);--paper:rgba(255,251,247,.91);--serif:"Songti SC","STSong",serif;--sans:"PingFang SC","Microsoft YaHei",sans-serif}
    *{box-sizing:border-box}body{margin:0;background:#eadbd4;color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}.toolbar{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:14px 24px;background:rgba(64,48,50,.94);color:#fff}.toolbar button{border:1px solid #ffffff80;border-radius:99px;padding:8px 18px;background:transparent;color:#fff}.toolbar span{opacity:.72;margin-left:8px}
    main{display:grid;justify-content:center;gap:40px;padding:48px 24px 80px}.page{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff8f3 center/cover no-repeat;box-shadow:0 22px 58px #5c423e2e}.cover{background-image:url("../../../assets/maodemi-cover-bg.png")}.content{background-image:url("../../../assets/maodemi-content-bg.png")}
    .brand{position:absolute;left:72px;top:62px;display:flex;align-items:center;gap:18px;color:var(--sub);font-size:26px;font-weight:800}.brand img{width:74px;height:74px;border-radius:50%;object-fit:contain;border:4px solid #ffffffe0;box-shadow:0 8px 20px #9c6f6b2e}.page-no{position:absolute;top:68px;right:72px;min-width:76px;height:48px;display:grid;place-items:center;border:2px solid #d879865c;border-radius:99px;color:var(--deep);background:#ffffff94;font:700 24px/1 Georgia}
    .sheet{position:absolute;inset:132px 64px 260px;display:flex;flex-direction:column;padding:28px 6px 18px}.topic{flex:none;margin:4px 0 22px;padding-bottom:18px;border-bottom:3px solid var(--line)}.topic-label{display:inline-flex;align-items:center;height:44px;padding:0 20px;border-radius:99px;color:var(--deep);background:#ffffffa8;font-size:22px;font-weight:900}.topic h2{margin:17px 0 0;font:900 62px/1.15 var(--serif)}.topic p{margin:12px 0 0;color:var(--sub);font:800 29px/1.42 var(--serif)}
    .cover-copy{position:absolute;left:74px;right:74px;top:420px;text-align:center}.kicker{margin:0 0 26px;color:var(--deep);font-size:38px;font-weight:900}.cover h1{margin:0;font:900 126px/1.08 var(--serif)}.cover h1 em{display:block;color:var(--deep);font-style:normal;font-size:168px}.cover-sub{max-width:900px;margin:38px auto 0;color:#5a5050;font:800 38px/1.5 var(--serif)}.cover-hook{max-width:860px;margin:48px auto 0;padding:22px 28px;border-top:4px solid #d87986a8;border-bottom:4px solid #d87986a8;font:800 29px/1.58 var(--serif)}
    .footer{position:absolute;left:76px;right:76px;bottom:34px;display:flex;align-items:center;justify-content:space-between;color:#8a7b7b;font-size:20px;font-weight:800}.mini-brand{display:flex;align-items:center;gap:10px}.mini-brand img{width:40px;height:40px;border-radius:50%}.popwave{width:324px;height:auto;display:block;flex:none}
    .formula{margin:4px 0 22px;padding:30px 34px;border:3px solid #cf7c884d;border-radius:30px;background:#fffaf4e8;text-align:center;box-shadow:0 14px 30px #80524f15}.formula b{display:block;color:var(--deep);font:900 30px/1.2 var(--sans)}.formula strong{display:block;margin-top:14px;font:900 45px/1.35 var(--serif)}.formula p{margin:14px 0 0;color:var(--sub);font:800 27px/1.5 var(--serif)}
    .grid{display:grid;gap:18px;flex:1;min-height:0}.grid.two{grid-template-columns:1fr 1fr}.grid.three{grid-template-columns:1fr}.card{padding:25px 28px;border:2px solid var(--line);border-radius:25px;background:var(--paper);box-shadow:0 12px 30px #80524f1c}.card .eyebrow{display:block;margin-bottom:9px;color:var(--deep);font-size:24px;font-weight:900}.card h3{margin:0 0 11px;font:900 36px/1.25 var(--serif)}.card p{margin:0;font:700 27px/1.5 var(--serif)}.card ul{margin:10px 0 0;padding-left:1.15em}.card li{margin:8px 0;font:700 26px/1.45 var(--serif)}.card strong{color:var(--deep)}
    .compare{display:grid;grid-template-columns:1fr 1fr;gap:18px}.compare .bad{border-color:#8b858034}.compare .good{border-color:#cc77854f;background:#fffaf5}.flag{display:inline-block;margin-bottom:12px;padding:7px 14px;border-radius:99px;background:#f4e1df;color:#8c6060;font-size:21px;font-weight:900}.good .flag{background:#efd4d8;color:var(--deep)}
    .steps{display:grid;gap:15px;flex:1;grid-auto-rows:1fr}.step{display:grid;grid-template-columns:70px 1fr;gap:17px;align-items:center;padding:18px 24px;border:2px solid var(--line);border-radius:24px;background:var(--paper)}.step .num{display:grid;place-items:center;width:58px;height:58px;border-radius:50%;background:#f2d6da;color:var(--deep);font:900 25px/1 Georgia}.step h3{margin:0 0 5px;font:900 30px/1.3 var(--serif)}.step p{margin:0;font:700 25px/1.42 var(--serif)}
    .scene-stack{display:grid;gap:18px;flex:1;grid-auto-rows:1fr}.scene{padding:25px 29px;border:2px solid var(--line);border-radius:26px;background:var(--paper)}.scene h3{margin:0 0 11px;color:var(--deep);font:900 34px/1.3 var(--serif)}.scene p{margin:0;font:700 26px/1.5 var(--serif)}.scene .beat{display:block;margin-top:10px;padding-top:10px;border-top:2px dashed var(--line);color:#675657;font-size:24px;font-weight:800}
    .map-title{margin:36px 0 22px;padding:22px;border-radius:30px;background:#ffffffa5;border:2px solid var(--line);text-align:center}.map-title h2{margin:0;font:900 65px/1.15 var(--serif)}.map-title p{margin:10px 0 0;color:var(--sub);font:800 26px/1.4 var(--serif)}.map-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.map-grid .card{min-height:182px}.map-grid .card h3{font-size:30px}.map-grid .card p{font-size:25px}.signoff{display:grid;grid-template-columns:190px 1fr;align-items:center;gap:22px;margin:22px auto 0;padding:14px 26px;border-radius:28px;background:#ffffffad;border:2px solid var(--line)}.signoff img{width:180px;height:200px;object-fit:cover}.signoff p{margin:0;color:#7a4c55;font:900 28px/1.5 var(--serif)}
    .tip{margin-top:16px;padding:17px 22px;border-left:6px solid var(--rose);border-radius:0 18px 18px 0;background:#fff9f4d9;color:#675657;font:800 25px/1.45 var(--serif)}
    /* v38：单一主图 + 完整论证 + 证据/风险边界，保留猫的咪视觉壳 */
    .mechanism-board{max-width:900px;margin:44px auto 0;padding:34px 36px 30px;border:3px solid #cf7c884d;background:#fffaf4d9;box-shadow:0 18px 38px #80524f15;text-align:left}.mechanism-board h3{margin:0 0 24px;text-align:center;color:var(--deep);font:900 32px/1.25 var(--serif)}.mechanism-flow{display:grid;grid-template-columns:1fr 46px 1fr 46px 1fr;align-items:center;gap:8px}.mechanism-node{min-height:128px;display:grid;place-items:center;padding:16px;border:2px solid var(--line);background:#fffdf9;color:var(--ink);font:900 28px/1.35 var(--serif);text-align:center}.mechanism-node strong{display:block;color:var(--deep);font-size:32px}.mechanism-arrow{color:var(--deep);font:900 42px/1 var(--serif);text-align:center}.mechanism-result{margin-top:18px;padding:16px 20px;background:#f2d6da99;color:#6f3e49;font:900 25px/1.45 var(--serif);text-align:center}
    .argument{padding:28px 32px;border:2px solid var(--line);background:var(--paper)}.argument p{margin:0 0 18px;font:700 28px/1.58 var(--serif);text-align:justify}.argument p:last-child{margin-bottom:0}.argument strong,.mark{color:var(--deep);font-weight:900;background:linear-gradient(transparent 58%,#efd4d8 58%)}
    .evidence-row{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:start;padding:22px 26px;border-bottom:2px solid var(--line);background:#fffaf4d9}.evidence-row:last-child{border-bottom:0}.evidence-row b{color:var(--deep);font:900 25px/1.35 var(--sans)}.evidence-row p{margin:0;font:700 26px/1.52 var(--serif)}
    .logic-table{width:100%;border-collapse:collapse;background:#fffaf4dc;font:700 25px/1.48 var(--serif)}.logic-table th,.logic-table td{padding:20px 22px;border:2px solid var(--line);vertical-align:top;text-align:left}.logic-table th{width:180px;color:#fff;background:#b85f72;font:900 25px/1.3 var(--sans)}.logic-table td strong{color:var(--deep)}
    .risk-box{margin-top:18px;padding:22px 26px;border:2px solid #d3ae5e80;background:#fff4d6b8;color:#67533f;font:800 25px/1.5 var(--serif)}.risk-box b{color:#9a5b3c}
    @media(max-width:1160px){main{display:block;padding:24px 0 64px}.page{margin:0 auto 28px;transform-origin:top center}}@media print{@page{size:1080px 1920px;margin:0}body{background:#fff}.toolbar{display:none}main{display:block;padding:0}.page{margin:0;box-shadow:none;break-after:page}}

  .alt-cover{overflow:hidden;border-radius:58px;background:#8f0b0e;color:#fffaf0;isolation:isolate}
  .alt-cover::before{content:"";position:absolute;inset:-12%;z-index:-2;background:
    radial-gradient(ellipse at 18% 10%,rgba(203,54,43,.24),transparent 32%),
    radial-gradient(ellipse at 72% 58%,rgba(35,0,2,.34),transparent 46%),
    radial-gradient(ellipse at 28% 88%,rgba(91,0,6,.34),transparent 38%),
    linear-gradient(126deg,#73080b 0%,#a30e12 42%,#81080c 100%);filter:saturate(.84) contrast(1.06)}
  .alt-cover::after{content:"";position:absolute;inset:0;z-index:-1;opacity:.42;mix-blend-mode:soft-light;background-image:
    repeating-radial-gradient(circle at 17% 23%,rgba(255,238,218,.13) 0 1px,transparent 1px 4px),
    repeating-linear-gradient(7deg,transparent 0 8px,rgba(24,0,1,.13) 8px 10px);filter:contrast(1.8)}
  .alt-title{position:absolute;inset:46px 30px 84px 42px;font-family:"Songti SC","STSong","SimSun",serif;font-weight:900;text-shadow:-3px 2px 0 rgba(255,255,255,.22),3px 5px 1px rgba(70,0,0,.18)}
  .alt-kicker{position:absolute;left:-4px;top:0;margin:0;font-size:92px;line-height:.95;font-weight:900;letter-spacing:-7px;white-space:nowrap;transform:scaleX(.98) rotate(-1.3deg);transform-origin:left top}
  .alt-line{position:absolute;margin:0;font-weight:900;letter-spacing:-28px;white-space:nowrap;transform-origin:left center}
  .alt-line.one{left:-18px;top:208px;font-size:372px;line-height:.82;transform:scaleX(.86) rotate(-2.4deg)}
  .alt-line.second{left:-30px;top:720px;font-size:386px;line-height:.82;transform:scaleX(.88) rotate(1.2deg)}
  .alt-tail{position:absolute;right:-44px;bottom:150px;margin:0;font-size:268px;line-height:.83;font-weight:900;letter-spacing:-24px;white-space:nowrap;transform:scaleX(.91) rotate(-3.4deg);transform-origin:right bottom}
  .alt-attribution{position:absolute;right:28px;bottom:20px;width:190px;height:auto;filter:grayscale(1) brightness(0) invert(1);opacity:.38}
  .alt-brand{position:absolute;left:34px;bottom:26px;display:flex;align-items:center;gap:10px;padding:8px 15px 8px 9px;border-radius:999px;background:rgba(83,0,0,.30);font:900 24px/1 "Songti SC","STSong",serif;color:#fffdf3;box-shadow:inset 0 0 0 1px rgba(255,255,255,.22)}
  .alt-brand img{width:42px;height:42px;border-radius:50%;object-fit:cover;border:1px solid rgba(255,255,255,.72)}
</style>
</head>
<body>
  <header class="toolbar"><div><strong>猫的咪图文预览</strong><span>v38 · 9页 · 1080×1920 · 硬核结构融合</span></div><button onclick="window.print()">打印 / 导出 PDF</button></header>
  <main>
    <section class="page cover">
      <div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">1/9</span>
      <div class="cover-copy"><p class="kicker">如何写好一个设定之</p><h1>堕仙<em>执念系</em></h1><p class="cover-sub">成仙旧愿｜执念禁区｜反噬代价</p><div class="mechanism-board"><h3>一眼看懂：堕仙不是变坏，是选择不断越界</h3><div class="mechanism-flow"><div class="mechanism-node"><span><strong>守戒</strong>曾为众生克己</span></div><div class="mechanism-arrow">→</div><div class="mechanism-node"><span><strong>徇私</strong>为一人开例外</span></div><div class="mechanism-arrow">→</div><div class="mechanism-node"><span><strong>反噬</strong>代价持续追债</span></div></div><div class="mechanism-result">追读问题：他会为执念走到哪一步，她又会不会接受这种“被救”？</div></div></div>
      <footer class="footer"><span>猫的咪｜网文素材积累</span><img class="popwave" src="../../../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由 AI Agent Popwave.cn 生成"></footer>
    </section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">2/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">先钉住核心</span><h2>堕仙的“堕”，要是他亲手选的</h2><p>天罚只能砸坏仙骨。真正把人拖下神坛的，是他明知会失去什么，仍把手伸向禁区。</p></header>
      <div class="formula"><b>设定公式</b><strong>昔日仙格 × 唯一执念 × 越界选择 × 持续反噬</strong><p>先写他曾守住什么，再写这一次为何偏偏守不住。</p></div>
      <div class="argument"><p><strong>先钉住旧秩序。</strong>他过去必须真心相信众生平等、因果不可逆、私情不可凌驾苍生，而且用行动守过这些规矩。读者见过他的自律，后来那一次徇私才会像裂缝，而不是换皮疯批。</p><p><strong>再给唯一例外一个不可替代的来处。</strong>可以是一个人、一段旧约、一座已亡的城，也可以是他唯一没能兑现的承诺。例外越具体，他每次越界的理由越能成立。</p></div>
      <div class="evidence-row"><b>状态变化</b><p>“守戒的仙”变成“替一个人改写戒律的人”，身份和判断权同时位移。</p></div><div class="evidence-row"><b>持续代价</b><p>仙骨裂、功德散、故人惧他，代价必须逐页追债，不能只在结尾补一场雷劫。</p></div>
      <div class="risk-box"><b>翻车边界：</b>如果他从登场起就无差别发疯，读者只能看到危险，看不到“堕”发生在哪里。</div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>核心公式</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">3/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">三层执念</span><h2>他嘴上想救人，心里未必只想救</h2><p>执念越往里挖，越不能只剩“爱得太深”。把愿望、恐惧和私心分开写。</p></header>
      <table class="logic-table"><tbody>
        <tr><th>表层愿望</th><td><strong>“我要她回来”要立刻变成任务。</strong>聚魂、改命、偷生死簿、截天劫、养一具能承魂的身体；只要目标能推动行动，执念才会把剧情往前拽。</td></tr>
        <tr><th>深层恐惧</th><td><strong>他怕的不是死亡，而是再次承认自己无能为力。</strong>他既怕当年没救下她，也怕她醒来后不再需要自己，于是“保护”一点点长成囚笼。</td></tr>
        <tr><th>隐藏私心</th><td><strong>她必须仍是旧日的她。</strong>转世者有新名字、新爱恨和新选择；他若执意抹去这些，想复活的其实不是她，而是自己不肯结束的过去。</td></tr>
      </tbody></table>
      <div class="argument"><p><strong>三层不能只是同一句爱的扩写。</strong>表层负责制造任务，深层负责解释失控，私心负责让关系产生反弹。她一旦拒绝被还原成旧人，他的“救”就会第一次遭遇真正的审判。</p></div>
      <div class="formula"><b>执念纵深</b><strong>想救她 → 怕失去她 → 不许她成为别人</strong></div>
      <div class="evidence-row"><b>场景证据</b><p>让她亲手改掉旧日习惯、烧掉前世遗物，或直说“我不是你等的那个人”。他如何回应，才是私心有没有被揭开的证据。</p></div>
      <div class="evidence-row"><b>关系变化</b><p>她从“被拯救者”变成“审判这场拯救的人”；他第一次发现，复活一个人并不等于有权替她决定余生。</p></div>
      <div class="risk-box"><b>迁移动作：</b>换题材时保留三层功能即可。现代文可以把聚魂换成找回失忆爱人，把生死簿换成被篡改的医疗记录，执念结构仍然成立。</div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>三层执念</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">4/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">堕落要有台阶</span><h2>用四次选择，写完他从仙到魔</h2><p>每次都给他退路。他每次都能停，却一次比一次更舍不得停。</p></header>
      <div class="steps">
        <article class="step"><span class="num">01</span><div><h3>第一次：偷偷留下一缕残魂</h3><p>他骗自己只为替她收尸。代价很轻，只违了一条不得扰亡魂的戒律。</p></div></article>
        <article class="step"><span class="num">02</span><div><h3>第二次：借无辜者的命灯养魂</h3><p>他仍给自己找理由：只借十日，事后会偿。被借走的人却开始忘记亲人。</p></div></article>
        <article class="step"><span class="num">03</span><div><h3>第三次：改掉她这一世的命数</h3><p>她本可平安长大，他却毁掉婚约、师门与名字，只为把她逼回自己身边。</p></div></article>
        <article class="step"><span class="num">04</span><div><h3>最后一次：拿苍生替她挡天劫</h3><p>走到这里，他终于不再辩解。天若不肯还她，他便让三界一起欠这条命。</p></div></article>
      </div><div class="tip">堕落升级看三件事：伤及的人更远、借口更短、回头路更少。</div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>四次越界</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">5/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">把神性写具体</span><h2>先让读者见过他没堕落的样子</h2><p>没有旧日的克制与慈悲，后来的偏执只会像普通疯批换了套仙侠衣裳。</p></header>
      <div class="grid three">
        <article class="card"><span class="eyebrow">旧日边界</span><h3>他曾经最守规矩</h3><p>过忘川不看故魂，听祈愿不徇私，宁损百年修为也不拿凡人填阵。规矩要有动作证明。</p></article>
        <article class="card"><span class="eyebrow">唯一裂缝</span><h3>她碰过他最软的一处</h3><p>也许她曾替他挡下一场因果，或在所有人拜神时，只问他冷不冷。她给过的东西必须无可替代。</p></article>
        <article class="card"><span class="eyebrow">堕后残响</span><h3>恶里还留着旧习惯</h3><p>他屠尽追兵，却避开她怕的血腥；锁她入殿，仍夜夜替她点凡间旧灯。矛盾比纯狠更扎心。</p></article>
      </div>
      <div class="formula"><b>反差落点</b><strong>过去他为众生克己，如今他为一人徇私</strong><p>神性没有凭空消失，只是被他亲手缩成了一个人的范围。</p></div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>神性反差</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">6/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">7种执念动作</span><h2>别总让他靠掐脖子证明偏执</h2><p>挑三四种反复出现，让执念进入他的身体、法术、习惯和判断。</p></header>
      <div class="steps">
        <article class="step"><span class="num">01</span><div><h3>记住无人会记的小事</h3><p>她转世后换了容貌，他仍知道她怕雷、先吃甜口、撒谎时会摸袖边。</p></div></article>
        <article class="step"><span class="num">02</span><div><h3>把天地异象当成她的病历</h3><p>星盘乱一寸，他便知道她今夜又做了前世的梦。</p></div></article>
        <article class="step"><span class="num">03</span><div><h3>重复失败过的救法</h3><p>同一座阵摆了三百年，每次都只差她最后一缕魂。</p></div></article>
        <article class="step"><span class="num">04</span><div><h3>替她抹掉不喜欢的命运</h3><p>未婚夫、师门、朋友一一离开，她以为是天意，其实是他。</p></div></article>
        <article class="step"><span class="num">05</span><div><h3>收集她每一世的遗物</h3><p>凡人的木簪、旧鞋、药方，与仙器并排供在无人能进的殿中。</p></div></article>
        <article class="step"><span class="num">06</span><div><h3>容忍她伤自己</h3><p>她的剑穿心时他不躲，只握住剑锋问：这一回，你记起我了吗？</p></div></article>
        <article class="step"><span class="num">07</span><div><h3>在最失控时叫旧称</h3><p>众人面前他喊她今生姓名，只有神识崩裂时，才唤那声三百年前的小字。</p></div></article>
      </div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>执念动作库</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">7/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">3组正误对照</span><h2>别把堕仙写成仙界版霸总</h2><p>境界再高，也不能拿强取豪夺替代人物变化。</p></header>
      <table class="logic-table"><tbody>
        <tr><th>✕ 天生就疯</th><td><strong>问题：</strong>出场便屠天灭地，读者只知道他危险，却不知道他失去了什么。<br><strong>改法：</strong>留下一条清楚的下坡路——先留魂，再借命，最后才敢拿苍生作筹码。</td></tr>
        <tr><th>✕ 执念等于控制</th><td><strong>问题：</strong>囚禁、掐腰、冷笑反复使用，动作只有占有，没有他独有的伤口。<br><strong>改法：</strong>让执念在矛盾动作里露馅；他控制她，也纵容她伤自己。</td></tr>
        <tr><th>✕ 爱能免罪</th><td><strong>问题：</strong>重逢就翻篇，受害者和三界的损失只剩几句旁白。<br><strong>改法：</strong>终局先处理代价，再决定他被救、被杀，还是独自偿还。</td></tr>
      </tbody></table>
      <div class="risk-box"><b>关系边界：</b>她可以仍然爱他，也可以拒绝原谅。男主受苦不能自动兑换她的同意。</div>
      <div class="argument"><p><strong>判断一段偏执有没有写成立，要看它是否改变了关系状态。</strong>一次越界至少留下一个可见后果：她更怕他、开始防他、夺回选择权，或逼他承认自己所谓的保护已经伤人。只有狠话，没有状态变化，场面再炸也只是原地表演。</p></div>
      <div class="evidence-row"><b>写前自查</b><p>这一场是谁做了选择？谁承担损失？谁因此改变了下一步行动？三个问题答不出来，就先别急着加更狠的台词。</p></div>
      <div class="evidence-row"><b>终局校验</b><p>结局不是“他够惨了吗”，而是伤害有没有被看见、责任有没有被承担，以及她是否仍握着拒绝的权利。</p></div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>误区修正</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">8/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">3个失控名场面</span><h2>先做出不可挽回的动作，再让他开口</h2><p>每场都放进目标、越界、代价与关系变化，狠话才不会悬在半空。</p></header>
      <div class="scene-stack">
        <article class="scene"><h3>01｜渡劫台：他替她接下不属于她的天雷</h3><p>她这一世本该飞升，雷落下时却先劈向他。众仙这才看见，他早把自己的仙骨炼成她的替劫符。她若成仙，他会魂飞魄散；她若回头救他，此生道途尽毁。</p><span class="beat">关系变化：守护者 → 命运绑缚者｜代价：她第一次知道，自己的自由一直用他的命抵着</span></article>
        <article class="scene"><h3>02｜藏魂殿：她看见了自己的九十九世</h3><p>每一盏灯里都是她的遗物。她抬手碰碎一盏，他竟当场吐血。原来他把神魂分进灯芯，陪她走完每个短命的人生。她问为什么不肯放过自己，他只说：因为你每一世都死在忘记我之后。</p><span class="beat">关系变化：陌生人 → 被迫共享百世记忆｜代价：真相越深，她越分不清爱与囚禁</span></article>
        <article class="scene"><h3>03｜众生局：她亲手划掉自己的名字</h3><p>生死簿上，只要她活，整座人间便替她偿命。她握笔划掉自己，他隔着结界第一次求她。她没有停。他便捏碎最后一枚仙印，让所有因果回到自己身上，笑着问：这次算我放你走了吗？</p><span class="beat">关系变化：占有 → 迟来的成全｜代价：他终于学会放手，也失去再次见她的资格</span></article>
      </div><div class="tip">名场面先写选择。角色一旦做出会改命的动作，情绪自然会追上来。</div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>名场面模板</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">9/9</span><div class="sheet">
      <div class="map-title"><h2>堕仙执念系<br>素材地图</h2><p>写前填完这 6 格，仙骨、执念和代价才能咬在一起。</p></div>
      <div class="map-grid">
        <article class="card"><h3>01 昔日仙格</h3><p>他从前最信哪条天规？又曾为众生守住什么？</p></article>
        <article class="card"><h3>02 唯一例外</h3><p>是谁或哪句旧约，让他第一次愿意徇私？</p></article>
        <article class="card"><h3>03 三层执念</h3><p>表层想救什么，深处怕什么，又藏着哪点私心？</p></article>
        <article class="card"><h3>04 四次越界</h3><p>每次伤及谁？借口如何变短？回头路如何被烧掉？</p></article>
        <article class="card"><h3>05 反噬刻度</h3><p>仙骨、神识、功德、关系，哪一种代价持续恶化？</p></article>
        <article class="card"><h3>06 终局回答</h3><p>他要继续占有、学会放手，还是用余生偿还？</p></article>
      </div>
      <div class="signoff"><img src="../../../assets/maodemi-cat-sticker-v1.png" alt=""><p>关注猫的咪，继续攒网文素材。<br>愿你的故事，有爱有恨，也有回声。</p></div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>今日存档 · 设定教程</span></footer></section>
  <section class="page alt-cover" data-cover="B">
    <div class="alt-title"><p class="alt-kicker">提升仙侠人物质感的方法</p><h1 class="alt-line one">堕仙</h1><h2 class="alt-line second">执念</h2><p class="alt-tail">怎么写</p></div>

    <img class="alt-attribution" src="../../../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由 AI Agent Popwave.cn 生成">
  </section><section class="page alt-cover" data-cover="C">
    <div class="alt-title"><p class="alt-kicker">提升仙侠人物质感的方法</p><h1 class="alt-line one">堕仙</h1><h2 class="alt-line second">执念</h2><p class="alt-tail">怎么写</p></div>
    <div class="alt-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div>
    <img class="alt-attribution" src="../../../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由 AI Agent Popwave.cn 生成">
  </section></main>
</body>
</html>
````
