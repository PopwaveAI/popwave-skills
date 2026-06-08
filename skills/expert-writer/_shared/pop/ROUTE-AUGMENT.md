# ROUTE-AUGMENT.md — 路由信息增强映射表

> 在 expert-writer §3.1.5 执行。不替换子 skill 的输入，只追加。
> 铁律：只追加信息，不删除/过滤/归纳/总结。子 skill 自己决定用什么。

---

## 增强源

所有增强数据来自 `workspace-index.yaml`，锚定项目名称后按路由目标提取。

---

## 一、增强映射总表

### pop-novel-bookstrap（开书）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **跨项目 P0 教训** | `cross_project_lessons[]` where `applicable_to` contains `bootstrap` or `new_book` | 引用原文：「教训 {id}：{lesson}（来源：{source}，证据：{evidence}）」 |
| **已有拆解报告** | `reference_materials.deconstructions[]` — 如果用户指明了参考书，检查是否已拆 | 「已有拆解报告：`{path}`。无需重新拆解。若无对应的 T 文件则需补齐。」 |
| **已下载参考书 TXT** | `reference_materials.reference_novels[]` | 「已有 TXT：`{path}`」 |
| **可用风格档案** | `style_profiles.dna_profiles[]` + `style_profiles.writer_styles[]` | 「可用风格列表：{name}×{N} 个。建议选择 1 个做文风锚定。」 |

### pop-novel-deconstructor（拆书）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **已有拆解报告** | `reference_materials.deconstructions[]` — 按书名匹配 | 「该书已有拆解报告：`{path}` 下 {N} 个文件。如有 T 文件缺失则补齐，已有则跳过。」 |
| **已有 TXT 原文** | `reference_materials.reference_novels[]` | 「已有 TXT：`{path}`」 |

### pop-novel-plot（剧情架构）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **constitution 路径** | `projects[].constitution_ok` → 推断 `{项目}/02-大纲/constitution.yaml` | 「宪法路径：`{path}`」 |
| **reader_profile** | `projects[].reader_profile_ok` → 推断 `{项目}/00-总控/project.yaml` | 「读者画像在 project.yaml 的 reader_profile 字段」 |
| **跨项目 plot 教训** | `cross_project_lessons[]` where `applicable_to` contains `plot` | 引用原文 |
| **style_profile** | `projects[].style_profile` | 「项目风格：`{profile}`」 |
| **拆解报告（如有参考书）** | `reference_materials.deconstructions[]` | 「该参考书的 T4(剧情全貌) / T6(叙事技法) 已存在：`{path}`」 |

### pop-novel-writer（正文写作）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **场景规格预取 L1** | 读 act-XX.yaml 当前章的 `combat/dialogue/discovery/crisis` | 「场景类型：{type}。附加设置：{预取的相关 L1 文件路径}」 |
| **info_release 预取** | 读 act-XX.yaml 的 `info_release[].source_doc` | 「需释放设定及原文路径：{item_id} → `{source_doc}`」 |
| **canvas 路径** | 读 act-XX.yaml 的 `canvas_refs`（如有） | 「画布文件：{列表}」 |
| **上章未闭合节点** | 读上一章 design 文件 | 「上一章未闭合：{节点列表}（如有则需本章跟进）」 |
| **constitution 路径** | `projects[].constitution_ok` | 「宪法路径：`{path}`。本章相关条款：{提取结果}」 |
| **style 文件路径** | `projects[].style_profile` 或 `style_profiles.writer_styles[]` | 「风格文件：`{path}`」 |
| **跨项目 writer 教训** | `cross_project_lessons[]` where `applicable_to` contains `writing` | 引用原文（如 L002 精读闸门、L003 风格执行） |
| **pre_read_status** | `file_registry[项目].pre_read_status` | 「精读闸门状态：verified={bool}。{note}」 |

### pop-novel-qa（质检）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **constitution 路径** | `projects[].constitution_ok` | 「宪法路径：`{path}`」 |
| **style 文件路径** | `projects[].style_profile` | 「风格检验参考：`{path}`」 |
| **跨项目 qa 教训** | `cross_project_lessons[]` where `applicable_to` contains `qa` | 引用原文（如 L006 — QC 必须独立验证原文事实） |
| **需质检的正文路径** | `file_registry[项目].active` — 取 type=draft 的最新文件 | 「需质检：`{path}`」 |

### pop-dna（文风DNA）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **已有 DNA** | `style_profiles.dna_profiles[]` — 按书名匹配 | 「该书的 DNA 档案已存在：`{path}`。跳过提取，如有新增维度则补充。」 |

### pop-novel-html-renderer（发布）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **style_profile** | `projects[].style_profile` | 「风格文件：`{path}`。用于渲染配色/字体选择。」 |
| **reader_profile** | `projects[].reader_profile_ok` | 「读者画像：见 project.yaml」 |

### download-webnovel-txt（下载TXT）

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| **已有 TXT** | `reference_materials.reference_novels[]` — 按书名匹配 | 「已有 TXT：`{path}`。无需重复下载。」 |

### cnovel-research / book-opinion-tracker / knowledge-downloader

| 增强项 | 索引字段 | 给子 skill 的形式 |
|--------|---------|-----------------|
| — | 无固定增强 | 这三个 skill 的输入不依赖于项目索引数据 |

---

## 二、增强规则

### 规则 1：只追加，不删减

```
✅ 「宪法路径：{path}。本章相关条款：{提取结果}」
❌ 「宪法已读，跳过」
```

### 规则 2：只给路径，不给总结

```
✅ 「已在素材库找到拆解报告：素材库/拆解报告/深渊主宰-T1-力量体系规则手册.md 等 10 个文件」
❌ 「深渊主宰的拆解报告已经分析过，力量体系规则是 XXX」
```

### 规则 3：给原文引用，不给判断

```
✅ 「跨项目教训 L002：续写前必须精读倒数20章全文并输出事实提取报告。来源：海贼法典 CH389多弗朗明哥关系线错误」
❌ 「小心精读不足——上次海贼法典就出事了」
```

### 规则 4：缺失时不阻塞

```
✅ 「未找到该书的已有拆解报告，正常走 deconstructor 全流程」
❌ 静默跳过 / 报错终止
```

---

## 三、降级风险检查清单

执行增强后，自检：

- [ ] 子 skill 仍然需要读它自己的 SKILL.md？
- [ ] 子 skill 的核心决策没有被增强信息替代？
- [ ] 增强信息全部来自 workspace-index.yaml？
- [ ] 没有任何"所以你应该…"的推理式建议？
