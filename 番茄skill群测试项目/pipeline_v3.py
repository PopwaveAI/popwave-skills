#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄skill群测试协议 v3
======================
当前版本反映 R1-R6 实际测试流程。测试通过 TRAE sub-agent 并行执行，不再使用
Python脚本直调API。本文件作为测试协议文档，描述如何组织和执行一轮测试。

---

## skill群架构（4 skill）

| skill | 版本 | 职责 | 产出 |
|-------|------|------|------|
| pop-fanqie-seed | v4.1.0 | 搜热门赛道→行为框架碰撞→合成金手指→四眼法验证 | 梗.md |
| pop-fanqie-plot | v4.0.0 | 从梗推导场景卡→分章施工卡 | 场景卡-batchN.md |
| pop-fanqie-write | v3.0.0 | 从施工卡渲染正文（2000-2500字/章） | chNNN.md |
| pop-fanqie-review | v2.0.0 | 审核正文质量（概念兑现/爽感闭环/节奏/钩子） | 审核-chNNN.md |

## 测试流程

### 标准全链路测试（R1/R2模式）

1. 主agent准备选题，为每个选题启动一组sub-agent
2. seed sub-agent：执行pop-fanqie-seed SKILL.md全流程，产出梗.md
3. plot sub-agent：读取梗.md，执行pop-fanqie-plot，产出场景卡
4. write sub-agent：读取场景卡，逐章渲染正文
5. review sub-agent：读取正文，执行审核
6. 每步产出存入 R{N}/prompts/ 和 R{N}/responses/ 和 R{N}/产出/

### AB对照测试（R6模式）

1. 主agent准备N个选题
2. 每个选题启动2组sub-agent：
   - skill组：注入对应skill的SKILL.md全文作为system prompt
   - 非skill组：只给自由创意指令，不注入skill规范
3. 上下文隔离：每组sub-agent只看到自己的选题，不知道其他选题
4. 产出存入 R{N}/skill模式/ 和 R{N}/非skill模式/

### 控制变量测试（R4/R5模式）

1. 固定种子，变换skill配置（纯燃料/正向心法/去AI味参考/完整skill/无skill）
2. 或固定skill配置，变换种子变体（对话炸弹/人物立体/冲突预埋）
3. 每组sub-agent隔离执行，产出第一章
4. 对比维度：开场冲击力/人物立体度/叙事维度/灵气自然度/节奏密度/章末钩子

## sub-agent隔离原则

- 每组sub-agent只能看到自己的选题和配置
- 不得透露其他选题、其他组别的配置、或预期结论
- skill组的system prompt = SKILL.md全文 + 选题方向
- 非skill组的system prompt = 自由创意指令 + 选题方向

## 产出目录规范

R{N}/
├── skill模式/          # AB测试的skill组产出
├── 非skill模式/        # AB测试的非skill组产出
├── prompts/            # 全链路测试的system/user prompt存档
├── responses/          # 全链路测试的API响应存档
├── 产出/
│   ├── 种子/           # 梗.md
│   ├── 场景卡/         # 场景卡-batchN.md
│   ├── 正文/           # chNNN.md
│   ├── 审核/           # 审核-chNNN.md
│   └── 事实快照.md
├── R{N}测试计划.md     # 本轮测试计划
└── run_pipeline.py     # （仅R1/R2）Python直调API脚本

## 版本历史

- v1 (R1-R2): Python脚本直调DeepSeek API，6阶段管线
- v2 (R3-R5): sub-agent + 控制变量测试方法论
- v3 (R6): sub-agent + AB对照测试方法论（当前）
"""

# 本文件为协议文档，不包含可执行代码。
# 测试通过 TRAE 的 Task 工具启动 sub-agent 执行。
# 如需历史Python脚本，参见 R1/run_pipeline.py 或 R2/run_pipeline.py。
