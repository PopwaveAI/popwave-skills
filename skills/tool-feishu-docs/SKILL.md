---
name: tool-feishu-docs
description: 当用户说"创建飞书文档""编辑文档""添加评论""回复评论""创建文件夹""设置权限""导入 Markdown""搜索文档""管理多维表格""操作文档 block"时启用。通过 Open API 对飞书云文档进行增删改查、评论管理、文件夹管理、权限设置、多维表格操作和 Markdown 导入。
allowed-tools: RunCommand(python:*), Write(*), Read(*)
version: 2.1.0
pipeline:
  upstream: []
  downstream: []
---
# Feishu Docs API Integration v2.1.0

> **定位：** 飞书云文档全操作工具箱。文档 CRUD、评论管理、文件夹管理、权限设置、多维表格操作、Markdown 导入。
> **前置：** 工作目录中必须放置 `feishu_token.py`（自动获取 Token）。

## 速查表

详见 [steps/00-quick-ref.md](steps/00-quick-ref.md)

| 操作类别 | 端点 | 所需权限 | User Token |
|:---------|:-----|:---------|:-----------|
| 文档 CRUD | `docx/v1/documents` | docx:document | 否 |
| Block 操作 | `docx/v1/documents/{id}/blocks` | docx:document | 否 |
| 评论 | `drive/v1/files/{id}/comments` | drive:drive | 是 |
| 文件夹 | `drive/v1/files` | drive:drive | 是 |
| 权限 | `drive/v1/permissions` | drive:drive | 是 |
| Bitable | `bitable/v1/apps/{token}/tables` | bitable:app | 否 |
| Markdown 导入 | `drive/v1/import_tasks` | docs:document:import | 是 |

## 红线

| # | 红线 | 说明 |
|:-:|:-----|:------|
| 1 | Token 文件必须存在 | `feishu_token.py` 不存在 → 退回 |
| 2 | 评论 API 用 `drive/v1` 路径 | 不能用 `docx/v1`；必须传 `?file_type=docx` |
| 3 | Bitable token 按 `_tbl` 拆分 | `appToken_tblTableId` → `app_token` + `table_id` |
| 4 | 评论 body 必须嵌套结构 | `reply_list.replies[].content.elements[]` 不可简写 |
| 5 | 删除文档走 `drive/v1/files` | 不是 `docx/v1` |
| 6 | User 操作需 User Token | 评论/文件夹/权限/导入需 User Token；Tenant Token → 退回 |
| 7 | Markdown 导入需轮询 | import 后必须 GET ticket 直到完成 |
| 8 | 权限变更需发布新版本 | 启用 scope 后不发布 → 不生效 |

## Drop Check

| # | 检查项 | 触发条件 | 动作 |
|:-:|:-------|:---------|:-----|
| D1 | Token 未初始化 | `feishu_token.py` 不存在 | 退回要求放置 token 文件 |
| D2 | User 操作混用 Tenant Token | 权限错误 99991672/99991679 | 提示切换到 User 模式 |
| D3 | 知识库文档用 doc API | 评论返回 1069307 | 切换到 Wiki API 解析 token |
| D4 | 导入未轮询 | import 后未 GET ticket | 补轮询直到状态完成 |
| D5 | 删除后继续操作 | API 返回 404 | 停止，通知用户文档已删除 |

## 核心流程

> 按以下顺序执行 Step 文件。

| Step | 文件 | 说明 |
|:-----|:-----|:-----|
| 1 | [steps/01-token.md](steps/01-token.md) | 初始化 Token（Tenant/User 双模式） |
| 2 | [steps/02-doc-crud.md](steps/02-doc-crud.md) | 文档 CRUD + Block 操作 |
| 3 | [steps/03-comments.md](steps/03-comments.md) | 评论管理（需 User Token） |
| 4 | [steps/04-folders.md](steps/04-folders.md) | 文件夹管理（需 User Token） |
| 5 | [steps/05-permissions.md](steps/05-permissions.md) | 权限管理（需 User Token） |
| 6 | [steps/06-bitable.md](steps/06-bitable.md) | 多维表格操作 |
| 7 | [steps/07-markdown-import.md](steps/07-markdown-import.md) | Markdown 导入（需 User Token） |

## WRONG 示例

| # | 错误 | 正确 |
|:-:|:-----|:-----|
| W1 | 评论 API 用 `docx/v1` | 评论在 `drive/v1`：`POST drive/v1/files/{id}/comments?file_type=docx` |
| W2 | Bitable token 不拆分直接用 | 按 `_tbl` 拆分为 `app_token` + `table_id` |
| W3 | Block type 号用错 | 段落=2，引用=15。查 type 表确认 |
| W4 | 评论 body `{"content": "X"}` | 必须用 `reply_list.replies[].content.elements[]` 嵌套 |
| W5 | 删除文档用 `docx/v1` | 走 `drive/v1/files/{id}?type=docx` |
| W6 | Tenant Token 操作权限 | 评论/文件夹/权限需 User Token（drive:drive） |

## 异常与边界条件

| 场景 | 处理 |
|:-----|:-----|
| Token 过期（99991679） | 自动刷新；User Token 需重新 OAuth |
| 权限不足（99991672） | 启用 scope → 发布新版本 |
| Block 参数错误（1770001） | 核对 block_type；文本 block 必含 `style: {}` |
| refresh_token 被消耗（20038） | 重新运行 `first_time_setup.py` |
| 评论 file not found（1069307） | 知识库文档需 Wiki API 解析 token |
| OAuth 缺 app_token（20014） | 请求头始终传递 `app_access_token` |
| 导入格式不支持 | 仅支持 `.md`、`.html` 等 |
| Bitable token 无法拆分 | 检查是否含 `_tbl` 分隔符 |
| 调用已废弃 API（95054） | 用 `docx/v1` 替代 `doc/v2` |
| 批量删除 index 错误 | 确认 start_index < end_index |

## 落盘检查点

| 检查点 | 确认项 | 确认 |
|:-------|:-------|:-----|
| Token 初始化 | `feishu_token.py` 存在，`headers()` 可正常返回 | [ ] |
| Token 模式匹配 | 根据操作类型确认 Tenant/User 模式 | [ ] |
| Doc CRUD 响应 | API 返回 200，`data` 正确 | [ ] |
| Block type 正确 | `block_type` 与期望格式一致 | [ ] |
| 评论含 file_type=docx | 所有评论 API 请求含 `?file_type=docx` | [ ] |
| Markdown 导入完成 | 轮询结果显示 success | [ ] |
| Bitable token 拆分 | `app_token` 和 `table_id` 均有效 | [ ] |

## 黄金规则

1. **权限变更 → 创建并发布新版本**：启用 scope 后必须发布新版本才生效
2. **评论 API → 始终传 `file_type=docx`**：作为 query 参数，不是 body
3. **Bitable token → 按 `_tbl` 拆分**：分成 `app_token` + `table_id`
4. **评论创建 body → 使用 `reply_list.replies[].content.elements[]` 嵌套结构**
5. **删除文件 → 走 `drive/v1/files`**，不是 `docx/v1`
