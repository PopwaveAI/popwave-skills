# Skill 全量审计清单

> 当用户说"改造/优化/审计 skill"时，按此清单逐项检查。
> 来源：pop-writer-chapter v2.3.0 + pop-writer-plot v7.6.0 审计实战总结。

## 1. 版本一致性

逐文件检查版本号：

| 检查点 | 方法 |
|:-------|:-----|
| SKILL.md frontmatter `version` | vs SKILL.md 文末版本行 → 一致？ |
| SKILL.md 标题中的版本 | vs frontmatter → 一致？ |
| skill.json `version` | vs SKILL.md → 一致？ |
| CHANGELOG 最新条目 | vs 以上三者 → 一致？ |

**常见问题**：标题写 v7.3.0，但 frontmatter/skill.json/CHANGELOG 是 v7.6.0。

## 2. 路径一致性

全文件搜索下列过时路径模式：

| 旧路径（标记为过时） | 新路径 |
|:-------------------|:------|
| `00-总控/` | `状态/` |
| `设计/卷/volume-XX.md` | `剧情设计/卷/卷{N}-卷纲.md` |
| `设计/幕/act-XX.yaml` | `剧情设计/幕/vol-XX/act-YY.md` |
| `设计/剧情线/` | `剧情设计/剧情线/` |
| `写作资产/设计包/` | `章节设计包/` |
| `chekhov-tracker.md`（独立文件） | 已并入 act-YY.md 枪链段 |
| `chapters[N].canvas.xxx`（yaml 字段） | Canvas 表格（markdown） |

## 3. 幽灵引用

全文件搜索被引用但**实际不存在**的文件：

```bash
# 提取所有被引用的文件路径
grep -roP '(?<=`)[^`]+\.md(?=`)' SKILL.md steps/ references/ templates/
# 逐一验证文件是否存在
```

**常见幽灵**：`层架构.md`（creative 已删，world/chapter 仍在引）。

## 4. PRD 对齐

| 检查点 | 方法 |
|:-------|:-----|
| 入（inputs） | skill 实际 read 的文件 vs PRD 管线表的 "入" 列 → 一致？ |
| 出（outputs） | skill 实际 write 的文件 vs PRD 管线表的 "出" 列 → 一致？ |
| 用途 | skill 定位 vs PRD "用途" 列 → 一致？ |
| 上下游 | skill pipeline vs PRD 管线顺序 → 一致？ |

## 5. 文件索引完备性

```bash
# 列出目录下所有 .md 文件
find . -name "*.md" | sort
# 对比 SKILL.md 速查表中列出的文件
# 每个文件都应在速查表中有对应行（含"什么时候读"）
```

## 6. Step 负载检查

| 检查点 | 方法 |
|:-------|:-----|
| 预加载数量 | 每个 Step 的"读什么"列出多少文件？> 4 个考虑拆分 |
| 预加载 vs 按需查 | "读什么"中有没有可以懒加载的？标注"按需查" |
| Step 职责单一 | 是否混了不同类型的操作？（如事件链里同时做爽点标注） |

## 7. 速查表格式

| 检查点 | 标准 |
|:-------|:-----|
| 分组 | steps/ / templates/ / references/ / 外部依赖 四组 |
| 列 | 什么时候 \| 读什么文件 \| 产出 \| 门禁（steps 列） |
| 覆盖 | 目录下每个文件都在速查表中有对应行 |
