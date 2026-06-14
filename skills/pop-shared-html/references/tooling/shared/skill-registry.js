/**
 * shared/skill-registry.js — 骨架注册表
 *
 * Vibe Creating Skill 的核心路由表。
 * 注册 5 种内容类型 × 12 个注入骨架。
 *
 * 用法：
 *   const { registry } = require('./shared/skill-registry.js');
 *   registry.detect(data)  → { contentType, skeletons }
 *   registry.match('百科') → { ... }
 *   registry.listAll()     → 完整的全量注册表
 */

const path = require('path');
const ROOT = path.resolve(__dirname, '..');

// ============================================================
// 注入骨架注册表
// ============================================================

const INJECT_SKELETONS = {
  encyclopedia: {
    name: '百科全书',
    description: '实体分类百科、设定集',
    skeletons: ['abyss', 'purple-orb'],
    dataSignals: ['categories'],
    detect: (data) => data && data.categories,
  },
  relationship: {
    name: '关系图谱',
    description: '角色/实体关系网络图',
    skeletons: ['dossier', 'social', 'xianxia-sect', 'family-tree'],
    dataSignals: ['nodes', 'edges'],
    detect: (data) => data && data.nodes && data.edges,
  },
  character: {
    name: '角色卡牌',
    description: '角色实体卡片/状态追踪',
    skeletons: ['card-deck', 'status-board'],
    dataSignals: ['characters'],
    detect: (data) => data && (data.characters || data.CHARACTERS),
  },
  timeline: {
    name: '叙事时间线',
    description: '事件时间线/甘特图',
    skeletons: ['narrative'],
    dataSignals: ['events'],
    detect: (data) => data && data.events,
  },
  worldMap: {
    name: '世界观地图',
    description: '世界地图/星系图',
    skeletons: ['canvas-map', 'galaxy', 'd3-galaxy'],
    dataSignals: ['NODES', 'central_concept'],
    detect: (data) => data && (data.NODES || data.central_concept),
  },
};

// ============================================================
// 核心 API
// ============================================================

const registry = {

  /** 自动检测数据类型 */
  detect(data, options = {}) {
    for (const [contentType, config] of Object.entries(INJECT_SKELETONS)) {
      if (config.detect(data)) {
        return { contentType, ...config };
      }
    }
    return null;
  },

  /** 按名称/关键词模糊匹配 */
  match(keyword) {
    for (const [contentType, config] of Object.entries(INJECT_SKELETONS)) {
      if (contentType.includes(keyword) || config.name.includes(keyword)) return { contentType, ...config };
    }
    return null;
  },

  /** 列出全部 */
  listAll() {
    return Object.entries(INJECT_SKELETONS).map(([id, cfg]) => ({
      id,
      name: cfg.name,
      skeletons: cfg.skeletons,
      skeletonCount: cfg.skeletons.length,
    }));
  },

  /** 获取骨架中文名列表 */
  getSkeletons(contentType) {
    const config = INJECT_SKELETONS[contentType];
    if (!config) return [];
    const names = {
      abyss: '深渊粒子', 'purple-orb': '紫色光晕',
      dossier: '档案线索板', social: '社交图谱', 'xianxia-sect': '仙侠宗派', 'family-tree': '家族谱系',
      'card-deck': '角色卡片集', 'status-board': '状态追踪看板',
      narrative: '叙事时间线',
      'canvas-map': '画布世界地图', galaxy: '世界观星系图', 'd3-galaxy': 'D3星系图',
    };
    return config.skeletons.map(id => ({ id, name: names[id] || id }));
  },
};

module.exports = { registry, INJECT_SKELETONS };
