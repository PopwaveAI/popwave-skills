/**
 * qa/issue-parser.js — 从 Kimi 回复中提取结构化修复指令
 *
 * Kimi K2.5 的回复格式：文字分析 + JSON 块（含 patches）
 * 这个文件负责：提取 JSON → 验证 → 生成 DeepSeek 可读的修复清单
 *
 * 用法：
 *   const { extractPatches } = require('./issue-parser.js');
 *   const patches = extractPatches(kimiTextResponse);
 *   // → [{ priority, type, skeleton_id, selector, cssOverrides, issue, reason }]
 */

const fs = require('fs');
const path = require('path');

// ─── 骨架 → 文件路径映射 ──────────────────────────────────────
// 这个映射让 DeepSeek 知道改哪个文件
const SKELETON_FILES = {
  // 百科全书
  abyss:      'skeletons/encyclopedia/abyss/showcase.html',
  'purple-orb': 'skeletons/encyclopedia/purple-orb/showcase.html',
  scroll:     'skeletons/encyclopedia/scroll/showcase.html',
  magazine:   'skeletons/encyclopedia/magazine/showcase.html',
  // 关系图谱
  dossier:      'skeletons/relationship/dossier/showcase.html',
  social:       'skeletons/relationship/social/showcase.html',
  'xianxia-sect': 'skeletons/relationship/xianxia-sect/showcase.html',
  'family-tree':  'skeletons/relationship/family-tree/showcase.html',
  // 角色卡牌
  'card-deck':    'skeletons/character/card-deck/showcase.html',
  'status-board': 'skeletons/character/status-board/showcase.html',
  // 叙事时间线
  narrative:      'skeletons/timeline/narrative/showcase.html',
  // 世界观地图
  'canvas-map':   'skeletons/world-map/canvas-map/showcase.html',
  galaxy:         'skeletons/world-map/galaxy/showcase.html',
  'd3-galaxy':    'skeletons/world-map/d3-galaxy/showcase.html',
};

const SKILL_ROOT = path.join(__dirname, '..');

/**
 * 从 Kimi 回复中提取 patches JSON 数组
 *
 * @param {string} kimiText - Kimi K2.5 的完整文本回复
 * @returns {Array} 结构化的修复指令数组
 */
function extractPatches(kimiText) {
  if (!kimiText) return [];

  // 尝试从 ```json ... ``` 代码块中提取
  let jsonMatch = kimiText.match(/```json\s*([\s\S]*?)```/);
  if (jsonMatch) {
    try {
      const parsed = JSON.parse(jsonMatch[1].trim());
      if (parsed.patches && Array.isArray(parsed.patches)) {
        return parsed.patches;
      }
      // 可能直接就是数组
      if (Array.isArray(parsed)) return parsed;
    } catch (e) {
      // JSON 解析失败，继续尝试其他方法
    }
  }

  // 尝试从 ``` ... ``` 代码块中提取（没有 json 标记的情况）
  jsonMatch = kimiText.match(/```\s*([\s\S]*?)```/);
  if (jsonMatch) {
    for (const candidate of [jsonMatch[1], `{${jsonMatch[1]}}`, `[${jsonMatch[1]}]`]) {
      try {
        const parsed = JSON.parse(candidate.trim());
        if (parsed.patches && Array.isArray(parsed.patches)) return parsed.patches;
        if (Array.isArray(parsed)) return parsed;
      } catch (e) { /* 继续尝试 */ }
    }
  }

  // 最后尝试：从文本中搜索 {"patches": 或 "patches": 模式
  const looseMatch = kimiText.match(/"patches"\s*:\s*\[([\s\S]*?)\]/);
  if (looseMatch) {
    try {
      const wrapped = '{"patches": [' + looseMatch[1] + ']}';
      const parsed = JSON.parse(wrapped);
      if (parsed.patches) return parsed.patches;
    } catch (e) { /* 放弃 */ }
  }

  return [];
}

/**
 * 将 patches 转换为 DeepSeek 可读的修复清单
 *
 * 输出格式：
 * {
 *   generated_at: "2026-05-25 09:30",
 *   from_file: "百科数据-abyss-blood-red.html",
 *   skeleton_id: "abyss",
 *   overall_score: 8.5,
 *   issues: [
 *     {
 *       priority: "P0",
 *       type: "typography",
 *       description: "图谱节点文字在深色背景上可读性差",
 *       target_file: "skeletons/encyclopedia/abyss/showcase.html",
 *       selector: ".graph-node text",
 *       // cssOverrides 是给 DeepSeek 看的变化清单
 *       cssChanges: { "font-size": "11px → 13px" },
 *       action: "在 showcase.html 中找到 .graph-node text 的 CSS 规则，更新 font-size 为 13px",
 *     }
 *   ]
 * }
 */
function generateManifest(patches, meta = {}) {
  const {
    fromFile = 'unknown.html',
    skeletonId = 'unknown',
    score = null,
    screenshotPath = null,
  } = meta;

  const issues = patches.map((p, i) => {
    // 以从文件名推断的 skeleton_id 为准，Kimi 的建议只做参考
    const effectiveSkeletonId = skeletonId !== 'unknown' ? skeletonId : (p.skeleton_id || skeletonId);
    const targetFile = SKELETON_FILES[effectiveSkeletonId] || null;

    // 构建 cssChanges：from → to 的描述
    const cssChanges = {};
    if (p.cssOverrides) {
      for (const [prop, val] of Object.entries(p.cssOverrides)) {
        cssChanges[prop] = `→ ${val}`;
      }
    }

    // 构建自然语言 action 指令（DeepSeek 可直接理解）
    const cssEntries = p.cssOverrides
      ? Object.entries(p.cssOverrides).map(([k, v]) => `${k}: ${v}`).join('; ')
      : '';
    const action = targetFile
      ? `在 ${targetFile} 中，找到选择器「${p.selector}」的 CSS 规则，确保包含：${cssEntries}`
      : `在展示 HTML 中，找到选择器「${p.selector}」并设置：${cssEntries}`;

    return {
      id: `FIX-${i + 1}`,
      priority: p.priority || 'P2',
      type: p.type || 'other',
      description: p.issue || p.reason || '未描述问题',
      target_file: targetFile,
      target_abs: targetFile ? path.join(SKILL_ROOT, targetFile) : null,
      selector: p.selector || 'unknown',
      cssOverrides: p.cssOverrides || {},
      cssChanges,
      action,
      reason: p.reason || '',
    };
  });

  // 按优先级排序
  const priorityOrder = { P0: 0, P1: 1, P2: 2 };
  issues.sort((a, b) => (priorityOrder[a.priority] ?? 9) - (priorityOrder[b.priority] ?? 9));

  const manifest = {
    manifest_version: 1,
    generated_at: new Date().toISOString().replace('T', ' ').slice(0, 19),
    from_file: fromFile,
    skeleton_id: skeletonId,
    overall_score: score,
    total_issues: issues.length,
    p0_count: issues.filter(i => i.priority === 'P0').length,
    p1_count: issues.filter(i => i.priority === 'P1').length,
    p2_count: issues.filter(i => i.priority === 'P2').length,
    issues,
    // 给 DeepSeek 的摘要
    summary: getSummary(issues, score),
  };

  return manifest;
}

/**
 * 生成给 DeepSeek 看的摘要文本（嵌入 manifest 中）
 */
function getSummary(issues, score) {
  const p0 = issues.filter(i => i.priority === 'P0');
  const p1 = issues.filter(i => i.priority === 'P1');
  const lines = [];
  lines.push(`视觉 QA 完成，总体评分 ${score ?? 'N/A'}/10。`);
  if (p0.length > 0) {
    lines.push(`\n【必须修复 - P0】共 ${p0.length} 项：`);
    p0.forEach(i => lines.push(`  - ${i.description}`));
  }
  if (p1.length > 0) {
    lines.push(`\n【建议修复 - P1】共 ${p1.length} 项：`);
    p1.forEach(i => lines.push(`  - ${i.description}`));
  }
  if (p0.length === 0 && p1.length === 0) {
    lines.push('\n整体质量良好，暂无急需修复的问题。');
  }
  lines.push(`\n详细修复清单见本 manifest 的 issues 字段，可直接按 target_abs + selector + cssOverrides 执行。`);
  return lines.join('\n');
}

/**
 * 保存修复清单到文件
 *
 * @param {object} manifest - generateManifest 的返回
 * @param {string} outputDir - 输出目录
 * @returns {string} 保存的文件路径
 */
function saveManifest(manifest, outputDir) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 1. 保存 JSON 版本（给 DeepSeek）
  const jsonPath = path.join(outputDir, `fix-manifest-${manifest.skeleton_id}.json`);
  fs.writeFileSync(jsonPath, JSON.stringify(manifest, null, 2), 'utf-8');

  // 2. 保存 Markdown 版本（给人看）
  const mdPath = path.join(outputDir, `fix-manifest-${manifest.skeleton_id}.md`);
  const md = toMarkdown(manifest);
  fs.writeFileSync(mdPath, md, 'utf-8');

  return jsonPath;
}

/**
 * 将 manifest 转换为 Markdown（供人阅读 + DeepSeek 也能读）
 */
function toMarkdown(manifest) {
  const lines = [];
  lines.push(`# HTML 视觉修复清单`);
  lines.push('');
  lines.push(`| 项目 | 值 |`);
  lines.push(`|------|-----|`);
  lines.push(`| 来源 | ${manifest.from_file} |`);
  lines.push(`| 骨架 | ${manifest.skeleton_id} |`);
  lines.push(`| 评分 | ${manifest.overall_score ?? 'N/A'}/10 |`);
  lines.push(`| 问题数 | P0: ${manifest.p0_count} / P1: ${manifest.p1_count} / P2: ${manifest.p2_count} |`);
  lines.push('');
  lines.push(`## 修复项`);
  lines.push('');

  for (const issue of manifest.issues) {
    lines.push(`### ${issue.id} [${issue.priority}] ${issue.description}`);
    lines.push('');
    lines.push(`- **类型**: ${issue.type}`);
    lines.push(`- **选择器**: \`${issue.selector}\``);
    if (issue.target_file) lines.push(`- **目标文件**: ${issue.target_file}`);
    if (issue.reason) lines.push(`- **原因**: ${issue.reason}`);
    lines.push(`- **CSS 改动**:`);
    for (const [prop, change] of Object.entries(issue.cssChanges)) {
      lines.push(`  - \`${prop}\` ${change}`);
    }
    lines.push(`- **执行指令**: ${issue.action}`);
    lines.push('');
  }

  return lines.join('\n');
}

module.exports = {
  extractPatches,
  generateManifest,
  saveManifest,
  toMarkdown,
  SKELETON_FILES,
};
