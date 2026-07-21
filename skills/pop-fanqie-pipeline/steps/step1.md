# Step 1: 初始化项目

> 只在project-state.md不存在时执行。创建标准目录结构+落盘project-state.md+生成project-state.html。

---

## 1a. 确认项目目录

如果用户指定了项目名，以项目名为目录名；如果用户在当前项目目录下对话，使用当前目录。

如果当前工作目录下已有project-state.md，跳过初始化，直接进Step 2路由。

---

## 1b. 创建标准目录结构（v3.2.0四文件夹+设计子目录）

```powershell
New-Item -ItemType Directory -Force -Path "$projectDir/素材" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/素材/downloads" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/素材/知识沉淀" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/设计" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/设计/全书设定" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/设计/角色库" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/设计/第一卷剧情" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/正文" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/审核" | Out-Null
```

**目录用途**：
| 文件夹 | 存什么 | 对应Phase |
|:--|:--|:--|
| 素材/ | 调研+DNA+拆书+原书 | Phase 0产出 |
| 设计/ | 创意（根目录）+全书设定+角色库+第一卷剧情 | Phase 1-3.5产出 |
| 正文/ | 逐章渲染 | Phase 4产出 |
| 审核/ | 审核记录 | Phase 5产出 |

---

## 1c. 落盘project-state.md

```markdown
# 项目：{项目名}

> 管线：番茄skill群 | 创建：{YYYY-MM-DD HH:MM} | 更新：{YYYY-MM-DD HH:MM}

## 当前阶段
phase: init
current_chapter: ch000

## 阶段完成情况
- [ ] Phase 0: 用户意图 + 并发前置准备
- [ ] Phase 1: Seed → 设计/创意.md + 正文/ch001.txt
- [ ] Phase 2: World → 设计/全书设定/（多文件）
- [ ] Phase 3: Plot → 设计/第一卷剧情/剧情白描.md
- [ ] Phase 3.5: Character → 设计/角色库/角色库.md
- [ ] Phase 4: Write → 正文/chXXX.txt (当前: ch000)
- [ ] Phase 5: Review → 审核/review-chXXX.md

## 底牌就绪
- 用户意图：素材/用户意图.md ❌
- 赛道调研：素材/赛道调研.md ❌
- 参考书下载：skipped
- 笔触DNA：素材/文风锚定.md ❌
- decon-lite：素材/decon-lite-{书名}.md ❌

## 创意摘要
- 书名(暂)：待seed产出
- 一句话：待seed产出

## 最近产出
| 阶段 | 产出文件 | 落盘时间 |
|------|---------|---------|
| pipeline | project-state.md | {timestamp} |
```

---

## 1d. 生成project-state.html

运行脚本生成HTML：

```bash
python skills/pop-fanqie-pipeline/scripts/generate-state-html.py {projectDir}/project-state.md
```

脚本自动读取project-state.md → 解析字段 → 替换模板占位符 → 同目录生成project-state.html。

**禁止手动写HTML**——必须用脚本生成。

---

## 下一步

> Step 2: 路由。读project-state.md → 当前phase=init → 进入Phase 0用户意图深问
