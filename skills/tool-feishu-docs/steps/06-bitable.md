# Step 6: 多维表格操作 SOP

## 从文档中提取 Bitable Token

```python
# 从 doc blocks 找到 block_type=18
bt = [b for b in items if b["block_type"] == 18][0]
full_token = bt["bitable"]["token"]  # "appToken_tblTableId"
parts = full_token.split("_tbl")
app_token = parts[0]
table_id = "tbl" + parts[1]
```

## 增删改记录

```python
# 读取字段
r = requests.get(
    f"{BASE}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
    headers=H)

# 添加记录
r = requests.post(
    f"{BASE}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records",
    headers=H, json={"fields": {
        "字段名": "值",
        "人员字段": [{"id": "open_id"}]
    }})
```
