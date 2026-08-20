import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const id = process.argv[2];
if (!id || !/^[a-zA-Z0-9_-]+$/.test(id)) {
  console.error("Usage: npm run skills:new -- <skill-id>");
  process.exit(1);
}

const root = process.cwd();
const skillRoot = path.join(root, "skills", id);
await mkdir(skillRoot, { recursive: true });

const manifest = {
  id,
  version: "0.1.0",
  displayName: id,
  description: "TODO: describe what this skill helps Paopao project users accomplish.",
  entry: "SKILL.md",
  activation: {
    slashCommands: [id],
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
  }
};

await writeFile(path.join(skillRoot, "skill.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
await writeFile(
  path.join(skillRoot, "SKILL.md"),
  `---\nname: ${id}\ndescription: TODO: describe when Paopao should use this skill.\n---\n\n# ${id}\n\n## Purpose\n\nTODO.\n\n## When To Use\n\nTODO.\n\n## Input Contract\n\nThe host app passes the user instruction, requested skill names, explicit @ references, and project metadata.\n\n## Workflow\n\n1. Restate the real task in one sentence.\n2. Use only the requested skill instructions and local project context.\n3. Produce the requested artifact as Markdown.\n4. End with one concrete next action.\n\n## Output Contract\n\nReturn clean Markdown.\n\n## Quality Bar\n\n- Be specific.\n- Preserve project facts.\n- Avoid generic filler.\n`,
  "utf8"
);
await writeFile(path.join(skillRoot, "CHANGELOG.md"), `# Changelog\n\n## 0.1.0 - ${new Date().toISOString().slice(0, 10)}\n\n- Initial skill scaffold.\n`, "utf8");
await writeFile(path.join(skillRoot, "README.md"), `# ${id}\n\nTODO: describe authoring and validation notes for this skill.\n`, "utf8");

console.log(`Created skills/${id}`);
