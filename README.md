# Popwave Skills

This repository is the remote Skill Hub for Paopao projects.

Skill authors add or update packages under `skills/<skill-id>`. CI validates each skill, builds zip packages, generates `dist/registry.json`, and publishes the `dist` folder to a domestic object storage bucket behind CDN.

Default registry URL:

```text
https://skills.popwave.cn/registry.json
```

Backup registry URL:

```text
https://skills-backup.popwave.cn/registry.json
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

After merge, GitHub Actions builds the registry and syncs `dist/` to the configured domestic object storage bucket. Paopao users can refresh Skills in the app, install the new version, and the project will lock that version in `.paopao/skills/config.json`.

## Domestic CDN Publishing

Runtime users should not depend on GitHub availability. Keep GitHub as the collaboration repo, and publish the built static hub to a domestic CDN.

Recommended target:

```text
skills.popwave.cn -> CDN -> OSS/COS/TOS/Kodo/USS bucket
```

The bucket root must contain:

```text
registry.json
skills/
  <skill-id>/
    <version>/
      skill-package.zip
```

Configure repository secrets in GitHub Actions with placeholders for your chosen S3-compatible provider:

```text
SKILL_HUB_S3_PROVIDER=Alibaba
SKILL_HUB_S3_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
SKILL_HUB_S3_REGION=cn-hangzhou
SKILL_HUB_S3_BUCKET=popwave-skills
SKILL_HUB_ACCESS_KEY_ID=<access-key-id>
SKILL_HUB_SECRET_ACCESS_KEY=<secret-access-key>
SKILL_HUB_CDN_REFRESH_WEBHOOK=<optional-refresh-webhook>
```

Common provider values for `rclone` include `Alibaba`, `TencentCOS`, `AWS`, and `Minio`. If your provider is not S3-compatible, keep `npm run build` and replace only the publish step in `.github/workflows/publish.yml`.

## Release Channels

The build script publishes a `stable` channel for normal versions and a `beta` channel for prerelease versions. The latest stable version is used as `latest` when available.
