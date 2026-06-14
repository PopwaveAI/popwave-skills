# Step 5: 权限管理 SOP

> **需要 User Token（drive:drive）。**

```python
# 查看协作者
r = requests.get(
    f"{BASE}/open-apis/drive/v1/permissions/{doc_id}/members?type=docx",
    headers=H)

# 设置分享链接
r = requests.patch(
    f"{BASE}/open-apis/drive/v1/permissions/{doc_id}/public",
    headers=H, json={
        "external_access_entity": "open",
        "security_entity": "anyone_can_view",           # anyone_can_view / anyone_can_edit / anyone_can_manage
        "link_share_entity": "tenant_readable",         # tenant_readable / anyone / closed
    })
```
