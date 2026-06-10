---
name: feishu-docs
description: Create, read, update, and delete Feishu (Lark) cloud documents, comments, bitable records, folders, and permissions via Open API. Invoke when user wants to create/edit docs, reply to comments, manage folders, set permissions, import Markdown, search files, or any Feishu office automation task. Triggers include "Feishu document", "飞书", "add a review", "reply to comment", "create a folder", "set permissions", "search my docs".
allowed-tools: RunCommand(python:*), Write(*), Read(*)
pipeline:
  upstream: []
  downstream: []
---

# Feishu Docs API Integration

Comprehensive skill for Feishu document operations 鈥?documents, comments, folders, permissions, bitable, tables, and Markdown import.

## Quick Start 鈥?One-Line Token

Place `feishu_token.py` in the working directory:

```python
from feishu_token import headers, get_token
H = headers()  # Auto-detect, auto-refresh, tenant/user dual mode
```

## Token Architecture

```
feishu_tokens.json 鈫愨攢鈹€ Persistent storage
    鈹溾攢鈹€ token_type           ("tenant" or "user")
    鈹溾攢鈹€ tenant_access_token  (tenant mode, no OAuth needed)
    鈹溾攢鈹€ user_access_token    (user mode, full permission)
    鈹溾攢鈹€ refresh_token        (user mode only, auto-cycled)
    鈹斺攢鈹€ updated_at
```

**Tenant mode**: Zero config. Works for app-created docs. No OAuth.
**User mode**: Browser OAuth once. Accesses all user's docs + comments + permissions.

`get_token()` auto-manages both modes: checks validity 鈫?refreshes if needed 鈫?saves back.

## Permissions Required

| Scope | Tenant | User | APIs Enabled |
|-------|--------|------|-------------|
| `docx:document` | 鉁?| 鉁?| Document CRUD, blocks |
| `docx:document:create` | 鉁?| 鉁?| Create documents |
| `bitable:app` | 鉁?| 鉁?| Bitable records |
| `drive:drive` | 鉂?| 鉁?| Comments write, folders, permissions, file search |
| `docs:document:import` | 鉂?| 鉁?| Markdown import |
| `offline_access` | N/A | 鉁?| refresh_token for long-term user access |

---

## 1. Document Operations (docx/v1)

All use: `H = headers()`, then `requests.{method}(f"{BASE}/path", headers=H, json=body)`

### Create Document
```python
r = requests.post(f"{BASE}/open-apis/docx/v1/documents", headers=H,
    json={"title": "Title"})
doc_id = r.json()["data"]["document"]["document_id"]
# URL: https://bytedance.feishu.cn/docx/{doc_id}
```

### Read Document Info
```python
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{doc_id}", headers=H)
title = r.json()["data"]["document"]["title"]
```

### Read Raw Content
```python
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{doc_id}/raw_content", headers=H)
text = r.json()["data"]["content"]
```

### Read Blocks (structured)
```python
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks", headers=H)
items = r.json()["data"]["items"]  # index 0 = page, 1..N = children
```

### Delete Document
```python
r = requests.delete(f\"{BASE}/open-apis/drive/v1/files/{doc_id}?type=docx\", headers=H)
```

---

## 2. Block Operations

### Block Type Reference (VERIFIED for docx/v1)

| block_type | JSON Key | Description |
|------------|----------|-------------|
| 1 | page | Root (block_id = doc_id) |
| 2 | text | Normal paragraph |
| 3 | heading1 | H1 |
| 4 | heading2 | H2 |
| 5 | heading3 | H3 |
| 12 | bullet | Bullet list |
| 13 | ordered | Numbered list |
| 15 | quote | Quote block |
| 18 | bitable | Multidimensional table |
| 22 | divider | Horizontal line |
| 31 | table | Inline table (use descendant API) |
| 32 | table_cell | Table cell (auto-created) |

### Append Blocks

```python
r = requests.post(
    f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
    headers=H, json={"children": [
        {"block_type": 2, "text": {"elements": [
            {"text_run": {"content": "text"}}], "style": {}}},
        {"block_type": 22, "divider": {}},
    ]})
# Add "index": N to insert at position
```

### Update a Block

```python
r = requests.patch(
    f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks/{block_id}",
    headers=H, json={"update_text_elements": {
        "elements": [{"text_run": {"content": "new text"}}],
        "style": {}
    }})
```

### Delete Blocks

```python
r = requests.delete(
    f"{BASE}/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children/batch_delete",
    headers=H, json={"start_index": 2, "end_index": 12})
```

### 馃毃 Error 1770001 (Invalid Param) 鈥?Common Causes

| Cause | Wrong | Right |
|-------|-------|-------|
| bullet type | `block_type: 9` | `block_type: 12` |
| ordered type | `block_type: 7` | `block_type: 13` |
| quote type | `block_type: 8` | `block_type: 15` |
| text type | `block_type: 1` | `block_type: 2` (1=page) |
| Missing style | no `"style"` field | `"style": {}` mandatory for text/heading/bullet/ordered/quote |
| text_run field | `"text":` | `"content":` |
| text style | `"style": {...}` | `"text_element_style": {...}` |

---

## 3. Comment Operations (drive/v1)

**CRITICAL**: Comment APIs live under `drive/v1`, not `docx/v1`. Always pass `file_type=docx` or `?file_type=docx` query param.

### List Comments (tenant + user token)

```python
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments?file_type=docx&page_size=50",
    headers=H)
items = r.json()["data"]["items"]
for c in items:
    print(c["comment_id"], c.get("is_solved"), c.get("reply_list", {}))
```

### Get a Single Comment

```python
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}?file_type=docx",
    headers=H)
```

### Create Comment (needs drive:drive + user token)

```python
r = requests.post(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments?file_type=docx",
    headers=H, json={
        "reply_list": {
            "replies": [{
                "content": {
                    "elements": [{
                        "type": "text_run",
                        "text_run": {"text": "comment text"}
                    }]
                }
            }]
        }
    })
comment_id = r.json()["data"]["comment_id"]
```

To @mention a user in a comment, add an element with `"type": "person"`:
```json
{"type": "person", "person": {"user_id": "ou_xxxx"}}
```

### Reply to a Comment

```python
r = requests.post(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}/replies?file_type=docx",
    headers=H, json={
        "content": {
            "elements": [{
                "type": "text_run",
                "text_run": {"text": "reply text"}
            }]
        }
    })
```

### Solve / Reopen a Comment

```python
r = requests.patch(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}?file_type=docx",
    headers=H, json={"is_solved": True})  # False to reopen
```

### Delete a Comment

```python
r = requests.delete(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}/comments/{comment_id}?file_type=docx",
    headers=H)
```

### Batch Query Comments

```python
r = requests.post(
    f"{BASE}/open-apis/drive/v1/files/comments/batch_query",
    headers=H, json={
        "file_tokens": [doc_id_1, doc_id_2],
        "file_type": "docx"
    })
```

---

## 4. Folder Management (drive/v1)

### Create Folder (needs drive:drive)

```python
r = requests.post(
    f"{BASE}/open-apis/drive/v1/files/create_folder",
    headers=H, json={
        "name": "Folder Name",
        "folder_token": ""  # "" = root; or parent folder token
    })
folder_token = r.json()["data"]["token"]
```

### List Files in a Folder

```python
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files/{folder_token}/children",
    headers=H)
```

### Search / List Files

```python
# List recent files, order by edit time DESC
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files?page_size=20&order_by=edited_time&direction=DESC",
    headers=H)
files = r.json()["data"]["files"]
```

### Get File Metadata

```python
r = requests.get(
    f"{BASE}/open-apis/drive/v1/files/{doc_id}?type=docx",
    headers=H)
# Returns: name, url, type, created_time, modified_time, owner
```

---

## 5. Permissions & Sharing

### Get Collaborators (needs drive:drive)

```python
r = requests.get(
    f"{BASE}/open-apis/drive/v1/permissions/{doc_id}/members?type=docx",
    headers=H)
members = r.json()["data"]["members"]
# Each: member_type, member_id, member_name, perm
```

### Set Link Sharing

```python
r = requests.patch(
    f"{BASE}/open-apis/drive/v1/permissions/{doc_id}/public",
    headers=H, json={
        "external_access_entity": "open",
        "security_entity": "anyone_can_view",
        "link_share_entity": "tenant_readable"  # org-wide
    })
```

`security_entity` values: `anyone_can_view`, `anyone_can_edit`, `anyone_can_manage`
`link_share_entity` values: `tenant_readable` (org), `anyone` (public), `closed`

---

## 6. Bitable (澶氱淮琛ㄦ牸)

### Embedded bitable in a doc

```python
# From doc blocks, find type=18
bt = [b for b in items if b["block_type"] == 18][0]
full_token = bt["bitable"]["token"]  # "appToken_tblTableId"
# Split token:
parts = full_token.split("_tbl")
app_token = parts[0]
table_id = "tbl" + parts[1]
```

### Create bitable block in doc (view_type=1, numeric)
```python
{"block_type": 18, "bitable": {"view_type": 1}}
```

### Read / Write Records

```python
# Fields
r = requests.get(
    f"{BASE}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
    headers=H)

# Add record
r = requests.post(
    f"{BASE}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records",
    headers=H, json={"fields": {
        "FieldName": "value",
        "PersonField": [{"id": "open_id"}]  # user field
    }})
```

---

## 7. Markdown Import (needs docs:document:import)

```python
import json, os

# Step 1: Upload media
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

# Step 2: Create import task
r = requests.post(f"{BASE}/open-apis/drive/v1/import_tasks",
    headers=H, json={
        "file_extension": "md",
        "file_token": file_token,
        "type": "docx",
        "file_name": "Imported Doc",
        "point": {"mount_type": 1, "mount_key": ""}
    })
ticket = r.json()["data"]["ticket"]

# Step 3: Poll result
r = requests.get(f"{BASE}/open-apis/drive/v1/import_tasks/{ticket}", headers=H)
```

---

## 8. Error Codes Reference

| Code | Meaning | Fix |
|------|---------|-----|
| 99991672 | Missing permission | Enable scope 鈫?publish new version |
| 99991679 | Token lacks scope | Re-OAuth with needed scopes |
| 20038 | refresh_token consumed | Re-run first_time_setup.py |
| 1770001 | Invalid block param | See block type table above |
| 99992402 | Field validation | Check body format against API doc |
| 1069307 | Comment API: file not found | For wiki docs, need wiki API to resolve token |
| 20014 | Missing app token in OAuth | Always pass app_access_token as Auth header |
| 95054 | Deprecated API | Use docx/v1 instead of doc/v2 |

**Golden rules**:
- Permission changes require **create & publish new version** in Feishu app console
- Comment APIs need `file_type=docx` query parameter
- Bitable full_token must be split on `_tbl` into app_token + table_id
- Comment create body uses nested `reply_list.replies[].content.elements[]`


