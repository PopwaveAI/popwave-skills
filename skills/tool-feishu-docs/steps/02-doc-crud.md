# Step 2: 文档操作 SOP

## 创建文档

```python
r = requests.post(f"{BASE}/open-apis/docx/v1/documents", headers=H,
    json={"title": "文档标题"})
doc_id = r.json()["data"]["document"]["document_id"]
# URL: https://bytedance.feishu.cn/docx/{doc_id}
```

**产出：** `doc_id` + 文档访问 URL

## 读取文档

```python
# 基本信息
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{doc_id}", headers=H)

# 原始文本（纯文本，无格式）
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{doc_id}/raw_content", headers=H)

# 结构化 Block
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks", headers=H)
items = r.json()["data"]["items"]  # index 0 = page, 1..N = children
```

**读什么：** `items` 数组，每个 item 含 `block_type` + `block_id` 和类型专属数据

**❌ 门禁：** `doc_id` 必须有效（可通过 GET 验证）。无效 id → 退回要求确认文档链接。

## 追加/更新/删除 Block

**Block 类型参考：**

| block_type | JSON Key | 说明 |
|-----------|----------|------|
| 1 | page | 根节点（block_id = doc_id） |
| 2 | text | 普通段落 |
| 3 | heading1 | H1 |
| 4 | heading2 | H2 |
| 5 | heading3 | H3 |
| 12 | bullet | 无序列表 |
| 13 | ordered | 有序列表 |
| 15 | quote | 引用块 |
| 18 | bitable | 多维表格 |
| 22 | divider | 分割线 |
| 31 | table | 内联表格 |
| 32 | table_cell | 表格单元格 |

```python
# 追加（在末尾）
r = requests.post(
    f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
    headers=H, json={"children": [
        {"block_type": 2, "text": {"elements": [
            {"text_run": {"content": "Hello"}}], "style": {}}},
        {"block_type": 22, "divider": {}},
    ]})

# 追加到指定位置
# 加 "index": N（从0开始）

# 更新 Block
r = requests.patch(
    f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks/{block_id}",
    headers=H, json={"update_text_elements": {
        "elements": [{"text_run": {"content": "新文本"}}],
        "style": {}
    }})

# 批量删除（从 index 2 到 12）
r = requests.delete(
    f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children/batch_delete",
    headers=H, json={"start_index": 2, "end_index": 12})
```

## 删除文档

```python
r = requests.delete(f"{BASE}/open-apis/drive/v1/files/{doc_id}?type=docx", headers=H)
```
