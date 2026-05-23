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

## Update A Skill

1. Make the smallest behavior change that solves the target use case.
2. Bump `skill.json.version`.
3. Update `CHANGELOG.md`.
4. Run `npm run build`.
5. Open a PR with test instructions and screenshots/log snippets when useful.

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
