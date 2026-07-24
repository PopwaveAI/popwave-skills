#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R35 v2 纯净版推演脚本
- 走API，避免agent上下文污染
- 让API读四张地图+索伦设定，推演索伦在BG3世界的卷1白描
- 禁止把深渊主宰原剧情搬过来，必须基于BG3剧情推演
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
R35_DIR = SCRIPT_DIR
MAPS_DIR = os.path.join(R35_DIR, "四张地图")
INPUT_V2 = os.path.join(R35_DIR, "input-v2")
OUTPUT_V2 = os.path.join(R35_DIR, "output-v2")
os.makedirs(INPUT_V2, exist_ok=True)
os.makedirs(OUTPUT_V2, exist_ok=True)

# ============ 加载四张地图 ============
def load_maps():
    maps = {}
    for name in ["01-地理地图", "02-力量地图", "03-势力地图", "04-危机地图"]:
        path = os.path.join(MAPS_DIR, f"{name}.md")
        with open(path, "r", encoding="utf-8") as f:
            maps[name] = f.read()
    return maps

# ============ 索伦设定（纯净版，去除深渊主宰剧情污染）============
SUOLUN_SETTING = """# 主角设定（索伦注入BG3世界）

## 主角：索伦

**身份背景**：
- 半精灵，盗贼职业，原本是费伦大陆的孤儿
- 在鹦鹉螺号坠毁事件中被夺心魔幼体感染
- 灵魂同时融合了一份"游戏数据流"——他能看到属性面板、技能树、升级路径
- 他预知主脑将在3个月后觉醒，知道各地BOSS的弱点

**金手指：游戏数据流**
- 【属性面板】：半空中浮现淡蓝色光屏，显示六维属性（力量/敏捷/体质/智力/感知/魅力）
- 【升级路径】：击杀敌人获得杀戮经验，可自主分配升级职业/属性/专长
- 【预知】：知道主脑3个月后将觉醒，知道各地BOSS的弱点
- 【限制】：数据流不能告诉他"选择"——他知道BOSS弱点，但不知道该不该打；预知有时模糊（未来在变化）

**初始属性**：
【姓名：索伦】
【种族：半精灵】
【职业：平民LV1 / 盗贼LV1】
【属性：力量12 敏捷19 体质15 智力18 感知15 魅力16】
【生命值：4/12】
【状态：被夺心魔幼体感染（倒计时14天）】

## 妹妹：薇薇安（8岁女孩）

**身份**：索伦的妹妹，在鹦鹉螺号坠毁时与索伦走散
**特征**：瘦弱，但有天生术士天赋（魅力21，超凡门槛）
**核心欲望**：跟着哥哥，不被抛弃
**功能**：情感锚点+行动动机

## 老狗希斯
十四岁的老猎犬，薇薇安的唯一守护者，在索伦昏迷期间保护薇薇安
"""

# ============ API调用函数 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
TEMPERATURE = 0.8
TIMEOUT = 600


def call_deepseek_api(system_prompt, user_prompt, max_tokens=8000):
    """调用DeepSeek API（配置与R33一致）"""
    import requests
    import time
    
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {DS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": TEMPERATURE,
        "stream": False
    }
    
    start = time.time()
    resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    elapsed = time.time() - start
    
    if resp.status_code != 200:
        raise RuntimeError(f"API调用失败: {resp.status_code} {resp.text}")
    
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    
    return content, elapsed, usage


# ============ 主流程 ============
def main():
    print("=" * 60)
    print("R35 v2 纯净版推演")
    print("索伦投入BG3世界，走API")
    print("=" * 60)
    
    # 加载四张地图
    maps = load_maps()
    print(f"\n[0] 加载四张地图:")
    for name, content in maps.items():
        print(f"  {name}: {len(content)}字")
    
    # 构建system prompt
    system_prompt = """你是一位资深网文写手和剧情设计师，精通博德之门3（Baldur's Gate 3）的剧情结构。

你的任务：基于博德之门3的世界，把一个叫索伦的半精灵盗贼投入这个世界，推演他在BG3世界Act1（对应网文卷1）的剧情白描。

核心要求：
1. 索伦必须经历BG3的主线剧情——被夺心魔幼体感染、寻找解药、对抗月出之塔教派
2. BG3的地理/势力/危机完全保留——鹦鹉螺号坠毁、德鲁伊树林、地精营地、幽冥地域、月出之塔
3. 索伦的金手指是"游戏数据流"——能看到属性面板、升级路径、BOSS弱点
4. 禁止搬运深渊主宰的剧情——不能出现"藏宝洞/蛇魔/食人魔/北地女巫"等深渊主宰元素
5. 剧情白描格式：叙事流，一口气讲完整卷故事，禁止拆章节标签，禁止使用表格，禁止结构化分析

输出格式：
# 索伦在BG3 · 卷1剧情白描（Act1，对应ch001-ch024）

{2000-4000字的流畅叙事白描}

---
卷末钩子：{1-2句话点明本卷留下的悬念}"""
    
    # 构建user prompt
    user_prompt = f"""请推演索伦在博德之门3世界Act1的剧情白描。

# 四张地图（BG3原版）

## 01-地理地图

{maps['01-地理地图']}

## 02-力量地图

{maps['02-力量地图']}

## 03-势力地图

{maps['03-势力地图']}

## 04-危机地图

{maps['04-危机地图']}

# 主角设定

{SUOLUN_SETTING}

# 推演要求

1. **地理坐标必须用BG3原版**：索伦在鹦鹉螺号坠毁→荒野沙滩→德鲁伊树林→地精营地→幽冥地域→月出之塔路径。禁止改成"琥珀城/乱葬岗/藏宝洞"等深渊主宰地名。

2. **势力碰撞必须用BG3原版**：索伦碰撞地精教派（明萨拉）、德鲁伊集会（哈尔辛）、提夫林难民、月出之塔教派（凯瑟里克）。禁止出现"科尔帮/晨曦神殿/北地女巫"等深渊主宰势力。

3. **危机推进必须用BG3原版**：感染倒计时14天→月出之塔扩张→戈塔什布局→主脑觉醒。禁止出现"圣者浩劫/恐惧魔神/神子"等深渊主宰危机。

4. **索伦的金手指是"游戏数据流"**：他能看到属性面板、升级路径、BOSS弱点。这让他在BG3世界有了"作弊"优势——他知道凯瑟里克的弱点，知道明萨拉的战术，知道戈塔什的大恶魔契约。

5. **薇薇安的定位**：索伦的妹妹，在坠毁时与索伦走散，索伦在Act1的主要个人动力是找到薇薇安。薇薇安有天生术士天赋（魅力21超凡门槛），但不涉及深渊主宰的魔神神子设定。

6. **推演方法**：对每个叙事节点，叠加四张地图的坐标：
   - 地理坐标：摄像头在哪
   - 力量坐标：索伦等级变化
   - 势力坐标：索伦和谁碰撞
   - 危机坐标：世界倒计时推进

7. **信息差**：读者知道但索伦不知道的信息（如戈塔什是幕后黑手、主脑是终极敌人）要用括号简注。

8. **字数**：2000-4000字叙事流，一口气讲完Act1故事。

请直接输出白描，不要写分析过程。"""
    
    # 落盘input
    input_path = os.path.join(INPUT_V2, "卷1白描_input.md")
    with open(input_path, "w", encoding="utf-8") as f:
        f.write(f"# R35 v2 推演输入\n\n## === SYSTEM ===\n\n{system_prompt}\n\n## === USER ===\n\n{user_prompt}")
    print(f"\n[1] 输入落盘: {input_path}")
    print(f"  system长度: {len(system_prompt)}字")
    print(f"  user长度: {len(user_prompt)}字")
    
    # 调用API
    print(f"\n[2] 调用DeepSeek API...")
    try:
        content, elapsed, usage = call_deepseek_api(system_prompt, user_prompt, max_tokens=8000)
        print(f"  用时: {elapsed:.1f}s")
        print(f"  tokens: {usage}")
        print(f"  产出长度: {len(content)}字")
    except Exception as e:
        print(f"  API调用失败: {e}")
        return
    
    # 落盘output
    output_path = os.path.join(OUTPUT_V2, "卷1剧情白描-v2.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n[3] 产出落盘: {output_path}")
    
    # 保存meta
    meta = {
        "config": "R35 v2 纯净版",
        "method": "API调用，避免agent上下文污染",
        "input_length": len(system_prompt) + len(user_prompt),
        "output_length": len(content),
        "elapsed_seconds": elapsed,
        "tokens": usage
    }
    meta_path = os.path.join(OUTPUT_V2, "meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("R35 v2 推演完成！")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
