# Step 1 · 素材生产

> 本步骤把"三可"价值（可截图×可套用×可回看）传导为可渲染的JSON数据。每个字段都是三可的载体——漏字段=三可缺失。消费 `references/content-method.md` 方法论，产出可直接喂给 Step 2 的完整JSON。

---

## 输入

用户提供的素材主题（如"恨海情天""100个古言氛围细节""病美人写法"），以及可选的账号配置（账号名/署名/收尾语/配色偏好）。

---

## 执行流程

### 1. 读取方法论

```
Get-Content -Encoding UTF8 -Raw references/content-method.md
```

### 2. 主题分析

分析用户给的主题，判断：

- 属于哪种素材类型（桥段/字句/人设/写法）？
- 核心卖点是什么？（读者第一眼想搜/想存的词）
- 对应 content-method.md 中哪种5页结构？

### 3. 内容生产

按素材类型对应的生产原则生产内容。核心质量标准（详见 content-method.md 第三节）：

- 每条素材句必须包含三层：物件/动作 + 感官细节 + 情绪暗示
- 素材句要有"可改写性"：换掉身份/场景/代价就能复用
- 正误对照的"好"例子必须比"坏"例子多一层具体细节
- 名场面必须包含"选择"和"代价"
- 封面钩子句必须：具体物件/动作 + 情绪张力

### 4. 按JSON格式组织产出

**产出格式为JSON**（不是Markdown），字段名与HTML母版占位符一一对应。详见 content-method.md 第七节字段清单。

桥段型完整JSON模板（60个内容字段 + 8个账号字段 = 68字段）：

```json
{
  "{{TITLE}}": "主题名",
  "{{TOOLBAR_TITLE}}": "工具栏标题",
  "{{ACCOUNT_NAME}}": "账号名",
  "{{ACCOUNT_INITIAL}}": "头像首字",
  "{{FOOTER_SIGN}}": "页脚左",
  "{{FOOTER_TAG}}": "页脚右",
  "{{CLOSING_LINE}}": "收尾语",
  "{{SIGNOFF_TEXT}}": "收尾视觉文字",

  "{{KICKER}}": "P1标签",
  "{{TITLE_MAIN}}": "封面主标题",
  "{{COVER_SUB}}": "封面副标题",
  "{{COVER_HOOK}}": "封面钩子句（具体物件/动作+情绪张力）",
  "{{COVER_DECO_TEXT}}": "封面装饰文字",

  "{{TOPIC_LABEL_2}}": "P2标签",
  "{{TOPIC_TITLE_2}}": "P2标题",
  "{{TOPIC_DESC_2}}": "P2描述",
  "{{FORMULA_MAIN}}": "核心公式",
  "{{FORMULA_KEY_1}}": "公式要素1", "{{FORMULA_VAL_1}}": "解释1",
  "{{FORMULA_KEY_2}}": "公式要素2", "{{FORMULA_VAL_2}}": "解释2",
  "{{FORMULA_KEY_3}}": "公式要素3", "{{FORMULA_VAL_3}}": "解释3",
  "{{FORMULA_KEY_4}}": "公式要素4", "{{FORMULA_VAL_4}}": "解释4",
  "{{QUOTE_1}}": "素材句1（触觉/视觉层）",
  "{{QUOTE_2}}": "素材句2（物件层）",
  "{{QUOTE_3}}": "素材句3（动作层）",
  "{{QUOTE_4}}": "素材句4（信息层）",

  "{{TOPIC_LABEL_3}}": "P3标签",
  "{{TOPIC_TITLE_3}}": "P3标题",
  "{{TOPIC_DESC_3}}": "P3描述",
  "{{CONTRAST_BAD_TITLE_1}}": "坏例1标题", "{{CONTRAST_BAD_1}}": "坏例1内容",
  "{{CONTRAST_GOOD_TITLE_1}}": "好例1标题", "{{CONTRAST_GOOD_1}}": "好例1内容",
  "{{CONTRAST_BAD_TITLE_2}}": "坏例2标题", "{{CONTRAST_BAD_2}}": "坏例2内容",
  "{{CONTRAST_GOOD_TITLE_2}}": "好例2标题", "{{CONTRAST_GOOD_2}}": "好例2内容",
  "{{SUMMARY_TITLE_3}}": "总结标题", "{{SUMMARY_COPY_3}}": "总结内容",

  "{{TOPIC_LABEL_4}}": "P4标签",
  "{{TOPIC_TITLE_4}}": "P4标题",
  "{{TOPIC_DESC_4}}": "P4描述",
  "{{SCENE_TITLE_4}}": "名场面标题",
  "{{SCENE_EXAMPLE_4}}": "完整名场面（含选择+代价+情绪反差）",
  "{{BREAKDOWN_1A}}": "拆解1标题", "{{BREAKDOWN_1B}}": "拆解1内容",
  "{{BREAKDOWN_2A}}": "拆解2标题", "{{BREAKDOWN_2B}}": "拆解2内容",
  "{{BREAKDOWN_3A}}": "拆解3标题", "{{BREAKDOWN_3B}}": "拆解3内容",
  "{{ROUTE_TITLE_A}}": "动作设计标题", "{{ROUTE_COPY_A}}": "动作设计内容",
  "{{ROUTE_TITLE_B}}": "情绪设计标题", "{{ROUTE_COPY_B}}": "情绪设计内容",

  "{{TOPIC_LABEL_5}}": "P5标签",
  "{{TOPIC_TITLE_5}}": "P5标题",
  "{{TOPIC_DESC_5}}": "P5描述",
  "{{ENDING_KEY_1}}": "HE", "{{ENDING_VAL_1}}": "HE结局",
  "{{ENDING_KEY_2}}": "BE", "{{ENDING_VAL_2}}": "BE结局",
  "{{ENDING_KEY_3}}": "OE", "{{ENDING_VAL_3}}": "OE结局",
  "{{ENDING_KEY_4}}": "转折", "{{ENDING_VAL_4}}": "转折结局"
}
```

字句型：P2-P4替换为 `{{ITEM_1}}` ~ `{{ITEM_20}}`（每页15-20条），P5改为使用指南字段。
人设型/写法型：参考 content-method.md 第二节对应结构调整字段。

### 5. 字段校验门禁

**JSON产出后，必须执行以下校验。任一不通过 = 回去补内容，禁止进入Step 2。**

校验清单（详见 content-method.md 第八节）：

1. **字段完整性**〔可截图〕：统计JSON key数量。桥段型必须有68个字段（60内容+8账号）。缺一个都不行。
2. **字段非空**〔可截图〕：每个value ≥ 5字，无空字符串。
3. **素材句三层**〔可截图+可套用〕：每条 `{{QUOTE_1~4}}` 含物件/动作 + 感官 + 情绪暗示。
4. **正误对照差异**〔可套用〕：每组好例（`CONTRAST_GOOD`）比坏例（`CONTRAST_BAD`）多一层具体细节。
5. **名场面三要素**〔可回看〕：`{{SCENE_EXAMPLE_4}}` 含"选择"+"代价"+"情绪反差"。
6. **封面钩子句**〔可截图〕：`{{COVER_HOOK}}` 含具体物件/动作 + 情绪张力。
7. **结局可套用**〔可套用+可回看〕：每个 `{{ENDING_VAL}}` 含具体物件/动作 + 代价 + 记忆点。
8. **感官覆盖**〔可截图〕：`{{QUOTE_1~4}}` 覆盖 ≥3种感官通道。

**校验通过 → 落盘JSON，进入Step 2。校验不通过 → 回第3步补内容。**

---

## 产出

一份JSON文件（`{主题}-content.json`），包含全部68个字段，字段名与HTML母版占位符一一对应。这份JSON是 Step 2 的直接输入。

---

## ⛔ 加载门禁 + 下一步指引

> JSON落盘且通过8项校验后，禁止跳过 Step 2 直接手写 HTML。
>
> 下一 step：`steps/step2-visual.md`
> 加载指令：`Get-Content -Encoding UTF8 -Raw steps/step2-visual.md`
> 什么时候进入下一步：JSON已落盘，8项校验全部通过
