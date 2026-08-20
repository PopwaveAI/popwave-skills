import { execFileSync } from "node:child_process";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

function getAddedFiles() {
  const output = execFileSync(
    "git",
    ["diff", "--cached", "--diff-filter=A", "--name-only", "-z"],
    { encoding: "buffer" }
  );

  return output
    .toString("utf8")
    .split("\0")
    .filter(Boolean);
}

function getStagedFileSize(relativePath) {
  return Number(
    execFileSync("git", ["cat-file", "-s", `:${relativePath}`], {
      encoding: "utf8"
    }).trim()
  );
}

function formatSize(bytes) {
  return `${(bytes / 1024 / 1024).toFixed(2)} MiB (${bytes} bytes)`;
}

const oversizedFiles = [];

for (const relativePath of getAddedFiles()) {
  const size = getStagedFileSize(relativePath);

  // Git stores submodules as a gitlink, whose object size is not the directory size.
  if (size > MAX_FILE_SIZE) {
    oversizedFiles.push({ path: relativePath, size });
  }
}

if (oversizedFiles.length > 0) {
  console.error("\nPre-commit file size check failed.");
  console.error("New files must not exceed 5 MiB:\n");

  for (const file of oversizedFiles) {
    console.error(`- ${file.path}: ${formatSize(file.size)}`);
  }

  console.error("\nRemove the file, reduce its size, or unstage it before committing.");
  process.exit(1);
}

console.log("Pre-commit file size check passed.");
