#!/usr/bin/env python3
"""
Beacons 关键词分类分析脚本
表头结构：关键词 | 搜索量 | 流量 | 更改 | 付费 | 位置 | 更改 | 位置 | 更改 | 顶部位置 | 搜索量 | 流量
"""

import re

# 全部 300 个关键词
keywords = [
    "beacons", "foothubhd", "beacons ai", "pokerseri", "jakipz", "barcaslot",
    "beacons.ai", "mvptogel", "download hub", "panentogel", "mulan togel",
    "elly clutch", "kepritogel link alternatif", "waifutania", "owltoto",
    "pamsnusnu", "megbanksxo onlyfans", "kepri togel", "chimden", "foothub",
    "lilijunex", "ayleks onlyfans", "berigalaxy", "instafest app",
    "how old is salish matter", "pornhub login", "norissa valdez", "lilecchigirl",
    "compass dollar tree", "cri3x", "kepritogel login link alternatif terbaru",
    "mvp togel", "kepritogel boskepri", "tatum bittick", "sayumi sutra",
    "whipitdev", "humas togel", "xxtattedbaddiexx", "cnfans spreadsheet",
    "banditjitu login", "xclass vn", "mary hạ lục", "kayla kapoor",
    "creamy spot", "crimsonkitten", "what is beacons.ai", "kepritogel login",
    "bandit jitu", "instagram bio punjabi", "aria banks", "spicycowgirl4498",
    "andrea botez", "hayami haru", "yololary onlyfans", "rgototo",
    "after long time meet caption", "lilith regia", "xnhau", "saba toto",
    "mahadev bio for instagram", "stella sedona", "dark aesthetic bio instagram",
    "pinky powers", "beacon", "dollar tree compass employee portal",
    "alibaba66 slot", "agung4d", "saramart links", "liquidcandy2000",
    "wulan togel", "nicsofiadiaz", "lara lane onlyfans", "zoweybunny",
    "lilmermaidxx", "silvia soprano", "samantra onlyfans", "iamhely",
    "humastogel login", "darcie does it", "msodile", "islot99 login",
    "dollar tree compass login", "runningprincess", "go shuttle",
    "drew gulliver onlyfans", "motivational bio for instagram", "sinden4d",
    "asianamethyst710", "kepritogel login link alternatif", "samantra official",
    "what is beacons", "mulaniscreamy", "kepritogel link alternatif terbaru",
    "pepperflavor", "abby berner", "bulan togel", "what is beacons ai",
    "lunaqueeeen", "blondiekayy", "saren robles", "kepri togel login",
    "beacon ai", "monisuea", "mikkistorm", "sorabuni", "lela sohna",
    "brownandsweet", "mulantogel", "sheeya onlyfans", "inked dory",
    "sophie aspin onlyfans", "becons", "dhgate spreadsheet", "sayumisutra",
    "meido moon", "sophidelyon", "sabatoto login", "shockify", "flirtygem",
    "mpvtogel", "okichloeo", "maggielovieee", "jostasy", "kira pregiato",
    "mila ricci nude", "butterybubblebutt", "gwy_ther", "allie lynn onlyfans",
    "clxragrace", "amelie warren", "thezayanna", "khloe knowles", "vixen11111",
    "lelasohna", "astarbabyxo", "ashley conejo", "znhau",
    "bulantogel login alternatif login", "beaconsai", "punjabi bio",
    "xclass", "carbonara madalenas", "after long time meet friends quotes",
    "pamnusnu", "bulan togel login", "xdsells", "vox888", "naiades aqua",
    "ariaonlyxo onlyfans", "nacrevictoire", "yasmin pariz",
    "bio for instagram mahadev", "heavann77 onlyfans", "punjabi bio for instagram",
    "after long time meet my friend quotes", "beacons login", "mistress enola",
    "neyrodesu", "nunadrama info", "mahadev bio", "waifumia", "ashleysoft",
    "tattedmamii", "alanah cole", "starfucked", "lord shiva bio for instagram",
    "luxlo onlyfans", "cristiana love", "c", "ơ", "m tấm mộc",
    "mvp togel login", "pockycats leaks", "devils.goddess", "photo credit caption",
    "togel seratus", "samantra of leaks", "panentogel login", "sallydinosaur",
    "when you meet your friend after a long time caption", "downlodhub",
    "pinky_powers", "frontlines media", "daily lotto prediction for today",
    "billie eilish onlyfans", "crislainechan", "mayuriix_x", "yogabella",
    "jellybellylillian", "chloe foxxe", "wettmelons", "sattamatkaji",
    "sweetiesuun", "kiwi sunset", "latoslot", "chilli thái",
    "sanskrit bio for instagram for girl", "kepritogel slot",
    "after long time meet my friend captions for instagram", "torayx",
    "jakeandrich", "stormiiy", "whipitdev onlyfans", "samantra",
    "alexa breit of", "latoxicasz", "mari avila telegram", "hiso168",
    "rotas beach", "xvampdoll", "emmaspice", "self obsessed captions for instagram",
    "money captions for instagram", "badassnugget", "badbaby187",
    "short motivational bio for instagram", "kendallbabe", "brecanyon",
    "blackgurlkitty", "blackwidof", "compassmobile dollartree com",
    "margopov nude", "c_thicc", "aviva sofia", "adelynmoore",
    "mvptogel login", "xstripx.com", "studygram", "bigb00tygodess",
    "comeoncamille", "sanskrit bio for instagram", "motivation bio for instagram",
    "bio for instagram hindu", "law student bio for instagram",
    "how old is salish matter in 2025", "howie the crab", "kamxalta",
    "jadierosaa", "ollyhibs", "flashx24", "lean beef patty age",
    "xclassvn sex", "khloe knowles onlyfans", "michelleerabbit onlyfans",
    "clarus polaris", "lylasbigheart", "gabyy_yt xxx", "sindal xie",
    "kathiesanderss", "unexpected friendship quotes", "xbhau",
    "marta gromova", "dabofhalo", "jadehascake", "aria adams onlyfans",
    "swimangieswim", "jill_bunny", "beacon.ai", "instagram bio mahadev",
    "madelinexx", "sharon piel morena", "motivation bio",
    "sanskrit shlok for instagram bio", "compass mobile dollar tree login",
    "marleyywynn", "quick escape caption", "11 months old baby caption",
    "eva violet", "val2yummi", "best punjabi quotes for instagram bio",
    "jade pixel", "islamic bio for instagram urdu", "hut4d login",
    "mulan togel.com", "gabscolleta", "1 month old baby caption",
    "drew gulliver", "oopbuy spreadsheet", "howtofaithalife",
    "instagram bio for hindu girl", "nicki minaj onlyfans", "kenalialuv",
    "jaat bio for instagram"
]

# 定义分类规则
def classify_keywords(keywords):
    categories = {
        "品牌词类": [],
        "人物/网红 - OnlyFans/成人创作者": [],
        "人物/网红 - 常规创作者": [],
        "博彩类 - 印尼": [],
        "Instagram Bio 类": [],
        "Instagram Caption 类": [],
        "工具/功能类": [],
        "其他类": []
    }
    
    for kw in keywords:
        kw_lower = kw.lower()
        
        # 1. 品牌词类
        if any(x in kw_lower for x in ['beacons', 'beacon', 'becons', 'beaconsai']):
            categories["品牌词类"].append(kw)
        # 2. OnlyFans/成人创作者
        elif 'onlyfans' in kw_lower or kw in [
            "elly clutch", "lilijunex", "pamsnusnu", "berigalaxy", "ayleks onlyfans",
            "megbanksxo onlyfans", "waifutania", "tatum bittick", "sayumi sutra",
            "whipitdev", "xxtattedbaddiexx", "creamy spot", "norissa valdez",
            "lilecchigirl", "crimsonkitten", "aria banks", "yololary onlyfans",
            "lara lane onlyfans", "zoweybunny", "lilmermaidxx", "silvia soprano",
            "samantra onlyfans", "drew gulliver onlyfans", "spicycowgirl4498",
            "iamhely", "darcie does it", "samantra official", "abby berner",
            "lunaqueeeen", "blondiekayy", "lela sohna", "brownandsweet",
            "sheeya onlyfans", "sophie aspin onlyfans", "inked dory", "sayumisutra",
            "meido moon", "sophidelyon", "flirtygem", "maggielovieee", "jostasy",
            "kira pregiato", "mila ricci nude", "butterybubblebutt", "gwy_ther",
            "allie lynn onlyfans", "clxragrace", "amelie warren", "thezayanna",
            "khloe knowles", "vixen11111", "lelasohna", "astarbabyxo", "pamnusnu",
            "ariaonlyxo onlyfans", "heavann77 onlyfans", "yasmin pariz",
            "mistress enola", "neyrodesu", "waifumia", "ashleysoft", "tattedmamii",
            "alanah cole", "starfucked", "luxlo onlyfans", "cristiana love",
            "devils.goddess", "pockycats leaks", "sallydinosaur", "stormiiy",
            "whipitdev onlyfans", "alexa breit of", "latoxicasz", "mari avila telegram",
            "rotas beach", "xvampdoll", "emmaspice", "kendallbabe", "brecanyon",
            "blackgurlkitty", "blackwidof", "margopov nude", "c_thicc", "aviva sofia",
            "adelynmoore", "bigb00tygodess", "comeoncamille", "nicki minaj onlyfans",
            "michelleerabbit onlyfans", "lylasbigheart", "gabyy_yt xxx", "sindal xie",
            "kathiesanderss", "xbhau", "marta gromova", "dabofhalo", "jadehascake",
            "aria adams onlyfans", "swimangieswim", "jill_bunny", "madelinexx",
            "sharon piel morena", "eva violet", "val2yummi", "jade pixel",
            "drew gulliver", "howtofaithalife", "kenalialuv"
        ]:
            categories["人物/网红 - OnlyFans/成人创作者"].append(kw)
        # 3. 常规网红
        elif kw in [
            "jakipz", "chimden", "andrea botez", "hayami haru", "stella sedona",
            "monisuea", "mikkistorm", "sorabuni", "okichloeo", "ashley conejo",
            "nacrevictoire", "nunadrama info", "jakeandrich", "samantra",
            "hiso168", "crislainechan", "mayuriix_x", "yogabella",
            "jellybellylillian", "chloe foxxe", "wettmelons", "kiwi sunset",
            "torayx", "badassnugget", "badbaby187", "howie the crab", "kamxalta",
            "jadierosaa", "ollyhibs", "flashx24", "lean beef patty age",
            "clarus polaris", "chilli thái"
        ] or "instagram" not in kw_lower and "bio" not in kw_lower and "caption" not in kw_lower:
            # 检查是否是博彩词
            if any(x in kw_lower for x in ['togel', 'slot', 'toto', 'login', 'bandit', '4d']):
                categories["博彩类 - 印尼"].append(kw)
            else:
                categories["人物/网红 - 常规创作者"].append(kw)
        # 4. Instagram Bio
        elif 'bio' in kw_lower or 'bio for instagram' in kw_lower:
            categories["Instagram Bio 类"].append(kw)
        # 5. Caption
        elif 'caption' in kw_lower or 'quotes' in kw_lower:
            categories["Instagram Caption 类"].append(kw)
        # 6. 工具/功能
        elif any(x in kw_lower for x in ['compass', 'spreadsheet', 'download', 'hub', 'login', 'app']):
            categories["工具/功能类"].append(kw)
        else:
            # 再次检查博彩
            if any(x in kw_lower for x in ['togel', 'slot', 'toto', 'poker', '4d']):
                categories["博彩类 - 印尼"].append(kw)
            else:
                categories["其他类"].append(kw)
    
    return categories

# 更精确的重新分类
def precise_classify(keywords):
    categories = {
        "品牌词类": [],
        "人物/网红 - OnlyFans/成人创作者": [],
        "人物/网红 - 常规创作者": [],
        "博彩类 - 印尼": [],
        "Instagram Bio 类": [],
        "Instagram Caption 类": [],
        "工具/功能类": [],
        "其他类": []
    }
    
    onlyfans_names = {
        "elly clutch", "lilijunex", "pamsnusnu", "megbanksxo onlyfans", "ayleks onlyfans",
        "waifutania", "sayumi sutra", "creamy spot", "norissa valdez", "aria banks",
        "yololary onlyfans", "lara lane onlyfans", "zoweybunny", "lilmermaidxx",
        "samantra onlyfans", "drew gulliver onlyfans", "iamhely", "abby berner",
        "lunaqueeeen", "lela sohna", "sheeya onlyfans", "sophie aspin onlyfans",
        "inked dory", "meido moon", "maggielovieee", "mila ricci nude",
        "allie lynn onlyfans", "khloe knowles", "lelasohna", "pamnusnu",
        "ariaonlyxo onlyfans", "heavann77 onlyfans", "mistress enola", "waifumia",
        "ashleysoft", "alanah cole", "starfucked", "luxlo onlyfans", "devils.goddess",
        "pockycats leaks", "sallydinosaur", "stormiiy", "whipitdev onlyfans",
        "mari avila telegram", "emmaspice", "margopov nude", "aviva sofia",
        "adelynmoore", "nicki minaj onlyfans", "michelleerabbit onlyfans",
        "gabyy_yt xxx", "sindal xie", "kathiesanderss", "xbhau", "marta gromova",
        "aria adams onlyfans", "swimangieswim", "jill_bunny", "madelinexx",
        "sharon piel morena", "eva violet", "val2yummi", "kenalialuv",
        "jade pixel", "drew gulliver", "howtofaithalife"
    }
    
    gambling_terms = {'togel', 'slot', 'toto', 'poker', 'seri', 'bandit', '4d', 'hub', 'link alternatif', 'login'}
    
    bio_terms = {'bio for instagram', 'instagram bio', 'bio for', 'bio ', 'sanskrit bio', 'punjabi bio'}
    caption_terms = {'caption', 'quotes', 'after long time meet', 'when you meet', 'friend quotes'}
    
    for kw in keywords:
        kw_lower = kw.lower()
        
        # 品牌词
        if any(x in kw_lower for x in ['beacons', 'beacon', 'becons']) and 'bio' not in kw_lower:
            categories["品牌词类"].append(kw)
        # OnlyFans
        elif 'onlyfans' in kw_lower or kw in onlyfans_names:
            categories["人物/网红 - OnlyFans/成人创作者"].append(kw)
        # 博彩
        elif any(x in kw_lower for x in gambling_terms) and 'bio' not in kw_lower:
            categories["博彩类 - 印尼"].append(kw)
        # Instagram Bio
        elif any(x in kw_lower for x in bio_terms):
            categories["Instagram Bio 类"].append(kw)
        # Caption
        elif any(x in kw_lower for x in caption_terms):
            categories["Instagram Caption 类"].append(kw)
        # 工具
        elif any(x in kw_lower for x in ['compass', 'spreadsheet', 'download', 'hub']):
            categories["工具/功能类"].append(kw)
        # 常规网红
        else:
            categories["人物/网红 - 常规创作者"].append(kw)
    
    return categories

# 执行分类
categories = precise_classify(keywords)

# 打印结果
print("="*80)
print("BEACONS 关键词分类分析报告")
print("="*80)
print()

for cat, words in categories.items():
    if words:
        print(f"\n📌 {cat} ({len(words)} 个关键词)")
        print("-"*60)
        for w in words:
            print(f"  • {w}")

print()
print("="*80)
print("分类统计")
print("="*80)
for cat, words in categories.items():
    if words:
        print(f"{cat}: {len(words)} 个")
