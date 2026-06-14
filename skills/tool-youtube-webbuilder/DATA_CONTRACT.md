# tool-youtube-webbuilder · 数据字段参考

> **此文档仅供参考。** agent 创作时可参考下面的字段结构来读取 `data.json`。
>
> 不再作为「模板注入契约」——因为 v3 已废弃模板注入。
>
> 所有数据由 `fetch_youtube.py` 产出，结构稳定（只要不改抓取脚本就不会变）。

---

## data.json 顶层结构

```json
{
  "channel":    { /* 频道信息（见下） */ },
  "videos":     [ /* 视频列表（最多 12 个） */ ],
  "fetchedAt":  "2026-05-29T12:00:00+00:00",
  "totalVideos": 12
}
```

### 频道信息 (`channel`)

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `title` | string | 频道名称 |
| `description` | string | 频道描述（完整） |
| `customUrl` | string | `@handle` |
| `publishedAt` | string | ISO 创建时间 |
| `country` | string | 国家代码 |
| `thumbnails` | object | `{ default/medium/high: { url, width, height } }` |
| `bannerUrl` | string | 频道 Banner URL，可用作 Hero 背景 |
| `statistics.viewCount` | string | 格式化播放量（如 "14.3亿"） |
| `statistics.subscriberCount` | string | 格式化订阅数（如 "142.0万"） |
| `statistics.videoCount` | string | 格式化视频数（如 "1,931"） |
| `statistics.raw*` | int | 原始数字，适合运算和可视化 |
| `socialLinks` | array | `[{ platform, url, label }]` |

### 视频列表 (`videos[]`)

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `id` | string | YouTube 视频 ID |
| `title` | string | 视频标题 |
| `description` | string | 简介（前200字） |
| `publishedAt` | string | ISO 发布时间 |
| `thumbnails` | object | `{ default/medium/high/standard/maxres: { url, width, height } }` |
| `duration` | string | 格式化时长（如 "15:30"） |
| `statistics.viewCount` | string | 格式化播放量 |
| `statistics.likeCount` | string | 格式化点赞数 |
| `statistics.commentCount` | string | 格式化评论数 |
| `timeAgo` | string | 相对时间（如 "2天前"） |
| `url` | string | `https://www.youtube.com/watch?v={id}` |

---

## analysis_ready.json 结构

由 `analyze.py` 产出，包含语言/标签/频道画像等分析结论。

| 字段 | 说明 |
|:-----|:-----|
| `channel_analysis.language` | `chinese` / `english` / `bilingual` |
| `channel_analysis.tags` | 内容赛道标签数组 |
| `channel_analysis.subscriber_count` | 原始订阅数（int） |
| `channel_analysis.video_count` | 原始视频数（int） |
| `channel_analysis.view_count` | 原始总播放量（int） |
| `channel_analysis.channel_description` | 频道描述前500字 |
| `video_analysis.total_videos` | 视频总数 |
| `video_analysis.titles` | 所有视频标题 |
| `video_analysis.descriptions` | 前6个视频的简介摘要 |

---

## 缩略图选择策略

agent 创作时，建议按以下优先级选择缩略图：

**频道头像**：`thumbnails.high` > `thumbnails.medium` > `thumbnails.default`
**视频缩略图**：`thumbnails.maxres` > `thumbnails.high` > `thumbnails.medium` > `thumbnails.default`
**Hero 背景**：`bannerUrl`（如果没有，用频道的 `high` 头像）
