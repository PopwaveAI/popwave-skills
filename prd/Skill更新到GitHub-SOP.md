# Skill 更新到 GitHub SOP

> 本地仓库：`D:\popwave-skills`
> 远程仓库：`https://github.com/PopwaveAI/popwave-skills`
> 分支：`main`（主分支）

---

## 前置条件

- 本地已安装 git
- 已配置 GitHub 认证（SSH key 或 HTTPS credential）
- 当前机器有仓库 push 权限

验证认证和权限：

```powershell
cd D:\popwave-skills
git remote -v
# 应显示 origin https://github.com/PopwaveAI/popwave-skills.git (fetch/push)
```

---

## 完整流程

### Step 1 · 拉取最新代码

开始任何改动前，先同步远程，避免冲突：

```powershell
cd D:\popwave-skills
git pull origin main
```

如果有本地未提交的改动导致冲突，先 stash 或 commit（见下方「常见问题」）。

---

### Step 2 · 修改 Skill 文件

在本地正常编辑 skill 文件。典型场景：

| 场景 | 涉及目录 |
|:-----|:---------|
| 新建 skill | `skills/{skill-name}/` 下创建 SKILL.md、skill.json、CHANGELOG.md 等 |
| 修改现有 skill | 编辑 `skills/{skill-name}/` 下的对应文件 |
| 删除 skill | 删除 `skills/{skill-name}/` 整个目录 |
| 更新 PRD/规范文档 | 编辑 `prd/` 下对应文件 |

---

### Step 3 · 检查改动

提交前必须检查，确保只提交该提交的文件：

```powershell
# 查看哪些文件变了
git status

# 逐文件查看具体改动
git diff

# 查看新增未跟踪的文件
git status --short
```

**重点检查：**

- `.trae/`、`.uploads/`、`dist/`、`downloads/`、`.trae-html-share-packages/` 等目录不该提交（部分已在 `.gitignore` 中排除）
- `.zip` 压缩包不该提交
- 运行时产物（`_temp_*`、`temp_*`、`workspace-index.yaml` 等）不该提交，已由 `.gitignore` 排除
- 确认 skill.json 的 version 字段已更新，且与 SKILL.md、CHANGELOG.md 三处一致

---

### Step 4 · 暂存和提交

```powershell
# 暂存指定文件（推荐，精确控制）
git add skills/{skill-name}/SKILL.md skills/{skill-name}/skill.json skills/{skill-name}/CHANGELOG.md

# 或暂存整个 skill 目录
git add skills/{skill-name}/

# 提交，commit message 遵循约定式提交格式
git commit -m "feat({skill-name}): 一句话描述本次改动"
```

**commit message 格式：**

| 前缀 | 用途 | 示例 |
|:-----|:-----|:-----|
| `feat` | 新增功能/skill | `feat(pop-novel-seed): 新增种子卡生成 skill` |
| `fix` | 修复 bug | `fix(pop-decon): 修复 ETL 章节拆分多页抓取问题` |
| `refactor` | 重构（不改功能） | `refactor(pop-novel): 专家系列重命名` |
| `docs` | 文档更新 | `docs(prd): 更新 Skill 知识工程分享 PRD` |
| `chore` | 杂项（配置、依赖等） | `chore: 更新 .gitignore` |

---

### Step 5 · 推送到 GitHub

```powershell
git push origin main
```

推送后到 GitHub 仓库页面确认提交已出现：`https://github.com/PopwaveAI/popwave-skills/commits/main`

---

## 常见场景

### 场景 A · 新建一个 Skill 并提交

```powershell
cd D:\popwave-skills

# 1. 拉最新
git pull origin main

# 2. 创建 skill 目录和文件（在本地正常创建）
# skills/my-new-skill/SKILL.md
# skills/my-new-skill/skill.json
# skills/my-new-skill/CHANGELOG.md

# 3. 检查
git status

# 4. 暂存 + 提交
git add skills/my-new-skill/
git commit -m "feat(my-new-skill): 新增 xxx skill"

# 5. 推送
git push origin main
```

### 场景 B · 修改现有 Skill 的 SKILL.md

```powershell
cd D:\popwave-skills
git pull origin main

# 编辑文件（本地正常编辑）
# skills/pop-decon/SKILL.md → 修改内容
# skills/pop-decon/skill.json → version +1
# skills/pop-decon/CHANGELOG.md → 新增版本记录

git add skills/pop-decon/
git commit -m "refactor(pop-decon): SKILL.md 增加 SOP 骨架，调整红线定位"
git push origin main
```

### 场景 C · 本地有未提交改动，需要先拉取

```powershell
# 暂存本地改动
git stash

# 拉取远程
git pull origin main

# 恢复本地改动
git stash pop

# 如果有冲突，手动解决后继续
```

### 场景 D · 误提交了不该提交的文件

```powershell
# 从 git 中移除但保留本地文件
git rm --cached <file-path>

# 加入 .gitignore（防止下次再被跟踪）
# 编辑 .gitignore 添加该路径

git add .gitignore
git commit -m "chore: 从 git 移除误提交的文件并加入 gitignore"
git push origin main
```

---

## .gitignore 速查

仓库已配置 `.gitignore`，以下内容自动排除：

| 排除项 | 说明 |
|:-------|:-----|
| `dist/` `node_modules/` | 构建产物 |
| `.trae/` | IDE 配置 |
| `_temp_*` `temp_*` `.tmp/` | 运行时临时文件 |
| `workspace-index.yaml` | 运行时状态文件 |
| `_projects/` `.tmp-deconstruction/` | 中间数据 |
| `*.pyc` `__pycache__/` | Python 编译产物 |
| `chapters_map.txt` `git_changes_temp.txt` | 子 agent 生成的临时文件 |

**需手动注意的（未在 .gitignore 中）：**

- `.trae-html-share-packages/` — HTML 分享包，不应提交
- `.uploads/` — 上传文件暂存，不应提交
- `downloads/` — 下载文件暂存，不应提交
- `*.zip` — 压缩包，不应提交

如果这些目录频繁出现在 `git status` 中，建议追加到 `.gitignore`。

---

## 检查清单

提交前逐项确认：

- [ ] 已 `git pull origin main` 拉取最新代码
- [ ] `git status` 检查无误提交文件
- [ ] skill.json 的 version 已更新
- [ ] version 在 SKILL.md、skill.json、CHANGELOG.md 三处一致
- [ ] commit message 符合约定式提交格式
- [ ] `git push origin main` 推送成功
