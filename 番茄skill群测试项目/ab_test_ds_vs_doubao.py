#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AB测试脚本: DeepSeek vs 豆包(Doubao)
=====================================
同一组prompt分别发给两个模型，输出并排保存供对比。

用法:
  python ab_test_ds_vs_doubao.py {task_name}

会读取:
  prompts/{task_name}-system-prompt.txt
  prompts/{task_name}-user-prompt.txt

输出:
  responses/{task_name}-ds-output.txt      (DeepSeek输出)
  responses/{task_name}-doubao-output.txt   (豆包输出)
  responses/{task_name}-meta.json           (对比统计)

也可以直接传prompt内容:
  python ab_test_ds_vs_doubao.py --system "系统提示" --user "用户提示" --name "task名"
"""

import sys
import os
import json
import time
import argparse
import requests

# ============ API配置 ============

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

DOUBAO_API_KEY = "b597f4e5-2370-4bdf-875f-5ae43e43c52b"
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DOUBAO_MODEL = "doubao-seed-2-1-turbo-260628"

# ============ 通用参数 ============

TEMPERATURE = 0.7
MAX_TOKENS = 16000
TIMEOUT = 300

# ============ 脚本目录 ============

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(SCRIPT_DIR, "prompts")
RESPONSES_DIR = os.path.join(SCRIPT_DIR, "responses")


def call_ds(system_prompt, user_prompt):
    """调用DeepSeek API"""
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
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    start = time.time()
    response = requests.post(
        f"{DS_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=TIMEOUT
    )
    response.raise_for_status()
    elapsed = time.time() - start
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return content, usage, elapsed


def call_doubao(system_prompt, user_prompt):
    """调用豆包API (ARK平台)"""
    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DOUBAO_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    start = time.time()
    response = requests.post(
        f"{DOUBAO_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=TIMEOUT
    )
    response.raise_for_status()
    elapsed = time.time() - start
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return content, usage, elapsed


def run_ab_test(system_prompt, user_prompt, task_name):
    """并行调用两个模型"""
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(RESPONSES_DIR, exist_ok=True)

    # 保存prompt
    with open(os.path.join(PROMPTS_DIR, f"{task_name}-system-prompt.txt"), "w", encoding="utf-8") as f:
        f.write(system_prompt)
    with open(os.path.join(PROMPTS_DIR, f"{task_name}-user-prompt.txt"), "w", encoding="utf-8") as f:
        f.write(user_prompt)

    results = {}

    # --- DeepSeek ---
    print(f"\n[1/2] 调用 DeepSeek ({DS_MODEL})...")
    print(f"  System: {len(system_prompt)}字符 | User: {len(user_prompt)}字符")
    try:
        ds_content, ds_usage, ds_elapsed = call_ds(system_prompt, user_prompt)
        ds_path = os.path.join(RESPONSES_DIR, f"{task_name}-ds-output.txt")
        with open(ds_path, "w", encoding="utf-8") as f:
            f.write(ds_content)
        print(f"  完成! {ds_elapsed:.1f}s | 输出{len(ds_content)}字 | tokens:{ds_usage.get('total_tokens', 'N/A')}")
        results["deepseek"] = {
            "content": ds_content,
            "content_length": len(ds_content),
            "usage": ds_usage,
            "elapsed": round(ds_elapsed, 1),
            "model": DS_MODEL
        }
    except Exception as e:
        print(f"  DeepSeek失败: {e}")
        results["deepseek"] = {"error": str(e)}

    # --- 豆包 ---
    print(f"\n[2/2] 调用 豆包 ({DOUBAO_MODEL})...")
    try:
        doubao_content, doubao_usage, doubao_elapsed = call_doubao(system_prompt, user_prompt)
        doubao_path = os.path.join(RESPONSES_DIR, f"{task_name}-doubao-output.txt")
        with open(doubao_path, "w", encoding="utf-8") as f:
            f.write(doubao_content)
        print(f"  完成! {doubao_elapsed:.1f}s | 输出{len(doubao_content)}字 | tokens:{doubao_usage.get('total_tokens', 'N/A')}")
        results["doubao"] = {
            "content": doubao_content,
            "content_length": len(doubao_content),
            "usage": doubao_usage,
            "elapsed": round(doubao_elapsed, 1),
            "model": DOUBAO_MODEL
        }
    except Exception as e:
        print(f"  豆包失败: {e}")
        results["doubao"] = {"error": str(e)}

    # --- 保存对比统计 ---
    meta = {
        "task": task_name,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "system_prompt_length": len(system_prompt),
        "user_prompt_length": len(user_prompt),
        "deepseek": {
            "model": DS_MODEL,
            "content_length": results.get("deepseek", {}).get("content_length", 0),
            "elapsed": results.get("deepseek", {}).get("elapsed", 0),
            "usage": results.get("deepseek", {}).get("usage", {}),
            "error": results.get("deepseek", {}).get("error", None)
        },
        "doubao": {
            "model": DOUBAO_MODEL,
            "content_length": results.get("doubao", {}).get("content_length", 0),
            "elapsed": results.get("doubao", {}).get("elapsed", 0),
            "usage": results.get("doubao", {}).get("usage", {}),
            "error": results.get("doubao", {}).get("error", None)
        }
    }
    meta_path = os.path.join(RESPONSES_DIR, f"{task_name}-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # --- 汇总 ---
    print(f"\n{'='*60}")
    print(f"AB测试完成: {task_name}")
    print(f"{'='*60}")
    for model_name, val in results.items():
        if "error" in val:
            print(f"  {model_name}: 失败 - {val['error']}")
        else:
            print(f"  {model_name}: {val['content_length']}字 | {val['elapsed']}s | tokens:{val['usage'].get('total_tokens', 'N/A')}")
    print(f"\n输出目录: {RESPONSES_DIR}")

    return results


def main():
    parser = argparse.ArgumentParser(description="AB测试 DeepSeek vs 豆包")
    parser.add_argument("task_name", nargs="?", help="任务名（从prompts/目录读取prompt文件）")
    parser.add_argument("--system", help="直接传系统提示")
    parser.add_argument("--user", help="直接传用户提示")
    parser.add_argument("--name", help="任务名（配合--system/--user使用）")
    args = parser.parse_args()

    # 方式1: 从文件读取
    if args.task_name:
        system_path = os.path.join(PROMPTS_DIR, f"{args.task_name}-system-prompt.txt")
        user_path = os.path.join(PROMPTS_DIR, f"{args.task_name}-user-prompt.txt")
        if not os.path.exists(system_path):
            print(f"错误: 找不到 {system_path}")
            sys.exit(1)
        if not os.path.exists(user_path):
            print(f"错误: 找不到 {user_path}")
            sys.exit(1)
        with open(system_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        with open(user_path, "r", encoding="utf-8") as f:
            user_prompt = f.read()
        run_ab_test(system_prompt, user_prompt, args.task_name)

    # 方式2: 直接传内容
    elif args.system and args.user:
        task_name = args.name or f"test_{int(time.time())}"
        run_ab_test(args.system, args.user, task_name)

    else:
        parser.print_help()
        print("\n示例:")
        print("  python ab_test_ds_vs_doubao.py my_task                    # 从prompts/读取")
        print("  python ab_test_ds_vs_doubao.py --system 'sys' --user 'usr' --name 'task'  # 直接传")


if __name__ == "__main__":
    main()
