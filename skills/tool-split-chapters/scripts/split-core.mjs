/**
 * tool-split-chapters · 分章归一纯函数核心模块
 *
 * 由 scripts/split-chapters.mjs 机械拆分而来（runner 注入限制单文件 ≤64KB）：
 * 字符归一、编码识别、标题识别、单资产分析、源清洗、边界修订、章节切分、范围与批次
 * 等纯函数区连同其常量与正则原样移入，行为与拆分前完全一致。
 * CLI 唯一入口仍是 scripts/split-chapters.mjs；本模块只被入口 import，不反向依赖入口。
 */

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";

/** 裁决与质量判定阈值（集中在这里，便于复核） */
const THRESHOLDS = {
  /** 未识别标题行占比阈值，超过即需要 Agent 裁决 */
  unrecognizedHeadingRatio: 0.05,
  /** 切出章数 / 预期章数 的下限比例 */
  detectedChapterRatio: 0.8,
  /** 置信度地板，低于即需要 Agent 裁决（覆盖「完全没识别到标题行」这类情形） */
  confidenceFloor: 0.6,
  /** 正文非空白字符少于此数记为 truncated（正文缺失或过短） */
  emptyBodyChars: 20,
  /** 正文前内容达到此长度时单独成章（否则只记录在 manifest.meta.leadingText） */
  prefaceMinChars: 200,
  /** 标题行最长字符数 */
  maxTitleChars: 40,
  /** 弱式数字标题（"12、标题"）至少出现多少行才采纳 */
  numberedHeadingMinLines: 3,
};

/**
 * 三档切批口径：档位名与产品交付物一一对应（标准 / 深度 / 骨架）。
 * - standard：六模块完整交付（默认），约 30 章/批
 * - deep：六模块完整交付、质量优先，每批 ≤20 章
 * - outline：卷级骨架交付（另一种交付物，不是更快的六模块），每批 ≤40 章
 * 任何档位每批均不超过 40 章。
 */
const BATCH_TIERS = {
  standard: { tier: "standard", label: "标准档", batchSize: 30, note: "六模块完整交付，约 30 章/批" },
  deep: { tier: "deep", label: "深度档", batchSize: 20, note: "六模块完整交付、质量优先，≤20 章/批" },
  outline: { tier: "outline", label: "骨架档", batchSize: 40, note: "卷级骨架交付（另一种交付物），≤40 章/批" },
};

class UsageError extends Error {}

/* ------------------------------------------------------------------ *
 * 文本归一
 * ------------------------------------------------------------------ */

/** 全角 ASCII（数字/字母/空格）转半角；中文标点（，。：等）保持原样，避免破坏正文 */
function toHalfwidthAscii(text) {
  let out = "";
  for (const ch of text) {
    const code = ch.codePointAt(0);
    if (code === 0x3000) {
      out += " ";
      continue;
    }
    if ((code >= 0xff10 && code <= 0xff19) || (code >= 0xff21 && code <= 0xff3a) || (code >= 0xff41 && code <= 0xff5a)) {
      out += String.fromCharCode(code - 0xfee0);
      continue;
    }
    out += ch;
  }
  return out;
}

/** CRLF / CR 统一为 LF，去掉 BOM 残留 */
function normalizeNewlines(text) {
  return text.replace(/^\uFEFF/, "").replace(/\r\n?/g, "\n");
}

/** 用于匹配的归一文本：全角 ASCII 半角化 + 去首尾空白 + 压缩连续空格 */
function normalizeForMatch(line) {
  return toHalfwidthAscii(line).trim().replace(/\s+/g, " ");
}

const DECORATION_CHARS = ">＞-–—_=+*~☆★◆◇■□▪▫〓·•。、，,.;；:：!！?？\"'“”‘’「」『』【】[]〔〕（）()《》<>|｜/\\";

function escapeForClass(text) {
  return text.replace(/[\\\]^[\-]/g, "\\$&");
}

const DECORATION_LEADING_RE = new RegExp(`^[${escapeForClass(DECORATION_CHARS)}\\s]+`, "u");
const DECORATION_TRAILING_RE = new RegExp(`[${escapeForClass(DECORATION_CHARS)}\\s]+$`, "u");

/** 去掉标题行两端的装饰性包裹（【】、（）、星号等），最多剥 4 层 */
function stripDecorations(text) {
  let current = text;
  for (let i = 0; i < 4; i += 1) {
    const next = current.replace(DECORATION_LEADING_RE, "").replace(DECORATION_TRAILING_RE, "");
    if (next === current) break;
    current = next;
  }
  return current;
}

/* ------------------------------------------------------------------ *
 * 编码识别
 * ------------------------------------------------------------------ */

const CJK_RE = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/u;
const CJK_SAMPLE_PUNCT = "，。！？：；“”‘’、（）《》〈〉—…·【】";
const LEGACY_LABELS = ["gbk", "gb18030", "big5"];

function decodeWith(buffer, label, fatal) {
  // 无 full-icu（small-icu）构建下 TextDecoder 会抛 RangeError，必须 try/catch
  const decoder = new TextDecoder(label, { fatal, ignoreBOM: true });
  return decoder.decode(buffer);
}

/** 解码可信度打分：合法字符占比高、替换字符（U+FFFD）少者胜 */
function plausibilityScore(text) {
  if (!text) return 0;
  let total = 0;
  let good = 0;
  let bad = 0;
  for (const ch of text) {
    total += 1;
    const code = ch.codePointAt(0);
    if (ch === "\n" || ch === "\r" || ch === "\t") {
      good += 1;
      continue;
    }
    if (code >= 0x20 && code < 0x7f) {
      good += 1;
      continue;
    }
    if (CJK_RE.test(ch) || CJK_SAMPLE_PUNCT.includes(ch)) {
      good += 1;
      continue;
    }
    if (ch === "\ufffd") {
      bad += 1;
      continue;
    }
    if (code > 0x7f) good += 0.5;
  }
  const denominator = Math.max(1, total);
  return good / denominator - (bad / denominator) * 3;
}

function looksLikeUtf16Le(buffer) {
  if (buffer.length < 4) return false;
  const sample = Math.min(buffer.length, 512);
  let oddZero = 0;
  let evenZero = 0;
  for (let i = 0; i + 1 < sample; i += 2) {
    if (buffer[i] === 0x00) evenZero += 1;
    if (buffer[i + 1] === 0x00) oddZero += 1;
  }
  const pairs = Math.floor(sample / 2) || 1;
  return oddZero / pairs > 0.6 && evenZero / pairs < 0.1;
}

/**
 * 编码识别：BOM 优先；否则先严格 UTF-8，失败后回退 gbk / gb18030 / big5（按可信度打分择优）。
 * 返回 { encoding, method, text, note }，method 用于可追溯。
 */
function decodeBuffer(buffer) {
  if (buffer.length >= 3 && buffer[0] === 0xef && buffer[1] === 0xbb && buffer[2] === 0xbf) {
    return { encoding: "utf-8", method: "bom", text: decodeWith(buffer.subarray(3), "utf-8", false), note: "" };
  }
  if (buffer.length >= 2 && buffer[0] === 0xff && buffer[1] === 0xfe) {
    return { encoding: "utf-16le", method: "bom", text: decodeWith(buffer.subarray(2), "utf-16le", false), note: "" };
  }
  if (buffer.length >= 2 && buffer[0] === 0xfe && buffer[1] === 0xff) {
    return { encoding: "utf-16be", method: "bom", text: decodeWith(buffer.subarray(2), "utf-16be", false), note: "" };
  }
  if (looksLikeUtf16Le(buffer)) {
    try {
      return { encoding: "utf-16le", method: "guess", text: decodeWith(buffer, "utf-16le", false), note: "按空字节分布猜测为 utf-16le" };
    } catch {
      /* 退化到后续分支 */
    }
  }

  try {
    return { encoding: "utf-8", method: "utf-8-strict", text: decodeWith(buffer, "utf-8", true), note: "" };
  } catch {
    /* UTF-8 严格解码失败，回退中文传统编码 */
  }

  const failures = [];
  const candidates = [];
  for (const label of LEGACY_LABELS) {
    try {
      const text = decodeWith(buffer, label, true);
      candidates.push({ label, text, score: plausibilityScore(text) });
    } catch (error) {
      failures.push(`${label}:${error instanceof Error ? error.message : String(error)}`);
    }
  }
  candidates.sort((left, right) => right.score - left.score);
  if (candidates.length) {
    const best = candidates[0];
    return {
      encoding: best.label,
      method: "fallback",
      text: best.text,
      note: candidates.length > 1 ? `候选打分：${candidates.map((item) => `${item.label}=${item.score.toFixed(2)}`).join(", ")}` : "",
    };
  }

  // 连 gbk/big5 都不可用（无 full-icu）：最后兜底并标记需人工确认
  return {
    encoding: "utf-8",
    method: "lossy",
    text: decodeWith(buffer, "utf-8", false),
    note: `无可用中文解码器，按非严格 UTF-8 兜底（${failures.join(" | ")}）`,
  };
}

/* ------------------------------------------------------------------ *
 * 标题识别
 * ------------------------------------------------------------------ */

const CN_NUMERALS = {
  零: 0, 〇: 0, 一: 1, 壹: 1, 二: 2, 贰: 2, 两: 2, 三: 3, 叁: 3, 四: 4, 肆: 4,
  五: 5, 伍: 5, 六: 6, 陆: 6, 七: 7, 柒: 7, 八: 8, 捌: 8, 九: 9, 玖: 9,
};
const CN_UNITS = { 十: 10, 拾: 10, 百: 100, 佰: 100, 千: 1000, 仟: 1000, 万: 10000 };

const CN_NUM_CHARS = "零〇一二三四五六七八九十百千万两壹贰叁肆伍陆柒捌玖拾佰仟";
const NUM_PATTERN = `(?:[0-9]{1,4}|[${CN_NUM_CHARS}]{1,8})`;
const CHAPTER_UNITS = "章节回话集幕";
const VOLUME_UNITS = "卷部篇册";

const CHAPTER_CN_RE = new RegExp(`^第\\s*(${NUM_PATTERN})\\s*[${CHAPTER_UNITS}]`);
const VOLUME_CN_RE = new RegExp(`^第\\s*(${NUM_PATTERN})\\s*[${VOLUME_UNITS}]`);
const CHAPTER_EN_RE = /^(?:chapter|chap\.?)\s*\.?\s*([0-9]{1,4})(?![0-9])/i;
const VOLUME_EN_RE = /^(?:volume|vol\.?)\s*\.?\s*([0-9]{1,4})(?![0-9])/i;
const VOLUME_PART_RE = /^(上|中|下|续)(部|卷|册|篇)$/;
const SPECIAL_CHAPTER_RE = /^(楔子|序章|序言|序幕|引子|前言|尾声|终章|结局|大结局|番外篇|番外|后记|外传|完本感言)/;
const SPECIAL_FOLLOW_RE = /^[\s:：、.．\-—·（(【[\d零〇一二三四五六七八九十百千两]/;
const NUMBERED_HEADING_RE = /^([0-9]{1,4})\s*[、．.·:：]\s*(\S.*)$/;
/** Markdown 标题前缀：#{1,6} + 可选空格（真实网文 TXT 常见排版） */
const MARKDOWN_HEADING_RE = /^(#{1,6})\s*(.*)$/;
/** 内部卷标记的完结标注（如「第一卷（完）」「（第三卷完）」） */
const VOLUME_COMPLETE_RE = /完/;
/** 盗版站标题残留后缀（按长到短匹配，且只在标题末尾命中才清理） */
const TITLE_RESIDUES = [
  "免费全文阅读",
  "全文免费阅读",
  "全本免费阅读",
  "无弹窗阅读",
  "手机版阅读",
  "免费阅读",
  "全文阅读",
  "无弹窗",
  "请记住本站",
  "记住本站",
  "一秒记住",
  "最新章节",
];
/** 残留后缀常见的尾部标点：只在紧随残留时一起剥离，单独出现不动 */
const TITLE_TRAILING_JUNK_RE = /[.。·、,，;；:：!！?？~～\-—_=+*|]+$/u;
/** 非章 Markdown 标题的类型猜测规则（谁先命中算谁） */
const NON_CHAPTER_TYPE_RULES = [
  { type: "side-story", re: /番外|外传|后记/ },
  { type: "author-note", re: /感言|通知|抱歉|关于|更新|汇报|推个书|推推|公告|卡牌|漫画|有声|新书|快乐|感谢|各位|书友|整理|直播|盟主|请假|晚点|身体|恢复|单章|上架/ },
];

/** 中文数字转阿拉伯数字，失败返回 null */
function chineseToNumber(text) {
  let total = 0;
  let section = 0;
  let digit = 0;
  let seen = false;
  for (const ch of text) {
    if (Object.prototype.hasOwnProperty.call(CN_NUMERALS, ch)) {
      digit = CN_NUMERALS[ch];
      seen = true;
      continue;
    }
    const unit = CN_UNITS[ch];
    if (!unit) return null;
    seen = true;
    if (unit === 10000) {
      section = (section + digit) * 10000;
      total += section;
      section = 0;
      digit = 0;
      continue;
    }
    if (digit === 0 && unit === 10) digit = 1;
    section += digit * unit;
    digit = 0;
  }
  if (!seen) return null;
  return total + section + digit;
}

function parseNumberToken(token) {
  if (/^[0-9]+$/.test(token)) return Number.parseInt(token, 10);
  return chineseToNumber(token);
}

/** 标题行是否「够短且不像句子」 */
function isHeadingShaped(probe, limit) {
  if (!probe || probe.length > limit) return false;
  if (/[。！？!?…~～]$/.test(probe)) return false;
  return true;
}

/** 无编号的特殊章标记（楔子/序章/番外…），要求后面跟分隔符或数字，避免把正文句子误判 */
function matchSpecialChapter(probe) {
  const match = probe.match(SPECIAL_CHAPTER_RE);
  if (!match) return null;
  const rest = probe.slice(match[0].length);
  if (rest && !SPECIAL_FOLLOW_RE.test(rest)) return null;
  if (probe.length > 30) return null;
  return { number: null, numberToken: null, unit: "special", level: "chapter" };
}

/**
 * 卷边界行后面只允许跟「短卷名」：不含句读、长度有限。
 * 用于把「第二卷写完了，嗯…那我就歇一天吧。」这类作者感言挡在卷边界之外。
 */
function isVolumeNameRest(rest) {
  if (rest.length > 20) return false;
  return !/[，。；：、！？…]/.test(rest);
}

/** 卷标记识别 */
function matchVolumeTitle(line) {
  const probe = headingProbe(line);
  if (!isHeadingShaped(probe, THRESHOLDS.maxTitleChars)) return null;
  const partMatch = probe.match(VOLUME_PART_RE);
  if (partMatch) return { number: null, numberToken: partMatch[1], unit: partMatch[2], level: "volume" };
  const enMatch = probe.match(VOLUME_EN_RE);
  if (enMatch) {
    if (!isVolumeNameRest(probe.slice(enMatch[0].length))) return null;
    return { number: Number.parseInt(enMatch[1], 10), numberToken: enMatch[1], unit: "volume", level: "volume" };
  }
  const cnMatch = probe.match(VOLUME_CN_RE);
  if (cnMatch) {
    if (!isVolumeNameRest(probe.slice(cnMatch[0].length))) return null;
    return { number: parseNumberToken(cnMatch[1]), numberToken: cnMatch[1], unit: "volume", level: "volume" };
  }
  return null;
}

/** 章标题识别；allowSpecial=false 时只认带编号的章标题（Markdown 标题无编号者判为非章标题） */
function matchChapterTitle(line, { allowSpecial = true } = {}) {
  const probe = headingProbe(line);
  if (!probe) return null;
  if (isHeadingShaped(probe, THRESHOLDS.maxTitleChars + 20)) {
    const cnMatch = probe.match(CHAPTER_CN_RE);
    if (cnMatch) return { number: parseNumberToken(cnMatch[1]), numberToken: cnMatch[1], unit: "chapter", level: "chapter" };
    const enMatch = probe.match(CHAPTER_EN_RE);
    if (enMatch) return { number: Number.parseInt(enMatch[1], 10), numberToken: enMatch[1], unit: "chapter", level: "chapter" };
  }
  if (!allowSpecial) return null;
  return matchSpecialChapter(probe);
}

/** 弱式数字标题（"12、标题"）候选 */
function matchNumberedHeading(line) {
  const probe = headingProbe(line);
  if (!probe) return null;
  const match = probe.match(NUMBERED_HEADING_RE);
  if (!match) return null;
  if (match[2].length > THRESHOLDS.maxTitleChars) return null;
  if (/[。！？!?…~～]$/.test(probe)) return null;
  return { number: Number.parseInt(match[1], 10), numberToken: match[1], unit: "numbered", rest: match[2] };
}

/* ------------------------------------------------------------------ *
 * 真实网文 TXT 排版补充能力
 *  - Markdown 标题前缀（#{1,6}）与加粗包裹（**第X章 xx**）
 *  - Markdown 标题无章节号 -> 非章标题（作者的话/公告/番外），不打断编号
 *  - 明文标题的盗版站残留后缀保守清理
 *  - 内部卷标记（第一卷（完））登记但不改「一个资产 = 一卷」建模
 * ------------------------------------------------------------------ */

function guessNonChapterType(title) {
  for (const rule of NON_CHAPTER_TYPE_RULES) if (rule.re.test(title)) return rule.type;
  return "other";
}

/**
 * 剥掉标题行的 Markdown 前缀（#{1,6}）与整行加粗包裹（`**第X章 xx**`）。
 * 只处理行首/行尾的标记字符，绝不动标题正文。
 */
function extractHeadingMarkup(line) {
  const trimmed = line.trim();
  const mdMatch = trimmed.match(MARKDOWN_HEADING_RE);
  const markdown = Boolean(mdMatch);
  let text = mdMatch ? mdMatch[2] : trimmed;
  let bold = false;
  if (text.startsWith("**")) {
    let next = text.slice(2);
    if (next.endsWith("**")) next = next.slice(0, -2);
    if (next.trim()) {
      text = next;
      bold = true;
    }
  } else if (text.endsWith("**")) {
    const next = text.slice(0, -2);
    if (next.trim()) {
      text = next;
      bold = true;
    }
  }
  return { text: text.trim(), markdown, bold };
}

/** 标题行归一探针：剥 Markdown/加粗标记 + 全角半角 + 装饰包裹，供各匹配器共用 */
function headingProbe(line) {
  return stripDecorations(normalizeForMatch(extractHeadingMarkup(line).text));
}

/** 派生存档标题：归一 + 保守清理已知盗版残留与紧邻尾部标点，返回 { title, residues } */
function deriveTitle(line, numberToken) {
  return cleanTitleResidue(normalizeTitle(extractHeadingMarkup(line).text), numberToken);
}

function cleanTitleResidue(rawTitle, numberToken) {
  let current = rawTitle.replace(/\s+/g, " ").trim();
  const residues = [];
  for (let pass = 0; pass < 4; pass += 1) {
    // 尾部标点只在「紧邻残留」时随残留一起剥，单独出现一律保留，避免误删正常标题文字
    const trimmed = current.replace(TITLE_TRAILING_JUNK_RE, "").trim();
    let matched = false;
    for (const residue of TITLE_RESIDUES) {
      if (!trimmed.endsWith(residue)) continue;
      const next = trimmed.slice(0, -residue.length).trim();
      if (!next) continue;
      residues.push(residue);
      current = next;
      matched = true;
      break;
    }
    if (!matched) break;
  }
  if (!current) return { title: rawTitle, residues: [] };
  // 保守守卫：清理后必须仍保留原编号 token，否则整条放弃（宁可留残留也不误删）
  if (numberToken && !current.includes(numberToken)) return { title: rawTitle, residues: [] };
  return { title: current, residues };
}

/** 内部卷标记识别（如「第一卷（完）」「（第三卷完）」）：命中即登记，不再当卷边界 */
function matchVolumeMarker(line) {
  const probe = headingProbe(line);
  if (!isHeadingShaped(probe, THRESHOLDS.maxTitleChars)) return null;
  if (!VOLUME_COMPLETE_RE.test(probe)) return null;
  const nameMatch = probe.match(new RegExp(`^(第\\s*(?:${NUM_PATTERN})\\s*[${VOLUME_UNITS}])`));
  if (!nameMatch) return null;
  // 只认「卷标记 + 完结标注」这种纯标记行；「第二卷写完了，…」这类作者感言要排除
  const leftover = stripDecorations(probe.slice(nameMatch[1].length))
    .replace(/完\s*结?|完结|终/g, "")
    .replace(/[\s.。·、,，;；:：!！?？~～\-—_=+*|]/gu, "");
  if (leftover) return null;
  return { name: nameMatch[1], complete: true, title: normalizeTitle(extractHeadingMarkup(line).text) };
}

/** 未识别但形似标题的行（用于算「未识别标题行占比」，也是 Agent 裁决的输入线索） */
function isLooseHeadingCandidate(line) {
  const probe = headingProbe(line);
  if (!isHeadingShaped(probe, THRESHOLDS.maxTitleChars)) return false;
  if (new RegExp(`^第\\s*[^\\s]{1,10}\\s*[${CHAPTER_UNITS}${VOLUME_UNITS}]`).test(probe)) return true;
  if (probe.length <= 12 && new RegExp(`^(?:[0-9]{1,4}\\s*)?[${CHAPTER_UNITS}${VOLUME_UNITS}]`).test(probe)) return true;
  if (/^(?:chapter|chap\.?|volume|vol\.?)\s*[^\s]{1,10}/i.test(probe)) return true;
  if (new RegExp(`^[^\\s]{1,6}[${VOLUME_UNITS}]$`).test(probe)) return true;
  if (probe.length <= 12 && SPECIAL_CHAPTER_RE.test(probe)) return true;
  return false;
}

/* ------------------------------------------------------------------ *
 * 单资产分析
 * ------------------------------------------------------------------ */

function normalizeTitle(line) {
  return toHalfwidthAscii(line).trim().replace(/\s+/g, " ");
}

const CONTAMINATION_PATTERNS = [
  { name: "site-notice", re: /请记住本站|记住本站|一秒记住|最新章节|全文阅读|无弹窗|手机版阅读/ },
  { name: "url", re: /(?:https?:\/\/|www\.)[^\s]{3,}/i },
  { name: "site-name", re: /(?:笔趣阁|顶点小说|新笔趣|书香门第|小说阅读网)/ },
];

function detectContamination(line) {
  for (const pattern of CONTAMINATION_PATTERNS) {
    const match = line.match(pattern.re);
    if (match) return { pattern: pattern.name, sample: match[0].slice(0, 60) };
  }
  return null;
}

function leadingTitleFromText(text) {
  const firstLine = text.split("\n").map((line) => line.trim()).find((line) => line.length > 0) ?? "";
  if (!firstLine) return "（正文前内容）";
  const probe = normalizeTitle(firstLine);
  if (!probe || probe.length > THRESHOLDS.maxTitleChars) return "（正文前内容）";
  // 首行是完整句子时不当作标题，避免把正文首句写成章名
  if (/[。！？!?…~～]$/.test(probe)) return "（正文前内容）";
  return probe;
}

/** 弱式数字标题：仅当出现足够多且编号大体递增时才采纳（避免把正文里的 "1、" 当章节） */
function shouldAdoptNumbered(candidates) {
  if (candidates.length < THRESHOLDS.numberedHeadingMinLines) return false;
  let increasing = 0;
  for (let i = 1; i < candidates.length; i += 1) {
    if (candidates[i].number > candidates[i - 1].number) increasing += 1;
  }
  return increasing / (candidates.length - 1) >= 0.8;
}

/* ------------------------------------------------------------------ *
 * 源清洗（确定性）
 *
 * 只做三件事，且全部可解释、可复现：
 *   1) drop-line  整行噪声（站点声明 / 报错浮层 / 压缩脚本 / 纯 URL / 推广行）
 *   2) trim       行内首尾噪声（分页标记、站点尾巴、行首域名）
 *   3) structure  结构改写（分页重复标题合并、目录块剔除）
 *
 * 保守红线：标题行永不整行删除；行内只切首尾；拿不准的只记 suspicion 不动手。
 * 默认不启用（--clean 才生效）；不启用时仍输出「可清洗项」预览供界面展示。
 * ------------------------------------------------------------------ */

const CLEANING_VERSION = 1;
const CLEANING_RULES_VERSION = "2026-10-09.1";
const CLEANING_SAMPLES_PER_RULE = 5;
const CLEANING_SAMPLES_TOTAL = 50;
const CLEANING_MAX_LINE_CHARS = 2000;
const CLEANING_RESIDUE_MAX = 12;
const CLEANING_OVERLAY_WINDOW = 12;
const CLEANING_OVERLAY_MIN_DISTINCT = 3;
const CLEANING_TOC_MIN_RUN = 3;
const CLEANING_TOC_BACKED_RATIO = 0.8;
const CLEANING_PAGE_DUPLICATE_MAX_GAP = 800;
const CLEANING_PAGE_TAG_RE = /[（(]\s*第\s*\d+\s*\/\s*\d+\s*页\s*[)）]/u;

/**
 * 整行噪声规则。命中后还要过两道闸才真删：
 *  - maxChars：整行超过这个长度就不删（可能是正文里夹了一句话），转 suspicion。
 *  - residueMax：命中片段之外的「非标点实义字」超过这个数就不删，避免「这是最新章节的标题」这类正文被误删。
 */
const CLEANING_DROP_RULES = [
  { id: "script-block", re: /<\/?(?:script|style)\b|!function\s*\(|\bvar\s+_idx\s*=|document\.write/iu, maxChars: null, residueMax: null },
  { id: "site-notice", re: /请记住本站|记住本站|一秒记住|最新章节|全文阅读|无弹窗|手机版阅读|本站首发|笔趣阁|顶点小说|新笔趣|书香门第|小说阅读网/u, maxChars: 40, residueMax: CLEANING_RESIDUE_MAX },
  { id: "promo-line", re: /(?:书友群|读者群|QQ群|qq群|微信群|公众号|加更群)\s*[群:：]?\s*\d{3,}|求收藏|求推荐票|求月票|求订阅|求打赏/u, maxChars: 40, residueMax: CLEANING_RESIDUE_MAX },
];

/** 盗版站报错浮层的固定文案：单行命中不算，窗口内命中 ≥3 个不同文案才整块删 */
const CLEANING_OVERLAY_TOKENS = [
  { id: "choose-error", re: /^请选择错误类型$/u },
  { id: "slow", re: /^更新太慢$/u },
  { id: "lack-chapter", re: /^缺少章节$/u },
  { id: "wrong-content", re: /^章节内容错误$/u },
  { id: "captcha", re: /^验证码[:：]?[^\s]{0,12}$/u },
  { id: "submit", re: /^提交$/u },
  { id: "close", re: /^关闭$/u },
];

/** 行内切除：只切行首 / 行尾，绝不切中间 */
const CLEANING_TRIM_TAIL_RULES = [
  { id: "page-tag", re: /\s*[（(]\s*第\s*\d+\s*\/\s*\d+\s*页\s*[)）]\s*$/u },
  { id: "site-tail", re: /\s*(?:请记住本站|记住本站|一秒记住|最新章节|全文阅读|无弹窗|手机版阅读)[^\s。！？!?…]*\s*$/u },
  { id: "url-tail", re: /\s+(?:https?:\/\/\S+|www\.\S+)\s*$/iu },
];
const CLEANING_TRIM_HEAD_RULES = [
  { id: "url-head", re: /^\s*(?:https?:\/\/\S+|www\.\S+)\s+/iu },
];
const CLEANING_URL_ONLY_RE = /^(?:https?:\/\/\S+|www\.\S+)$/iu;
const CLEANING_HEADING_PREFIX_RE = new RegExp(`^第\\s*(?:${NUM_PATTERN})\\s*[${CHAPTER_UNITS}${VOLUME_UNITS}]\\s*`, "u");
const CLEANING_PAGE_TAG_GLOBAL_RE = new RegExp(CLEANING_PAGE_TAG_RE.source, "gu");

/**
 * 标题比较键：剥掉「第X回」前缀与分页标记后再比。
 * 否则「第二十一回 …」与「第021回 …」会被当成两个不同标题，目录块与重复标题都识别不出来。
 */
function cleaningHeadingKey(line, chapter) {
  const title = deriveTitle(line, chapter.numberToken).title
    .replace(CLEANING_PAGE_TAG_GLOBAL_RE, "")
    .replace(/\s+/g, " ")
    .trim();
  return `${chapter.number ?? ""}#${title.replace(CLEANING_HEADING_PREFIX_RE, "").trim()}`;
}

/** 标题行受保护：整行删除与行内切除都不碰它（分页重复标题合并是唯一例外，见结构规则 3） */
function isProtectedHeadingLine(line) {
  return Boolean(matchChapterTitle(line) ?? matchVolumeTitle(line) ?? matchVolumeMarker(line));
}

/** 命中片段之外还剩多少实义字符（标点、符号、空白全部不计） */
function cleaningResidue(text, matched) {
  return text.replace(matched, "").replace(/[\s\p{P}\p{S}]/gu, "").length;
}

function createCleaningReport(applied) {
  return {
    applied: applied === true,
    version: CLEANING_VERSION,
    rulesVersion: CLEANING_RULES_VERSION,
    assetsChanged: 0,
    removedLines: 0,
    removedByRule: {},
    trimmedLines: 0,
    mergedPageDuplicates: 0,
    droppedTocBlocks: 0,
    droppedTocLines: 0,
    suspicion: [],
    samples: [],
    cleanedTextHash: null,
  };
}

function noteCleaningSample(report, rule, lineNo, before) {
  if (report.samples.length >= CLEANING_SAMPLES_TOTAL) return;
  if (report.samples.filter((item) => item.rule === rule).length >= CLEANING_SAMPLES_PER_RULE) return;
  report.samples.push({ line: lineNo, rule, before: before.trim().slice(0, 60) });
}

function noteCleaningRemoved(report, rule) {
  report.removedLines += 1;
  report.removedByRule[rule] = (report.removedByRule[rule] ?? 0) + 1;
}

/**
 * 对一个资产的归一文本做清洗，返回清洗后的文本与报告。
 * 纯函数：同输入必得同输出，便于幂等与复现。
 */
function applyCleaning(text) {
  const report = createCleaningReport(false);
  const source = text.split("\n");
  const dropped = new Set();

  // 1) 整行噪声
  for (let i = 0; i < source.length; i += 1) {
    const raw = source[i];
    const trimmed = raw.trim();
    if (!trimmed || trimmed.length > CLEANING_MAX_LINE_CHARS) continue;
    if (isProtectedHeadingLine(raw)) continue;

    if (!stripDecorations(normalizeForMatch(raw))) {
      dropped.add(i);
      noteCleaningRemoved(report, "decoration-only");
      noteCleaningSample(report, "decoration-only", i + 1, raw);
      continue;
    }
    if (CLEANING_URL_ONLY_RE.test(trimmed)) {
      dropped.add(i);
      noteCleaningRemoved(report, "url-only");
      noteCleaningSample(report, "url-only", i + 1, raw);
      continue;
    }
    for (const rule of CLEANING_DROP_RULES) {
      const match = trimmed.match(rule.re);
      if (!match) continue;
      if (rule.maxChars !== null && trimmed.length > rule.maxChars) {
        report.suspicion.push({ line: i + 1, rule: rule.id, reason: "命中噪声词但整行偏长，可能是正文", sample: trimmed.slice(0, 60) });
        break;
      }
      if (rule.residueMax !== null && cleaningResidue(trimmed, match[0]) > rule.residueMax) {
        report.suspicion.push({ line: i + 1, rule: rule.id, reason: "命中噪声词但正文占比过高，未删除", sample: trimmed.slice(0, 60) });
        break;
      }
      dropped.add(i);
      noteCleaningRemoved(report, rule.id);
      noteCleaningSample(report, rule.id, i + 1, raw);
      break;
    }
  }

  // 2) 报错浮层整块：窗口内命中 ≥3 个「不同」固定文案才认，避免误删正文里的单个词
  const overlayTokens = source.map((line) => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.length > 20) return -1;
    return CLEANING_OVERLAY_TOKENS.findIndex((token) => token.re.test(trimmed));
  });
  for (let i = 0; i < source.length; i += 1) {
    if (overlayTokens[i] < 0) continue;
    const hits = [];
    for (let j = i; j < Math.min(source.length, i + CLEANING_OVERLAY_WINDOW); j += 1) {
      if (overlayTokens[j] >= 0 && !dropped.has(j)) hits.push({ index: j, token: overlayTokens[j] });
    }
    if (new Set(hits.map((hit) => hit.token)).size < CLEANING_OVERLAY_MIN_DISTINCT) continue;
    let changed = false;
    for (const hit of hits) {
      if (dropped.has(hit.index)) continue;
      dropped.add(hit.index);
      noteCleaningRemoved(report, "error-overlay");
      changed = true;
    }
    if (changed) noteCleaningSample(report, "error-overlay", hits[0].index + 1, source[hits[0].index]);
  }

  // 3) 分页重复标题合并：同一回连续出现两次，且至少一侧带 (第N/N页) 分页标记（证据门）
  let previousHeading = null;
  for (let i = 0; i < source.length; i += 1) {
    if (dropped.has(i)) continue;
    const raw = source[i];
    const chapter = matchChapterTitle(raw);
    if (!chapter) continue;
    const hasPageTag = CLEANING_PAGE_TAG_RE.test(raw);
    const key = cleaningHeadingKey(raw, chapter);
    if (
      previousHeading &&
      previousHeading.key === key &&
      i - previousHeading.line <= CLEANING_PAGE_DUPLICATE_MAX_GAP &&
      (hasPageTag || previousHeading.hasPageTag)
    ) {
      dropped.add(i);
      report.mergedPageDuplicates += 1;
      noteCleaningSample(report, "page-duplicate", i + 1, raw);
      continue;
    }
    previousHeading = { key, line: i, hasPageTag };
  }

  // 4) 目录块：连续 ≥3 个「自身没有正文」的章标题，且这些标题在后文以「标题 + 正文」形式再次出现
  const bodyBackedTitles = new Set();
  const lineHasBody = source.map(() => false);
  for (let i = 0; i < source.length; i += 1) {
    if (dropped.has(i)) continue;
    const chapter = matchChapterTitle(source[i]);
    if (!chapter) continue;
    let j = i + 1;
    while (j < source.length && (!source[j].trim() || dropped.has(j))) j += 1;
    if (j >= source.length) continue;
    if (!matchChapterTitle(source[j]) && !matchVolumeTitle(source[j])) {
      lineHasBody[i] = true;
      bodyBackedTitles.add(cleaningHeadingKey(source[i], chapter));
    }
  }
  for (let i = 0; i < source.length; i += 1) {
    // 只从「自身没正文」的章标题起算目录；真章（后面跟着正文）永远不进目录块
    if (dropped.has(i) || lineHasBody[i] || !matchChapterTitle(source[i])) continue;
    const run = [i];
    let cursor = i;
    for (;;) {
      let k = cursor + 1;
      while (k < source.length && (!source[k].trim() || dropped.has(k))) k += 1;
      if (k >= source.length) break;
      // 遇到「后面跟着正文」的真章，目录块到此结束
      if (!matchChapterTitle(source[k]) || lineHasBody[k]) break;
      run.push(k);
      cursor = k;
    }
    if (run.length < CLEANING_TOC_MIN_RUN) continue;
    const backed = run.filter((index) => {
      const chapter = matchChapterTitle(source[index]);
      return chapter && bodyBackedTitles.has(cleaningHeadingKey(source[index], chapter));
    }).length;
    if (backed < Math.ceil(run.length * CLEANING_TOC_BACKED_RATIO)) continue;
    for (const index of run) {
      if (dropped.has(index)) continue;
      dropped.add(index);
      report.droppedTocLines += 1;
      noteCleaningSample(report, "toc-block", index + 1, source[index]);
    }
    report.droppedTocBlocks += 1;
  }

  // 5) 行内切除（只切首尾）+ 组装
  const out = [];
  for (let i = 0; i < source.length; i += 1) {
    if (dropped.has(i)) continue;
    const raw = source[i];
    if (!raw.trim()) {
      out.push(raw);
      continue;
    }
    // 标题行只允许剥「(第N/N页)」这一种无语义分页标记；其余首尾清洗一律不碰标题
    const rules = isProtectedHeadingLine(raw)
      ? CLEANING_TRIM_TAIL_RULES.filter((rule) => rule.id === "page-tag")
      : [...CLEANING_TRIM_HEAD_RULES, ...CLEANING_TRIM_TAIL_RULES];
    let next = raw;
    for (const rule of rules) next = next.replace(rule.re, "");
    if (next === raw) {
      out.push(raw);
      continue;
    }
    if (next.trim()) {
      report.trimmedLines += 1;
      noteCleaningSample(report, "trim", i + 1, raw);
      out.push(next);
    } else {
      noteCleaningRemoved(report, "trim");
      noteCleaningSample(report, "trim", i + 1, raw);
    }
  }

  const cleanedText = out.join("\n");
  report.cleanedTextHash = createHash("sha256").update(Buffer.from(cleanedText, "utf8")).digest("hex");
  return { text: cleanedText, report };
}

function mergeCleaningReports(reports, applied) {
  const merged = createCleaningReport(applied);
  for (const report of reports) {
    merged.assetsChanged += report.removedLines || report.trimmedLines || report.mergedPageDuplicates || report.droppedTocLines ? 1 : 0;
    merged.removedLines += report.removedLines;
    merged.trimmedLines += report.trimmedLines;
    merged.mergedPageDuplicates += report.mergedPageDuplicates;
    merged.droppedTocBlocks += report.droppedTocBlocks;
    merged.droppedTocLines += report.droppedTocLines;
    for (const [rule, count] of Object.entries(report.removedByRule)) {
      merged.removedByRule[rule] = (merged.removedByRule[rule] ?? 0) + count;
    }
    for (const item of report.suspicion) {
      if (merged.suspicion.length >= CLEANING_SAMPLES_TOTAL) break;
      merged.suspicion.push(item);
    }
    for (const item of report.samples) {
      if (merged.samples.length >= CLEANING_SAMPLES_TOTAL) break;
      if (merged.samples.filter((existing) => existing.rule === item.rule).length >= CLEANING_SAMPLES_PER_RULE) continue;
      merged.samples.push(item);
    }
  }
  if (applied) {
    merged.cleanedTextHash = createHash("sha256")
      .update(reports.map((report) => report.cleanedTextHash ?? "").join("|"), "utf8")
      .digest("hex");
  }
  return merged;
}

/** 分析一个资产：解码结果 -> 标题识别 + 候选收集 + 编码指纹 */
function analyzeAsset({ index, filePath, buffer, decoded }) {
  const text = normalizeNewlines(decoded.text);
  const lines = text.split("\n");
  const sha256 = createHash("sha256").update(buffer).digest("hex");

  const boundaries = [];
  const numberedCandidates = [];
  const looseCandidates = [];
  const nonChapterHeadings = [];
  const volumeMarkers = [];

  const pushChapterBoundary = (line, lineNo, match) => {
    const derived = deriveTitle(line, match.numberToken);
    boundaries.push({
      line: lineNo,
      level: "chapter",
      title: derived.title,
      titleResidues: derived.residues,
      number: match.number,
      numberToken: match.numberToken,
      unit: match.unit,
      weak: false,
      source: "script",
    });
  };

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (!line.trim()) continue;
    const lineNo = i + 1;
    const markup = extractHeadingMarkup(line);

    // 1) 内部卷标记（第一卷（完）/（第三卷完）…）：只登记，不建卷边界
    const volumeMarker = matchVolumeMarker(line);
    if (volumeMarker) {
      volumeMarkers.push({ line: lineNo, name: volumeMarker.name, complete: volumeMarker.complete, title: volumeMarker.title });
      continue;
    }
    // 2) 卷边界（「第一卷 风起卷」这类卷首标记）
    const volumeMatch = matchVolumeTitle(line);
    if (volumeMatch) {
      boundaries.push({ line: lineNo, level: "volume", title: deriveTitle(line, volumeMatch.numberToken).title, ...volumeMatch, weak: false, source: "script" });
      continue;
    }
    // 3) Markdown 标题：带章节号才建章边界；不带章节号的是作者的话/公告/番外，登记为非章标题，正文归入上一章
    if (markup.markdown) {
      const chapterMatch = matchChapterTitle(line, { allowSpecial: false });
      if (chapterMatch) {
        pushChapterBoundary(line, lineNo, chapterMatch);
        continue;
      }
      nonChapterHeadings.push({ line: lineNo, title: deriveTitle(line, null).title, type: guessNonChapterType(markup.text) });
      continue;
    }
    // 4) 明文标题行（含加粗包裹）：与既有口径一致
    const chapterMatch = matchChapterTitle(line);
    if (chapterMatch) {
      pushChapterBoundary(line, lineNo, chapterMatch);
      continue;
    }
    const numbered = matchNumberedHeading(line);
    if (numbered) {
      numberedCandidates.push({ line: lineNo, title: deriveTitle(line, null).title, ...numbered });
      continue;
    }
    if (isLooseHeadingCandidate(line)) {
      looseCandidates.push({ line: lineNo, text: normalizeTitle(line) });
    }
  }

  // 弱式数字标题兜底：只有在「没有任何强章边界」时才采纳，避免作者公告里的「1、2、3、」清单被当成章
  const hasStrongChapterBoundary = boundaries.some((item) => item.level === "chapter");
  const adoptedNumbered = !hasStrongChapterBoundary && shouldAdoptNumbered(numberedCandidates);
  if (adoptedNumbered) {
    for (const candidate of numberedCandidates) {
      boundaries.push({ line: candidate.line, level: "chapter", title: candidate.title, number: candidate.number, numberToken: candidate.numberToken, unit: "numbered", weak: true, source: "script" });
    }
  }
  boundaries.sort((left, right) => left.line - right.line);

  return {
    index,
    fileName: path.basename(filePath),
    filePath,
    sizeBytes: buffer.length,
    sha256,
    shortHash: sha256.slice(-8),
    encoding: decoded.encoding,
    encodingMethod: decoded.method,
    encodingNote: decoded.note,
    lines,
    text,
    boundaries,
    looseCandidates,
    numberedCandidates,
    adoptedNumbered,
    nonChapterHeadings,
    volumeMarkers,
  };
}

/* ------------------------------------------------------------------ *
 * 边界修订（Agent 裁决回灌）
 * ------------------------------------------------------------------ */

function revisionAssetKeyOf(op) {
  return op.asset ?? op.assetId ?? op.file ?? op.fileName ?? null;
}

function resolveRevisionAssetKey(op, assets) {
  const key = revisionAssetKeyOf(op);
  if (key === null || key === undefined || key === "") {
    return assets.length === 1 ? { asset: assets[0], status: "auto" } : { asset: null, status: "ambiguous" };
  }
  const asString = String(key);
  const byIndex = /^[0-9]+$/.test(asString) ? assets.find((asset) => asset.index + 1 === Number.parseInt(asString, 10)) : null;
  const found =
    byIndex ??
    assets.find((asset) => asset.assetId === asString) ??
    assets.find((asset) => asset.fileName === asString) ??
    assets.find((asset) => path.basename(asset.fileName, path.extname(asset.fileName)) === asString);
  return found ? { asset: found, status: "matched" } : { asset: null, status: "missing" };
}

/** 读取 revisions（内联 JSON 或文件），归一成扁平 ops 列表 */
async function loadRevisionOps(revisions) {
  if (!revisions) return { ops: [], source: "", warnings: [] };
  let text = "";
  if (revisions.source === "inline") {
    text = revisions.data;
  } else {
    try {
      text = await readFile(revisions.data, "utf8");
    } catch (error) {
      throw new UsageError(`--revisions 文件读取失败：${revisions.data}（${error instanceof Error ? error.message : String(error)}）`);
    }
  }
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch (error) {
    throw new UsageError(`--revisions 不是合法 JSON：${error instanceof Error ? error.message : String(error)}`);
  }

  const warnings = [];
  const ops = [];
  const pushTitleOverrides = (assetKey, overrides) => {
    for (const [chapterNo, title] of Object.entries(overrides)) {
      ops.push({ asset: assetKey, op: "rename", chapter: Number.parseInt(chapterNo, 10), title });
    }
  };

  if (Array.isArray(parsed)) {
    ops.push(...parsed);
  } else if (parsed && typeof parsed === "object") {
    if (Array.isArray(parsed.ops)) ops.push(...parsed.ops);
    if (Array.isArray(parsed.revisions)) ops.push(...parsed.revisions);
    if (Array.isArray(parsed.assets)) {
      for (const asset of parsed.assets) {
        const assetKey = asset.asset ?? asset.assetId ?? asset.file ?? asset.fileName;
        if (Array.isArray(asset.ops)) for (const op of asset.ops) ops.push({ asset: assetKey, ...op });
        if (Array.isArray(asset.revisions)) for (const op of asset.revisions) ops.push({ asset: assetKey, ...op });
        if (Array.isArray(asset.ranges)) for (const range of asset.ranges) ops.push({ asset: assetKey, op: "range", ...range });
        const overrides = asset.titleOverrides ?? asset.title_overrides ?? null;
        if (overrides && typeof overrides === "object") pushTitleOverrides(assetKey, overrides);
        const handled = Array.isArray(asset.ops) || Array.isArray(asset.revisions) || Array.isArray(asset.ranges) || overrides;
        if (!handled) warnings.push(`assets 条目没有可识别的操作：${JSON.stringify(asset).slice(0, 80)}`);
      }
    }
    const topOverrides = parsed.titleOverrides ?? parsed.title_overrides ?? null;
    if (topOverrides && typeof topOverrides === "object") pushTitleOverrides(undefined, topOverrides);
    if (!ops.length && !warnings.length) {
      warnings.push("revisions 里没有可识别的操作（支持 ops / revisions / assets[].ops / assets[].ranges / titleOverrides）");
    }
  } else {
    throw new UsageError("--revisions 顶层必须是数组或对象");
  }
  return { ops, source: revisions.source === "inline" ? "inline" : revisions.data, warnings };
}

function isRenameOp(op, explicitOp) {
  if (explicitOp === "rename") return true;
  if (op.line !== undefined || op.startLine !== undefined || op.start_line !== undefined) return false;
  return op.title !== undefined && (op.chapter !== undefined || op.chapterNo !== undefined || op.assetChapterNo !== undefined || op.globalNo !== undefined);
}

/** 把修订展开成「边界操作」与「改名操作」，range 展开成若干 split/merge */
function expandRevisionOps(rawOps) {
  const boundaryOps = [];
  const renameOps = [];
  for (const raw of rawOps) {
    const op = { ...raw };
    const explicitOp = typeof op.op === "string" ? op.op.toLowerCase() : typeof op.type === "string" ? op.type.toLowerCase() : "";

    if (explicitOp === "range") {
      const from = Number(op.from ?? op.fromLine ?? op.from_line);
      const to = Number(op.to ?? op.toLine ?? op.to_line);
      const inRange = (line) => (!Number.isFinite(from) || line >= from) && (!Number.isFinite(to) || line <= to);
      const items = Array.isArray(op.boundaries) ? op.boundaries : Array.isArray(op.rewrites) ? op.rewrites : [];
      for (const item of items) {
        const line = Number(item.line ?? item.startLine ?? item.start_line);
        if (!Number.isInteger(line) || !inRange(line)) continue;
        if (item.drop === true || item.op === "merge") {
          boundaryOps.push({ op: "merge", asset: revisionAssetKeyOf(op), line, range: { from, to } });
        } else {
          boundaryOps.push({ op: "split", asset: revisionAssetKeyOf(op), line, title: item.title, level: item.level, range: { from, to } });
        }
      }
      for (const line of Array.isArray(op.dropLines) ? op.dropLines : []) {
        const numeric = Number(line);
        if (!Number.isInteger(numeric) || !inRange(numeric)) continue;
        boundaryOps.push({ op: "merge", asset: revisionAssetKeyOf(op), line: numeric, range: { from, to } });
      }
      continue;
    }

    if (isRenameOp(op, explicitOp)) {
      renameOps.push({ ...op, op: "rename" });
      continue;
    }

    const line = Number(op.line ?? op.startLine ?? op.start_line);
    if (Number.isInteger(line) && line >= 1) {
      if (op.drop === true || explicitOp === "merge") {
        boundaryOps.push({ ...op, op: "merge", line });
      } else {
        boundaryOps.push({ ...op, op: "split", line });
      }
      continue;
    }
    renameOps.push({ ...op, op: "rename", __unknown: true });
  }
  return { boundaryOps, renameOps };
}

/** 对单资产应用边界修订（split / merge），返回 { boundaries, applied } */
function applyBoundaryOps(asset, boundaryOps) {
  const applied = [];
  const boundaries = asset.boundaries.map((item) => ({ ...item }));
  for (const op of boundaryOps) {
    const line = op.line;
    if (!Number.isInteger(line) || line < 1 || line > asset.lines.length) {
      applied.push({ op: op.op, asset: asset.assetId, line: Number.isInteger(line) ? line : null, status: "skipped", note: `行号超出文件范围（共 ${asset.lines.length} 行）` });
      continue;
    }
    if (op.op === "split") {
      const title = op.title !== undefined && op.title !== null ? normalizeTitle(String(op.title)) : normalizeTitle(asset.lines[line - 1] ?? "");
      if (!title) {
        applied.push({ op: "split", asset: asset.assetId, line, status: "skipped", note: "该行为空且未提供 title" });
        continue;
      }
      const level = op.level === "volume" ? "volume" : "chapter";
      const existing = boundaries.findIndex((item) => item.line === line);
      const nextBoundary = { line, level, title, number: null, numberToken: null, unit: "revision", weak: false, source: "revision" };
      if (existing >= 0) {
        boundaries[existing] = { ...boundaries[existing], ...nextBoundary, replaced: true };
      } else {
        boundaries.push(nextBoundary);
      }
      boundaries.sort((left, right) => left.line - right.line);
      applied.push({ op: "split", asset: asset.assetId, line, title, level, status: "applied", note: existing >= 0 ? "该行已有边界，按修订覆盖标题" : "" });
      continue;
    }
    if (op.op === "merge") {
      const index = boundaries.findIndex((item) => item.line === line);
      if (index < 0) {
        applied.push({ op: "merge", asset: asset.assetId, line, status: "skipped", note: "该行没有边界" });
        continue;
      }
      const removed = boundaries[index];
      if (index === 0 && removed.level === "chapter") {
        applied.push({ op: "merge", asset: asset.assetId, line, status: "skipped", note: "首个章边界不可合并（会丢失章节起点）" });
        continue;
      }
      boundaries.splice(index, 1);
      applied.push({ op: "merge", asset: asset.assetId, line, title: removed.title, level: removed.level, status: "applied", note: "" });
      continue;
    }
    applied.push({ op: op.op ?? "unknown", asset: asset.assetId, line, status: "skipped", note: "不支持的操作" });
  }
  return { boundaries, applied };
}

/* ------------------------------------------------------------------ *
 * 章节切分
 * ------------------------------------------------------------------ */

function makeChapter({ asset, title, startLine, endLine, boundary, kind, flagNoBoundary = false }) {
  const bodyLines = asset.lines.slice(startLine, endLine);
  const bodyText = bodyLines.join("\n").replace(/^\s*\n+/, "").replace(/\s+$/u, "");
  const flags = [];
  if (kind === "preface") flags.push("preface");
  if (kind === "special") flags.push("special-title");
  if (kind === "unsplit" || flagNoBoundary) flags.push("no-boundary");
  if (boundary?.weak) flags.push("weak-title");
  if (boundary?.source === "revision") flags.push("revision-boundary");
  if (Array.isArray(boundary?.titleResidues)) {
    for (const residue of boundary.titleResidues) flags.push(`title-residue:${residue}`);
  }
  if (asset.encodingMethod === "fallback" || asset.encodingMethod === "lossy") flags.push(`encoding:${asset.encodingMethod}`);

  const contaminationHits = [];
  for (const line of bodyLines.slice(0, 400)) {
    const hit = detectContamination(line);
    if (hit) contaminationHits.push(hit);
  }
  if (contaminationHits.length) flags.push("contamination");

  const chars = bodyText.replace(/\s/g, "").length;
  if (bodyText.trim().length === 0) flags.push("empty-body");
  else if (chars < THRESHOLDS.emptyBodyChars) flags.push("short-body");

  // 非章 Markdown 标题（作者的话/公告/番外）不建边界，其正文归入上一章：给该章打 flag 供审阅。
  // 覆盖范围是 [startLine, startLine + bodyLines.length]，比对外暴露的 endLine 多算一行（下一章的标题行之前）。
  const coveredEnd = startLine + bodyLines.length;
  const hasNonChapterHeading = (asset.nonChapterHeadings ?? []).some((item) => item.line >= startLine && item.line <= coveredEnd);
  if (hasNonChapterHeading) flags.push("contains-non-chapter-heading");

  return {
    assetId: asset.assetId,
    assetIndex: asset.index,
    assetChapterNo: 0,
    assetVolumeName: asset.defaultVolumeName,
    title,
    startLine,
    endLine: startLine + bodyLines.length - 1,
    bodyText,
    chars,
    flags,
    kind,
    number: boundary?.number ?? null,
    weakTitle: Boolean(boundary?.weak),
    contaminationHits,
  };
}

/** 从边界切出章节（含正文前内容与「完全无标题」兜底） */
function buildChapters(asset) {
  const lines = asset.lines;
  const boundaries = asset.boundaries;
  const chapters = [];
  const chapterBoundaries = boundaries.filter((item) => item.level === "chapter");
  let currentVolumeName = asset.defaultVolumeName;

  const firstChapter = chapterBoundaries[0] ?? null;
  const leadingEnd = firstChapter ? firstChapter.line - 1 : lines.length;
  const leadingText = lines.slice(0, Math.max(0, leadingEnd)).join("\n").replace(/\s+$/u, "");
  const leadingTrimmed = leadingText.trim();
  let leadingConsumed = leadingTrimmed.length === 0;

  if (!leadingConsumed && firstChapter && leadingTrimmed.length >= THRESHOLDS.prefaceMinChars) {
    // 只有「确实存在章边界」时，前面的长内容才叫正文前内容；否则整块正文走下面的兜底单章
    const chapter = makeChapter({ asset, title: leadingTitleFromText(leadingText), startLine: 1, endLine: Math.max(1, leadingEnd), boundary: null, kind: "preface" });
    chapter.volumeName = currentVolumeName;
    chapters.push(chapter);
    leadingConsumed = true;
  }

  for (let i = 0; i < boundaries.length; i += 1) {
    const boundary = boundaries[i];
    if (boundary.level === "volume") {
      currentVolumeName = boundary.title;
      continue;
    }
    const nextBoundary = boundaries.slice(i + 1).find((item) => item.line > boundary.line) ?? null;
    const endLine = nextBoundary ? Math.max(boundary.line, nextBoundary.line - 1) : lines.length;
    const chapter = makeChapter({
      asset,
      title: boundary.title,
      startLine: boundary.line,
      endLine,
      boundary,
      kind: boundary.unit === "special" ? "special" : "chapter",
    });
    chapter.volumeName = currentVolumeName;
    chapters.push(chapter);
  }

  if (!chapterBoundaries.length && !chapters.length && leadingTrimmed.length) {
    const chapter = makeChapter({ asset, title: leadingTitleFromText(leadingText), startLine: 1, endLine: lines.length, boundary: null, kind: "unsplit", flagNoBoundary: true });
    chapter.volumeName = currentVolumeName;
    chapters.push(chapter);
  }

  chapters.forEach((chapter, i) => {
    chapter.assetChapterNo = i + 1;
    chapter.assetVolumeName = chapter.volumeName ?? asset.defaultVolumeName;
    delete chapter.volumeName;
  });

  // 资产内的卷视图（按相邻同名合并）
  const assetVolumes = [];
  for (const chapter of chapters) {
    const last = assetVolumes[assetVolumes.length - 1];
    if (last && last.name === chapter.assetVolumeName) {
      last.chapterCount += 1;
      last.assetLocalEnd = chapter.assetChapterNo;
      continue;
    }
    assetVolumes.push({ name: chapter.assetVolumeName, assetLocalStart: chapter.assetChapterNo, assetLocalEnd: chapter.assetChapterNo, chapterCount: 1 });
  }

  return { chapters, assetVolumes, leadingText, leadingConsumed };
}

/** 逐资产质量检查：编号乱序、缺号、重复章名、正文缺失、污染、弱标题 */
function inspectQuality(asset, chapters) {
  const duplicated = [];
  const outOfOrder = [];
  const missing = [];
  const truncated = [];
  const contamination = [];
  const weakTitles = [];
  const byTitle = new Map();

  const numberedChapters = chapters.filter((chapter) => chapter.number !== null && Number.isInteger(chapter.number));
  let previousNumber = null;
  for (const chapter of numberedChapters) {
    if (previousNumber !== null && chapter.number <= previousNumber) {
      outOfOrder.push({ assetId: asset.assetId, chapterNo: chapter.assetChapterNo, title: chapter.title, expectedAtLeast: previousNumber + 1, actual: chapter.number });
      chapter.flags.push("out-of-order");
    }
    previousNumber = chapter.number;
  }
  for (let i = 1; i < numberedChapters.length; i += 1) {
    const gapBefore = numberedChapters[i - 1].number;
    const current = numberedChapters[i].number;
    if (current > gapBefore + 1) {
      const missingNumbers = [];
      for (let n = gapBefore + 1; n < current; n += 1) missingNumbers.push(n);
      // 缺号一律留痕：缺口再大也要记录（列表截断到 50 个，避免超大缺口撑爆产物）
      missing.push({ assetId: asset.assetId, afterChapterNo: numberedChapters[i - 1].assetChapterNo, missingNumbers: missingNumbers.slice(0, 50) });
      numberedChapters[i].flags.push(`missing-before:${missingNumbers[0]}`);
    }
  }

  for (const chapter of chapters) {
    const list = byTitle.get(chapter.title);
    if (list) list.push(chapter.assetChapterNo);
    else byTitle.set(chapter.title, [chapter.assetChapterNo]);
  }
  for (const [title, chapterNumbers] of byTitle.entries()) {
    if (chapterNumbers.length > 1) {
      duplicated.push({ assetId: asset.assetId, title, chapterNos: chapterNumbers });
      for (const chapter of chapters) {
        if (chapter.title === title && !chapter.flags.includes("duplicated-title")) chapter.flags.push("duplicated-title");
      }
    }
  }

  for (const chapter of chapters) {
    if (chapter.chars < THRESHOLDS.emptyBodyChars) {
      truncated.push({ assetId: asset.assetId, chapterNo: chapter.assetChapterNo, title: chapter.title, chars: chapter.chars });
    }
    if (chapter.weakTitle) weakTitles.push({ assetId: asset.assetId, chapterNo: chapter.assetChapterNo, title: chapter.title });
    if (chapter.contaminationHits.length) {
      contamination.push({ assetId: asset.assetId, chapterNo: chapter.assetChapterNo, pattern: chapter.contaminationHits[0].pattern, sample: chapter.contaminationHits[0].sample });
    }
  }

  return { duplicated, outOfOrder, missing, truncated, contamination, weakTitles };
}

/* ------------------------------------------------------------------ *
 * 范围与批次
 * ------------------------------------------------------------------ */

function selectRange({ options, totalChapters, volumes }) {
  if (options.scope === "full") {
    return { type: "full", from: 1, to: totalChapters, selectedChapters: totalChapters, selectedVolumes: volumes.length };
  }
  if (options.scope === "chapters") {
    const from = options.from ?? 1;
    const to = options.to ?? totalChapters;
    if (totalChapters === 0) throw new UsageError("范围校验失败：没有识别到任何章节，无法按章选择。");
    if (to > totalChapters) {
      throw new UsageError(`范围校验失败：本次输入共 ${totalChapters} 章，无法选择第 ${from}-${to} 章。请缩小 --to，或改用 --scope full。`);
    }
    if (from > totalChapters) throw new UsageError(`范围校验失败：本次输入共 ${totalChapters} 章，--from ${from} 超出范围。`);
    return { type: "chapters", from, to, selectedChapters: to - from + 1, selectedVolumes: null };
  }
  const from = options.from ?? 1;
  const to = options.to ?? volumes.length;
  if (volumes.length === 0) throw new UsageError("范围校验失败：没有识别到任何卷，无法按卷选择。");
  if (to > volumes.length) throw new UsageError(`范围校验失败：本次输入共 ${volumes.length} 卷，无法选择第 ${from}-${to} 卷。`);
  if (from > volumes.length) throw new UsageError(`范围校验失败：本次输入共 ${volumes.length} 卷，--from ${from} 超出范围。`);
  const selected = volumes.filter((volume) => volume.no >= from && volume.no <= to);
  return {
    type: "volume",
    from,
    to,
    selectedChapters: selected.reduce((sum, volume) => sum + volume.chapterCount, 0),
    selectedVolumes: selected.length,
    volumeNos: selected.map((volume) => volume.no),
  };
}

function isSelected(chapter, range) {
  if (range.type === "full") return true;
  if (range.type === "chapters") return chapter.globalNo >= range.from && chapter.globalNo <= range.to;
  return Array.isArray(range.volumeNos) && range.volumeNos.includes(chapter.volumeNo);
}

function computeBatches(chapters, tier) {
  const { batchSize } = BATCH_TIERS[tier];
  const batches = [];
  for (let i = 0; i < chapters.length; i += batchSize) {
    const slice = chapters.slice(i, i + batchSize);
    batches.push({
      batchNo: batches.length + 1,
      fromGlobalNo: slice[0].globalNo,
      toGlobalNo: slice[slice.length - 1].globalNo,
      chapterCount: slice.length,
      volumeNos: Array.from(new Set(slice.map((chapter) => chapter.volumeNo))),
      files: slice.map((chapter) => chapter.file),
    });
  }
  return {
    tier,
    label: BATCH_TIERS[tier].label,
    note: BATCH_TIERS[tier].note,
    batchSize: batchSize,
    totalChapters: chapters.length,
    batchCount: batches.length,
    batches,
  };
}

export {
  UsageError,
  THRESHOLDS,
  BATCH_TIERS,
  normalizeTitle,
  normalizeForMatch,
  decodeBuffer,
  applyCleaning,
  mergeCleaningReports,
  analyzeAsset,
  loadRevisionOps,
  expandRevisionOps,
  applyBoundaryOps,
  resolveRevisionAssetKey,
  revisionAssetKeyOf,
  buildChapters,
  inspectQuality,
  selectRange,
  isSelected,
  computeBatches,
};
