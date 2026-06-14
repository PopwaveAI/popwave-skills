/**
 * HTML 数据注入器 v3
 * 
 * 核心改进：从「正则搜索 JS 变量声明替换」改为「标记替换」
 * 
 * 每个 showcase.html 中，可被替换的数据用注释标记：
 *   /* INJECT:KEY *\/const DATA = {};/* ENDINJECT *\/
 * 
 * 注入器通过精确匹配标记替换，不再依赖正则搜索变量声明。
 * 
 * 注入函数清单：
 *   injectEncyclopedia   → INJECT:CATEGORIES, CAT_STATS, TITLE, DESCRIPTION
 *   injectGraph          → INJECT:DATA
 *   injectCharacterCards → INJECT:CHARACTERS
 *   injectCharacterBoard → INJECT:D
 *   injectTimeline       → INJECT:DATA_JSON
 *   injectWorldMap       → INJECT:NODES, EDGES
 *   injectD3Galaxy       → INJECT:DATA
 */

const fs = require('fs');

// ============================================================
// 标记替换引擎 + 清理
// ============================================================

const INJECT_START_RE = /\/\*\s*INJECT:\w+\s*\*\//g;
const INJECT_END_RE = /\/\*\s*ENDINJECT\s*\*\//g;

/**
 * 替换 /* INJECT:KEY *\/ ... /* ENDINJECT *\/ 之间的内容
 * @returns {string} 替换后的 HTML（标记仍保留，最终调用 stripInjectMarkers 清理）
 */
function injectByMarker(html, markerName, replacement) {
  const startTag = `/* INJECT:${markerName} */`;
  const endTag = `/* ENDINJECT */`;
  const start = html.indexOf(startTag);
  if (start === -1) return html;
  const end = html.indexOf(endTag, start + startTag.length);
  if (end === -1) return html;
  return html.slice(0, start + startTag.length) + replacement + html.slice(end);
}

/** 移除所有 INJECT 标记注释，仅保留替换后的内容 */
function stripInjectMarkers(html) {
  return html.replace(INJECT_START_RE, '').replace(INJECT_END_RE, '');
}

// ============================================================
// 辅助函数
// ============================================================

function hashCode(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h) + str.charCodeAt(i);
    h = h & h;
  }
  return Math.abs(h);
}

function escAttr(v) {
  return String(v || '').replace(/[&<>"']/g, m =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m]);
}

/**
 * 替换带嵌套子标签的 SVG 元素（<g class="nodes"> 内多子 <g>）
 */
function replaceBalancedTag(html, tag, attrMatch, replacement) {
  const openTag = `<${tag} ${attrMatch}>`;
  const closeTag = `</${tag}>`;
  const startIdx = html.indexOf(openTag);
  if (startIdx === -1) return html;

  let depth = 0, pos = startIdx, endIdx = -1;
  while (pos < html.length) {
    const nextOpen = html.indexOf(`<${tag}`, pos);
    const nextClose = html.indexOf(closeTag, pos);
    if (nextClose === -1) break;
    if (nextOpen !== -1 && nextOpen < nextClose) {
      const selfClose = html.indexOf('/>', nextOpen);
      if (selfClose !== -1 && selfClose < nextClose) { pos = selfClose + 2; continue; }
      depth++; pos = nextOpen + tag.length + 1;
    } else {
      depth--;
      if (depth === 0) { endIdx = nextClose + closeTag.length; break; }
      pos = nextClose + closeTag.length;
    }
  }
  if (endIdx === -1) return html;
  return html.substring(0, startIdx) + replacement + html.substring(endIdx);
}

// ============================================================
// 注入：百科全书
// ============================================================
function injectEncyclopedia(html, newData) {
  const cats = newData.categories || {};
  const title = newData.title || '百科';
  const desc = newData.description || '';

  // 构建分类统计
  const stats = {};
  for (const [key, cat] of Object.entries(cats)) {
    stats[key] = (cat.entries || []).length;
  }

  // 构建位置映射
  const positions = {};
  for (const [key, cat] of Object.entries(cats)) {
    const entries = cat.entries || [];
    positions[key] = entries.map((_, i) => {
      if (cat._positions && cat._positions[i]) return cat._positions[i];
      const angle = (i / entries.length) * Math.PI * 2 - Math.PI / 2;
      const cx = 50, cy = 50, r = 20;
      return [cx + Math.cos(angle) * r, cy + Math.sin(angle) * r * 0.7].map(v => Math.round(v));
    });
  }

  // 标记替换
  html = injectByMarker(html, 'CATEGORIES',
    JSON.stringify(cats, null, 2).replace(/"([^"]+)":\s*\{/g, '"$1": {'));
  html = injectByMarker(html, 'CAT_STATS', JSON.stringify(stats));
  html = injectByMarker(html, 'mapPositions', JSON.stringify(positions));
  html = injectByMarker(html, 'TITLE', JSON.stringify(title));
  html = injectByMarker(html, 'DESCRIPTION', JSON.stringify(desc || ('一张可检索的' + title + '世界图谱')));

  return stripInjectMarkers(html);
}

// ============================================================
// 注入：关系图谱（dossier / social / xianxia-sect / family-tree）
// ============================================================
function injectGraph(html, newData) {
  const nodes = newData.nodes || [];
  const edges = newData.edges || [];
  const title = newData.title || '关系图谱';

  // 布局计算
  const COUNT = nodes.length;
  const nodeStep = 120;
  const idealR = (COUNT * nodeStep) / (2 * Math.PI);
  const baseR = Math.max(160, Math.min(400, idealR));

  const positioned = nodes.map((n, i) => {
    if (n.x !== undefined && n.y !== undefined) return n;
    const angle = (i / COUNT) * Math.PI * 2 - Math.PI / 2;
    const jitter = Math.sin(i * 1.7) * Math.min(60, baseR * 0.2);
    const r = baseR + jitter;
    return { ...n, x: 500 + Math.cos(angle) * r, y: 325 + Math.sin(angle) * r * 0.65 };
  });

  // 密度缩放
  const viewBoxScale = baseR > 280 ? 1.35 : baseR > 220 ? 1.15 : 1;
  if (viewBoxScale > 1) {
    const newW = Math.round(1000 * viewBoxScale);
    const newH = Math.round(650 * viewBoxScale);
    html = html.replace(/viewBox="0 0 1000 650"/, `viewBox="0 0 ${newW} ${newH}"`);
    const scalePct = viewBoxScale > 1.2 ? '0.75' : '0.88';
    const styleInject = [
      `/* ── 自动密度缩放（${COUNT} 个节点） ── */`,
      `svg{min-width:${newW}px;min-height:${newH}px}`,
      `html[data-density="dense"] .graph{transform-origin:center;transform:scale(${scalePct})}`,
    ].join('\n');
    html = html.replace('</style>', styleInject + '\n</style>');
  }

  const edgeTypes = [...new Set(edges.map(e => e.type))];
  const typeLabels = {
    blood: '血亲', romantic: '爱恋', mentor: '师承', ally: '盟友',
    hostile: '敌对', betrayal: '背叛', identity: '身份', control: '控制',
    evidence: '证据', event: '事件', platform: '平台'
  };

  const dataObj = {
    nodes: positioned.map(n => ({
      id: n.id, name: n.name, role: n.role || '', group: n.group || 'support',
      desc: n.desc || '', x: n.x, y: n.y, tilt: n.tilt || 0
    })),
    edges: edges.map(e => ({
      source: e.source, target: e.target, type: e.type || 'ally', label: e.label || ''
    }))
  };

  // 替换 DATA
  html = injectByMarker(html, 'DATA', JSON.stringify(dataObj));

  // 重建 SVG 节点 DOM
  const nodeSvg = positioned.map((n, i) => {
    const tilt = n.tilt || (Math.random() - 0.5) * 2;
    return `<g class="node node-${escAttr(n.group || 'support')}" data-id="${escAttr(n.id)}" data-name="${escAttr(n.name)}" data-role="${escAttr(n.role || '')}" data-desc="${escAttr(n.desc || '')}" transform="translate(${n.x.toFixed(1)} ${n.y.toFixed(1)}) rotate(${tilt.toFixed(1)})"><rect class="node-core dossier" x="-55" y="-38" width="110" height="82"></rect><rect class="dossier-head" x="-55" y="-38" width="110" height="20"></rect><text class="case-no" x="37" y="-24">${String(i + 1).padStart(2, '0')}</text><rect class="dossier-photo" x="-47" y="-10" width="30" height="32"></rect><path class="dossier-photo-mark" d="M-42 17 L-32 4 L-22 17"></path><rect class="redact" x="-8" y="0" width="44" height="5"></rect><rect class="redact redact-small" x="-8" y="12" width="32" height="5"></rect><rect class="redact redact-long" x="-47" y="31" width="68" height="5"></rect><circle class="dossier-pin" cy="-42" r="3.5"></circle><text class="node-label dossier-name" x="-47" y="-24">${escAttr(n.name)}</text><text class="node-sub dossier-role" x="-8" y="-5">${escAttr(n.role || '')}</text></g>`;
  }).join('');
  html = replaceBalancedTag(html, 'g', 'class="nodes"', '<g class="nodes">' + nodeSvg + '</g>');

  // 重建 SVG 边 DOM
  const edgeSvg = edges.map((e, i) =>
    `<path class="edge edge-${escAttr(e.type || 'ally')}" data-source="${escAttr(e.source)}" data-target="${escAttr(e.target)}" data-curve="dossier" data-index="${i}" d=""></path>`
  ).join('');
  html = replaceBalancedTag(html, 'g', 'class="edges"', '<g class="edges">' + edgeSvg + '</g>');

  // 重建边标签 DOM
  const labelSvg = edges.map(e =>
    `<text class="edge-label" x="0" y="0">${escAttr(e.label || '')}</text>`
  ).join('');
  html = replaceBalancedTag(html, 'g', 'class="edge-labels"', '<g class="edge-labels">' + labelSvg + '</g>');

  // 更新 TYPE_LABELS
  const existingTypes = { ...typeLabels };
  edgeTypes.forEach(t => { if (!existingTypes[t]) existingTypes[t] = t; });
  html = injectByMarker(html, 'TYPE_LABELS', JSON.stringify(existingTypes));

  // 重建 filter 按钮
  let filterHtml = '<button class="filter is-active" data-type="all">全部</button>';
  edgeTypes.forEach(t => {
    const label = existingTypes[t] || t;
    filterHtml += `<button class="filter" data-type="${t}"><span class="line-swatch edge-${t}"></span>${label}</button>`;
  });
  html = html.replace(/<nav class="filters">[\s\S]*?<\/nav>/, '<nav class="filters">' + filterHtml + '</nav>');

  // 更新标题
  html = injectByMarker(html, 'TITLE', JSON.stringify(title));

  return stripInjectMarkers(html);
}

// ============================================================
// 注入：角色卡片集
// ============================================================
function injectCharacterCards(html, newData) {
  const characters = Array.isArray(newData) ? newData : (newData.characters || newData.CHARACTERS || []);
  html = injectByMarker(html, 'CHARACTERS', JSON.stringify(characters));
  if (html.includes('/* INJECT:D */')) {
    const dataObj = typeof newData === 'object' && !Array.isArray(newData) ? newData : { characters };
    html = injectByMarker(html, 'D', JSON.stringify(dataObj));
  }
  return stripInjectMarkers(html);
}

// ============================================================
// 注入：角色状态看板
// ============================================================
function injectCharacterBoard(html, newData) {
  const dataObj = typeof newData === 'object' && !Array.isArray(newData) ? newData : { characters: newData };
  html = injectByMarker(html, 'D', JSON.stringify(dataObj));
  return stripInjectMarkers(html);
}

// ============================================================
// 注入：叙事时间线
// ============================================================
function injectTimeline(html, newData) {
  const jsonStr = JSON.stringify(newData);
  html = injectByMarker(html, 'DATA_JSON', jsonStr);
  return stripInjectMarkers(html);
}

// ============================================================
// 注入：世界观地图
// canvas-map 版 → INJECT:DATA (嵌套结构)
// galaxy 版 → INJECT:NODES, INJECT:EDGES
// ============================================================
function injectCanvasMap(html, newData) {
  const dataObj = typeof newData === 'object' ? newData : {};
  html = injectByMarker(html, 'DATA', JSON.stringify(dataObj));
  return stripInjectMarkers(html);
}

function injectWorldMap(html, newData) {
  const nodes = newData.nodes || newData.NODES || [];
  const edges = newData.edges || newData.EDGES || [];
  html = injectByMarker(html, 'NODES', JSON.stringify(nodes));
  html = injectByMarker(html, 'EDGES', JSON.stringify(edges));
  return stripInjectMarkers(html);
}

// ============================================================
// 注入：D3 星系图
// ============================================================
function injectD3Galaxy(html, newData) {
  const dataObj = typeof newData === 'object' ? newData : { nodes: [], edges: [] };
  html = injectByMarker(html, 'DATA', JSON.stringify(dataObj));
  return stripInjectMarkers(html);
}

// ============================================================
// 自动检测 + 注入（CLI 兼容）
// ============================================================
function inject(html, newData, outputPath) {
  const has = (s) => html.includes(s);

  let result;
  if (has('/* INJECT:CATEGORIES */')) {
    console.log('  检测到: 百科全书');
    result = injectEncyclopedia(html, newData);
  } else if (has('/* INJECT:DATA */') && !has('/* INJECT:NODES */')) {
    console.log('  检测到: 关系图谱/D3星系图');
    if (has('"central_concept"')) {
      result = injectD3Galaxy(html, newData);
    } else {
      result = injectGraph(html, newData);
    }
  } else if (has('/* INJECT:CHARACTERS */')) {
    console.log('  检测到: 角色卡片集');
    result = injectCharacterCards(html, newData);
  } else if (has('/* INJECT:NODES */') || has('/* INJECT:EDGES */')) {
    console.log('  检测到: 世界观星系图');
    result = injectWorldMap(html, newData);
  } else if (has('/* INJECT:DATA_JSON */')) {
    console.log('  检测到: 叙事时间线');
    result = injectTimeline(html, newData);
  } else {
    console.log('  ✗ 无匹配的 INJECT 标记，无法注入');
    return;
  }

  fs.writeFileSync(outputPath, result);
  console.log('  注入完成: ' + outputPath + ' (' + (result.length / 1024).toFixed(0) + 'KB)');
}

// ============================================================
// CLI
// ============================================================
if (require.main === module) {
  const [showcasePath, dataPath, outputPath] = process.argv.slice(2);
  if (!showcasePath || !outputPath) {
    console.log('用法: node inject-data.js <showcase.html> <data.json?> <output.html>');
    process.exit(1);
  }
  const html = fs.readFileSync(showcasePath, 'utf8');
  let newData;
  if (dataPath) {
    newData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  } else {
    let input = '';
    process.stdin.on('data', chunk => input += chunk);
    process.stdin.on('end', () => { newData = JSON.parse(input); inject(html, newData, outputPath); });
    return;
  }
  inject(html, newData, outputPath);
}

module.exports = {
  inject, injectByMarker, stripInjectMarkers,
  injectEncyclopedia, injectGraph, injectCharacterCards,
  injectCharacterBoard, injectTimeline, injectCanvasMap, injectWorldMap, injectD3Galaxy
};
