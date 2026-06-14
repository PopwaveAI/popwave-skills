/**
 * core/analyzer.js — Node.js 内容分析器
 *
 * 检测两个维度：
 *   1. contentType — 内容的结构类型（encyclopedia / relationship / character / scene / timeline / quote）
 *   2. genre       — 小说题材类型（诡异 / 仙侠 / 甜宠 / 都市 / ...）
 *
 * 从文件名、文件路径和数据中的字段名综合判断。
 */

const path = require('path');

// ─── 内容类型信号 ────────────────────────────────────────────────

const CONTENT_SIGNALS = {
  // 百科全书
  categories:  { encyclopedia: 0.9 },
  CATEGORIES:  { encyclopedia: 0.9 },
  entries:     { encyclopedia: 0.7 },
  catKey:      { encyclopedia: 0.5 },

  // 关系图谱
  nodes:    { relationship: 0.9 },
  edges:    { relationship: 0.9 },
  source:   { relationship: 0.6 },
  target:   { relationship: 0.6 },

  // 角色卡
  characters: { character: 0.9 },
  character:  { character: 0.6 },
  traits:     { character: 0.4 },
  alias:      { character: 0.3 },

  // 场景卡
  scenes:  { scene: 0.9 },
  excerpt: { scene: 0.7 },
  mood:    { scene: 0.5 },

  // 金句卡
  quotes:  { quote: 0.9 },
  speaker: { quote: 0.7 },

  // 时间线
  timeline: { timeline: 0.9 },
  events:   { timeline: 0.8 },
  date:     { timeline: 0.4 },
};

// ─── 文件路径 → 内容类型 ─────────────────────────────────────────

const PATH_HINTS = [
  { pattern: /百科|encyclopedia/i,      type: 'encyclopedia' },
  { pattern: /关系|图谱|graph|network/i, type: 'relationship' },
  { pattern: /角色|character|人物|卡片/i,type: 'character' },
  { pattern: /场景|scene|场面/i,         type: 'scene' },
  { pattern: /金句|quote|名句/i,         type: 'quote' },
  { pattern: /时间|timeline|编年|叙事/i, type: 'timeline' },
  { pattern: /地图|世界|星系|map|world/i,type: 'worldMap' },
];

// ─── 文件路径 → 小说类型 ─────────────────────────────────────────

const GENRE_HINTS = [
  // 小说名关键词 → 类型
  { pattern: /诡异|恐怖|惊悚|怪谈|灵异/i,        genre: '诡异' },
  { pattern: /修仙|仙侠|修真|飞升/i,             genre: '修仙' },
  { pattern: /仙侠|武侠|江湖|武林/i,             genre: '仙侠' },
  { pattern: /甜宠|恋爱|纯爱|心动/i,             genre: '甜宠' },
  { pattern: /都市|职场|现言|商战/i,             genre: '都市' },
  { pattern: /科幻|赛博|异能|系统/i,             genre: '科幻' },
  { pattern: /悬疑|推理|侦探|刑侦/i,            genre: '悬疑' },
  { pattern: /奇幻|魔法|异世界|西幻/i,          genre: '奇幻' },
  { pattern: /种田|田园|慢生活/i,                genre: '种田' },
  { pattern: /权谋|宫廷|宫斗|争霸/i,             genre: '权谋' },
  // 目录名暗示
  { pattern: /诡异人生/i,                         genre: '诡异' },
  { pattern: /白月光/i,                           genre: '甜宠' },
];

// ─── 内容关键词 → 类型（在 JSON/MD 正文中搜索） ────────────────

const CONTENT_KEYWORDS = [
  { keywords: ['大雪山', '密藏域', '模拟器', '诡', '驭诡者'], type: 'encyclopedia', genre: '诡异' },
  { keywords: ['苏午', '丹加', '李岳山', '赤龙真人', '卓玛尊胜'], type: 'character', genre: '诡异' },
  { keywords: ['乔晚', '周衍', '沈溯微'], type: 'character', genre: '甜宠' },
  { keywords: ['师承', '盟友', '敌对', '派系'], type: 'relationship', genre: null },
];

// ─── 核心分析函数 ───────────────────────────────────────────────

function analyze(raw, filePath) {
  const result = {
    type: null,
    genre: null,
    title: null,
    confidence: 0,
    signals: [],
  };

  // 1. 从文件路径推断
  if (filePath) {
    const basename = path.basename(filePath);
    const dirname = path.dirname(filePath);

    // 小说类型
    for (const hint of GENRE_HINTS) {
      if (hint.pattern.test(basename) || hint.pattern.test(dirname)) {
        result.genre = hint.genre;
        break;
      }
    }

    // 内容类型
    for (const hint of PATH_HINTS) {
      if (hint.pattern.test(basename)) {
        result.type = hint.type;
        result.confidence = 0.6;
        break;
      }
    }
  }

  // 2. 如果是 JSON，扫描字段名
  let data = null;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    // 非 JSON
  }

  if (data && typeof data === 'object') {
    // 扫描顶层字段
    const topKeys = Object.keys(data);
    for (const key of topKeys) {
      const signals = CONTENT_SIGNALS[key];
      if (signals) {
        for (const [type, weight] of Object.entries(signals)) {
          result.signals.push({ key, type, weight });
          if (weight > result.confidence) {
            result.confidence = weight;
            result.type = type;
          }
        }
      }
    }

    // 如果有 title 字段
    if (data.title) {
      result.title = data.title;
    }

    // 从数据内容推断小说类型
    if (!result.genre) {
      const rawStr = JSON.stringify(data).slice(0, 5000);
      for (const ck of CONTENT_KEYWORDS) {
        const matched = ck.keywords.filter(k => rawStr.includes(k));
        if (matched.length >= 2) {
          result.genre = ck.genre;
          break;
        }
      }
    }
  }

  // 3. 如果还没有类型，扫描原始字符串中的关键词
  if (!result.type) {
    for (const ck of CONTENT_KEYWORDS) {
      const matchedCount = ck.keywords.filter(k => raw.includes(k)).length;
      if (matchedCount >= 3) {
        result.type = ck.type;
        if (ck.genre && !result.genre) result.genre = ck.genre;
        result.confidence = 0.5;
        break;
      }
    }
  }

  // 4. 兜底
  if (!result.type) {
    result.type = 'encyclopedia';
    result.confidence = 0.2;
  }

  return result;
}

module.exports = { analyze };
