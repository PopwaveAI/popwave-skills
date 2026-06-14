# Step 7：Critique R1（事实安全拦截） — SOP

## 第一步：优先排查

| 排查项 | 说明 |
|:-------|:-----|
| `critical_bug` | 事实错误、时间/产品/版本/价格/品牌归属 |
| `factual_risk` | 来源缺失、猜测写成事实 |
| `logic_break` | 前后矛盾、步骤不可执行、结论与论据不匹配 |
| 合规风险 | 公开资料伪装成亲测、过度承诺 |
| 结构缺陷 | 核心问题未回答、段落缺失 |

**❌ 门禁：** `critical_bug` 存在 → 必须修复后方可进入下一轮。

## 第二步：输出

```markdown
- critical_bug: [必须修复]
- factual_risk: [事实风险]
- logic_break: [逻辑断裂]
- keep: [应保留的强项]
```
