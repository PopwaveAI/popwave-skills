# Step4：receipt检查 — manifest vs receipt一致性 + 导演意图验证

> **执行者**：主会话
> **输入**：context manifest（Step3组装）+ create receipt + revise receipt + 导演意图
> **产出**：receipt一致性检查结果（通过/不通过 + 修复策略）
> **人工check**：无（自动进入Step5）
> **红线**：❌5 子agent失败降级时必须重读完整context+文风DNA完整加载+独立质检

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
```

---

## 1. 检查项总览

主会话收到子agent产出后，对照manifest和receipt逐项检查（6项）：

| # | 检查项 | 来源 | 通过条件 |
|:-:|:-------|:-----|:---------|
| 1 | 完整性 | create receipt + revise receipt | receipt.status=full 且 actual_read≈manifest.size |
| 2 | 关键元素 | create receipt | key_elements_confirmed覆盖所有声明元素 |
| 3 | 导演意图（create） | create receipt | three_questions全部confirmed=true |
| 4 | 设定文件读取 | create receipt | settings_ref全部status=full |
| 5 | 文风DNA（revise） | revise receipt | status=full 且 deviations=0（精确匹配） |
| 6 | 导演意图验证（revise） | revise receipt | 5项验证全部passed=true |

---

## 2. 逐项检查

### 2.1 完整性检查

对每个receipt中的每个item：

```yaml
检查逻辑:
  - manifest中声明的每个item，receipt中必须有对应记录
  - receipt.item.status 必须为 full
  - receipt.item.actual_read 必须 ≈ manifest.item.size（允许±10%误差）
  
通过条件: 所有item status=full 且 actual_read在合理范围
不通过: 任一item status=partial 或 actual_read严重偏离manifest.size
```

### 2.2 关键元素检查

```yaml
检查逻辑:
  - create receipt的key_elements_confirmed必须覆盖manifest中声明的所有关键元素
  - 必须包含: "导演意图三问全部回答"、"event_chain全部推进"、"chapter_hook已留"

通过条件: 所有声明元素均在key_elements_confirmed中
不通过: 缺少任一声明元素
```

### 2.3 导演意图（create）检查

```yaml
检查逻辑:
  - create receipt的three_questions_confirmed必须全部为true
  - info: true（读者必须知道的信息已传达）
  - pressure: true（压力必须推进到指定程度）
  - hook: true（章末留了指定钩子）

通过条件: 三问全部confirmed=true
不通过: 任一问confirmed=false
```

### 2.4 设定文件读取检查

```yaml
检查逻辑:
  - 导演意图的settings_ref列表中的每个指针
  - 对应的receipt item status必须为full
  - 读取路径必须与settings_ref指向的路径一致

通过条件: settings_ref全部status=full
不通过: 任一设定文件status=partial或缺失
```

### 2.5 文风DNA（revise）检查

```yaml
检查逻辑:
  - revise receipt的style_dna_match.status必须为full
  - style_dna_match.deviations必须为0（精确匹配，0误差）
  - 不允许"大致匹配"或"风格接近"

通过条件: status=full 且 deviations=0
不通过: status=partial 或 deviations>0
```

### 2.6 导演意图验证（revise）检查

```yaml
检查逻辑:
  - revise receipt的director_intent_verification中5项验证
  - 每项的passed必须为true:
    1. narrative_function已体现
    2. event_chain完整推进
    3. emotion_curve已遵循
    4. chapter_hook已留
    5. three_questions全部回答

通过条件: 5项验证全部passed=true
不通过: 任一项passed=false
```

---

## 3. 检查结果

```yaml
receipt_check_result:
  chapter: 3
  checks:
    - id: completeness
      status: pass         # pass / fail
      details: "6/6 items full, actual_read均在合理范围"
    - id: key_elements
      status: pass
      details: "所有声明元素已确认"
    - id: director_intent_create
      status: pass
      details: "三问全部confirmed=true"
    - id: settings_read
      status: pass
      details: "2/2 settings_ref status=full"
    - id: style_dna_revise
      status: pass
      details: "status=full, deviations=0"
    - id: director_intent_revise
      status: pass
      details: "5/5验证通过"
  overall: pass             # 全部pass=pass, 任一fail=fail
  degraded: false           # 是否使用了降级策略
```

---

## 4. 修复策略

### 4.1 单项不通过

某项检查不通过时：

1. 定位不通过的具体item
2. 重新调度对应子agent（create或revise），注入：
   - 原始context manifest
   - 不通过项的具体原因
   - 修复要求
3. 重新检查该单项

### 4.2 连续2次同一项不通过 → 降级策略B（红线5）

> ❌5 子agent失败降级时必须重读完整context+文风DNA完整加载+独立质检

1. 标注 `degraded_master_execution: true`
2. **重读完整context**：
   - 导演意图 + 状态快照 + 设定文件 + info_acquired + 文风DNA
   - 全部 `Get-Content -Raw` 完整加载
3. **文风DNA完整加载**：
   - `Get-Content -Encoding UTF8 -Raw` 读取 `写作资产/文风库/{书名}.md`
   - 确认完整加载（不限制行数）
4. **独立质检**：
   - 主会话直接执行create/revise
   - 完成后自检所有6项检查
5. 降级≠跳过门禁：receipt仍然必须产出，检查仍然必须通过

### 4.3 降级后仍不通过

- 暂停5步循环
- 向用户报告：连续降级仍无法通过检查
- 等待用户决策（修改导演意图 / 修改设定 / 手动介入）

---

## 5. 完成条件

- [x] 6项检查全部执行
- [x] 检查结果已记录（receipt_check_result）
- [x] 如有不通过项 → 修复策略已执行
- [x] overall=pass → 进入 Step5（活记忆更新+落盘）
- [x] degraded标注（如适用）
