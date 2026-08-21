# 如何写恨海情天｜HTML 源码

原始文件：v1_如何写恨海情天图文_小熊3比4直出版.html

````html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=720, initial-scale=1">
  <title>如何写恨海情天｜小熊起床码字了</title>
  <link rel="stylesheet" href="../assets/xiaoxiong-hardcore-3x4.css">
  <style>
    .content.compact{font-size:16px;line-height:1.55;margin-top:18px}.content.compact p{margin-bottom:10px}
    .page-head.compact-head{margin-top:16px}.compact-head h2{font-size:30px}.compact-head .lead{font-size:15.5px}.compact-head .rule{margin-top:12px}
    .cover h1{font-size:53px}.cover .subtitle{font-size:19px}.cover .brand-mark{margin-top:12px}.cover-viz{margin-top:18px;padding:15px 18px 13px;border:1px solid var(--line);background:rgba(255,252,245,.9)}
    .hate-curves svg{display:block;width:100%;height:190px}.curve-key{display:flex;justify-content:center;gap:28px;margin-top:4px;font-size:12px;color:var(--muted)}.curve-key i{display:inline-block;width:24px;height:4px;margin-right:6px;vertical-align:middle}.love-key{background:#6f4e37}.hate-key{background:#a44738}
    .ledger{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}.ledger-col{padding:12px 13px;border-top:5px solid var(--brown);background:var(--paper-light)}.ledger-col.hate{border-color:var(--red)}.ledger-col b{display:block;margin-bottom:7px;color:var(--red);font-size:14px}.ledger-col span{display:block;padding:5px 0;border-bottom:1px solid var(--line);font-size:12px;line-height:1.35}.ledger-col span:last-child{border:0}
    .scene-engine{display:grid;grid-template-columns:1fr 44px 1fr 44px 1fr;gap:5px;align-items:stretch;margin-top:12px}.engine-cell{padding:11px 8px;border:1px solid var(--line);background:var(--paper-light);text-align:center;font-size:12px;line-height:1.4}.engine-cell b{display:block;color:var(--red);font-size:14px;margin-bottom:5px}.engine-arrow{display:grid;place-items:center;color:var(--red);font-size:24px;font-weight:900}
    .wave-box{margin-top:11px;padding:10px 14px;border:1px solid var(--line);background:var(--paper-light)}.wave-box svg{display:block;width:100%;height:112px}.wave-labels{display:flex;justify-content:space-between;color:var(--muted);font-size:11px}
    .scene-beats{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:10px}.scene-beat{padding:9px 7px;border-top:4px solid var(--red);background:var(--paper-light);font-size:11.5px;line-height:1.38}.scene-beat b{display:block;color:var(--red);font-size:13px;margin-bottom:4px}
    .formula-row{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:12px}.formula-node{position:relative;padding:10px 7px;border:1px solid var(--line);background:var(--paper-light);text-align:center;font-size:12px;line-height:1.4}.formula-node:not(:last-child)::after{content:"+";position:absolute;right:-8px;top:24px;color:var(--red);font-weight:900}.formula-node b{display:block;color:var(--red);font-size:14px;margin-bottom:4px}
    .brand-mark{width:206px;padding:6px 9px;margin-bottom:6px}.footer{font-size:11px}.compare.tight{font-size:12px;margin-top:11px}.compare.tight th,.compare.tight td{padding:7px 8px}.pressure-field.small{height:182px;margin-top:11px}.pressure-field.small .field-node{min-height:42px;font-size:11px}.pressure-field.small .field-center{height:62px}
    .example.tight{margin-top:0;padding:13px 16px;font-size:14.5px;line-height:1.58}.example.tight h3{font-size:16px;margin-bottom:6px}
  </style>
</head>
<body>
<main class="deck" data-xiaoxiong-kind="standard">
  <section class="page cover" id="p01">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <p class="kicker">CP 张力写法｜写作归纳</p>
    <h1>如何写好<br><span class="accent">恨海情天</span></h1>
    <p class="subtitle">爱没有退场，伤害也没有作废。<br>两本账一起涨，纠缠才会越写越深。</p>
    <div class="cover-viz" role="img" aria-label="爱意与恨意在剧情阶段中互相追赶的双曲线">
      <div class="visual-title">爱意证据 × 伤害后果：同场并存，错峰见顶</div>
      <div class="hate-curves"><svg viewBox="0 0 540 190"><path d="M10 42 C105 30 130 62 205 74 S305 125 390 118 S470 76 530 86" fill="none" stroke="#6f4e37" stroke-width="6" stroke-linecap="round"/><path d="M10 142 C105 134 142 102 210 96 S300 54 378 64 S463 128 530 112" fill="none" stroke="#a44738" stroke-width="7" stroke-linecap="round"/><circle cx="212" cy="94" r="8" fill="#f4ead9" stroke="#a44738" stroke-width="4"/><circle cx="390" cy="118" r="8" fill="#f4ead9" stroke="#6f4e37" stroke-width="4"/><text x="176" y="84" fill="#a44738" font-size="13">旧伤被重释</text><text x="397" y="142" fill="#6f4e37" font-size="13">爱以代价现形</text></svg></div>
      <div class="curve-key"><span><i class="love-key"></i>仍在起作用的爱</span><span><i class="hate-key"></i>必须清算的恨</span></div>
      <div class="diagnostic-strip"><div><b>旧爱</b><span>曾经互选</span></div><div><b>真伤</b><span>损失已落地</span></div><div><b>当场</b><span>爱恨同时行动</span></div><div><b>余波</b><span>选择不能复原</span></div></div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜恨海情天</span><span>01 / 10</span></footer>
  </section>

  <section class="page" id="p02">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">01｜先立关系底盘</p><h2>恨得越狠，越要先证明<span class="accent">爱得有凭有据</span></h2><p class="lead">恨海情天的起点，是“我曾把命门交给你，你偏偏拿它伤我”。</p><div class="rule"></div></header>
    <div class="content compact">
      <p>两个人只要互相看不顺眼，写出来更像强强对抗；要到恨海情天，恨意必须长在一段真实旧爱上。先给他们一件只对彼此发生过的事：他把唯一退路告诉她，她替他瞒下足以灭门的身份；她在所有人面前不肯低头，却允许他看见自己最狼狈的那一晚。后来造成伤害的人，恰好握着这份信任，所以一刀下去才会比敌人的刀更深。</p>
      <p>伤害也得具体。别只写“他背叛了她”，要写她因此失去谁、背了什么罪、再也不敢把哪件事交给别人。<mark>可直接套一句：她恨的从来不止那场背叛，她恨自己直到刀落下来，还认得他握刀时怕她疼的旧习惯。</mark>这句话好用，是因为旧爱与新伤挤在同一个动作里，角色没有任何一条轻松的解释可走。</p>
      <div class="mechanism-rail"><div class="rail-node"><b>唯一信任</b><span>把命门交给对方</span></div><div class="rail-node"><b>精准伤害</b><span>偏在旧承诺处落刀</span></div><div class="rail-node"><b>现实损失</b><span>名声、亲人或退路</span></div><div class="rail-node"><b>恨意生根</b><span>爱越真，账越重</span></div></div>
      <div class="feedback-line"><b>追读层：</b>读者会等的，是伤害发生后，他还会不会沿着旧习惯继续爱她，以及她会怎样拒绝这份迟来的照顾。</div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜关系底盘</span><span>02 / 10</span></footer>
  </section>

  <section class="page" id="p03">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">02｜让爱恨同时可见</p><h2>同一个动作里，既要<span class="accent">报复</span>，也要<span class="accent">舍不得</span></h2><p class="lead">情绪写在嘴上会飘，动作有相反方向才会拉扯。</p><div class="rule"></div></header>
    <div class="content compact">
      <p>最省力的写法，是安排角色刚放完狠话就立刻心软。可这种“切换”没有阻力，像作者在替人物按开关。更有劲的场面，会让一个动作同时完成两件互相冲突的事：她公开指认他的罪，却提前换走了会置他于死地的证物；他扣住她做人质，刀锋贴着颈侧，手却垫在她旧伤最重的地方。恨意负责推进局面，残存的爱负责改变动作的形状。</p>
      <p>判断一场够不够纠缠，可以问三个问题：这个动作让谁真正吃亏？它泄露了哪段旧关系？对方看见以后，会误解、利用，还是更加愤怒？<mark>可直接套一句：她把他的罪名一条条念给满殿的人听，唯独漏掉那条足够判死的，因为她要他偿还，不许他用一死把账赖掉。</mark>爱在这里没有替伤害开脱，它只让报复变得更私人、更漫长。</p>
      <table class="compare tight"><tr><th>只写情绪切换</th><th>改成双向动作</th><th>关系变化</th></tr><tr><td>“我恨你”，转身又替他求情</td><td>亲手定罪，却换走致命证物</td><td>他活下来，也知道她仍在乎</td></tr><tr><td>劫持她，随后忽然温柔</td><td>用她换城，同时护住旧伤</td><td>她发现他的狠与软都是真的</td></tr></table>
      <div class="diagnostic-strip"><div><b>明面目标</b><span>赢下这一局</span></div><div><b>暗里泄露</b><span>仍记得她的痛</span></div><div><b>现实后果</b><span>双方都要付费</span></div><div><b>下一问</b><span>这算爱还是控制</span></div></div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜双向动作</span><span>03 / 10</span></footer>
  </section>

  <section class="page" id="p04">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">03｜两本账都要记</p><h2>爱账不能抵债，恨账也<span class="accent">删不掉旧爱</span></h2><p class="lead">让同一件往事，在两个人心里留下两种都成立的解释。</p><div class="rule"></div></header>
    <div class="content compact">
      <p>许多拉扯会写塌，是因为作者急着替一方平反：当年的背叛原来全为保护，于是受伤的人显得不讲理；或者伤害被判得太死，过去所有温柔都成了骗局。可以给角色各记一本账。她记结果：他隐瞒真相，让她替仇人活了三年；他记选择：那一夜只要开口，她就会陪他一起死。两套解释都能拿出证据，也都藏着自私。</p>
      <p>回收秘密时，不要让真相自动完成和解。新信息只负责改写责任比例，损失仍要有人承担。<mark>可直接套一句：他终于把当年的真相交给她，没有求她原谅，只把那把旧钥匙放回桌上；门由他锁了三年，如今该由她决定还开不开。</mark>这会把“爱不爱”的争论推到更难的一层：知道他爱过以后，她是否仍有权不回来？当然有。</p>
      <div class="ledger" data-visual-role="relation"><div class="ledger-col"><b>爱账｜他为什么隐瞒</b><span>怕她陪自己赴死</span><span>替她保住身份与亲人</span><span>代她决定了什么是真正安全</span></div><div class="ledger-col hate"><b>恨账｜她实际失去什么</b><span>三年选择权被拿走</span><span>把仇人当恩人侍奉</span><span>再听真话也会先怀疑</span></div></div>
      <div class="feedback-line"><b>边界：</b>“为你好”可以解释动机，不能注销损失。和解要靠后续行动重新交还选择权。</div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜爱恨两本账</span><span>04 / 10</span></footer>
  </section>

  <section class="page" id="p05">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">04｜把纠缠逐级加价</p><h2>每一轮交锋，都要多<span class="accent">暴露一层爱</span>，多<span class="accent">欠一笔债</span></h2><p class="lead">原地吵十次不叫拉扯；权限、筹码和退路必须跟着变化。</p><div class="rule"></div></header>
    <div class="content compact">
      <p>恨海情天很容易陷进循环：见面讥讽、回忆旧情、误会加深、再见面继续讥讽。更稳的递进，是让双方每次都能做一件上次做不到的事。第一次只敢试探旧习惯，第二次拿共同秘密逼对方让步，第三次公开站到敌对位置，第四次必须决定救不救那个最恨的人。动作升级以后，关系也会换位，昨天掌握解释权的人，今天可能要等一句宣判。</p>
      <p>每级都要同时收费。她救他，便失去彻底否认旧爱的资格；他替她认罪，便让当年的“我别无选择”显得更加可疑，因为如今他明明会选。<mark>安排递进时可以直接套：试探旧习惯 → 利用旧信任 → 公开伤害 → 在不可逆处仍选择对方。</mark>最后一级最重要，角色要清醒地知道代价，依旧伸手。那一刻爱才从回忆变成当下证据。</p>
      <div class="steps"><div class="step"><b>01 试探</b><span>叫旧称呼、留旧物<br>代价：先暴露在意</span></div><div class="step"><b>02 利用</b><span>拿软肋换筹码<br>代价：信任再裂一次</span></div><div class="step"><b>03 公开</b><span>阵营与罪名摆上桌<br>代价：再无体面退路</span></div><div class="step"><b>04 选择</b><span>明知会输仍救对方<br>代价：承认爱未死</span></div></div>
      <div class="diagnostic-strip"><div><b>筹码</b><span>一轮比一轮重</span></div><div><b>权限</b><span>解释权不断换手</span></div><div><b>伤口</b><span>旧账被新行动重写</span></div><div><b>终局</b><span>必须清醒选择</span></div></div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜递进加价</span><span>05 / 10</span></footer>
  </section>

  <section class="page" id="p06">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">05｜一场戏的发动机</p><h2>让台词交锋，动作<span class="accent">偷偷泄底</span></h2><p class="lead">嘴上争的是当下输赢，身体记得的却是旧关系。</p><div class="rule"></div></header>
    <div class="content compact">
      <p>写对手戏时，先给双方一个必须当场解决的公开目标：抢证据、换人质、争继承权、逼对方承认罪名。再给其中一人一个不能让旁人看见的私心，比如拖延搜查，好让对方逃；故意激怒她，免得她发现自己中毒；把最狠的话说给满堂人听，却把真正的警告藏进只有两人懂的旧称呼。公开目标让剧情往前走，私心让关系往深处陷。</p>
      <p>场尾还要留下后坐力。对方有没有看懂这次保护？看懂以后会感动，还是更恨？如果她认为“你又替我决定”，爱意泄露反倒会把旧伤撕得更开。<mark>可直接套一句：他说的每个字都在逼她认罪，手指却在桌下轻轻敲了三下，那是很多年前他们约好的，快走。</mark>一句台词、一处暗号、一个误读，便能把情节目标和情感账绑在一起。</p>
      <div class="scene-engine" data-visual-role="relation"><div class="engine-cell"><b>明面争夺</b>谁拿走证据<br>谁掌握解释权</div><div class="engine-arrow">→</div><div class="engine-cell"><b>私心泄露</b>旧暗号、护伤动作<br>故意留一条路</div><div class="engine-arrow">→</div><div class="engine-cell"><b>关系后坐力</b>被看懂、被误解<br>或被反过来利用</div></div>
      <div class="coupling-map"><div class="coupling-head">局面结果</div><div class="coupling-head">同一动作</div><div class="coupling-head">关系结果</div><div class="coupling-cell">她背上罪名，暂时失势</div><div class="coupling-cell action">公开指认</div><div class="coupling-cell">她发现他漏掉死罪</div><div class="coupling-cell">他放走人质，失去筹码</div><div class="coupling-cell action">暗号示警</div><div class="coupling-cell">旧默契重新起作用</div></div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜对手戏发动机</span><span>06 / 10</span></footer>
  </section>

  <section class="page" id="p07">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">06｜守住人物边界</p><h2>伤害可以很重，关系却不能靠<span class="accent">失去选择权</span>续命</h2><p class="lead">虐待、囚禁、羞辱若没有后果，只会消耗张力。</p><div class="rule"></div></header>
    <div class="content compact">
      <p>恨海情天允许角色做错事，甚至做出很难原谅的事；作者要记得，严重伤害会改变关系资格。囚禁之后不能靠一场发烧照顾就回到暧昧，公开羞辱也不能用“他其实吃醋”轻轻带过。受伤的一方需要真实反制：离开、夺回资源、公开拒绝、建立新的盟友。施害者则要失去曾经默认拥有的权限，想再靠近，只能重新申请。</p>
      <p>判断尺度时，看作品有没有把她的“拒绝”当成有效行动。她说不，剧情是否真的停下？她决定不原谅，故事有没有允许这个选择存在？<mark>好看的修复并非他受多少苦，而是他终于学会：爱她这件事，不能继续替她做主。</mark>如果最终复合，要靠持续行动补回具体损失；如果无法补回，也可以让爱留下，让关系结束。恨海情天不必强行大团圆。</p>
      <div class="pressure-field small"><div class="field-center">她的选择权</div><div class="field-node nw">身体边界：拒绝能否生效</div><div class="field-node ne">资源边界：能否独立离开</div><div class="field-node sw">叙事边界：痛苦是否被承认</div><div class="field-node se">关系边界：复合由谁决定</div></div>
      <div class="feedback-line"><b>反制层：</b>让受伤者亲手拿回资源、解释权和拒绝权；让施害者承担“可能永远得不到原谅”的结果。</div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜边界与修复</span><span>07 / 10</span></footer>
  </section>

  <section class="page" id="p08">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">07｜控制爱恨节奏</p><h2>别平均撒糖撒刀，要让两条线<span class="accent">错峰见顶</span></h2><p class="lead">一边刚赢，另一边立刻用代价把胜利改写。</p><div class="rule"></div></header>
    <div class="content compact">
      <p>爱恨各占一半，听起来平衡，写出来常常很平。更好的节奏是阶段性偏斜：开局让恨意占上风，读者先看见伤害与敌对；中段漏出旧爱证据，但证据不够洗清责任；后段让两人被迫共同完成一件事，旧默契复活，新的损失也随之发生；终局再把“是否继续相爱”与“是否必须偿还”分开作答。爱可以确认，关系未必复原。</p>
      <p>每次情绪抬头，都用外部行动验真。嘴上越恨，越要看他会不会在不可逆处收手；心里越爱，越要看她能不能在他示弱时仍坚持清算。<mark>可直接套节奏：恨赢局面 → 爱改动作 → 误读加深 → 共同行动 → 真相重释 → 清醒选择。</mark>千万别每隔一章安排一次强吻、一次吵架。那是重复刺激，没有关系位移，也留不下新的账。</p>
      <div class="wave-box" data-visual-role="relation"><svg viewBox="0 0 540 112"><path d="M8 30 C62 18 93 23 130 58 S208 91 260 68 S333 18 392 44 S468 89 532 72" fill="none" stroke="#6f4e37" stroke-width="5"/><path d="M8 91 C75 81 92 48 145 35 S230 43 278 66 S350 94 408 72 S478 29 532 42" fill="none" stroke="#a44738" stroke-width="6"/><line x1="145" y1="10" x2="145" y2="102" stroke="#9d9186" stroke-dasharray="4 5"/><line x1="392" y1="10" x2="392" y2="102" stroke="#9d9186" stroke-dasharray="4 5"/></svg><div class="wave-labels"><span>敌对开局</span><span>旧爱漏出</span><span>共同任务</span><span>真相重释</span><span>清醒选择</span></div></div>
      <div class="diagnostic-strip"><div><b>恨赢</b><span>局面被推进</span></div><div><b>爱漏</b><span>动作发生变形</span></div><div><b>再加价</b><span>误读或损失落地</span></div><div><b>终局</b><span>爱与关系分开答</span></div></div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜爱恨节奏</span><span>08 / 10</span></footer>
  </section>

  <section class="page" id="p09">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head compact-head"><p class="eyebrow">08｜完整正文示范</p><h2>她来杀他，他却把<span class="accent">唯一的出口</span>留给她</h2><p class="lead">原创写法演示：明面清算 × 暗里示警 × 关系换位。</p><div class="rule"></div></header>
    <div class="content compact">
      <div class="example tight"><h3>可直接仿写</h3><p>雨水顺着刀尖滴在他的案卷上。她把那页供词推过去，声音很稳：“三年前北门失守，守军名册被人换过。你的印。”他看完，只问她一路进来，有没有碰见巡夜司。她笑了一声，刀锋往前送了半寸：“你还是先想想自己的命。”门外忽然响起甲叶摩擦声。他抬手，像从前替她整理披风那样，替她掖好被雨打湿的衣领，指节在她肩头敲了两下。左窗。旧暗号。她的刀没有动：“你以为放我走，这笔账就清了？”“清不了。”他把染血的印章塞进她掌心，合拢她的手指，“所以活着回来，慢慢算。”下一刻，他转身推翻烛台。火沿着案卷窜起，门被撞开的瞬间，她从左窗跃进雨里。身后有人问他刺客去了哪里。他望着她消失的方向，抬手指向相反的长街。</p></div>
      <p>这场里，她的刀和供词负责清算，他的问话、旧暗号与错指方向泄露爱意；他烧掉案卷，也让她暂时失去公开定罪的证据。救她和伤她发生在同一场，谁都没被洗白。<mark>短句“左窗。旧暗号。”让旧默契突然回到现场，后面的“慢慢算”则把爱写成继续受审的意愿。</mark></p>
      <div class="scene-beats" data-visual-role="relation"><div class="scene-beat"><b>旧证据</b>敲肩两下，是从前的逃生暗号</div><div class="scene-beat"><b>当下争夺</b>供词与印章决定谁能定罪</div><div class="scene-beat"><b>双向代价</b>他毁证护她，她更难清算</div><div class="scene-beat"><b>余波钩子</b>她握着印章，还会回来算账</div></div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊素材本｜完整示范</span><span>09 / 10</span></footer>
  </section>

  <section class="page" id="p10">
    <div class="brand"><img src="../assets/avatar.png" alt="小熊头像"><span>小熊起床码字了</span></div>
    <header class="page-head"><p class="eyebrow">09｜收进素材本</p><h2>恨海情天<span class="accent">这样写</span></h2><p class="lead">旧爱证据 + 真实伤害 + 同场双向动作 + 不能轻轻翻篇的代价。</p><div class="rule"></div></header>
    <div class="content" style="font-size:15.5px;line-height:1.5;margin-top:18px">
      <div class="formula-row" data-visual-role="relation"><div class="formula-node"><b>旧爱证据</b>只对彼此发生过的信任、暗号或破例</div><div class="formula-node"><b>真实伤害</b>失去亲人、名声、资源、自由或判断力</div><div class="formula-node"><b>双向动作</b>明面报复，暗里仍保护或记得</div><div class="formula-node"><b>不可逆代价</b>关系资格改变，和解必须重新申请</div></div>
      <table class="compare tight"><tr><th>填槽位</th><th>你的 CP</th></tr><tr><td>他曾把什么命门交给她</td><td>秘密 / 退路 / 身份 / 唯一一次示弱</td></tr><tr><td>后来偏在何处伤了她</td><td>把旧信任变成最准确的刀</td></tr><tr><td>她因此实际失去什么</td><td>不要只填“很痛苦”，写可见损失</td></tr><tr><td>下一场明面争什么</td><td>证据 / 人质 / 阵营 / 继承权 / 生路</td></tr><tr><td>哪个动作泄露爱还活着</td><td>旧暗号 / 护伤 / 留路 / 漏掉死罪</td></tr><tr><td>终局是否复合</td><td>由修复结果决定，不拿爱自动抵债</td></tr></table>
      <div class="follow"><img src="../assets/follow-bear-v1.png" alt="拿着本子的小熊"><p><b>我是小熊。</b><br>关注我，为你整理直接能拿去写的素材。<br>今天也多码一点。</p></div>
    </div>
    <div class="brand-mark"><img src="../assets/branding/popwave-ai-agent-attribution-brand-blue.png" alt="Popwave AI Agent"></div>
    <footer class="footer"><span>小熊起床码字了｜个人写作素材本</span><span>10 / 10</span></footer>
  </section>
</main>
</body>
</html>
````
