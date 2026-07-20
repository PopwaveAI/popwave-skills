# Step 2: 状态路由

> 每次对话开始，读project-state.md → 按phase值分流到对应Phase执行 → 完成后更新project-state.md。

---

## 读state

打开`project-state.md`，提取：

| 字段 | 用途 |
|------|------|
| phase | 当前在哪个阶段，决定路由 |
| current_chapter | Write阶段当前该写哪一章 |
| 参考书.书名 | Phase 0是否已完成 |
| 参考书.笔触DNA | 笔触DNA是否已部署 |

---

## 路由分流

### Phase: init

→ 执行Step 1初始化（创建目录+落盘project-state.md）→ 更新state到phase0 → 进Phase 0

### Phase: phase0（参考书闸门）

```
问用户："开工前先确认一下——有没有想参考笔触的书？
比如觉得哪本书的节奏/爽感/写法对胃口？
如果还没想好，我可以帮你搜几本同赛道卖得好的参考。"

用户回答 → 路由：

答案A·给了书名
  → Step 1: tool-download-webnovel 下载参考书
  → Step 2: pop-dna-style 提取笔触DNA（档位A笔触必做，档位B剧情brief可选）
     · 问用户："要不要顺便提取这本书的剧情DNA brief（爽点节奏/Boss梯度/主角成长曲线）？seed和plot可以用"
  → 更新project-state.md：
     参考书.书名 = 《XXX》
     参考书.本地文件 = ✅
     参考书.笔触DNA = ✅ 档位A / ✅ 档位A+B
     phase = phase1

答案B·没想好，需要推荐
  → Step 1: pop-research（种子级）调研同赛道热门 → 产出推荐书单
  → Step 2: 推荐书单呈现给用户 → 用户选1-2本
  → Step 3: tool-download-webnovel 下载
  → Step 4: pop-dna-style 提取DNA
  → 更新project-state.md：phase = phase1

答案C·明确拒绝（"不需要参考书"）
  → 再次确认："没有参考书的话，write skill的笔触DNA插槽会空转（trial模式），文章风格由API自由发挥，质量有波动。确定不要？"
  → 用户坚持拒绝 → 更新project-state.md：
     参考书.用户拒绝 = 是
     phase = phase1（附风险标注）
```

### Phase: phase1（Seed创意阶段）

```
前置检查：
  ✅ 参考书已就绪 或 用户已明确拒绝 → 放行
  ❌ 参考书未就绪 → 回到Phase 0

执行：
  → 调pop-fanqie-seed（v13.1.0）
  → 执行完整SOP：市场调研 → 纯自由发散 → 市场校准 → 用户选 → 结构化打磨 → 黄金首章
  → Seed产出的创意.md + ch001.md 落盘后
  → 更新project-state.md：
     phase = phase2
     current_chapter = ch001
     创意摘要.书名(暂) = seed产出
     创意摘要.一句话 = seed产出
     最近产出表追加 seed 行
```

### Phase: phase2（Plot世界构筑）

```
前置检查：
  ✅ 0-立项/创意.md 存在
  ✅ 2-正文/ch001.md 存在

执行：
  → 调pop-fanqie-plot（v9.1.0）
  → 执行完整SOP：加载创意文档 → 世界构筑 → 第一卷详规 → 四图叠加推演剧情白描 → 落盘
  → Plot产出的骨架/剧情白描/章锚点表落盘后
  → 更新project-state.md：
     phase = phase3
     current_chapter = ch002
     最近产出表追加 plot 行
```

### Phase: phase3（Write正文渲染）

```
前置检查：
  ✅ 1-骨架/剧情白描.md 存在
  ✅ 1-骨架/章锚点表.md 存在
  ✅ current-state.md 存在（首次进phase3时从project-state.md+创意摘要生成）

执行：
  → 调pop-fanqie-write（v8.0.0）
  → 写current_chapter指定的章节
  → chNNN.md 落盘后
  → 更新project-state.md：
     phase = phase4
     最近产出表追加 write 行
```

### Phase: phase4（Review审核沉淀）

```
前置检查：
  ✅ 2-正文/chNNN.md 存在

执行：
  → 调pop-fanqie-review（v4.1.0）
  → 四维审核 → 落盘审核-chNNN.md

结果A·通过
  → 更新project-state.md：
     phase = phase3
     current_chapter = ch{NNN+1}
     最近产出表追加 review 行

结果B·废章打回
  → 更新project-state.md：
     phase = phase3（current_chapter不变，回到同一章重写）
     最近产出表追加 review 行（标注"打回"）
```

---

## 更新project-state.md的方法

用SearchReplace工具编辑project-state.md中的以下字段：

1. `phase:` 行 → 更新为新phase值
2. `current_chapter:` 行 → 更新为当前章节号
3. 阶段完成情况 → 勾选完成的phase
4. 参考书区块 → 填写书名/文件路径/DNA状态
5. 创意摘要 → 填写seed产出
6. 最近产出表 → 追加新行

**更新后**，project-state.md的当前阶段变为下一个phase。对话中直接进入对应phase的Skill执行。

---

## 下一步

> 路由完成 → 进入对应phase执行 → 执行完成后回到本Step 2继续路由
