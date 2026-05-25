# Popwave Skills

本仓库是泡泡项目的远程 Skill Hub。

Skill 作者在 `skills/<skill-id>` 下新增或更新技能包。CI 会校验每个 Skill，构建 zip 包，生成 `dist/registry.json`，并将 `dist` 目录发布到接入 CDN 的国内对象存储桶。

默认 registry 地址：

```text
https://skills.popwave.cn/registry.json
```

备用 registry 地址：

```text
https://skills-backup.popwave.cn/registry.json
```

## Skill 目录结构

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

`skill.json` 是面向应用的清单文件。`SKILL.md` 是面向模型的指令入口。

## 作者工作流

1. 创建或编辑 `skills/<skill-id>`。
2. 按照 SemVer 规范更新 `skill.json.version`。
3. 更新 `CHANGELOG.md`。
4. 运行：

```bash
npm install
npm run build
```

5. 发起 PR。

合并后，GitHub Actions 会构建 registry，并将 `dist/` 同步到已配置的国内对象存储桶。泡泡用户可以在应用中刷新 Skills、安装新版本，项目会在 `.paopao/skills/config.json` 中锁定该版本。

## 国内 CDN 发布

运行时用户不应依赖 GitHub 的可用性。建议将 GitHub 作为协作仓库，同时把构建后的静态 Skill Hub 发布到国内 CDN。

推荐目标架构：

```text
skills.popwave.cn -> CDN -> OSS/COS/TOS/Kodo/USS bucket
```

存储桶根目录必须包含：

```text
registry.json
skills/
  <skill-id>/
    <version>/
      skill-package.zip
```

在 GitHub Actions 中配置仓库 secrets。以下是适用于所选 S3 兼容服务商的占位示例：

```text
SKILL_HUB_S3_PROVIDER=Alibaba
SKILL_HUB_S3_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
SKILL_HUB_S3_REGION=cn-hangzhou
SKILL_HUB_S3_BUCKET=popwave-skills
SKILL_HUB_ACCESS_KEY_ID=<access-key-id>
SKILL_HUB_SECRET_ACCESS_KEY=<secret-access-key>
SKILL_HUB_CDN_REFRESH_WEBHOOK=<optional-refresh-webhook>
```

`rclone` 常见的服务商取值包括 `Alibaba`、`TencentCOS`、`AWS` 和 `Minio`。如果你的服务商不兼容 S3，请保留 `npm run build`，只替换 `.github/workflows/publish.yml` 中的发布步骤。

## 发布通道

构建脚本会为普通版本发布 `stable` 通道，为预发布版本发布 `beta` 通道。当存在稳定版本时，最新稳定版本会作为 `latest` 使用。
