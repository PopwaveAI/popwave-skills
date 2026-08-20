import path from "node:path";

function relativePath(filePath) {
  return path.relative(process.cwd(), filePath) || filePath;
}

function parseJsonLocation(message) {
  const match = /\(line (\d+) column (\d+)\)/.exec(message);
  if (!match) {
    return null;
  }
  return {
    line: Number(match[1]),
    column: Number(match[2])
  };
}

function formatJsonSnippet(content, location) {
  if (!location) {
    return "";
  }

  const lines = content.split(/\r?\n/);
  const targetIndex = location.line - 1;
  const start = Math.max(0, targetIndex - 2);
  const end = Math.min(lines.length, targetIndex + 3);
  const lineNumberWidth = String(end).length;
  const snippet = [];

  for (let index = start; index < end; index += 1) {
    const lineNumber = String(index + 1).padStart(lineNumberWidth, " ");
    snippet.push(`${lineNumber} | ${lines[index]}`);
    if (index === targetIndex) {
      snippet.push(`${" ".repeat(lineNumberWidth)} | ${" ".repeat(Math.max(0, location.column - 1))}^`);
    }
  }

  return snippet.join("\n");
}

export function formatSkillJsonError({ skillId, filePath, content, error }) {
  const detail = error instanceof Error ? error.message : String(error);
  const location = parseJsonLocation(detail);
  const snippet = formatJsonSnippet(content, location);
  const lines = [
    "Skill JSON validation failed.",
    `Skill: ${skillId}`,
    `File: ${relativePath(filePath)}`,
    "Problem: skill.json is not valid JSON.",
    `Parser error: ${detail}`
  ];

  if (snippet) {
    lines.push("Nearby content:", snippet);
  }

  lines.push(
    "AI repair prompt:",
    `Fix the JSON syntax error in ${relativePath(filePath)} for skill "${skillId}". Preserve the existing fields and values unless changing them is required to make valid JSON.`
  );

  return lines.join("\n");
}

export function formatSkillValidationError({ skillId, filePath, problem, hint }) {
  const lines = [
    "Skill validation failed.",
    `Skill: ${skillId}`,
    filePath ? `File: ${relativePath(filePath)}` : null,
    `Problem: ${problem}`,
    hint ? `Fix hint: ${hint}` : null
  ].filter(Boolean);

  if (filePath) {
    lines.push(
      "AI repair prompt:",
      `Fix ${relativePath(filePath)} for skill "${skillId}" so this validation problem is resolved: ${problem}`
    );
  }

  return lines.join("\n");
}
