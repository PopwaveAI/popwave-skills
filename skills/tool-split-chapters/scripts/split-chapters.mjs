#!/usr/bin/env node
/**
 * tool-split-chapters · 分章归一（拆书链路第零期 T1.3）
 *
 * 设计约束（不要打破）：
 * 1. 纯 Node ESM，零第三方依赖，Node >= 20。
 * 2. 确定性：同一组输入 + 同一组参数，除 generatedAt 外产物逐字节一致；脚本不做任何模型调用。
 * 3. 主路径纯脚本分章（零 token），Agent 只在低置信度时裁决候选边界，并经 --revisions 回灌重跑。
 * 4. 源包（manifest + chapters + 索引 + 指纹 + 批次计划）永远由本脚本写出，Agent 不直接写源包。
 *
 * 产物（<out> 下）：
 *   manifest.json          章清单 / 卷边界 / 每章字数 / 质量问题 / encoding / confidence / 裁决标记 / revisions
 *   chapters/chNNN.txt     按章正文（首行为标题行）
 *   章节索引.json           逐资产的卷内序号视图
 *   合并章节索引.json       多资产按序拼接，每章带 globalNo / volumeLocalNo / assetId
 *   指纹.json               每资产 SHA-256 与后 8 位
 *   批次计划.json           三档切批（standard 约 30 章/批、deep ≤20、outline ≤40）
 */

import { createHash } from "node:crypto";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const SKILL_ID = "tool-split-chapters";
const SKILL_VERSION = "0.1.0";
const SCHEMA_VERSION = "1";

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

/** --profile 与生效档位的映射：档位名与交付物一一对应，故为恒等映射 */
const PROFILE_ACTIVE_TIER = { standard: "standard", deep: "deep", outline: "outline" };
const PROFILES = Object.keys(PROFILE_ACTIVE_TIER);
const SCOPES = ["full", "volume", "chapters"];

const EXIT_OK = 0;
const EXIT_RUNTIME = 1;
const EXIT_USAGE = 2;

class UsageError extends Error {}

/* ------------------------------------------------------------------ *
 * 参数解析
 * ------------------------------------------------------------------ */

const USAGE = `用法：node scripts/split-chapters.mjs --input <文件> [--input <文件> ...] --out <目录> [选项]

必填：
  --input <路径>            输入 TXT，可重复；每个 TXT 视为一卷资产
  --out <目录>              产物目录（--dry-run 时可省略）

选项：
  --profile <standard|deep|outline> 档位，默认 standard；deep 走「质量优先」六模块、outline 走「卷级骨架」交付物
  --reference-book-id <id>  参考书 ID，写入 manifest
  --title <书名>            书名，默认取首资产文件名
  --scope <full|volume|chapters>  范围类型，默认 full
  --from <N>                范围起始（scope=chapters 为章号，scope=volume 为卷号）
  --to <N>                  范围结束（含）
  --revisions <json|路径>   边界修订（行号区间 / 标题覆盖），内联 JSON 或 .json 文件路径
  --json                    以 JSON 输出运行摘要
  --dry-run                 只计算不写盘
  --clean                   先做确定性源清洗再分章（默认不洗，只输出「可清洗项」预览）
  --clean-out <目录>         把每个输入清洗后的完整正文写到该目录（需与 --clean 同用）
  --help                    显示用法

退出码：0 成功 / 1 运行期错误 / 2 参数或范围非法`;

function parseRevisionsArg(value) {
  const raw = String(value).trim();
  if (!raw) return null;
  if (raw.startsWith("{") || raw.startsWith("[")) {
    return { source: "inline", data: raw };
  }
  return { source: "file", data: path.resolve(process.cwd(), raw) };
}

function parseArgs(argv) {
  const options = {
    inputs: [],
    out: "",
    profile: "standard",
    referenceBookId: "",
    title: "",
    scope: "full",
    from: null,
    to: null,
    revisions: null,
    json: false,
    dryRun: false,
    clean: false,
    cleanOut: "",
    help: false,
  };

  const takeValue = (flag, index) => {
    const value = argv[index];
    if (value === undefined || value.startsWith("--")) {
      throw new UsageError(`参数 ${flag} 缺少取值`);
    }
    return value;
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    let flag = arg;
    let inlineValue = null;
    const eq = arg.indexOf("=");
    if (arg.startsWith("--") && eq > 2) {
      flag = arg.slice(0, eq);
      inlineValue = arg.slice(eq + 1);
    }
    const nextValue = () => {
      if (inlineValue !== null) return inlineValue;
      i += 1;
      return takeValue(flag, i);
    };

    switch (flag) {
      case "--input":
        options.inputs.push(nextValue());
        break;
      case "--out":
        options.out = nextValue();
        break;
      case "--profile":
        options.profile = nextValue();
        break;
      case "--reference-book-id":
        options.referenceBookId = nextValue();
        break;
      case "--title":
        options.title = nextValue();
        break;
      case "--scope":
        options.scope = nextValue();
        break;
      case "--from":
        options.from = Number.parseInt(nextValue(), 10);
        break;
      case "--to":
        options.to = Number.parseInt(nextValue(), 10);
        break;
      case "--revisions":
        options.revisions = parseRevisionsArg(nextValue());
        break;
      case "--json":
        options.json = true;
        break;
      case "--dry-run":
        options.dryRun = true;
        break;
      case "--clean":
        options.clean = true;
        break;
      case "--clean-out":
        options.cleanOut = nextValue();
        break;
      case "--help":
      case "-h":
        options.help = true;
        break;
      default:
        throw new UsageError(`未知参数：${arg}`);
    }
  }

  if (options.help) return options;
  if (!options.inputs.length) throw new UsageError("至少需要一个 --input");
  if (!PROFILES.includes(options.profile)) {
    throw new UsageError(`--profile 只支持 ${PROFILES.join(" | ")}，收到：${options.profile}`);
  }
  if (!SCOPES.includes(options.scope)) {
    throw new UsageError(`--scope 只支持 ${SCOPES.join(" | ")}，收到：${options.scope}`);
  }
  for (const [name, value] of [["--from", options.from], ["--to", options.to]]) {
    if (value !== null && (!Number.isInteger(value) || value < 1)) {
      throw new UsageError(`${name} 必须是 >= 1 的整数`);
    }
  }
  if (options.from !== null && options.to !== null && options.from > options.to) {
    throw new UsageError(`--from (${options.from}) 不能大于 --to (${options.to})`);
  }
  if (!options.dryRun && !options.out) {
    throw new UsageError("--out 为必填（--dry-run 时可省略）");
  }
  if (options.cleanOut && !options.clean) {
    throw new UsageError("--clean-out 只在 --clean 时有效，请同时加上 --clean");
  }
  if (options.dryRun && options.cleanOut) {
    throw new UsageError("--dry-run 与 --clean-out 不能同时使用");
  }
  return options;
}

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

/* ------------------------------------------------------------------ *
 * 产物组装
 * ------------------------------------------------------------------ */

function chapterFileName(globalNo, width) {
  return `ch${String(globalNo).padStart(width, "0")}.txt`;
}

function buildChapterIndex(manifest, assets, width) {
  return {
    generatedAt: manifest.generatedAt,
    referenceBookId: manifest.referenceBookId,
    totalChapters: manifest.totalChapters,
    assets: assets.map((asset) => ({
      assetId: asset.assetId,
      fileName: asset.fileName,
      encoding: asset.encoding,
      sha256: asset.sha256,
      shortHash: asset.shortHash,
      skippedAsDuplicate: Boolean(asset.skippedAsDuplicate),
      chapterCount: (asset.chapters ?? []).length,
      volumes: (asset.assetVolumes ?? []).map((volume) => ({ name: volume.name, fromLocalNo: volume.assetLocalStart, toLocalNo: volume.assetLocalEnd, chapterCount: volume.chapterCount })),
      chapters: (asset.chapters ?? []).map((chapter) => ({
        volumeLocalNo: chapter.assetChapterNo,
        volumeName: chapter.assetVolumeName,
        title: chapter.title,
        file: chapterFileName(chapter.globalNo, width),
        chars: chapter.chars,
        flags: chapter.flags,
      })),
    })),
  };
}

function buildMergedChapterIndex(manifest) {
  return {
    generatedAt: manifest.generatedAt,
    referenceBookId: manifest.referenceBookId,
    bookName: manifest.book.name,
    totalChapters: manifest.totalChapters,
    volumes: manifest.volumes,
    chapters: manifest.chapters.map((chapter) => ({
      globalNo: chapter.no,
      volumeNo: chapter.volumeNo,
      volumeLocalNo: chapter.volumeLocalNo,
      assetId: chapter.assetId,
      title: chapter.title,
      file: chapter.file,
      chars: chapter.chars,
      flags: chapter.flags,
      selected: chapter.selected,
    })),
  };
}

function buildFingerprints(fingerprints, assets, generatedAt) {
  const groups = new Map();
  for (const fingerprint of fingerprints) {
    const list = groups.get(fingerprint.sha256) ?? [];
    list.push(fingerprint.assetId);
    groups.set(fingerprint.sha256, list);
  }
  return {
    algorithm: "sha256",
    shortHashLength: 8,
    generatedAt: generatedAt,
    assets: fingerprints.map((fingerprint) => ({
      assetId: fingerprint.assetId,
      fileName: fingerprint.fileName,
      sizeBytes: fingerprint.sizeBytes,
      sha256: fingerprint.sha256,
      shortHash: fingerprint.shortHash,
      cleanedTextHash: fingerprint.cleanedTextHash ?? null,
      duplicateOf: fingerprint.duplicateOf ?? null,
      encoding: fingerprint.encoding,
      encodingMethod: fingerprint.encodingMethod,
      chapterCount: (assets.find((asset) => asset.assetId === fingerprint.assetId)?.chapters ?? []).length,
    })),
    duplicateGroups: Array.from(groups.entries())
      .filter(([, ids]) => ids.length > 1)
      .map(([sha256, assetIds]) => ({ sha256, shortHash: sha256.slice(-8), assetIds: assetIds })),
    uniqueCount: fingerprints.filter((fingerprint) => !fingerprint.duplicateOf).length,
  };
}

async function writeJson(filePath, value, written) {
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  written.push(path.basename(filePath));
}

function renderHumanSummary(summary, manifest) {
  const lines = [];
  lines.push(`分章归一完成${summary.dryRun ? "（dry-run，未写盘）" : ""}`);
  lines.push(`  源包目录：${summary.outDir ?? "（未指定）"}`);
  lines.push(`  总章数：${summary.totalChapters}　总字数：${summary.totalChars}`);
  lines.push(`  卷：${summary.volumes.map((volume) => `${volume.no}. ${volume.name}[${volume.from}-${volume.to}]`).join("　") || "（无）"}`);
  lines.push(`  编码：${summary.encodings.primary}（${Object.entries(summary.encodings.assets).map(([id, enc]) => `${id}=${enc}`).join(", ")}）`);
  lines.push(`  范围：${summary.scope.type} ${summary.scope.from}-${summary.scope.to}（选中 ${summary.scope.selectedChapters} 章）`);
  lines.push(`  置信度：${summary.confidence}　需要 Agent 裁决：${summary.agentArbitrationRequired ? "是" : "否"}`);
  for (const reason of summary.arbitrationReasons) lines.push(`    - ${reason}`);
  const q = summary.qualitySummary;
  lines.push(`  质量问题：缺号 ${q.missing}　重复章名 ${q.duplicated}　正文过短 ${q.truncated}　污染 ${q.contamination}　乱序 ${q.outOfOrder}　未识别标题行 ${q.unrecognizedHeadings}`);
  const c = summary.cleaning;
  if (c) {
    const detail = [
      c.removedLines ? `删整行 ${c.removedLines}` : "",
      c.trimmedLines ? `切首尾 ${c.trimmedLines}` : "",
      c.mergedPageDuplicates ? `合并分页重复标题 ${c.mergedPageDuplicates}` : "",
      c.droppedTocLines ? `剔除目录块 ${c.droppedTocBlocks} 块 / ${c.droppedTocLines} 行` : "",
    ].filter(Boolean).join("　");
    const verdict = c.applied ? "已应用" : "仅预览（未改盘）";
    const extra = c.suspicion.length ? `　待人工判断 ${c.suspicion.length} 处（见 manifest.cleaning.suspicion）` : "";
    lines.push(`  源清洗：${verdict}${detail ? `　${detail}` : "　无可清洗项"}${extra}`);
  }
  lines.push(`  非章标题：${summary.nonChapterHeadingCount}（见 manifest.nonChapterHeadings）　内部卷标记：${summary.volumeMarkerCount}（见 manifest.volumeMarkers）`);
  lines.push(`  批次计划（${summary.batchPlan.activeTier}）：${summary.batchPlan.batchCount} 批 × 每批 ≤${summary.batchPlan.batchSize} 章`);
  lines.push(`  产物：manifest.json / chapters(${manifest.totalChapters}) / 章节索引.json / 合并章节索引.json / 指纹.json / 批次计划.json`);
  if (summary.arbitrationReasons.length) {
    lines.push("  下一步：核对未识别的标题行与候选边界，再用 --revisions 回灌重跑。");
  }
  return `${lines.join("\n")}\n`;
}

/* ------------------------------------------------------------------ *
 * 主流程
 * ------------------------------------------------------------------ */

/**
 * 资产 ID：默认取文件名（去扩展名）。遇到同名资产时用指纹后 8 位区分，
 * 保证「同名不同文件」在合并索引与指纹表里各自可寻址。
 */
function resolveAssetId(fileName, sha256, used) {
  const base = path.basename(fileName, path.extname(fileName)).trim() || "asset";
  const sanitized = base.replace(/[\\/:*?"<>|\s]+/g, "-").replace(/^-+|-+$/g, "") || "asset";
  if (!used.has(sanitized)) {
    used.add(sanitized);
    return sanitized;
  }
  const hashBase = `${sanitized}~${sha256.slice(-8)}`;
  let candidate = hashBase;
  let suffix = 2;
  while (used.has(candidate)) {
    candidate = `${hashBase}-${suffix}`;
    suffix += 1;
  }
  used.add(candidate);
  return candidate;
}

/**
 * 跨资产（多卷）对齐分析：判断每个上传文件接在哪里、是否重叠、是否重复。
 *
 * 产出即「正文台账」的当前快照：每个上传文件 → 本书内的全书章号区间（xx 章-xx 章）。
 *
 * 判定口径：
 * - `first`       第一个可编号资产
 * - `continues`   本卷首章号 = 上卷末章号 + 1（干净续接）
 * - `restarts`    本卷从第一章重新开始（分卷文件常见排版，只记录，不报问题）
 * - `overlaps`    本卷首章号 ≤ 上卷末章号（真正重叠，疑似重复上传）
 * - `gap`         卷间断号（可能漏卷，也可能两卷之间本就没有连续章节）
 * - `unnumbered`  本卷标题无章节号，无法比对（链条在此断开）
 *
 * 跨卷同章名（`duplicates`）与 `overlaps` 都只作为确定性证据输出，
 * 由 Agent 裁决是不是同一本书、是不是重复上传。
 */
function analyzeCrossAsset(activeAssets) {
  const assets = activeAssets.map((asset) => {
    const chapters = asset.chapters ?? [];
    const numbers = chapters.map((chapter) => chapter.number).filter((value) => Number.isInteger(value));
    const globalNos = chapters.map((chapter) => chapter.globalNo);
    return {
      assetId: asset.assetId,
      fileName: asset.fileName,
      filePath: asset.filePath,
      shortHash: asset.shortHash,
      chapterCount: chapters.length,
      charCount: chapters.reduce((sum, chapter) => sum + chapter.chars, 0),
      fromGlobalNo: globalNos.length ? globalNos[0] : 0,
      toGlobalNo: globalNos.length ? globalNos[globalNos.length - 1] : 0,
      volumeNos: Array.from(new Set(chapters.map((chapter) => chapter.volumeNo))),
      firstNumber: numbers.length ? numbers[0] : null,
      lastNumber: numbers.length ? numbers[numbers.length - 1] : null,
      numberedChapters: numbers.length,
    };
  });

  const relations = [];
  let previous = null;
  for (const view of assets) {
    if (view.firstNumber === null) {
      relations.push({ assetId: view.assetId, previousAssetId: previous ? previous.assetId : null, kind: "unnumbered", previousLastNumber: null, currentFirstNumber: null, overlapChapters: 0, expectedFrom: null });
      previous = null;
      continue;
    }
    if (!previous) {
      relations.push({ assetId: view.assetId, previousAssetId: null, kind: "first", previousLastNumber: null, currentFirstNumber: view.firstNumber, overlapChapters: 0, expectedFrom: null });
      previous = view;
      continue;
    }
    let kind = "gap";
    if (view.firstNumber === 1 && previous.lastNumber > 1) kind = "restarts";
    else if (view.firstNumber <= previous.lastNumber) kind = "overlaps";
    else if (view.firstNumber === previous.lastNumber + 1) kind = "continues";
    relations.push({
      assetId: view.assetId,
      previousAssetId: previous.assetId,
      kind,
      previousLastNumber: previous.lastNumber,
      currentFirstNumber: view.firstNumber,
      overlapChapters: kind === "overlaps" ? previous.lastNumber - view.firstNumber + 1 : 0,
      expectedFrom: previous.lastNumber + 1,
    });
    previous = view;
  }

  // 跨资产重复章名：同一归一标题出现在不同上传文件里（卷内重名已由 quality.duplicated 覆盖）
  const titleMap = new Map();
  for (const asset of activeAssets) {
    for (const chapter of asset.chapters ?? []) {
      const key = normalizeForMatch(chapter.title);
      const list = titleMap.get(key) ?? [];
      list.push({ assetId: asset.assetId, globalNo: chapter.globalNo, assetChapterNo: chapter.assetChapterNo, number: chapter.number, title: chapter.title });
      titleMap.set(key, list);
    }
  }
  const duplicates = [];
  for (const [key, allOccurrences] of titleMap.entries()) {
    if (allOccurrences.length <= 1) continue;
    const assetIds = Array.from(new Set(allOccurrences.map((item) => item.assetId)));
    if (assetIds.length <= 1) continue;
    const numbers = allOccurrences.map((item) => item.number).filter((value) => Number.isInteger(value));
    duplicates.push({
      title: allOccurrences[0].title,
      key,
      assetIds,
      occurrenceCount: allOccurrences.length,
      occurrences: allOccurrences.slice(0, 10),
      sameNumber: numbers.length === allOccurrences.length && new Set(numbers).size === 1,
    });
  }

  return { assets, relations, duplicates };
}

async function run(argv) {
  const options = parseArgs(argv);
  if (options.help) {
    process.stdout.write(`${USAGE}\n`);
    return EXIT_OK;
  }

  // 1) 读入并归一每个资产
  const usedAssetIds = new Set();
  const assets = [];
  for (const [index, input] of options.inputs.entries()) {
    const filePath = path.resolve(process.cwd(), input);
    let buffer;
    try {
      buffer = await readFile(filePath);
    } catch (error) {
      throw new UsageError(`输入文件不可读：${input}（${error instanceof Error ? error.message : String(error)}）`);
    }
    const decoded = decodeBuffer(buffer);
    // 源清洗默认只出「可清洗项」预览；--clean 才真正把清洗结果交给分章。
    const cleaned = applyCleaning(decoded.text);
    cleaned.report.applied = options.clean;
    const asset = analyzeAsset({ index, filePath, buffer, decoded: { ...decoded, text: options.clean ? cleaned.text : decoded.text } });
    asset.cleaning = cleaned.report;
    asset.assetId = resolveAssetId(asset.fileName, asset.sha256, usedAssetIds);
    if (options.cleanOut) asset.cleanedText = cleaned.text;
    asset.defaultVolumeName = path.basename(asset.fileName, path.extname(asset.fileName)) || `第 ${index + 1} 卷`;
    assets.push(asset);
  }

  // 2) 读取并展开 revisions
  const revisionBundle = await loadRevisionOps(options.revisions);
  const { boundaryOps, renameOps } = expandRevisionOps(revisionBundle.ops);
  const revisionsApplied = revisionBundle.warnings.map((note) => ({ op: "load", asset: null, status: "skipped", note }));
  if (revisionBundle.source) {
    revisionsApplied.unshift({ op: "load", asset: null, status: "applied", note: `revisions 来源：${revisionBundle.source}，操作数 ${revisionBundle.ops.length}` });
  }

  // 3) 边界修订（split / merge / range）
  for (const asset of assets) {
    const ops = boundaryOps.filter((op) => resolveRevisionAssetKey(op, assets).asset === asset);
    if (!ops.length) continue;
    const result = applyBoundaryOps(asset, ops);
    asset.boundaries = result.boundaries;
    revisionsApplied.push(...result.applied);
  }
  for (const op of boundaryOps) {
    if (!resolveRevisionAssetKey(op, assets).asset) {
      revisionsApplied.push({ op: op.op, asset: revisionAssetKeyOf(op), line: op.line ?? null, status: "skipped", note: "未匹配到资产（单资产可省略 asset，多资产必须指定）" });
    }
  }
  // 修订过的行不再计入「未识别标题行」
  for (const asset of assets) {
    const boundaryLines = new Set(asset.boundaries.map((item) => item.line));
    asset.resolvedByRevision = asset.looseCandidates.filter((candidate) => boundaryLines.has(candidate.line)).length;
    asset.unresolvedLoose = asset.looseCandidates.filter((candidate) => !boundaryLines.has(candidate.line));
  }

  // 4) 切章 + 质量检查 + 指纹去重
  const quality = { missing: [], duplicated: [], truncated: [], contamination: [], outOfOrder: [], weakTitles: [], unrecognizedHeadings: [], encodingFallbacks: [] };
  const flatChapters = [];
  const flatVolumes = [];
  const fingerprints = [];
  const duplicateAssets = [];
  const seenHashes = new Map();
  let globalNo = 0;

  for (const asset of assets) {
    const fingerprint = {
      assetId: asset.assetId,
      fileName: asset.fileName,
      filePath: asset.filePath,
      sizeBytes: asset.sizeBytes,
      sha256: asset.sha256,
      shortHash: asset.shortHash,
      // 仅当本次真的清洗过，才记录清洗后文本指纹；否则为 null，避免"看起来洗过"
      cleanedTextHash: asset.cleaning?.applied ? asset.cleaning.cleanedTextHash : null,
      encoding: asset.encoding,
      encodingMethod: asset.encodingMethod,
      duplicateOf: null,
    };
    fingerprints.push(fingerprint);
    if (asset.encodingMethod === "fallback" || asset.encodingMethod === "lossy") {
      quality.encodingFallbacks.push({ assetId: asset.assetId, fileName: asset.fileName, encoding: asset.encoding, method: asset.encodingMethod, note: asset.encodingNote });
    }

    const duplicateOf = seenHashes.get(asset.sha256) ?? null;
    if (duplicateOf) {
      fingerprint.duplicateOf = duplicateOf;
      duplicateAssets.push({ assetId: asset.assetId, duplicateOf: duplicateOf, sha256: asset.sha256, shortHash: asset.shortHash });
      asset.skippedAsDuplicate = true;
      asset.chapters = [];
      asset.assetVolumes = [];
      continue;
    }
    seenHashes.set(asset.sha256, asset.assetId);

    const { chapters, assetVolumes, leadingText, leadingConsumed } = buildChapters(asset);
    asset.chapters = chapters;
    asset.assetVolumes = assetVolumes;
    asset.leadingText = leadingConsumed ? "" : leadingText;

    const assetQuality = inspectQuality(asset, chapters);
    quality.missing.push(...assetQuality.missing);
    quality.duplicated.push(...assetQuality.duplicated);
    quality.truncated.push(...assetQuality.truncated);
    quality.contamination.push(...assetQuality.contamination);
    quality.outOfOrder.push(...assetQuality.outOfOrder);
    quality.weakTitles.push(...assetQuality.weakTitles);
    for (const candidate of asset.unresolvedLoose) {
      quality.unrecognizedHeadings.push({ assetId: asset.assetId, line: candidate.line, text: candidate.text });
    }

    // 全局章号 / 卷号
    for (const chapter of chapters) {
      globalNo += 1;
      chapter.globalNo = globalNo;
      const name = chapter.assetVolumeName;
      let volume = flatVolumes[flatVolumes.length - 1];
      if (!volume || volume.assetId !== asset.assetId || volume.name !== name) {
        volume = { no: flatVolumes.length + 1, name, from: globalNo, to: globalNo, assetId: asset.assetId, chapterCount: 0 };
        flatVolumes.push(volume);
      }
      volume.to = globalNo;
      volume.chapterCount += 1;
      chapter.volumeNo = volume.no;
      chapter.volumeLocalNo = chapter.assetChapterNo;
      flatChapters.push(chapter);
    }
  }

  // 5) 标题覆盖（rename）
  for (const op of renameOps) {
    const resolved = resolveRevisionAssetKey(op, assets);
    if (!resolved.asset) {
      revisionsApplied.push({ op: "rename", asset: revisionAssetKeyOf(op), status: "skipped", note: "未匹配到资产" });
      continue;
    }
    const asset = resolved.asset;
    if (asset.skippedAsDuplicate) {
      revisionsApplied.push({ op: "rename", asset: asset.assetId, status: "skipped", note: "该资产被指纹去重跳过" });
      continue;
    }
    const chapterNo = Number(op.chapter ?? op.chapterNo ?? op.assetChapterNo ?? NaN);
    const target = Number.isInteger(chapterNo) ? asset.chapters.find((chapter) => chapter.assetChapterNo === chapterNo) : null;
    if (!target) {
      revisionsApplied.push({ op: "rename", asset: asset.assetId, chapter: Number.isInteger(chapterNo) ? chapterNo : null, status: "skipped", note: op.__unknown ? "无法识别的 rename 操作" : "未找到对应章（按资产内章序号定位）" });
      continue;
    }
    const previousTitle = target.title;
    target.title = normalizeTitle(String(op.title));
    target.flags.push("revision-title");
    revisionsApplied.push({ op: "rename", asset: asset.assetId, chapter: target.assetChapterNo, title: target.title, previousTitle: previousTitle, status: "applied", note: "" });
  }

  const totalChapters = flatChapters.length;
  const width = Math.max(3, String(totalChapters).length);
  for (const chapter of flatChapters) chapter.file = chapterFileName(chapter.globalNo, width);

  // 6) 范围校验（非法直接非零退出，且不写任何产物）
  const range = selectRange({ options, totalChapters, volumes: flatVolumes });
  for (const chapter of flatChapters) chapter.selected = isSelected(chapter, range);

  // 6.5) 跨资产对齐：每个上传文件接在哪里、是否重叠、是否重复（正文台账的当前快照）
  const activeAssets = assets.filter((asset) => !asset.skippedAsDuplicate);
  const crossAsset = analyzeCrossAsset(activeAssets);
  // 真正可疑的只有「重叠」，restarts / gap 只记录不报问题
  const crossAssetOverlaps = crossAsset.relations.filter((item) => item.kind === "overlaps");

  // 7) 裁决触发与置信度
  const unrecognizedTotal = quality.unrecognizedHeadings.length;
  const chapterBoundaryTotal = assets.reduce((sum, asset) => sum + (asset.skippedAsDuplicate ? 0 : asset.boundaries.filter((item) => item.level === "chapter").length), 0);
  const headingLikeTotal = chapterBoundaryTotal + unrecognizedTotal;
  const unrecognizedHeadingRatio = headingLikeTotal === 0 ? 0 : unrecognizedTotal / headingLikeTotal;
  const expectedChapters = Math.max(chapterBoundaryTotal, headingLikeTotal);
  const detectedChapterRatio = expectedChapters === 0 ? 1 : totalChapters / expectedChapters;
  const reasons = [];

  if (unrecognizedHeadingRatio > THRESHOLDS.unrecognizedHeadingRatio) {
    reasons.push(`未识别标题行占比 ${(unrecognizedHeadingRatio * 100).toFixed(1)}% > ${(THRESHOLDS.unrecognizedHeadingRatio * 100).toFixed(0)}%（${unrecognizedTotal} 行疑似标题未被识别）`);
  }
  if (expectedChapters > 0 && detectedChapterRatio < THRESHOLDS.detectedChapterRatio) {
    reasons.push(`切出章数 ${totalChapters} 低于预期 ${expectedChapters} 的 ${(THRESHOLDS.detectedChapterRatio * 100).toFixed(0)}%（比例 ${(detectedChapterRatio * 100).toFixed(1)}%）`);
  }
  if (quality.outOfOrder.length) reasons.push(`出现编号乱序 ${quality.outOfOrder.length} 处`);
  if (quality.duplicated.length) reasons.push(`出现重复章名 ${quality.duplicated.length} 组`);
  // 缺号与「空正文」过去只记录不判定，导致一本缺章 / 空章的书在界面上与干净书一模一样（静默放行）。
  // 现在纳入仲裁触发线：至少让 agentArbitrationRequired 为真，由用户在配置页知情确认后再跑。
  // 取保守口径——空正文只认 chars === 0，避免误伤正常短章。
  const emptyBodyChapters = quality.truncated.filter((item) => item.chars === 0);
  const missingNumberTotal = quality.missing.reduce((sum, item) => sum + item.missingNumbers.length, 0);
  if (missingNumberTotal) {
    reasons.push(`缺章号 ${missingNumberTotal} 个（${quality.missing.length} 处缺口）`);
  }
  if (emptyBodyChapters.length) {
    reasons.push(`正文为空 ${emptyBodyChapters.length} 章`);
  }
  if (crossAssetOverlaps.length) {
    reasons.push(`跨卷章节编号重叠 ${crossAssetOverlaps.length} 处：${crossAssetOverlaps.map((item) => `${item.previousAssetId} → ${item.assetId} 的第 ${item.currentFirstNumber} 章 ≤ 上卷末章 ${item.previousLastNumber}（重叠 ${item.overlapChapters} 章）`).join("；")}，需判定是否为重复上传的同一卷`);
  }
  if (crossAsset.duplicates.length) {
    const preview = crossAsset.duplicates.slice(0, 5).map((item) => `「${item.title}」出现于 ${item.assetIds.join(" / ")}（各 ${item.occurrenceCount} 处）`).join("；");
    reasons.push(`跨卷重复章名 ${crossAsset.duplicates.length} 组：${preview}${crossAsset.duplicates.length > 5 ? " …" : ""}，需判定是不是同一本书 / 是否重复上传`);
  }
  if (totalChapters <= 1) reasons.push("没有识别到章节标题，整本被当成一整块，需要确认章节边界");

  const signals = {
    headingLikeLines: headingLikeTotal,
    recognizedChapterBoundaries: chapterBoundaryTotal,
    unrecognizedHeadings: unrecognizedTotal,
    unrecognizedRatio: Number(unrecognizedHeadingRatio.toFixed(4)),
    resolvedByRevision: assets.reduce((sum, asset) => sum + (asset.resolvedByRevision ?? 0), 0),
    detectedChapters: totalChapters,
    expectedChapters: expectedChapters,
    detectedRatio: Number(detectedChapterRatio.toFixed(4)),
    outOfOrder: quality.outOfOrder.length,
    duplicatedTitles: quality.duplicated.length,
    truncatedChapters: quality.truncated.length,
    emptyBodyChapters: emptyBodyChapters.length,
    missingGaps: quality.missing.length,
    missingNumbers: missingNumberTotal,
    contaminationChapters: quality.contamination.length,
    encodingFallbacks: quality.encodingFallbacks.length,
    weakTitles: quality.weakTitles.length,
    crossAssetOverlaps: crossAssetOverlaps.length,
    crossAssetDuplicateTitles: crossAsset.duplicates.length,
    crossAssetRestarts: crossAsset.relations.filter((item) => item.kind === "restarts").length,
    crossAssetGaps: crossAsset.relations.filter((item) => item.kind === "gap").length,
    assetCount: crossAsset.assets.length,
  };

  let confidence = 1;
  confidence -= Math.min(0.4, unrecognizedHeadingRatio * 2);
  confidence -= expectedChapters > 0 && detectedChapterRatio < 1 ? Math.min(0.3, (1 - detectedChapterRatio) * 0.5) : 0;
  confidence -= Math.min(0.15, signals.outOfOrder * 0.05);
  confidence -= Math.min(0.15, signals.duplicatedTitles * 0.05);
  confidence -= Math.min(0.1, signals.truncatedChapters * 0.02);
  confidence -= Math.min(0.05, signals.contaminationChapters * 0.01);
  confidence -= Math.min(0.05, signals.encodingFallbacks * 0.03);
  confidence -= Math.min(0.05, signals.weakTitles * 0.01);
  confidence -= Math.min(0.2, signals.crossAssetOverlaps * 0.1);
  confidence -= Math.min(0.2, signals.crossAssetDuplicateTitles * 0.05);
  if (totalChapters <= 1) confidence = Math.min(confidence, 0.3);
  confidence = Number(Math.max(0, Math.min(1, confidence)).toFixed(2));
  if (confidence < THRESHOLDS.confidenceFloor) reasons.push(`置信度 ${confidence} 低于地板 ${THRESHOLDS.confidenceFloor}`);

  const agentArbitrationRequired = reasons.length > 0;

  // 8) 批次计划（三档全出，生效档位由 --profile 决定；切批只覆盖本次选中章）
  const selectedChapters = flatChapters.filter((chapter) => chapter.selected);
  const tiers = { standard: computeBatches(selectedChapters, "standard"), deep: computeBatches(selectedChapters, "deep"), outline: computeBatches(selectedChapters, "outline") };
  const activeTier = PROFILE_ACTIVE_TIER[options.profile] ?? "standard";
  const batchPlan = {
    generatedAt: new Date().toISOString(),
    profile: options.profile,
    activeTier: activeTier,
    activeTierLabel: BATCH_TIERS[activeTier].label,
    totalChapters: totalChapters,
    selectedChapters: selectedChapters.length,
    tiers,
    batches: tiers[activeTier].batches,
  };

  // 8.5) 源清洗汇总：默认只是「可清洗项」预览（不改盘）；--clean 时才真正作用于 chapters/
  const cleaning = mergeCleaningReports(
    assets.map((asset) => asset.cleaning).filter(Boolean),
    options.clean,
  );

  // 9) manifest
  const bookName = options.title || options.referenceBookId || path.basename(assets[0].fileName, path.extname(assets[0].fileName));
  const encodings = Array.from(new Set(assets.filter((asset) => !asset.skippedAsDuplicate).map((asset) => asset.encoding)));
  const generatedAt = new Date().toISOString();

  // 非章 Markdown 标题与内部卷标记：逐资产汇总，供用户审阅与按卷选择参考
  const nonChapterHeadings = activeAssets.flatMap((asset) =>
    asset.nonChapterHeadings.map((item) => ({ assetId: asset.assetId, line: item.line, title: item.title, type: item.type })),
  );
  const volumeMarkers = activeAssets.flatMap((asset) =>
    asset.volumeMarkers.map((item) => ({ assetId: asset.assetId, line: item.line, name: item.name, complete: item.complete })),
  );
  const internalVolumeAssets = activeAssets.filter((asset) => asset.volumeMarkers.length > 0).map((asset) => asset.assetId);

  const manifest = {
    schemaVersion: SCHEMA_VERSION,
    generator: { id: SKILL_ID, version: SKILL_VERSION, script: "scripts/split-chapters.mjs", node: process.version },
    generatedAt: generatedAt,
    referenceBookId: options.referenceBookId || null,
    profile: options.profile,
    activeTier: activeTier,
    book: {
      name: bookName,
      author: "",
      source: assets.map((asset) => asset.fileName),
      sourcePaths: assets.map((asset) => asset.filePath),
      fetchedAt: "",
    },
    totalChapters: totalChapters,
    totalChars: flatChapters.reduce((sum, chapter) => sum + chapter.chars, 0),
    crossAsset: crossAsset,
    encoding: {
      primary: encodings.length === 1 ? encodings[0] : encodings.length ? "mixed" : "unknown",
      assets: Object.fromEntries(assets.map((asset) => [asset.assetId, asset.encoding])),
      methods: Object.fromEntries(assets.map((asset) => [asset.assetId, asset.encodingMethod])),
      notes: Object.fromEntries(assets.filter((asset) => asset.encodingNote).map((asset) => [asset.assetId, asset.encodingNote])),
    },
    splitMethod: "title-regex",
    confidence,
    confidenceSignals: signals,
    agentArbitrationRequired,
    reasons,
    arbitrationReasons: reasons,
    revisionsApplied,
    revisionsSource: revisionBundle.source || null,
    scope: { type: range.type, from: range.from, to: range.to, selectedChapters: range.selectedChapters, selectedVolumes: range.selectedVolumes ?? null },
    rangeCheck: { status: "ok", scope: options.scope, from: options.from, to: options.to, checkedAgainst: { totalChapters, totalVolumes: flatVolumes.length } },
    volumes: flatVolumes.map((volume) => ({ no: volume.no, name: volume.name, from: volume.from, to: volume.to, assetId: volume.assetId, chapterCount: volume.chapterCount })),
    chapters: flatChapters.map((chapter) => ({
      no: chapter.globalNo,
      title: chapter.title,
      file: chapterFileName(chapter.globalNo, width),
      chars: chapter.chars,
      flags: chapter.flags,
      volumeNo: chapter.volumeNo,
      volumeLocalNo: chapter.volumeLocalNo,
      assetId: chapter.assetId,
      assetChapterNo: chapter.assetChapterNo,
      lineStart: chapter.startLine,
      lineEnd: chapter.endLine,
      number: chapter.number,
      weakTitle: chapter.weakTitle,
      selected: chapter.selected,
    })),
    quality,
    cleaning,
    duplicates: duplicateAssets,
    nonChapterHeadings,
    volumeMarkers,
    ignoredInputs: assets.filter((asset) => asset.skippedAsDuplicate).map((asset) => ({ assetId: asset.assetId, fileName: asset.fileName, reason: "fingerprint-duplicate" })),
    meta: {
      leadingText: Object.fromEntries(assets.filter((asset) => asset.leadingText).map((asset) => [asset.assetId, { chars: asset.leadingText.replace(/\s/g, "").length, preview: asset.leadingText.slice(0, 500) }])),
      numberedHeadingsAdopted: Object.fromEntries(assets.map((asset) => [asset.assetId, asset.adoptedNumbered])),
      internalVolumeAssets,
      thresholds: THRESHOLDS,
    },
    batchSummary: { activeTier: activeTier, batchSize: tiers[activeTier].batchSize, batchCount: tiers[activeTier].batchCount },
    artifacts: {
      chaptersDir: "chapters",
      chapterIndex: "章节索引.json",
      mergedChapterIndex: "合并章节索引.json",
      fingerprints: "指纹.json",
      batchPlan: "批次计划.json",
    },
    note: "chapters/ 始终全量写出（源包完整、可复现）；scope 只决定批次计划与 selected 标记。",
  };

  // 10) 写盘
  const outDir = options.out ? path.resolve(process.cwd(), options.out) : "";
  const written = [];
  if (!options.dryRun) {
    const chaptersDir = path.join(outDir, "chapters");
    await mkdir(outDir, { recursive: true });
    await rm(chaptersDir, { recursive: true, force: true });
    await mkdir(chaptersDir, { recursive: true });

    for (const asset of assets) {
      if (asset.skippedAsDuplicate) continue;
      for (const chapter of asset.chapters) {
        const fileName = chapterFileName(chapter.globalNo, width);
        const content = `${chapter.title}\n${chapter.bodyText}\n`.replace(/\n{3,}/g, "\n\n");
        await writeFile(path.join(chaptersDir, fileName), content, "utf8");
      }
    }
    written.push(`chapters/（${totalChapters} 个文件）`);

    await writeJson(path.join(outDir, "manifest.json"), manifest, written);
    await writeJson(path.join(outDir, "章节索引.json"), buildChapterIndex(manifest, assets, width), written);
    await writeJson(path.join(outDir, "合并章节索引.json"), buildMergedChapterIndex(manifest), written);
    await writeJson(path.join(outDir, "指纹.json"), buildFingerprints(fingerprints, assets, generatedAt), written);
    await writeJson(path.join(outDir, "批次计划.json"), batchPlan, written);

    if (options.cleanOut) {
      const cleanOutDir = path.resolve(process.cwd(), options.cleanOut);
      await mkdir(cleanOutDir, { recursive: true });
      for (const [index] of options.inputs.entries()) {
        await writeFile(path.join(cleanOutDir, `${index}.txt`), assets[index].cleanedText, "utf8");
      }
      written.push(`清洗后正文/（${options.inputs.length} 个文件）`);
    }
  }

  const summary = {
    ok: true,
    dryRun: options.dryRun,
    outDir: outDir || null,
    profile: options.profile,
    activeTier: activeTier,
    totalChapters: totalChapters,
    totalChars: manifest.totalChars,
    volumes: flatVolumes.map((volume) => ({ no: volume.no, name: volume.name, from: volume.from, to: volume.to })),
    // 正文台账快照：每个上传文件 → 本书内的全书章号区间；relations/duplicates 是待裁决证据
    sources: crossAsset.assets,
    crossAsset: {
      relations: crossAsset.relations,
      duplicates: crossAsset.duplicates,
      overlaps: crossAssetOverlaps.length,
      duplicateTitles: crossAsset.duplicates.length,
      restarts: signals.crossAssetRestarts,
      gaps: signals.crossAssetGaps,
    },
    scope: manifest.scope,
    encodings: manifest.encoding,
    confidence,
    agentArbitrationRequired: agentArbitrationRequired,
    arbitrationReasons: reasons,
    qualitySummary: {
      missing: quality.missing.length,
      duplicated: quality.duplicated.length,
      truncated: quality.truncated.length,
      contamination: quality.contamination.length,
      outOfOrder: quality.outOfOrder.length,
      unrecognizedHeadings: quality.unrecognizedHeadings.length,
      missingNumbers: missingNumberTotal,
      emptyBody: emptyBodyChapters.length,
    },
    cleaning,
    duplicates: duplicateAssets,
    nonChapterHeadingCount: nonChapterHeadings.length,
    volumeMarkerCount: volumeMarkers.length,
    internalVolumeAssets,
    batchPlan: {
      activeTier: activeTier,
      batchSize: tiers[activeTier].batchSize,
      batchCount: tiers[activeTier].batchCount,
      tiers: Object.fromEntries(Object.entries(tiers).map(([tier, plan]) => [tier, { batchSize: plan.batchSize, batchCount: plan.batchCount, totalChapters: plan.totalChapters }])),
    },
    files: written,
  };

  process.stdout.write(options.json ? `${JSON.stringify(summary, null, 2)}\n` : renderHumanSummary(summary, manifest));
  return EXIT_OK;
}

run(process.argv.slice(2))
  .then((code) => {
    process.exitCode = code;
  })
  .catch((error) => {
    if (error instanceof UsageError) {
      process.stderr.write(`错误：${error.message}\n\n${USAGE}\n`);
      process.exitCode = EXIT_USAGE;
      return;
    }
    process.stderr.write(`运行失败：${error instanceof Error ? error.stack ?? error.message : String(error)}\n`);
    process.exitCode = EXIT_RUNTIME;
  });
