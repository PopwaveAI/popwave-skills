# Step 4: 文件夹管理 SOP

> **需要 User Token（drive:drive）。**

```python
# 创建文件夹（"" = 根目录）
r = requests.post(
    f"{BASE}/open-apis/drive/v1/files/create_folder",
    headers=H, json={
        "name": "文件夹名称",
        "folder_token": ""  # 或父文件夹 token
    })

# 列出文件夹内容
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files/{folder_token}/children",
    headers=H)
```
