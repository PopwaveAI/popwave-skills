#!/usr/bin/env node
/**
 * tool-split-chapters · 分章归一（拆书链路第零期 T1.3）
 *
 * 设计约束（不要打破）：
 * 1. 纯 Node ESM，零第三方依赖，Node >= 20。
 * 2. 确定性：同一组输入 + 同一组参数，除 generatedAt 外产物逐字节一致；脚本不做任何模型调用。
 * 3. 主路径纯脚本分章（零 token），Agent 只在低置信度时裁决候选边界，并经 --revisions 回灌重跑。
 * 4. 源包（manifest + chapters + 索引 + 指纹 + 批次计划）永远由本脚本写出，Agent 不直接写源包。
 * 5. 受 runner 注入单文件 ≤64KB 限制，纯函数核心抽至 scripts/split-core.mjs；本入口只保留 CLI 解析、主流程编排与产物组装，两文件行为与拆分前一致。
 *
 * 产物（<out> 下）：
 *   manifest.json          章清单 / 卷边界 / 每章字数 / 质量问题 / encoding / confidence / 裁决标记 / revisions
 *   chapters/chNNN.txt     按章正文（首行为标题行）
 *   章节索引.json           逐资产的卷内序号视图
 *   合并章节索引.json       多资产按序拼接，每章带 globalNo / volumeLocalNo / assetId
 *   指纹.json               每资产 SHA-256 与后 8 位
 *   批次计划.json           三档切批（standard 约 30 章/批、deep ≤20、outline ≤40）
 */

import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import {
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
} from "./split-core.mjs";

const SKILL_ID = "tool-split-chapters";
const SKILL_VERSION = "0.1.0";
const SCHEMA_VERSION = "1";

/** --profile 与生效档位的映射：档位名与交付物一一对应，故为恒等映射 */
const PROFILE_ACTIVE_TIER = { standard: "standard", deep: "deep", outline: "outline" };
const PROFILES = Object.keys(PROFILE_ACTIVE_TIER);
const SCOPES = ["full", "volume", "chapters"];

const EXIT_OK = 0;
const EXIT_RUNTIME = 1;
const EXIT_USAGE = 2;

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
