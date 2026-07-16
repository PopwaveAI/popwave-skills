#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄R8测试管线 - AB对照测试（API直调版）
4选题 × 2模式（skill v5.0.0 vs 非skill自由创意） = 8组创意种子
通过DeepSeek API直调，不使用sub-agent
"""
import os, json, requests, time

API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-v4-flash"

R8_DIR = r"d:\popwave-skills\番茄skill群测试项目\R8"
PROMPTS_DIR = os.path.join(R8_DIR, "prompts")
RESPONSES_DIR = os.path.join(R8_DIR, "responses")
SKILL_DIR_OUT = os.path.join(R8_DIR, "skill模式")
NOSKILL_DIR_OUT = os.path.join(R8_DIR, "非skill模式")

SKILL_MD_PATH = r"d:\popwave-skills\skills\pop-fanqie-seed\SKILL.md"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

NOSKILL_SYSTEM = """你是一个网文创意编辑，擅长从零开始构思有趣的开书创意。请基于用户给的方向和市场搜索数据，生成创意种子。"""

TOPICS = {
    "A": {
        "name": "都市异能",
        "direction": "想写都市异能",
        "search_data": """## 市场搜索数据（WebSearch结果）

### 2026年5月番茄榜单热门
- 《十日终焉》热度指数:现象级悬疑智斗，长期霸榜，在读超400万+
- 《我在精神病院学斩神》番茄门面担当，改编动画都火了
- 《都重生了谁还装富二代啊》5月涨幅王，日增在读超10万
- 《末世:开局先囤十亿物资》

### 2025都市异能热门趋势
- 《我不是戏神》三九音域(320万字连载) - 悬疑+民俗+身份反转
- 《捞尸人》纯洁滴小龙(349万字连载) - 湘南捞尸+民俗+中式克苏鲁
- 《国民法医》志鸟村(370万字完本) - 职业流+都市
- 《莫犯太岁》脑洞玄幻+都市异能+轻松解压+反向套路

### 核心趋势总结
- 悬疑+民俗+身份反转为主流方向
- 冷门职业切口不容易撞车
- 失意主角低谷开局+扮猪吃虎
- 单元剧结构（每卷一个独立事件）"""
    },
    "B": {
        "name": "诡异流",
        "direction": "想写诡异流",
        "search_data": """## 市场搜索数据（WebSearch结果）

### 2025诡异流热门作品
- 《捞尸人》纯洁滴小龙 - 民俗中式恐怖+克苏鲁式未知恐惧+人性博弈，以湘南捞尸行当为切口
- 《诡舍》夜来风雨声 - 规则怪谈+无限轮回+高概念惊悚，密室逃生+生死游戏+诅咒解谜
- 《山海见诡》玄鵺 - 中式奇诡+克苏鲁元素+民间传说重构
- 《旧域怪诞》狐尾的笔 - 回到童年，家里处处是诡异（吃饭必须在子时前结束，不能回应窗外敲门声，楼梯不能数到第7级）

### 诡异流核心模式
- 规则怪谈+叛逆流（最大爆款方向）
- 中式民俗+克苏鲁（高端品质线）
- 诡异国运流（宏大叙事）
- 诡异复苏+驭诡者（经典框架）
- 轻松搞笑流诡异（蓝海差异化）

### 核心趋势总结
- 规则怪谈仍是主流底盘，但"被动求生"已审美疲劳
- "主动对抗规则"是已验证的爽感方向
- 需要新鲜切入点破同质化"""
    },
    "C": {
        "name": "女拳问题",
        "direction": "想写当前女拳问题严重的（即当前社会男女对立、打拳现象严重的现实题材方向）",
        "search_data": """## 市场搜索数据（WebSearch结果）

### 现有热门作品
- 《我，怒怼女拳，奖励千万豪车！》番茄小说 - 陈慕穿越到平行世界，开局怒怼女拳，奖励千万豪车
- 《男女对立:开局被女拳师锁狗链！》飞卢 - 系统觉醒流
- 《全世界男人消失！女拳崩溃了！》飞卢 - 这个世界的女拳极度盛行
- 《穿越：开局打翻极端女权者》17k - 玄幻奇幻+女拳+战斗

### 现有作品通病
- 清一色"系统奖励/怒怼"流
- 行为引擎空泛（只会"怼"）
- 直接对抗易踩红线
- 同质化严重

### 核心趋势总结
- 需要差异化切入（非直接对抗）
- 聚焦"反差/反转/博弈"而非直接攻击
- 对称设计（不分男女，专治双标）更安全"""
    },
    "D": {
        "name": "海贼王",
        "direction": "想写海贼王同人",
        "search_data": """## 市场搜索数据（WebSearch结果）

### 番茄热门海贼王同人
- 《海贼:海军史上最大败类》又名《酒色财气?可我是个好海军》作者:马里奥吃鸡胸肉 133万字连载中 - 亦正亦邪海军流，用自己的行动影响海贼世界
- 《海贼之火山猎人》永攀 105万字 - 赏金猎人胎穿流，决心成为最强赏金猎人
- 《海贼王之白夜叉》Zippo 241万字 - 亲眼见证海贼王罗杰的传奇
- 《海贼之化身为雷》认真一点 167万字 - 波澜壮阔的大海贼时代
- 《海贼法典》惟求得中 87万字 - 普通白领穿越到罗杰死后的大海贼时代
- 《我在海贼镇守推进城一百年》李四羊 101万字完本
- 《这个海贼背靠正义》信息交流 167万字连载中

### 海贼王同人金手指模式
- 穿越带系统（氪金抽卡/卡牌碎片/兑换商城）
- 自创金手指（无人荒岛开局，自创修行法门）
- 猎人笔记（写需求+记录敌人名字+杀死获得加成）
- 胎穿/魂穿（从小培养，改变剧情走向）
- 海军视角（正义与邪恶的灰度博弈）

### 核心趋势总结
- 海军视角比海贼视角更受欢迎（正义灰度博弈>纯海贼打打杀杀）
- 亦正亦邪人设最吸粉
- 同人需要新鲜切入点——纯系统流/抽奖流已审美疲劳
- 影响原著角色走向比单打独斗更有代入感"""
    }
}

SKILL_USER_TEMPLATE = """## 用户选题方向
{direction}

## 市场搜索数据
{search_data}

## 任务
请严格按照SKILL.md的SOP执行：

1. Step 1 搜梗+发散：基于以上搜索数据（已为你搜好，无需再搜），执行1d自由发散——给出3个完全不同方向的创意（名称+一句话描述+画面+为什么有意思）
2. Step 2 碰撞加固+合成：选最好的1个，用行为框架碰撞加固（装上行为引擎），然后梗×机制×限制合成金手指
3. 四眼法验证（画面/限制/场景量/行为引擎）
4. Step 3 落盘：输出梗.md格式

注意：
- 发散阶段不加约束，3个方向必须差异最大化
- 行为框架碰撞在选定方向后做加固，不在发散阶段做限定
- 梗不得与番茄Top20核心机制雷同
- 必须有行为引擎，不能是纯系统机制（抽卡/升级/兑换）
- 限制条件必须天然存在，不能是"无敌系统"
- 番茄简介必须是散文体——第一人称，带对话，带情绪弧线，带钩子
"""

NOSKILL_USER_TEMPLATE = """## 用户选题方向
{direction}

## 市场搜索数据
{search_data}

## 任务
请用你自己的创意能力，为用户生成一个开书创意种子。

要求：
1. 基于以上搜索数据和你的创意能力，给出3个不同的创意方向供选择
2. 选其中最好的1个，完善为一个开书种子

## 3个创意方向格式
### 创意1：[名称]
一句话描述：[一句话说清这个创意是什么]
画面：[脑补的场景]
为什么有意思：[吸引人的点]

### 创意2：...
### 创意3：...

## 最终种子格式
# 创意种子

## 核心创意
- 创意名：（一句话）
- 灵感来源：（搜索到的/自己想的）
- 机制：（一句话）
- 限制：（一句话）
- 一句话简介：（完整的创意描述）

## 番茄简介
【关键词1】+【关键词2】+【关键词3】+【关键词4】

简介（150-300字）
"""

def call_api(system_prompt, user_prompt, task_name):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 8000,
        "stream": False
    }
    print(f"  调用API [{task_name}]...")
    print(f"  System: {len(system_prompt)}字符 | User: {len(user_prompt)}字符")
    start = time.time()
    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    elapsed = time.time() - start

    write_file(os.path.join(PROMPTS_DIR, f"{task_name}-system.txt"), system_prompt)
    write_file(os.path.join(PROMPTS_DIR, f"{task_name}-user.txt"), user_prompt)
    write_file(os.path.join(RESPONSES_DIR, f"{task_name}-response.txt"), content)
    write_file(os.path.join(RESPONSES_DIR, f"{task_name}-meta.json"), json.dumps({
        "task": task_name, "content_length": len(content),
        "usage": usage, "elapsed": round(elapsed, 1)
    }, ensure_ascii=False, indent=2))

    print(f"  完成! {elapsed:.1f}s | 输出{len(content)}字 | tokens:{usage.get('total_tokens','N/A')}")
    return content, usage, elapsed

def main():
    for d in [PROMPTS_DIR, RESPONSES_DIR, SKILL_DIR_OUT, NOSKILL_DIR_OUT]:
        os.makedirs(d, exist_ok=True)

    skill_md = read_file(SKILL_MD_PATH)
    print(f"已加载SKILL.md v5.0.0: {len(skill_md)}字符")

    results = {}

    for topic_key, topic in TOPICS.items():
        topic_name = topic["name"]
        direction = topic["direction"]
        search_data = topic["search_data"]

        print(f"\n{'='*60}")
        print(f"选题{topic_key}: {topic_name}")
        print(f"{'='*60}")

        # --- Skill模式 ---
        print(f"\n--- [{topic_key}-skill] ---")
        skill_user = SKILL_USER_TEMPLATE.format(direction=direction, search_data=search_data)
        skill_content, skill_usage, skill_elapsed = call_api(
            skill_md, skill_user, f"R8-{topic_key}-skill"
        )
        skill_path = os.path.join(SKILL_DIR_OUT, f"选题{topic_key}-{topic_name}.md")
        write_file(skill_path, skill_content)
        print(f"  已保存: {skill_path}")
        results[f"{topic_key}-skill"] = {
            "content": skill_content, "usage": skill_usage, "elapsed": skill_elapsed
        }

        # --- 非Skill模式 ---
        print(f"\n--- [{topic_key}-noskill] ---")
        noskill_user = NOSKILL_USER_TEMPLATE.format(direction=direction, search_data=search_data)
        noskill_content, noskill_usage, noskill_elapsed = call_api(
            NOSKILL_SYSTEM, noskill_user, f"R8-{topic_key}-noskill"
        )
        noskill_path = os.path.join(NOSKILL_DIR_OUT, f"选题{topic_key}-{topic_name}.md")
        write_file(noskill_path, noskill_content)
        print(f"  已保存: {noskill_path}")
        results[f"{topic_key}-noskill"] = {
            "content": noskill_content, "usage": noskill_usage, "elapsed": noskill_elapsed
        }

    print(f"\n{'='*60}")
    print("R8测试完成！汇总：")
    print(f"{'='*60}")
    for key, val in results.items():
        print(f"  {key}: {len(val['content'])}字 | {val['elapsed']:.1f}s | tokens:{val['usage'].get('total_tokens','N/A')}")
    print(f"\n产出目录: {R8_DIR}")

if __name__ == "__main__":
    main()
