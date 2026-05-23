# Popwave Skills

This repository is the remote Skill Hub for Paopao projects.

Skill authors add or update packages under `skills/<skill-id>`. CI validates each skill, builds zip packages, generates `dist/registry.json`, and publishes the `dist` folder to GitHub Pages.

Default registry URL:

```text
https://popwaveai.github.io/popwave-skills/registry.json
```

## Skill Layout

```text
skills/
  example-writing/
    skill.json
    SKILL.md
    CHANGELOG.md
    README.md
    references/
    examples/
    scripts/
```

`skill.json` is the app-facing manifest. `SKILL.md` is the model-facing instruction entry.

## Author Workflow

1. Create or edit `skills/<skill-id>`.
2. Bump `skill.json.version` using SemVer.
3. Update `CHANGELOG.md`.
4. Run:

```bash
npm install
npm run build
```

5. Open a PR.

After merge, GitHub Actions deploys the registry. Paopao users can refresh Skills in the app, install the new version, and the project will lock that version in `.paopao/skills/config.json`.

## Release Channels

The build script publishes a `stable` channel for normal versions and a `beta` channel for prerelease versions. The latest stable version is used as `latest` when available.
