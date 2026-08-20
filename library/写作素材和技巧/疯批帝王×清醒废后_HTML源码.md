# 疯批帝王×清醒废后｜HTML 源码

原始文件：v2_疯批帝王×清醒废后_每页Popwave_小熊直出版.html

````html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>疯批帝王×清醒废后｜每页 Popwave｜小熊直出版 v2</title>
  <style>
    :root{--ink:#171411;--red:#9e3029;--paper:#fbf8f1;--muted:#736a62;--line:#d8cec4}
    *{box-sizing:border-box}
    html,body{margin:0;background:#aaa;font-family:"Songti SC","STSong","Noto Serif CJK SC",serif;color:var(--ink)}
    .deck{display:flex;flex-direction:column;align-items:center;gap:24px;padding:24px}
    .page{position:relative;width:1080px;height:1920px;overflow:hidden;background:#f4efe8 url("../assets/content-bg.png") center/cover no-repeat;break-after:page}
    .page:after{content:"";position:absolute;inset:30px;border:1px solid rgba(55,40,30,.18);pointer-events:none}
    .page:not(.cover):before{content:"";position:absolute;left:50%;top:62px;transform:translateX(-50%);width:258px;height:48px;border-radius:10px;background:rgba(255,250,239,.82) url("../assets/branding/popwave-ai-agent-attribution-brand-blue.png") center/232px auto no-repeat;z-index:3}
    .cover{background:#776b63 url("../assets/cover-bg.png") center/cover no-repeat}
    .avatar{position:absolute;left:72px;top:58px;width:74px;height:74px;border-radius:50%;object-fit:cover;box-shadow:0 7px 18px rgba(0,0,0,.18);z-index:2}
    .pager{position:absolute;right:70px;top:72px;font:18px/1.2 Georgia,serif;letter-spacing:2px;color:#796f68;z-index:2}
    .brand{position:absolute;left:178px;bottom:66px;font-size:22px;letter-spacing:2px;color:#554c45}
    .topic{position:absolute;right:76px;bottom:66px;font-size:20px;color:#7a6d64}
    .cover-card{position:absolute;left:100px;right:100px;top:382px;min-height:1000px;padding:155px 78px 100px;background:rgba(255,253,248,.94);box-shadow:0 18px 40px rgba(48,35,26,.12)}
    .eyebrow{font-size:25px;letter-spacing:8px;color:#786d64;margin-bottom:30px}
    .cover h1{margin:0;font-size:146px;line-height:.95;letter-spacing:-5px;font-weight:900}
    .cover h1 span{display:block;color:var(--red);font-size:88px;letter-spacing:2px;margin-top:24px}
    .cover-rule{height:4px;background:linear-gradient(90deg,#b64b43,transparent);margin:54px 0 38px}
    .cover-lead{font-size:36px;line-height:1.55;font-weight:700}
    .cover-lead em{font-style:normal;color:var(--red)}
    .tags{display:flex;gap:14px;flex-wrap:wrap;margin-top:46px}
    .tag{border:1px solid #c99b94;padding:12px 22px;font-size:23px;color:#80372f;background:#fffaf5}
    .attribution{position:absolute;left:50%;bottom:150px;transform:translateX(-50%);width:320px;padding:10px 15px;border-radius:12px;background:rgba(255,250,239,.82);z-index:3}
    .attribution img{display:block;width:100%;height:auto}
    .head{position:absolute;left:86px;right:80px;top:138px;display:grid;grid-template-columns:88px 1fr;gap:38px;align-items:start}
    .num{background:#171411;color:#fff;width:88px;height:88px;display:flex;align-items:center;justify-content:center;font:700 28px/1 Georgia,serif;letter-spacing:2px}
    .head h2{margin:-4px 0 13px;font-size:66px;line-height:1.12;letter-spacing:-2px}
    .sub{font-size:27px;line-height:1.45;color:var(--muted)}
    .body{position:absolute;left:86px;right:80px;top:410px;bottom:132px}
    .grid2,.grid3{display:grid;gap:22px}
    .grid2{grid-template-columns:1fr 1fr}.grid3{grid-template-columns:repeat(3,1fr)}
    .card{background:rgba(255,253,248,.92);border:1px solid var(--line);padding:29px 30px;font-size:27px;line-height:1.62}
    .card h3{margin:0 0 13px;font-size:32px;line-height:1.25}
    .card strong,.red{color:var(--red)}
    .note{margin-top:22px;padding:24px 28px;background:rgba(255,253,248,.94);border-left:6px solid var(--red);font-size:27px;line-height:1.6}
    .direct{margin-top:22px;padding:29px 32px;background:#fffaf2;border:1px solid #d6c5b9;font-size:28px;line-height:1.7}
    .direct b{display:block;color:var(--red);margin-bottom:8px}
    .stack{display:flex;flex-direction:column;gap:18px}
    .row{display:grid;grid-template-columns:140px 1fr;background:rgba(255,253,248,.94);border-left:6px solid var(--red)}
    .row .label{padding:24px 18px;font-size:28px;font-weight:800;color:var(--red)}
    .row .copy{padding:24px 28px;font-size:26px;line-height:1.55;border-left:1px solid #e1d7ce}
    .contrast{display:grid;grid-template-columns:1fr 1fr;gap:24px}
    .bad,.good{padding:28px 30px;background:rgba(255,253,248,.94);font-size:27px;line-height:1.6;border-top:8px solid #777}
    .good{border-color:var(--red)}.bad h3,.good h3{margin:0 0 18px;font-size:34px}.good h3{color:var(--red)}
    .stairs{display:flex;flex-direction:column;gap:17px}
    .stair{display:grid;grid-template-columns:190px 1fr;background:rgba(255,253,248,.94);border:1px solid var(--line)}
    .stair .lv{padding:25px 22px;font-size:28px;font-weight:800;color:#fff;background:#29231f}
    .stair:nth-child(2) .lv{background:#5d443a}.stair:nth-child(3) .lv{background:#813b33}.stair:nth-child(4) .lv{background:#a32f29}
    .stair .txt{padding:23px 29px;font-size:26px;line-height:1.55}
    .costs{display:grid;grid-template-columns:1fr 1fr;gap:18px}
    .cost{background:rgba(255,253,248,.94);border-left:6px solid var(--red);padding:23px 26px;font-size:25px;line-height:1.5}
    .cost b{display:block;font-size:29px;margin-bottom:6px;color:var(--red)}
    .beats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
    .beat{min-height:178px;background:rgba(255,253,248,.94);padding:22px 21px;border-top:5px solid #241f1b;font-size:23px;line-height:1.45}
    .beat b{display:block;color:var(--red);font-size:26px;margin-bottom:8px}
    .prose{background:rgba(255,253,248,.94);padding:42px 48px;border:1px solid var(--line);font-size:29px;line-height:1.95;text-align:justify}
    .prose p{margin:0 0 24px}.prose p:last-child{margin-bottom:0}
    .formula{font-size:34px;line-height:1.55;font-weight:800;padding:28px 32px;background:#241f1b;color:#fff;margin-bottom:22px}
    .slots{display:flex;flex-direction:column;gap:13px}
    .slot{padding:19px 25px;background:rgba(255,253,248,.94);border-left:5px solid var(--red);font-size:25px;line-height:1.45}
    .follow{position:absolute;left:86px;right:80px;bottom:145px;height:220px;background:rgba(255,248,236,.94);border:1px solid #d4c3b5;display:flex;align-items:center;padding:18px 40px 18px 240px;font-size:25px;line-height:1.55}
    .follow img{position:absolute;left:28px;bottom:0;width:190px}
    @page{size:1080px 1920px;margin:0}
    @media print{html,body{background:#fff}.deck{display:block;padding:0}.page{margin:0;break-after:page}}
  </style>
</head>
<body>
<main class="deck">
  <section class="page cover">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">01 / 09</div>
    <div class="cover-card">
      <div class="eyebrow">如何写好一组高张力 CP</div>
      <h1 style="font-size:122px">疯批帝王<br><span style="font-size:76px">× 清醒废后</span></h1>
      <div class="cover-rule"></div>
      <div class="cover-lead">他有权毁掉她的一切，<br>却偏偏<em>留不住一颗厌他的心</em>。</div>
      <div class="tags"><span class="tag">权力倒置</span><span class="tag">智性拉扯</span><span class="tag">双向破碎</span><span class="tag">无解 BE</span></div>
    </div>
    <div class="attribution"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">疯帝×废后</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">02 / 09</div>
    <header class="head"><div class="num">01</div><div><h2>先立五重对冲<br>权力越悬殊，心越倒置</h2><div class="sub">这对 CP 不能只靠“他疯、她惨”。真正好看的是：身位与心位永远相反。</div></div></header>
    <div class="body">
      <div class="grid2">
        <div class="card"><h3>权力</h3>他主宰生死，她被废去尊荣；<strong>可她主宰他的情绪，他拿她的心毫无办法。</strong></div>
        <div class="card"><h3>状态</h3>他高居九重却内心荒芜；她跌到尘埃，反而通透安稳。</div>
        <div class="card"><h3>情爱</h3>他宁毁不放，她爱过便割舍；<strong>一个越陷越深，一个早已离席。</strong></div>
        <div class="card"><h3>姿态</h3>他对天下强硬、只对她失度；她对旁人温淡、只对他寸步不让。</div>
      </div>
      <div class="note"><strong>宿命落点：</strong>他拥有世间一切，唯独得不到她的真心；她失去世间所有，唯独守住自己的本心。</div>
      <div class="direct"><b>可直接套一句</b>最高的权势，困不住最淡的人心；最疯的执念，换不回最彻底的释然。</div>
    </div>
    <div class="brand">小熊起床码字了</div><div class="topic">五重对冲</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">03 / 09</div>
    <header class="head"><div class="num">02</div><div><h2>双人底盘别写反<br>他失度，她不失骨</h2><div class="sub">疯批不是无脑发疯，废后也不是懦弱受虐。两个人都要清醒，悲剧才成立。</div></div></header>
    <div class="body">
      <div class="stack">
        <div class="row"><div class="label">帝王·外</div><div class="copy">冷血、善制衡、杀伐果断。朝堂上必须理智得可怕，不给任何人看见破绽。</div></div>
        <div class="row"><div class="label">帝王·内</div><div class="copy">只对她偏执、惶恐、反复破例；一边伤害，一边补偿，明知强求仍不肯放手。</div></div>
        <div class="row"><div class="label">废后·外</div><div class="copy">褪去凤袍，不争宠、不结党、不诉苦。看似无所作为，其实主动退出他的棋局。</div></div>
        <div class="row"><div class="label">废后·内</div><div class="copy">不是不爱，是爱过、痛过、看透后彻底脱敏；身被宫墙困住，心已经自由。</div></div>
      </div>
      <div class="direct"><b>长句示范</b>他能在金殿上一句话定百人生死，却在她平静唤出“陛下”二字时，忽然明白这世上原来真有一道旨意，连天子也无权收回。</div>
      <div class="note"><strong>小熊笔记：</strong>他要“只对她失度”；她要“身困而心不困”。少一个，都会写俗。</div>
    </div>
    <div class="brand">小熊起床码字了</div><div class="topic">双人底盘</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">04 / 09</div>
    <header class="head"><div class="num">03</div><div><h2>四层镜头落地<br>别只写“爱恨纠缠”</h2><div class="sub">远景定尊卑，近景写错位，特写抓失控，最后用一句宿命判词收刀。</div></div></header>
    <div class="body">
      <div class="stack">
        <div class="row"><div class="label">远景</div><div class="copy">金殿上，他黄袍加身、百官俯首；冷宫里，她素衣荆钗、独坐窗下。云泥之别先压下来。</div></div>
        <div class="row"><div class="label">近景</div><div class="copy">他下旨封门、隔绝内外；她不哭不闹，照旧看书养花。顺从不是臣服，是不在意。</div></div>
        <div class="row"><div class="label">特写</div><div class="copy">他因她一句淡话捏碎杯盏，她只垂眼拂去衣袖上的茶沫，像看一场与己无关的雨。</div></div>
        <div class="row"><div class="label">判词</div><div class="copy">旁人都怕他的雷霆之怒，只有她知道，那不过是一个求而不得的人最后的体面。</div></div>
      </div>
      <div class="direct"><b>可直接套一句</b>他坐拥万里江山，唯独求她一眼回望；她身陷方寸囚笼，唯独心向山海自由。</div>
    </div>
    <div class="brand">小熊起床码字了</div><div class="topic">镜头锚点</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">05 / 09</div>
    <header class="head"><div class="num">04</div><div><h2>避开五个俗套<br>清醒 BE 才不塌</h2><div class="sub">最怕表面写“高级意难平”，骨子里还是追妻火葬场和无脑强制爱。</div></div></header>
    <div class="body">
      <div class="contrast">
        <div class="bad"><h3>不好看</h3><strong>他：</strong>对谁都疯，靠摔杯、杀人证明深情。<br><br><strong>她：</strong>反复心软，受尽折磨还等一句解释。<br><br><strong>结局：</strong>复位封后，旧伤被告白一笔勾销。</div>
        <div class="good"><h3>好看</h3><strong>他：</strong>对外理智制衡，只在她面前失去尺度。<br><br><strong>她：</strong>不争不是软弱，而是再也不参加。<br><br><strong>结局：</strong>他守住她的人，却永远失去她的爱。</div>
      </div>
      <div class="note"><strong>三条红线：</strong>禁女主二次沦陷；禁男主全员疯批；禁强行圆满和解。爱恨一旦重新对等，这组 CP 独有的错位就没了。</div>
      <div class="direct"><b>可直接套一句</b>“臣妾不是原谅了陛下。”她把旧凤印推回去，“只是往事太远，已经不值得恨了。”</div>
    </div>
    <div class="brand">小熊起床码字了</div><div class="topic">正反避雷</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">06 / 09</div>
    <header class="head"><div class="num">05</div><div><h2>四阶拉扯<br>从暗流写到终身无解</h2><div class="sub">不要开场就跪地求爱。帝王尊严一层层掉，废后的心却一层层静，才有递进。</div></div></header>
    <div class="body">
      <div class="stairs">
        <div class="stair"><div class="lv">Level 1<br>冷淡制衡</div><div class="txt">他人前冷漠、暗中偏袒；她以平常心接住他的阴晴不定。<strong>他暗流汹涌，她死水无澜。</strong></div></div>
        <div class="stair"><div class="lv">Level 2<br>偏执试探</div><div class="txt">他禁足、推拉、言语伤人后再补偿；她不接招、不解释，步步退出情爱棋局。</div></div>
        <div class="stair"><div class="lv">Level 3<br>疯魔卑微</div><div class="txt">他放权、低头、许她凤位荣宠；她不贪他的温柔，也不拿他的悔恨疗伤。</div></div>
        <div class="stair"><div class="lv">Level 4<br>宿命无解</div><div class="txt">他守她一生却得不到真心；她守住本心，却终身走不出宫墙。</div></div>
      </div>
      <div class="direct"><b>长句示范</b>他终于肯把江山里最尊贵的位置还给她，才发现她早已不需要那件凤袍；他能补回名分、荣宠与迟来的公道，唯独补不回那个曾经等他回头的人。</div>
    </div>
    <div class="brand">小熊起床码字了</div><div class="topic">四阶递进</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">07 / 09</div>
    <header class="head"><div class="num">06</div><div><h2>一场废后名场面<br>照这 9 拍来写</h2><div class="sub">示例骨架：深夜冷宫，他带着凤印来求她重回中宫。</div></div></header>
    <div class="body">
      <div class="beats">
        <div class="beat"><b>01 强者入场</b>宫门尽开，帝王带着凤印与仪仗而来。</div>
        <div class="beat"><b>02 弱者反常</b>她不跪不喜，只合上读了一半的书。</div>
        <div class="beat"><b>03 先给诱饵</b>他许凤位、权势，替她洗净旧罪。</div>
        <div class="beat"><b>04 她不接招</b>她问：“陛下想换回哪一年的我？”</div>
        <div class="beat"><b>05 帝王失态</b>他捏紧凤印，第一次承认自己错了。</div>
        <div class="beat"><b>06 旧伤见光</b>她说当年等过，后来便不等了。</div>
        <div class="beat"><b>07 放下尊严</b>他低声求她，哪怕只装作从前。</div>
        <div class="beat"><b>08 温柔拒绝</b>她替他扶正衣襟：“不必了，陛下。”</div>
        <div class="beat"><b>09 余波落刀</b>凤印留下，人却再也没回到他身边。</div>
      </div>
      <div class="note"><strong>这场戏的张力：</strong>他拿出全天下都想要的东西，她却只用一句“不必”证明——他的最高权力，对她已经失效。</div>
    </div>
    <div class="brand">小熊起床码字了</div><div class="topic">9拍名场面</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">08 / 09</div>
    <header class="head"><div class="num">07</div><div><h2>完整示范段<br>凤印可以归还，旧人不能</h2><div class="sub">一段里同时放进权力、旧情、低头与清醒拒绝。</div></div></header>
    <div class="body">
      <article class="prose" style="font-size:27px;line-height:1.82">
        <p>凤印落在案上时，发出很轻的一声响。她抬眼看了看，没有伸手。</p>
        <p>“你想要的，朕都可以还。”他仍穿着退朝时的玄色龙袍，语气却不像下旨，“凤位、母族的清白、从前受过的委屈——”</p>
        <p>“陛下。”她打断他，替将熄的灯拨亮了一点，“臣妾从前想要这些，是因为以为有了它们，便能与你长久。如今不想与你长久，自然也就不需要了。”</p>
        <p>他指骨抵着桌沿，许久才问：“那你要什么？”</p>
        <p>她望向窗外。“想要明日醒来，不必再猜陛下今天爱我几分，又疑我几分。”</p>
        <p>他能叫满朝噤声，能把旧案翻过来重审，能让废去多年的凤印重新生出分量；可那一夜，他第一次听见一个比圣旨更不容置疑的答案。</p>
        <p>“不必了，陛下。”</p>
      </article>
    </div>
    <div class="brand">小熊起床码字了</div><div class="topic">正文示范</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">09 / 09</div>
    <header class="head"><div class="num">08</div><div><h2>收束小节<br>清醒无解 CP 这样写</h2><div class="sub">换掉皇权、凤位和冷宫，也能迁移到仙侠、豪门、权谋或末世。</div></div></header>
    <div class="body" style="bottom:390px">
      <div class="formula">外在强弱悬殊 × 内在主导倒置 × 一人执念 × 一人释然 = 无解 BE</div>
      <div class="slots">
        <div class="slot"><strong>① 外在权力：</strong>谁能决定对方的身份、生死与去留？</div>
        <div class="slot"><strong>② 内在权力：</strong>谁真正主宰对方的情绪与选择？</div>
        <div class="slot"><strong>③ 失度证据：</strong>强者只为她破了哪一条原则？</div>
        <div class="slot"><strong>④ 清醒证据：</strong>弱者放弃了什么诱饵，证明自己已经离席？</div>
        <div class="slot"><strong>⑤ 递进代价：</strong>他依次失去权威、尊严，还是圆满？</div>
        <div class="slot"><strong>⑥ 终局判词：</strong>他最终困住了什么，又永远失去了什么？</div>
      </div>
    </div>
    <div class="follow"><img src="../assets/follow-bear-v1.png" alt=""><div><strong>我是小熊。</strong><br>关注我，为你整理直接能拿去写的素材。<br>今天也多码一点。</div></div>
    <div class="brand">小熊起床码字了</div><div class="topic">疯帝×废后</div>
  </section>
</main>
</body>
</html>
````
