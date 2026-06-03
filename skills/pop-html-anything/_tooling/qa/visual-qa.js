/**
 * qa/visual-qa.js — HTML 视觉 QA 编排器
 *
 * 职责：
 *   1. 接收生成的 HTML 文件列表
 *   2. 用 Puppeteer 截图
 *   3. 发送截图到 Kimi K2.5 做视觉评估
 *   4. 输出可视化 + 可读的 QA 报告
 *
 * 用法（CLI）：
 *   node qa/visual-qa.js <html文件1> [<html文件2> ...]
 *   node qa/visual-qa.js output/百科数据-abyss-blood-red.html  # 单文件
 *   node qa/visual-qa.js output/  # 整个 output 目录
 *
 * 用法（API）：
 *   const { runQA, runOnOutputDir } = require('./qa/visual-qa.js');
 *   const report = await runOnOutputDir();
 *   console.log(report.summary);
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const puppeteer = require('puppeteer');
const { analyzeBatch, QA_CONFIG } = require('./kimi-client.js');
const { extractPatches, generateManifest, saveManifest } = require('./issue-parser.js');

// ─── Chrome 路径查找 ────────────────────────────────────────
// 优先级：1. 本地 chrome/ 目录  2. 用户 cache（npx install 后的位置）
function findChrome() {
  // 尝试本地目录
  const localDir = path.join(__dirname, '..', 'chrome');
  if (fs.existsSync(localDir)) {
    try {
      const entries = fs.readdirSync(localDir);
      for (const entry of entries) {
        if (entry === '.metadata') continue;
        const exePath = path.join(localDir, entry, 'chrome-win64', 'chrome.exe');
        if (fs.existsSync(exePath)) return exePath;
      }
    } catch (e) { /* ignore */ }
  }
  // 尝试用户 cache
  const cachePaths = [
    path.join(os.homedir(), '.cache', 'puppeteer', 'chrome'),
    path.join(os.homedir(), 'AppData', 'Local', 'puppeteer', 'chrome'),
  ];
  for (const cacheDir of cachePaths) {
    if (fs.existsSync(cacheDir)) {
      try {
        const entries = fs.readdirSync(cacheDir);
        for (const entry of entries) {
          const exePath = path.join(cacheDir, entry, 'chrome-win64', 'chrome.exe');
          if (fs.existsSync(exePath)) return exePath;
        }
      } catch (e) { /* ignore */ }
    }
  }
  return null;
}
const CHROME_PATH = findChrome();

// ─── 骨架中文名映射（用于报告） ─────────────────────────────
const SKELETON_NAMES = {
  abyss: '深渊粒子', 'purple-orb': '紫色光晕', dossier: '档案线索板',
  social: '社交图谱', 'xianxia-sect': '仙侠宗派', 'family-tree': '家族谱系',
  'card-deck': '角色卡片集', 'status-board': '状态追踪看板',
  narrative: '叙事时间线', 'canvas-map': '画布世界地图',
  galaxy: '世界观星系图', 'd3-galaxy': 'D3星系图',
  scroll: '水墨卷轴', magazine: '杂志卡片',
};

function skeletonName(id) { return SKELETON_NAMES[id] || id; }

// ─── Puppeteer 截图 ──────────────────────────────────────────

async function screenshotHtml(htmlPath, opts = {}) {
  const {
    viewport = { width: 1440, height: 900 },
    waitMs = 2000,
  } = opts;

  if (!CHROME_PATH) {
    throw new Error(
      '找不到 Chrome 浏览器。Chrome 可能未安装或已从 `html-anything/chrome/` 移除。\n' +
      '如需安装，请运行: npx @puppeteer/browsers install chrome@stable\n' +
      '或手动指定 PUPPETEER_EXECUTABLE_PATH 环境变量。'
    );
  }

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: CHROME_PATH,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  }).catch(err => {
    throw new Error(
      `浏览器启动失败（版本可能不兼容）。\n` +
      `请运行: npx @puppeteer/browsers install chrome@stable\n` +
      `或运行: PUPPETEER_EXECUTABLE_PATH="${CHROME_PATH}" node skill-unified.js <数据.json> --qa\n` +
      `原始错误: ${err.message}`
    );
  });

  try {
    const page = await browser.newPage();
    await page.setViewport(viewport);

    // 打开本地 HTML 文件
    // 注意：不能用 networkidle0 — 粒子动画/ForecLayout会持续产生网络请求
    const fileUrl = 'file://' + path.resolve(htmlPath).replace(/\\/g, '/');
    await page.goto(fileUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

    // 等待 DOM 完全解析 + CSS/JS 执行
    await page.waitForFunction(() => document.readyState === 'complete', { timeout: 15000 });

    // 额外等待粒子渲染/D3布局等
    // Puppeteer v25 已移除 waitForTimeout
    await new Promise(r => setTimeout(r, waitMs));

    // 全页面截图
    const screenshotBuffer = await page.screenshot({
      fullPage: QA_CONFIG.SCREENSHOT.fullPage,
      type: QA_CONFIG.SCREENSHOT.type,
      quality: QA_CONFIG.SCREENSHOT.quality,
    });

    const base64 = screenshotBuffer.toString('base64');
    const mimeType = QA_CONFIG.SCREENSHOT.type === 'png' ? 'image/png' : 'image/jpeg';

    return { base64, mimeType, buffer: screenshotBuffer };

  } finally {
    await browser.close();
  }
}

// ─── 从文件名推断骨架 ID ──────────────────────────────────

function inferSkeletonId(filename) {
  // 基于已知骨架 ID 列表做精确匹配（解决 skeleton ID 和 palette ID 都含连字符的问题）
  const SKELETON_IDS = [
    'purple-orb', 'xianxia-sect', 'family-tree',
    'card-deck', 'status-board', 'canvas-map', 'd3-galaxy',
    'abyss', 'dossier', 'social', 'narrative', 'galaxy',
    'scroll', 'magazine',
  ];
  const baseName = path.basename(filename, '.html');
  for (const id of SKELETON_IDS) {
    // 匹配 -骨架ID- 或 骨架ID- 在文件名中的出现
    if (baseName.includes('-' + id) || baseName.startsWith(id)) {
      return id;
    }
  }
  const map = {
    '百科全书': 'abyss', '百科': 'abyss',
    '关系图谱': 'dossier', '图谱': 'dossier',
    '角色卡': 'card-deck', '状态看板': 'status-board', '看板': 'status-board',
    '时间线': 'narrative', '叙事': 'narrative',
    '星系': 'galaxy', '地图': 'canvas-map',
  };
  for (const [kw, id] of Object.entries(map)) {
    if (filename.includes(kw)) return id;
  }
  return 'unknown';
}

// ─── 核心 QA 编排 ──────────────────────────────────────────

/**
 * 对单个或多个 HTML 文件执行视觉 QA
 *
 * @param {string|string[]} htmlInputs - HTML 文件路径或 output 目录路径
 * @param {object} [opts]
 * @param {number} [opts.viewportWidth] - 截图宽度
 * @param {number} [opts.viewportHeight]
 * @param {number} [opts.waitMs] - 截图前等待时间（毫秒）
 * @param {function} [opts.onProgress] - 进度回调
 * @returns {Promise<object>} 报告对象
 */
async function runQA(htmlInputs, opts = {}) {
  const {
    viewportWidth = 1440,
    viewportHeight = 900,
    waitMs = 2000,
    onProgress,
  } = opts;

  // 1. 收集 HTML 文件
  const files = [];
  const inputs = Array.isArray(htmlInputs) ? htmlInputs : [htmlInputs];
  for (const input of inputs) {
    if (fs.statSync(input).isDirectory()) {
      const entries = fs.readdirSync(input)
        .filter(f => f.endsWith('.html'))
        .map(f => path.join(input, f));
      files.push(...entries);
    } else {
      files.push(input);
    }
  }

  if (files.length === 0) {
    return { success: false, error: '没有找到 HTML 文件', files: 0 };
  }

  console.log(`\n📸 视觉 QA 开始 — ${files.length} 个文件\n`);

  // 2. 逐文件截图
  const screenshots = [];
  for (let i = 0; i < files.length; i++) {
    const htmlPath = files[i];
    const fileName = path.basename(htmlPath);
    const skeletonId = inferSkeletonId(fileName);
    const msg = `  [${i + 1}/${files.length}] 截图: ${fileName}`;
    console.log(msg);
    if (onProgress) onProgress('screenshot', i + 1, files.length, fileName);

    try {
      const shot = await screenshotHtml(htmlPath, {
        viewport: { width: viewportWidth, height: viewportHeight },
        waitMs,
      });
      screenshots.push({ htmlPath, skeletonId, ...shot });
      console.log(`    ✓ ${(shot.buffer.length / 1024).toFixed(0)}KB`);
    } catch (err) {
      console.log(`    ✗ 截图失败: ${err.message}`);
    }
  }

  if (screenshots.length === 0) {
    return { success: false, error: '所有文件截图均失败', files: files.length };
  }

  // 3. 批量发送给 Kimi 评估
  let kimiProgress = '';
  const images = screenshots.map(s => ({
    htmlPath: s.htmlPath,
    skeletonId: s.skeletonId,
    base64: s.base64,
    mimeType: s.mimeType,
  }));

  console.log(`\n🔍 发送 ${images.length} 张截图给 Kimi K2.5 评估...\n`);
  if (onProgress) onProgress('analyze', 0, images.length, '');

  const evaluations = await analyzeBatch(images, (current, total, filePath) => {
    const name = path.basename(filePath || '');
    const msg = `  [${current}/${total}] Kimi 评估: ${name}`;
    kimiProgress = msg;
    console.log(msg);
    if (onProgress) onProgress('analyze', current, total, name);
  });

  // 4. 从 Kimi 回复中提取结构化修复指令
  console.log(`\n🔧 提取结构化修复指令...`);
  const manifests = [];
  for (const ev of evaluations) {
    const patches = extractPatches(ev.text);
    const fileName = path.basename(ev.htmlPath);
    const skeletonId = inferSkeletonId(fileName);
    const manifest = generateManifest(patches, {
      fromFile: fileName,
      skeletonId,
      score: ev.score,
    });
    manifests.push(manifest);
    if (patches.length > 0) {
      console.log(`  ${fileName}: ${patches.length} 个修复项 (P0:${manifest.p0_count} P1:${manifest.p1_count} P2:${manifest.p2_count})`);
    } else {
      console.log(`  ${fileName}: 无修复指令`);
    }
  }

  // 5. 保存修复清单
  const qaOutputDir = path.join(__dirname, '..', 'qa-output');
  const savedManifests = manifests.map(m => saveManifest(m, qaOutputDir));
  console.log(`\n📄 修复清单已保存 (${savedManifests.length} 个文件)`);

  // 6. 生成报告
  return generateReport(files, screenshots, evaluations, manifests);
}

// ─── 报告生成 ────────────────────────────────────────────────

function generateReport(files, screenshots, evaluations, manifests = []) {
  const timestamp = new Date().toISOString().replace(/T/, ' ').slice(0, 19);
  const avgScore = evaluations.length > 0
    ? (evaluations.reduce((s, e) => s + (e.score || 0), 0) / evaluations.length).toFixed(1)
    : 'N/A';

  const totalP0 = manifests.reduce((s, m) => s + m.p0_count, 0);
  const totalP1 = manifests.reduce((s, m) => s + m.p1_count, 0);

  const lines = [];
  lines.push('═══════════════════════════════════════════════════');
  lines.push('  HTML 视觉 QA 报告');
  lines.push('═══════════════════════════════════════════════════');
  lines.push(`  时间:      ${timestamp}`);
  lines.push(`  评估模型:  Kimi K2.5`);
  lines.push(`  总文件数:  ${files.length}`);
  lines.push(`  评估成功:  ${evaluations.length}`);
  lines.push(`  平均评分:  ${avgScore}` + (evaluations.length > 0 ? '/10' : ''));
  lines.push(`  需修复:    P0:${totalP0} 项 / P1:${totalP1} 项`);
  lines.push('');

  for (let idx = 0; idx < evaluations.length; idx++) {
    const ev = evaluations[idx];
    const fileName = path.basename(ev.htmlPath);
    const sId = inferSkeletonId(fileName);
    const sName = skeletonName(sId);
    const score = ev.score !== null ? `${ev.score}/10` : '未评分';
    const usageInfo = ev.usage?.total_tokens
      ? ` (${ev.usage.total_tokens} tokens)` : '';
    const mf = manifests[idx];

    lines.push(`── ${fileName} ──`);
    lines.push(`   骨架:   ${sName} (${sId})`);
    lines.push(`   评分:   ${score}${usageInfo}`);
    if (mf && mf.issues.length > 0) {
      lines.push(`   修复:   P0:${mf.p0_count}  P1:${mf.p1_count}  P2:${mf.p2_count}`);
      lines.push(`   清单:   qa-output/fix-manifest-${sId}.json`);
      for (const issue of mf.issues.slice(0, 3)) {
        lines.push(`     [${issue.priority}] ${issue.description}`);
      }
      if (mf.issues.length > 3) lines.push(`     ... +${mf.issues.length - 3} 项`);
    }
    lines.push('');
    lines.push(`   ${ev.text.replace(/\n/g, '\n   ')}`);
    if (idx < evaluations.length - 1) lines.push('');
  }

  lines.push('═══════════════════════════════════════════════════');
  lines.push('  报告结束');
  lines.push('═══════════════════════════════════════════════════');

  const textReport = lines.join('\n');

  // 结构化摘要
  const summary = {
    success: true,
    timestamp,
    model: 'Kimi K2.5',
    totalFiles: files.length,
    evaluated: evaluations.length,
    averageScore: avgScore,
    totalIssues: { p0: totalP0, p1: totalP1 },
    details: evaluations.map((ev, idx) => ({
      file: path.basename(ev.htmlPath),
      filePath: ev.htmlPath,
      skeletonId: inferSkeletonId(ev.htmlPath),
      skeletonName: skeletonName(inferSkeletonId(ev.htmlPath)),
      score: ev.score,
      evaluation: ev.text,
      issues: manifests[idx]?.issues || [],
      fixManifest: `qa-output/fix-manifest-${inferSkeletonId(ev.htmlPath)}.json`,
    })),
  };

  return { summary, textReport, evaluations, manifests };
}

// ─── 快捷：对 output/ 目录一键执行 ─────────────────────────

async function runOnOutputDir(opts = {}) {
  const outputDir = path.join(__dirname, '..', 'output');
  if (!fs.existsSync(outputDir)) {
    return { success: false, error: `output 目录不存在: ${outputDir}` };
  }
  return runQA(outputDir, opts);
}

// ─── CLI ─────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('用法:');
    console.log('  node qa/visual-qa.js <html文件> [<html文件2> ...]');
    console.log('  node qa/visual-qa.js output/        ← 评估 output 目录');
    process.exit(0);
  }

  (async () => {
    try {
      const report = await runQA(args);
      if (report.textReport) console.log('\n' + report.textReport);

      // 保存报告到 qa-output 目录
      const qaOutDir = path.join(__dirname, '..', 'qa-output');
      if (!fs.existsSync(qaOutDir)) fs.mkdirSync(qaOutDir, { recursive: true });

      if (report.textReport) {
        const reportPath = path.join(qaOutDir, 'qa-report.txt');
        fs.writeFileSync(reportPath, report.textReport, 'utf-8');
        console.log(`\n📄 报告已保存: ${reportPath}`);
      }

      // 保存 JSON 结构化报告（DeepSeek 可直接解析）
      if (report.summary) {
        const jsonPath = path.join(qaOutDir, 'qa-report.json');
        fs.writeFileSync(jsonPath, JSON.stringify(report.summary, null, 2), 'utf-8');
        console.log(`📄 结构化报告已保存: ${jsonPath}`);
      }
    } catch (err) {
      console.error('\n❌ QA 失败:', err.message);
      process.exit(1);
    }
  })();
}

module.exports = { runQA, runOnOutputDir, screenshotHtml, inferSkeletonId, QA_CONFIG };
