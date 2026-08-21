# 隐忍暗卫系｜HTML 源码

原始文件：v2_隐忍暗卫系_全页Popwave_PDF版.html

````html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>隐忍暗卫系｜全页 Popwave PDF版 v2</title>
  <style>
    :root{--ink:#171411;--red:#9e3029;--paper:#fbf8f1;--muted:#736a62;--line:#d8cec4}
    *{box-sizing:border-box}
    html,body{margin:0;background:#aaa;font-family:"Songti SC","STSong","Noto Serif CJK SC",serif;color:var(--ink)}
    .deck{display:flex;flex-direction:column;align-items:center;gap:24px;padding:24px}
    .page{position:relative;width:1080px;height:1920px;overflow:hidden;background:#f4efe8 url("../assets/content-bg.png") center/cover no-repeat;break-after:page}
    .page:after{content:"";position:absolute;inset:30px;border:1px solid rgba(55,40,30,.18);pointer-events:none}
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
    .page-mark{position:absolute;left:50%;bottom:108px;transform:translateX(-50%);width:320px;padding:10px 15px;border-radius:12px;background:rgba(255,250,239,.88);z-index:3}
    .page-mark img{display:block;width:100%;height:auto}
    .page:last-child .page-mark{bottom:405px}
    .head{position:absolute;left:86px;right:80px;top:138px;display:grid;grid-template-columns:88px 1fr;gap:38px;align-items:start}
    .num{background:#171411;color:#fff;width:88px;height:88px;display:flex;align-items:center;justify-content:center;font:700 28px/1 Georgia,serif;letter-spacing:2px}
    .head h2{margin:-4px 0 13px;font-size:66px;line-height:1.12;letter-spacing:-2px}
    .sub{font-size:27px;line-height:1.45;color:var(--muted)}
    .body{position:absolute;left:86px;right:80px;top:410px;bottom:220px}
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
    <img class="avatar" src="../assets/avatar.png" alt="">
    <div class="pager">01 / 09</div>
    <div class="cover-card">
      <div class="eyebrow">如何写好一个设定之</div>
      <h1>隐忍<br>暗卫系<span>刀能杀人，心不能越界</span></h1>
      <div class="cover-rule"></div>
      <div class="cover-lead">别只写“忠诚、冷酷、能打”。<br>好看的暗卫，要让他的<em>每一次保护，都付得出代价</em>。</div>
      <div class="tags"><span class="tag">身份枷锁</span><span class="tag">克制美学</span><span class="tag">行为证据</span><span class="tag">高能名场面</span></div>
    </div>
    <div class="attribution"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">隐忍暗卫系</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">02 / 09</div>
    <header class="head"><div class="num">01</div><div><h2>先把四道枷锁<br>扣在他身上</h2><div class="sub">强，不会自动变成张力。能做什么，与不敢做什么同时出现，人物才会疼。</div></div></header>
    <div class="body">
      <div class="grid2">
        <div class="card"><h3>能力自由</h3>刀快、判断准、能在混战里掌控生死。<strong>他有改变局面的能力。</strong></div>
        <div class="card"><h3>身份不自由</h3>命令高于意愿，站位永远落后半步。<strong>他没有选择关系的资格。</strong></div>
        <div class="card"><h3>情感不自由</h3>心动会被解释成逾矩，偏爱只能伪装成尽职。<strong>越爱，越要像无情。</strong></div>
        <div class="card"><h3>姓名不自由</h3>功劳归于主人，过错落在自己；活成一串代号，死后也未必留名。</div>
      </div>
      <div class="note"><strong>小熊笔记：</strong>奴籍、死契、门规、旧恩，至少选一条写清楚。没有能执行的规矩，“不敢爱”就只剩作者按头。</div>
      <div class="direct"><b>可直接套一句</b>他能在三十步外取人性命，却不敢在她回头时，多看一眼。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">设定底盘</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">03 / 09</div>
    <header class="head"><div class="num">02</div><div><h2>别写“他很隐忍”<br>写他怎么站、怎么收手</h2><div class="sub">抽象情绪一落到身体，画面就出来了。</div></div></header>
    <div class="body">
      <div class="stack">
        <div class="row"><div class="label">远景</div><div class="copy">众人因他退开，他却在她身后停住；不是贴身，是永远隔着一臂。</div></div>
        <div class="row"><div class="label">近景</div><div class="copy">先替她试毒、清路、封窗，再把染血的手藏进袖中，不留邀功的机会。</div></div>
        <div class="row"><div class="label">特写</div><div class="copy">伤口绷开时，指节只紧了一瞬；回话仍稳，刀也没有碰响刀鞘。</div></div>
        <div class="row"><div class="label">反差</div><div class="copy">对敌一刀封喉，对她一句责问，只回“属下领罚”。</div></div>
      </div>
      <div class="direct"><b>长句示范</b>廊下风急，他先一步按住被吹起的帘角，等她安稳跨过门槛，才把肩上那支折断的箭往里推了半寸，免得血滴在她看得见的地方。</div>
      <div class="note">写克制常用四个动作：<strong>停、收、藏、退。</strong>每次少做半步，比反复写“眸色一暗”更有用。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">动作锚点</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">04 / 09</div>
    <header class="head"><div class="num">03</div><div><h2>忠诚要有证据<br>克制也要有后果</h2><div class="sub">别拿沉默替代人物逻辑。读者要看见他做了什么，又因此失去了什么。</div></div></header>
    <div class="body">
      <div class="contrast">
        <div class="bad"><h3>不好看</h3>她遇险，他突然出现替她挡刀；被误会也不解释，因为“暗卫都沉默”。<br><br>问题：只有功能，没有选择。换一个保镖也能完成。</div>
        <div class="good"><h3>好看</h3>他违令调走两名同僚，先把她送出火场，再独自回去补上缺口。事后不辩，是因为供出调令来源会牵连她。<br><br>选择、代价、沉默理由都在。</div>
      </div>
      <div class="note"><strong>判断标准：</strong>删掉“他爱她”这句话，读者还能不能从站位、取舍和后果里看出来？</div>
      <div class="direct"><b>可直接套一句</b>他跪下领罚时没有抬头。那封能证明清白的密信正贴在心口，他只要交出去，就能活；可信上有她的私印。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">正反对照</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">05 / 09</div>
    <header class="head"><div class="num">04</div><div><h2>四级递进<br>从守规矩写到越界</h2><div class="sub">越界别来得太早。先让他守得住，后面那半步才值钱。</div></div></header>
    <div class="body">
      <div class="stairs">
        <div class="stair"><div class="lv">Level 1<br>尽职</div><div class="txt">按命令保护，动作精准，不多问一句。温柔全藏在顺手做完的小事里。</div></div>
        <div class="stair"><div class="lv">Level 2<br>自困</div><div class="txt">开始回避目光、减少近身，却在危险来时比任何人都快。<strong>身体先于规矩。</strong></div></div>
        <div class="stair"><div class="lv">Level 3<br>偏私</div><div class="txt">表面照章办事，暗中改掉一处名单、放走一个证人、替她藏下一项罪证。</div></div>
        <div class="stair"><div class="lv">Level 4<br>越界</div><div class="txt">第一次拒绝她的命令：不是为了占有，是为了不让她去死。关系从主从变成了对抗。</div></div>
      </div>
      <div class="direct"><b>长句示范</b>他从前接令从不问缘由，那一夜却把令牌轻轻推回案上，膝仍跪着，声音也仍低，只那句“此令，属下不能领”终于把十年规矩割开一道口子。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">情绪递进</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">06 / 09</div>
    <header class="head"><div class="num">05</div><div><h2>每次偏爱<br>都给他开一张账单</h2><div class="sub">只挡刀会重复。把代价换着写，人物才不会永远停在同一场戏里。</div></div></header>
    <div class="body">
      <div class="costs">
        <div class="cost"><b>身体</b>旧伤复发、惯用手受损、失去继续护卫的能力。</div>
        <div class="cost"><b>身份</b>被除名、降级、从近卫调往死士营。</div>
        <div class="cost"><b>信任</b>主人误以为他背叛；同僚认定他坏了规矩。</div>
        <div class="cost"><b>名声</b>替她担下罪名，史书只留下“叛奴”二字。</div>
        <div class="cost"><b>自由</b>本可赎身，却为继续守在暗处主动续下死契。</div>
        <div class="cost"><b>关系</b>救她的方式伤了她；人活下来，两人却再回不到从前。</div>
      </div>
      <div class="direct"><b>长句示范</b>他终于替她洗净嫌疑，也终于把自己钉成了叛徒；城门合拢时，她在万人簇拥中回宫，他独自走向刑台，连回头都像一次僭越。</div>
      <div class="note">甜结局也能保留克制：让双向感情出现，但身份、信任与选择的代价不能凭一句告白自动清零。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">代价链</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">07 / 09</div>
    <header class="head"><div class="num">06</div><div><h2>一场暗卫名场面<br>照这 9 拍来写</h2><div class="sub">示例骨架：她被指通敌，他奉命亲自押她入狱。</div></div></header>
    <div class="body">
      <div class="beats">
        <div class="beat"><b>01 公令</b>众目睽睽之下，主人命他拿人。</div>
        <div class="beat"><b>02 私情</b>他知道证据有假，也知道她怕黑。</div>
        <div class="beat"><b>03 守规</b>照样上锁、押送，不替她求情。</div>
        <div class="beat"><b>04 微偏</b>锁链扣松一格，火把留在牢门外。</div>
        <div class="beat"><b>05 误解</b>她问：“连你也不信我？”</div>
        <div class="beat"><b>06 失语</b>他不能说查案已惊动真正的内鬼。</div>
        <div class="beat"><b>07 暗行</b>夜里离城取证，伤重仍赶在天亮前回来。</div>
        <div class="beat"><b>08 代价</b>证据送到，他因擅离职守被废去职位。</div>
        <div class="beat"><b>09 余波</b>她获释时，他已不再有资格站回身后。</div>
      </div>
      <div class="note"><strong>这场戏真正的钩子：</strong>表面上他最冷，实际每个冷动作里都藏着一处保护；等读者回看，才发现他早把退路铺完了。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">名场面骨架</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">08 / 09</div>
    <header class="head"><div class="num">07</div><div><h2>完整示范段<br>把克制写进动作里</h2><div class="sub">场景：她被押入诏狱，他负责落锁。</div></div></header>
    <div class="body">
      <article class="prose">
        <p>铁门在身后合拢时，她终于回头：“你也信那封信？”</p>
        <p>他没有答，只垂眼检查腕上的锁。铜齿咬合的声音很轻，他的手也很稳，仿佛昨夜翻过三道宫墙、从死人袖中取回半枚私印的人不是他。</p>
        <p>锁扣落下前，他指腹停了一瞬，悄悄留出一线余量。她若挣扎，不至磨破旧伤。</p>
        <p>“属下奉命看守。”他说。</p>
        <p>她笑了一声，把手抽回去。那点松动立刻藏进宽袖，像从未存在。</p>
        <p>他退出牢门，把唯一一盏灯留在廊下。天亮前，他还要去城西找活着的证人；若回不来，案卷最末那页已经压在主人书房的砚台下。只是这些，他一句也不能说。</p>
        <p>因为她若知道，便一定会拦。可他能领她的命，却不能眼看她去死。</p>
      </article>
      <div class="note">这里没写“深情”“心疼”“隐忍”。锁扣、灯、案卷和那句拒绝死亡，已经把感情说完了。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">正文示范</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">09 / 09</div>
    <header class="head"><div class="num">08</div><div><h2>收束小节<br>隐忍暗卫系这样写</h2><div class="sub">换掉身份、规矩和代价，就能改成你自己的角色。</div></div></header>
    <div class="body" style="bottom:390px">
      <div class="formula">强能力 × 低身份 × 禁忌心动 × 行为偏爱 × 真实代价</div>
      <div class="slots">
        <div class="slot">① 他最擅长什么，能解决怎样的危险？</div>
        <div class="slot">② 哪条契约、门规或旧恩限制着他？</div>
        <div class="slot">③ 他平时固定站在哪里，又会为谁破例？</div>
        <div class="slot">④ 哪个“停、收、藏、退”的动作能证明心动？</div>
        <div class="slot">⑤ 第一次越界，他会违抗哪一道命令？</div>
        <div class="slot">⑥ 这次偏爱让他失去身体、身份、信任，还是关系？</div>
      </div>
      <div class="direct"><b>最后自检</b>删掉“他爱她”，这份爱还能从选择与后果里被看见，暗卫就立住了。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <div class="follow"><img src="../assets/follow-bear-v1.png" alt=""><div><strong>我是小熊。</strong><br>关注我，为你整理直接能拿去写的素材。<br>今天也多码一点。</div></div>
    <div class="brand">小熊起床码字了</div><div class="topic">隐忍暗卫系</div>
  </section>
</main>
</body>
</html>
````
