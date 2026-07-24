"""单独跑B组(zhanggang skill)"""
import os
import time
from pathlib import Path
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

R39_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R39")
WHITE_PAPER_FILE = Path(r"d:\popwave-skills\workspace\深渊主宰-瘦身白描测试\下游产出\Phase1.5-全书剧情白描.md")
DNA_FILE = Path(r"d:\popwave-skills\skills\pop-qidian-write\dna\深渊主宰-v10.md")

B_OUTPUT = R39_DIR / "B-zhanggang"
B_OUTPUT.mkdir(parents=True, exist_ok=True)

white_paper = WHITE_PAPER_FILE.read_text(encoding="utf-8")
dna = DNA_FILE.read_text(encoding="utf-8")
lines = white_paper.split('\n')
paper_segment = '\n'.join(lines[:80])

ch001_anchor = """章号: ch001
核心事件: 索伦在贫民窟夜雨中苏醒，灵魂已融合游戏数据流，用匕首背刺巴拉斯和卡诺波获得30点杀戮经验，查看属性半精灵敏捷19智力18职业平民和一级盗贼，看到薇薇安后背淤伤决定找治疗药剂
爽点: 压力突破(首杀+金手指激活)
钩子: 预知诸神黄昏与圣者浩劫即将来临
关键数据: 杀戮经验30点, 敏捷19, 智力18, 1级盗贼"""

b_prompt = f"""你是一位资深网文写手，严格按 pop-zhanggang 章纲流执行。

# 任务
基于以下输入，写ch001的正文。3100-3500字，不准低于3100字，不准超过3500字。

# zhanggang skill SOP（2步）

## Step 1: 前文分析
（本章是第一章，无前文，直接进入Step 2）

## Step 2: 拆解框架 + 填充细节 + 节奏与收尾

### 2a. 4段式骨架分配篇幅
| 段 | 字数 | 内容 |
|----|------|------|
| 开篇 | 650-750字 | 渲染场景氛围，交代人物行动动机 |
| 发展 | 950-1050字 | 探索/行动过程，1-2个小阻碍，逐步接近核心目标 |
| 高潮 | 850-950字 | 达成核心目标，同步引发新冲突 |
| 结尾 | 650-750字 | 即时反应，留悬念钩子 |

总字数目标：3100-3500字

### 2b. 填充细节
- 多维场景描写 + 动作链 + 心理 + 对话，全部围绕核心冲突
- 描写每章控制在3-8个，每个≤30字——拒绝过多形容词/比喻/拟人
- 大白话，强情绪，高代入感

### 2c. 节奏与收尾
- 慢描写与快行动交替
- 留未完成悬念

# 红线
1. 每章结尾必须是期待感对话钩子——禁止事件完结或情绪落地，强制引导读者读下一章
2. 正文开头完美衔接前文结尾——禁止与前文重复剧情
3. 描写每章控制在3-8个，每个≤30字
4. 禁止AI叙述词和总结性/展望性内容
5. 字数3100-3500字

# 输出格式
```
【第1章正文 | 为第2章铺垫：XXX】

章节名

正文内容...
```

# 深渊主宰笔触DNA（必须遵循）
{dna}

# 本章章纲（核心事件）
{ch001_anchor}

# 剧情白描ch001段（故事流参考）
{paper_segment}

# 开始写作
"""

session = requests.Session()
session.proxies.update(PROXIES)
session.verify = False

headers = {
    "Authorization": f"Bearer {DS_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "model": DS_MODEL,
    "messages": [
        {"role": "system", "content": "你是一位资深网文写手，严格按skill SOP执行。"},
        {"role": "user", "content": b_prompt}
    ],
    "max_tokens": 32768,
    "temperature": 0.85,
    "stream": False
}

for attempt in range(5):
    print(f"[B-zhanggang] 第{attempt+1}次尝试...")
    try:
        response = session.post(
            f"{DS_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        (B_OUTPUT / "ch001.md").write_text(content, encoding="utf-8")
        print(f"[B-zhanggang] 完成，{len(content)}字符")
        break
    except Exception as e:
        print(f"[B-zhanggang] 第{attempt+1}次失败: {type(e).__name__}: {str(e)[:100]}")
        if attempt < 4:
            print(f"[B-zhanggang] 等待10秒后重试...")
            time.sleep(10)
        else:
            print(f"[B-zhanggang] 全部重试失败")
