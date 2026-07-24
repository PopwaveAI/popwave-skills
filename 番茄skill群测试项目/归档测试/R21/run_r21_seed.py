#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R21测试: 参考书DNA约束下的seed质量验证
变量: 印度背景 + 系统强调战斗杀戮升级（与参考书非战斗为主形成gap）
AB test: DeepSeek vs 豆包
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
TIMEOUT = 600  # seed产出可能较长，加大timeout

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============ System Prompt ============

SYSTEM_PROMPT = """# pop-fanqie-seed · 番茄立项引擎

> 参考书DNA提取（可选）→ 问偏好 → 标签搜索 → 创意融合 → 完整立项包 → 世界自洽验证
> 产出：0-立项/创意.md（金手指+主角设定卡+世界观骨架+长线线索+番茄简介）

## SOP骨架

| 步骤 | 做什么 | 产出 |
|------|--------|------|
| Step 0 | 参考书DNA提取（可选·有txt时执行） | 参考书DNA.md |
| Step 1 | 问用户偏好→标签搜索→创意发散→选+融合 | 1个融合创意 |
| Step 2 | 立项展开（7个产出） | 立项包 |
| Step 3 | 验证（四眼法+衍生性+自洽+代价+世界观深度+主角危机） | 通过/打回 |
| Step 4 | 项目空间初始化+落盘创意.md | 创意.md |

## 红线

1. 必须先问用户偏好再搜索——禁止跳过直接搜索
2. 金手指只加限制不加代价——使用条件/边界/冷却可以，扣寿命/扣记忆等负反馈禁止
3. 世界自洽四问必须全部回答——能力从何来/触发条件/作用边界/世界规则如何执行
4. 世界观不能是"静态舞台"——必须有世界格局/力量体系（多路径）/世界危机/势力格局
5. 主角必须有"存在性危机"——不是任务式倒计时，危机与金手指本质挂钩
6. 有参考书时必须执行Step 0——提取DNA作为Step 2设计约束，禁止跳过

---

# Step 2: 立项展开

把融合创意展开为完整立项包。每个产出都有推导逻辑，不是填空。

## 参考书DNA约束（有参考书时生效）

如果Step 0产出了`参考书DNA.md`，立项展开时必须加载它，作为以下设计约束：

| DNA维度 | 约束什么 | 怎么约束 |
|---------|---------|---------|
| 系统设计模式 | 金手指设计 | 系统需要匹配参考书的深度——非战斗功能（商店/任务/被动技能）+ 世界观转译机制 |
| 剧情节奏样本·单元剧循环 | plot骨架 | 单元剧循环模式（遇到NPC→系统扫描→交互→结算→新危机）作为plot骨架的节奏基础 |
| 剧情节奏样本·长线推进 | plot骨架 | 长线在单元剧之间怎么穿插、boss什么时候暗示/出场 |
| 主角生存压力源 | 主角危机+节奏 | 压力曲线升降嵌入每章节奏中，不是独立设计 |
| 社会交互模式 | 世界观+骨架 | 必须设计非战斗社会交互场景+NPC系统标注机制 |
| 资源经济系统 | 世界观骨架 | 资源稀缺+可转换链+替代品经济 |
| 世界观转译机制 | 金手指+世界观 | 系统把现实世界转译成游戏术语 |
| 主角设计 | 主角设定卡 | 前世身份赋能/初始弱点/核心生存策略/成长方向 |
| Boss设计 | plot骨架 | boss首次暗示时机/出场前铺垫层数/设计维度/第一次交互方式 |
| 笔触特征 | write心法参考 | 系统面板格式/句式节奏作为write心法的补充约束 |

**关键原则**：DNA是设计约束不是内容模板——学习参考书"怎么做到好"，不是复制"做了什么"。

## 产出1·一句话故事
谁+想做什么+为什么

## 产出2·草纲
谁+想做什么+为什么+如何做+阻力+结局方向

## 产出3·金手指

### 铁律：只加限制不加代价
- 限制 = 使用条件/边界
- 代价 = 用一次扣一年寿命/用一次忘一段记忆 ← 禁止
- 限制随剧情逐渐解锁

### 6要素
1. 创意：一句话
2. 功能：能做什么（入口能力——最劲爆的那个）
3. 触发条件：什么情况下能用（自然限制，不是惩罚）
4. 限制边界：使用条件/范围/冷却——初始限制严格，随成长解锁
5. 进化方向：含≥3种衍生分支（质变型，不是量的变化）
6. 本质：金手指与世界底层逻辑的关系。进化到尽头会触及什么世界真相？

## 产出4·主角设定卡

从金手指反推主角。6要素：
- 职业/身份：什么人最适合这个金手指
- 主性格
- 记忆点：视觉化特征
- 缺点：从金手指限制推导
- 主角危机：存在性危机——不解决就xxx，不是任务式倒计时。危机与金手指本质挂钩
- 成长弧线：从"被金手指驱动"→"驾驭金手指"→"超越金手指"

## 产出5·世界观骨架

从金手指推导世界规则。6要素：
1. 世界格局：世界有多大？谁掌控？普通人在哪？
2. 力量体系：至少2条并行路径，金手指属于哪条？
3. 核心规则：2-3层互相制约。世界自洽四问必须回答
4. 世界危机：世界级威胁正在发生
5. 势力格局：谁掌握核心资源？谁对抗谁？主角在哪个位置？至少2个对立势力
6. 进度框架：主角在世界格局中的位置迁移

### 世界自洽四问
- 能力从何来？
- 触发条件是什么？
- 作用边界在哪？
- 世界规则如何执行？

## 产出6·长线线索
- 主线悬念：金手指本质的终极秘密
- 长线伏笔：金手指进化方向暗示的终极格局

## 产出7·番茄简介
150-300字散文体，含创意展示/限制暗示/爽点期待/2句台词/情绪弧线。
"""

# ============ 参考书DNA摘要 ============

DNA_SUMMARY = """
# 参考书DNA摘要（从《我在美国搞内战-捕梦者》提取）

## 维度1·系统设计模式
系统是生存管理系统，管5件事：HP/属性/技能/商店/任务。
关键设计："斩杀线"——血量低于5就死，每小时扣1点。系统是生存倒计时，不只是战力面板。
非战斗交互占70%：搜尸获得技能、交易触发被动技能、吃药触发系统反馈、社交触发忠诚度。

## 维度2·剧情节奏样本
单元剧循环：遇到NPC→系统扫描标注→交互→系统结算→获得资源/技能→章末新危机引入
每3-5章一个闭环。变种方式：换NPC类型/换交互方式/换资源类型/换系统功能。
长线穿插：每2-3个单元剧后插1章长线推进。boss通过NPC随口提及+系统标注自然埋入。
战斗vs非战斗 = 1:4。

## 维度3·主角生存压力源（合入节奏）
系统级压力（血量4/60，不回血就死）。压力随单元剧升降——杀人后缓解→新危机引入→再升高。

## 维度4·社会交互模式
系统给每个NPC加游戏化标注（影响主角决策）。社交触发被动技能/交易触发系统结算/救人触发忠诚度。

## 维度5·资源经济系统
6种稀缺资源（HP/药/钱/食物/技能/信息）。资源可转换（尸体→钱→药→血量）。有替代品（鱼药=人药）。信息本身是资源。

## 维度6·世界观转译机制
系统把现实世界"翻译"成游戏术语。美国→魔域地下城、警察→堕落执法者、流浪汉→哥布林、帮派→食人魔。
转译影响决策（看到"堕落执法者"就知道可以贿赂）。双重视角制造反差爽感。

## 维度7·主角设计
前世身份直接赋能（前童星→表演技能+名人效应+社交能力）。
核心生存策略是"交易+信息差+系统辅助"，不是战斗力。
成长方向是"建势力网/获取信息/控制资源"，不是"从Lv1到Lv99"。

## 维度8·Boss设计
ch02首次暗示→ch10正式出场（8章铺垫）。系统标注包含完整背景故事。
第一次交互是谈判不是战斗。boss有honor code。与主角是利用关系不是敌杀关系。
"""

# ============ User Prompt ============

USER_PROMPT = f"""
# 用户偏好

- 赛道：都市异能/系统流，印度新德里背景
- 元素：杀戮升级、种姓制度、华裔无种姓者的生存挣扎
- 创意点子：主角是新德里华裔少年，觉醒杀戮神子系统——击杀获得经验值，升级获得属性点和技能。系统本质是远古死神阎摩散落人间的权柄碎片。强调战斗+杀戮升级，但世界不是只有战斗。
- 参考书：《我在美国搞内战-捕梦者》DNA已提取（见下方摘要）

{DNA_SUMMARY}

---

# 关键变量说明

本项目的核心gap设计：

**参考书DNA来自一本"非战斗为主"的书（战斗:非战斗=1:4），但我们的项目要"强调战斗+杀戮升级"。**

这不是矛盾——DNA约束的是"方法论"不是"比例"：
1. 系统深度要匹配参考书（HP/斩杀线/非战斗功能/资源经济/NPC标注/转译机制），但战斗比例可以提高
2. 单元剧循环模式要学（遇到NPC→系统扫描→交互→结算→新危机），但交互方式可以是战斗为主
3. 资源经济要学（资源稀缺+转换链+替代品），但资源类型适配战斗系统（经验值/技能/装备/血量）
4. Boss设计要学（提前暗示+完整背景+第一次交互是谈判+honor code），但boss最终还是要打
5. 世界观转译要学（系统给现实世界起游戏名字），但用印度神话体系（阎摩/罗刹/阿修罗/轮回）而不是DND

战斗比例目标：战斗:非战斗 = 3:2（参考书是1:4，我们调整到3:2但保留非战斗的系统交互）

---

# 任务

按seed v11流程执行：
1. Step 1已由用户提供偏好（赛道/元素/创意点子已明确），直接进入创意发散→选+融合
2. Step 2: 立项展开7个产出（必须加载参考书DNA约束）
3. Step 3: 验证（六项检查）
4. 如果验证通过，直接输出完整立项包（创意.md格式）

注意：
- 金手指本质要设计（阎摩权柄碎片→进化到尽头触及什么世界真相？）
- 主角危机必须是存在性危机（与金手指本质挂钩，不是任务式倒计时）
- 世界观必须有世界格局/力量体系（多路径）/世界危机/势力格局
- 世界观转译机制要用印度神话体系
- Boss设计要有提前暗示+完整背景+honor code+第一次交互是谈判
- 系统要有HP/斩杀线机制+非战斗功能（商店/搜尸获得技能/NPC标注）
- 资源经济要有稀缺设计+转换链+替代品
- 战斗比例调整为3:2但保留非战斗系统交互

直接输出完整立项包，不要问用户，不要分段确认。
"""


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
    output_dir = os.path.join(SCRIPT_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)

    all_results = []

    # --- DeepSeek ---
    print(f"\n[1/2] 调用DeepSeek ({DS_MODEL})...")
    print(f"  System: {len(SYSTEM_PROMPT)}字符 | User: {len(USER_PROMPT)}字符")
    try:
        ds_content, ds_usage, ds_elapsed = call_api("ds", SYSTEM_PROMPT, USER_PROMPT)
        ds_path = os.path.join(output_dir, "r21-ds-seed.md")
        with open(ds_path, "w", encoding="utf-8") as f:
            f.write(ds_content)
        print(f"  完成! {ds_elapsed:.1f}s | {len(ds_content)}字 | tokens:{ds_usage.get('total_tokens', 'N/A')}")
        ds_result = {
            "model": DS_MODEL,
            "content_length": len(ds_content),
            "elapsed": round(ds_elapsed, 1),
            "usage": ds_usage,
            "path": ds_path
        }
    except Exception as e:
        print(f"  DeepSeek失败: {e}")
        ds_result = {"model": DS_MODEL, "error": str(e)}
        ds_content = ""

    # --- 豆包 ---
    print(f"\n[2/2] 调用豆包 ({DOUBAO_MODEL})...")
    try:
        doubao_content, doubao_usage, doubao_elapsed = call_api("doubao", SYSTEM_PROMPT, USER_PROMPT)
        doubao_path = os.path.join(output_dir, "r21-doubao-seed.md")
        with open(doubao_path, "w", encoding="utf-8") as f:
            f.write(doubao_content)
        print(f"  完成! {doubao_elapsed:.1f}s | {len(doubao_content)}字 | tokens:{doubao_usage.get('total_tokens', 'N/A')}")
        doubao_result = {
            "model": DOUBAO_MODEL,
            "content_length": len(doubao_content),
            "elapsed": round(doubao_elapsed, 1),
            "usage": doubao_usage,
            "path": doubao_path
        }
    except Exception as e:
        print(f"  豆包失败: {e}")
        doubao_result = {"model": DOUBAO_MODEL, "error": str(e)}
        doubao_content = ""

    all_results = {"deepseek": ds_result, "doubao": doubao_result}

    # 保存meta
    meta_path = os.path.join(output_dir, "r21-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    # 汇总
    print(f"\n{'='*60}")
    print("R21 seed测试完成！")
    print(f"{'='*60}")
    for name, val in all_results.items():
        if "error" in val:
            print(f"  {name}: 失败 - {val['error']}")
        else:
            print(f"  {name}: {val['content_length']}字 | {val['elapsed']}s | tokens:{val['usage'].get('total_tokens', 'N/A')}")
    print(f"\n输出目录: {output_dir}")


if __name__ == "__main__":
    main()
