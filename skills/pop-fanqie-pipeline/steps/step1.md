# Step 1: 初始化项目

> 只在project-state.md不存在时执行。创建标准目录结构+落盘project-state.md。

---

## 1a. 确认项目目录

如果用户指定了项目名，以项目名为目录名；如果用户在当前项目目录下对话，使用当前目录。

如果当前工作目录下已有project-state.md，跳过初始化，直接进Step 2路由。

---

## 1b. 创建标准目录结构

```bash
New-Item -ItemType Directory -Force -Path "$projectDir/0-立项" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/1-骨架" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/2-正文" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/审核" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/涌现" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/downloads" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/写作参考" | Out-Null
New-Item -ItemType Directory -Force -Path "$projectDir/写作参考/知识沉淀" | Out-Null
```

---

## 1c. 落盘project-state.md

```markdown
# 项目：{项目名}

> 管线：番茄skill群 | 创建：{YYYY-MM-DD HH:MM}

## 当前阶段
phase: init
current_chapter: ch000

## 阶段完成情况
- [ ] Phase 0: 参考书就绪
- [ ] Phase 1: Seed → 创意.md + ch001.md
- [ ] Phase 2: Plot → 世界构筑 + 剧情白描 + 章锚点表
- [ ] Phase 3: Write → 逐章渲染 (当前: ch000)
- [ ] Phase 4: Review → 审核-chNNN.md

## 参考书
- 书名：未就绪
- 本地文件：downloads/{书名}.txt ❌
- 笔触DNA：涌现/文风锚定.md ❌
- 用户拒绝：否

## 创意摘要
- 书名(暂)：待seed产出
- 一句话：待seed产出

## 最近产出
| 阶段 | 产出文件 | 落盘时间 |
|------|---------|---------|
| pipeline | project-state.md | {timestamp} |
```

---

## 下一步

> Step 2: 路由。读project-state.md → 当前phase=init → 进入Phase 0参考书摸底
