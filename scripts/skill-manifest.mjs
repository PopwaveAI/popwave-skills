import { readFile, stat } from "node:fs/promises";
import path from "node:path";
import { formatSkillJsonError, formatSkillValidationError } from "./skill-error-format.mjs";

export const idPattern = /^[a-zA-Z0-9_-]+$/;
export const versionPattern = /^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$/;

export async function exists(filePath) {
  try {
    await stat(filePath);
    return true;
  } catch {
    return false;
  }
}

function fail(message) {
  throw new Error(message);
}

function unquoteYamlScalar(value) {
  const trimmed = value.trim();
  if ((trimmed.startsWith('"') && trimmed.endsWith('"')) || (trimmed.startsWith("'") && trimmed.endsWith("'"))) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

export function parseSkillFrontmatter(content) {
  if (!content.startsWith("---")) {
    return new Map();
  }

  const lines = content.split(/\r?\n/);
  if (lines[0].trim() !== "---") {
    return new Map();
  }

  const metadata = new Map();
  for (let index = 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (line.trim() === "---") {
      return metadata;
    }

    if (/^\s/.test(line)) {
      continue;
    }

    const match = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
    if (match) {
      metadata.set(match[1], unquoteYamlScalar(match[2]));
    }
  }

  return new Map();
}

async function readSkillJson(filePath, skillId) {
  const content = await readFile(filePath, "utf8");
  try {
    return JSON.parse(content);
  } catch (error) {
    fail(formatSkillJsonError({ skillId, filePath, content, error }));
  }
}

async function readCommunitySkillManifest(skillRoot, directoryName, skillFilePath) {
  const content = await readFile(skillFilePath, "utf8");
  const metadata = parseSkillFrontmatter(content);
  const name = metadata.get("name") || directoryName;

  return {
    id: name,
    version: metadata.get("version") || "0.1.0",
    displayName: metadata.get("name") || directoryName,
    description: metadata.get("description"),
    entry: path.basename(skillFilePath),
    activation: {
      slashCommands: [name],
      default: false
    },
    permissions: {
      readProjectFiles: true,
      writeProjectFiles: true,
      network: false,
      shell: false
    },
    loadPolicy: {
      includeReferences: "on-demand",
      maxPromptChars: 50000
    },
    _source: "frontmatter"
  };
}

export async function readSkillManifest(skillRoot, directoryName) {
  const manifestPath = path.join(skillRoot, "skill.json");
  if (await exists(manifestPath)) {
    return {
      manifest: await readSkillJson(manifestPath, directoryName),
      manifestPath,
      source: "skill.json"
    };
  }

  const skillFilePath = path.join(skillRoot, "SKILL.md");
  if (await exists(skillFilePath)) {
    return {
      manifest: await readCommunitySkillManifest(skillRoot, directoryName, skillFilePath),
      manifestPath: skillFilePath,
      source: "frontmatter"
    };
  }

  fail(formatSkillValidationError({
    skillId: directoryName,
    filePath: manifestPath,
    problem: "missing skill.json or SKILL.md",
    hint: "Add a Popwave skill.json file or a community-style SKILL.md with YAML frontmatter."
  }));
}

export async function validateSkillManifest({ directoryName, skillRoot, manifest, manifestPath, source }) {
  if (!manifest.id || !idPattern.test(manifest.id)) {
    fail(formatSkillValidationError({
      skillId: directoryName,
      filePath: manifestPath,
      problem: `skill id must match ${idPattern}`,
      hint: source === "frontmatter"
        ? "Set frontmatter name to the skill directory name using only letters, numbers, underscores, or hyphens."
        : "Set id to the skill directory name using only letters, numbers, underscores, or hyphens."
    }));
  }

  if (manifest.id !== directoryName) {
    fail(formatSkillValidationError({
      skillId: directoryName,
      filePath: manifestPath,
      problem: `directory name must match skill id "${manifest.id}"`,
      hint: source === "frontmatter"
        ? `Either rename the directory to "${manifest.id}" or set SKILL.md frontmatter name to "${directoryName}".`
        : `Either rename the directory to "${manifest.id}" or set skill.json id to "${directoryName}".`
    }));
  }

  if (!manifest.version || !versionPattern.test(manifest.version)) {
    fail(formatSkillValidationError({
      skillId: directoryName,
      filePath: manifestPath,
      problem: `version must be SemVer, got ${manifest.version}`,
      hint: source === "frontmatter"
        ? "Add a frontmatter version like 1.2.3 or omit it to use the default 0.1.0."
        : "Use a version like 1.2.3 or 1.2.3-beta.1."
    }));
  }

  if (!manifest.description || manifest.description.length < 8) {
    fail(formatSkillValidationError({
      skillId: directoryName,
      filePath: manifestPath,
      problem: "description is required and must be at least 8 characters",
      hint: source === "frontmatter"
        ? "Add a frontmatter description explaining when this skill should be used."
        : "Add a concise sentence describing what this skill helps users accomplish."
    }));
  }

  const entry = manifest.entry || "SKILL.md";
  if (entry.includes("..") || path.isAbsolute(entry)) {
    fail(formatSkillValidationError({
      skillId: directoryName,
      filePath: manifestPath,
      problem: "entry must be a safe relative path",
      hint: "Use a relative path such as SKILL.md and do not include '..' or an absolute path."
    }));
  }

  if (!(await exists(path.join(skillRoot, entry)))) {
    fail(formatSkillValidationError({
      skillId: directoryName,
      filePath: manifestPath,
      problem: `entry file "${entry}" does not exist`,
      hint: `Create ${entry} under skills/${directoryName}/ or update the manifest entry to the correct file.`
    }));
  }

  return {
    ...manifest,
    entry
  };
}
