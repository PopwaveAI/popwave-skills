# Step 7: Markdown 导入 SOP

> **需要 User Token（docs:document:import）。**

```python
# Step 1: 上传文件
with open("file.md", "rb") as f:
    r = requests.post(f"{BASE}/open-apis/drive/v1/medias/upload_all",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "file_name": "file.md",
            "parent_type": "ccm_import_open",
            "size": str(os.path.getsize("file.md")),
            "extra": json.dumps({"obj_type": "docx", "file_extension": "md"})
        }, files={"file": f})
    file_token = r.json()["data"]["file_token"]

# Step 2: 创建导入任务
r = requests.post(f"{BASE}/open-apis/drive/v1/import_tasks",
    headers=H, json={
        "file_extension": "md",
        "file_token": file_token,
        "type": "docx",
        "file_name": "导入的文档",
        "point": {"mount_type": 1, "mount_key": ""}
    })

# Step 3: 轮询结果
ticket = r.json()["data"]["ticket"]
r = requests.get(f"{BASE}/open-apis/drive/v1/import_tasks/{ticket}", headers=H)
```

**❌ 门禁：** Markdown import 需要 `docs:document:import` 权限 + User Token。缺少任一 → 退回切换模式。
