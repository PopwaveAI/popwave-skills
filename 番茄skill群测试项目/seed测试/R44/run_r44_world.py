#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R44 world测试：用王道1·宗门公务员的创意.md+ch001.md走world流程
验证world能否承接seed产出的三核心故事纲领，产出骨架.md

输入：R44 phase2-创意.md + phase3-ch001.md
输出：骨架.md（力量体系+地图+势力+危机+第一卷弧线）
"""

import os
import sys
import json
import time
import requests

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
TEMPERATURE = 0.85
TIMEOUT = 600

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

SKILLS_BASE = r"d:\popwave-skills\skills"
R44_OUTPUT = os.path.join(SCRIPT_DIR, "output")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        parts.append(read_file(path))
    return "\n\n---\n\n".join(parts)

# world SKILL.md + step3 + step4 作为system prompt
WORLD_SYSTEM = read_skill_files("pop-fanqie-world", ["SKILL.md", "steps/step3.md", "steps/step4.md"])

# 输入：R44的创意.md + ch001.md
CREATIVE_MD = read_file(os.path.join(R44_OUTPUT, "phase2-创意.md"))
CH001_MD = read_file(os.path.join(R44_OUTPUT, "phase3-ch001.md"))

def call_ds(system_prompt, user_prompt, max_tokens=12000):
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": max_tokens,
        "stream": False
    }
    start = time.time()
    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT, proxies=PROXIES)
    response.raise_for_status()
    elapsed = time.time() - start
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return content, usage, elapsed

def build_world_prompt():
    return f"""# 任务

按pop-fanqie-world v1.0.0的完整SOP，基于以下创意.md和ch001.md，执行world流程，产出骨架.md。

## 输入1：创意.md（seed Phase 2产出）

{CREATIVE_MD}

## 输入2：ch001.md（seed Phase 3产出）

{CH001_MD}

## 输入3：市场校准.md
（缺失——本项目无市场校准文件，标注缺失，不阻塞）

## 输入4：参考书DNA
（缺失——本项目无参考书DNA，标注缺失，不阻塞）

## 执行要求

按world SOP完整执行Step 1-4：

### Step 1 · 加载三件底牌
- 从创意.md提取种子条款（创意/金手指机制+限制/行为引擎/主角轮廓/故事纲领三核心）
- 从ch001提取起点（核心事件→章末钩子→金手指激活状态→已出场角色）
- 市场校准和参考书DNA标注缺失

### Step 2 · 从创意生长世界

#### 2a. 三源合流设计力量体系
- 第一源（赛道参考）：缺失，从玄幻修仙赛道常识推导
- 第二源（参考书DNA）：缺失
- 第三源（创意.md）：从金手指机制+限制+行为引擎+故事纲领推导

力量体系设计起点判定：这个项目是"修炼流"（世界观自带修炼体系，金手指只是加速器）还是"规则系"（世界规则就是力量体系）？根据创意.md判断。

产出力量层级表（5-7个层级），每个层级必须有：
- 名称（≤6字，贴合本项目世界观，不套"炼气筑基"模板）
- 这个世界长什么样（MMO式等级区描述）
- 主角在这个层级面对什么
- 升级触发条件（从行为引擎推导，不是"打够怪就升级"）
- 参考源

力量跨度：第一卷从阶位1到阶位N（对齐创意.md故事纲领的力量路径第一幕）

#### 2b. 从力量体系+行为引擎生长地图
推导逻辑（MMO式）：力量层级→每个阶位的"区域主题"→宗门/世界地图

每个区域回答：
- 对应哪个力量阶位？
- 主角的核心行为是什么？（从行为引擎推导——管理事务）
- 有什么信息差可以利用？

输出：城市结构表（区域/对应阶位/主角行为/信息差来源/势力归属/出现幕）

#### 2c. 从力量体系+地图生长势力
推导逻辑：力量阶位→区域→谁控制资源？→势力

每层势力必须回答：
1. 为什么主角必须和这个势力冲突？
2. 主角靠什么赢？
3. 赢了得到什么？

注意：创意.md故事纲领已有4层敌人梯度（杂物科内部→外门既得利益→内门长老院→宗门规则本身），world需要把这4层细化为具名势力。

#### 2d. 危机体系设计（四源）
- 世界固有危险：从创意.md故事纲领的危机源头推导
- 力量体系内压：进入更高阶位必然面对的压力
- 金手指反噬：从金手指限制条款（阻力值/信任值）推导
- 赛道惯例压力：修仙流读者期待的特定压力

倒计时设计：2-3条倒计时（触发条件→到期章→后果）

### Step 3 · 第一卷弧线设计

#### 3a. 第一卷终点
从Step 2的势力结构和危机倒计时推导。

#### 3b. 幕序列（3-4幕）
从Step 2的敌人梯度+危机倒计时推导。每幕=一个"对赌难度升级"的弧段。

注意：创意.md故事纲领已有4级力量路径映射4幕（部门自治→外门整合→宗门体制→棋局博弈），world需要把这4级细化为具体幕序列。

每幕必须有：
- 功能位（建置/冲突升级/高潮/余波+伏笔）
- 对赌难度
- 弧线（一句话）
- 章节预算
- 幕末钩子

#### 3c. 核心高潮点（2-3个）
基于Step 2的"危机叠加节点"展开为三段式高潮。

#### 3d. 悬念分层
每条悬念必须回答"读者在猜什么"。

#### 3e. 配角设计
补充seed未覆盖的功能性配角。每个配角必须回答"这个角色在主角的对赌行为中扮演什么角色？"。

### Step 4 · 落盘骨架.md

按以下格式产出完整骨架.md：

```markdown
# 《宗门公务员》· 第一卷骨架

> world Step 1-3 · {{timestamp}}
> 回溯创意.md条款：[列出核心回溯链]

## 一、三件底牌
（底牌状态汇总）

## 二、世界从创意生长

### 力量体系（从金手指限制推导）
（力量层级表+推导链）

### 城市舞台（为对赌设计）
（城市结构表+对赌场景说明）

### 势力结构（每层提供对赌对象）
（势力结构表+三问回答）

### 危机压力（从限制条款推导）
（倒计时清单+推导链）

## 三、第一卷弧线

### 终点
（Step 3a产出）

### 幕序列
（Step 3b产出）

### 核心高潮点
（Step 3c产出）

### 悬念分层
（Step 3d产出）

### 配角
（Step 3e产出）
```

## 红线（必须遵守）
1. 必须加载三件底牌——创意+首章必须加载，市场校准和参考书DNA缺失标注缺失
2. 每项世界要素必须回溯创意.md条款——金手指/行为引擎/主角轮廓/故事纲领三核心，至少回溯一条
3. 力量体系必须三源合流——赛道常识+创意.md要素推导（参考书DNA缺失）
4. 第一卷敌人必须4层梯度——每层至少1个具名反派
5. 力量体系是骨架，地图/势力/危机是血肉——血肉必须塞入骨架

## 注意
- 这个创意是阶级攀爬型——主角生在修仙世界里，靠管理才能往上爬。world要设计的是"主角要往上爬的阶梯"（力量体系=管理权限层级），不是"主角要发现的世界"
- 金手指是《宗门管理手册》——机制是生成管理方案，限制是阻力值/信任值。力量体系要围绕"管理权限"设计，不是传统的"修仙境界"
- 行为引擎是管理事务（开分工会/制定规章/资源盘点/谈判/人事任免）——地图和势力必须支持这些行为

直接输出完整骨架.md，不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print(f"R44 world：王道1（宗门公务员）走world流程")
    print(f"输入：创意.md + ch001.md → 输出：骨架.md")
    print("=" * 60)

    print(f"\n[world] 从创意生长世界→骨架.md...")
    world_prompt = build_world_prompt()
    try:
        world_output, world_usage, world_elapsed = call_ds(
            WORLD_SYSTEM, world_prompt, max_tokens=12000
        )

        # 落盘input
        input_content = f"# SYSTEM PROMPT\n\n{WORLD_SYSTEM}\n\n---\n\n# USER PROMPT\n\n{world_prompt}"
        input_path = os.path.join(INPUTS_DIR, "world-骨架_input.md")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(input_content)

        # 落盘output
        output_path = os.path.join(OUTPUT_DIR, "world-骨架.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(world_output)

        print(f"  完成! {world_elapsed:.1f}s | {len(world_output)}字符 | tokens:{world_usage.get('total_tokens', 0)}")
        print(f"    input  → {input_path}")
        print(f"    output → {output_path}")
    except Exception as e:
        print(f"  失败: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("R44 world测试完成！")
    print(f"{'='*60}")
    print(f"\n产出: {os.path.join(OUTPUT_DIR, 'world-骨架.md')}")
    print(f"下一步：人工验收骨架.md能否被plot承接")

if __name__ == "__main__":
    main()
