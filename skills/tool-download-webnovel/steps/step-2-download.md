# Step 2：直链下载/导入并转码

> **读什么：** Step 1 的 `source` 与 `title`。
> **产出什么：** UTF-8 TXT 文件。

## 推荐命令

从仓库根目录运行：

```powershell
python skills\tool-download-webnovel\scripts\download_text.py "SOURCE" --title "书名"
```

指定输出目录：

```powershell
python skills\tool-download-webnovel\scripts\download_text.py "SOURCE" --title "书名" --output-dir "D:\popwave-skills\downloads"
```

短篇/样章可降低阈值：

```powershell
python skills\tool-download-webnovel\scripts\download_text.py "SOURCE" --title "书名" --min-bytes 2048
```

## 脚本会做什么

- 下载 http(s) URL，或复制本地文件。
- 如来源是 `.zip`，提取其中最大的 `.txt/.md`。
- 尝试识别 `utf-8-sig/utf-8/gb18030/gbk/big5`。
- 统一保存为 UTF-8。
- 拦截 HTML、错误页、网盘页、过小文件。

## 门禁

| 检查项 | 失败动作 |
|:-------|:---------|
| 脚本退出码为 0 | 进入 Step 3 |
| 脚本退出码为 2 | 读取错误信息，说明文件疑似无效 |
| 下载失败 | 请用户换授权来源 |
| RAR/7z | 请用户解压后提供 TXT 或 ZIP |

## 输出

脚本输出中读取：

- `output=...`
- `encoding=...`
- `bytes=...`
- `preview=...`
