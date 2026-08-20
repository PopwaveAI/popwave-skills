# 落难公主复仇系｜HTML 源码

原始文件：v3_落难公主复仇系_小熊直出版_原始品牌资产.html

````html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>落难公主复仇系｜小熊直出版 v3｜原始品牌资产</title>
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
    .page-mark{position:absolute;left:50%;bottom:108px;transform:translateX(-50%);width:320px;padding:10px 15px;border-radius:12px;background:rgba(255,250,239,.88);z-index:4}
    .page-mark img{display:block;width:100%;height:auto}
    .cover .page-mark{bottom:150px}
    .page:last-child .page-mark{bottom:382px}
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
    <img class="avatar" src="../assets/avatar.png" alt="">
    <div class="pager">01 / 09</div>
    <div class="cover-card">
      <div class="eyebrow">如何写好一个设定之</div>
      <h1>落难<br>公主系<span>她低头，不等于她认输</span></h1>
      <div class="cover-rule"></div>
      <div class="cover-lead">别只写“从娇贵变狠毒”。<br>好看的复仇公主，是<em>手段被炼黑了，风骨却没有烂</em>。</div>
      <div class="tags"><span class="tag">破碎强者</span><span class="tag">清醒复仇</span><span class="tag">行为锚点</span><span class="tag">名场面骨架</span></div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">落难公主复仇系</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">02 / 09</div>
    <header class="head"><div class="num">01</div><div><h2>先立五重对冲<br>她才不是换装黑化</h2><div class="sub">破碎感来自落差，强者感来自选择；两样要同时存在。</div></div></header>
    <div class="body">
      <div class="grid2">
        <div class="card"><h3>昔日荣光</h3>她见过真正的体面，也受过朝堂教养。<strong>这决定她为何仍有分寸。</strong></div>
        <div class="card"><h3>今朝泥泞</h3>身份、亲人、故国尽失，必须在最卑劣的人情里活下来。</div>
        <div class="card"><h3>清醒隐忍</h3>她不靠侥幸，不沉溺悲痛；低头是为了看清谁的鞋上沾着血。</div>
        <div class="card"><h3>狠绝有界</h3>对仇人精准清算，对无辜绝不牵连。<strong>她变狠，却没有变脏。</strong></div>
      </div>
      <div class="note"><strong>第五层是宿命：</strong>她能夺回山河，却夺不回旧日。胜利越完整，“得胜无归”越疼。</div>
      <div class="direct"><b>可直接套一句</b>她学会了把人心放上秤，却始终不肯把无辜者也算进代价里。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">人设底盘</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">03 / 09</div>
    <header class="head"><div class="num">02</div><div><h2>别写“她很破碎”<br>写荣光怎样留在身体里</h2><div class="sub">她可以换素衣、做粗活，但旧身份会从下意识里漏出来。</div></div></header>
    <div class="body">
      <div class="stack">
        <div class="row"><div class="label">远景</div><div class="copy">素衣荆钗站在人群末尾，脊背微弯，却从未真正塌下去。</div></div>
        <div class="row"><div class="label">近景</div><div class="copy">被推来脏活，她先应下，再看清门锁、换岗时辰和每个人的站位。</div></div>
        <div class="row"><div class="label">特写</div><div class="copy">听见故国旧名，指腹只在杯沿停了一瞬；抬眼时，情绪已经收净。</div></div>
        <div class="row"><div class="label">反差</div><div class="copy">她替欺辱过自己的婢女挡下一鞭，却在夜里把仇人的账簿送进御史府。</div></div>
      </div>
      <div class="direct"><b>长句示范</b>满座拿她亡国取乐，她仍垂眼添酒，腕骨稳得没有溅出一滴；直到那人说起先帝死状，她才把酒壶往左挪了半寸——那里，正好能照见屏风后偷听的影子。</div>
      <div class="note">写破碎感常用四个动作：<strong>认出、停顿、收回、继续。</strong>旧物只刺她一下，她仍把眼前的局走完。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">视觉锚点</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">04 / 09</div>
    <header class="head"><div class="num">03</div><div><h2>复仇不是发疯<br>而是一次次精准取舍</h2><div class="sub">读者要看的不是狠话，而是她愿意舍掉什么、又坚持不舍什么。</div></div></header>
    <div class="body">
      <div class="contrast">
        <div class="bad"><h3>不好看</h3>被羞辱就当场打脸，遇仇人就失控拔刀；靠男主救出牢狱，再突然拿到兵权。<br><br>问题：复仇只剩情绪，翻盘全靠作者发礼包。</div>
        <div class="good"><h3>好看</h3>她忍下宴上折辱，让对方误判她无害；借献酒换来接近书房的机会，只拿走能撬动整条利益链的一页账。<br><br>示弱、目标、行动与后果都在。</div>
      </div>
      <div class="note"><strong>判断标准：</strong>删掉“她很聪明、她要复仇”，读者还能不能从信息差、筹码和取舍里看懂她的计划？</div>
      <div class="direct"><b>可直接套一句</b>她不是不能杀他，只是此刻一具尸体只能解恨，一张活人的嘴却能把三年前关上的宫门重新撬开。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">正反对照</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">05 / 09</div>
    <header class="head"><div class="num">04</div><div><h2>四阶递进<br>从活下来写到得胜无归</h2><div class="sub">别开场就满级权谋。她每升一级，都该失去一点原本的自己。</div></div></header>
    <div class="body">
      <div class="stairs">
        <div class="stair"><div class="lv">Level 1<br>蛰伏</div><div class="txt">先活下来：藏身份、忍小辱、记人情，把每一处地形与规矩变成未来筹码。</div></div>
        <div class="stair"><div class="lv">Level 2<br>博弈</div><div class="txt">开始借力：放出半真消息，引两方互疑，自己只拿走最关键的证据。</div></div>
        <div class="stair"><div class="lv">Level 3<br>清算</div><div class="txt">不再只求自保。她主动设局，让仇人失去羽翼、名声与退路，<strong>却仍不伤无辜。</strong></div></div>
        <div class="stair"><div class="lv">Level 4<br>归位</div><div class="txt">她夺回权柄，也承认故国无法复原。胜利不是回到从前，而是带着伤继续掌舵。</div></div>
      </div>
      <div class="direct"><b>长句示范</b>她从前连宫灯灭了一盏都有人来换，如今却能在漏雨的柴房里等到天明，把三拨守卫的脚步一一记熟，再用冻裂的手指把地图画进灰里。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">成长递进</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">06 / 09</div>
    <header class="head"><div class="num">05</div><div><h2>每次翻盘<br>都给她开一张账单</h2><div class="sub">只写爽点会轻。复仇越向前，代价越应该碰到她珍惜的东西。</div></div></header>
    <div class="body">
      <div class="costs">
        <div class="cost"><b>身体</b>旧伤、毒、失眠或不可逆的残疾，提醒她不是无损升级。</div>
        <div class="cost"><b>身份</b>为进入敌营主动抹去姓名；日后归位，也有人只记得她曾卑微。</div>
        <div class="cost"><b>信任</b>计划不能说全，旧臣把她当叛徒，盟友也开始防她。</div>
        <div class="cost"><b>底线</b>必须利用一个真心待她的人；事成之后，她仍要承担这笔情债。</div>
        <div class="cost"><b>归处</b>故宫可重开，旧人却不归；熟悉的地方已经不再是家。</div>
        <div class="cost"><b>关系</b>爱她的人想救她离开，她却选择留下完成清算，两人从此站在不同的岸。</div>
      </div>
      <div class="direct"><b>长句示范</b>她终于让满朝喊回那声殿下，也终于明白，曾替她梳发的人、教她执笔的人、在雪夜背她回宫的人，都不会从这声呼喊里走回来。</div>
      <div class="note">HE 也能保留破碎感：她可以被爱，但爱不能替她报仇，更不能把付过的代价一键清零。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">代价链</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">07 / 09</div>
    <header class="head"><div class="num">06</div><div><h2>一场公主复仇戏<br>照这 9 拍来写</h2><div class="sub">示例骨架：她以罪臣遗孤的身份，赴仇人的上元宴。</div></div></header>
    <div class="body">
      <div class="beats">
        <div class="beat"><b>01 入局</b>她穿旧衣入宴，任众人拿亡国旧事取乐。</div>
        <div class="beat"><b>02 刺痛</b>故宫旧曲响起，她认出母后曾改过的尾音。</div>
        <div class="beat"><b>03 藏锋</b>她失手打翻酒盏，顺势跪下，像真的慌乱。</div>
        <div class="beat"><b>04 取信</b>主动献上半条“旧臣密道”的假消息。</div>
        <div class="beat"><b>05 误判</b>仇人认定她怕死、无能，准她进入内院。</div>
        <div class="beat"><b>06 取证</b>她从镜中看清书案暗格，不立刻动手。</div>
        <div class="beat"><b>07 折返</b>先救出被牵连的宫女，放弃最安全的撤退时机。</div>
        <div class="beat"><b>08 落子</b>账页送出，同时引两名仇敌互相指认。</div>
        <div class="beat"><b>09 余波</b>满城灯火，她独自把那支旧曲听完。</div>
      </div>
      <div class="note"><strong>这场戏真正的钩子：</strong>她看似一路被羞辱，其实每次低头都换回一条信息；唯一计划外的动作，是她仍救了无辜的人。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">名场面骨架</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">08 / 09</div>
    <header class="head"><div class="num">07</div><div><h2>完整示范段<br>把破碎写进一场旧宴</h2><div class="sub">场景：上元宴上，仇人命她为故国旧曲添酒。</div></div></header>
    <div class="body">
      <article class="prose">
        <p>旧曲响到第三叠，她提壶的手终于停了一瞬。</p>
        <p>那年母后嫌尾音太冷，亲自改过半拍。满殿乐师无人知道，今夜却有人原样奏了出来，像从废墟里翻出一截尚带体温的骨。</p>
        <p>席间有人笑：“听说殿下从前最爱这支曲？”</p>
        <p>她垂下眼，壶口稳稳贴住杯沿：“大人认错了。罪臣之女，不曾听过宫乐。”</p>
        <p>酒满七分，一滴未洒。银壶映出屏风后的半角书案，也映出那人腰间新换的铜钥。她跪得更低，像被旧事吓破了胆，指尖却在裙褶里轻轻数完了守卫换岗的第三遍脚步。</p>
        <p>曲终，她起身告退，顺手扶住被推倒的宫女。为这一扶，她错过了最安全的半刻钟。</p>
        <p>可她若连这一只手都不肯伸，今日夺回山河，来日也不过坐成另一个仇人。</p>
      </article>
      <div class="note">这里没写“破碎、清醒、强大”。旧曲、银壶、脚步与那只伸出去的手，已经把人设说完了。</div>
    </div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">正文示范</div>
  </section>

  <section class="page">
    <img class="avatar" src="../assets/avatar.png" alt=""><div class="pager">09 / 09</div>
    <header class="head"><div class="num">08</div><div><h2>收束小节<br>落难公主复仇系这样写</h2><div class="sub">换掉故国、仇人和代价，就能长成你自己的角色。</div></div></header>
    <div class="body" style="bottom:390px">
      <div class="formula">昔日荣光 × 今日泥泞 × 清醒蛰伏 × 精准清算 × 风骨底线</div>
      <div class="slots">
        <div class="slot">① 她从前拥有过什么，才懂得真正的体面？</div>
        <div class="slot">② 她失去了谁，又为何必须亲自清算？</div>
        <div class="slot">③ 她用哪种卑微身份藏住锋芒？</div>
        <div class="slot">④ 她第一次主动设局，拿谁的弱点做了筹码？</div>
        <div class="slot">⑤ 哪个救助无辜的动作，证明她没有变成仇人？</div>
        <div class="slot">⑥ 她赢回权柄后，永远赢不回什么？</div>
      </div>
      <div class="direct"><b>最后自检</b>删掉“她很惨、她很狠”，读者仍能从选择、筹码、底线和代价里看见她，公主就立住了。</div>
    </div>
    <div class="follow"><img src="../assets/follow-bear-v1.png" alt=""><div><strong>我是小熊。</strong><br>关注我，为你整理直接能拿去写的素材。<br>今天也多码一点。</div></div>
    <div class="page-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="本页面由网文 AI Agent Popwave.cn 生成"></div>
    <div class="brand">小熊起床码字了</div><div class="topic">落难公主复仇系</div>
  </section>
</main>
</body>
</html>
````
