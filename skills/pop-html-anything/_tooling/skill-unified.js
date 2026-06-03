#!/usr/bin/env node
/**
 * skill-unified.js — Vibe Creating 统一入口
 *
 * 用法：
 *   node skill-unified.js <data.json>                 ← 自动检测 + 注入
 *   node skill-unified.js <data.json> --skeleton X    ← 强制骨架
 *   node skill-unified.js <data.json> --palette Y     ← 强制调色板
 *   node skill-unified.js <data.json> --qa            ← 注入后跑 QA
 *   node skill-unified.js <data.json> --output path   ← 指定输出路径
 *
 *   node skill-unified.js list                        ← 列出全部类型
 *   node skill-unified.js info <contentType>          ← 查看类型详情
 *
 * 示例：
 *   node skill-unified.js test-data/诡异人生/百科数据.json
 *   node skill-unified.js test-data/诡异人生/百科数据.json --skeleton abyss --palette blood-red --qa
 */

const fs = require('fs');
const path = require('path');

const { registry } = require('./shared/skill-registry.js');

// ─── 骨架中文名 ──────────────────────────────────────────────
const SKELETON_NAMES = {
  abyss: '深渊粒子', 'purple-orb': '紫色光晕',
  dossier: '档案线索板', social: '社交图谱', 'xianxia-sect': '仙侠宗派', 'family-tree': '家族谱系',
  'card-deck': '角色卡片集', 'status-board': '状态追踪看板',
  narrative: '叙事时间线',
  'canvas-map': '画布世界地图', galaxy: '世界观星系图', 'd3-galaxy': 'D3星系图',
};

function skeletonName(id) { return SKELETON_NAMES[id] || id; }

// ═══════════════════════════════════════════════════════════════
// 注入管线
// ═══════════════════════════════════════════════════════════════

function runInjectPipeline(dataPath, options = {}) {
  if (!fs.existsSync(dataPath)) {
    return { success: false, error: `数据文件不存在: ${dataPath}` };
  }

  let styleEngine;
  try {
    styleEngine = require('./core/style-engine.js');
  } catch (e) {
    return { success: false, error: `注入引擎加载失败: ${e.message}` };
  }

  const result = styleEngine.styleEngine.run(dataPath, {
    skeleton: options.skeleton,
    palette: options.palette,
    outputPath: options.output,
    genre: options.genre,
  });

  if (!result.success) {
    return { success: false, error: result.error };
  }

  return {
    success: true,
    pipeline: 'inject',
    outputPath: result.outputPath,
    contentType: result.contentType,
    skeleton: result.skeleton,
    skeletonName: skeletonName(result.skeleton),
    palette: result.palette,
    density: result.density,
    size: result.size,
    warnings: result.warnings,
  };
}

// ═══════════════════════════════════════════════════════════════
// Kimi 视觉 QA
// ═══════════════════════════════════════════════════════════════

async function runQA(htmlPath) {
  try {
    const qa = require('./qa/visual-qa.js');
    const result = await qa.runQA(htmlPath);
    return {
      success: true,
      score: result.summary?.averageScore || null,
      issueCount: result.summary?.totalIssues || { p0: 0, p1: 0 },
      reportPath: path.join(__dirname, 'qa-output', 'qa-report.txt'),
    };
  } catch (e) {
    return { success: false, error: `QA 失败: ${e.message}` };
  }
}

// ═══════════════════════════════════════════════════════════════
// CLI
// ═══════════════════════════════════════════════════════════════

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  // ── list ─────────────────────────────────────────────────
  if (cmd === 'list') {
    const all = registry.listAll();
    console.log('\n═══════════════════════════════════════════');
    console.log('  Vibe Creating — 骨架注册表');
    console.log(`  共 ${all.length} 个内容类型`);
    console.log('═══════════════════════════════════════════\n');
    for (const item of all) {
      const skeletons = registry.getSkeletons(item.id);
      const skList = skeletons.map(s => skeletonName(s.id)).join('、');
      console.log(`  ${item.id.padEnd(16)} ${item.name.padEnd(12)} ${item.skeletonCount}个骨架: ${skList}`);
    }
    console.log('\n用法: node skill-unified.js <data.json> [选项]');
    return;
  }

  // ── info ─────────────────────────────────────────────────
  if (cmd === 'info') {
    const typeId = args[1];
    if (!typeId) return console.log('用法: node skill-unified.js info <类型ID>');

    const match = registry.match(typeId);
    if (!match) return console.log(`未找到: "${typeId}"`);

    console.log('\n═══════════════════════════════════════════');
    console.log(`  内容类型: ${match.name}`);
    console.log('═══════════════════════════════════════════\n');
    console.log(`  ID:       ${match.contentType}`);
    const skeletons = registry.getSkeletons(match.contentType);
    for (const sk of skeletons) {
      console.log(`    ${sk.id.padEnd(16)} ${sk.name}`);
    }
    console.log(`\n用法: node skill-unified.js <${match.contentType}数据.json>`);
    return;
  }

  // ── 默认：执行注入 ──────────────────────────────────────
  if (!cmd || cmd.startsWith('-')) {
    console.log(`
用法:
  node skill-unified.js <data.json> [选项]
  node skill-unified.js list
  node skill-unified.js info <类型ID>

选项:
  --skeleton <ID>   强制指定骨架
  --palette <ID>    强制指定调色板
  --output <path>   指定输出路径
  --genre <名称>    强制指定小说类型（诡异/仙侠/甜宠等）
  --qa              生成后自动执行 Kimi K2.5 视觉 QA
`);
    return;
  }

  const dataPath = path.resolve(cmd);
  if (!fs.existsSync(dataPath)) {
    return console.error(`❌ 数据文件不存在: ${dataPath}`);
  }

  // 解析选项
  const options = {};
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--qa') { options.qa = true; continue; }
    if (args[i] === '--skeleton') { options.skeleton = args[++i]; continue; }
    if (args[i] === '--palette') { options.palette = args[++i]; continue; }
    if (args[i] === '--output') { options.output = args[++i]; continue; }
    if (args[i] === '--genre') { options.genre = args[++i]; continue; }
  }

  // 检测内容类型
  const raw = fs.readFileSync(dataPath, 'utf-8');
  let data;
  try { data = JSON.parse(raw); } catch (e) { data = { raw }; }

  const detected = registry.detect(data, { fileName: path.basename(dataPath) });
  if (!detected) {
    return console.error('❌ 无法检测内容类型。支持:\n' +
      registry.listAll().map(i => `    ${i.id}: ${i.name}`).join('\n'));
  }

  console.log(`\n🔍 检测到: ${detected.name}`);
  console.log(`   骨架: ${options.skeleton || '自动路由'}`);
  console.log(`   调色板: ${options.palette || '自动匹配'}\n`);

  const result = runInjectPipeline(dataPath, options);
  if (!result.success) {
    return console.error(`❌ 注入失败: ${result.error}`);
  }

  console.log(`✅ 生成成功`);
  console.log(`   输出: ${result.outputPath}`);
  console.log(`   骨架: ${result.skeletonName} (${result.skeleton})`);
  console.log(`   调色板: ${result.palette}`);
  console.log(`   密度: ${result.density}`);
  console.log(`   大小: ${result.size}`);

  if (result.warnings?.length > 0) {
    console.log(`\n⚠️  警告:`);
    result.warnings.forEach(w => console.log(`  ${w}`));
  }

  // 可选 QA
  if (options.qa && result.outputPath) {
    console.log(`\n🔍 执行 Kimi K2.5 视觉 QA...`);
    const qaResult = await runQA(result.outputPath);
    if (qaResult.success) {
      console.log(`   评分: ${qaResult.score}/10`);
      console.log(`   需修复: P0:${qaResult.issueCount.p0}  P1:${qaResult.issueCount.p1}`);
      console.log(`   报告: ${qaResult.reportPath}`);
    } else {
      console.log(`   QA 失败: ${qaResult.error}`);
    }
  }

  console.log(`\n📎 打开文件查看效果:`);
  console.log(`   ${result.outputPath}`);
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
