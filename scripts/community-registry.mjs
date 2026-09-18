import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { cp, mkdir, mkdtemp, readdir, readFile, rm, utimes, chmod, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { readSkillManifest, validateSkillManifest } from './skill-manifest.mjs';

async function filesIn(root, relative = '') {
  const files = [];
  for (const entry of await readdir(path.join(root, relative), { withFileTypes: true })) {
    const name = path.posix.join(relative, entry.name);
    if (/[\r\n\\]/.test(entry.name)) throw new Error(`Unsupported community filename: ${name}`);
    if (entry.isSymbolicLink()) throw new Error(`Community packages cannot contain symlinks: ${name}`);
    if (entry.isDirectory()) files.push(...await filesIn(root, name));
    else if (entry.isFile()) files.push(name);
    else throw new Error(`Unsupported community file: ${name}`);
  }
  return files.sort();
}

export async function communitySkills(root) {
  const directory = path.join(root, 'community');
  const entries = await readdir(directory, { withFileTypes: true });
  const skills = [];
  for (const entry of entries) {
    if (entry.name.startsWith('.') || entry.name.startsWith('_')) continue;
    if (entry.isSymbolicLink()) throw new Error(`Community skill cannot be a symlink: ${entry.name}`);
    if (!entry.isDirectory()) continue;
    const skillRoot = path.join(directory, entry.name);
    const resolved = await readSkillManifest(skillRoot, entry.name);
    const manifest = await validateSkillManifest({ directoryName: entry.name, skillRoot, ...resolved });
    await filesIn(skillRoot);
    skills.push({ skillRoot, manifest });
  }
  return skills.sort((a, b) => a.manifest.id.localeCompare(b.manifest.id));
}

export async function buildCommunityRegistry(root, distRoot) {
  const skills = [];
  await mkdir(path.join(distRoot, 'community'), { recursive: true });
  for (const { skillRoot, manifest } of await communitySkills(root)) {
    const temp = await mkdtemp(path.join(os.tmpdir(), 'community-build-'));
    try {
      const source = path.join(temp, 'source');
      await cp(skillRoot, source, { recursive: true });
      const files = await filesIn(source);
      // Fixed timestamps, permissions and ordering make unchanged versions reproducible.
      for (const file of files) {
        await utimes(path.join(source, file), new Date('2000-01-01T00:00:00Z'), new Date('2000-01-01T00:00:00Z'));
        await chmod(path.join(source, file), file.endsWith('.sh') ? 0o755 : 0o644);
      }
      const zipPath = path.join(temp, 'skill-package.zip');
      await new Promise((resolve, reject) => {
        const child = spawn('zip', ['-X', '-q', zipPath, '-@'], { cwd: source, env: { ...process.env, TZ: 'UTC' }, stdio: ['pipe', 'inherit', 'inherit'] });
        child.on('error', reject);
        child.on('close', code => code === 0 ? resolve() : reject(new Error(`zip exited ${code}`)));
        child.stdin.on('error', reject);
        child.stdin.end(files.join('\n') + '\n');
      });
      const bytes = await readFile(zipPath);
      const digest = createHash('sha256').update(bytes).digest('hex');
      const packageUrl = `community/${manifest.id}/${manifest.version}/${digest}/skill-package.zip`;
      await mkdir(path.dirname(path.join(distRoot, packageUrl)), { recursive: true });
      await writeFile(path.join(distRoot, packageUrl), bytes);
      skills.push({ id: manifest.id, displayName: manifest.displayName || manifest.id, description: manifest.description, latest: manifest.version,
        versions: [{ version: manifest.version, packageUrl, checksum: `sha256-${digest}`, packageSize: bytes.length }] });
    } finally { await rm(temp, { recursive: true, force: true }); }
  }
  await mkdir(distRoot, { recursive: true });
  await writeFile(path.join(distRoot, 'community-registry.json'), JSON.stringify({ schemaVersion: 1, updatedAt: new Date().toISOString(), skills }, null, 2));
  return skills.length;
}
