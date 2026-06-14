# Step 0: Backlog 检查 — SOP

## 第一步：判断主题是否已有近似文章

| 来源 | 检查方式 |
|:-----|:---------|
| Google Sheets | 读取内容库列表 |
| Airtable/Notion | 查询已有文章记录 |
| CMS 文章列表 | 读取发布清单 |
| 站内 URL 清单 | 搜索已有 URL |

## 第二步：输出决策

| 结果 | 行为 |
|:-----|:-----|
| `new_article` | 继续后续步骤 |
| `update_existing` | 切到旧文更新流程 |
| `needs_manual_decision` | 暂停，报告原因 |

**❌ 门禁：** 如果没有内容库数据 → 明确说明"未执行去重校验"。
