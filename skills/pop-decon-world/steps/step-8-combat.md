# Step 8：数值体系

**数据来源**：`world-data.json#class.entries[]` + 角色卡等级路径

**归纳逻辑**：
- 段位映射必须来自原文面板数据（如 ch2 "10级平民/1级盗贼【一阶】"、ch17 "5级盗贼【二阶】"）
- 每项末尾加 `# @chXX` 标注原文出处
- 包含段位名、攻击范围、突破条件、战斗角色、弱点、标志性画面锚点

**产出**：按 `templates/combat-capability.tpl.yaml` 填写 → `combat_capability.yaml`
