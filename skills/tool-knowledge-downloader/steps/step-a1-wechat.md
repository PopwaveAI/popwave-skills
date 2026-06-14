# Phase A-1: 微信文章下载

## 前置依赖
必须运行 CDP Chrome Proxy（localhost:3456），Chrome 已登录微信公众平台。

## 第一步：确认输入

| 输入格式 | 示例 | 说明 |
|:---------|:-----|:-----|
| 单篇 URL | `https://mp.weixin.qq.com/s/xxxxx` | 1 篇 → 1 个 `.md` |
| 专辑 URL | `https://mp.weixin.qq.com/album/...` | 1 专辑 → N 篇 |
| 批量文件 | `urls.txt`（每行一个 URL） | 自动去重 |

**门禁：** URL 必须是 `mp.weixin.qq.com` 域名。非微信链接 → 退回。

## 第二步：执行下载

```powershell
# 单篇下载（含 OCR）
py scripts/downloader.py "https://mp.weixin.qq.com/s/xxxxx" -o ./articles

# 专辑下载
py scripts/downloader.py "专辑URL" --album -o ./articles

# 批量下载
py scripts/downloader.py --batch urls.txt -o ./articles

# 跳过 OCR
py scripts/downloader.py "URL" --no-ocr -o ./articles
```

## 第三步：验收

产出目录结构：
```
./articles/
├── {标题}.md              ← 原文（含正文）
├── images/                 ← 文章截图（可选）
└── 拆解文/（Phase B 后产生）
```

**门禁：** 检查 `.md` 是否有正文内容（`# 正文` 部分非空）。正文为空 → 重试或标记失败。
