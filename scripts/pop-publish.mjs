#!/usr/bin/env node
/**
 * pop-publish.mjs — 一键镜像发布 skill 到三处
 *   1. git commit + push（推送到 GitHub，popwave 云端由 publish.yml 自动分发）
 *   2. 同步到 TRAE 全局技能目录（C:\Users\AWMPRO\.trae-cn\skills，平铺 {skill}/）
 *   3. 同步到 popwave 本地缓存（...\AppData\Roaming\popwave\remote-skills，{skill}/{version}/）
 *
 * 全量镜像语义：
 *   - 源 skills/ 下新增/修改的 skill 会覆盖到两端；
 *   - 两端中「源里已不存在」且属于本项目管理前缀（pop/short/tool）的旧 skill 会被删除；
 *   - 源 skills/_deprecated 目录会被删除（不再发布）。
 *
 * 用法：
 *   node scripts/pop-publish.mjs            # 完整三步（commit+push + 双端镜像同步）
 *   node scripts/pop-publish.mjs --no-git   # 跳过 git，只做双端镜像同步
 *   node scripts/pop-publish.mjs --sync-only # 同 --no-git
 *   node scripts/pop-publish.mjs --post-commit # 供 git hook：只 push + 双端同步，不 commit（避免递归）
 */
import { spawnSync } from "node:child_process";
import { cp, mkdir, readdir, readFile, rm as rmOriginal } from "node:fs/promises";
import path from "node:path";
import { existsSync, readdirSync, lstatSync, rmdirSync, unlinkSync } from "node:fs";

// 手动递归删除：先删文件再删空目录（比 fs.rm 在 Windows 上更可靠，
// fs.rm recursive 对个别目录会静默失败——报成功但目录仍在）
function forceRemoveSync(target) {
  if (!existsSync(target)) return;
  const st = lstatSync(target);
  if (st.isDirectory()) {
    for (const entry of readdirSync(target)) {
      forceRemoveSync(path.join(target, entry));
    }
    try { rmdirSync(target); } catch (e) { /* 目录仍被占用时最后再验证 */ }
  } else {
    try { unlinkSync(target); } catch (e) { /* 文件仍被占用时最后再验证 */ }
  }
}

// 可靠的删除 helper：手动递归删除后验证，清理未删净的残留（带重试）
// 返回是否删除成功；调用方可决定是否降级处理
async function rmSafe(target, options = { recursive: true, force: true }) {
  try {
    await rmOriginal(target, options);
  } catch (e) {
    // 继续走兜底
  }
  if (!existsSync(target)) return true;

  // 瞬时占用（如 .git 对象被后台进程锁定）→ 重试几次
  for (let i = 0; i < 3; i++) {
    forceRemoveSync(target);
    if (!existsSync(target)) return true;
    await new Promise((r) => setTimeout(r, 800));
  }
  return false; // 仍未删净（可能被进程占用）
}

// 将 rm 替换为 rmSafe，使后续所有删除操作都使用安全删除
const rm = rmSafe;

// ---------- 配置 ----------
const GIT = process.env.GIT_PATH || "C:\\Program Files\\Git\\cmd\\git.exe";
const ROOT = process.cwd();
const SKILLS_ROOT = path.join(ROOT, "skills");
const TRAE_ROOT = "C:\\Users\\AWMPRO\\.trae-cn\\skills";
const POPWAVE_ROOT = "C:\\Users\\AWMPRO\\AppData\\Roaming\\popwave\\remote-skills";
const DEFAULT_BRANCH = "main";
const DEPRECATED_DIR = path.join(SKILLS_ROOT, "_deprecated");

// 本项目管理前缀：只有这些前缀的旧 skill 才会被镜像清理（避免误删 lark-* 等第三方）
const MANAGED_PREFIXES = ["pop-", "short-", "tool-"];

// ---------- 工具 ----------
function runGit(args, opts = {}) {
  const res = spawnSync(GIT, args, { encoding: "utf8", ...opts });
  if (res.status !== 0) {
    throw new Error(`git ${args.join(" ")} 失败: ${res.stderr?.trim() || res.stdout?.trim()}`);
  }
  return res.stdout.trim();
}

function hasGit() {
  const res = spawnSync(GIT, ["--version"], { encoding: "utf8", stdio: "pipe" });
  return res.status === 0;
}

async function readJson(file) {
  try {
    const raw = await readFile(file, "utf8");
    return JSON.parse(raw.charCodeAt(0) === 0xfeff ? raw.slice(1) : raw);
  } catch (e) {
    return null;
  }
}

async function listSkillDirs() {
  const entries = await readdir(SKILLS_ROOT, { withFileTypes: true });
  return entries
    .filter((e) => e.isDirectory() && !e.name.startsWith(".") && !e.name.startsWith("_"))
    .map((e) => e.name);
}

function isManaged(name) {
  return MANAGED_PREFIXES.some((p) => name.startsWith(p));
}

// ---------- 步骤 1：git commit ----------
async function gitCommit() {
  if (!hasGit()) {
    console.warn("[git] 未找到 git，跳过 git 提交。");
    return;
  }
  const statusOut = runGit(["status", "--porcelain"]);
  if (!statusOut) {
    console.log("[git] 工作区干净，无改动，跳过 commit。");
    return;
  }
  const changedFiles = statusOut.split("\n");
  const changeSummary = changedFiles.slice(0, 5).map((l) => l.slice(3).trim()).join(", ");
  const summary = changedFiles.length > 5
    ? `${changeSummary} 等共 ${changedFiles.length} 项`
    : changeSummary;
  runGit(["add", "-A"]);
  const msg = `publish: sync skills (${new Date().toISOString().slice(0, 16).replace("T", " ")})\n\n${summary}`;
  runGit(["commit", "-m", msg]);
  console.log(`[git] 已提交: ${msg.split("\n")[0]}`);
}

// ---------- 步骤 1b：git push ----------
async function gitPush() {
  if (!hasGit()) {
    console.warn("[git] 未找到 git，跳过 push。");
    return;
  }
  const branch = runGit(["branch", "--show-current"]) || DEFAULT_BRANCH;
  runGit(["push", "origin", branch]);
  console.log(`[git] 已 push 到 origin/${branch}（popwave 云端由 GitHub Actions 自动分发）`);
}

// ---------- 镜像清理：删除目标端中「源里不存在」且属管理前缀的旧 skill ----------
async function pruneStale(root, validNames, label) {
  if (!existsSync(root)) return { removed: 0, blocked: [] };
  const entries = await readdir(root, { withFileTypes: true });
  let removed = 0;
  const blocked = [];
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const name = e.name;
    if (!isManaged(name)) continue; // 只清理本项目管理前缀
    if (validNames.includes(name)) continue; // 源里存在则保留
    const dst = path.join(root, name);
    const ok = await rmSafe(dst);
    if (ok) {
      console.log(`  [${label}] 已删除旧版 ${name}`);
      removed++;
    } else {
      console.warn(`  [${label}] ${name} 被进程占用，跳过（下次发布或应用重启后再清理）`);
      blocked.push(name);
    }
  }
  return { removed, blocked };
}

// ---------- 步骤 2：同步到 TRAE 全局目录（平铺 {skill}/） ----------
async function syncTrae(skillName) {
  const src = path.join(SKILLS_ROOT, skillName);
  const dst = path.join(TRAE_ROOT, skillName);
  await rmSafe(dst);
  await mkdir(path.dirname(dst), { recursive: true });
  await cp(src, dst, { recursive: true });
  return dst;
}

// ---------- 步骤 3：同步到 popwave 缓存（{skill}/{version}/） ----------
async function syncPopwave(skillName) {
  const src = path.join(SKILLS_ROOT, skillName);
  const manifest = await readJson(path.join(src, "skill.json"));
  const version = manifest?.version || "0.1.0";
  const dst = path.join(POPWAVE_ROOT, skillName, version);
  await rmSafe(dst);
  await mkdir(path.dirname(dst), { recursive: true });
  await cp(src, dst, { recursive: true });
  return { dst, version };
}

async function readVersion(name) {
  const m = await readJson(path.join(SKILLS_ROOT, name, "skill.json"));
  return m?.version || "";
}

// ---------- 主流程 ----------
async function main() {
  const args = process.argv.slice(2);
  const doCommit = !args.includes("--no-git") && !args.includes("--sync-only") && !args.includes("--post-commit");
  const doPush = !args.includes("--no-git") && !args.includes("--sync-only");
  const doSync = true;

  const skillNames = await listSkillDirs();
  console.log(`发现 ${skillNames.length} 个 skill。`);

  // 删除源 _deprecated 目录（旧版本不再发布）
  if (existsSync(DEPRECATED_DIR)) {
    await rm(DEPRECATED_DIR, { recursive: true, force: true });
    console.log("[源] 已删除 skills/_deprecated 目录。");
  }

  if (doCommit) {
    await gitCommit();
  }
  if (doPush) {
    await gitPush();
  }

  if (!doSync) {
    console.log("跳过双端同步。");
    return;
  }

  // 镜像清理两端旧版
  console.log("\n[镜像] 清理两端「源里已不存在」的旧 skill…");
  const traeStale = await pruneStale(TRAE_ROOT, skillNames, "trae");
  const popwaveStale = await pruneStale(POPWAVE_ROOT, skillNames, "popwave");
  console.log(`[镜像] trae 清理 ${traeStale.removed} 个，popwave 清理 ${popwaveStale.removed} 个。`);
  if (traeStale.blocked.length || popwaveStale.blocked.length) {
    console.log(`[镜像] 被占用待清理：trae=[${traeStale.blocked.join(", ")}] popwave=[${popwaveStale.blocked.join(", ")}]`);
  }

  // 同步源里的 skill 到两端
  let okTrae = 0, okPopwave = 0;
  for (const name of skillNames) {
    let traePatch = null, popwavePatch = null;
    try {
      traePatch = await syncTrae(name);
      okTrae++;
    } catch (e) {
      console.warn(`  [trae] ${name} 同步失败: ${e.message}`);
    }
    try {
      const r = await syncPopwave(name);
      popwavePatch = r.dst;
      okPopwave++;
    } catch (e) {
      console.warn(`  [popwave] ${name} 同步失败: ${e.message}`);
    }
    if (traePatch || popwavePatch) {
      const ver = await readVersion(name);
      console.log(`  ✓ ${name}${popwavePatch ? ` @${ver}` : ""}`);
    }
  }

  console.log(`\n完成：git=${doCommit ? "commit+push" : doPush ? "仅push" : "跳过"} | TRAE ${okTrae}/${skillNames.length} | popwave ${okPopwave}/${skillNames.length}`);
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});