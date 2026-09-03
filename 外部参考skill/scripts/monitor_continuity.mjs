#!/usr/bin/env node
/**
 * monitor_continuity.mjs
 * 网文长线连贯性 · 确定性监控脚本 v1.0
 *
 * 作用：对《拆解昨日书》这类扁平结构项目（无白描卡/状态快照，只有正文+章文件）
 * 在纯文本层面自动抓"可确定性"的跨章走偏信号。不做语义判断。
 *
 * 用法：node monitor_continuity.mjs [扫描目录] [输出报告.md]
 */
import { readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const dir = process.argv[2] || 'D:\\拆解昨日书\\卷一';
const outFile = process.argv[3] || 'D:\\拆解昨日书\\脚本监控_跨章连贯_20260903.md';

const HAN = /[\u4e00-\u9fa5]/;
// 只保留汉字+阿拉伯数字，其余（标点/空白/英文/emoji）丢弃，用于 n-gram 短语检测
const clean = (s) => s.replace(/[^\u4e00-\u9fa50-9]/g, '');
const isHan = (c) => HAN.test(c);

async function main() {
  const files = (await readdir(dir)).filter((f) => /^第?章节?/.test(f) || /\.md$/i.test(f));
  const records = [];
  for (const f of files) {
    const p = path.join(dir, f);
    let s;
    try { s = await readFile(p, 'utf8'); } catch (e) { continue; }
    const m = f.match(/第\s*(\d+)\s*章/);
    const no = m ? parseInt(m[1], 10) : null;
    // 去掉 markdown 标题行，只留正文
    const lines = s.split(/\r?\n/).filter((l) => !/^\s*#{1,3}\s/.test(l));
    const body = lines.join('\n');
    const titleLine = (s.split(/\r?\n/)[0] || '').replace(/^\s*#+\s*/, '').trim();
    records.push({ file: f, no, titleLine, body, hanCount: clean(body).length });
  }
  records.sort((a, b) => a.no - b.no);
  const valid = records.filter((r) => r.no != null);

  const L = [];
  const h1 = `# 跨章连贯性 · 确定性脚本监控报告
> 扫描目录：\`${dir}\` ｜ 日期：2026-09-03 ｜ 引擎：monitor_continuity.mjs v1.0
> 扫描到 ${valid.length} 章（${records.length - valid.length} 个文件未解析章号，已跳过）。
> 定位：只抓**可确定性**信号（重复描写/称谓/结构/实体追踪）；语义级走偏见文末"脚本够不到"清单。`;
  L.push(h1, '');

  // ============ D1 结构审计 ============
  L.push('## D1 章节结构审计（序号/字数）', '');
  const numbers = valid.map((r) => r.no);
  const missing = [];
  for (let i = 1; i <= Math.max(...numbers); i++) if (!numbers.includes(i)) missing.push(i);
  L.push(`- 章序：${numbers.length} 章，缺章号：${missing.length ? missing.join(',') : '无'}（计数基于文件名，若文件本身标错会误报，需人工核）`);
  L.push(`- 字数异常（纯汉字 <1200 或 >9000，或为 0）：`);
  const wordAnoms = valid.filter((r) => r.hanCount < 1200 || r.hanCount > 9000 || r.hanCount === 0);
  if (!wordAnoms.length) L.push('  - 无');
  else for (const r of wordAnoms) L.push(`  - ch${String(r.no).padStart(3, '0')} 字数=${r.hanCount}`);
  L.push('');

  // ============ D2 跨章固定短语复用（n-gram）============
  function ngramMap(n) {
    const g = new Map(); // phrase -> {chs:Set, total:0}
    for (const r of valid) {
      const t = clean(r.body);
      for (let i = 0; i + n <= t.length; i++) {
        const sub = t.slice(i, i + n);
        if (!isHan(sub[0]) || !isHan(sub[n - 1])) continue;
        let o = g.get(sub);
        if (!o) { o = { chs: new Set(), total: 0 }; g.set(sub, o); }
        o.chs.add(r.no);
        o.total++;
      }
    }
    return g;
  }

  L.push('## D2 跨章固定短语复用检测（同一长短语在 ≥4 个不同章出现 = 描写/称谓重复的强信号）', '');
  const g8 = ngramMap(8);
  const longReuse = [...g8.entries()]
    .filter(([, o]) => o.chs.size >= 4)
    .map(([ph, o]) => ({ ph, chs: o.chs.size, total: o.total }))
    .sort((a, b) => b.chs - a.chs || b.total - a.total)
    .slice(0, 40);
  if (!longReuse.length) L.push('- 未检出 ≥4 章的 8 字固定短语复用');
  else {
    L.push('| 复用短语(8字) | 跨章数 | 总出现 |');
    L.push('|---|---|---|');
    for (const x of longReuse) L.push(`| ${x.ph} | ${x.chs} | ${x.total} |`);
    L.push('');
    L.push('### 明细：每个复现短语命中哪些章');
    for (const x of longReuse.slice(0, 12)) {
      const hits = g8.get(x.ph).chs;
      L.push(`- \`${x.ph}\`【跨${x.chs}章·共${x.total}次】→ 章 ${[...hits].sort((a, b) => a - b).join(', ')}`);
    }
  }
  L.push('');

  // 章内自重复：同一 8 字短语在同章内 ≥3 次
  L.push('### 章内重复描写（同一 8 字短语在同章 ≥3 次）');
  const intra = [];
  for (const r of valid) {
    const t = clean(r.body);
    const m = new Map();
    for (let i = 0; i + 8 <= t.length; i++) {
      const sub = t.slice(i, i + 8);
      if (sub.length < 8) continue;
      m.set(sub, (m.get(sub) || 0) + 1);
    }
    for (const [ph, c] of m) if (c >= 3) intra.push({ no: r.no, ph, c });
  }
  if (!intra.length) L.push('- 无');
  else for (const x of intra) L.push(`- ch${String(x.no).padStart(3, '0')}：\`${x.ph}\` ×${x.c}`);
  L.push('');

  // ============ D3 实体/固定描写追踪（种子词/短语出现频次表）============
  L.push('## D3 实体·固定描写追踪（种子词跨章出现频次与命中章）', '');
  L.push('> 种子来源：从已有问题清单与正文高频物提炼。纵**看频次是否异常**（固定描写应低频，正文物高频正常但需人工留意横跳）。命中数=出现该子串的章节数。');
  const seeds = [
    '伞尖点地', '手办安安静静', '铁盒', '手腕上的疤', '录音', '别听',
    '山药排骨汤', '断桥', '等风来', '月亮', '云梦泽', '游雪',
  ];
  L.push('| 种子 | 命中章数 | 总出现 | 命中章列表(前12) |');
  L.push('|---|---|---|---|');
  for (const seed of seeds) {
    const hits = new Map();
    for (const r of valid) {
      const c = (r.body.match(new RegExp(seed.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
      if (c) hits.set(r.no, c);
    }
    const chs = [...hits.keys()].sort((a, b) => a - b);
    if (!chs.length) continue;
    const list = chs.slice(0, 12).map((n) => n).join(',');
    L.push(`| ${seed} | ${hits.size} | ${[...hits.values()].reduce((a, b) => a + b, 0)} | ${list}${chs.length > 12 ? '…' : ''} |`);
  }
  L.push('');

  // ============ D4 章首-章末"物质状态"粗探  ============
  L.push('## D4 章内实体词出现密度（物质追踪辅助）', '');
  L.push('- 说明：真正的手办/录音位置"横跳"需语义，本脚本只给出现密度供人工/agent 精审。');
  L.push('');

  // ============ 脚本够不到的边界 ============
  L.push('## 脚本够不到的（需 review/agent 语义审核）', '');
  L.push('- **人物关系/口吻不稳定**：情绪、对白 persona 漂移、OOC —— 规则判不了。');
  L.push('- **设定"同物不同说法"**（同上个疤来源=手术 vs 搬家磕）：需要把多说法对齐，非纯文本可解。');
  L.push('- **时间口径矛盾**（"这个月第三次" / 决赛月末口径）：需据细纲时间轴人工。');
  L.push('- **决心/钩子未回收**（"明天一定要听""查他爸的事"无下文）：需"承诺账本"才可脚本化，本项目无。');
  L.push('- **主线是否在推进、是否水章**：叙事级，脚本判不了。');
  L.push('');
  L.push('---');
  L.push('> 报告由脚本自动生成。请与 pop(主Agent精读)+ 跨章状态机比对 的结论交叉验证，脚本负责**确定性部分、缩小人工/agent 精读范围**。');

  await writeFile(outFile, L.join('\n'), 'utf8');
  console.log(`报告已写出：${outFile}`);

  // ============ D5 终端摘要 ============
  console.log(`\n[摘要] 扫描 ${valid.length} 章`);
  if (missing.length) console.log(`  结构缺失：缺章 ${missing.join(',')}`);
  console.log(`  长固定短语复用(≥4章×8字)：${longReuse.length} 条`);
  console.log(`  章内重复描写：${intra.length} 条`);
  const hi = [...seeds].map((s) => {
    let tot = 0; for (const r of valid) tot += (r.body.split(s).length - 1); return [s, tot];
  }).filter(([, t]) => t >= 5).sort((a, b) => b[1] - a[1]);
  if (hi.length) console.log(`  高频种子词(≥5次)：${hi.map(([s, t]) => `${s}×${t}`).join('  ')}`);
}

main().catch((e) => { console.error(e); process.exit(1); });