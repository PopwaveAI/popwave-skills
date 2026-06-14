# Step 3: 评论操作 SOP

> **注意：** 评论 API 在 `drive/v1`，不在 `docx/v1`。必须传 `?file_type=docx`。

**❌ 门禁：** 评论操作需要 User Token（drive:drive 权限）。只有 Tenant Token → 退回要求切换到 User 模式。

## 列出/查看评论

```python
# 列出所有评论
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments?file_type=docx&page_size=50",
    headers=H)

# 查看单条评论
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}?file_type=docx",
    headers=H)
```

## 创建评论

```python
r = requests.post(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments?file_type=docx",
    headers=H, json={
        "reply_list": {
            "replies": [{
                "content": {
                    "elements": [{
                        "type": "text_run",
                        "text_run": {"content": "评论内容"}
                    }]
                }
            }]
        }
    })
```

**@提及用户：** 在 elements 中加 `{"type": "person", "person": {"user_id": "ou_xxxx"}}`

## 回复/解决/删除评论

```python
# 回复
r = requests.post(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}/replies?file_type=docx",
    headers=H, json={
        "content": {
            "elements": [{"type": "text_run", "text_run": {"content": "回复内容"}}]
        }
    })

# 解决/重开
r = requests.patch(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}?file_type=docx",
    headers=H, json={"is_solved": True})  # False = 重开

# 删除
r = requests.delete(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}?file_type=docx",
    headers=H)
```
