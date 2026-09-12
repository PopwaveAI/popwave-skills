# -*- coding: utf-8 -*-
"""跑批：三个评委（读者／编辑／对手）＋ 三维排序官。

设计要点（照 评委agent/ 与 参数冻结.md）：
1. 每稿每角色一次独立调用，互不共享 message 历史，评委看不到别人的结论。
2. 两轮分离：第一轮只发正文；第二轮再发"本章该写什么"，只用于内容剧情维。
3. 零 system message；temperature 0；max_tokens 32000。
4. 排序官单独一次调用，看到全部匿名稿，但看不到任何角色的结论。
5. 每稿记 finish_reason 与 reasoning_tokens；正文为 0 或截断即判失败。
"""
import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
SK = Path(r"d:\popwave-skills\新流程探索\网文编辑")
IN = SK / "scripts" / "输入"
ROOT = SK / "scripts" / "输出"
HAN = re.compile(r"[\u4e00-\u9fff]")

ROLE_PROMPT = {
    "读者": """你是一个网文读者，只读这一章，不评价作者，不看别的稿。
按下面的顺序回答，全部用 JSON，不要写别的话：
{{
 "读到哪里被抓住":[{{"位置":"行号或原文片段","为什么":"用一句话说清是哪一笔起了作用"}}],
 "读到哪里出戏":[{{"位置":"行号或原文片段","为什么":"说清是哪个词或哪句话让你卡住"}}],
 "还想不想看下一章":"想 / 不想 / 说不上来",
 "理由":"一到两句"
}}""",
    "编辑": """你是一个逐句审稿的编辑。只读这一章，逐句看，不许只给整体印象。

【判据】（命中就写编号）
{criteria}

全部用 JSON，不要写别的话：
{{
 "逐句问题":[{{"行":12,"引文":"原句","问题":"搭配矛盾 / 成分缺 / 生造词 / 情绪直述 / 替读者下结论 / 比喻方向错 / 指代不明 / 时代语域 / 其他","红线":"G17 或空","为什么":"一句话"}}],
 "最严重的三处":["行号"],
 "无明显问题的小节":["行号区间"]
}}""",
    "对手": """你是一个专门挑死穴的对手。只读这一章，你的任务不是夸，是找出这一章最经不起追问的地方。
全部用 JSON，不要写别的话：
{{
 "最经不起追问的一处":{{"位置":"行号或原文片段","追问":"你会问作者什么","为什么答不上来":"一句话"}},
 "次严重的一处":{{"位置":"","追问":"","为什么答不上来":""}},
 "如果要删一段":"哪一段，为什么"
}}""",
    "修正官": """你是一个逐句审稿的编辑，任务是把这一章改到能发布（合格线 60 分）。只读这一章，逐句看，不许只给整体印象。

【判据】（命中就写编号）
{criteria}

【硬要求】
1. 每条问题都要带行号与原文引文。
2. **每条问题都要给"改法"，且改法必须是可直接替换的整句**——不许写"建议删掉""建议加强""注意节奏"这类空话，也不许用省略号代替句子。
3. 找问题的顺序：先句法层硬伤（生造词、话没说完、搭配矛盾、比喻方向错、动词被省掉），再描写层（情绪直述、抽象空泛），再节奏层（长句塞满、连续平段）。
4. 最后指出该章**最需要重写的一段**，并给出重写后的整段（不要只给要点）。

全部用 JSON，不要写别的话：
{{
 "逐句问题":[{{"行":12,"引文":"原句","问题":"搭配矛盾 / 成分缺 / 生造词 / 情绪直述 / 替读者下结论 / 比喻方向错 / 指代不明 / 时代语域 / 其他","红线":"G17 或空","为什么":"一句话","改法":"替换后的整句"}}],
 "最严重的三处":["行号"],
 "最需要重写的一段":{{"起止行":"23-31","为什么":"一句话","重写":"重写后的整段"}},
 "改后能否到 60 分":"能 / 不能，说明一句"
}}""",
}

ROUND2_PROMPT = """下面是本章的"本章该写什么"，以及另一份正文。只判一件事：该写的东西有没有被写出来（不是有没有被提到）。
全部用 JSON，不要写别的话：
{{
 "该写的条目":[{{"条目":"原文摘录","有没有被写出来":"写出来了 / 只是提到了 / 漏了","位置":"行号或原文片段","证据":"一句话"}}],
 "落点":"命中了 / 略偏 / 失守，说明一句",
 "前后矛盾":[{{"位置":"","矛盾在哪":""}}]
}}

【本章该写什么】
{spec}

【正文】
{body}"""

PARA_PROMPT = """下面给你一整章，以及这一章里最该重写的一段（起止行）。你的任务是**只重写这一段**，其余不动。

【判据】
{criteria}

【硬要求】
1. 产出必须是**可以直接替换原文那一段的整段文字**。不许出现"建议""可以改成""注意"这类话，不许用省略号代替段落。
2. 保留原段承担的情节功能（发生了什么、谁做了什么、结果是什么），不许改剧情。
3. 把概述改成实景：给出地点、动作、感官细节；把"告知感受"换成可见的动作。
4. 段落长度与原文相当，不超过原文的两倍。

全部用 JSON，不要写别的话：
{{
 "原文问题":"一句话说清原段差在哪",
 "重写":"重写后的整段",
 "动过的地方":["逐条列出改了什么"]
}}

【要重写的段】行 {lines}

【全章正文】
{body}"""

REBUILD_PROMPT = """下面给你一章正文。你的任务是把**整章重写一遍**，目标是达到 60 档（及格线：能发布）。

【判据】
{criteria}

【硬要求】
1. 产出必须是**完整的、可直接替换原章的整章正文**。不许出现"建议""省略""同上"这类话，不许用省略号代替段落。
2. 事件不变：谁做了什么、结果是什么，按原文。
3. 章内结构重排：把最抓人的一处钩子提到开篇前三段内；信息释放改成一次一件事；落点移到章末。
4. 清掉一级红线：正文带工作标记、生造词、成分缺（动词被省掉）、假反转。
5. 长度与原文相当，不少于原文的八成。

全部用 JSON，不要写别的话：
{{
 "原章的三处硬伤":["带行号"],
 "重排说明":"一句话说清动了什么结构",
 "重写正文":"整章正文，段落之间用空行分隔"
}}

【本章该写什么】
{spec}

【原章正文】
{body}"""

RANK_PROMPT = """下面是同一批的几份正文，匿名编号。你是排序官。先读判据，再排序。

【判据】
{criteria}

【本批口径】本批各稿都是开篇单元（第1章或独立单章），位置相同，可以直接比。比"内容剧情"时，比的是**开局立的钩子清不清楚、读者知不知道接下来要看什么**，不是"这一章发生了多少事"；比"情绪节奏"时，比的是**本章内部的情绪起伏与落点有没有效**，不是情节密度。位置不同或不同赛道的稿本批不存在，不必考虑。

【纪律】
1. 先给每稿标出主要场景类型（环境／人物／对话／战斗／情感／过渡／日常）。
2. **先判档**：按判据里的三档标尺，给每稿判一个档（80／60／40），并写出依据（哪一条跨档差）。判档先于排序。
3. 文笔质感排序分两步，第一步是硬门槛，不许绕过：
   第一步——先扫一级红线，任一命中即进"红线组"：G18 工作标记（章节编号、项目名、状态、markdown 残留）、G16 生造词与文言残句、G17 成分缺（动词被省掉）、G22 假反转。
   **红线组一律排在非红线组之下**；红线组内部再互排。破折号（G45）不计入红线组，只在所属组内作为减分项。
   第二步——组内按"句子有没有增量"排：每一句是给出新信息或新画面，还是把已说过的意思换个说法重说一遍。重说多者排后。
3. 内容剧情／情绪节奏：先写 2 至 3 条带位置的证据再给序，不做加权求和；两维相反的稿单列，不许抹平。
4. 不许并列。

全部用 JSON，不要写别的话：
{{
 "场景标注":{{"稿一":"环境"}},
 "档位":[{{"稿":"稿一","档":"80／60／40","依据":"哪一条跨档差起的决定"}}],
 "红线栏":[{{"稿":"稿一","编号":"G18","位置":"原文片段","为什么":"一句话"}}],
 "文笔质感证据":[{{"稿":"稿一","位置":"行号或原文","证据":"一句话"}}],
 "内容剧情证据":[{{"稿":"稿一","位置":"","证据":""}}],
 "情绪节奏证据":[{{"稿":"稿一","位置":"","证据":""}}],
 "文笔质感":["稿一","稿二"],
 "内容剧情":["稿一","稿二"],
 "情绪节奏":["稿一","稿二"],
 "两维相反":["稿号"],
 "跨档倒挂":["按判据的分数标尺，指出被放错了档的稿；没有就写空数组"],
 "最稳的一稿":"稿号",
 "最差的一稿":"稿号"
}}

{body}"""


def load_env():
    env = {}
    for line in (SK / "scripts" / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def call(env, prompt, tag, out_dir, no_skip):
    path = out_dir / ("%s.json" % tag)
    if path.exists() and not no_skip:
        return "skip"
    body = {
        "model": env["MODELS"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": float(env.get("TEMPERATURE", 0)),
        "top_p": float(env.get("TOP_P", 1)),
        "max_tokens": int(env.get("MAX_TOKENS", 32000)),
    }
    for attempt in range(3):
        try:
            r = requests.post(
                env["BASE_URL"].rstrip("/") + "/chat/completions",
                headers={"Authorization": "Bearer %s" % env["DEEPSEEK_API_KEY"],
                         "Content-Type": "application/json"},
                json=body, timeout=900)
            r.raise_for_status()
            d = r.json()
            msg = d["choices"][0]
            content = msg["message"]["content"] or ""
            rec = {
                "tag": tag, "model": env["MODELS"],
                "finish_reason": msg.get("finish_reason"),
                "reasoning_tokens": (d.get("usage") or {}).get("completion_tokens_details", {}).get("reasoning_tokens"),
                "usage": d.get("usage"),
                "汉字数": len(HAN.findall(content)),
                "raw": content,
            }
            m = re.search(r"\{.*\}", content, re.S)
            rec["json"] = json.loads(m.group(0)) if m else None
            path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            if rec["finish_reason"] == "length" or rec["汉字数"] == 0:
                return "fail"
            return "ok"
        except Exception as e:                       # noqa: BLE001
            if attempt == 2:
                path.write_text(json.dumps({"tag": tag, "error": str(e)}, ensure_ascii=False, indent=2),
                                encoding="utf-8")
                return "error"
            time.sleep(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True,
                    choices=["judge", "round2", "rank", "fix", "para", "rebuild"])
    ap.add_argument("--round", default="1")
    ap.add_argument("--spec", help="第二批用：本章该写什么（一个文件，全批共用）；rebuild 模式用它")
    ap.add_argument("--id", help="fix／para／rebuild 用：素材 id（逗号分隔），直接取 素材/ 下的真身")
    ap.add_argument("--lines", help="para 模式用：要重写的起止行，如 11-15；不传则由模型自己判")
    ap.add_argument("--no-skip", action="store_true")
    args = ap.parse_args()

    env = load_env()
    crit = (SK / "references" / "判据摘要.md").read_text(encoding="utf-8")
    out_dir = ROOT / ("第%s轮" % args.round)
    out_dir.mkdir(parents=True, exist_ok=True)
    drafts = sorted([p for p in IN.glob("稿*.md")])

    if args.mode == "judge":
        tasks = [(p.stem, role, p) for p in drafts for role in ROLE_PROMPT]
        def run(t):
            code, role, p = t
            tpl = ROLE_PROMPT[role]
            head = tpl.format(criteria=crit) if role == "编辑" else tpl      # 读者与对手保持"素读"，不给判据
            prompt = "%s\n\n【正文】\n%s" % (head, p.read_text(encoding="utf-8"))
            return code, role, call(env, prompt, "%s__%s" % (code, role), out_dir, args.no_skip)
        with ThreadPoolExecutor(max_workers=int(env.get("CONCURRENCY", 4))) as ex:
            for code, role, st in ex.map(run, tasks):
                print("  %s %s → %s" % (code, role, st))
    elif args.mode == "round2":
        spec = Path(args.spec).read_text(encoding="utf-8") if args.spec else "（未提供）"
        def run(p):
            prompt = ROUND2_PROMPT.format(spec=spec, body=p.read_text(encoding="utf-8"))
            return p.stem, call(env, prompt, "%s__内容剧情二轮" % p.stem, out_dir, args.no_skip)
        with ThreadPoolExecutor(max_workers=int(env.get("CONCURRENCY", 4))) as ex:
            for code, st in ex.map(run, drafts):
                print("  %s 内容剧情二轮 → %s" % (code, st))
    elif args.mode in ("fix", "para", "rebuild"):
        want = [s.strip() for s in (args.id or "").split(",") if s.strip()]
        if not want:
            print("%s 模式要 --id，例：--id X-灰烬之主ch001" % args.mode)
            return
        byid = {}
        for line in (SK / "素材" / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                byid[r["id"]] = r
        spec = Path(args.spec).read_text(encoding="utf-8").rstrip() if args.spec else "（未提供）"
        seg = args.lines or ""
        def run(i):
            r = byid.get(i)
            if not r:
                return i, "notfound"
            body = (SK / r["路径"]).read_text(encoding="utf-8")
            if args.mode == "fix":
                prompt = "%s\n\n【正文】\n%s" % (ROLE_PROMPT["修正官"].format(criteria=crit), body)
                tag = "%s__修正官" % i
            elif args.mode == "para":
                prompt = PARA_PROMPT.format(criteria=crit, lines=seg or "由你判断最该重写的一段", body=body)
                tag = "%s__段落改写" % i
            else:
                prompt = REBUILD_PROMPT.format(criteria=crit, spec=spec, body=body)
                tag = "%s__重构" % i
            return i, call(env, prompt, tag, out_dir, args.no_skip)
        with ThreadPoolExecutor(max_workers=3) as ex:
            for i, st in ex.map(run, want):
                print("  %s %s → %s" % (i, args.mode, st))
    else:
        body = "\n\n".join("【%s】\n%s" % (p.stem, p.read_text(encoding="utf-8")) for p in drafts)
        st = call(env, RANK_PROMPT.format(criteria=crit, body=body), "排序官", out_dir, args.no_skip)
        print("  排序官 → %s" % st)
    print("输出 → %s" % out_dir)


if __name__ == "__main__":
    main()
