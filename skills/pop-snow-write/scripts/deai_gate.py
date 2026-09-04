#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deai_gate.py —— 正文去AI味门禁 v2.1

零风险自动修（--fix，机械替换，不碰语义）+ 滥用检测（报告定位，agent 自查自修）。

用法:
  python deai_gate.py <文件或目录>               仅检测出报告
  python deai_gate.py <文件或目录> --fix        自动修零风险项 + 出报告
  python deai_gate.py <文件> --json             JSON 输出（agent 消费）
  python deai_gate.py <文件> --fix --json       修复 + JSON
  python deai_gate.py <目录> --fix              批处理（目录下 *.txt，不递归）

退出码: 0=无WARN/FAIL  1=存在需自查项  2=参数或文件错误

检测面（2026-09-05 大范围调研扩容。来源：NGA"AI惯犯句式""还我一双没看过ai写作的眼睛"
"抵制ai入侵"、晋江读者帖、头条"AI写小说的特点"词汇分类表、碎嘴子老王AI文清单、
GitHub cn-humanizer中文AI词汇表、番茄2026低质治理公告、smzdm编辑去味法）:
  1. 套话硬模板 ~120条（瞳孔地震/唇角微勾/顿了顿/眸光/名为X的情绪/并不存在的眼镜/
     X感词族/章末悬念模板/马尔克斯开头/外貌脸谱/世界只剩声音…）
  2. 软密度 ~28组（一丝一抹/急转副词/眸系/意象动词/抽象名词/感到式情绪/副词道白/
     承接套话/句首而字/绝对量词/精确计时/环境名词/此刻强调/AI高频成语…）
  3. 结构统计（句长段长变异/四字格连排/长短语重复/超长段/开篇环境堆砌/语气词缺失/
     语气句缺失/超短段连击/无对话长流/气口缺失——的着了/代词/顿号低于人书基线）
  4. 工具痕迹（已思考/嗯，用户/（96字）/markdown残留/HTML残留/单引号/
     emoji残留/舞台指示（笑）/场景标注【旁白】/英文残留行——实锤级）

阈值校准依据（2026-09-05，参考小说txt人书抽样 vs AI样文，详见 temp/_cal4.py）:
  句号密度   人书 21-38/千字 → WARN 45 / FAIL 55
  破折号密度 人书近零       → WARN 1.0 / FAIL 2.0（/500字）
  省略号     人书 0-11.1/千字 → WARN 8 / FAIL 12（对话尾……系作者风格）
  人书误伤校准轮（6本×章节对齐段回归，FAIL 全清零）:
  语气词/语气句/四字格连排/5字重复/段长CV/单引号 → REPORT_ONLY（人书风格方差过大）
  引号未配对 WARN 3/FAIL 6（跨行引文块合法）；烙印移出意象动词（奴隶烙印实体用法）
  en_line 需两个3+字母英文词（"mss！"单词感叹对白放行）
  原则：WARN 线压人书最大值上方，FAIL 再上浮——人书全过、AI稿多挂。
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter

CJK = r'\u4e00-\u9fff'
# 汉字 + 常用中文标点（判断"英文标点是否长在中文语境里"的邻接集）
CJKX = (r'\u4e00-\u9fff\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09'
        r'\u201c\u201d\u2018\u2019\u2026\u2014\uff5e\u300a\u300b\u3010\u3011')

# 检查项定义: (id, 名称, warn阈值, fail阈值, 单位说明, 修法指引)
CHECKS = [
    # --- 密度类（/千字） ---
    ('period_density',  '句号密度',   45, 55, '/千字', '砍碎句、合并同主语短句，让部分句子回到15字以上'),
    ('ellipsis_density', '省略号密度', 8, 12, '/千字', '省略号改逗号或句号，只留情绪停顿必要处（对话尾……是作者风格，酌情豁免）'),
    ('cliche_hits',     'AI套话密度', 3, 6, '/千字', '套话库命中（瞳孔地震/唇角微勾/名为X的情绪类），按命中处改写为具体动作'),
    ('yisi_density',    '一丝一抹',   8, 15, '/千字', '"一丝/一抹/一缕+抽象名词"换成具体可感细节'),
    ('simile_density',  '比喻引导词', 6, 10, '/千字', '仿佛/宛如/犹如/似乎扎堆——留一两处，其余改直陈或换具体意象'),
    ('burst_adv',       '急转副词',   5, 9, '/千字', '猛然/骤然/蓦地/倏地扎堆，多改"突然"或直接写动作本身'),
    ('redup_density',   '叠词副词',   15, 25, '/千字', '缓缓/微微/淡淡/轻轻扎堆，删一半不影响意思'),
    ('mou_density',     '眸系描写',   2, 4, '/千字', '眸光/眸底/抬眸——AI高频眼部修辞，换直白眼神动作或删'),
    ('voice_adj',       '声音形容词', 2, 4, '/千字', '"低沉/沙哑/清冷的嗓音"模板——写台词内容本身带语气'),
    ('gaze_v',          '凝视扫视',   2, 4, '/千字', '凝视/扫视/注视扎堆——换"看了一眼/瞥"等具体动作'),
    ('envverb_density', '意象动词',   2, 4, '/千字', '勾勒/描摹/晕染/氤氲/浸染——文艺滤镜动词，换成看得见的动作'),
    ('abstract_density','抽象意象',   3, 6, '/千字', '悸动/涟漪/暖流/寒意/迷雾/枷锁——落到具体可感细节'),
    ('feel_filter',     '感到式情绪', 2, 4, '/千字', '"感到一阵X/涌上心头"——删情绪标签，写身体反应和动作'),
    ('dialog_tag',      '副词道白',   5, 9, '/千字', '低声道/沉声道/淡淡道扎堆——多数直接写"说"，让台词自带语气'),
    ('nod_shake',       '点头摇头',   3, 6, '/千字', '点了点头/摇了摇头扎堆——换别的回应动作或干脆省略'),
    ('dun_dun',         '顿了顿',     2, 4, '/千字', '"顿了顿"是AI头号口癖——删掉多数，一章最多留一处'),
    ('just_then',       '承接套话',   3, 6, '/千字', '就在这时/下一秒/闻言扎堆——换自然承接方式'),
    ('trans_density',   '书面转折',   4, 7, '/千字', '然而/但是/不过/可是——网文口语少书面转折，删一半改直叙'),
    ('degree_adv',      '程度副词',   4, 8, '/千字', '非常/十分/极其——多数直接删，把程度写进内容本身'),
    ('precise_num',     '精确数字',   1, 2, '/千字', '"前倾15度/快了三拍/百分之30"——换模糊量词或体感（系统面板内数字合法）'),
    ('semicolon',       '分号密度',   0.5, 1.5, '/千字', '网文极少用分号——改逗号或句号'),
    ('gan_sense',       'X感词族',    1, 2, '/千字', '宿命感/破碎感/少年感/氛围感——AI抽象审美词，换成看得见的画面'),
    ('ta_knows',        '他知道句',   2, 4, '/千字', '"他知道，/他明白，"全知旁白腔——多数删，信息放进动作和对白'),
    ('fact_adv',        '阐释副词',   1, 2, '/千字', '事实上/实际上/某种程度上——删掉直接给内容'),
    ('universal_q',     '绝对量词',   3, 6, '/千字', '一切/所有/全部扎堆——落到具体的人事物'),
    ('time_precise',    '精确计时',   1, 2, '/千字', '三秒后/五分钟后——改模糊时间（片刻后/过了一阵）'),
    ('env_noun',        '环境名词',   6, 10, '/千字', '夜色/月光/暮色/晚风扎堆——环境描写减半，留最有用的一笔'),
    ('zhe_yike',        '此刻强调',   3, 5, '/千字', '在这一刻/此时此刻/这一瞬间扎堆——多数删，时间感用动作带出'),
    ('ai_idiom',        'AI高频成语', 3, 6, '/千字', '心照不宣/油然而生/百感交集类扎堆——换白话或具体动作'),
    ('emotion_adv',     '情绪副词',   2, 4, '/千字', '愤怒地/悲伤地/复杂地——删副词，情绪写进动作和台词'),
    ('causal_density',  '因果解释',   5, 8, '/千字', '因为/由于/为了/试图/想要扎堆——AI爱解释动机，删掉让动作自己说'),
    ('nominal_v',       '名词化动词', 1, 2, '/千字', '进行了/做出了/完成了——直接写动词（进行了一场比赛→比了一场）'),
    ('er_start',        '句首而字',   3, 5, '/千字', '句子以"而"开头（而这一切/而他）——改直接陈述'),
    ('paren_note',      '括号注释',   7, 10, '/千字', '正文里（说明性括号）——AI爱夹注，删掉或改进叙述'),
    # --- 模板类（处） ---
    ('parallel',        '对仗关联词', 3, 5, '处', '拆成两个独立短句，删"而是/而且/更是"这类对仗轴'),
    ('heart_pat',       '心中一X',    2, 4, '处', '"心中一紧/一沉"族改外显：手停了/话没接住'),
    ('eye_pat',         '眼部模板',   2, 4, '处', '眼中闪过/瞳孔紧缩族换成具体反应或删'),
    ('freeze_pat',      '凝固套话',   1, 2, '处', '空气凝固/时间凝固——写在场者具体的反应替代'),
    ('triple_pat',      '三连排比',   1, 2, '处', '有人X有人X有人X/一切X都X——打散成具体的人'),
    ('cliff_tmpl',      '悬念引导语', 2, 4, '处', '殊不知/谁也没想到/而他不知道——旁白全知预告少用'),
    ('mental_direct',   '心理直述',   3, 6, '处', '心想/暗想/暗忖——改动作外显或删'),
    ('idiom_runs',      '四字格连排', 1, 2, '处', '三个以上四字短语连排（勤奋工作，努力学习，积极进取）——拆散、换长短、塞具体细节'),
    ('repeat_phrase',   '长短语重复', 1, 2, '处', '同一5字以上片段反复出现——换说法或删'),
    ('frag_runs',       '碎句连段',   3, 6, '处', '连续3句以上的超短句，合并或补细节拉长其中一两句'),
    ('even_runs',       '句长均匀连3', 3, 6, '处', '连续3句同为15-25字，穿插超短句或拉长一句打破节奏'),
    ('para_start_rep',  '段首重复',   3, 5, '处', '连续3段以上同词开头（都是"他"），换视角词或并入前段'),
    ('subj_rep',        '主语连缀',   2, 4, '处', '连续3句以上"他/她+动词"开头——换主语或省略主语'),
    ('para_wall',       '超长段',     1, 3, '处', '单段≥180字——拆段；网文段落1-3行（≤90字）为宜'),
    ('env_open',        '开篇环境堆砌', 1, 9, '处', '开篇无对话纯写景堆形容词——前3段内让人说话或动起来'),
    ('name_style',      'AI人名风',   1, 2, '处', '昱珩/司辰/晚晚类AI味名字——起接地气或有糙感的名字'),
    ('punch_para',      '超短段连击', 2, 4, '处', '连续3段≤6字的强调腔——留一处，其余并入或扩写'),
    ('env_run',         '无对话长流', 5, 7, '处', '连续8段以上无对白——插一句台词或动作反应打破叙述流'),
    ('enum_list',       '提纲式列举', 0, 1, '处', '"一、二、三"式列举行——正文不许提纲化，改成叙述或删除'),
    # --- 统计类（系数/比例） ---
    ('dash_density',    '破折号密度', 1.0, 2.0, '/500字', '多数破折号改为逗号断句或直接删；一章只留最有必要的一两处'),
    ('sent_cv',         '句长变异系数', 0.38, 0.30, '', '全章句长波动太小（AI平稳句），穿插极短句和长句拉开方差'),
    ('para_cv',         '段长变异系数', 0.45, 0.35, '', '段落长度过于均匀，合并或拆分几段打破节奏'),
    ('dialog_ratio',    '对话比例',   0, 0, '', '过低像说明书、过高像剧本；自然区间约5%-65%（本项只报数不判级）'),
    ('ngram_rep',       '四字片段重复率', 0.11, 0.14, '', '同一4字片段反复出现（机械重复感），换说法或删'),
    ('ngram3_rep',      '三字片段重复率', 0.24, 0.30, '', '同一3字片段反复出现（平台检测最重权重维度之一），换说法或删'),
    ('punct_cv',        '标点节奏变异', 0.30, 0.22, '', '标点间隔过于均匀（AI平板节奏），用长短句打破'),
    ('sem_smooth',      '顺滑句对占比', 0.15, 0.25, '', '相邻句高度相似（AI语义过顺滑），插跳跃、换话题或删'),
    ('ttr',             '二字组多样性', 0.66, 0.62, '', '用词多样性过低（翻来覆去那几个词），引入新词和具体名词'),
    ('tone_div',        '语气句比例', 0.15, 0.08, '', '问句/感叹句太少（AI平板叙述）——对白里加反问和情绪句'),
    ('modal_part',      '语气词密度', 3, 1.5, '/千字', '对白里几乎没有啊/吧/呢/嘛（AI平板腔）——给台词加口气'),
    ('dunhao',          '顿号密度',   1, 0.3, '/千字', '仅报数：AI几乎不用顿号；人书方差也大（0-8/千字），不作判级依据'),
    ('func_word',       '的着了气口', 36, 28, '/千字', '的/着/了密度低于人书基线（AI缺气口）——补自然口语连接'),
    ('pron_density',    '代词气口',   5.5, 4, '/千字', '这/那/这个/那个密度过低（AI少指代）——指代落地到人和物'),
    # --- 其他 ---
    ('connectives',     '模板连接词', 2, 4, '处', '段首句首的过渡词直接删，用话题自然承接'),
    ('cjk_space',       '中文间空格', 2, 4, '处', '确认是AI误加（删）还是收件人/名单类有意排版（留）'),
    ('quote_unpaired',  '引号未配对', 3, 6, '处', '补齐或删除落单引号；跨行引文块（法术/书信说明，首行“末行”）与多段对话约定属合法，豁免'),
    ('sq_quote',        '单引号使用', 4, 8, '处', '少量‘’多为术语引用/内心独白惯例（人书合法）；整章大量出现才可能是AI格式转换——按书内惯例判断'),
    ('ai_meta',         'AI工具痕迹', 0, 1, '处', '生成器残留（已思考/嗯，用户/（96字）/如果你想）——整行删除'),
    ('stage_dir',       '舞台指示',   0, 1, '处', '（笑）（叹气）（沉默）剧本式残留——改为正文动作描写'),
    ('bracket_label',   '场景标注',   0, 1, '处', '【场景】【旁白】结构标注残留——整行删除，信息融进正文'),
    ('emoji_res',       'emoji残留',  0, 1, '处', '正文emoji——生成器残留，删除'),
    ('en_line',         '英文残留行', 0, 1, '处', '整行英文——生成器残留，删除或重写'),
]

# ---- AI套话库（硬模板：人书低频、AI高频的标志性句式，按密度判级）----
# 调研来源：NGA/晋江/头条/碎嘴子老王/GitHub cn-humanizer，2026-09汇总
CLICHE_HARD = [
    # 眼/瞳/眸
    r'瞳孔(地震|骤缩|微缩|紧缩|放大)',
    r'眼中闪过一丝',
    r'(眼|眸)底闪过',
    r'眼中(划过|浮现|暗藏)',
    r'眼神一(凝|暗|凛|闪)',
    r'眸光一(沉|冷|凝|暗|闪|厉)',
    r'(抬|垂|敛)眸',
    r'深不见底的|深不可测的',
    r'(没有|毫无)(丝毫|一丝)?笑意',
    r'眼底(有|含|噙|藏着)|眼底(笑意|雾气|微光)',
    # 唇/嘴
    r'嘴角勾起一抹',
    r'勾起(一抹|一个)(玩味|莫名|危险|似笑非笑)的?弧度',
    r'唇角(微微|轻轻)?(勾|扬|勾起|扬起)',
    r'薄唇(轻)?(启|抿|勾)',
    r'似笑非笑',
    # 面部/身体反应
    r'心脏骤缩',
    r'心跳(漏了|停了)一拍',
    r'倒吸一口(凉气|冷气)',
    r'指节(发白|泛白|抠得发白)',
    r'喉结(上下)?滚(动|了滚)',
    r'下颌线(绷出|紧绷)',
    r'挑了挑眉',
    r'眉心(紧锁|微蹙)|眉头紧锁',
    r'深吸(了)?一口(凉)?气',
    r'脊背(发凉|一僵)|寒意顺着(脊背|脊椎)',
    r'浑身(一僵|发抖|战栗)',
    r'死死(盯|攥|抓|按|掐|抵|顶|撑|扣)',
    r'握紧(了)?(拳头|双拳)',
    r'指尖(摩挲|轻颤|微颤|蜷缩|敲击)|指腹摩挲',
    r'摩挲',
    r'骨节分明|指节分明|修长的?手指',
    r'推了推(眼镜|镜框)|抹平(了)?(并不存在的?)?褶皱',
    r'并不存在的',
    r'猛地(睁眼|回头|抬头|转身|站起)',
    r'咬(牙切齿|紧牙关)|牙关紧咬',
    r'(面色|脸色)(惨白|煞白|铁青|苍白如纸)',
    r'(猛然|浑身|身躯)一震',
    # 环境/气氛
    r'(空气|气氛|时间)仿佛?(在这一刻)?凝固',
    r'空气瞬间凝固',
    r'激起(层层|一圈圈)涟漪',
    r'投入湖面(的)?(一颗|一粒)(石子|石头)',
    r'像一颗?石子投入',
    r'(空气|气氛)(仿佛|似乎)?(都)?安静(下来)?',
    r'(气氛|温度)(仿佛)?降到了?冰点',
    r'落针可闻|针落可闻|鸦雀无声|死(一?般)?的?寂静',
    r'空气里?弥漫',
    r'(月光|灯光|阳光|夕阳|晨光|暮色)(洒|落|倾泻|洒落)',
    r'微风(拂过|轻拂|吹拂)|晚风(拂|掠)',
    r'光影(交错|交织|斑驳)',
    r'猎猎作响',
    # 心理
    r'心中暗道|心中暗想|暗自思忖',
    r'心中一(凛|震|悸|颤|沉|紧)',
    r'心里咯噔',
    r'内心深处|心底深处|灵魂深处|内心最深处',
    r'名为[^，。！？]{1,8}的?(情绪|感觉|感受|东西)',
    r'一种名为',
    r'涌上心头|涌上心间|涌上鼻腔',
    r'说不清道不明|难以言喻|难以名状|难以言表|无法言喻|不可名状|言语(无法|难以)(形容|描述)',
    r'某种(情绪|感觉|东西|意味|直觉|不安|预感|不祥)',
    r'莫名(的|地)?(情绪|不安|心悸|慌乱|熟悉|悸动)',
    r'微不可察|几不可(闻|察|见)',
    # 动作/对话
    r'一声不吭地',
    r'久久没有说话',
    r'沉默(了)?(片刻|半晌|许久)',
    r'上下打量',
    r'(低声|轻声)呢喃|喃喃自语',
    r'一字一顿',
    r'语气(平淡|平稳|平静)|像在(陈述|讲述|叙述|复述)别人的故事',
    r'这就够了',
    r'不由得?',
    # 意象词
    r'氤氲',
    r'眼眶(泛红|湿润|一热)',
    r'眼眶(噙|含)(着)?泪',
    # 悬念旁白
    r'命运(的齿轮|之轮)',
    r'而他(还)?不知道的是|他不知道的是|此时尚不知|殊不知',
    r'无声的(警告|压迫|威慑)',
    # X感词族（AI审美抽象化，2026-09 NGA/晋江读者实锤）
    r'(宿命|破碎|少年|故事|氛围|松弛|距离|疏离|危险|压迫|孤独|荒凉|无力|撕裂|神秘|仪式)感',
    # 外貌脸谱模板
    r'五官(立体|分明|深邃)|轮廓(分明|深邃|锐利)|眉眼(清隽|干净)',
    r'气质(清冷|沉稳|矜贵|疏离|温润|凛然)',
    r'周身(气场|气息)|身上(有|透着)(一?种|说不清|难以言喻)',
    r'眼底(藏着|盛着)(星辰|星光|大海|碎光)',
    r'眼底(的)?(情绪|神色)(翻涌|涌动|流转)',
    r'深深(地)?看了[^。！？\n]{0,6}一眼',
    r'终究没有(说话|开口|回头|挽留)',
    # 章末悬念模板
    r'而这[，,]?(仅仅|只是)?(是)?(个)?(新)?的?开始',
    r'真正的?[^。！？\n]{1,10}(还)?在(后面|后头|路上|前方)',
    r'一切[，,]?(都)?才(刚刚)?开始',
    r'(帷幕|大幕)(就此)?(缓缓)?(拉开|落下|开启|降下)',
    r'属于(他|她|它|他们)的(时代|传奇|征程|故事|舞台)',
    r'好戏[，,]?才(刚刚)?(开始|上演)',
    # 马尔克斯开头
    r'多年(以后|之后)[^。！？\n]{0,15}(想起|记得|回忆)',
    r'那(一)?年[，,]?[^。！？\n]{0,8}(他|她)(还|只|不过)',
    # 嘴上心里模板
    r'嘴上[^。！？\n]{0,15}[^。！？\n]{0,15}(心里|心底|内心)却',
    r'脸上[^。！？\n]{0,8}却(藏|掩)不住',
    # 世界只剩声音
    r'世界[^。！？\n]{0,8}(安静|寂静)[^。！？\n]{0,6}只剩',
    r'只剩下[^。！？\n]{0,12}的?(声音|呼吸)',
    # 双重否定/自问自答
    r'不是没有',
    r'答案(是否定|肯定|显而易见)的',
    # 拟人环境
    r'(夜色|月光|微风|暮色|晨光|细雨)(仿佛|似乎)?[^。！？\n]{0,6}(诉说|见证|守护|抚摸)',
    r'诉说(着|了)|见证(着|了)(一切|历史)|承载(着|了)[^。！？\n]{0,8}(记忆|重量|期望)',
    # 深度套话
    r'不可思议',
    r'眼神(深处)|笑容(背后|深处)',
    r'看不(清|透)的?(情绪|神色|表情)',
    r'藏(着)?不?住?的?(笑意|情绪|锋芒|野心)',
    r'野心(昭然|勃勃)?(写在|爬上)[^。！？\n]{0,6}脸上',
]
CLICHE_RE = [re.compile(p) for p in CLICHE_HARD]

# ---- 软信号组（人书也用，看密度扎堆程度；/千字判级）----
SOFT_GROUPS = [
    ('yisi_density',    r'一丝|一抹|一缕'),
    ('simile_density',  r'仿佛|宛如|犹如|如同|恰似|恍若|似乎'),
    ('burst_adv',       r'猛然|骤然|陡然|霎时|刹那间|蓦地|蓦然|倏地|倏然|乍然'),
    ('redup_density',   r'缓缓|微微|淡淡|轻轻|静静|默默|悄悄|深深|冷冷|幽幽|森然'),
    ('mou_density',     r'眸光|眸底|眸中|眸色|眸子|眼眸|凤眸|美眸|黑眸|星眸'),
    ('envverb_density', r'勾勒|描摹|渲染|晕染|氤氲|浸染|蛰伏|流淌|交织|弥漫|刻入'),
    ('abstract_density', r'悸动|涟漪|暖流|寒意|迷雾|枷锁|漩涡|暗流|寒潭|冰层|深渊'),
    ('feel_filter',     r'感到|感受到|感觉到|意识到|涌上心头|涌上心间|心中涌起|心底泛起|泛起(一丝|一阵|阵阵)'),
    ('dialog_tag',      r'(?:低声|沉声|冷声|淡声|轻声|缓声|柔声|厉声|朗声|幽幽|淡淡|缓缓)(?:地)?(?:说|道|开口|笑|问)'),
    ('nod_shake',       r'点了点头|点了下头|点点头|摇了摇头|摇摇头'),
    ('dun_dun',         r'顿了顿'),
    ('just_then',       r'就在这时|就在此刻|就在此时|下一秒|下一刻|话音(刚落|未落|落下)|此话一出|闻言|听到这话'),
    ('trans_density',   r'然而|但是|不过|可是'),
    ('degree_adv',      r'非常|十分|极其|格外|异常|相当|特别|颇为|甚为'),
    ('precise_num',     r'\d+(度|拍|分贝|%)|百分之[一二三四五六七八九十\d]'),
    ('semicolon',       r'；'),
    # --- v2.1 新增（NGA气口理论/火山引擎检测维度/社区鉴AI法，2026-09-05）---
    ('ta_knows',        r'(他|她)(知道|明白|清楚)[，,]'),
    ('fact_adv',        r'事实上|实际上|某种(程度|意义)上|从某种意义'),
    ('universal_q',     r'一切|所有'),
    ('time_precise',    r'\d+(秒|分钟|小时|天)后'),
    ('env_noun',        r'夜色|月色|晨光|暮色|雾气|雨丝|晚风|夜风|灯火|薄雾|月华'),
    ('zhe_yike',        r'在这一刻|此时此刻|这一瞬间|刹那间'),
    ('ai_idiom',        r'恍然大悟|不由自主|情不自禁|如释重负|若有所思|意味深长|理所当然|'
                       r'心领神会|哑口无言|心照不宣|油然而生|与生俱来|挥之不去|百感交集|'
                       r'五味杂陈|循循善诱|语重心长|耐人寻味|瞠目结舌|面面相觑|不约而同|'
                       r'异口同声|势在必行|顺理成章|水到渠成|心有灵犀|了然于胸|跃然纸上|'
                       r'溢于言表|尽收眼底|一览无余|身不由己|百般滋味|难言之隐|不可言说'),
    ('emotion_adv',     r'(愤怒|悲伤|绝望|开心|高兴|激动|紧张|焦虑|恐惧|厌恶|惊讶|失望|无奈|平静|复杂)地'),
    ('causal_density',  r'因为|由于|为了|试图|想要'),
    ('nominal_v',       r'进行[了着中]|做出[了着]|完成[了着]'),
    ('gan_sense',       r'(宿命|破碎|少年|故事|氛围|松弛|距离|疏离|危险|压迫|孤独|荒凉|无力|撕裂|神秘|仪式)感'),
    ('paren_note',      r'（[^（）\n]{2,25}）'),
    ('voice_adj',       r'(声音|语气|嗓音|嗓|声线)(低沉|沙哑|沉稳|清冷|淡漠|冷峻|磁性|平静)'),
    ('gaze_v',          r'凝视|扫视|注视'),
]
SOFT_RE = [(cid, re.compile(p)) for cid, p in SOFT_GROUPS]

# ---- 模板类 pattern（处判级）----
PAT_PARALLEL = [
    (r'不是[^。！？\n"]{0,12}而是', '不是…而是'),
    (r'不仅[^。！？\n]{0,15}(?:而且|更是|还是|也)', '不仅…而且族'),
    (r'不只是[^。！？\n]{0,12}(?:还是|更是)', '不只是…还是'),
    (r'这不只是[^。！？\n]{0,12}更是', '这不只是…更是'),
    (r'既[^。！？\n]{0,10}又[^。！？\n]{0,10}(?!而)', '既…又'),
    (r'一方面[^。！？\n]{0,15}另一方面', '一方面…另一方面'),
]
PAT_HEART = r'心中一[紧沉痛酸暖震凛颤悸喜惊]|心里一[紧沉咯噔]'
PAT_EYE = r'眼中闪过|眼底闪过|瞳孔[微骤紧地]?[缩震]|眼神一[凝暗凛闪]|眼中划过'
PAT_FREEZE = r'(空气|气氛|时间|周围)(仿佛)?(在这一刻|瞬间)?(凝固|静止)|空气死寂'
PAT_TRIPLE = [r'有人[^。！？\n]{1,20}[，,]有人[^。！？\n]{1,20}[，,]有人',
              r'一切[^。！？\n]{1,8}的?都[^。！？\n]{1,8}[，,]一切[^。！？\n]{1,8}的?都',
              r'有的[^。！？\n]{1,20}[，,]有的[^。！？\n]{1,20}[，,]有的']
PAT_CLIFF = r'殊不知|谁也没想到|没有人(想到|料到)|无人知晓|而他不知道|他不知道的是|浑然不知|尚不知'
PAT_MENTAL = r'心想|暗想|想道|暗忖'
PAT_IDIOM_RUN = r'[\u4e00-\u9fff]{4}(?:[，、][\u4e00-\u9fff]{4}){2,}'
PAT_NAME_STYLE = (r'昱珩|司辰|暮白|凌夜|清辞|景渊|淮之|瑾舟|晚晚|若兮|清婉|云舟|'
                  r'星回|知遥|言澈|念初|芷晴|倾月|疏影|依依')
PAT_AI_META = (r'已思考|已深度思考|思考中|思考过程|用时\d+秒|嗯，用户|好的，用户|根据用户|'
               r'（\d+字）|\(\d+字\)|Response formatting|作为一个?AI|需要我帮|'
               r'以下是[^，。]{0,6}(分析|回答|介绍|总结|清单|章)|如果你想(即刻)?动笔|'
               r'本章节?[:：]|章节标题[:：]|希望这(段|章|篇)|祝(你|您)(阅读|愉快)')
PAT_CONN = (r'(?:^|[。！？\n])[ \t]*(与此同时|值得注意的是|值得一提的是|总而言之|综上所述|'
            r'众所周知|在当今|纵观|换言之|换句话说|总的来说|总得来说|让我们|不难发现|由此可见|'
            r'毫无疑问|不可否认|不言而喻|毋庸置疑|可以说|这说明)')
# 舞台指示（剧本式残留）
PAT_STAGE = (r'（(苦笑|轻笑|低笑|冷笑|叹气|叹息|沉默|摇头|点头|无奈|尴尬|疑惑|惊讶|'
             r'激动|思考|狡黠|玩味|赞许|了然|郑重|悠然|淡淡|平静|注|笑|叹)）')
# 场景标注行（结构标注残留；正文合法的【系统面板】不含这些词头）
PAT_BRACKET = (r'^\s*【(场景|旁白|内心独白|独白|画面|闪回|回忆|转场|'
               r'第[一二三四五六七八九十百\d]+[幕场])[^】]{0,20}】\s*$|'
               r'^\s*(时间|地点|人物|场景|背景)[:：]')
# 提纲式列举行（番茄"结构失常"治理项）
PAT_ENUM = r'^\s*[一二三四五六七八九十]{1,3}、|^\s*[（(][一二三四五六七八九十]{1,3}[)）]|^\s*\d+[\.、）)]'

MODAL_CHARS = '啊呀嘛呗哦嘿诶呐啦哟吧呢哈'
LOW_BAD = {'sent_cv', 'para_cv', 'ttr', 'tone_div', 'modal_part',
           'punct_cv', 'func_word', 'pron_density'}  # 值越低越危险
RANGE_OK = {'dialog_ratio': (0.05, 0.65)}
# 只报数不判级（人书八本×多位实测方差过大/风格依赖，FAIL 级会误伤人书：
# 顿号0-8.4、四字格连排0-27、5字重复0-17、语气词0-9.9、语气句0-0.47、
# 段长CV下探0.33、单引号内心独白惯例一章24处）
REPORT_ONLY = {'dunhao', 'idiom_runs', 'repeat_phrase', 'modal_part',
               'tone_div', 'para_cv', 'sq_quote'}


# ---------------- 零风险修复 ----------------

HTML_ENTITIES = {
    '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"',
    '&#39;': "'", '&mdash;': '——', '&ndash;': '—', '&hellip;': '……',
    '&ldquo;': '“', '&rdquo;': '”', '&lsquo;': '‘', '&rsquo;': '’', '&middot;': '·',
}


def fix_fullwidth_ascii(t):
    """全角英文字母数字转半角（ＡＢＣ１２３→ABC123），不碰全角标点。"""
    table = {}
    table.update({i: chr(i - 0xFEE0) for i in range(0xFF10, 0xFF1A)})  # ０-９
    table.update({i: chr(i - 0xFEE0) for i in range(0xFF21, 0xFF3B)})  # Ａ-Ｚ
    table.update({i: chr(i - 0xFEE0) for i in range(0xFF41, 0xFF5B)})  # ａ-ｚ
    return t.translate(table)


def _adj_sub(t, punct, repl):
    """英文标点两侧任一侧是中文（含中文标点）时转全角。"""
    pat = re.compile(r'(?<=[%s])%s|%s(?=[%s])' % (CJKX, re.escape(punct), re.escape(punct), CJKX))
    return pat.sub(repl, t)


def fix_zero_risk(text):
    """机械修复，不改任何语义。返回 (新文本, {修复名: 处数})。"""
    counts = {}
    t = text

    def bump(name, n):
        if n:
            counts[name] = counts.get(name, 0) + n

    # 0a. 隐形字符清理（AI输出/网页复制常见，肉眼不可见但平台检测器可见）
    new, n = re.subn(r'[\u200b\u200c\u200d\u2060\ufeff\u00ad]', '', t)
    bump('零宽字符清理', n)
    t = new
    new, n = re.subn('\u00a0', ' ', t)
    bump('不间断空格转普通', n)
    t = new

    # 0a-2. HTML实体解码（AI复制粘贴残留）
    ent_n = 0
    for k, v in HTML_ENTITIES.items():
        if k in t:
            ent_n += t.count(k)
            t = t.replace(k, v)
    bump('HTML实体解码', ent_n)

    # 0a-3. HTML标签剥离（<br>/<p>/<div>等）
    new, n = re.subn(r'</?(?:br|p|div|span|em|strong|b|i|section|article|h[1-6]|blockquote)[^>]*>', '', t)
    bump('HTML标签剥离', n)
    t = new

    # 0a-4. emoji清理（正文不该有emoji；保留★☆→等常用符号）
    new, n = re.subn(r'[\U0001F000-\U0001FAFF\u2600-\u2604\u2607-\u26FF\u2700-\u27BF'
                    r'\u2B50\u2B55\uFE0F]', '', t)
    bump('emoji清理', n)
    t = new

    # 0a-5. 生成器思考/响应残留行整行删除（精确模式，正常正文不可能出现）
    think_line = re.compile(r'^\s*(已思考.*|已深度思考.*|思考中.*|嗯，用户.*|好的，用户.*|'
                            r'（?\s*Response formatting.*|\d+\s*秒\s*)$')
    lines0 = t.split('\n')
    kept = [ln for ln in lines0 if not think_line.match(ln)]
    bump('思考残留行删除', len(lines0) - len(kept))
    t = '\n'.join(kept)

    # 0a-6. tab清理（正文\t一律为AI/排版残留）
    tab_n = t.count('\t')
    if tab_n:
        t = t.replace('\t', '')
    bump('tab清理', tab_n)

    # 0b. markdown残留清理（AI输出正文常带md符号；正文纯文本不应有）
    new, n = re.subn(r'\*\*|__|##|``', '', t)
    bump('markdown符号清理', n)
    t = new
    # markdown斜体（内容含中文）: *X* → X
    def _de_italic(m):
        return m.group(1) if re.search(r'[%s]' % CJK, m.group(1)) else m.group(0)
    new = re.sub(r'\*([^*\n]{1,60})\*', _de_italic, t)
    bump('markdown斜体清理', _diff_count(t, new))
    t = new
    # 删除线 ~~X~~ → X
    new, n = re.subn(r'~~([^~\n]{1,60})~~', r'\1', t)
    bump('markdown删除线清理', n)
    t = new
    lines = t.split('\n')
    md_list = sum(1 for ln in lines if re.match(r'^\s*[-*]\s+\S|^\s*\d+\.\s+\S', ln))
    if md_list:
        lines = [re.sub(r'^(\s*)([-*]\s+|\d+\.\s+)', r'\1', ln) for ln in lines]
        t = '\n'.join(lines)
    bump('markdown列表符清理', md_list)
    # markdown标题符（行首#+空格）与引用符（行首>）
    new, n1 = re.subn(r'^#{1,6}[ \t]+', '', t, flags=re.M)
    new, n2 = re.subn(r'^[ \t]*>[ \t]?', '', new, flags=re.M)
    bump('markdown标题引用符清理', n1 + n2)
    t = new

    # 0c. 破折号变体统一：单—、──、— —、—— —等 → 标准——
    new, n = re.subn(r'—(?:[ \t]?—)+|(?<!)—(?!—)', '——', t)
    n = sum(1 for a, b in zip(t, new) if a != b)
    bump('破折号变体统一', n)
    t = new

    # 0d. 重复标点压缩：，，、、、、；；；：：：→单个
    #     （连续中文句号"。。。"是网文省略号习惯写法，留给后面省略号归一规则；
    #       ？？！！！保留——网文情绪表达合法）
    new, n = re.subn(r'，{2,}|、{2,}|；{2,}|：{2,}',
                     lambda m: m.group(0)[0], t)
    bump('重复标点压缩', n)
    t = new

    # 0e. 相邻句读修正：，。→。 等
    swap = {'，。': '。', '、。': '。', '，、': '，', '、，': '、', '，；': '；', '；，': '；'}
    new, n = re.subn(r'，。|、。|，、|、，|，；|；，',
                     lambda m: swap.get(m.group(0), m.group(0)), t)
    bump('相邻句读修正', n)
    t = new

    # 0f. 行首缩进删除（网文txt惯例顶格）
    lines = t.split('\n')
    indent_n = sum(1 for ln in lines if re.match(r'^[ \t\u3000]+\S', ln))
    if indent_n:
        lines = [re.sub(r'^[ \t\u3000]+(?=\S)', '', ln) for ln in lines]
        t = '\n'.join(lines)
    bump('行首缩进删除', indent_n)

    # 0f-2. 行首标点上移（AI断行错误：逗号句号挂在段首，归位到上一行末尾）
    lines = t.split('\n')
    out_lines = []
    moved = 0
    for ln in lines:
        if out_lines and out_lines[-1].strip() and re.match(r'^[，。、；：]', ln):
            out_lines[-1] = out_lines[-1] + ln[0]
            ln = ln[1:]
            moved += 1
        out_lines.append(ln)
    if moved:
        t = '\n'.join(out_lines)
    bump('行首标点归位', moved)

    # 0g. 中文与数字之间空格删除（"第 3 章"→"第3章"，AI/翻译腔空格）
    new, n = re.subn(r'(?<=[%s])[ \t]+(?=\d)|(?<=\d)[ \t]+(?=[%s])' % (CJKX, CJKX), '', t)
    bump('中数间空格删除', n)
    t = new

    # 1. 全角字母数字 → 半角
    new = fix_fullwidth_ascii(t)
    bump('全角字母数字转半角', sum(1 for a, b in zip(t, new) if a != b))
    t = new

    # 2. 省略号归一：非双字符的…连续串 → 标准双字符……；'… …'→'……'
    def _norm_ellipsis(m):
        return '……' if len(m.group(0)) != 2 else m.group(0)
    new, n = re.subn(r'…+', _norm_ellipsis, t)
    n = sum(1 for a, b in zip(t, new) if a != b)
    bump('单省略号补双', n)
    t = new
    new, n = re.subn(r'…[ \t]+…', '……', t)
    bump('省略号间空格清理', n)
    t = new

    # 3. 半角点串（2个以上）中文邻接 → ……
    new, n = re.subn(r'(?<=[%s])\.{2,}|\.{2,}(?=[%s])' % (CJKX, CJKX), '……', t)
    bump('英文省略号转……', n)
    t = new

    # 4. 连续中文句号（打字式省略号 。。。）→ ……
    new, n = re.subn(r'。{2,}', '……', t)
    bump('连续句号转省略号', n)
    t = new

    # 5. 句读后紧跟句号（！。→！、……。→……）
    new, n1 = re.subn(r'([！？；：，、])。+', r'\1', t)
    new, n2 = re.subn(r'……。+', '……', new)
    bump('重复句读清理', n1 + n2)
    t = new

    # 6. 中文邻接的英文逗号/冒号/分号/问叹号 → 全角
    for punct, repl, name in ((',', '，', '英文逗号'), (':', '：', '英文冒号'),
                              (';', '；', '英文分号'), ('?', '？', '英文问号'),
                              ('!', '！', '英文叹号')):
        new = _adj_sub(t, punct, repl)
        bump(name, _diff_count(t, new))
        t = new

    # 7. 中文后的英文句点 → 。（避开小数/缩写/文件名）
    new, n = re.subn(r'(?<=[%s])\.(?![0-9A-Za-z])' % CJKX, '。', t)
    bump('英文句点转句号', n)
    t = new

    # 8. 括号中文邻接 → 全角
    new, n1 = re.subn(r'\((?=[%s])' % CJKX, '（', t)
    new, n2 = re.subn(r'(?<=[%s])\)' % CJKX, '）', new)
    bump('英文括号转全角', n1 + n2)
    t = new

    # 9. 中文后波浪号 → ～；英文双连字符中文邻接 → ——
    new, n = re.subn(r'(?<=[%s])~' % CJKX, '～', t)
    bump('半角波浪号转～', n)
    t = new
    new, n = re.subn(r'(?<=[%s])--|--(?=[%s])' % (CJKX, CJKX), '——', t)
    bump('双连字符转——', n)
    t = new

    # 10. 中文之间的空格只检测不修（"沈念 收"这类收件人/名单格式是有意空格，
    #     误删会改语义），由 check 层报告给 agent 判断

    # 11. 标点前的空格删除（中 ，→ 中，）
    new, n = re.subn(r'[ \t\u3000]+(?=[，。！？；：、”）])', '', t)
    bump('标点前空格清理', n)
    t = new

    # 11b. 引号内边缘空格（“ 你好 ”→“你好”）
    new, n1 = re.subn(r'“[ \t]+', '“', t)
    new, n2 = re.subn(r'[ \t]+”', '”', new)
    bump('引号内边缘空格清理', n1 + n2)
    t = new

    # 12. 行尾空白 + 3连以上空行压成1空行
    lines = t.split('\n')
    lines = [ln.rstrip(' \t\u3000') for ln in lines]
    bump('行尾空白清理', sum(1 for a, b in zip(t.split('\n'), lines) if a != b))
    t = '\n'.join(lines)
    new, n = re.subn(r'\n{3,}', '\n\n', t)
    bump('多余空行压缩', n)
    t = new

    # 13. 英文双引号配对 → 中文引号（逐行状态机；网文引号不跨行）
    fixed_lines = []
    pair_count = 0
    for ln in t.split('\n'):
        out = []
        inside = False
        for ch in ln:
            if ch == '"':
                out.append('“' if not inside else '”')
                inside = not inside
                pair_count += 1
            else:
                if ch == '“':
                    inside = True
                elif ch == '”':
                    inside = False
                out.append(ch)
        fixed_lines.append(''.join(out))
    t = '\n'.join(fixed_lines)
    bump('英文引号转中文引号', pair_count)

    # 14. 英文单引号：中文邻接且非英文单词内部 → ‘’（逐行配对）
    fixed_lines = []
    sq_count = 0
    for ln in t.split('\n'):
        out = []
        inside = False
        for i, ch in enumerate(ln):
            if ch == "'":
                prev = ln[i - 1] if i > 0 else ''
                nxt = ln[i + 1] if i + 1 < len(ln) else ''
                cjk_adj = _is_cjkx(prev) or _is_cjkx(nxt)
                word_inner = prev.isascii() and prev.isalnum() and nxt.isascii() and nxt.isalnum()
                if cjk_adj and not word_inner:
                    out.append('‘' if not inside else '’')
                    inside = not inside
                    sq_count += 1
                    continue
            out.append(ch)
        fixed_lines.append(''.join(out))
    t = '\n'.join(fixed_lines)
    bump('英文单引号转中文引号', sq_count)

    # 14b. 独立单引号对→双引号（NGA读者鉴AI实锤法：人手打几乎不用''；
    #      仅转双引号外的，对话内嵌套引用的''合法保留）
    sq_lines = []
    sq_fix = 0
    for ln in t.split('\n'):
        if '‘' not in ln and '’' not in ln:
            sq_lines.append(ln)
            continue
        in_dq = False
        buf = []
        for ch in ln:
            if ch == '“':
                in_dq = True
            elif ch == '”':
                in_dq = False
            if not in_dq:
                if ch == '‘':
                    buf.append('“')
                    sq_fix += 1
                    continue
                if ch == '’':
                    buf.append('”')
                    sq_fix += 1
                    continue
            buf.append(ch)
        sq_lines.append(''.join(buf))
    t = '\n'.join(sq_lines)
    bump('独立单引号转双引号', sq_fix)

    # 15. 连续ASCII空格压缩（2+→1；中文间空格已在check层报告）
    new, n = re.subn(r' {2,}', ' ', t)
    bump('连续空格压缩', n)
    t = new

    return t, counts


def _is_cjkx(ch):
    return bool(ch) and re.match(r'^[%s]$' % CJKX, ch)


def _diff_count(old, new):
    return sum(1 for a, b in zip(old, new) if a != b)


# ---------------- 滥用检测 ----------------

def check_abuse(text):
    """在（已修复的）文本上跑滥用检测。返回 (结果dict, 正文字数)。"""
    lines = text.split('\n')
    body = ''.join(ln for ln in lines if ln.strip())
    n = max(len(body), 1)
    results = {}

    def verdict(cid, value):
        for c in CHECKS:
            if c[0] == cid:
                if cid in REPORT_ONLY:
                    return 'PASS'
                if cid in RANGE_OK:
                    lo, hi = RANGE_OK[cid]
                    return 'PASS' if lo <= value <= hi else 'WARN'
                if cid in LOW_BAD:
                    if value <= c[3]:
                        return 'FAIL'
                    if value <= c[2]:
                        return 'WARN'
                    return 'PASS'
                if value >= c[3]:
                    return 'FAIL'
                if value > c[2]:
                    return 'WARN'
                return 'PASS'

    def scan_lines(pat_list):
        """逐行扫描多个pattern，返回命中list[{line,snippet,match}]。"""
        hits = []
        for i, ln in enumerate(lines, 1):
            for pat in pat_list:
                for m in pat.finditer(ln) if hasattr(pat, 'finditer') else re.finditer(pat, ln):
                    ctx = ln[max(0, m.start() - 6):min(len(ln), m.end() + 6)]
                    hits.append({'line': i, 'snippet': ctx, 'match': m.group(0)})
        return hits

    def put(cid, value, hits, cap=8):
        results[cid] = {
            'value': value, 'verdict': verdict(cid, value),
            'hits': [{'line': h['line'], 'snippet': h['snippet'][:42]} for h in hits[:cap]],
            'total_hits': len(hits)}

    def put_density(cid, hits):
        d = round(len(hits) / n * 1000, 1)
        put(cid, d, hits)

    # --- 密度类 ---
    pd = round(text.count('。') / n * 1000, 1)
    results['period_density'] = {'value': pd, 'verdict': verdict('period_density', pd), 'hits': []}
    ed = round(text.count('……') / n * 1000, 1)
    results['ellipsis_density'] = {'value': ed, 'verdict': verdict('ellipsis_density', ed), 'hits': []}
    put_density('cliche_hits', scan_lines(CLICHE_RE))
    for cid, pat in SOFT_RE:
        put_density(cid, scan_lines([pat]))

    # --- 模板类 ---
    par_hits = []
    for i, ln in enumerate(lines, 1):
        for pat, name in PAT_PARALLEL:
            for m in re.finditer(pat, ln):
                par_hits.append({'line': i, 'snippet': m.group(0)})
    put('parallel', len(par_hits), par_hits)

    for cid, pat in (('heart_pat', PAT_HEART), ('eye_pat', PAT_EYE),
                     ('freeze_pat', PAT_FREEZE), ('cliff_tmpl', PAT_CLIFF),
                     ('mental_direct', PAT_MENTAL)):
        hits = scan_lines([pat])
        put(cid, len(hits), hits)

    triple_hits = []
    for i, ln in enumerate(lines, 1):
        for pat in PAT_TRIPLE:
            for m in re.finditer(pat, ln):
                triple_hits.append({'line': i, 'snippet': m.group(0)[:42]})
    put('triple_pat', len(triple_hits), triple_hits)

    # 四字格连排（三个以上四字短语以逗号/顿号连排）
    idiom_hits = []
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(PAT_IDIOM_RUN, ln):
            idiom_hits.append({'line': i, 'snippet': m.group(0)[:42]})
    put('idiom_runs', len(idiom_hits), idiom_hits)

    # 长短语重复（同一5字片段出现≥3次）
    han = ''.join(re.findall(r'[%s]' % CJK, body))
    rep_hits = []
    if len(han) >= 300:
        g5 = Counter(han[i:i + 5] for i in range(len(han) - 4))
        for g, c in g5.items():
            if c >= 3:
                rep_hits.append({'line': 0, 'snippet': '%s ×%d' % (g, c)})
        rep_hits.sort(key=lambda h: -int(h['snippet'].split('×')[1]))
    put('repeat_phrase', len(rep_hits), rep_hits, cap=6)

    # 碎句连段 / 句长均匀连3
    frag_hits, even_hits = [], []
    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            continue
        sents = []
        for s in re.split(r'[。！？…]', ln):
            s2 = s.strip().strip('“”‘’「」')
            if s2:
                sents.append(s2)
        if len(sents) < 3:
            continue
        for j in range(len(sents) - 2):
            if all(0 < len(sents[k]) <= 8 for k in (j, j + 1, j + 2)):
                frag_hits.append({'line': i, 'snippet': '／'.join(sents[j:j + 3])})
                break
        run = 0
        for s in sents:
            if 15 <= len(s) <= 25:
                run += 1
                if run >= 3:
                    even_hits.append({'line': i, 'snippet': s[:20] + '…'})
                    break
            else:
                run = 0
    put('frag_runs', len(frag_hits), frag_hits)
    put('even_runs', len(even_hits), even_hits)

    # 段首重复（连续≥3段同词开头）
    para_start_hits = []
    paras = [(i, ln) for i, ln in enumerate(lines, 1) if ln.strip()]
    run = 1
    for k in range(1, len(paras)):
        prev_head = paras[k - 1][1][:2]
        cur_head = paras[k][1][:2]
        if prev_head == cur_head and re.match(r'^[%s]{1,2}' % CJK, cur_head):
            run += 1
            if run >= 3:
                para_start_hits.append({'line': paras[k][0], 'snippet': '段首×%d「%s…」' % (run, cur_head)})
        else:
            run = 1
    put('para_start_rep', len(para_start_hits), para_start_hits)

    # 主语连缀（段内连续≥3句以同一代词开头）
    subj_hits = []
    for i, ln in enumerate(lines, 1):
        if not ln.strip() or len(ln) < 30:
            continue
        sents = [s for s in re.split(r'[。！？…]', ln) if s.strip()]
        run = 1
        for k in range(1, len(sents)):
            head = sents[k].strip()[:1]
            prev = sents[k - 1].strip()[:1]
            if head == prev and head in '他她它我你':
                run += 1
                if run >= 3:
                    subj_hits.append({'line': i, 'snippet': '「%s」字头连×%d' % (head, run)})
                    run = 1
            else:
                run = 1
    put('subj_rep', len(subj_hits), subj_hits)

    # 超长段（单段≥180字）
    wall_hits = [{'line': i, 'snippet': '段落%d字：%s…' % (len(ln), ln[:30])}
                 for i, ln in enumerate(lines, 1) if len(ln) >= 180]
    put('para_wall', len(wall_hits), wall_hits)

    # 开篇环境堆砌（前2段无对话+写景+形容词密集）
    env_hits = []
    if paras:
        head2 = ''.join(p[1] for p in paras[:2])
        head1 = paras[0][1]
        has_dialog = '“' in head2 or '”' in head2
        env_words = len(re.findall(r'光|风|雨|夜|晨|阳|月|雾|云|街|窗|空气|天色|暮', head1))
        if not has_dialog and len(head2) >= 60 and head1.count('的') >= 3 and env_words >= 2:
            env_hits.append({'line': 1, 'snippet': head1[:42]})
    put('env_open', len(env_hits), env_hits)

    # AI人名风
    put('name_style', len(scan_lines([re.compile(PAT_NAME_STYLE)])),
        scan_lines([re.compile(PAT_NAME_STYLE)]))

    # --- 统计类 ---
    dash_hits = []
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'.{0,12}——.{0,12}', ln):
            dash_hits.append({'line': i, 'snippet': m.group(0).strip()})
    dd = round(text.count('——') / n * 500, 2)
    results['dash_density'] = {'value': dd, 'verdict': verdict('dash_density', dd),
                               'hits': dash_hits[:8], 'total_hits': len(dash_hits)}

    # 句长变异系数（burstiness反向：低=AI）
    all_sents = []
    sent_texts = []
    for ln in lines:
        if not ln.strip():
            continue
        for s in re.split(r'[。！？…]', ln):
            s2 = s.strip().strip('“”‘’')
            if s2:
                all_sents.append(len(s2))
                sent_texts.append(s2)
    if len(all_sents) >= 10:
        mean = sum(all_sents) / len(all_sents)
        var = sum((x - mean) ** 2 for x in all_sents) / len(all_sents)
        scv = round((var ** 0.5) / mean, 2) if mean else 1.0
    else:
        scv = 1.0
    results['sent_cv'] = {'value': scv, 'verdict': verdict('sent_cv', scv), 'hits': []}

    # 顺滑句对占比（语义平滑度代理：相邻句二字组Jaccard≥0.25的句对占比；高=AI过顺滑）
    if len(sent_texts) >= 6:
        smooth_pairs = 0
        total_pairs = 0
        for a, b in zip(sent_texts, sent_texts[1:]):
            sa = set(a[i:i + 2] for i in range(len(a) - 1))
            sb = set(b[i:i + 2] for i in range(len(b) - 1))
            union = len(sa | sb)
            if union:
                total_pairs += 1
                if len(sa & sb) / union >= 0.25:
                    smooth_pairs += 1
        sem = round(smooth_pairs / total_pairs, 2) if total_pairs else 0.0
    else:
        sem = 0.0
    results['sem_smooth'] = {'value': sem, 'verdict': verdict('sem_smooth', sem), 'hits': []}

    # 段落长度变异系数（低=AI）
    para_lens = [len(ln) for ln in lines if ln.strip()]
    if len(para_lens) >= 10:
        mean = sum(para_lens) / len(para_lens)
        var = sum((x - mean) ** 2 for x in para_lens) / len(para_lens)
        pcv = round((var ** 0.5) / mean, 2) if mean else 1.0
    else:
        pcv = 1.0
    results['para_cv'] = {'value': pcv, 'verdict': verdict('para_cv', pcv), 'hits': []}

    # 对话比例（引号内字符占比；区间型，仅WARN）
    in_quote = 0
    for ln in lines:
        open_q = False
        for ch in ln:
            if ch == '“':
                open_q = True
            elif ch == '”':
                open_q = False
            elif open_q:
                in_quote += 1
    dr = round(in_quote / n, 2)
    results['dialog_ratio'] = {'value': dr, 'verdict': verdict('dialog_ratio', dr), 'hits': []}

    # 四字片段重复率（字符4-gram重复占比；机械重复感）
    if len(han) >= 200:
        grams = [han[i:i + 4] for i in range(len(han) - 3)]
        gc = Counter(grams)
        rep = sum(v for v in gc.values() if v > 1)
        ngram = round(rep / len(grams), 3)
    else:
        ngram = 0.0
    results['ngram_rep'] = {'value': ngram, 'verdict': verdict('ngram_rep', ngram), 'hits': []}

    # 二字组多样性（TTR；低=AI翻来覆去）
    if len(han) >= 200:
        g2 = [han[i:i + 2] for i in range(len(han) - 1)]
        ttr = round(len(set(g2)) / len(g2), 3)
    else:
        ttr = 1.0
    results['ttr'] = {'value': ttr, 'verdict': verdict('ttr', ttr), 'hits': []}

    # 语气句比例（？！句占比；低=AI平板）
    n_sents = len(all_sents)
    tone = sum(1 for ln in lines if ln.strip() for _ in re.findall(r'[！？]', ln))
    tdiv = round(tone / n_sents, 2) if n_sents else 0.0
    results['tone_div'] = {'value': tdiv, 'verdict': verdict('tone_div', tdiv), 'hits': []}

    # 语气词密度（低=AI对白无口气）
    mp = round(sum(body.count(c) for c in MODAL_CHARS) / n * 1000, 1)
    results['modal_part'] = {'value': mp, 'verdict': verdict('modal_part', mp), 'hits': []}

    # --- v2.1 新增统计 ---
    # 顿号密度（AI不用顿号——NGA标点规范法反向特征，低=AI）
    dh = round(text.count('、') / n * 1000, 1)
    results['dunhao'] = {'value': dh, 'verdict': verdict('dunhao', dh), 'hits': []}

    # 的着了气口密度（NGA气口理论：AI少用虚词气口，低=AI）
    fw = round((text.count('的') + text.count('着') + text.count('了')) / n * 1000, 1)
    results['func_word'] = {'value': fw, 'verdict': verdict('func_word', fw), 'hits': []}

    # 代词气口密度（这/那族，AI少指代）
    prn = len(re.findall(r'这|那', body))
    prd = round(prn / n * 1000, 1)
    results['pron_density'] = {'value': prd, 'verdict': verdict('pron_density', prd), 'hits': []}

    # 句首"而"字密度（AI高频句式起手）
    er_n = 0
    for ln in lines:
        if not ln.strip():
            continue
        for s in re.split(r'[。！？…]', ln):
            s2 = s.strip().strip('“”‘’「」')
            if s2.startswith('而'):
                er_n += 1
    erd = round(er_n / n * 1000, 1)
    results['er_start'] = {'value': erd, 'verdict': verdict('er_start', erd), 'hits': []}

    # 3-gram重复率（平台检测最重权重维度之一）
    if len(han) >= 200:
        g3 = [han[i:i + 3] for i in range(len(han) - 2)]
        g3c = Counter(g3)
        rep3 = sum(v for v in g3c.values() if v > 1)
        ng3 = round(rep3 / len(g3), 3)
    else:
        ng3 = 0.0
    results['ngram3_rep'] = {'value': ng3, 'verdict': verdict('ngram3_rep', ng3), 'hits': []}

    # 标点节奏变异系数（火山引擎：标点间隔CV，自然约0.45，AI过均匀）
    gaps = []
    cur = 0
    for ch in body:
        if ch in '，。！？；：、…':
            gaps.append(cur + 1)
            cur = 0
        else:
            cur += 1
    if len(gaps) >= 15:
        gmean = sum(gaps) / len(gaps)
        gvar = sum((x - gmean) ** 2 for x in gaps) / len(gaps)
        pcv2 = round((gvar ** 0.5) / gmean, 2) if gmean else 1.0
    else:
        pcv2 = 1.0
    results['punct_cv'] = {'value': pcv2, 'verdict': verdict('punct_cv', pcv2), 'hits': []}

    # 超短段连击（连续3段≤6字的非对白短段）
    punch_hits = []
    run = 0
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s and len(s) <= 6 and '“' not in s:
            run += 1
            if run >= 3:
                punch_hits.append({'line': i - 2, 'snippet': 'L%d起×%d连短段' % (i - 2, run)})
                run = 0
        else:
            run = 0
    put('punch_para', len(punch_hits), punch_hits)

    # 无对话长流（连续≥8段无对白）
    env_hits = []
    run = 0
    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            continue
        if '“' in ln or '”' in ln:
            run = 0
        else:
            run += 1
            if run == 8:
                env_hits.append({'line': i - 7, 'snippet': 'L%d起连续8段+无对白' % (i - 7)})
    put('env_run', len(env_hits), env_hits)

    # --- 其他 ---
    conn_hits = []
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(PAT_CONN, ln):
            ctx = ln[max(0, m.start()):m.end() + 15].strip()
            conn_hits.append({'line': i, 'snippet': ctx})
    put('connectives', len(conn_hits), conn_hits)

    space_hits = []
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'(?<=[%s])[ \t\u3000]+(?=[%s])' % (CJKX, CJKX), ln):
            ctx = ln[max(0, m.start() - 5):m.end() + 5]
            space_hits.append({'line': i, 'snippet': ctx})
    put('cjk_space', len(space_hits), space_hits)

    q_hits = []
    for i, ln in enumerate(lines, 1):
        if ln.count('"') % 2:
            q_hits.append({'line': i, 'snippet': ln[:30]})
        if ln.count('“') != ln.count('”'):
            q_hits.append({'line': i, 'snippet': ln[:30]})
    put('quote_unpaired', len(q_hits), q_hits)

    sq = text.count('‘') + text.count('’')
    results['sq_quote'] = {'value': sq, 'verdict': verdict('sq_quote', sq), 'hits': []}

    meta_hits = scan_lines([re.compile(PAT_AI_META)])
    put('ai_meta', len(meta_hits), meta_hits)

    # v2.1 工具痕迹扩展
    stage_hits = scan_lines([re.compile(PAT_STAGE)])
    put('stage_dir', len(stage_hits), stage_hits)

    bracket_hits = [{'line': i, 'snippet': ln.strip()[:36]}
                    for i, ln in enumerate(lines, 1)
                    if ln.strip() and re.match(PAT_BRACKET, ln)]
    put('bracket_label', len(bracket_hits), bracket_hits)

    enum_hits = [{'line': i, 'snippet': ln.strip()[:36]}
                 for i, ln in enumerate(lines, 1)
                 if ln.strip() and re.match(PAT_ENUM, ln)]
    put('enum_list', len(enum_hits), enum_hits)

    emo = len(re.findall(r'[\U0001F000-\U0001FAFF\u2600-\u2604\u2607-\u26FF\u2700-\u27BF\u2B50\u2B55\uFE0F]', text))
    results['emoji_res'] = {'value': emo, 'verdict': verdict('emoji_res', emo), 'hits': []}

    en_hits = [{'line': i, 'snippet': ln.strip()[:40]}
               for i, ln in enumerate(lines, 1)
               if ln.strip() and not re.search(r'[%s]' % CJK, ln)
               and re.search(r'[A-Za-z]{3,}[\s,.;:!?\'\"]+[A-Za-z]{3,}', ln)]
    put('en_line', len(en_hits), en_hits)

    return results, n


# ---------------- 报告 ----------------

def render_report(path, n_chars, fixes, checks, json_out=False, do_fix=False):
    check_map = {c[0]: c for c in CHECKS}
    if json_out:
        payload = {
            'file': path,
            'chars': n_chars,
            'fixes': fixes,
            'checks': [],
        }
        for cid, c in check_map.items():
            r = checks.get(cid, {})
            payload['checks'].append({
                'id': cid, 'name': c[1], 'value': r.get('value'), 'unit': c[4],
                'verdict': r.get('verdict'), 'threshold': {'warn': c[2], 'fail': c[3]},
                'advice': c[5],
                'hits': r.get('hits', []),
            })
        payload['need_agent_fix'] = [c['id'] for c in payload['checks'] if c['verdict'] in ('WARN', 'FAIL')]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    icons = {'PASS': '[PASS]', 'WARN': '[警告]', 'FAIL': '[必改]'}
    lines = []
    lines.append('=' * 56)
    lines.append('正文去AI味门禁  %s  (%d字)' % (os.path.basename(path), n_chars))
    lines.append('=' * 56)
    if fixes:
        lines.append('—— 零风险自动修复（已执行）——')
        for name, cnt in sorted(fixes.items(), key=lambda x: -x[1]):
            lines.append('  %-14s %d 处' % (name, cnt))
    elif do_fix:
        lines.append('—— 零风险自动修复：已执行，本次无可修复项 ——')
    else:
        lines.append('—— 零风险自动修复：未执行（加 --fix 启用）——')
    lines.append('')
    lines.append('—— 滥用检测（定位如下，自查自修）——')
    for cid, c in check_map.items():
        r = checks.get(cid, {})
        v = r.get('value', 0)
        if cid in REPORT_ONLY:
            lines.append('  [报告] %-8s %s%s（仅报告，人书方差大不判级）' % (c[1], v, c[4]))
        else:
            lines.append('  %s %-8s %s%s（警告线%s / 必改线%s）' % (
                icons.get(r.get('verdict'), '[?]?'), c[1], v, c[4], c[2], c[3]))
        if r.get('verdict') in ('WARN', 'FAIL'):
            for h in r.get('hits', []):
                lines.append('      L%-4d %s' % (h['line'], h['snippet'][:42]))
            th = r.get('total_hits', len(r.get('hits', [])))
            if th > len(r.get('hits', [])):
                lines.append('      …另有 %d 处' % (th - len(r.get('hits', []))))
    warns = sum(1 for r in checks.values() if r.get('verdict') == 'WARN')
    fails = sum(1 for r in checks.values() if r.get('verdict') == 'FAIL')
    lines.append('')
    if fails or warns:
        lines.append('结论: %d项必改 / %d项警告 —— 按上行定位自查自修，修后复跑' % (fails, warns))
    else:
        lines.append('结论: 全部通过')
    return '\n'.join(lines)


def process_file(path, do_fix, json_out):
    raw = open(path, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        text, eol = raw.decode('utf-8-sig'), ('\r\n' if b'\r\n' in raw else '\n')
    else:
        try:
            text, eol = raw.decode('utf-8'), ('\r\n' if b'\r\n' in raw else '\n')
        except UnicodeDecodeError:
            text, eol = raw.decode('gb18030'), ('\r\n' if b'\r\n' in raw else '\n')
    text = text.replace('\r\n', '\n')

    if do_fix:
        fixed, fixes = fix_zero_risk(text)
    else:
        fixed, fixes = text, {}
    checks, n_chars = check_abuse(fixed)

    if do_fix and fixed != text:
        out = fixed.replace('\n', eol)
        open(path, 'wb').write(out.encode('utf-8'))
    report = render_report(path, n_chars, fixes, checks, json_out, do_fix)
    has_issue = any(r.get('verdict') in ('WARN', 'FAIL') for r in checks.values())
    return report, has_issue


def main():
    ap = argparse.ArgumentParser(description='正文去AI味门禁 v2.1：零风险自动修 + 滥用检测')
    ap.add_argument('input', help='正文文件或目录（目录批处理*.txt，不递归）')
    ap.add_argument('--fix', action='store_true', help='执行零风险自动修复（原地写回）')
    ap.add_argument('--json', action='store_true', help='JSON 输出')
    args = ap.parse_args()

    if os.path.isdir(args.input):
        files = sorted(glob.glob(os.path.join(args.input, '*.txt')))
    elif os.path.isfile(args.input):
        files = [args.input]
    else:
        print('错误: 找不到 %s' % args.input, file=sys.stderr)
        sys.exit(2)
    if not files:
        print('错误: 目录下没有 .txt 文件', file=sys.stderr)
        sys.exit(2)

    any_issue = False
    for f in files:
        report, issue = process_file(f, args.fix, args.json)
        print(report)
        any_issue = any_issue or issue
    sys.exit(1 if any_issue else 0)


if __name__ == '__main__':
    main()
