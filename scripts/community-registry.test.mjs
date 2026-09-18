import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, rm, writeFile, symlink, utimes } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildCommunityRegistry, communitySkills } from './community-registry.mjs';
const buildScript = fileURLToPath(new URL('./build-registry.mjs', import.meta.url));

test('独立索引不污染内置目录，相同内容重建包完全一致', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'community-registry-test-'));
  try {
    for (const directory of ['skills/builtin-editor', 'community/community-editor']) {
      await mkdir(path.join(root, directory), { recursive: true });
      await writeFile(path.join(root, directory, 'skill.json'), JSON.stringify({ id: path.basename(directory), version: '1.0.0', description: 'Test writing editor skill', entry: 'SKILL.md' }));
      await writeFile(path.join(root, directory, 'SKILL.md'), 'Edit prose with care.');
    }
    execFileSync(process.execPath, [buildScript], { cwd: root });
    const builtin = JSON.parse(await readFile(path.join(root, 'dist/registry.json'), 'utf8'));
    const community = JSON.parse(await readFile(path.join(root, 'dist/community-registry.json'), 'utf8'));
    assert.deepEqual(builtin.skills.map(item => item.id), ['builtin-editor']);
    assert.deepEqual(community.skills.map(item => item.id), ['community-editor']);
    const first = community.skills[0].versions[0];
    assert.equal((await readFile(path.join(root, 'dist', first.packageUrl))).length, first.packageSize);
    await utimes(path.join(root, 'community/community-editor/SKILL.md'), new Date(), new Date());
    await buildCommunityRegistry(root, path.join(root, 'second'));
    const second = JSON.parse(await readFile(path.join(root, 'second/community-registry.json'), 'utf8'));
    assert.deepEqual(second.skills[0].versions, community.skills[0].versions);
    await symlink('/tmp', path.join(root, 'community/community-editor/escape'));
    await assert.rejects(communitySkills(root), /symlinks/);
  } finally { await rm(root, { recursive: true, force: true }); }
});

test('空社区目录也生成独立的空索引与包目录', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'community-empty-test-'));
  try {
    await mkdir(path.join(root, 'community'));
    await buildCommunityRegistry(root, path.join(root, 'dist'));
    assert.deepEqual(JSON.parse(await readFile(path.join(root, 'dist/community-registry.json'), 'utf8')).skills, []);
  } finally { await rm(root, { recursive: true, force: true }); }
});
