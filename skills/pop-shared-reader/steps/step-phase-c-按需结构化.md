# Phase C -- 按需结构化（可选）

> 问了才做，不做也行。从已有笔记生成，不做"从原文重新提取"。

---

## 判断标准

问：把笔记变成数据库/HTML，对用户有实质帮助吗？

回答"有"：
- 角色极多需要检索
- 设定复杂需要交叉查询
- 用户明确说要

回答"没有"：
- 书不长、角色少
- 阅读笔记已经够用

---

## 可选工具

| 工具 | 用途 |
|:----|:----|
| `references/gen_html_knowledge_graph.py` | 从 novel.db 生成知识图谱 HTML（力导向图，零外部依赖） |

用法：
```
python references/gen_html_knowledge_graph.py <novel.db 路径> [--out 输出路径]
```

---

## 产出文件（按需）

```
小说项目/<书名>/
├── novel.db                        # Phase C（按需）
├── 数据库浏览器.html                # Phase C（按需）
└── 知识图谱.html                    # Phase C（按需）
```
