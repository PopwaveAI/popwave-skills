# OC 设定卡设计方案

## 基本信息

- **小说标题**：{{title}}
- **内容类型**：{{type}}（人物卡/势力卡/地理卡/规则卡/场景卡）
- **实体名**：{{entity_name}}
- **实体称号/定位**：{{entity_title}}
- **档位**：{{tier}}（基础版/加强版/设定卡传播版/HTML组装版）
- **画幅比例**：{{ratio}}
- **输出尺寸**：{{size}}

## 设定档案

- **档案文件**：`素材/[类型][实体名]档案.md`（或 `素材/场景资产表.md`）
- **美术设定集篇**：`素材/美术设定集.md` → {{bible_section}}（唯一真源）
- **核心气质**：{{core_temperament}}
- **选取形态/场景**：{{selected_scene}}（第{{line_number}}行）
- **形态/场景描述**：{{scene_description}}

## 系列化规划（如需）

| 图序 | 形态/场景 | 服饰/层级/细节 | 姿态/构图 | 变量 | 文字层 |
|:-----|:---------|:-------------|:---------|:-----|:-------|
| {{fig_1}} | {{scene_1}} | {{costume_1}} | {{pose_1}} | {{var_1}} | {{text_1}} |
| {{fig_2}} | {{scene_2}} | {{costume_2}} | {{pose_2}} | {{var_2}} | {{text_2}} |

### 冻结特征（系列一致性，按类型）
1. {{frozen_feature_1}}（如人物：暗金眸子 / 势力：标志色+纹饰 / 地理：空间氛围 / 规则：视觉外显 / 场景：场景基调）
2. {{frozen_feature_2}}
3. {{frozen_feature_3}}

## 信息架构

### 人物卡六层（基础版/加强版）

| 层级 | 内容 | 位置 | 字体/质感 |
|:-----|:-----|:-----|:---------|
| 第1层 | {{name_identity}} | {{position_1}} | {{font_1}} |
| 第2层 | {{title_text}} | {{position_2}} | {{font_2}} |
| 第3层 | {{biography}} | {{position_3}} | {{font_3}} |
| 第4层 | {{poem}} | {{position_4}} | {{font_4}} |
| 第5层 | {{calligraphy}} | {{position_5}} | {{font_5}} |
| 第6层 | {{seal}} | {{position_6}} | {{font_6}} |

### 设定卡传播版模块化信息（所有类型通用）

| 模块 | 内容 | 位置 | 字体/质感 |
|:-----|:-----|:-----|:---------|
| 主视觉 | {{hero_visual}} | {{hero_position}} | 无文字 |
| 标题区 | {{title_area}}（实体名·定位，≤8字） | {{title_position}} | {{title_font}} |
| 属性/标签栏 | {{attr_bar}}（≤4字/项，最多5-6项） | {{attr_position}} | {{attr_font}} |
| 配色板 | {{palette}}（3-5色块） | {{palette_position}} | 无文字，仅色块 |
| 象征/地标/层级 | {{symbols}}（≤4字/项） | {{symbols_position}} | {{symbols_font}} |
| 口号/隐喻/台词 | {{quote}}（≤15字） | {{quote_position}} | {{quote_font}} |

> 设定卡传播版总模块≤7，文字均≤15字，宁减模块保清晰。

> 规则卡注：主视觉载体（器物/天象/纹路）必须来自美术设定集规则篇，无凭空发明符号。

### HTML组装版·画册页（第四档位）

> 必读 `references/mode-album-html.md`。范式：一张图放页面中央，四周 HTML 装裱排版。图是主角，HTML 是装裱。

| 模块 | 内容 | 位置 |
|:-----|:-----|:-----|
| 主视觉（无文字） | {{hero_visual}}（AI 出图，保留 no text） | 中央独立 `<figure>` 图框 |
| 顶部标题区 | 系列名 {{series}} / 类型标签 {{type}} / 实体名 {{entity_name}}（鎏金大字）/ 定位 {{entity_title}} | 图框上方 |
| 信息区-箴言 | {{mantra}}（压图下缘，金光） | 图框下方 |
| 信息区-核心气质 | {{core_temperament}}（一句短句，可加粗高亮） | 图框外 |
| 信息区-等级/色板 | {{level_palette}}（横向色块阵列） | 图框外 |
| 信息区-象征 | {{symbols}}（两栏词条，≤4字/项） | 图框外 |
| 品牌水印 | popwave.cn 让创意一键落地 | footer（已内嵌，不走 watermark.py） |

> 画册页三铁律：A1 图是主角（禁止铺满当 background）；A2 主视觉零文字；A3 信息区在图框之外。

## 布局模板

- **选择**：{{layout_template}}（人物：底部面板型/侧边条型/叠加层型/四角分布型/右侧古籍版式型；设定实体卡：设定卡模块化版式；HTML组装版：画册页版式）
- **主视觉占比**：{{hero_ratio}}

## 参考图（如有）

- **参考图**：{{reference_image}}
- **参考点**：{{reference_point}}

## 提示词记录

<!-- 生成完成后在此追加提示词记录 -->

## 门禁A：设定档案确认

### 用户反馈
{{gate_a_feedback}}

## 门禁B：方案对齐

### 设计方案
{{confirmed_design}}

### 用户反馈
{{gate_b_feedback}}

---

> 本设计方案由 popwave 生成