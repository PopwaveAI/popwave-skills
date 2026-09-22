#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拆书源文本预处理：分章归一、合并章节索引、切批、范围校验、token 估算。

这是确定性脚本，同一输入必须产出逐字节一致的输出，不引入任何随机或 AI 判断。

子命令：
  split          把整册 TXT 切成可寻址章节，产出 chapters/ 与章节索引
  batch          按档位切批，产出批次清单 JSON
  validate-scope 校验拆解配置的 scope 是否合法
  estimate       按字数估算 token 区间

示例：
  python split_book.py split book.txt -o out --name 某书 --author 某人
  python split_book.py batch out/合并章节索引.json --profile standard -o batches.json
  python split_book.py validate-scope out/合并章节索引.json config.json
  python split_book.py estimate out/合并章节索引.json --chapters 1 30
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

# 章节标题允许的最大长度（字符），超过视为正文误判而非标题。
MAX_TITLE_LEN = 80

# 中文 token 估算系数（每字符 token 数）的下限与上限。经验值，可覆盖。
# 中文文本 1 字符约 0.6~1.0 token。
TOKEN_PER_CHAR_MIN = 0.6
TOKEN_PER_CHAR_MAX = 1.0

# 试拆门槛：L1 门禁要求锚点池至少 20 章，范围小于此值属于试拆，需专用质量规则。
TRIAL_THRESHOLD = 20

# 切批档位 → 每批章数（含上限）。
PROFILES = {
    "standard": {"size": 30, "max": 40},
    "deep": {"size": 20, "max": 20},
    "skeleton": {"size": 40, "max": 40},
}

ARAB = r"[0-9０-９]+"
CN = r"[零一二三四五六七八九十百千万两]+"

# 卷/部/集 标题（一级边界，只认数字卷号，不含特殊章节标记）
VOLUME_TITLE_RE = re.compile(
    r"^\s*(?:#+\s*)?"
    r"(?:"
    r"第\s*(?:" + ARAB + r"|" + CN + r")\s*[卷部集]"
    r"|(?:" + ARAB + r")\s*[卷部集]"
    r"|卷\s*(?:" + ARAB + r")"
    r")"
    r"(?:\s*[:：]?\s*\S.*)?$"
)

# 章/回/节 标题（二级边界，含序章/楔子/尾声等特殊章节，不改卷号）
CHAPTER_TITLE_RE = re.compile(
    r"^\s*(?:#+\s*)?"
    r"(?:"
    r"第\s*(?:" + ARAB + r"|" + CN + r")\s*[章回节]"
    r"|(?:" + ARAB + r")\s*[章回节]"
    r"|Chapter\s+(?:" + ARAB + r")"
    r"|序章|楔子|引子|尾声|后记|番外"
    r")"
    r"(?:\s*[:：]?\s*\S.*)?$",
    re.IGNORECASE,
)

# 防盗/污染标记
ANTILEECH_RE = re.compile(r"\[ANTILEECH:[^\]]*\]")


def fail(msg: str) -> "NoReturn":  # type: ignore
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def detect_encoding(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        return "utf-16"
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass
    try:
        data.decode("gb18030")
        return "gb18030"
    except UnicodeDecodeError:
        pass
    return "gbk"


def read_text(path: Path) -> tuple[str, str]:
    """读文件并归一为 UTF-8 文本（LF 换行）。返回 (文本, 源编码)。"""
    data = path.read_bytes()
    enc = detect_encoding(data)
    try:
        text = data.decode(enc)
    except UnicodeDecodeError:
        text = data.decode(enc, errors="replace")
    # 归一换行
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text, enc


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def classify_line(line: str) -> str:
    """把一行归类为 volume / chapter / body。"""
    stripped = line.strip()
    if not stripped:
        return "blank"
    if len(stripped) > MAX_TITLE_LEN:
        return "body"
    if VOLUME_TITLE_RE.match(line):
        return "volume"
    if CHAPTER_TITLE_RE.match(line):
        return "chapter"
    return "body"


def split_book(input_path: Path, output_dir: Path, name: str, author: str, source: str) -> dict:
    """分章归一。返回合并章节索引 dict。"""
    text, enc = read_text(input_path)
    lines = text.split("\n")

    chapters: list[dict] = []  # 中间态，每条含 title / body_lines / volume_no
    cur_title = None
    cur_body: list[str] = []
    cur_volume = 0  # 0 = 尚未进入任何卷
    volume_names: dict[int, str] = {}

    def flush():
        nonlocal cur_title, cur_body, cur_volume
        if cur_title is None:
            cur_body = []
            return
        if cur_volume == 0:
            cur_volume = 1  # 无卷标题时归默认卷 1
        chapters.append({"title": cur_title, "body": cur_body, "volume": cur_volume})
        cur_title = None
        cur_body = []

    for i, line in enumerate(lines):
        kind = classify_line(line)
        if kind == "volume":
            flush()
            vname = line.strip().lstrip("#").strip()
            cur_volume += 1
            volume_names[cur_volume] = vname
            cur_title = None
            cur_body = []
        elif kind == "chapter":
            flush()
            cur_title = line.strip()
            cur_body = []
        else:
            cur_body.append(line)

    flush()

    if not chapters:
        fail(
            "未识别到任何章节标题。本脚本只处理带明确标题（第X章/回/节、Chapter X）的文本，"
            "连续无标题文本需要人工或 AI 切分，不能自动分章。"
        )

    # 写章节文件与单卷索引
    chapters_dir = output_dir / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    vol_idx_dir = output_dir / "章节索引"
    vol_idx_dir.mkdir(parents=True, exist_ok=True)

    index_chapters: list[dict] = []
    vol_groups: dict[int, list[int]] = {}

    for global_no, ch in enumerate(chapters, start=1):
        vno = ch["volume"]
        vol_groups.setdefault(vno, []).append(global_no)

        body_text = "\n".join(ch["body"]).rstrip("\n")
        full_text = ch["title"] + "\n\n" + body_text if body_text else ch["title"]
        # 章节级防盗标记检测与去标记字数
        has_leech = ANTILEECH_RE.search(body_text) is not None
        clean_body = ANTILEECH_RE.sub("", body_text)
        char_count = len(clean_body)

        fn = f"ch{global_no:04d}.txt"
        (chapters_dir / fn).write_text(full_text + "\n", encoding="utf-8")

        flags = []
        if has_leech:
            flags.append("antileech")

        index_chapters.append({
            "no": global_no,
            "globalNo": global_no,
            "volumeNo": vno,
            "volumeLocalNo": 0,  # 卷内序号稍后回填
            "title": ch["title"],
            "file": fn,
            "chars": char_count,
            "flags": flags,
        })

    # 卷内序号回填 + 卷信息
    vol_list: list[dict] = []
    vol_counter = 0
    for vno in sorted(vol_groups.keys()):
        vol_counter += 1
        ch_nos = vol_groups[vno]
        for c in index_chapters:
            if c["volumeNo"] == vno:
                c["volumeLocalNo"] = c["globalNo"] - ch_nos[0] + 1
        vol_list.append({
            "no": vno,
            "name": volume_names.get(vno, f"第{vno}卷"),
            "from": ch_nos[0],
            "to": ch_nos[-1],
        })
        # 写单卷索引
        vol_chapters = [
            {
                "no": c["globalNo"] - ch_nos[0] + 1,
                "globalNo": c["globalNo"],
                "title": c["title"],
                "file": c["file"],
                "chars": c["chars"],
                "flags": c["flags"],
            }
            for c in index_chapters if c["volumeNo"] == vno
        ]
        (vol_idx_dir / f"asset-{vno:03d}.json").write_text(
            json.dumps({
                "schemaVersion": SCHEMA_VERSION,
                "assetId": f"asset-{vno:03d}",
                "volumeNo": vno,
                "chapterCount": len(vol_chapters),
                "chapters": vol_chapters,
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    total_chars = sum(c["chars"] for c in index_chapters)

    # 质量检测：缺失/重复（按标题内嵌数字 vs 分章序号）
    quality = detect_quality(index_chapters)

    book = {
        "schemaVersion": SCHEMA_VERSION,
        "name": name or input_path.stem,
        "author": author,
        "source": source,
        "inputFile": str(input_path),
        "inputEncoding": enc,
        "fingerprint": sha256_of(input_path),
        "totalChars": total_chars,
        "totalChapters": len(index_chapters),
        "volumeCount": len(vol_list),
        "splitMethod": "title-regex",
        "splitAt": datetime.now(timezone.utc).isoformat(),
    }

    merged = {
        "schemaVersion": SCHEMA_VERSION,
        "book": book,
        "assets": [
            {
                "id": f"asset-{v:03d}",
                "fileName": input_path.name,
                "fingerprint": book["fingerprint"],
                "order": i + 1,
                "volumeNo": v,
                "chapterCount": (vlist[-1] - vlist[0] + 1) if vlist else 0,
                "chapterIndexFile": f"章节索引/asset-{v:03d}.json",
            }
            for i, (v, vlist) in enumerate(sorted(vol_groups.items()))
        ],
        "totalChapters": len(index_chapters),
        "volumes": vol_list,
        "chapters": index_chapters,
        "quality": quality,
        "splitMethod": "title-regex",
    }

    # 写合并章节索引与 book.json
    (output_dir / "book.json").write_text(
        json.dumps(book, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "合并章节索引.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    return merged


def parse_title_number(title: str) -> int | None:
    """从标题里尽量提取数字序号（仅用于质量检测的辅助信号）。"""
    m = re.search(r"第\s*([0-9０-９]+|[零一二三四五六七八九十百千万两]+)\s*[章回节]", title)
    if not m:
        m = re.search(r"([0-9０-９]+)\s*[章回节]", title)
    if not m:
        return None
    raw = m.group(1)
    try:
        return int(raw)
    except ValueError:
        return cn_to_int(raw)


def cn_to_int(s: str) -> int:
    digits = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    units = {"十": 10, "百": 100, "千": 1000, "万": 10000}
    total = 0
    section = 0
    num = 0
    for ch in s:
        if ch in digits:
            num = digits[ch]
        elif ch in units:
            u = units[ch]
            if u >= 10000:
                section = (section + num) * u
                total += section
                section = 0
            else:
                section += (num if num else 1) * u
            num = 0
        else:
            return None
    return total + section + num


def detect_quality(chapters: list[dict]) -> dict:
    """按标题内嵌序号做连续性检测，产出质量标记。"""
    missing = []
    duplicated = []
    seen: dict[int, int] = {}
    for c in chapters:
        n = parse_title_number(c["title"])
        if n is None:
            continue
        if n in seen:
            duplicated.append({"titleNo": n, "globalNo": c["globalNo"], "title": c["title"]})
        else:
            seen[n] = c["globalNo"]

    nums = sorted(seen.keys())
    for a, b in zip(nums, nums[1:]):
        gap = b - a
        if gap > 1:
            for missing_no in range(a + 1, b):
                missing.append(missing_no)

    return {
        "missing": missing,
        "duplicated": duplicated,
        "truncated": [],
        "contamination": [c["globalNo"] for c in chapters if "antileech" in c["flags"]],
    }


def load_index(path: Path) -> dict:
    if not path.exists():
        fail(f"索引文件不存在：{path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_json_file(path: Path) -> dict:
    if not path.exists():
        fail(f"文件不存在：{path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def resolve_scope(index: dict, scope: dict) -> tuple[int, int, str]:
    """把 scope 解析为 (from, to, 描述)。from/to 为全书序号，含端点。"""
    total = index["totalChapters"]
    stype = scope.get("type", "full")
    if stype == "full":
        return 1, total, "full"
    if stype == "volume":
        vno = scope.get("volumeNo")
        vol = next((v for v in index["volumes"] if v["no"] == vno), None)
        if vol is None:
            fail(f"scope.volumeNo={vno} 不存在于索引卷列表")
        return vol["from"], vol["to"], f"volume {vno}"
    if stype == "chapters":
        f = int(scope.get("from", 1))
        t = int(scope.get("to", total))
        if f < 1 or t > total or f > t:
            fail(f"scope.chapters from={f} to={t} 越界或非法（总章数 {total}）")
        return f, t, f"chapters {f}-{t}"
    fail(f"未知 scope.type={stype}")
    return 0, 0, ""  # unreachable


def cmd_batch(args):
    index = load_index(Path(args.index))
    profile = PROFILES.get(args.profile, PROFILES["standard"])
    size = profile["size"]

    if args.scope:
        scope = load_json_file(Path(args.scope))
    else:
        scope = {"type": "full"}
        if args.volume:
            scope = {"type": "volume", "volumeNo": int(args.volume)}
        elif args.chapters:
            scope = {"type": "chapters", "from": int(args.chapters[0]), "to": int(args.chapters[1])}

    frm, to, desc = resolve_scope(index, scope)

    # 取范围内章节，按卷分组切批（跨卷不合并）
    chapters = [c for c in index["chapters"] if frm <= c["globalNo"] <= to]
    batches = []
    vol_chs: dict[int, list[dict]] = {}
    for c in chapters:
        vol_chs.setdefault(c["volumeNo"], []).append(c)

    for vno in sorted(vol_chs.keys()):
        chs = vol_chs[vno]
        for i in range(0, len(chs), size):
            chunk = chs[i:i + size]
            first = chunk[0]["globalNo"]
            last = chunk[-1]["globalNo"]
            m = i // size + 1
            batches.append({
                "batchId": f"V{vno}_B{m}_ch{first:03d}-{last:03d}",
                "volumeNo": vno,
                "from": first,
                "to": last,
                "chapterCount": len(chunk),
                "chars": sum(c["chars"] for c in chunk),
            })

    out = {
        "schemaVersion": SCHEMA_VERSION,
        "profile": args.profile,
        "batchSize": size,
        "totalChapters": index["totalChapters"],
        "scope": {"type": scope["type"], "from": frm, "to": to},
        "scopeLabel": desc,
        "batches": batches,
        "batchCount": len(batches),
    }
    write_out(args.output, out)
    print(f"ok {len(batches)} batches (profile={args.profile}, size={size}, scope={desc})")


def cmd_validate_scope(args):
    index = load_index(Path(args.index))
    config = load_json_file(Path(args.config))
    scope = config.get("scope", {})
    frm, to, desc = resolve_scope(index, scope)
    chapter_count = to - frm + 1
    is_trial = chapter_count < TRIAL_THRESHOLD

    result = {
        "valid": True,
        "scope": {"type": scope.get("type", "full"), "from": frm, "to": to},
        "chapterCount": chapter_count,
        "isTrial": is_trial,
        "trialThreshold": TRIAL_THRESHOLD,
        "message": (
            f"范围合法：{desc}，共 {chapter_count} 章"
            + ("（低于 20 章，属于试拆，需专用质量规则）" if is_trial else "")
        ),
    }
    if args.output:
        write_out(Path(args.output), result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    # 试拆不视为错误，但用退出码 2 提示需要试拆规则
    sys.exit(2 if is_trial else 0)


def cmd_estimate(args):
    index = load_index(Path(args.index))
    scope = {"type": "full"}
    if args.volume:
        scope = {"type": "volume", "volumeNo": int(args.volume)}
    elif args.chapters:
        scope = {"type": "chapters", "from": int(args.chapters[0]), "to": int(args.chapters[1])}
    frm, to, desc = resolve_scope(index, scope)
    chapters = [c for c in index["chapters"] if frm <= c["globalNo"] <= to]
    total_chars = sum(c["chars"] for c in chapters)

    lo = args.ratio[0] if args.ratio else TOKEN_PER_CHAR_MIN
    hi = args.ratio[1] if args.ratio else TOKEN_PER_CHAR_MAX

    out = {
        "schemaVersion": SCHEMA_VERSION,
        "scope": {"type": scope["type"], "from": frm, "to": to},
        "scopeLabel": desc,
        "chapterCount": len(chapters),
        "totalChars": total_chars,
        "ratio": {"min": lo, "max": hi},
        "estimatedTokens": {"min": int(total_chars * lo), "max": int(total_chars * hi)},
    }
    write_out(args.output, out)
    print(
        f"ok {len(chapters)} chapters, {total_chars} chars, "
        f"~{int(total_chars * lo)}-{int(total_chars * hi)} tokens ({desc})"
    )


def write_out(path, data: dict):
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    else:
        print(text)


def main():
    parser = argparse.ArgumentParser(description="拆书源文本预处理脚本")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_split = sub.add_parser("split", help="分章归一")
    p_split.add_argument("input", help="整册 TXT 路径")
    p_split.add_argument("-o", "--output", required=True, help="输出目录")
    p_split.add_argument("--name", default="", help="书名")
    p_split.add_argument("--author", default="", help="作者")
    p_split.add_argument("--source", default="", help="来源 URL")
    p_split.set_defaults(func=lambda a: split_book(Path(a.input), Path(a.output), a.name, a.author, a.source))

    p_batch = sub.add_parser("batch", help="切批")
    p_batch.add_argument("index", help="合并章节索引.json 路径")
    p_batch.add_argument("--profile", choices=list(PROFILES), default="standard", help="切批档位")
    p_batch.add_argument("--scope", help="scope JSON 文件（优先于 --volume/--chapters）")
    p_batch.add_argument("--volume", help="按卷切批（卷号）")
    p_batch.add_argument("--chapters", nargs=2, type=int, metavar=("FROM", "TO"), help="按章范围切批")
    p_batch.add_argument("-o", "--output", required=True, help="批次清单输出 JSON")
    p_batch.set_defaults(func=cmd_batch)

    p_val = sub.add_parser("validate-scope", help="校验范围配置")
    p_val.add_argument("index", help="合并章节索引.json 路径")
    p_val.add_argument("config", help="拆解配置.json 路径")
    p_val.add_argument("-o", "--output", help="结果输出 JSON（默认打印）")
    p_val.set_defaults(func=cmd_validate_scope)

    p_est = sub.add_parser("estimate", help="token 估算")
    p_est.add_argument("index", help="合并章节索引.json 路径")
    p_est.add_argument("--volume", help="按卷估算（卷号）")
    p_est.add_argument("--chapters", nargs=2, type=int, metavar=("FROM", "TO"), help="按章范围估算")
    p_est.add_argument("--ratio", nargs=2, type=float, metavar=("MIN", "MAX"), help="每字符 token 系数区间")
    p_est.add_argument("-o", "--output", required=True, help="估算输出 JSON")
    p_est.set_defaults(func=cmd_estimate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
