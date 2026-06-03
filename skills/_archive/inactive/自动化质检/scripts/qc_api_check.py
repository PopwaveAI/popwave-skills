"""
qc_api_check.py — LLM API 独立验证引擎

内置两套prompt模板：
- 通用内容审核（content_review）
- 小说章节审核（chapter_review）

支持任何 OpenAI 兼容 API。
"""

import json
import re
import os
import requests
from datetime import datetime


# ── 默认配置 ──
DEFAULT_MODEL = "gpt-4o"
DEFAULT_ENDPOINT = "https://api.openai.com/v1"


# ── Prompt 模板库 ──

PROMPT_TEMPLATES = {
    "content_review": {
        "system": "你是一位专业的内容质量审核员。审核以下内容，按指定维度评分(0~1)。输出合法JSON。",
        "user": """请审核以下内容，按维度打分。

审核内容：
{output_text}

评分维度：
{scoring_dimensions_text}

输出格式（严格JSON，不要额外文字）：
{{"scores": {{"维度1": 0.xx, "维度2": 0.xx}}, "feedback": "评价", "issues": [], "overall_pass": true/false}}"""
    },

    "chapter_review": {
        "system": "你是一位严格的小说质量审核编辑。审核一篇小说章节正文，按标准打分。输出合法JSON。",
        "user": """请审核以下小说章节正文，按7项标准逐项打分(0-10)。

评分标准：
1. 字数达标 (目标2000-2500字)
2. 违禁句式 ("不是A而是B"/"他没有问"/"是某种说不清的")
3. 前300字钩子 (是否有悬念钩子)
4. 章末翻页驱动 (是否有驱动翻页的钩子)
5. 情感弧线匹配 (情绪节奏与设计目标是否一致)
6. 否定句密度 (全章否定句是否合理)
7. 整体可读性 (读者体验综合评分)

正文：
{output_text}

输出JSON格式：
{{"scores": {{"字数达标":0-10,"违禁句式":0-10,"前300字钩子":0-10,"章末翻页驱动":0-10,"情感弧线匹配":0-10,"否定句密度":0-10,"整体可读性":0-10}}, "summary": {{"total_score":0.0,"pass":true,"word_count":0,"critical_issues":[],"违禁句式命中":[],"strong_points":[]}}, "recommendation":"PASS"}}"""
    }
}


# ── 核心调用函数 ──

def call_llm_verify(api_config: dict, template_name: str, output_text: str, scoring_dimensions: list = None) -> dict:
    """
    调用 LLM API 对输出内容做独立验证。

    参数:
        api_config: {
            "endpoint": "https://api.openai.com/v1",
            "model": "gpt-4o",
            "api_key": "sk-xxx"  # 或从环境变量读取
        }
        template_name: prompt 模板名称（"content_review" / "chapter_review"）
        output_text: 待审核的文本内容
        scoring_dimensions: 评分维度列表（仅 content_review 使用）

    返回:
        {"error": str} 或 {"scores": {...}, "feedback": "...", "overall_pass": bool}
    """
    api_key = api_config.get("api_key") or os.environ.get("QC_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    endpoint = api_config.get("endpoint", DEFAULT_ENDPOINT).rstrip("/")
    model = api_config.get("model", DEFAULT_MODEL)

    if not api_key:
        return {"error": "API密钥未配置。设置 QC_LLM_API_KEY 环境变量或在 api_config 中传入。"}

    template = PROMPT_TEMPLATES.get(template_name)
    if not template:
        return {"error": f"未找到模板: {template_name}，可选: {list(PROMPT_TEMPLATES.keys())}"}

    # 构建 scoring_dimensions_text
    if scoring_dimensions:
        dims_text = "\n".join(f"- {d}" for d in scoring_dimensions)
    else:
        dims_text = "（使用模板默认维度）"

    user_msg = template["user"].format(
        output_text=output_text[:8000],  # 限制输入
        scoring_dimensions_text=dims_text
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": template["system"]},
            {"role": "user", "content": user_msg}
        ],
        "max_tokens": 4096
    }

    url = f"{endpoint}/chat/completions"

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        raw = data["choices"][0]["message"]["content"].strip()

        # 提取 JSON
        content = raw
        if "```" in content:
            m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
            if m:
                content = m.group(1).strip()

        # 备用：提取第一个大括号块
        if not content.startswith("{"):
            m = re.search(r'\{[\s\S]*\}', content)
            if m:
                content = m.group(0)

        result = json.loads(content)
        return result

    except requests.exceptions.Timeout:
        return {"error": "API请求超时（120秒）"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API请求失败: {str(e)}"}
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"响应解析失败: {str(e)}", "raw_response": raw if 'raw' in locals() else "N/A"}


# ── 命令行入口 ──

def main():
    """命令行独立调用。"""
    import argparse

    parser = argparse.ArgumentParser(description="LLM API 独立验证")
    parser.add_argument("--text", help="直接输入文本")
    parser.add_argument("--file", help="从文件读取文本")
    parser.add_argument("--template", default="chapter_review", help="prompt 模板名")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="API地址")

    args = parser.parse_args()

    # 获取文本
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        # 从 stdin 读取
        import sys
        text = sys.stdin.read()

    if not text.strip():
        print("QC_API_ERROR: 未提供文本")
        return

    api_config = {
        "api_key": args.api_key or os.environ.get("QC_LLM_API_KEY", ""),
        "model": args.model,
        "endpoint": args.endpoint
    }

    result = call_llm_verify(api_config, args.template, text)

    if "error" in result:
        print(f"QC_API_ERROR: {result['error']}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        scores = result.get("scores", {})
        if scores:
            avg = sum(scores.values()) / len(scores)
            print(f"\nQC_API_RESULT: avg_score={avg:.2f}")


if __name__ == "__main__":
    main()
