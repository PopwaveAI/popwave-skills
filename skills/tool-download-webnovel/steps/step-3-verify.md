# Step 3：验证并交付

> **读什么：** Step 2 的脚本输出和保存文件。
> **产出什么：** 可交给 `pop-decon` 的 TXT 路径，或阻塞原因。

## 验证项

| 检查项 | 标准 |
|:-------|:-----|
| 文件存在 | `output` 路径存在 |
| 文件大小 | 默认 ≥ 100KB；短篇/样章需用户确认 |
| 编码 | 最终文件为 UTF-8 |
| 内容 | 非 HTML、非错误页、非网盘提示页 |
| 预览 | 前 100-120 字可读 |

## 可选人工复查命令

```powershell
Get-Item "D:\popwave-skills\downloads\书名.txt"
Get-Content "D:\popwave-skills\downloads\书名.txt" -Encoding UTF8 -TotalCount 20
```

## 交付格式

不要粘贴全文。只回复：

```text
已导入：D:\popwave-skills\downloads\书名.txt
大小：{N} MB
原编码：{encoding}
预览：{preview}
状态：可交给 pop-decon
```

## 失败格式

```text
未能导入：{原因}
建议：请提供授权 TXT/ZIP 直链，或先手动下载后把本地文件路径发给我。
```
