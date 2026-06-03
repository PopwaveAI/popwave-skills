/**
 * palette-system.js — 调色板注册表 + CSS变量生成器
 * 
 * 每个调色板定义一套完整的视觉 tokens：
 *   - bg/paper/ink/accent/muted/text 为基础色
 *   - 骨架特有的变量（如 --particle-glow、--node-color）在骨架层补充
 * 
 * 使用方式：
 *   paletteSystem.get('abyss', 'blood-red')
 *   → { name, cssVars, match, description }
 * 
 *   paletteSystem.generateCSS('abyss', 'blood-red')
 *   → ":root { --abyss-bg: #020308; --abyss-accent: ... }"
 * 
 *   paletteSystem.forGenre('诡异')
 *   → { skeleton: 'abyss', palette: 'blood-red' }
 */

// ─── 调色板注册表 ────────────────────────────────────────────────
//
// 命名规范：
//   key 用英文短横命名，如 'ink-classic', 'blood-red'
//   name 用中文，如 '墨水经典', '暗红血犹腥'
//   match 数组 = 该调色板天然适合的小说类型

const PALETTES = {

  // ============================
  // 深渊粒子骨架（深色背景）
  // ============================
  abyss: {
    name: '深渊粒子',
    description: '深色背景 + 发光粒子 + 强对比',
    tokens: {
      bg: { default: '#020308', label: '背景' },
      surface: { default: 'rgba(12,16,25,.62)', label: '卡片表面' },
      accent: { default: '#58a6ff', label: '强调色' },
      text: { default: '#f2f4f8', label: '正文' },
      muted: { default: '#9ca6b5', label: '次要文字' },
      dim: { default: '#637083', label: '最弱文字' },
      line: { default: 'rgba(242,244,248,.10)', label: '分割线' },
      glow: { default: 'rgba(88,166,255,.045)', label: '辉光' },
      particle: { default: '#9ca6b5', label: '粒子色' },
    },
    palettes: [
      {
        id: 'blood-red',
        name: '暗红血犹腥',
        match: ['诡异', '悬疑', '惊悚', '克苏鲁', '恐怖'],
        css: {
          bg: '#0a0505',
          surface: 'rgba(26,10,10,.62)',
          accent: '#dc2626',
          text: '#f5f0f0',
          muted: '#a68a8a',
          dim: '#735555',
          line: 'rgba(220,38,38,.15)',
          glow: 'rgba(220,38,38,.06)',
          particle: '#dc2626',
        },
      },
      {
        id: 'deep-ocean',
        name: '深海幽冥',
        match: ['悬疑', '克苏鲁', '诡异', '深海', '孤岛'],
        css: {
          bg: '#020a14',
          surface: 'rgba(4,20,40,.62)',
          accent: '#06b6d4',
          text: '#e0f0f8',
          muted: '#7a9aaa',
          dim: '#4a6a7a',
          line: 'rgba(6,182,212,.12)',
          glow: 'rgba(6,182,212,.05)',
          particle: '#06b6d4',
        },
      },
      {
        id: 'cyber-purple',
        name: '赛博紫晶',
        match: ['科幻', '赛博', '异能', '系统'],
        css: {
          bg: '#0a0514',
          surface: 'rgba(20,10,40,.62)',
          accent: '#a855f7',
          text: '#f0e8f8',
          muted: '#a88ad5',
          dim: '#6a4a9a',
          line: 'rgba(168,85,247,.12)',
          glow: 'rgba(168,85,247,.05)',
          particle: '#a855f7',
        },
      },
      {
        id: 'golden-ages',
        name: '黄金纪元',
        match: ['修仙', '玄幻', '史诗', '上古'],
        css: {
          bg: '#0a0802',
          surface: 'rgba(26,20,10,.62)',
          accent: '#f59e0b',
          text: '#f5f0e0',
          muted: '#b5a07a',
          dim: '#756040',
          line: 'rgba(245,158,11,.12)',
          glow: 'rgba(245,158,11,.05)',
          particle: '#f59e0b',
        },
      },
      {
        id: 'emerald-night',
        name: '翡翠夜幕',
        match: ['奇幻', '精灵', '自然', '治愈'],
        css: {
          bg: '#020a06',
          surface: 'rgba(4,26,14,.62)',
          accent: '#34d399',
          text: '#e0f5ea',
          muted: '#7aaa8e',
          dim: '#4a7a5e',
          line: 'rgba(52,211,153,.10)',
          glow: 'rgba(52,211,153,.04)',
          particle: '#34d399',
        },
      },
    ],
  },

  // ============================
  // 水墨卷轴骨架（暖色·宣纸感）
  // ============================
  scroll: {
    name: '水墨卷轴',
    description: '暖色宣纸底 + 墨色文字 + 衬线字体',
    tokens: {
      bg: { default: '#f5f4ed', label: '宣纸底色' },
      paper: { default: '#efeee5', label: '次级背景' },
      ink: { default: '#1f1d18', label: '正文墨色' },
      accent: { default: '#1B365D', label: '墨蓝色点缀' },
      muted: { default: '#6b665b', label: '次要文字' },
      rule: { default: '#d4d1c5', label: '分割线' },
      tag: { default: '#e8e5de', label: '标签背景' },
    },
    palettes: [
      {
        id: 'ink-classic',
        name: '墨水经典',
        match: ['仙侠', '武侠', '古风', '历史'],
        css: {
          bg: '#f5f1e8',
          paper: '#f0ead8',
          ink: '#1f1d18',
          accent: '#2d5a3d',
          muted: '#6b665b',
          rule: '#d4d1c5',
          tag: '#e8e5de',
        },
      },
      {
        id: 'indigo-porcelain',
        name: '靛蓝瓷',
        match: ['修仙', '玄幻', '奇幻', '宫廷'],
        css: {
          bg: '#f1f3f5',
          paper: '#e4e8ec',
          ink: '#0a1f3d',
          accent: '#1B365D',
          muted: '#6b7280',
          rule: '#c8ccd4',
          tag: '#e0e4ea',
        },
      },
      {
        id: 'cinnabar-red',
        name: '朱砂印',
        match: ['悬疑', '灵异', '民俗', '志怪'],
        css: {
          bg: '#f5ede0',
          paper: '#efe6d6',
          ink: '#1a1008',
          accent: '#c0392b',
          muted: '#7a6a5a',
          rule: '#d4c8b8',
          tag: '#eae0d0',
        },
      },
      {
        id: 'forest-ink',
        name: '森林墨',
        match: ['种田', '田园', '自然', '慢生活'],
        css: {
          bg: '#f5f1e8',
          paper: '#ece7da',
          ink: '#1a2e1f',
          accent: '#4a7a5a',
          muted: '#5a6a4a',
          rule: '#d0ccc0',
          tag: '#e4e0d4',
        },
      },
      {
        id: 'gold-leaf',
        name: '金箔笺',
        match: ['宫廷', '权谋', '华丽', '优雅'],
        css: {
          bg: '#f5efe0',
          paper: '#efe8d6',
          ink: '#1a1410',
          accent: '#b8860b',
          muted: '#8a7a5a',
          rule: '#d8d0bc',
          tag: '#eae4d0',
        },
      },
    ],
  },

  // ============================
  // 杂志卡片骨架（浅色·网格·干净）
  // ============================
  magazine: {
    name: '杂志卡片',
    description: '浅色背景 + 网格布局 + 干净现代',
    tokens: {
      bg: { default: '#fafafa', label: '背景' },
      card: { default: '#ffffff', label: '卡片' },
      accent: { default: '#3b82f6', label: '强调色' },
      text: { default: '#1a1a2e', label: '正文' },
      muted: { default: '#64748b', label: '次要文字' },
      dim: { default: '#94a3b8', label: '最弱文字' },
      border: { default: '#e2e8f0', label: '边框' },
      shadow: { default: 'rgba(0,0,0,.06)', label: '阴影' },
    },
    palettes: [
      {
        id: 'steel-blue',
        name: '都市冷调蓝',
        match: ['都市', '职场', '现言', '商战'],
        css: {
          bg: '#f8fafc',
          card: '#ffffff',
          accent: '#3b82f6',
          text: '#1e293b',
          muted: '#64748b',
          dim: '#94a3b8',
          border: '#e2e8f0',
          shadow: 'rgba(0,0,0,.06)',
        },
      },
      {
        id: 'warm-pink',
        name: '暖粉甜梦',
        match: ['甜宠', '恋爱', '校园', '青春'],
        css: {
          bg: '#fef8f8',
          card: '#ffffff',
          accent: '#ec4899',
          text: '#2d1b2e',
          muted: '#9d6b7e',
          dim: '#c49aae',
          border: '#fce7f0',
          shadow: 'rgba(236,72,153,.04)',
        },
      },
      {
        id: 'forest-green',
        name: '碧水春山',
        match: ['种田', '田园', '治愈', '美食'],
        css: {
          bg: '#f6faf6',
          card: '#ffffff',
          accent: '#059669',
          text: '#0d2818',
          muted: '#4a7a5e',
          dim: '#8aaa9e',
          border: '#dcfce7',
          shadow: 'rgba(5,150,105,.04)',
        },
      },
      {
        id: 'sunset-orange',
        name: '落日橘红',
        match: ['热血', '冒险', '竞技', '成长'],
        css: {
          bg: '#fefaf5',
          card: '#ffffff',
          accent: '#f97316',
          text: '#2d1a0a',
          muted: '#8a6a4a',
          dim: '#b59a7a',
          border: '#ffedd5',
          shadow: 'rgba(249,115,22,.04)',
        },
      },
      {
        id: 'lavender-mist',
        name: '雾紫薰衣',
        match: ['奇幻', '西幻', '魔法', '异世界'],
        css: {
          bg: '#faf8fe',
          card: '#ffffff',
          accent: '#8b5cf6',
          text: '#1a0a2e',
          muted: '#6a4a8a',
          dim: '#a08ab5',
          border: '#ede9fe',
          shadow: 'rgba(139,92,246,.04)',
        },
      },
    ],
  },

  // ============================
  // 档案线索板骨架（关系图谱专用）
  // ============================
  dossier: {
    name: '档案线索板',
    description: '暖米色 + 橙色档案标签 + 间谍悬疑风',
    tokens: {
      paper: { default: '#f7f3ed', label: '纸面' },
      accent: { default: '#ea580c', label: '档案标签' },
      ink: { default: '#1c1917', label: '正文' },
      muted: { default: '#78716c', label: '次要文字' },
      line: { default: '#e7e5e4', label: '连接线' },
    },
    palettes: [
      {
        id: 'orange-spy',
        name: '橘色密档',
        match: ['悬疑', '谍战', '探案', '诡异'],
        css: {
          paper: '#f7f3ed',
          accent: '#ea580c',
          ink: '#1c1917',
          muted: '#78716c',
          line: '#e7e5e4',
        },
      },
      {
        id: 'blood-ink',
        name: '血墨卷宗',
        match: ['诡异', '惊悚', '刑侦', '犯罪'],
        css: {
          paper: '#f5ece6',
          accent: '#b91c1c',
          ink: '#1f0a0a',
          muted: '#7a4a4a',
          line: '#e0d4cc',
        },
      },
      {
        id: 'sage-green',
        name: '碧色密函',
        match: ['仙侠', '古风', '权谋', '历史'],
        css: {
          paper: '#f0f2ec',
          accent: '#4a7a5a',
          ink: '#141a10',
          muted: '#5a6a5a',
          line: '#dce0d4',
        },
      },
      {
        id: 'indigo-file',
        name: '靛蓝案卷',
        match: ['侦探', '推理', '智斗', '法律'],
        css: {
          paper: '#eef0f5',
          accent: '#1e40af',
          ink: '#0f172a',
          muted: '#4a5a7a',
          line: '#d8dce8',
        },
      },
      {
        id: 'dark-chocolate',
        name: '黑咖档案',
        match: ['都市', '黑道', '硬汉', '暗黑'],
        css: {
          paper: '#e8e2da',
          accent: '#78350f',
          ink: '#1c1410',
          muted: '#5a4a3a',
          line: '#d4cec4',
        },
      },
    ],
  },
};

// ─── 小说类型 → (骨架, 调色板) 路由映射 ────────────────────────

// ============================
// 紫色光晕骨架（百科·紫调变体）
// ============================
PALETTES['purple-orb'] = {
  name: '紫色光晕',
  description: '深色背景 + 紫色/蓝色光晕 + 毛玻璃卡片',
  tokens: {
    bg: { default: '#06070a', label: '背景' },
    accent: { default: '#7c5cff', label: '主色调' },
    text: { default: '#f2f4f8', label: '正文' },
    muted: { default: '#9ca6b5', label: '次要文字' },
    line: { default: 'rgba(255,255,255,.06)', label: '分割线' },
  },
  palettes: [
    {
      id: 'purple-magic',
      name: '紫韵流光',
      match: ['奇幻', '玄幻', '仙侠', '魔法'],
      css: { bg: '#06070a', accent: '#7c5cff', text: '#f2f4f8', muted: '#9ca6b5', line: 'rgba(255,255,255,.06)' },
    },
    {
      id: 'rose-dawn',
      name: '玫瑰晨曦',
      match: ['甜宠', '恋爱', '古言'],
      css: { bg: '#0a0608', accent: '#e8799f', text: '#f5f0f2', muted: '#b59aa5', line: 'rgba(255,255,255,.06)' },
    },
    {
      id: 'sapphire-night',
      name: '蓝宝石之夜',
      match: ['都市', '悬疑', '谍战'],
      css: { bg: '#060810', accent: '#3b82f6', text: '#f0f2f8', muted: '#8a9ab5', line: 'rgba(255,255,255,.06)' },
    },
  ],
};

// ============================
// 角色卡片集骨架
// ============================
PALETTES['card-deck'] = {
  name: '角色卡片集',
  description: '全屏滚动卡片 + 光晕背景',
  tokens: {
    bg: { default: '#06070a', label: '背景' },
    accent: { default: '#7c5cff', label: '角色色' },
    text: { default: '#f2f4f8', label: '正文' },
    muted: { default: '#9ca6b5', label: '次要' },
    cardBg: { default: 'rgba(20,24,36,.78)', label: '卡片背景' },
  },
  palettes: [
    {
      id: 'purple-aura',
      name: '紫光幻影',
      match: ['奇幻', '玄幻', '仙侠'],
      css: { bg: '#06070a', accent: '#7c5cff', text: '#f2f4f8', muted: '#9ca6b5', cardBg: 'rgba(20,24,36,.78)' },
    },
    {
      id: 'golden-radiance',
      name: '金色荣光',
      match: ['权谋', '宫廷', '史诗'],
      css: { bg: '#0a0806', accent: '#d4a854', text: '#f5f0e0', muted: '#b5a07a', cardBg: 'rgba(30,24,16,.78)' },
    },
    {
      id: 'ocean-deep',
      name: '深海幽蓝',
      match: ['悬疑', '克苏鲁', '神秘'],
      css: { bg: '#060a0e', accent: '#2d8793', text: '#e0f0f5', muted: '#7aaab5', cardBg: 'rgba(10,20,30,.78)' },
    },
  ],
};

// ============================
// 状态追踪看板骨架
// ============================
PALETTES['status-board'] = {
  name: '状态追踪看板',
  description: '深色表格 + 阶段切换 + 维度筛选',
  tokens: {
    bg: { default: '#06070a', label: '背景' },
    card: { default: '#0c1018', label: '卡片' },
    text: { default: '#f2f4f8', label: '正文' },
    accent: { default: '#58a6ff', label: '强调' },
  },
  palettes: [
    {
      id: 'standard-dark',
      name: '深色标准',
      match: ['通用'],
      css: { bg: '#06070a', card: '#0c1018', text: '#f2f4f8', accent: '#58a6ff' },
    },
    {
      id: 'ember-glow',
      name: '余烬暖光',
      match: ['仙侠', '武侠', '古风'],
      css: { bg: '#0a0806', card: '#14100a', text: '#f5f0e0', accent: '#d48a3a' },
    },
  ],
};

// ============================
// 叙事时间线骨架
// ============================
PALETTES['narrative'] = {
  name: '叙事时间线',
  description: '横向时间线 + 甘特图弧段 + 字数折线',
  tokens: {
    bg: { default: '#06070a', label: '背景' },
    text: { default: '#f2f4f8', label: '正文' },
    muted: { default: '#9ca6b5', label: '次要' },
  },
  palettes: [
    {
      id: 'timeline-dark',
      name: '暗色时间线',
      match: ['通用'],
      css: { bg: '#06070a', text: '#f2f4f8', muted: '#9ca6b5' },
    },
  ],
};

// ============================
// 画布世界地图骨架
// ============================
PALETTES['canvas-map'] = {
  name: '画布世界地图',
  description: 'Canvas地图 + 多层级世界',
  tokens: {
    bg: { default: '#0b0e14', label: '背景' },
    accent: { default: '#7c5cff', label: '强调' },
    text: { default: '#e4dcc8', label: '文字' },
  },
  palettes: [
    {
      id: 'world-dark',
      name: '深色世界',
      match: ['通用'],
      css: { bg: '#0b0e14', accent: '#7c5cff', text: '#e4dcc8' },
    },
    {
      id: 'scroll-map',
      name: '古卷地图',
      match: ['仙侠', '古风', '历史'],
      css: { bg: '#1a1410', accent: '#d4a854', text: '#e8dcc8' },
    },
  ],
};

// ============================
// 世界观星系图骨架
// ============================
PALETTES['galaxy'] = {
  name: '世界观星系图',
  description: 'D3.js力导向星系图 + 多层次概念网络',
  tokens: {
    bg: { default: '#0a0a14', label: '背景' },
    accent: { default: '#7c5cff', label: '核心色' },
    text: { default: '#e8d5b7', label: '金色文字' },
  },
  palettes: [
    {
      id: 'galaxy-dark',
      name: '暗色星系',
      match: ['通用'],
      css: { bg: '#0a0a14', accent: '#7c5cff', text: '#e8d5b7' },
    },
    {
      id: 'nebula-purple',
      name: '紫色星云',
      match: ['奇幻', '玄幻'],
      css: { bg: '#0e0a18', accent: '#a855f7', text: '#e8dcc8' },
    },
  ],
};

// ============================
// D3星系图骨架
// ============================
PALETTES['d3-galaxy'] = {
  name: 'D3星系图',
  description: 'D3.js力导向多层概念星系',
  tokens: {
    bg: { default: '#0b0e14', label: '背景' },
    accent: { default: '#7c5cff', label: '核心色' },
    text: { default: '#e8d5b7', label: '文字' },
  },
  palettes: [
    {
      id: 'galaxy-purple',
      name: '紫色星系',
      match: ['通用'],
      css: { bg: '#0b0e14', accent: '#7c5cff', text: '#e8d5b7' },
    },
    {
      id: 'galaxy-blue',
      name: '蓝色星系',
      match: ['科幻', '都市'],
      css: { bg: '#0a0e1a', accent: '#3b82f6', text: '#e0e8f0' },
    },
  ],
};

// ============================
// 仙侠宗派骨架（关系图谱）
// ============================
PALETTES['xianxia-sect'] = {
  name: '仙侠宗派',
  description: '暖仿古纸 + 深红/墨绿强调 + 门派谱系',
  tokens: {
    surface: { default: '#f1eee5', label: '纸面' },
    panel: { default: '#fffaf0', label: '面板' },
    ink: { default: '#24211c', label: '墨色' },
    muted: { default: '#746d62', label: '次要' },
    accent: { default: '#b94b37', label: '主色' },
    accent2: { default: '#4f8778', label: '辅色' },
  },
  palettes: [
    { id: 'xianxia-classic', name: '经典仙侠', match: ['仙侠', '武侠', '古风'],
      css: { surface: '#f1eee5', panel: '#fffaf0', ink: '#24211c', muted: '#746d62', accent: '#b94b37', accent2: '#4f8778' } },
    { id: 'xianxia-gold', name: '金色古卷', match: ['宫廷', '权谋', '史诗'],
      css: { surface: '#f2ecdf', panel: '#fff9ed', ink: '#272118', muted: '#756753', accent: '#9f3d32', accent2: '#997736' } },
    { id: 'xianxia-forest', name: '碧色林间', match: ['种田', '田园', '自然'],
      css: { surface: '#eef0e8', panel: '#f8faf2', ink: '#1c2418', muted: '#5a6a52', accent: '#3a7a5a', accent2: '#6a8a5a' } },
  ],
};

// ============================
// 社交图谱骨架（关系图谱）
// ============================
PALETTES['social'] = {
  name: '社交图谱',
  description: '冷灰背景 + 青蓝强调 + 圆形头像网络',
  tokens: {
    surface: { default: '#f3f6f7', label: '纸面' },
    panel: { default: '#ffffff', label: '面板' },
    ink: { default: '#20252a', label: '墨色' },
    muted: { default: '#69737b', label: '次要' },
    accent: { default: '#2d8793', label: '主色' },
    accent2: { default: '#5d6fc8', label: '辅色' },
  },
  palettes: [
    { id: 'urban-default', name: '都市冷灰', match: ['都市', '现代', '职场'],
      css: { surface: '#f3f6f7', panel: '#ffffff', ink: '#20252a', muted: '#69737b', accent: '#2d8793', accent2: '#5d6fc8' } },
    { id: 'social-warm', name: '暖色社交', match: ['甜宠', '恋爱', '校园'],
      css: { surface: '#faf3f0', panel: '#fff8f5', ink: '#2a2020', muted: '#7a6a6a', accent: '#d56f5f', accent2: '#c85a7a' } },
    { id: 'cyber-social', name: '赛博社交', match: ['科幻', '赛博', '异能'],
      css: { surface: '#0e0e12', panel: '#1a1a24', ink: '#e0e0e8', muted: '#7a7a8a', accent: '#6c5ce7', accent2: '#00cec9' } },
  ],
};

// ============================
// 家族谱系骨架（关系图谱）
// ============================
PALETTES['family-tree'] = {
  name: '家族谱系',
  description: '羊皮纸色 + 深红/金色强调 + 家族族谱',
  tokens: {
    surface: { default: '#f2ecdf', label: '纸面' },
    panel: { default: '#fff9ed', label: '面板' },
    ink: { default: '#272118', label: '墨色' },
    muted: { default: '#756753', label: '次要' },
    accent: { default: '#9f3d32', label: '主色' },
    accent2: { default: '#997736', label: '辅色' },
  },
  palettes: [
    { id: 'family-default', name: '古典族谱', match: ['古风', '权谋', '历史'],
      css: { surface: '#f2ecdf', panel: '#fff9ed', ink: '#272118', muted: '#756753', accent: '#9f3d32', accent2: '#997736' } },
    { id: 'family-blue', name: '蓝血贵族', match: ['宫廷', '世家', '商战'],
      css: { surface: '#eef0f2', panel: '#f8f9fa', ink: '#1a202a', muted: '#5a6a7a', accent: '#1e40af', accent2: '#6a5a8a' } },
  ],
};

const GENRE_ROUTES = {
  '诡异':     { skeleton: 'abyss',     palette: 'blood-red' },
  '悬疑':     { skeleton: 'abyss',     palette: 'blood-red' },
  '惊悚':     { skeleton: 'abyss',     palette: 'blood-red' },
  '恐怖':     { skeleton: 'abyss',     palette: 'blood-red' },
  '克苏鲁':   { skeleton: 'abyss',     palette: 'deep-ocean' },
  '科幻':     { skeleton: 'abyss',     palette: 'cyber-purple' },
  '赛博':     { skeleton: 'abyss',     palette: 'cyber-purple' },
  '异能':     { skeleton: 'abyss',     palette: 'cyber-purple' },
  '系统':     { skeleton: 'abyss',     palette: 'cyber-purple' },
  '修仙':     { skeleton: 'scroll',    palette: 'ink-classic' },
  '仙侠':     { skeleton: 'scroll',    palette: 'ink-classic' },
  '武侠':     { skeleton: 'scroll',    palette: 'ink-classic' },
  '古风':     { skeleton: 'scroll',    palette: 'ink-classic' },
  '玄幻':     { skeleton: 'scroll',    palette: 'indigo-porcelain' },
  '奇幻':     { skeleton: 'magazine',  palette: 'lavender-mist' },
  '西幻':     { skeleton: 'magazine',  palette: 'lavender-mist' },
  '魔法':     { skeleton: 'magazine',  palette: 'lavender-mist' },
  '都市':     { skeleton: 'magazine',  palette: 'steel-blue' },
  '现言':     { skeleton: 'magazine',  palette: 'steel-blue' },
  '职场':     { skeleton: 'magazine',  palette: 'steel-blue' },
  '甜宠':     { skeleton: 'magazine',  palette: 'warm-pink' },
  '恋爱':     { skeleton: 'magazine',  palette: 'warm-pink' },
  '校园':     { skeleton: 'magazine',  palette: 'warm-pink' },
  '种田':     { skeleton: 'magazine',  palette: 'forest-green' },
  '田园':     { skeleton: 'magazine',  palette: 'forest-green' },
  '治愈':     { skeleton: 'magazine',  palette: 'forest-green' },
  '美食':     { skeleton: 'magazine',  palette: 'forest-green' },
  '热血':     { skeleton: 'magazine',  palette: 'sunset-orange' },
  '冒险':     { skeleton: 'magazine',  palette: 'sunset-orange' },
  '竞技':     { skeleton: 'magazine',  palette: 'sunset-orange' },
  '宫廷':     { skeleton: 'scroll',    palette: 'gold-leaf' },
  '权谋':     { skeleton: 'scroll',    palette: 'gold-leaf' },
  '历史':     { skeleton: 'scroll',    palette: 'ink-classic' },
  '民俗':     { skeleton: 'scroll',    palette: 'cinnabar-red' },
  '志怪':     { skeleton: 'scroll',    palette: 'cinnabar-red' },
  '灵异':     { skeleton: 'scroll',    palette: 'cinnabar-red' },
  '侦探':     { skeleton: 'dossier',   palette: 'indigo-file' },
  '推理':     { skeleton: 'dossier',   palette: 'indigo-file' },
  '刑侦':     { skeleton: 'dossier',   palette: 'blood-ink' },
  '犯罪':     { skeleton: 'dossier',   palette: 'blood-ink' },
  '谍战':     { skeleton: 'dossier',   palette: 'orange-spy' },
  '黑道':     { skeleton: 'dossier',   palette: 'dark-chocolate' },
  '硬汉':     { skeleton: 'dossier',   palette: 'dark-chocolate' },
  '暗黑':     { skeleton: 'dossier',   palette: 'dark-chocolate' },
};

// 兜底映射（当小说类型无法匹配时，按内容类型给出安全默认值）
const FALLBACK = {
  encyclopedia:  { skeleton: 'abyss',     palette: 'blood-red' },
  'relationship': { skeleton: 'dossier',   palette: 'orange-spy' },
  character:     { skeleton: 'card-deck',  palette: 'purple-aura' },
  timeline:      { skeleton: 'narrative',  palette: 'timeline-dark' },
  worldMap:      { skeleton: 'galaxy',     palette: 'galaxy-dark' },
  quote:         { skeleton: 'abyss',      palette: 'golden-ages' },
};

// ─── 核心 API ────────────────────────────────────────────────────

const paletteSystem = {

  /** 获取某骨架的某调色板的 CSS 变量 */
  get(skeletonId, paletteId) {
    const group = PALETTES[skeletonId];
    if (!group) return null;
    const p = group.palettes.find(p => p.id === paletteId);
    if (!p) return null;
    return {
      id: p.id,
      name: p.name,
      match: p.match,
      skeleton: skeletonId,
      skeletonName: group.name,
      css: { ...p.css },
      tokens: group.tokens,
    };
  },

  /** 获取某骨架的所有调色板列表 */
  list(skeletonId) {
    const group = PALETTES[skeletonId];
    if (!group) return [];
    return group.palettes.map(p => ({
      id: p.id,
      name: p.name,
      match: p.match,
      description: p.match.join(' / '),
    }));
  },

  /** list 的别名 */
  listSkeleton(skeletonId) {
    return this.list(skeletonId);
  },

  /** 生成完整的 CSS 变量字符串，注入到 HTML 的 :root */
  generateCSS(skeletonId, paletteId) {
    const p = this.get(skeletonId, paletteId);
    if (!p) return '';
    const vars = Object.entries(p.css)
      .map(([key, val]) => {
        const prefixed = `  --${skeletonId}-${key}: ${val};`;
        // 同时输出短名别名（兼容 showcase 原有的 var(--bg) 引用）
        const alias = `  --${key}: ${val};`;
        return prefixed + '\n' + alias;
      })
      .join('\n');
    return `:root {\n${vars}\n}`;
  },

  /** 根据小说类型自动匹配合适的骨架+调色板 */
  route(contentType, novelGenre) {
    if (novelGenre && GENRE_ROUTES[novelGenre]) {
      return { ...GENRE_ROUTES[novelGenre] };
    }
    // 尝试部分匹配
    if (novelGenre) {
      for (const [key, route] of Object.entries(GENRE_ROUTES)) {
        if (novelGenre.includes(key) || key.includes(novelGenre)) {
          return { ...route };
        }
      }
    }
    // 兜底
    return { ...(FALLBACK[contentType] || FALLBACK.encyclopedia) };
  },

  /** 返回所有骨架的注册表（供 UI 使用） */
  getRegistry() {
    const result = {};
    for (const [skeletonId, group] of Object.entries(PALETTES)) {
      result[skeletonId] = {
        id: skeletonId,
        name: group.name,
        description: group.description,
        tokens: group.tokens,
        palettes: group.palettes.map(p => ({
          id: p.id,
          name: p.name,
          match: p.match,
        })),
      };
    }
    return result;
  },

  /** 注入调色板 CSS 到 HTML 字符串 */
  injectPaletteCSS(html, skeletonId, paletteId) {
    const cssVars = this.generateCSS(skeletonId, paletteId);
    if (!cssVars) return html;
    // 替换已有的 :root 或插入到 <style> 中
    if (html.includes(':root {')) {
      return html.replace(/:root \{[\s\S]*?\}/, cssVars);
    }
    // 尝试在 </style> 前插入
    return html.replace('</style>', cssVars + '\n</style>');
  },
};

// 同时支持 require 和 browser 环境
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { paletteSystem, PALETTES, GENRE_ROUTES };
}
