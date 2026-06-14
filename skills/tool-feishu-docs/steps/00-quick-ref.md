# 速查表

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
