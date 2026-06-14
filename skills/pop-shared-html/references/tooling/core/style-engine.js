/**
 * style-engine.js — 风格编排引擎（v2 多内容类型版）
 *
 * 职责：
 *   1. 接收「素材路径」和「可选风格覆盖」
 *   2. 调用 analyzer 检测内容类型 + 小说类型
 *   3. 调用 paletteSystem.route() 匹配最优骨架+调色板
 *   4. 加载对应的 showcase HTML
 *   5. 调用 injector 注入数据 + 调色板 CSS
 *   6. 输出最终 HTML
 *
 * 使用方式：
 *   styleEngine.run('素材.json')
 *   styleEngine.run('素材.json', { skeleton: 'social', palette: 'avatar-default' })
 *
 * 注册新骨架 = 在此文件的 SKELETON_REGISTRY 添加一行
 * 注入器在 engines/injector.js 中
 */

const fs = require('fs');
const path = require('path');

const { paletteSystem } = require('../shared/palette-system.js');
const analyzer = require('./analyzer.js');
const { adapt } = require('./adapter.js');

// 视觉 QA 模块（仅在使用时加载，不阻塞主管线）
let visualQA = null;
function getVisualQA() {
  if (!visualQA) {
    try { visualQA = require(path.join(__dirname, '..', 'qa', 'visual-qa.js')); }
    catch (e) { /* QA 模块未安装时静默降级 */ }
  }
  return visualQA;
}

// ─── 骨架注册表（内容类型 → 可用骨架列表） ───────────────────────
//
// 每添加一个 show case = 加一行在对应类型的 showcase 对象里。
// 如果该 show case 的数据格式不同 → 用不同的 injectFn。
// 所有关系图谱变体都用 injectGraph（相同 const DATA 格式）。

const SKELETON_REGISTRY = {
  // ── 百科全书 ──────────────────────────────────────────────
  encyclopedia: {
    name: '百科全书',
    showcase: {
      abyss:      path.join(__dirname, '..', 'skeletons', 'encyclopedia', 'abyss', 'showcase.html'),
      'purple-orb': path.join(__dirname, '..', 'skeletons', 'encyclopedia', 'purple-orb', 'showcase.html'),
    },
    injectFn: 'injectEncyclopedia',
  },

  // ── 关系图谱 ──────────────────────────────────────────────
  // 所有变体都用 const DATA = {nodes, edges} 格式 → 复用 injectGraph
  relationship: {
    name: '关系图谱',
    showcase: {
      dossier:      path.join(__dirname, '..', 'skeletons', 'relationship', 'dossier', 'showcase.html'),
      social:       path.join(__dirname, '..', 'skeletons', 'relationship', 'social', 'showcase.html'),
      'xianxia-sect': path.join(__dirname, '..', 'skeletons', 'relationship', 'xianxia-sect', 'showcase.html'),
      'family-tree':  path.join(__dirname, '..', 'skeletons', 'relationship', 'family-tree', 'showcase.html'),
    },
    injectFn: 'injectGraph',
  },

  // ── 角色卡牌 ──────────────────────────────────────────────
  // 数据格式 1: const CHARACTERS = [{name, desc, faction, type, ...}]
  // 数据格式 2: const D = {characters: [{name, states: [...]}], stages: [...]} (状态看板)
  character: {
    name: '角色卡牌',
    showcase: {
      'card-deck':    path.join(__dirname, '..', 'skeletons', 'character', 'card-deck', 'showcase.html'),
      'status-board': path.join(__dirname, '..', 'skeletons', 'character', 'status-board', 'showcase.html'),
    },
    injectFn: 'injectCharacterData',
  },

  // ── 叙事时间线 ────────────────────────────────────────────
  timeline: {
    name: '叙事时间线',
    showcase: {
      narrative: path.join(__dirname, '..', 'skeletons', 'timeline', 'narrative', 'showcase.html'),
    },
    injectFn: 'injectTimeline',
  },

  // ── 世界观星系图 ──────────────────────────────────────────
  // 数据格式: canvas-map: const DATA = {...}
  //          galaxy/d3-galaxy: const NODES = [...] / const EDGES = [...]
  worldMap: {
    name: '世界观地图',
    showcase: {
      'canvas-map': path.join(__dirname, '..', 'skeletons', 'world-map', 'canvas-map', 'showcase.html'),
      'galaxy':     path.join(__dirname, '..', 'skeletons', 'world-map', 'galaxy', 'showcase.html'),
      'd3-galaxy':  path.join(__dirname, '..', 'skeletons', 'world-map', 'd3-galaxy', 'showcase.html'),
    },
    injectFn: {
      'canvas-map': 'injectCanvasMap',
      'galaxy': 'injectWorldMap',
      'd3-galaxy': 'injectD3Galaxy',
    },
  },

  // ── 金句卡片（from html-anything card-twitter pattern）─ TODO
  // quote: {
  //   name: '金句卡片',
  //   showcase: {
  //     poster: path.join(__dirname, '..', 'skeletons', 'quote', 'poster', 'showcase.html'),
  //   },
  //   injectFn: 'injectQuote',
  // },
};

// ─── 核心引擎 ────────────────────────────────────────────────────

const styleEngine = {

  /**
   * 运行一条完整的风格注入管线
   * 
   * @param {string} contentPath    - 素材文件路径（JSON/YAML/MD/TXT）
   * @param {object} [options]      - 可选覆盖参数
   * @param {string} [options.skeleton]   - 强制指定骨架
   * @param {string} [options.palette]    - 强制指定调色板
   * @param {string} [options.genre]      - 强制指定小说类型
   * @param {string} [options.outputPath] - 输出路径
   * @returns {{ success, outputPath, skeleton, palette, warnings, contentType }}
   */
  run(contentPath, options = {}) {
    const warnings = [];

    const raw = fs.readFileSync(contentPath, 'utf-8');
    const analysis = analyzer.analyze(raw, contentPath);
    const contentType = analysis.type;
    const novelGenre = options.genre || analysis.genre || null;

    if (!contentType) {
      return { success: false, error: '无法检测内容类型', warnings };
    }

    // 风格路由
    let skeletonId, paletteId;
    if (options.skeleton && options.palette) {
      skeletonId = options.skeleton;
      paletteId = options.palette;
    } else {
      const route = paletteSystem.route(contentType, novelGenre);
      skeletonId = options.skeleton || route.skeleton;
      paletteId = options.palette || route.palette;
    }

    // 确认骨架存在
    const contentTypeConfig = SKELETON_REGISTRY[contentType];
    if (!contentTypeConfig) {
      return { success: false, error: `不支持的内容类型: ${contentType}`, warnings };
    }
    const showcasePath = contentTypeConfig.showcase[skeletonId];
    if (!showcasePath || !fs.existsSync(showcasePath)) {
      warnings.push(`骨架 ${skeletonId} 不存在，使用第一个可用骨架`);
      const fallbackId = Object.keys(contentTypeConfig.showcase).find(
        id => fs.existsSync(contentTypeConfig.showcase[id])
      );
      if (!fallbackId) {
        return { success: false, error: `内容类型 ${contentType} 无可用骨架`, warnings };
      }
      skeletonId = fallbackId;
      paletteId = paletteSystem.list(fallbackId)[0]?.id || paletteId;
    }

    // 加载 showcase HTML
    const showcaseHtml = fs.readFileSync(contentTypeConfig.showcase[skeletonId], 'utf-8');

    // 加载注入器
    const injector = require(path.join(__dirname, '..', 'engines', 'injector.js'));
    let injectFnName = contentTypeConfig.injectFn;
    // 支持 per-skeleton 注入函数映射（如 worldMap 每个骨架用不同注入器）
    if (typeof injectFnName === 'object' && injectFnName !== null) {
      injectFnName = injectFnName[skeletonId] || Object.values(injectFnName)[0];
    }
    const injectFn = injector[injectFnName];
    if (!injectFn) {
      return { success: false, error: `注入函数 ${injectFnName} 不存在`, warnings };
    }

    // 解析数据
    let newData;
    try { newData = JSON.parse(raw); }
    catch (e) { newData = raw; }

    // 注入数据 + 密度适配
    let resultHtml = injectFn(showcaseHtml, newData);

    // 密度适配：分析数据量 → 注入 data-density → 日志诊断
    const adapterResult = adapt(resultHtml, newData, { skeletonId, contentType });
    resultHtml = adapterResult.html;
    if (adapterResult.diagnostic) {
      console.log('  [适配]', adapterResult.diagnostic.summary);
      adapterResult.diagnostic.warnings.forEach(w => console.log('  [适配!]', w));
    }

    // 注入调色板 CSS
    const paletteInfo = paletteSystem.get(skeletonId, paletteId);
    if (paletteInfo) {
      resultHtml = paletteSystem.injectPaletteCSS(resultHtml, skeletonId, paletteId);
    } else {
      warnings.push(`调色板 ${paletteId} 不存在，使用默认配色`);
    }

    // 输出
    const outputPath = options.outputPath || this._defaultOutputPath(contentPath, skeletonId, paletteId);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, resultHtml);

    return {
      success: true,
      outputPath,
      skeleton: skeletonId,
      palette: paletteId,
      contentType,
      genre: novelGenre,
      warnings: warnings.concat(adapterResult.diagnostic?.warnings || []),
      density: adapterResult.diagnostic?.density || 'sparse',
      size: `${(resultHtml.length / 1024).toFixed(0)}KB`,
    };
  },

  /** 列出某内容类型可用的骨架 */
  listSkeletons(contentType) {
    const config = SKELETON_REGISTRY[contentType];
    if (!config) return [];
    const available = [];
    for (const [id, showcasePath] of Object.entries(config.showcase)) {
      available.push({
        id,
        name: this._skeletonName(id),
        exists: fs.existsSync(showcasePath),
        palettes: paletteSystem.list(id),
      });
    }
    return available;
  },

  /** 列出所有可用骨架 */
  listAll() {
    const result = {};
    for (const [contentType, config] of Object.entries(SKELETON_REGISTRY)) {
      result[contentType] = this.listSkeletons(contentType);
    }
    return result;
  },

  _defaultOutputPath(contentPath, skeletonId, paletteId) {
    const basename = path.basename(contentPath, path.extname(contentPath));
    const dir = path.join(__dirname, '..', 'output');
    return path.join(dir, `${basename}-${skeletonId}-${paletteId}.html`);
  },

  _skeletonName(id) {
    const names = {
      abyss: '深渊粒子',
      'purple-orb': '紫色光晕',
      scroll: '水墨卷轴',
      magazine: '杂志卡片',
      dossier: '档案线索板',
      social: '社交图谱',
      'xianxia-sect': '仙侠宗派',
      'family-tree': '家族谱系',
      'card-deck': '角色卡片集',
      'status-board': '状态追踪看板',
      narrative: '叙事时间线',
      'canvas-map': '画布世界地图',
      galaxy: '世界观星系图',
      'd3-galaxy': 'D3星系图',
    };
    return names[id] || id;
  },

  // ── 视觉 QA（可选后置步骤） ──────────────────────────────
  //
  // 用法：
  //   const result = styleEngine.run(dataPath);
  //   const qa = await styleEngine.runQA(result.outputPath);
  //   console.log(qa.summary.averageScore);
  //
  // 依赖：qa/ 目录（puppeteer + Kimi K2.5 API Key）
  //
  async runQA(htmlPath, opts = {}) {
    const qa = getVisualQA();
    if (!qa) {
      return { success: false, error: 'QA 模块未安装（缺少 qa/ 目录或 puppeteer）' };
    }
    return qa.runQA(htmlPath, opts);
  },

  /** 快捷：对 output 目录执行全量 QA */
  async runAllQA(opts = {}) {
    const qa = getVisualQA();
    if (!qa) {
      return { success: false, error: 'QA 模块未安装' };
    }
    return qa.runOnOutputDir(opts);
  },
};

module.exports = { styleEngine, SKELETON_REGISTRY };
