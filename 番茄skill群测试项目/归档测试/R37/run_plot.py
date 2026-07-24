#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R37 plot阶段 - 四张地图推演卷1剧情白描
- 走API，避免agent上下文污染
- 输入：seed立项包（四张地图+人物包）
- 产出：卷1剧情白描（2000-4000字叙事流）
"""

import os
import json
import time
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(SCRIPT_DIR, "01-seed", "立项包.md")
PLOT_DIR = os.path.join(SCRIPT_DIR, "02-plot")
os.makedirs(PLOT_DIR, exist_ok=True)

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"


def call_api(system, user, max_tokens=8000):
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": max_tokens, "temperature": 0.8, "stream": False
    }
    start = time.time()
    resp = requests.post(url, headers=headers, json=payload, timeout=600)
    elapsed = time.time() - start
    if resp.status_code != 200:
        raise RuntimeError(f"API失败: {resp.status_code} {resp.text}")
    data = resp.json()
    return data["choices"][0]["message"]["content"], elapsed, data.get("usage", {})


def main():
    print("=" * 60)
    print("R37 plot阶段 - 四张地图推演卷1剧情白描")
    print("=" * 60)

    with open(SEED_PATH, "r", encoding="utf-8") as f:
        seed_content = f.read()
    print(f"\n[0] 加载seed立项包: {len(seed_content)}字")

    system_prompt = """你是一位资深网文剧情设计师，精通"四张地图叠加推演法"。

你的任务：基于seed立项包的四张地图+人物包，推演卷1剧情白描。

核心方法：四张地图叠加推演法
对每个L2单元卡执行6步：
1. 查地理地图 → 确定摄像头位置
2. 查力量地图 → 确定主角等级变化
3. 查势力地图 → 确定碰撞和演变
4. 查危机地图 → 确定倒计时推进
5. 因果链串联 → 生成叙事段
6. 标注信息差 → 增加"读者知道但角色不知道"

输出格式：
# 卷1剧情白描（ch001-ch020，对应纽约市篇）

{2000-4000字叙事流，一口气讲完整卷故事}

---
卷末钩子：{1-2句话点明本卷留下的悬念}

格式要求：
- 叙事流，一口气讲完
- 禁止拆"第X章"标签
- 禁止使用表格
- 禁止写"铺垫/推进/高潮/余波"结构标签
- 每段叙事自然包含2-3层地图信息（地理+力量+势力+危机）
- 信息差用括号简注：（读者知道但阿米尔不知道：XXX）
- 像给朋友讲一部你刚看完的剧"""

    user_prompt = f"""请推演"印度版我在美国搞内战"卷1剧情白描。

# seed立项包（四张地图+人物包）

{seed_content}

# 推演要求

1. **地理坐标**：第一卷限定在纽约市五区+泽西城。摄像头路径：肯尼迪机场→哈莱姆→布鲁克林→曼哈顿→自由女神像。

2. **力量坐标**：阿米尔从LV1（被抢劫）→LV5（扶植华尔街代理人），对应美元资产从0→500万。

3. **势力碰撞**：阿米尔从底层起步，依次碰撞：
   - 第一战：哈莱姆毒枭黑桃（LV3）
   - 第二战：布鲁克林帮派大D（LV2，策反吞并）
   - 第三战：警察局长沃克（LV5，渗透）
   - 第四战：老钱家族阿什利（LV8，卷末正面交锋）

4. **危机推进**：
   - 个人：7天倒计时贯穿全卷（必须挑起冲突）
   - 表层：纽约帮派战争升级
   - 深层：老钱家族操控市长选举
   - 终极：美国社会撕裂

5. **信息差**：读者知道阿什利是终极反派，阿米尔直到卷末才知道。

6. **金手指融入**：阿米尔的"内战系统"能看到派系面板/矛盾洞察/战利品分配。系统的本质是"把印度的种姓矛盾经验反向应用"——阿米尔用印度底层智慧看穿美国的阶级矛盾。

7. **卷末高潮**：自由女神像决战——阿米尔在自由女神像前与阿什利正面对决，象征"印度达利特挑战美国老钱"。

8. **字数**：2500-4000字叙事流。

请直接输出白描，不要写分析过程。"""

    input_path = os.path.join(PLOT_DIR, "白描推演_input.md")
    with open(input_path, "w", encoding="utf-8") as f:
        f.write(f"# R37 plot阶段输入\n\n## === SYSTEM ===\n\n{system_prompt}\n\n## === USER ===\n\n{user_prompt}")
    print(f"\n[1] 输入落盘: {input_path}")

    print(f"\n[2] 调用API...")
    try:
        content, elapsed, usage = call_api(system_prompt, user_prompt, max_tokens=8000)
        print(f"  用时: {elapsed:.1f}s")
        print(f"  tokens: {usage}")
        print(f"  产出: {len(content)}字")
    except Exception as e:
        print(f"API失败: {e}")
        return

    output_path = os.path.join(PLOT_DIR, "卷1剧情白描.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n[3] 产出落盘: {output_path}")

    meta = {"input_length": len(system_prompt) + len(user_prompt), "output_length": len(content), "elapsed": elapsed, "tokens": usage}
    with open(os.path.join(PLOT_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("R37 plot阶段完成！")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
