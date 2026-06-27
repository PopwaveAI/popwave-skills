# Step2：信息获取 — 设定指针强制读取 + library按需查询 + pop-research

> **执行者**：主会话
> **输入**：导演意图的 settings_ref + 写作参考/索引.md + 活记忆 + 前章正文
> **产出**：info_acquired 记录（含设定文件读取清单+查询结果摘要）
> **人工check**：无（自动进入Step3）
> **红线**：无（本步无人工check，自动连贯）

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
```

---

## A. 设定指针强制读取（机械执行）

> 导演意图的 settings_ref 列表是硬指针。指针指向了就必须读。不靠agent判断。

1. 从 Step0 产出的导演意图 YAML 中提取 `settings_ref` 列表
2. 对每个指针，`Get-Content -Raw` 读取对应文件：

   ```powershell
   # 示例
   Get-Content -Raw '写作参考/设定/金手指.md'
   Get-Content -Raw '写作参考/设定/主角引擎.md'
   ```

3. 记录读取结果到 info_acquired：

   ```yaml
   settings_read:
     - path: "写作参考/设定/金手指.md#升级机制"
       status: full          # full=完整读取 / partial=部分读取（需修复）
       size: 2048            # 文件大小（bytes）
       key_points:           # 提取的关键信息
         - "升级触发条件：击杀+危机值达标"
         - "升级后属性+2，解锁感知技能"
     - path: "写作参考/设定/主角引擎.md#行为准则"
       status: full
       size: 1536
       key_points:
         - "保护欲驱动行为优先级"
         - "冷静决策，不冲动"
   ```

### 强制读取规则

- settings_ref 列表中的每个指针 **必须读取**，无一例外
- 读取状态必须为 `full`（完整读取）
- 如某个文件读取失败（文件不存在/路径错误）→ **暂停并报错**，不允许跳过
- 读取结果将在 Step4 receipt检查中被验证（settings_ref全部status=full）

---

## B. 按需查询（agent判断）

> 以下查询由agent根据本章需要判断是否执行。非强制，但鼓励充分获取信息。

### B1. 写作参考索引查询

1. `Get-Content -Encoding UTF8 -Raw` 读取 `写作参考/索引.md`
2. 扫描索引中的设定/知识沉淀文件列表
3. 判断是否有与本章相关的额外参考文件
4. 如有 → `Get-Content -Raw` 读取该文件 → 记录到 info_acquired

### B2. library套路库/L2卡参考

1. 查询 pop-trope-library（公共知识库）：
   - 套路库：本章涉及的网文套路（如"反杀套路"、"系统流升级"）
   - 剧情库L2卡：同类题材的L2卡结构参考样本
2. 如查询到相关内容 → 记录到 info_acquired.library_refs

### B3. pop-research（如需）

> pop-research 尚未创建，暂用 WebSearch 替代。

1. 判断本章是否需要外部调研（如：特定行业知识、地理细节、历史背景）
2. 如需 → 调用 pop-research（或 WebSearch）
3. 调研结果如有长期参考价值 → 沉淀到 `写作参考/知识沉淀/` 并更新 `写作参考/索引.md`

### B4. 前文细节查询

1. 从活记忆中提取本章需要延续的前文细节
2. 如需精确引用前文 → `Get-Content -Raw` 读取对应 `正文/chXXX.md`
3. 通常读取上一章末尾（500-800字）作为Step3的"上章末尾"输入

---

## C. 产出 info_acquired

汇总所有读取和查询结果：

```yaml
info_acquired:
  settings_read:           # A部分：强制读取
    - path: "..."
      status: full
      size: 2048
      key_points: [...]
  library_refs:             # B2部分：library查询
    - source: "套路库/反杀套路.md"
      relevance: "本章废弃厂房双杀参考"
  research_results:         # B3部分：pop-research结果
    - query: "..."
      result_summary: "..."
  prev_chapter_tail:        # B4部分：上章末尾
    chapter: 2
    text: "（上章末尾500-800字原文）"
  additional_refs:          # B1部分：额外参考
    - path: "写作参考/知识沉淀/..."
      relevance: "..."
```

---

## D. 完成条件

- [x] settings_ref 全部强制读取完毕（status=full）
- [x] 写作参考索引已查询
- [x] library查询已完成（按需）
- [x] pop-research已完成（如需）
- [x] 上章末尾已提取
- [x] info_acquired 已汇总
- [x] 自动进入 Step3（子agent创作）
