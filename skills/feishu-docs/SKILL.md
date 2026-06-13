---
name: feishu-docs
description: 当用户说"创建飞书文档""编辑文档""添加评论""回复评论""创建文件夹""设置权限""导入 Markdown""搜索文档""管理多维表格""操作文档 block"时启用。通过 Open API 对飞书云文档进行增删改查、评论管理、文件夹管理、权限设置、多维表格操作和 Markdown 导入。
allowed-tools: RunCommand(python:*), Write(*), Read(*)
pipeline:
  upstream: []
  downstream: []
---

# Feishu Docs API Integration v2.0.0

> **定位：** 飞书云文档全操作工具箱。文档 CRUD、评论管理、文件夹管理、权限设置、多维表格操作、Markdown 导入。
> **前置：** 工作目录中必须放置 `feishu_token.py`（自动获取 Token）。

---

## 速查表

| 操作 | 端点/API | 所需权限 | 是否需要 User Token |
|:-----|:---------|:---------|:-------------------|
| 创建文档 | POST `docx/v1/documents` | docx:document:create | 否 |
| 读取文档信息 | GET `docx/v1/documents/{id}` | docx:document | 否 |
| 读取原始内容 | GET `docx/v1/documents/{id}/raw_content` | docx:document | 否 |
| 读取结构化 Block | GET `docx/v1/documents/{id}/blocks` | docx:document | 否 |
| 追加 Block | POST `docx/v1/documents/{id}/blocks/{id}/children` | docx:document | 否 |
| 更新 Block | PATCH `docx/v1/documents/{id}/blocks/{bid}` | docx:document | 否 |
| 批量删除 Block | DELETE `docx/v1/documents/{id}/blocks/{id}/children/batch_delete` | docx:document | 否 |
| 删除文档 | DELETE `drive/v1/files/{id}?type=docx` | docx:document | 否 |
| 列出评论 | GET `drive/v1/files/{id}/comments?file_type=docx` | drive:drive | 是 |
| 创建评论 | POST `drive/v1/files/{id}/comments?file_type=docx` | drive:drive | 是 |
| 回复评论 | POST `drive/v1/files/{id}/comments/{cid}/replies?file_type=docx` | drive:drive | 是 |
| 解决/重开评论 | PATCH `drive/v1/files/{id}/comments/{cid}?file_type=docx` | drive:drive | 是 |
| 创建文件夹 | POST `drive/v1/files/create_folder` | drive:drive | 是 |
| 列出文件夹内容 | GET `drive/v1/files/{token}/children` | drive:drive | 是 |
| 搜索文件 | GET `drive/v1/files?page_size=20` | drive:drive | 是 |
| 获取文件元数据 | GET `drive/v1/files/{id}?type=docx` | drive:drive | 是 |
| 查看协作者 | GET `drive/v1/permissions/{id}/members?type=docx` | drive:drive | 是 |
| 设置分享链接 | PATCH `drive/v1/permissions/{id}/public` | drive:drive | 是 |
| 导入 Markdown | POST `drive/v1/import_tasks` | docs:document:import | 是 |
| 读取多维表格记录 | GET `bitable/v1/apps/{token}/tables/{tid}/records` | bitable:app | 否 |

---

## 第一步：初始化 Token

### 准备 Token 文件

在工作目录中创建/放置 `feishu_token.py`：

```python
from feishu_token import headers, get_token
H = headers()  # 自动检测、自动刷新、tenant/user 双模式
```

### Token 架构

```
feishu_tokens.json ←── 持久化存储
    ├── token_type           ("tenant" 或 "user")
    ├── tenant_access_token  (tenant 模式，无需 OAuth)
    ├── user_access_token    (user 模式，完整权限)
    ├── refresh_token        (user 模式，自动轮换)
    └── updated_at
```

| 模式 | 配置 | 能做什么 |
|:-----|:-----|:---------|
| Tenant | 零配置，开箱即用 | 应用创建的文档 CRUD、Bitable |
| User | 浏览器 OAuth 一次 | 全部操作（评论/文件夹/权限/导入/搜索） |

**❌ 门禁：** 检查 `feishu_token.py` 是否存在。不存在 → 退回要求提供。

---

## 第二步：文档操作 — SOP

### 创建文档

```python
r = requests.post(f"{BASE}/open-apis/docx/v1/documents", headers=H,
    json={"title": "文档标题"})
doc_id = r.json()["data"]["document"]["document_id"]
# URL: https://bytedance.feishu.cn/docx/{doc_id}
```

**产出：** `doc_id` + 文档访问 URL

### 读取文档

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

### 追加/更新/删除 Block

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

### 删除文档

```python
r = requests.delete(f"{BASE}/open-apis/drive/v1/files/{doc_id}?type=docx", headers=H)
```

---

## 第三步：评论操作 — SOP

> **注意：** 评论 API 在 `drive/v1`，不在 `docx/v1`。必须传 `?file_type=docx`。

**❌ 门禁：** 评论操作需要 User Token（drive:drive 权限）。只有 Tenant Token → 退回要求切换到 User 模式。

### 列出/查看评论

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

### 创建评论

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

### 回复/解决/删除评论

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

---

## 第四步：文件夹管理 — SOP

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

---

## 第五步：权限管理 — SOP

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

---

## 第六步：多维表格操作 — SOP

### 从文档中提取 Bitable Token

```python
# 从 doc blocks 找到 block_type=18
bt = [b for b in items if b["block_type"] == 18][0]
full_token = bt["bitable"]["token"]  # "appToken_tblTableId"
parts = full_token.split("_tbl")
app_token = parts[0]
table_id = "tbl" + parts[1]
```

### 增删改记录

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

---

## 第七步：Markdown 导入 — SOP

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

---

## WRONG 示例

### WRONG 1：评论 API 用了 docx/v1 路径

> ❌ `POST /open-apis/docx/v1/documents/{id}/comments`
> ✅ 评论 API 在 `drive/v1`：`POST /open-apis/drive/v1/files/{id}/comments?file_type=docx`

### WRONG 2：Bitable token 不拆分直接用

> ❌ `appToken_tblTableId` 直接当 app_token 使用
> ✅ 按 `_tbl` 拆分为：`app_token` = 前半部分，`table_id` = "tbl" + 后半部分

### WRONG 3：Block 类型号用错

> ❌ 段落用 `block_type: 1`（1 = page）、引用用 `block_type: 8`（8 不存在）
> ✅ 段落 = 2，引用 = 15。查看 type 表确认后再调用

### WRONG 4：评论创建 body 结构错误

> ❌ `{"content": "评论内容"}`（没有嵌套结构）
> ✅ 必须用 `reply_list.replies[].content.elements[].text_run.content` 嵌套结构

### WRONG 5：删除文档用了 docx/v1 删除

> ❌ `DELETE /open-apis/docx/v1/documents/{id}`
> ✅ 删除文档走 `drive/v1/files/{id}?type=docx`

### WRONG 6：Tenant Token 尝试操作权限

> ❌ Tenant Token 调用文件夹/评论/权限 API
> ✅ 这些需要 User Token（drive:drive）。检测到权限错误 → 提示切换到 User 模式

---

## 异常与边界条件表

| 场景 | 处理 |
|:-----|:-----|
| **Token 过期（99991679）** | 检查 `feishu_tokens.json`，自动刷新；User Token 需重新 OAuth |
| **权限不足（99991672）** | 在飞书开发者后台启用对应 scope → 发布新版本 |
| **Block 参数错误（1770001）** | 核对 block_type 编号表；确认文本 block 必须包含 `style: {}` |
| **refresh_token 被消耗（20038）** | 重新运行 `first_time_setup.py` 获取新 token |
| **评论 API：file not found（1069307）** | 知识库文档需用 Wiki API 解析 token，不能直接用 doc_id |
| **OAuth 缺少 app_token（20014）** | 请求头中始终传递 `app_access_token` 作为 Auth header |
| **导入文件格式不支持** | 仅支持 Markdown（`.md`）、HTML（`.html`）等指定格式 |
| **Bitable full_token 无法拆分** | 检查 token 格式是否包含 `_tbl` 分隔符 |
| **调用已废弃 API（95054）** | 使用 `docx/v1` 替代 `doc/v2` |
| **批量删除 start_index > end_index** | 确认 start_index < end_index；index 范围在 block 总数内 |

---

## 阶段边界越界检测

| 边界场景 | 检测条件 | 处理 |
|:---------|:---------|:-----|
| 未初始化 Token 直接操作 | `feishu_token.py` 不存在 | ❌ 退回要求放置 token 文件 |
| User 操作混用 Tenant Token | 权限错误（99991672/99991679） | ❌ 提示切换到 User 模式 |
| 知识库文档用 doc API | 评论返回 1069307 | ❌ 切换到 Wiki API 解析 token |
| 导入任务未轮询结果 | import 后未 GET 检查 ticket | ❌ 补轮询直到状态为"完成" |
| 删除文档后继续操作 | 后续 API 返回 404 | ❌ 停止，通知用户文档已删除 |

---

## 落盘检查点

| 检查点 | 确认项 | 确认 |
|:-------|:-------|:-----|
| Token 初始化 | `feishu_token.py` 存在，`headers()` 可正常返回 | [ ] |
| Token 模式匹配 | 根据操作类型确认使用 Tenant 还是 User 模式 | [ ] |
| Doc CRUD 响应 | API 返回 200，`data` 中包含正确结果 | [ ] |
| Block 操作用对类型号 | `block_type` 与期望格式一致 | [ ] |
| 评论操作含 file_type=docx | 所有评论 API 请求包含 `?file_type=docx` | [ ] |
| Markdown 导入完成 | 轮询结果显示导入状态为 success | [ ] |
| Bitable token 正确拆分 | `app_token` 和 `table_id` 均有效 | [ ] |

---

## 黄金规则

1. **权限变更 → 创建并发布新版本**：在飞书开发者后台启用 scope 后，必须发布新版本才生效
2. **评论 API → 始终传 `file_type=docx`**：作为 query 参数，不是 body
3. **Bitable token → 按 `_tbl` 拆分**：分成 `app_token` + `table_id`
4. **评论创建 body → 使用 `reply_list.replies[].content.elements[]` 嵌套结构**
5. **删除文件 → 走 `drive/v1/files`**，不是 `docx/v1`

---

## 版本

v2.0.0 | 当前稳定版本。完整覆盖文档 CRUD、评论、文件夹、权限、Bitable、Markdown 导入。
