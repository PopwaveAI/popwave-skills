# Contributing Skills

Popwave skills are project-local ability packages consumed by Paopao. They are not Codex skills and should not assume any Codex-specific runtime.

## Create A Skill

```bash
npm run skills:new -- my-skill-id
```

Then edit:

- `skills/my-skill-id/skill.json`
- `skills/my-skill-id/SKILL.md`
- `skills/my-skill-id/CHANGELOG.md`

This is the Popwave-native format. The hub also accepts community-style skills that only include `SKILL.md` with YAML frontmatter:

```markdown
---
name: my-skill-id
description: Use when the user needs this skill for a specific task.
version: 0.1.0
---
```

For community-style skills, `version` is optional and defaults to `0.1.0`. The directory name must match `name`.

For large skills maintained in their own repositories, add the external repository as a Git submodule under `skills/<skill-id>` instead of copying files into this repo. See `docs/submodule-skill-workflow.md`.

## Update A Skill

1. Make the smallest behavior change that solves the target use case.
2. Bump `skill.json.version`, or bump `SKILL.md` frontmatter `version` for community-style skills.
3. Update `CHANGELOG.md` if the skill keeps one.
4. If the skill is a submodule, update the skill repo first, then update the submodule pointer in this hub repo.
5. Run `npm run skills:sync` when the change depends on submodules.
6. Run `npm run build`.
7. Open a PR with test instructions and screenshots/log snippets when useful.

## Pre-commit Validation

`npm install` installs the repository Git hooks automatically. If hooks are not active, run:

```bash
npm run hooks:install
```

Before each commit, `.githooks/pre-commit` runs:

```bash
npm run skills:validate
```

Validation failures include the skill id, file path, problem, and an AI repair prompt. JSON parse errors also include nearby file content and a caret location when Node reports line and column details.

## Submodule Skills

Use a submodule when a skill is large, has a dedicated owner, has its own issues or release workflow, or contains many references and tools that are easier to maintain independently.

Do not use a submodule for small skills that are only maintained together with this hub repo.

Submodule requirements:

- The submodule path must be `skills/<skill-id>`.
- The submodule root must contain `skill.json`, `SKILL.md`, and `CHANGELOG.md`.
- `skill.json.id` must match `<skill-id>`.
- Version bumps happen inside the skill repository.
- This hub repository publishes exactly the submodule commit recorded in git, not "whatever is latest" on the submodule branch.

## Versioning

- `patch`: Prompt wording, examples, docs, references, no contract changes.
- `minor`: New capability or compatible output additions.
- `major`: Input contract, output contract, permission, or file layout changes.
- prerelease: Use `x.y.z-beta.n` for internal validation.

## Safety Rules

- Keep secrets out of the repo.
- Declare network and shell permissions in `skill.json`.
- Prefer `references/` for large knowledge files and load them on demand.
- Do not assume the host App has built-in domain knowledge.
- Do not write outside the active project unless the skill explicitly documents why.
