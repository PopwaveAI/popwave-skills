#!/usr/bin/env python3
"""Extract sessions_spawn calls from events.jsonl to find format specs."""
import json
import sys

path = r"C:/Users/AWMPRO/.paopao/projects/海贼法典/runs/bf64b56c-6a26-4c78-a551-0b58c3b3924d/events.jsonl"
with open(path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        try:
            event = json.loads(line.strip())
        except:
            continue
        items = event.get("items", [])
        for item in items:
            if item.get("toolName") == "sessions_spawn":
                inp_str = item.get("input", "{}")
                try:
                    inp = json.loads(inp_str)
                except:
                    inp = {}
                goal = inp.get("goal", "")
                context = inp.get("context", "")
                
                # Detect which design-pack batch
                batch_id = "?"
                if "001" in goal or "001" in context:
                    batch_id = "ch001-batch"
                if "004" in goal or "004" in batch_id == "?":
                    if "004" in goal or "004" in context:
                        batch_id = "ch004-batch"
                if "007" in goal:
                    batch_id = "ch007-batch"
                if "010" in goal:
                    batch_id = "ch010-batch"
                if "013" in goal:
                    batch_id = "ch013-batch"
                if "016" in goal:
                    batch_id = "ch016-batch"
                if "ch019" in goal or "019" in goal:
                    batch_id = "ch019-batch"
                if "022" in goal:
                    batch_id = "ch022-batch"
                if "025" in goal:
                    batch_id = "ch025-batch"
                if "028" in goal:
                    batch_id = "ch028-batch"
                if "031" in goal:
                    batch_id = "ch031-batch"
                
                # Check context for format instructions
                has_format_table = ("| # | 事件 | 类型 |" in context)
                has_format_anchor = ("设计包v3-格式规范" in context or "v3-format" in context)
                has_simplified = ("| 场景# | 场景名称 |" in context or "| 场景# |" in context)
                has_dimension = ("| 维度 | 内容 |" in context)
                has_l1l2 = ("L1 主线" in context or "L1/L2/L3" in context)
                has_裁剪 = ("| 节点 | 情节作用 | 裁剪" in context)
                
                context_size = len(context)
                
                print(f"Session #{i} | {batch_id}")
                print(f"  Goal: {goal[:150]}...")
                print(f"  Context: {context_size} chars")
                if has_format_table:
                    print(f"  >>> FORMAT LOCKED: 8-col event table")
                if has_format_anchor:
                    print(f"  >>> References v3-format spec")
                if has_simplified:
                    print(f"  >>> FORMAT: scene# table (简化版)")
                if has_dimension:
                    print(f"  >>> FORMAT: dimension table (维度版)")
                if has_l1l2:
                    print(f"  >>> FORMAT: L1/L2/L3 hierarchical")
                if has_裁剪:
                    print(f"  >>> FORMAT: 裁剪影响表")
                if not (has_format_table or has_simplified or has_dimension or has_l1l2 or has_裁剪):
                    print(f"  >>> NO FORMAT SPEC FOUND IN CONTEXT!")
                    # Show what IS in context
                    keywords_found = [k for k in ["事件链", "爽点", "骨架", "格式", "模板", "设计包"] if k in context]
                    print(f"  >>> Context keywords: {keywords_found}")
                print()

sys.exit(0)
