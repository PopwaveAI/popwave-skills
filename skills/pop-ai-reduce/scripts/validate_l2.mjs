#!/usr/bin/env node
/**
 * validate_l2.mjs — L2 轻量校验脚本（v2.0 Node 版）
 * Popwave 标准运行时为 Node.js（openclaw-runtime 自带），替代 Python 版 validate_l2.py。
 * 逻辑与 Python 版 1:1。禁止 agent 运行时自写脚本，统一用本脚本。
 *
 * 用法:
 *   node validate_l2.mjs <路径> <期望字节数> [首行前20字] [末行后20字] [更多文件...]
 *   期望值缺省或传 '-' 时不校验对应项。
 *
 * 输出: 每行 PASS/FAIL（附实际值），任一 FAIL 时 exit code 1。
 */
import { readFileSync, statSync } from "node:fs";

function check(path, expSize, expFirst, expLast) {
  const name = path.split(/[\\/]/).pop();
  let size = -1, first = null, last = null;
  try {
    size = statSync(path).size;
    const lines = readFileSync(path, "utf-8").split("\n");
    const nz = lines.filter((l) => l.trim().length > 0);
    first = nz.length > 0 ? nz[0].slice(0, 20) : "";
    last = nz.length > 0 ? nz[nz.length - 1].slice(-20) : "";
  } catch (e) {
    // 文件不存在，size 保持 -1
  }
  let ok = true;
  const issues = [];
  if (expSize && expSize !== "-" && size !== Number(expSize)) {
    ok = false;
    issues.push(`size=${size} 期望=${expSize}`);
  }
  if (expFirst && expFirst !== "-" && !(first !== null && first.includes(expFirst))) {
    ok = false;
    issues.push("首行不含期望片段");
  }
  if (expLast && expLast !== "-" && !(last !== null && last.includes(expLast))) {
    ok = false;
    issues.push("末行不含期望片段");
  }
  const status = ok ? "PASS" : "FAIL";
  console.log(`${status} ${name}: size=${size} first='${first}' last='${last}'` + (issues.length > 0 ? ` | ${issues.join("; ")}` : ""));
  return ok;
}

const args = process.argv.slice(2);
if (args.length < 1 || args.length % 4 !== 0) {
  console.error("用法: node validate_l2.mjs <路径> <期望字节数> <首行20字> <末行20字> [更多文件...]");
  process.exit(2);
}
let allOk = true;
for (let i = 0; i < args.length; i += 4) {
  if (!check(args[i], args[i + 1], args[i + 2], args[i + 3])) allOk = false;
}
process.exit(allOk ? 0 : 1);
