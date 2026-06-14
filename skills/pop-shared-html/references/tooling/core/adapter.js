/**
 * core/adapter.js — 内容密度自适应层
 *
 * 职责：注入完成后，根据实际数据量自动调整 CSS 变量，
 *       让骨架的视觉密度与内容匹配。
 *
 * 我是 agent（pop），所以 adapter 的产出是：
 *   1. 数据诊断摘要（给我看）
 *   2. CSS 覆盖变量（直接写进 HTML）
 *   3. 建议备注（如果数据异常需要我手动处理）
 *
 * 使用：
 *   const result = adapt(html, data, { skeletonId, contentType });
 *   result.html       ← 注入密度变量后的 HTML
 *   result.density    ← 'sparse' | 'normal' | 'dense'
 *   result.diagnostic ← 供我阅读的数据摘要
 *   result.overrides  ← 具体改了什么
 */

// ─── 骨架密度配置 ──────────────────────────────────────────────
// 每个骨架可注册密度阈值和对应的 CSS 变量覆盖
// threshold: [sparseMax, normalMax] — 超出 normalMax 即为 dense

const DENSITY_CONFIG = {
  // 百科 — 条目数决定密度
  abyss: {
    thresholds: [8, 20],     // ≤8 sparse, 9-20 normal, >20 dense
    getKey: (data) => countEntriesInCategories(data),
    overrides: null,          // 由 :root[data-density="X"] 控制
  },
  'purple-orb': {
    thresholds: [8, 20],
    getKey: (data) => countEntriesInCategories(data),
    overrides: null,          // 原生 responsive grid
  },

  // 角色卡片集 — 角色数决定
  'card-deck': {
    thresholds: [5, 12],
    getKey: (data) => {
      if (Array.isArray(data)) return data.length;
      if (data.characters) return data.characters.length;
      if (data.CHARACTERS) return data.CHARACTERS.length;
      return 0;
    },
    overrides: null,          // TODO: 加卡片的字号/间距变量
  },

  // 状态追踪看板 — 角色数 × 阶段数
  'status-board': {
    thresholds: [30, 80],     // 总 cell 数
    getKey: (data) => {
      if (!data.characters || !data.stages) return 0;
      return data.characters.length * data.stages.length;
    },
    overrides: null,
  },

  // 关系图谱 — 节点数
  dossier: {
    thresholds: [10, 25],
    getKey: (data) => {
      if (data.nodes) return data.nodes.length;
      return 0;
    },
    overrides: null,
  },

  // 仙侠宗派 / 社交图谱 / 家族谱系 — 都用同一 DATA 格式
  'xianxia-sect': {
    thresholds: [8, 20],
    getKey: (data) => { if (data.nodes) return data.nodes.length; return 0; },
    overrides: null,
  },
  social: {
    thresholds: [10, 25],
    getKey: (data) => { if (data.nodes) return data.nodes.length; return 0; },
    overrides: null,
  },
  'family-tree': {
    thresholds: [10, 20],
    getKey: (data) => { if (data.nodes) return data.nodes.length; return 0; },
    overrides: null,
  },

  // 叙事时间线 — 事件数
  narrative: {
    thresholds: [15, 40],
    getKey: (data) => {
      if (data.events) return data.events.length;
      return 0;
    },
    overrides: null,
  },

  // D3 星系图 — 节点数（D3 自动处理力导向，不需要密度适配）
  'd3-galaxy': null,
  galaxy: null,
  canvas_map: null,
};

// ─── 辅助函数 ──────────────────────────────────────────────────

function countEntriesInCategories(data) {
  if (!data || !data.categories) return 0;
  let total = 0;
  for (const key of Object.keys(data.categories)) {
    const cat = data.categories[key];
    if (cat.entries) total += cat.entries.length;
  }
  return total;
}

// ─── 核心适配函数 ──────────────────────────────────────────────

function adapt(html, data, opts = {}) {
  const { skeletonId, contentType } = opts;
  const diagnostic = { skeletonId, contentType, totalEntries: 0, density: 'sparse', warnings: [] };

  // 1. 获取密度配置
  const config = DENSITY_CONFIG[skeletonId];
  if (!config) {
    diagnostic.warnings.push(`骨架 ${skeletonId} 无密度配置，跳过适配`);
    return { html, density: 'sparse', diagnostic, overrides: {} };
  }

  // 2. 计算密度指标
  const count = config.getKey(data);
  diagnostic.totalEntries = count;

  const [sparseMax, normalMax] = config.thresholds;
  let density;
  if (count <= sparseMax) density = 'sparse';
  else if (count <= normalMax) density = 'normal';
  else density = 'dense';
  diagnostic.density = density;

  // 3. 注入 data-density 属性到 <html> 或 <body>
  if (html.includes('<html')) {
    html = html.replace('<html', `<html data-density="${density}"`);
  } else if (html.includes('<body')) {
    html = html.replace('<body', `<body data-density="${density}"`);
  }

  // 4. 收集改了什么
  const overrides = { density };
  diagnostic.overrides = overrides;

  // 5. 诊断摘要（给我看的）
  diagnostic.summary =
    `${contentType}/${skeletonId}: ${count}个条目 → ${density}密度 ` +
    `(${count <= sparseMax ? '宽裕布局' : count <= normalMax ? '标准布局' : '紧凑布局'})`;

  if (density === 'dense') {
    diagnostic.warnings.push(`条目数 ${count} 超过 ${normalMax}，已启用紧凑模式`);
  }
  if (density === 'sparse' && count > 0) {
    diagnostic.warnings.push(`条目数 ${count} 较少，${skeletonId} 可能有大量留白，如需填充请告知`);
  }

  return { html, density, diagnostic, overrides };
}

module.exports = { adapt, DENSITY_CONFIG, countEntriesInCategories };
