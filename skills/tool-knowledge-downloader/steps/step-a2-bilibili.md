# Phase A-2: B站字幕获取

## 前置依赖
无（直连 API），AI 字幕需要 CDP Chrome Proxy（需 B站登录）。

## 第一步：确认输入

| 输入格式 | 示例 |
|:---------|:-----|
| BV 号 | `BV1GJ411x7sF` |
| 完整 URL | `https://www.bilibili.com/video/BV1GJ411x7sF` |
| 短链接 | `https://b23.tv/xxxxx` |

**门禁：** 无法提取 BV 号 → 退回，要求提供标准 B站视频链接。

## 第二步：执行获取

```powershell
# 单集获取
py scripts/bili_subtitle.py "https://www.bilibili.com/video/BV1GJ411x7sF" -o ./articles

# 批量获取
py scripts/bili_subtitle.py --batch urls.txt -o ./articles

# 仅输出 JSON
py scripts/bili_subtitle.py "BV1GJ411x7sF" --json-only

# 禁用 CDP fallback
py scripts/bili_subtitle.py "URL" --no-cdp
```

## 第三步：验收

```
./articles/原文/
├── {标题}_字幕原始数据.json    ← AI 清洗输入
```

**门禁：** 检查 `subtitle_body` 是否非空。空数组 → 标记为"无字幕视频"。

## 第四步（可选）：AI 清洗字幕

读取 `_字幕原始数据.json`，按 `subtitle-clean-prompt.md` 清洗规则：
1. 去掉时间戳
2. 合并碎片句子
3. 去除废话互动语
4. 按语义智能分段
5. 保留口语化风格

产出 `{标题}.md`（标准 frontmatter + 正文）。
