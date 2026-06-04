import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { readSkillManifest, validateSkillManifest } from "./skill-manifest.mjs";

const root = process.cwd();
const skillsRoot = path.join(root, "skills");
const distRoot = path.join(root, "dist");

function isPrerelease(version) {
  return version.includes("-");
}

function compareVersions(left, right) {
  const leftMain = left.split("-")[0].split(".").map(Number);
  const rightMain = right.split("-")[0].split(".").map(Number);
  for (let index = 0; index < 3; index += 1) {
    if (leftMain[index] !== rightMain[index]) {
      return leftMain[index] - rightMain[index];
    }
  }
  return left.localeCompare(right);
}

async function zipDirectory(sourceDir, outputPath) {
  await mkdir(path.dirname(outputPath), { recursive: true });
  return new Promise((resolve, reject) => {
    const child = spawn("zip", ["-qr", outputPath, "."], {
      cwd: sourceDir,
      stdio: "inherit"
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`zip exited with code ${code}`));
      }
    });
  });
}

async function sha256File(filePath) {
  const buffer = await readFile(filePath);
  return createHash("sha256").update(buffer).digest("hex");
}

async function main() {
  await rm(distRoot, { recursive: true, force: true });
  await mkdir(distRoot, { recursive: true });

  const entries = await readdir(skillsRoot, { withFileTypes: true });
  const skills = [];

  for (const entry of entries.filter((item) => item.isDirectory())) {
    const skillRoot = path.join(skillsRoot, entry.name);
    const resolved = await readSkillManifest(skillRoot, entry.name);
    const manifest = await validateSkillManifest({ directoryName: entry.name, skillRoot, ...resolved });
    const packagePath = path.join(distRoot, "skills", manifest.id, manifest.version, "skill-package.zip");
    await zipDirectory(skillRoot, packagePath);
    const checksum = await sha256File(packagePath);
    const packageUrl = `skills/${manifest.id}/${manifest.version}/skill-package.zip`;
    skills.push({
      id: manifest.id,
      displayName: manifest.displayName || manifest.id,
      description: manifest.description,
      latest: manifest.version,
      channels: {
        [isPrerelease(manifest.version) ? "beta" : "stable"]: manifest.version
      },
      versions: [
        {
          version: manifest.version,
          packageUrl,
          checksum: `sha256-${checksum}`,
          createdAt: new Date().toISOString()
        }
      ]
    });
  }

  skills.sort((left, right) => left.id.localeCompare(right.id));
  for (const skill of skills) {
    skill.versions.sort((left, right) => compareVersions(right.version, left.version));
    const stable = skill.versions.find((version) => !isPrerelease(version.version));
    skill.latest = stable?.version ?? skill.versions[0].version;
    if (stable) {
      skill.channels.stable = stable.version;
    }
    const beta = skill.versions.find((version) => isPrerelease(version.version));
    if (beta) {
      skill.channels.beta = beta.version;
    }
  }

  await writeFile(
    path.join(distRoot, "registry.json"),
    JSON.stringify(
      {
        schemaVersion: 1,
        updatedAt: new Date().toISOString(),
        skills
      },
      null,
      2
    ),
    "utf8"
  );
  await writeFile(path.join(distRoot, ".nojekyll"), "", "utf8");
  console.log(`Built ${skills.length} skills into dist/registry.json`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
