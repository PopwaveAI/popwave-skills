#!/usr/bin/env node
/**
 * analyze_metrics.mjs — 降AI 指标统计脚本（v2.0 Node 版）
 * Popwave 标准运行时为 Node.js（openclaw-runtime 自带），替代 Python 版 analyze_metrics.py。
 * 逻辑与 Python 版 1:1，口径一致。禁止 agent 运行时自写脚本，统一用本脚本。
 *
 * 用法:
 *   模式1 单文件/多文件指标:
 *     node analyze_metrics.mjs <文件路径> [更多文件路径...]
 *   模式2 区间字数统计（报告段落分层明细用）:
 *     node analyze_metrics.mjs --zones <原文路径> <改后路径> <区间定义>
 *     区间定义格式: 名称:起始段-结束段,名称:起始段-结束段,...（段落按改后文件的非空行计，1-based）
 *     示例: node analyze_metrics.mjs --zones orig.txt new.txt "A:1-3,B:4-6,L3区:7-9"
 *
 * 输出: JSON（stdout）
 *   模式1: [{file, chars, paras, sents, len_dist, max_streak, streak_sents,
 *            short5, long50, max_single_para_run, dashes, dash_per_100,
 *            ascii_punct, not_but, first20, last20}]
 *   模式2: {zones:[{name,paras,orig_chars,new_chars,ratio}], total:{orig_chars,new_chars,ratio},
 *           orig_paras, new_paras}
 */
import { readFileSync } from "node:fs";

function readText(path) {
  return readFileSync(path, "utf-8");
}

function stripTitle(text) {
  const lines = text.split("\n");
  if (lines.length > 0 && lines[0].trim() && lines[0].trim().length < 30 && !lines[0].includes("。")) {
    return lines.slice(1).join("\n").trim();
  }
  return text.trim();
}

function metrics(path) {
  const raw = readText(path);
  const text = stripTitle(raw);
  // 字符统计（去空白：\s 含中文全角空格 \u3000）
  const chars = text.replace(/\s+/g, "").length;
  // 段落（按空行）
  const paras = text.split("\n\n").map((p) => p.trim()).filter((p) => p.length > 0);
  // 句子（按 。！？； 切分；省略号 … 统一为 \u2026，不算切分）
  const seg = text.replace(/…/g, "\u2026");
  const parts = seg.split(/[。！？；]/);
  const sents = parts.map((p) => p.trim()).filter((p) => p.length > 0);
  const lens = sents.map((s) => s.replace(/\s+/g, "").length);
  // 句长分布
  const dist = { "<=5": 0, "6-14": 0, "15-25": 0, "26-35": 0, "36-49": 0, ">=50": 0 };
  for (const l of lens) {
    if (l <= 5) dist["<=5"]++;
    else if (l <= 14) dist["6-14"]++;
    else if (l <= 25) dist["15-25"]++;
    else if (l <= 35) dist["26-35"]++;
    else if (l <= 49) dist["36-49"]++;
    else dist[">=50"]++;
  }
  // 15-25 连击
  let maxStreak = 0, cur = 0, streakStart = null;
  const streakSents = [];
  for (let i = 0; i < lens.length; i++) {
    const l = lens[i];
    if (l >= 15 && l <= 25) {
      if (cur === 0) streakStart = i;
      cur++;
      if (cur > maxStreak) maxStreak = cur;
      if (cur >= 3) {
        if (streakSents.length > 0 && streakSents[streakSents.length - 1].start === streakStart) {
          streakSents[streakSents.length - 1] = { start: streakStart, end: i, n: cur };
        } else {
          streakSents.push({ start: streakStart, end: i, n: cur });
        }
      }
    } else {
      cur = 0;
      streakStart = null;
    }
  }
  // 连续单句段
  const paraSentCounts = paras.map((p) => (p.match(/[。！？；]/g) || []).length);
  let maxSingleParaRun = 0, curSingle = 0;
  for (const c of paraSentCounts) {
    if (c === 1) {
      curSingle++;
      if (curSingle > maxSingleParaRun) maxSingleParaRun = curSingle;
    } else {
      curSingle = 0;
    }
  }
  // 表层字符
  const dashes = (raw.match(/——/g) || []).length;
  const asciiPunct = (text.match(/["',.!?;:\-]/g) || []).length;
  const notBut =
    (text.match(/不是[^。！？；]{0,20}而是/g) || []).length +
    (text.match(/不是[^。！？；]{0,15}[，,]是/g) || []).length;
  const linesNz = raw.split("\n").filter((l) => l.trim().length > 0);
  const first20 = linesNz.length > 0 ? linesNz[0].slice(0, 20) : "";
  const last20 = linesNz.length > 0 ? linesNz[linesNz.length - 1].slice(-20) : "";
  return {
    file: path,
    chars,
    paras: paras.length,
    sents: sents.length,
    len_dist: dist,
    max_streak: maxStreak,
    streak_sents: streakSents,
    short5: dist["<=5"],
    long50: dist[">=50"],
    max_single_para_run: maxSingleParaRun,
    dashes,
    dash_per_100: Math.round((dashes * 100) / Math.max(chars, 1) * 1000) / 1000,
    ascii_punct: asciiPunct,
    not_but: notBut,
    first20,
    last20,
  };
}

function zonesStats(origPath, newPath, zonesDef) {
  function parasOf(path) {
    const raw = readText(path);
    const lines = raw.split("\n");
    let bodyLines;
    if (lines.length > 0 && lines[0].trim() && lines[0].trim().length < 30 && !lines[0].includes("。")) {
      bodyLines = lines.slice(1);
    } else {
      bodyLines = lines;
    }
    // 按非空行计段（与报告"段落分层明细"口径一致：每非空行 = 一段）
    return bodyLines.map((l) => l.replace(/\s+/g, "")).filter((p) => p.length > 0);
  }
  const orig = parasOf(origPath);
  const new_ = parasOf(newPath);
  const zones = [];
  for (const seg of zonesDef.split(",").map((s) => s.trim()).filter((s) => s.length > 0)) {
    const [name, rng] = seg.split(":");
    const [a, b] = rng.split("-").map(Number);
    zones.push({ name, a, b });
  }
  const out = [];
  let totO = 0, totN = 0;
  for (const { name, a, b } of zones) {
    const o = orig.slice(a - 1, b).reduce((s, p) => s + p.length, 0);
    const n = new_.slice(a - 1, b).reduce((s, p) => s + p.length, 0);
    totO += o;
    totN += n;
    out.push({ name, paras: `${a}-${b}`, orig_chars: o, new_chars: n, ratio: Math.round((n / Math.max(o, 1)) * 100) / 100 });
  }
  return {
    zones: out,
    total: { orig_chars: totO, new_chars: totN, ratio: Math.round((totN / Math.max(totO, 1)) * 100) / 100 },
    orig_paras: orig.length,
    new_paras: new_.length,
  };
}

const argv = process.argv.slice(2);
if (argv.length < 1) {
  console.error("用法: node analyze_metrics.mjs <文件> [更多...] 或 --zones <原文> <改后> <区间>");
  process.exit(1);
}
if (argv[0] === "--zones") {
  if (argv.length !== 4) {
    console.error("--zones 需要: <原文路径> <改后路径> <区间定义>");
    process.exit(2);
  }
  console.log(JSON.stringify(zonesStats(argv[1], argv[2], argv[3]), null, 2));
} else {
  const results = argv.map((p) => metrics(p));
  console.log(JSON.stringify(results, null, 2));
}
