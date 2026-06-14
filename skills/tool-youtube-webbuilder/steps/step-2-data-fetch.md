# Step 2: 获取数据 — SOP

## 第一步：运行数据采集脚本

```powershell
# PowerShell 用户
cd 项目目录; $env:PYTHONIOENCODING='utf-8'; python scripts/run.py --channel-url "https://www.youtube.com/@handle"
```

**读什么：** 脚本自动从 YouTube API 抓取频道信息 + 前 12 个视频

## 第二步：验收产出

两个文件必须存在：

| 文件 | 内容 | 关键字段 |
|:-----|:-----|:---------|
| `data.json` | 频道信息+视频列表+统计数据 | `channel.title`, `channel.statistics`, `videos[].thumbnails.maxres` |
| `analysis_ready.json` | 频道分析摘要 | `channel_analysis.language`, `video_analysis.titles` |

**❌ 门禁：** `data.json` 缺失或为空 → 退回检查网络/API Key，重试。
