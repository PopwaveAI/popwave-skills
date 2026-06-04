import { spawnSync } from "node:child_process";

function run(command, args) {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    stdio: "pipe"
  });
  return result;
}

const insideWorkTree = run("git", ["rev-parse", "--is-inside-work-tree"]);

if (insideWorkTree.status !== 0 || insideWorkTree.stdout.trim() !== "true") {
  console.log("Skipping Git hook install: not inside a Git worktree.");
  process.exit(0);
}

const config = run("git", ["config", "core.hooksPath", ".githooks"]);

if (config.status !== 0) {
  console.error(config.stderr || "Failed to configure core.hooksPath.");
  process.exit(config.status ?? 1);
}

console.log("Git hooks installed: core.hooksPath=.githooks");
