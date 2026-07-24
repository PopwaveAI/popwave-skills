#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R20测试: DeepSeek vs 豆包 AB测试
项目C: 杀戮神子系统（新德里华裔少年黑道升级流）
ch01-ch05，严格按write v6.2 skill走API

执行方式: 串行（每章需要前章输出作为衔接）
"""

import os
import sys
import json
import time
import requests

# ============ API配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

DOUBAO_API_KEY = "b597f4e5-2370-4bdf-875f-5ae43e43c52b"
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DOUBAO_MODEL = "doubao-seed-2-1-turbo-260628"

TEMPERATURE = 0.7
MAX_TOKENS = 16000
TIMEOUT = 300

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
R20_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_C_DIR = r"C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects\7-16-项目c"

# ============ System Prompt ============
# 完整的write v6.2 skill文件拼合

SYSTEM_PROMPT = """# pop-fanqie-write · 番茄正文渲染

> 心法引导方向，状态驱动写作。写完交付伏笔+方向，人机共创。

---

## SOP骨架

| 步骤 | 做什么 | 产出 | 详细方法 |
|------|--------|------|---------|
| Step 1 | 加载状态+素材+心法分支 | 燃料就绪 | steps/step1.md |
| Step 2 | 写正文 | 2000-2500字 | steps/step2.md |
| Step 3 | 篇幅控制+落盘 | 字数检查 | steps/step3.md |
| Step 4 | 交付+人机共创 | 交付面板 | steps/step4.md |

---

## 红线

1. 搜索必须调用工具——禁止凭记忆
2. 第一章用黄金开篇——前3句扔炸弹
3. 后续章节不套黄金开篇
4. 篇幅不准超3000字
5. 每章有章末钩子
6. 不写思考过程/检查表——直接写正文
7. 写完呈现交付面板

> `references/technique.md` 仅在卡壳时翻阅，不在写作前加载。

---

# Step 1: 加载燃料

## 1a. 加载项目状态

**第一章**：读取`0-立项/创意.md` + `1-骨架/骨架.md`，提取金手指功能+主角设定卡+世界观核心规则+骨架幕序列。

**后续章节**：读取`current-state.md`（已有主角状态+已建立内容+钩子库存+节奏检查）。不重新提取立项包全文——只查current-state.md里没有的特定信息时才回查创意.md/骨架.md对应段落。

## 1b. 搜索素材

写之前搜1-2条真实素材（不是每章都搜，有素材库就用素材库）：

| 搜索类型 | 搜索词 | 找什么 |
|---------|--------|--------|
| 题材相关真实事件 | 关键词 + "真实案例/事件/新闻" | 给故事落地感 |
| 场景参考 | 关键词 + "场景/环境/细节" | 给画面具体感 |

## 1c. 确定心法分支

根据金手指类型选1个分支（不加载其他分支）：

- 金手指有等级/经验/属性/技能树 → **分支A：系统流**
- 金手指偏感知/人际/情感 → **分支B：情感流**
- 金手指偏修炼/功法/血脉 → **分支C：玄幻流**

选好后只默念该分支 + 通用底座，不读其他分支。

### 通用底座（2条）

1. **读者什么时候想关页面** — 无聊立刻切场景
2. **不想规则想什么好看** — 选最好看的写法

### 分支A：系统流

1. 系统交互即爽点 — 面板弹出是爽点窗口不是信息展示
2. 战术博弈>蛮力 — 用规则打信息差
3. 弱→强反差炸裂 — 升级瞬间给足篇幅
4. 冷性满足不是热血 — 冷静计算后精准执行
5. 每章≥1次系统交互且推动剧情

## 1d. 章节类型确认

| 章节类型 | 额外燃料 |
|---------|---------|
| 第一章 | 黄金开篇：前3句扔炸弹，300字内完成冲突+主角+金手指+钩子 |
| 后续章节 | 接前章钩子 + 每3章≥1爽点 + 连续憋屈≤2章 + 章末有钩子 |

---

# Step 2: 写正文

## 约束（6条）

1. 2000-2500字，不准超3000
2. 12岁读者模型（每30秒需新内容）
3. 金手指本章可见且推动剧情
4. 对话引导词只用"道"
5. 章末有钩子
6. 参照主角记忆点和缺点写人物

## 写

跟着心法写。不想规则，想什么好看。

---

# Step 3: 篇幅控制

写完后检查字数：2000-2500字合格。超过3000必须裁剪。

---

# Step 4: 交付 + 人机共创

写完并检查字数后，在章节正文末尾附加"人机共创面板"。

## 交付面板格式

## 📋 本章交付面板

### 当前伏笔清单
| 编号 | 伏笔 | 埋设章 | 状态 |
|------|------|--------|------|

### 下一章方向（请选择或补充）

**方向A：** xxx（预期爽点：xxx）
**方向B：** xxx（预期爽点：xxx）
**方向C：** xxx（预期爽点：xxx）
"""

# ============ 立项包+骨架摘要（注入给API） ============

PROJECT_CONTEXT = """
# 项目立项包·杀戮神子系统

## 一句话故事
华裔少年陈锋在新德里地下世界觉醒杀戮神子系统，从被踩在最底层的无种姓异类，一路杀穿种姓地狱，在新德里黑道的尸山血海上登临神座。

## 金手指
DND杀戮神子系统——击杀获得杀戮经验(KEP)，升级获得属性点(6属性)+专长槽+技能点。可视化面板：等级/经验条/六维属性(力量/敏捷/体质/智力/感知/魅力)/专长树/职业能力/冷却状态。

入口能力：死亡嗅觉——能感知周围半径50米内对自己有杀意的目标。

触发条件：濒死/极端求生状态激活。进入战斗场景自动激活面板，击杀结算需确认。

限制边界：
1. 敌意判定：只有对你有明确杀意的目标才给完整经验——偷袭无防备路人仅获1点
2. 等级衰减：同级目标经验减半，低于自己5级的目标仅给1点
3. 曲线陡峭：Lv1→Lv2需100经验（杀3个普通人）；Lv5→Lv6需5000经验
4. 进阶试炼：兼职武僧需徒手击杀高于自己2级的敌人；进阶影舞者需单人暗杀高于自己3级的目标
5. 能力冷却：职业大招有CD（游荡者"暗影一击"：30秒）
6. 等级锁：初始上限10级——击杀特定首领解锁更高上限

进化方向：
1. 暗影渗透→潜行偷袭→阴影瞬移→暗影分身→暗影领域
2. 杀戮直觉→战斗预感→看穿弱点→因果级读秒
3. 百战躯壳(武僧兼职)→武器刺客→徒手格杀→钢筋铁骨→肉身撼枪械

本质：系统是远古死神阎摩(Yama)散落人间的权柄碎片。觉醒者都是阎摩的"镰刀"——杀人，神祇分食灵魂。觉醒者之间是养蛊关系——最终只能活一个。

## 主角设定卡
- 职业/身份：鞋店之子、街头跑腿——游荡者天然适合底层社会
- 主性格：隐忍的狠辣。表面圆滑（会笑、会低头、会说漂亮话），但每个目标的经验值、风险、回报都在脑子里算好了
- 记忆点：走路无声（猫步）/说话前先扯嘴角笑一下/左手虎口13岁刀疤/兜里永远一把折叠刀
- 缺点：等级焦虑（看到经验值忍不住想刷）/信任障碍（没人能信）/越级冲动（看到高等级目标就估算"杀了能跳几级"）
- 主角危机：系统是阎摩镰刀契约。不收割就被换镰刀。不杀人就变不了强，不变强就被其他觉醒者或黑帮踩死
- 成长弧线：被驱动(为活命杀)→驾驭(主动规划成长)→超越(找摆脱镰刀身份的路)

## 世界观骨架
- 世界格局：新德里三层结构——表层(普通人的大都市)/夹层(地下黑帮割据)/里层(种姓=地狱等级，华裔=连地狱编号都没有的异类)
- 力量体系：4条并行路径——杀戮系统/自然觉醒者/科技武装/印度秘术。主角走第一条
- 核心规则：阎摩权柄碎片+濒死激活+等级锁+敌意判定+灵魂收割自动执行
- 世界危机：表层(黑帮火并)/深层(觉醒者猎杀)/终极(阎摩苏醒)
- 势力格局：达亚尔家族(高种姓刹帝利)/血牛帮(贱民)/辛格警局/阎摩之眼(全球秘社)

## 骨架·第一幕（ch001-025）
幕名：绝境觉醒
功能位：建置——世界观+主角处境+系统激活+第一次杀戮落地
弧线：追债死巷→碎玻璃割喉觉醒→逃入老德里→适应面板→第一次升级→接达亚尔脏活→第一次正式暗杀→Lv.3

### 黄金三章设计：
Ch001·死巷：被堵死巷，四把砍刀，兜里折叠刀。碎玻璃割喉→面板弹出
Ch002·系统：面板展示+第一次杀戮结算+升级Lv.1游荡者。章末钩子：还有三人在追
Ch003·猎杀：利用系统能力反杀+潜行背刺。Lv.0→Lv.3，属性点安排+专长选择

### 配角：
- 阿米尔·汗（发小，血牛帮，情感锚点）
- 拉吉·辛格（警察副局长，中期压力源）
- 盲僧伽内什（助力者，武僧兼职引路人）
- 娜亚（阎摩之眼外勤使者，卷末出场）

### 分层反派：
- 低级·库纳尔：达亚尔家族打手头目，狂躁易怒
- 中期·辛格：贪腐警察副局长
- 中期·卡兰·达亚尔：家族操盘手，傲慢
- 终极·阎摩本尊：远古死神
"""

# ============ 每章User Prompt ============

def get_chapter_prompt(ch_num, prev_chapter_output=None):
    """生成每章的user prompt"""

    if ch_num == 1:
        return f"""{PROJECT_CONTEXT}

---

## 本章任务：写第1章（ch001·死巷）

### 素材参考（已为你搜好，无需再搜）
- 新德里贫民窟真实环境：拥挤巷道、露天排水沟、塑料布搭的棚顶、空气中弥漫着香料和垃圾混合的气味
- 印度高利贷真实运作：月息10%-20%，还不上了就断手断脚，华裔无种姓不受任何法律保护
- 印度街头暴力：砍刀是常见武器，死巷堵人是黑帮收债标准操作

### 心法分支确认
本作金手指有等级/经验/属性/技能树 → 使用**分支A：系统流**
- 系统交互即爽点：面板弹出是爽点窗口不是信息展示
- 战术博弈>蛮力：用规则打信息差
- 弱→强反差炸裂：升级瞬间给足篇幅
- 冷性满足不是热血：冷静计算后精准执行
- 每章≥1次系统交互且推动剧情

### 章节类型：第一章
黄金开篇：前3句扔炸弹，300字内完成冲突+主角+金手指+钩子

### 骨架指引
Ch001·死巷：陈锋被达亚尔家族马仔追债堵在死巷，面前四把砍刀，兜里只有一把折叠刀。章末钩子：碎玻璃割喉→面板弹出

### 约束
1. 2000-2500字，不准超3000
2. 12岁读者模型（每30秒需新内容）
3. 金手指本章可见且推动剧情
4. 对话引导词只用"道"
5. 章末有钩子
6. 参照主角记忆点（走路无声/微笑面具/虎口刀疤/折叠刀）和缺点（等级焦虑/信任障碍/越级冲动）写人物

### 注意
- 不写思考过程/检查表/章意图分析——直接写正文
- 写完后附"交付面板"（伏笔清单+3个下一章方向）
"""

    else:
        # 后续章节：注入前章输出
        ch_hooks = {
            2: "前章钩子：陈锋割喉后系统面板弹出",
            3: "前章钩子：还有三人在追他，而他只有一把碎玻璃和刚加的1点属性",
            4: "前章钩子：杀了达亚尔家族的人，不可能就这么算了",
            5: "前章钩子：需要从ch04输出中提取"
        }

        prev_text = ""
        if prev_chapter_output:
            # 只取前章最后500字作为衔接
            prev_text = f"\n\n### 前章结尾（衔接参考）\n{prev_chapter_output[-500:]}"

        return f"""{PROJECT_CONTEXT}
{prev_text}

---

## 本章任务：写第{ch_num}章

### 心法分支确认
本作金手指有等级/经验/属性/技能树 → 使用**分支A：系统流**
- 系统交互即爽点：面板弹出是爽点窗口不是信息展示
- 战术博弈>蛮力：用规则打信息差
- 弱→强反差炸裂：升级瞬间给足篇幅
- 冷性满足不是热血：冷静计算后精准执行
- 每章≥1次系统交互且推动剧情

### 章节类型：后续章节
{ch_hooks.get(ch_num, "接前章钩子")}
节奏控制：每3章≥1爽点 + 连续憋屈≤2章 + 章末有钩子

### 骨架指引
"""

        # ch02-ch05的骨架指引
        ch_guide = {
            2: """Ch002·系统：面板展示+第一次杀戮结算+升级到Lv.1游荡者。章末钩子：还有三人在追，只有碎玻璃和1点属性
系统面板要像游戏一样——数字跳动、属性选择让读者"也想加点"。升级瞬间给足篇幅，不是"嗯加了"。
陈锋用系统规则做决策：经验值计算、敌意判定、升级路线规划""",
            3: """Ch003·猎杀：第一次利用系统能力反杀——潜行+背刺+经验结算。Lv.0→Lv.3，属性点安排+专长选择
战术博弈：陈锋用"敌意判定"规则判断谁给完整经验，用"死亡嗅觉"感知杀意方向
冷性满足：不是愤怒爆发，是冷静计算后精准执行
弱→强反差：升级前后战力反差要炸裂""",
            4: """Ch004：陈锋逃入老德里贫民窟，适应系统面板。开始理解系统规则——经验衰减/敌意判定/等级锁
系统交互：日常探索中触发面板（查看属性/规划升级路线/发现技能树）
引入新冲突：达亚尔家族在搜捕割喉案的主角
冷性满足：陈锋冷静分析形势，计算下一步""",
            5: """Ch005：陈锋第一次有计划地使用系统能力。可能开始接达亚尔家族的"脏活"（踩点/传递消息）
系统交互：第一次正式任务中的面板使用（死亡嗅觉感知目标杀意/经验计算）
战术博弈：用系统信息差完成任务，不是蛮力
章末钩子：为第一个正式暗杀任务做铺垫"""
        }

        return f"""{get_chapter_prompt_base(ch_num, prev_chapter_output)}

{ch_guide.get(ch_num, "")}

### 约束
1. 2000-2500字，不准超3000
2. 12岁读者模型（每30秒需新内容）
3. 金手指本章可见且推动剧情
4. 对话引导词只用"道"
5. 章末有钩子
6. 参照主角记忆点和缺点写人物

### 注意
- 不写思考过程/检查表/章意图分析——直接写正文
- 写完后附"交付面板"（伏笔清单+3个下一章方向）
"""


def get_chapter_prompt_base(ch_num, prev_chapter_output=None):
    """基础prompt"""
    prev_text = ""
    if prev_chapter_output:
        prev_text = f"\n\n### 前章结尾（衔接参考）\n{prev_chapter_output[-800:]}"

    return f"""{PROJECT_CONTEXT}
{prev_text}

---

## 本章任务：写第{ch_num}章

### 心法分支确认
本作金手指有等级/经验/属性/技能树 → 使用**分支A：系统流**

### 章节类型：后续章节
接前章钩子 + 每3章≥1爽点 + 连续憋屈≤2章 + 章末有钩子"""


def call_api(api_name, system_prompt, user_prompt):
    """调用API"""
    if api_name == "ds":
        url = f"{DS_BASE_URL}/chat/completions"
        key = DS_API_KEY
        model = DS_MODEL
    else:
        url = f"{DOUBAO_BASE_URL}/chat/completions"
        key = DOUBAO_API_KEY
        model = DOUBAO_MODEL

    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    start = time.time()
    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    elapsed = time.time() - start
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return content, usage, elapsed


def main():
    # 输出目录
    ds_dir = os.path.join(R20_DIR, "R20", "deepseek")
    doubao_dir = os.path.join(R20_DIR, "R20", "doubao")
    os.makedirs(ds_dir, exist_ok=True)
    os.makedirs(doubao_dir, exist_ok=True)

    # 存储每章输出用于后续衔接
    ds_chapters = {}
    doubao_chapters = {}

    all_results = []

    for ch in range(1, 6):
        ch_name = f"ch{ch:03d}"
        print(f"\n{'='*60}")
        print(f"第{ch}章 ({ch_name})")
        print(f"{'='*60}")

        # 生成prompt
        if ch == 1:
            user_prompt = get_chapter_prompt(ch)
        else:
            user_prompt = get_chapter_prompt(ch, ds_chapters.get(ch-1))

        # --- DeepSeek ---
        print(f"\n[DS] 调用DeepSeek ({DS_MODEL})...")
        print(f"  System: {len(SYSTEM_PROMPT)}字符 | User: {len(user_prompt)}字符")
        try:
            ds_content, ds_usage, ds_elapsed = call_api("ds", SYSTEM_PROMPT, user_prompt)
            ds_path = os.path.join(ds_dir, f"{ch_name}.txt")
            with open(ds_path, "w", encoding="utf-8") as f:
                f.write(ds_content)
            ds_chapters[ch] = ds_content
            print(f"  完成! {ds_elapsed:.1f}s | {len(ds_content)}字 | tokens:{ds_usage.get('total_tokens', 'N/A')}")
            ds_result = {
                "chapter": ch_name,
                "model": DS_MODEL,
                "content_length": len(ds_content),
                "elapsed": round(ds_elapsed, 1),
                "usage": ds_usage
            }
        except Exception as e:
            print(f"  DeepSeek失败: {e}")
            ds_result = {"chapter": ch_name, "model": DS_MODEL, "error": str(e)}
            ds_chapters[ch] = ""

        # --- 豆包 ---
        # 豆包用独立的前章衔接
        if ch > 1:
            user_prompt_doubao = get_chapter_prompt(ch, doubao_chapters.get(ch-1))
        else:
            user_prompt_doubao = user_prompt

        print(f"\n[豆包] 调用豆包 ({DOUBAO_MODEL})...")
        try:
            doubao_content, doubao_usage, doubao_elapsed = call_api("doubao", SYSTEM_PROMPT, user_prompt_doubao)
            doubao_path = os.path.join(doubao_dir, f"{ch_name}.txt")
            with open(doubao_path, "w", encoding="utf-8") as f:
                f.write(doubao_content)
            doubao_chapters[ch] = doubao_content
            print(f"  完成! {doubao_elapsed:.1f}s | {len(doubao_content)}字 | tokens:{doubao_usage.get('total_tokens', 'N/A')}")
            doubao_result = {
                "chapter": ch_name,
                "model": DOUBAO_MODEL,
                "content_length": len(doubao_content),
                "elapsed": round(doubao_elapsed, 1),
                "usage": doubao_usage
            }
        except Exception as e:
            print(f"  豆包失败: {e}")
            doubao_result = {"chapter": ch_name, "model": DOUBAO_MODEL, "error": str(e)}
            doubao_chapters[ch] = ""

        all_results.append({"deepseek": ds_result, "doubao": doubao_result})

    # 保存汇总
    summary_path = os.path.join(R20_DIR, "R20", "summary.json")
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    # 打印汇总
    print(f"\n{'='*60}")
    print("R20测试完成！汇总：")
    print(f"{'='*60}")
    print(f"{'章节':<10} {'DeepSeek':>30} {'豆包':>30}")
    print("-" * 72)
    for r in all_results:
        ch = r["deepseek"].get("chapter", "?")
        ds_info = f"{r['deepseek'].get('content_length', 0)}字 {r['deepseek'].get('elapsed', 0)}s" if "error" not in r["deepseek"] else "失败"
        db_info = f"{r['doubao'].get('content_length', 0)}字 {r['doubao'].get('elapsed', 0)}s" if "error" not in r["doubao"] else "失败"
        print(f"{ch:<10} {ds_info:>30} {db_info:>30}")

    print(f"\nDeepSeek目录: {ds_dir}")
    print(f"豆包目录: {doubao_dir}")
    print(f"汇总: {summary_path}")


if __name__ == "__main__":
    main()
