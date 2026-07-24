"""
R38 剧情白描推演脚本
严格按 pop-fanqie-plot v9.0.0 Step 4 四图叠加推演法
调用DeepSeek API推演ch02-ch020剧情白描
"""
import json
import os
from pathlib import Path
import requests

# ============ 配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

R38_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R38")
WORLD_BUILD_FILE = R38_DIR / "02-plot" / "世界构筑.md"
CH001_FILE = R38_DIR / "01-seed" / "ch001.md"
IDEA_FILE = R38_DIR / "01-seed" / "创意.md"
OUTPUT_FILE = R38_DIR / "02-plot" / "卷1剧情白描.md"
INPUT_LOG_FILE = R38_DIR / "02-plot" / "api_input.md"

# ============ 加载世界构筑 + ch001锚点 + 创意文档 ============
world_build = WORLD_BUILD_FILE.read_text(encoding="utf-8")
ch001 = CH001_FILE.read_text(encoding="utf-8")
idea_doc = IDEA_FILE.read_text(encoding="utf-8")

# ============ 构造system prompt ============
system_prompt = f"""你是一位资深网文剧情设计师，精通"四张地图叠加推演法"。

任务：基于以下世界构筑文档+创意文档+黄金首章锚点，推演第一卷剧情白描（ch02-ch020）。

# 推演方法：四张地图叠加推演法

核心公式：剧情白描 = L2单元卡 × 四张地图叠加 × 因果链推理

对每个L2单元卡执行6步：
1. 查地理地图 → 确定摄像头位置（这段故事发生在哪个地标）
2. 查力量地图 → 确定主角等级变化（这段故事主角从LVx到LVy）
3. 查势力地图 → 确定碰撞和演变（这段故事哪些势力碰撞）
4. 查危机地图 → 确定倒计时推进（这段故事哪些倒计时推进）
5. 因果链串联 → 生成叙事段（把以上四图信息串成故事流）
6. 标注信息差 → 增加"读者知道但角色不知道"

# L2单元卡（从幕序列提取）

第一幕（ch002-007）：鹦鹉螺号坠毁点 → 德鲁伊树林 → 地精营地
- L2-1：ch002-003 德鲁伊树林接触（主角到达树林，与提夫林+德鲁伊建立临时关系，发现蝌蚪网络节点）
- L2-2：ch004-005 地精营地外围（与明萨拉第一次冲突，灵能感知LV2激活）
- L2-3：ch006-007 地精营地核心（清除三首领，救出更多俘虏，发现月出之塔坐标）

第二幕（ch008-015）：月出之塔 → 幽冥地域
- L2-4：ch008-010 前往月出之塔+幽冥地域过渡（凯瑟里克追杀开始，影心加入，灵能屏障LV3激活）
- L2-5：ch011-012 月出之塔外围（死亡骑士围攻，灵能屏障首次实战）
- L2-6：ch013-015 月出之塔核心（凯瑟里克决战，审判之火LV4激活，种子消耗过半）

第三幕（ch016-020）：博德之门城
- L2-7：ch016-018 进入博德之门城（发现戈塔什的阴谋，下城区接触）
- L2-8：ch019-020 戈塔什对决+卷末高潮（帝皇投影LV5，戈塔什败北但幕后阿什利家族暗示）

# 写作要求

1. 整卷一口气写完，不拆章节标签，整卷故事流一口气写下来
2. 以"给朋友讲故事"的方式，自然流畅，确保故事本身好看
3. 融入叙事：画面/情绪/内心活动都融入叙事，不单独标注
4. 每段标注信息差/伏笔/钩子，用括号内联
5. 消化世界构筑：把四张地图+人物包的关键信息融入故事流

# 世界构筑文档

{world_build}

# 创意文档

{idea_doc}

# 黄金首章锚点（ch001，已由seed产出，不重新推演）

{ch001}

# 开始推演

从ch002开始推演，从ch001章末钩子（月出之塔+蝌蚪指向塔+种子消耗倒计时）延续。
推演到ch020为止，整卷一口气写完。
"""

# 保存input
INPUT_LOG_FILE.write_text(system_prompt, encoding="utf-8")
print(f"[INPUT] 已保存到 {INPUT_LOG_FILE}")
print(f"[INPUT] 长度: {len(system_prompt)} 字符")

# ============ 调用API ============
print("[API] 开始调用DeepSeek API...")
headers = {
    "Authorization": f"Bearer {DS_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "model": DS_MODEL,
    "messages": [
        {"role": "system", "content": "你是一位资深网文剧情设计师，精通四张地图叠加推演法。"},
        {"role": "user", "content": system_prompt}
    ],
    "max_tokens": 8000,
    "temperature": 0.8,
    "stream": False
}

try:
    response = requests.post(
        f"{DS_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=300
    )
    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    
    # 落盘output
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"[OUTPUT] 已保存到 {OUTPUT_FILE}")
    print(f"[OUTPUT] 长度: {len(content)} 字符")
    print(f"[API] 推演完成")
except Exception as e:
    print(f"[ERROR] API调用失败: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"[ERROR] 响应: {e.response.text}")
