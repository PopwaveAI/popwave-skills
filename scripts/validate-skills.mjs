import { readdir } from "node:fs/promises";
import path from "node:path";
import { readSkillManifest, validateSkillManifest } from "./skill-manifest.mjs";

const root = process.cwd();
const skillsRoot = path.join(root, "skills");

function fail(message) {
  throw new Error(message);
}

async function validateSkill(directoryName) {
  const skillRoot = path.join(skillsRoot, directoryName);
  const resolved = await readSkillManifest(skillRoot, directoryName);
  return await validateSkillManifest({ directoryName, skillRoot, ...resolved });
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
