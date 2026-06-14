# Step 0: Token 初始化

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
