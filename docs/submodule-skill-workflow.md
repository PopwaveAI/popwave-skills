# Submodule Skill 接入与维护流程

本文说明如何把独立仓库维护的大型 Skill 以 Git submodule 的形式接入 Popwave Skills Hub。

## 一、是否适合使用 submodule

适合使用 submodule 的情况：

- Skill 内容较大，包含大量 `references/`、`examples/` 或 `scripts/`。
- Skill 有独立负责人或独立团队维护。
- Skill 有自己的 issue、评审、发布节奏或测试流程。
- Skill 可能被多个 Skill Hub 或项目复用。
- 不希望把大型资料直接复制进本仓库。

不建议使用 submodule 的情况：

- Skill 很小，只包含一个 `SKILL.md` 和简单配置。
- Skill 只由本仓库维护，没有独立发布需求。
- 维护成员不熟悉 Git submodule，且没有技术同事协助。

建议原则：大型、独立、多人维护的 Skill 用 submodule；小型、简单、强依赖本仓库的 Skill 直接放在 `skills/` 下。

## 二、目录约定

所有 submodule Skill 仍然必须放在：

```text
skills/<skill-id>/
```

例如：

```text
skills/cnovel-research/
```

submodule 仓库根目录必须包含：

```text
skill.json
SKILL.md
CHANGELOG.md
README.md
```

其中：

- `skill.json.id` 必须和 `<skill-id>` 完全一致。
- `skill.json.version` 必须在 Skill 仓库内更新。
- `CHANGELOG.md` 必须记录本次版本变化。

## 三、首次接入一个独立 Skill 仓库

以下命令需要在本仓库根目录执行。

### 1. 添加 submodule

```bash
git submodule add <skill-repo-url> skills/<skill-id>
```

示例：

```bash
git submodule add git@github.com:popwave/skill-cnovel-research.git skills/cnovel-research
```

如果仓库使用 HTTPS：

```bash
git submodule add https://github.com/popwave/skill-cnovel-research.git skills/cnovel-research
```

### 2. 检查 `.gitmodules`

添加后，本仓库会出现或更新 `.gitmodules`：

```ini
[submodule "skills/cnovel-research"]
  path = skills/cnovel-research
  url = git@github.com:popwave/skill-cnovel-research.git
```

确认：

- `path` 是 `skills/<skill-id>`。
- `url` 指向正确的独立 Skill 仓库。

### 3. 校验 Skill 内容

```bash
npm run build
```

校验成功后，再提交本仓库里的变更：

```bash
git add .gitmodules skills/<skill-id>
git commit -m "Add <skill-id> skill submodule"
```

注意：本仓库提交的是 submodule 指向的 commit，不会把独立仓库的全部文件复制进来。

## 四、克隆本仓库后的初始化

新成员第一次克隆本仓库后，需要拉取 submodule 内容。

推荐：

```bash
git clone --recurse-submodules <hub-repo-url>
```

如果已经普通克隆了本仓库，则运行：

```bash
npm run skills:sync
```

这条命令等价于：

```bash
git submodule update --init --recursive
```

## 五、修改 submodule Skill 的标准流程

submodule Skill 的修改分两步：先改 Skill 独立仓库，再更新 Hub 仓库里的 submodule 指针。

### 1. 在 Skill 独立仓库中修改

进入 Skill 目录：

```bash
cd skills/<skill-id>
```

修改对应文件，例如：

```text
SKILL.md
skill.json
CHANGELOG.md
references/
examples/
scripts/
```

然后在 Skill 仓库内提交：

```bash
git add .
git commit -m "Update <skill-id> behavior"
git push
```

如果这次修改会发布给用户，请确认：

- `skill.json.version` 已更新。
- `CHANGELOG.md` 已记录变化。
- 权限变化已在 `skill.json` 中声明。
- 输出格式变化已在 `SKILL.md` 中说明。

### 2. 回到 Hub 仓库更新 submodule 指针

回到本仓库根目录：

```bash
cd ../..
```

查看状态：

```bash
git status
```

你会看到类似：

```text
modified: skills/<skill-id> (new commits)
```

这表示 Hub 仓库记录的 submodule commit 需要更新。

运行校验：

```bash
npm run build
```

提交 Hub 仓库里的指针更新：

```bash
git add skills/<skill-id>
git commit -m "Update <skill-id> submodule"
```

然后发起 Hub 仓库 PR。

## 六、只更新到远端最新版本

如果 Skill 独立仓库已经有人合并了更新，你只需要让 Hub 指向最新 commit：

```bash
git submodule update --remote skills/<skill-id>
npm run build
git add skills/<skill-id>
git commit -m "Update <skill-id> submodule"
```

建议不要在没有评审的情况下批量更新所有 submodule。每次只更新需要发布的 Skill，更容易回溯问题。

## 七、发布规则

Hub 发布时会打包当前仓库记录的 submodule commit。

这意味着：

- Skill 独立仓库合并后，不会自动发布。
- 必须在 Hub 仓库中更新 submodule 指针并合并 PR，才会发布到 Skill Hub。
- 如果 Hub 仓库没有更新指针，即使 Skill 独立仓库有新 commit，线上仍然发布旧版本。

发布前请检查：

```bash
git submodule status
```

输出中的 commit 就是本次 Hub 将使用的 Skill 版本来源。

## 八、CI 与发布流水线

本仓库的 CI 和发布流水线会递归 checkout submodule：

```yaml
submodules: recursive
```

因此只要 submodule 仓库可访问，下面命令会照常执行：

```bash
npm run build
```

构建脚本仍然扫描：

```text
skills/<skill-id>/skill.json
```

所以 submodule Skill 和普通 Skill 在最终 registry 中没有区别。

## 九、私有 submodule 仓库注意事项

如果 submodule 仓库是私有仓库，GitHub Actions 需要有权限拉取它。

推荐做法：

1. 优先把 submodule 仓库放在同一个 GitHub 组织下。
2. 给 CI 使用只读权限的机器用户或细粒度 Token。
3. 在 Hub 仓库 secrets 中保存 Token。
4. 如默认 `GITHUB_TOKEN` 无法读取私有 submodule，请让技术同事调整 `.github/workflows/*.yml` 的 checkout 配置。

不要把访问 Token 写进：

- `.gitmodules`
- `README.md`
- `skill.json`
- 任何提交到仓库的文件

## 十、常见问题

### 为什么我看不到 submodule 里的文件？

可能还没有初始化 submodule。运行：

```bash
npm run skills:sync
```

### 为什么 `npm run build` 提示缺少 `skill.json`？

常见原因：

- submodule 没有拉取成功。
- submodule 路径不是 `skills/<skill-id>`。
- Skill 独立仓库根目录没有 `skill.json`。
- `skill.json.id` 和文件夹名不一致。

### 为什么 Skill 独立仓库已经更新了，线上还没变？

因为 Hub 仓库记录的是固定 commit。需要在 Hub 仓库更新 submodule 指针、发 PR，并合并到 `main` 后才会发布。

### 可以把 submodule 指向某个分支吗？

可以配置跟踪分支，但发布仍然建议以 Hub 仓库记录的 commit 为准。这样每次发布都可追溯、可回滚。

### 可以把普通 Skill 改成 submodule 吗？

可以。建议流程：

1. 新建独立 Skill 仓库。
2. 把原 `skills/<skill-id>/` 内容迁移到独立仓库。
3. 确认独立仓库根目录包含 `skill.json`、`SKILL.md`、`CHANGELOG.md`。
4. 删除 Hub 仓库中的原目录。
5. 使用 `git submodule add <skill-repo-url> skills/<skill-id>` 接回同一路径。
6. 运行 `npm run build`。
7. 发起 PR。

## 十一、PR 检查清单

提交 submodule 相关 PR 前请确认：

- [ ] `.gitmodules` 中的 `path` 和 `url` 正确。
- [ ] submodule 路径是 `skills/<skill-id>`。
- [ ] submodule 根目录包含 `skill.json`、`SKILL.md`、`CHANGELOG.md`。
- [ ] `skill.json.id` 和 `<skill-id>` 一致。
- [ ] `skill.json.version` 已按修改程度更新。
- [ ] `CHANGELOG.md` 已记录变化。
- [ ] 已运行 `npm run skills:sync`。
- [ ] 已运行 `npm run build`。
- [ ] 私有仓库的 CI 读取权限已确认。
