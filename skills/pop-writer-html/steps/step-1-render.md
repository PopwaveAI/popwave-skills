# Step 1：执行渲染流程

> 管线: pop-writer-html v1.3

---

## 目的

将小说正文/设定/场景卡等结构化数据，通过三步调用完成一次发布。

---

## 执行

### 第一步：前置决策（NodeF.decide）

| 项目 | 内容 |
|:-----|:------|
| 读什么 | 文档类型 / 受众 / 效果目标 / 规格说明 |
| 做什么 | 调用 `NodeF.decide()` 确定设计系统（Swiss / Guizang / Kami / Glitch 等 27 种之一） |
| 产出什么 | intent 决议对象（含 resolved_skill） |
| ❌ 门禁 | `doc_type` / `audience` 任一缺失 → 抛出 `ValueError`，列出缺失字段 |

```python
intent = NodeF.decide(
    doc_type="scene_card",
    doc_name="场景卡-001-纸身",
    audience="readers",
    goal="horror_immersion",
    specialization="游戏UI切入→恐怖排版收尾"
)
```

### 第二步：执行渲染（render）

| 项目 | 内容 |
|:-----|:------|
| 读什么 | intent 决议 + 上游结构化数据（dict / YAML） |
| 做什么 | 调用 `HTMLRenderer.render()` 生成 HTML |
| 产出什么 | 单文件 HTML（写入 `宣传/` 子目录） |
| ❌ 门禁 | `pop-shared-html` 未安装 → 抛出 `ImportError` |

```python
renderer = HTMLRenderer()
html = renderer.render(intent.resolved_skill, data, output_path)
```

### 第三步：质量验证

| 项目 | 内容 |
|:-----|:------|
| 做什么 | 逐项检查质量红线 |
| 产出什么 | 验证报告 / 修复动作 |
| ❌ 门禁 | 任一项未通过 → 阻塞修正，不跳过 |

---

## 产出

- 单文件 HTML → 写入 `宣传/` 子目录
- 告知用户："已写入 {路径}。预览核心：{视觉效果描述}。需调整告诉我。"
