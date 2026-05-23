import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const skillsRoot = path.join(root, "skills");
const idPattern = /^[a-zA-Z0-9_-]+$/;
const versionPattern = /^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$/;

async function exists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readJson(filePath) {
  return JSON.parse(await readFile(filePath, "utf8"));
}

function fail(message) {
  throw new Error(message);
}

async function validateSkill(directoryName) {
  const skillRoot = path.join(skillsRoot, directoryName);
  const manifestPath = path.join(skillRoot, "skill.json");
  if (!(await exists(manifestPath))) {
    fail(`${directoryName}: missing skill.json`);
  }

  const manifest = await readJson(manifestPath);
  if (!manifest.id || !idPattern.test(manifest.id)) {
    fail(`${directoryName}: skill.json id must match ${idPattern}`);
  }
  if (manifest.id !== directoryName) {
    fail(`${directoryName}: directory name must match skill id ${manifest.id}`);
  }
  if (!manifest.version || !versionPattern.test(manifest.version)) {
    fail(`${directoryName}: version must be SemVer, got ${manifest.version}`);
  }
  if (!manifest.description || manifest.description.length < 8) {
    fail(`${directoryName}: description is required`);
  }
  const entry = manifest.entry || "SKILL.md";
  if (entry.includes("..") || path.isAbsolute(entry)) {
    fail(`${directoryName}: entry must be a safe relative path`);
  }
  if (!(await exists(path.join(skillRoot, entry)))) {
    fail(`${directoryName}: entry file ${entry} does not exist`);
  }
  if (!(await exists(path.join(skillRoot, "CHANGELOG.md")))) {
    fail(`${directoryName}: missing CHANGELOG.md`);
  }
  return manifest;
}

async function main() {
  const entries = await readdir(skillsRoot, { withFileTypes: true }).catch(() => []);
  const directories = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name);
  if (!directories.length) {
    fail("No skills found under skills/");
  }

  const seen = new Set();
  for (const directory of directories) {
    const manifest = await validateSkill(directory);
    if (seen.has(manifest.id)) {
      fail(`Duplicate skill id ${manifest.id}`);
    }
    seen.add(manifest.id);
    console.log(`ok ${manifest.id}@${manifest.version}`);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
