# 如何写好禅意和尚x妖艳妖妃｜HTML 源码

原始文件：v36_如何写好禅意和尚x妖艳妖妃_新版交付包.html

````html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>如何写好禅意和尚 × 妖艳妖妃｜猫的咪 v36｜新版交付包</title>
  <style>
    :root{--ink:#302729;--sub:#6f6261;--rose:#d77786;--deep:#ad4a60;--line:rgba(201,116,126,.25);--paper:rgba(255,251,247,.91);--serif:"Songti SC","STSong",serif;--sans:"PingFang SC","Microsoft YaHei",sans-serif}
    *{box-sizing:border-box}body{margin:0;background:#eadbd4;color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}.toolbar{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:14px 24px;background:rgba(64,48,50,.94);color:#fff}.toolbar button{border:1px solid #ffffff80;border-radius:99px;padding:8px 18px;background:transparent;color:#fff}.toolbar span{opacity:.72;margin-left:8px}
    main{display:grid;justify-content:center;gap:40px;padding:48px 24px 80px}.page{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff8f3 center/cover no-repeat;box-shadow:0 22px 58px #5c423e2e}.cover{background-image:url("../../../assets/maodemi-cover-bg.png")}.content{background-image:url("../../../assets/maodemi-content-bg.png")}
    .brand{position:absolute;left:72px;top:62px;display:flex;align-items:center;gap:18px;color:var(--sub);font-size:26px;font-weight:800}.brand img{width:74px;height:74px;border-radius:50%;object-fit:contain;border:4px solid #ffffffe0;box-shadow:0 8px 20px #9c6f6b2e}.page-no{position:absolute;top:68px;right:72px;min-width:76px;height:48px;display:grid;place-items:center;border:2px solid #d879865c;border-radius:99px;color:var(--deep);background:#ffffff94;font:700 24px/1 Georgia}
    .sheet{position:absolute;inset:132px 64px 100px;display:flex;flex-direction:column;padding:28px 6px 18px}.topic{flex:none;margin:4px 0 22px;padding-bottom:18px;border-bottom:3px solid var(--line)}.topic-label{display:inline-flex;align-items:center;height:44px;padding:0 20px;border-radius:99px;color:var(--deep);background:#ffffffa8;font-size:22px;font-weight:900}.topic h2{margin:17px 0 0;font:900 62px/1.15 var(--serif)}.topic p{margin:12px 0 0;color:var(--sub);font:800 29px/1.42 var(--serif)}
    .cover-copy{position:absolute;left:74px;right:74px;top:420px;text-align:center}.kicker{margin:0 0 26px;color:var(--deep);font-size:38px;font-weight:900}.cover h1{margin:0;font:900 126px/1.08 var(--serif)}.cover h1 em{display:block;color:var(--deep);font-style:normal;font-size:168px}.cover-sub{max-width:900px;margin:38px auto 0;color:#5a5050;font:800 38px/1.5 var(--serif)}.cover-hook{max-width:860px;margin:48px auto 0;padding:22px 28px;border-top:4px solid #d87986a8;border-bottom:4px solid #d87986a8;font:800 29px/1.58 var(--serif)}
    .footer{position:absolute;left:76px;right:76px;bottom:34px;display:flex;align-items:center;justify-content:space-between;color:#8a7b7b;font-size:20px;font-weight:800}.mini-brand{display:flex;align-items:center;gap:10px}.mini-brand img{width:40px;height:40px;border-radius:50%}.popwave{width:324px;height:auto;display:block;flex:none}
    .formula{margin:4px 0 22px;padding:30px 34px;border:3px solid #cf7c884d;border-radius:30px;background:#fffaf4e8;text-align:center;box-shadow:0 14px 30px #80524f15}.formula b{display:block;color:var(--deep);font:900 30px/1.2 var(--sans)}.formula strong{display:block;margin-top:14px;font:900 45px/1.35 var(--serif)}.formula p{margin:14px 0 0;color:var(--sub);font:800 27px/1.5 var(--serif)}
    .grid{display:grid;gap:18px;flex:1;min-height:0}.grid.two{grid-template-columns:1fr 1fr}.grid.three{grid-template-columns:1fr}.card{padding:25px 28px;border:2px solid var(--line);border-radius:25px;background:var(--paper);box-shadow:0 12px 30px #80524f1c}.card .eyebrow{display:block;margin-bottom:9px;color:var(--deep);font-size:24px;font-weight:900}.card h3{margin:0 0 11px;font:900 36px/1.25 var(--serif)}.card p{margin:0;font:700 27px/1.5 var(--serif)}.card ul{margin:10px 0 0;padding-left:1.15em}.card li{margin:8px 0;font:700 26px/1.45 var(--serif)}.card strong{color:var(--deep)}
    .compare{display:grid;grid-template-columns:1fr 1fr;gap:18px}.compare .bad{border-color:#8b858034}.compare .good{border-color:#cc77854f;background:#fffaf5}.flag{display:inline-block;margin-bottom:12px;padding:7px 14px;border-radius:99px;background:#f4e1df;color:#8c6060;font-size:21px;font-weight:900}.good .flag{background:#efd4d8;color:var(--deep)}
    .steps{display:grid;gap:15px;flex:1;grid-auto-rows:1fr}.step{display:grid;grid-template-columns:70px 1fr;gap:17px;align-items:center;padding:18px 24px;border:2px solid var(--line);border-radius:24px;background:var(--paper)}.step .num{display:grid;place-items:center;width:58px;height:58px;border-radius:50%;background:#f2d6da;color:var(--deep);font:900 25px/1 Georgia}.step h3{margin:0 0 5px;font:900 30px/1.3 var(--serif)}.step p{margin:0;font:700 25px/1.42 var(--serif)}
    .scene-stack{display:grid;gap:18px;flex:1;grid-auto-rows:1fr}.scene{padding:25px 29px;border:2px solid var(--line);border-radius:26px;background:var(--paper)}.scene h3{margin:0 0 11px;color:var(--deep);font:900 34px/1.3 var(--serif)}.scene p{margin:0;font:700 26px/1.5 var(--serif)}.scene .beat{display:block;margin-top:10px;padding-top:10px;border-top:2px dashed var(--line);color:#675657;font-size:24px;font-weight:800}
    .map-title{margin:36px 0 22px;padding:22px;border-radius:30px;background:#ffffffa5;border:2px solid var(--line);text-align:center}.map-title h2{margin:0;font:900 65px/1.15 var(--serif)}.map-title p{margin:10px 0 0;color:var(--sub);font:800 26px/1.4 var(--serif)}.map-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.map-grid .card{min-height:182px}.map-grid .card h3{font-size:30px}.map-grid .card p{font-size:25px}.signoff{display:grid;grid-template-columns:190px 1fr;align-items:center;gap:22px;margin:22px auto 0;padding:14px 26px;border-radius:28px;background:#ffffffad;border:2px solid var(--line)}.signoff img{width:180px;height:200px;object-fit:cover}.signoff p{margin:0;color:#7a4c55;font:900 28px/1.5 var(--serif)}
    .tip{margin-top:16px;padding:17px 22px;border-left:6px solid var(--rose);border-radius:0 18px 18px 0;background:#fff9f4d9;color:#675657;font:800 25px/1.45 var(--serif)}.finale .map-grid{gap:18px}.finale .map-grid .card{min-height:220px;padding:30px}.finale .signoff{margin-top:28px;padding:24px 32px}.finale .signoff img{width:210px;height:230px}.finale .signoff p{font-size:30px}
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
  <header class="toolbar"><div><strong>猫的咪图文预览</strong><span>9页 · 1080×1920 · 设定教程</span></div><button onclick="window.print()">打印 / 导出 PDF</button></header>
  <main>
    <section class="page cover">
      <div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">1/9</span>
      <div class="cover-copy"><p class="kicker">如何写好一组禁忌 CP</p><h1>禅意和尚<em>× 妖艳妖妃</em></h1><p class="cover-sub">戒律｜欲望｜权谋｜双向救赎<br>1套完整写法 + 3个破戒名场面</p><div class="cover-hook">她教他看见一人，他教她看见众生<br>爱不是把谁拉下神坛，是逼彼此做一次清醒的选择</div></div>
      <footer class="footer"><span>猫的咪｜网文素材积累</span><img class="popwave" src="../../../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由 AI Agent Popwave.cn 生成"></footer>
    </section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">2/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">先钉住核心</span><h2>别只写“他禁欲，她勾引”</h2><p>这组 CP 好看，是两套活法正面相撞：他要守住众生，她要从吃人的深宫里活下来。</p></header>
      <div class="formula"><b>关系公式</b><strong>慈悲戒心 × 求生欲望 × 政局共谋 × 有价破例</strong><p>她试他的戒，他照见她的伤；谁都不能只负责被另一个人改变。</p></div>
      <div class="grid two">
        <article class="card"><span class="eyebrow">他要守的</span><h3>不是清白，是愿</h3><p>护寺中流民、止住兵祸、查清皇室借佛敛权。他的戒必须连着责任，才有重量。</p></article>
        <article class="card"><span class="eyebrow">她要抢的</span><h3>不是宠爱，是生路</h3><p>扳倒外戚、保住族人、夺回被皇帝拿走的名字。她的艳，是盔甲，也是武器。</p></article>
        <article class="card"><span class="eyebrow">两人必须做的</span><h3>一桩不干净的同盟</h3><p>他有密道与民心，她有宫门与证据。救人要合作，合作就要互相交出软肋。</p></article>
        <article class="card"><span class="eyebrow">每次靠近都要有</span><h3>可见的代价</h3><p>名声、戒籍、权位、证人或一座城的安危。破例之后，关系不能原地归零。</p></article>
      </div><div class="tip">一句话记住：禁忌感不在“不能爱”，在“爱了以后，谁来承担后果”。</div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>核心公式</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">3/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">先把两个人写活</span><h2>他有尘心，她有真心</h2><p>反差别停在衣着和表情。给他们各自的判断、手段，以及不会为恋爱让掉的东西。</p></header>
      <div class="grid three">
        <article class="card"><span class="eyebrow">和尚｜冷静不是没情绪</span><h3>他看得懂欲，也承担得住</h3><p>他曾是罪臣之子，入寺后救过疫民，也见过权贵借清名杀人。他不怕她美，只怕自己把私心误认成慈悲。</p></article>
        <article class="card"><span class="eyebrow">妖妃｜妖艳不是没脑子</span><h3>她知道凝视怎样变成权力</h3><p>她能记住朝臣的酒量、宫人的亲眷和皇帝每次翻脸前的小动作。她拿美貌做局，却不愿再被谁当成一件东西。</p></article>
        <article class="card"><span class="eyebrow">共同底子｜他们都被误读</span><h3>一个被供上神坛，一个被钉在祸水柱上</h3><p>他厌恶别人替他决定圣洁，她厌恶别人替她决定污秽。两人第一次同频，来自“我知道你不只是传闻”。</p></article>
      </div>
      <div class="formula"><b>人物底盘</b><strong>他的慈悲有锋芒，她的风情有边界；都能爱，也都能说不</strong></div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>三重身份</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">4/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">张力要一寸寸长</span><h2>四次靠近，四次改写边界</h2><p>别一见面就让他失态。先让例外发生在判断、权限和选择上。</p></header>
      <div class="steps">
        <article class="step"><span class="num">01</span><div><h3>试心：她故意靠近，他只问她手腕疼不疼</h3><p>他不接挑逗，先看见镯子下的勒痕。她第一次发现，美色在他面前不必表演到底。</p></div></article>
        <article class="step"><span class="num">02</span><div><h3>共谋：他把寺中暗门交给她</h3><p>她借暗门送走宫女，他因此被同门怀疑。信任从一句判断，变成能追责的权限。</p></div></article>
        <article class="step"><span class="num">03</span><div><h3>失衡：她替他饮下皇帝赐的酒</h3><p>他扶她回廊，手始终隔着一层袈裟；越克制，越显得那一步碰不得。</p></div></article>
        <article class="step"><span class="num">04</span><div><h3>破戒：他当众认下藏匿妖妃的罪</h3><p>失去清名并非爱情奖章。他要先救人、止乱，再决定自己还配不配穿这身僧衣。</p></div></article>
      </div><div class="tip">升级看三件事：距离更近、代价更重、下一次再也装不回陌生人。</div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>四级任务链</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">5/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">把“欲”写进细节</span><h2>别急着亲，先让身体出卖克制</h2><p>挑三种反复写。欲望越具体，角色嘴上的否认才越有用。</p></header>
      <div class="grid three">
        <article class="card"><span class="eyebrow">视线｜他从不盯她的唇</span><h3>却记得她每次说谎前会抿一下</h3><p>她换了三种唇脂，他都没评价；她唇角破了一道口子，他诵经时错了一字。</p></article>
        <article class="card"><span class="eyebrow">触碰｜每次都有正当理由</span><h3>把脉、挡箭、渡河、换药</h3><p>他碰完便收手，她却第一次没有顺势逗他。停顿半息，比多写十句“呼吸灼热”更有分量。</p></article>
        <article class="card"><span class="eyebrow">称呼｜身份决定距离</span><h3>娘娘、施主、真名、你</h3><p>公开时他叫她娘娘，独处仍守着施主。直到她要赴死，他第一次喊出她被夺走的本名。</p></article>
      </div>
      <div class="formula"><b>暧昧证据</b><strong>想碰而不碰，想问却先忍住，想留下却把路让开</strong><p>克制不是木头。每一次收手，都要让读者看见他差点做了什么。</p></div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>情感反噬</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">6/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">她也要主动选择</span><h2>别把妖妃写成等他渡的祸水</h2><p>她可以爱得热烈，仍要保留判断、拒绝和离开的能力。</p></header>
      <div class="steps">
        <article class="step"><span class="num">01</span><div><h3>她先停止试探</h3><p>发现他真会为她受罚后，她不再拿身体逼答复，改用证据和条件谈同盟。</p></div></article>
        <article class="step"><span class="num">02</span><div><h3>她保留拒绝权</h3><p>他愿带她出宫，她却先留下救被牵连的宫人。爱不是更换一个新的庇护者。</p></div></article>
        <article class="step"><span class="num">03</span><div><h3>她替欲望命名</h3><p>“我想要你”与“我要你救我”分开说。两种需要可以同时存在，不能混成一笔债。</p></div></article>
        <article class="step"><span class="num">04</span><div><h3>她也为他守一次边界</h3><p>他动摇时，她把佛珠放回他掌心：“想清楚再来。别拿后悔偿我。”</p></div></article>
        <article class="step"><span class="num">05</span><div><h3>她有自己的终局</h3><p>无论他还俗、留寺或战死，她都要完成揭案、安置旧部、拿回姓名这条人物线。</p></div></article>
      </div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>暴露递进</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">7/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">3组正误对照</span><h2>反差很香，也最容易写扁</h2><p>把标签换成选择。读者要看的，是他们怎样一步步走到越界。</p></header>
      <div class="steps">
        <div class="compare"><article class="card bad"><span class="flag">✕ 假禁欲</span><h3>嘴上念经，见她就失控</h3><p>戒律只用来延迟亲密，没有信念、职责和失去它的后果。</p></article><article class="card good"><span class="flag">✓ 真克制</span><h3>他动心，仍能把选择权还给她</h3><p>每次破例都经过判断，也愿意承担名声与身份的代价。</p></article></div>
        <div class="compare"><article class="card bad"><span class="flag">✕ 假妖艳</span><h3>除了撩人，什么都不会</h3><p>她没有目标和手段，剧情只靠男人为她发疯。</p></article><article class="card good"><span class="flag">✓ 真锋利</span><h3>她会做局，也知道何时停手</h3><p>风情服务于处境，能力推动政局，欲望由她自己承认。</p></article></div>
        <div class="compare"><article class="card bad"><span class="flag">✕ 强行渡化</span><h3>他一句佛理，她立刻改邪归正</h3><p>她的创伤、恶行和求生手段都被爱情轻轻抹掉。</p></article><article class="card good"><span class="flag">✓ 双向照见</span><h3>他学会承认私心，她学会不拿伤人护身</h3><p>两个人都改变，也都要为旧选择付账。</p></article></div>
      </div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>误区修正</span></footer></section>

    <section class="page content"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">8/9</span><div class="sheet">
      <header class="topic"><span class="topic-label">3个破戒名场面</span><h2>先让动作发生，再让情绪追上</h2><p>每场都放进目标、选择、代价与关系变化，别只摆一张漂亮画面。</p></header>
      <div class="scene-stack">
        <article class="scene"><h3>01｜雨夜问心：她把佛珠绕上他的腕</h3><p>追兵就在门外，她笑问：“大师救众生，也救我么？”他解下佛珠，没有推开她，只把密道钥匙放进她掌心：“今夜救你。天亮后，你把名册给我。”她第一次没有继续靠近。</p><span class="beat">关系变化：猎人与猎物 → 有条件的同盟｜代价：他交出寺中秘密，她交出宫中证据</span></article>
        <article class="scene"><h3>02｜佛前验伤：他撕下半幅袈裟</h3><p>她肩上中箭，仍拿笑遮痛。他背过身让她自己褪衣，只递来布与药。箭头刻着寺中印记，他沉默片刻，撕下袈裟替她止血：“这件事，我会给你交代。”</p><span class="beat">关系变化：试探 → 共担一桩丑闻｜代价：他的信仰共同体，也可能是伤她的人</span></article>
        <article class="scene"><h3>03｜宫门破戒：他当众喊出她的真名</h3><p>皇帝命人烧死“祸国妖妃”，百官等他诵经送行。他却踏进火场，叫出她入宫前的名字，把罪证塞进她手里：“你去敲登闻鼓。这里的人，我来拦。”</p><span class="beat">关系变化：暗中相护 → 公开站队｜代价：他失去清名，她必须活着面对审判</span></article>
      </div><div class="tip">所谓破戒，不一定先落在吻上。一次公开站队，往往比亲密更重。</div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>名场面模板</span></footer></section>

    <section class="page content finale"><div class="brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div><span class="page-no">9/9</span><div class="sheet">
      <div class="map-title"><h2>和尚 × 妖妃<br>素材地图</h2><p>写前填完这 6 格，禁忌感就不会只剩袈裟与红裙。</p></div>
      <div class="map-grid">
        <article class="card"><h3>01 他的愿</h3><p>他为何出家？守戒保护着谁？失去身份会牵连什么？</p></article>
        <article class="card"><h3>02 她的局</h3><p>她靠什么活到今天？美貌之外，还有哪项硬本事？</p></article>
        <article class="card"><h3>03 共同任务</h3><p>谁借佛敛权？谁困住宫人？他们非合作不可的事是什么？</p></article>
        <article class="card"><h3>04 四次靠近</h3><p>试心、共谋、失衡、破戒，每次改掉哪条边界？</p></article>
        <article class="card"><h3>05 有价破例</h3><p>名声、戒籍、权位、证人和百姓，他们要失去哪一样？</p></article>
        <article class="card"><h3>06 清醒终局</h3><p>还俗、留寺、分离或同行，都要尊重两人的完整人物线。</p></article>
      </div>
      <div class="signoff"><img src="../../../assets/maodemi-cat-sticker-v1.png" alt=""><p>关注猫的咪，继续攒网文素材。<br>愿你的故事，有爱有恨，也有回声。</p></div>
    </div><footer class="footer"><span class="mini-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪｜网文素材积累</span><span>今日存档 · CP 写法</span></footer></section>
  <section class="page alt-cover" data-cover="B">
    <div class="alt-title"><p class="alt-kicker">提升禁忌CP张力的方法</p><h1 class="alt-line one">禅意</h1><h2 class="alt-line second">妖妃</h2><p class="alt-tail">×和尚</p></div>

    <img class="alt-attribution" src="../../../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由 AI Agent Popwave.cn 生成">
  </section><section class="page alt-cover" data-cover="C">
    <div class="alt-title"><p class="alt-kicker">提升禁忌CP张力的方法</p><h1 class="alt-line one">禅意</h1><h2 class="alt-line second">妖妃</h2><p class="alt-tail">×和尚</p></div>
    <div class="alt-brand"><img src="../../../assets/maodemi-avatar.png" alt="">猫的咪</div>
    <img class="alt-attribution" src="../../../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由 AI Agent Popwave.cn 生成">
  </section></main>
</body>
</html>
````
