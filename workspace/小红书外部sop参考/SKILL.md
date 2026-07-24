---
name: "xhs-video-to-text"
description: "从小红书视频笔记批量提取全部文案信息，支持并发处理和简体中文输出。当用户提供小红书视频链接并需要提取视频中的文字内容时调用此skill。"
---

# 小红书视频转文案（并发版）

## 功能

从小红书视频笔记中批量提取全部文案信息，包括：
1. 帖子标题、描述、标签（从页面 `__INITIAL_STATE__` 提取）
2. 视频中的语音内容（下载视频 → 提取音频 → faster-whisper 语音转文字）
3. 自动繁转简（opencc t2s），输出简体中文文档

## 适用场景

- 用户提供单条小红书视频链接，需要提取文案
- 用户需要批量提取某作者的多篇视频笔记内容
- 用户需要处理合集/系列视频

## 前置条件

- 浏览器MCP工具可用（integrated_browser）
- ffmpeg 已安装（音频提取）
- Python 环境：`pip install faster-whisper opencc-python-reimplemented`
- 网络可访问 hf-mirror.com（whisper 模型下载镜像）

## SOP 步骤

### Step 1: 获取视频URL

**方式A：用户直接提供笔记链接（含 xsec_token）**

1. `browser_navigate` 访问 `https://www.xiaohongshu.com/explore/{noteId}?xsec_token={token}&xsec_source=pc_user`
2. `browser_evaluate` 执行JS提取数据：

```javascript
var state = window.__INITIAL_STATE__;
var key = Object.keys(state.note.noteDetailMap)[0];
var n = state.note.noteDetailMap[key].note;
return JSON.stringify({
  title: n.title,
  desc: n.desc,
  duration: n.video.capa.duration,
  videoUrl: n.video.media.stream.h264[0].masterUrl,
  noteId: n.noteId
});
```

**方式B：从作者主页批量获取**

1. `browser_navigate` 访问作者主页 `https://www.xiaohongshu.com/user/profile/{userId}?xsec_token={token}`
2. `browser_snapshot` 获取页面结构，找到笔记卡片的 element ref
3. `browser_scroll`（scrollIntoView: true）确保目标卡片在视口内
4. `browser_click` 逐个点击笔记卡片（**不要用JS `.click()`，Vue Router 不响应**）
5. 每个笔记页面执行上述JS提取视频URL
6. 提取完成后 `browser_navigate_back` 回到主页继续下一个

**方式C：用户分别提供每条链接**

用户可在聊天中直接粘贴多条小红书链接（含 xsec_token），逐条访问提取即可。

### Step 2: 并发下载+转写+繁转简（一体化脚本）

将所有视频元数据传入脚本，使用 `ProcessPoolExecutor` 并发处理。每个 worker 独立完成：下载视频 → 提取音频 → 加载模型 → 转写 → opencc 繁转简 → 保存。

```python
import os, sys, json, subprocess, urllib.request
from concurrent.futures import ProcessPoolExecutor, as_completed

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

WORK_DIR = r"C:\path\to\work_dir"  # 临时工作目录
OUTPUT_DIR = r"D:\path\to\output"   # 最终输出目录

videos = [
    {"id": "01", "title": "视频标题", "url": "http://...", "note_id": "xxx"},
    {"id": "02", "title": "视频标题", "url": "http://...", "note_id": "xxx"},
    # ...
]

def process_video(video):
    vid = video["id"]
    title = video["title"]
    url = video["url"]
    vpath = os.path.join(WORK_DIR, f"v_{vid}.mp4")
    apath = os.path.join(WORK_DIR, f"a_{vid}.m4a")

    # 1. 下载视频
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(vpath, 'wb') as f:
            while True:
                chunk = resp.read(8192)
                if not chunk: break
                f.write(chunk)

    # 2. 提取音频（m4a，非wav）
    subprocess.run(
        ["ffmpeg", "-i", vpath, "-map", "0:a", "-c", "copy", "-f", "mp4", apath, "-y"],
        capture_output=True, timeout=60
    )

    # 3. 语音转文字（每个进程独立加载模型）
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        apath, language="zh", beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )
    seg_list = [{"start": s.start, "end": s.end, "text": s.text} for s in segments]

    # 4. 繁转简
    from opencc import OpenCC
    cc = OpenCC('t2s')
    for seg in seg_list:
        seg["text"] = cc.convert(seg["text"])
    title_s = cc.convert(title)
    desc_s = cc.convert(video.get("desc", ""))

    # 5. 保存为Markdown
    os.makedirs(os.path.join(OUTPUT_DIR, "原始转写"), exist_ok=True)
    outpath = os.path.join(OUTPUT_DIR, "原始转写", f"{vid}_{title_s}_原始转写.md")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(f"# {title_s}\n\n")
        f.write(f"> 帖子描述：{desc_s}\n\n")
        f.write(f"> 转写工具：faster-whisper (small, CPU, int8) | 繁转简：opencc t2s\n\n---\n\n")
        for seg in seg_list:
            f.write(f"[{seg['start']:.1f}s-{seg['end']:.1f}s] {seg['text']}\n\n")

    # 6. 清理临时文件
    for p in [vpath, apath]:
        if os.path.exists(p): os.remove(p)

    return f"[{title_s}] Done: {len(seg_list)} segments"

if __name__ == "__main__":
    print(f"Starting {len(videos)} concurrent workers...")
    with ProcessPoolExecutor(max_workers=min(3, len(videos))) as executor:
        futures = {executor.submit(process_video, v): v for v in videos}
        for future in as_completed(futures):
            print(future.result())
    print("All done!")
```

> **并发数建议**：CPU核心数的一半或3，取较小值。每进程约占用1GB内存。

### Step 3: 输出文档结构

```
目标文件夹/
├── 原始转写/
│   ├── 01_标题_原始转写.md      # 1:1转写+繁转简，含时间戳
│   ├── 02_标题_原始转写.md
│   └── ...
├── 加工SOP/
│   ├── 01_标题_加工整理.md      # AI加工：纠错+分段+结构化
│   └── 总SOP.md                 # 跨视频主题汇总
└── SKILL.md
```

## 关键注意事项

### xsec_token 机制
- 每篇笔记有独立的 xsec_token，**不能跨笔记复用**
- 获取方式：从作者主页 `browser_click` 笔记卡片，浏览器自动生成带 token 的 URL
- **JS `.click()` 无效**（Vue Router 不响应），必须用 `browser_click` 工具
- 合集页面的笔记ID无法直接获取 xsec_token，需从作者主页逐个点击

### 视频URL时效性
- 视频URL含 `sign` 和 `t` 参数，有时效性
- 提取后需尽快下载，建议在同一批处理脚本中完成

### 音频提取
- 使用 m4a 格式（`-f mp4`），**不要用 wav**（精简版 ffmpeg 不支持）
- faster-whisper 支持直接读取 m4a

### 模型配置
- HF 镜像：`HF_ENDPOINT=https://hf-mirror.com`
- 禁用 xet：`HF_HUB_DISABLE_XET=1`（避免下载失败）
- small 模型对中文准确率约90%，常见误识别：弧光→湖光、章纲→张刚

### 并发处理
- `ProcessPoolExecutor`（非 ThreadPoolExecutor，因 faster-whisper 有 C 扩展 GIL 释放问题）
- 每个进程独立加载 WhisperModel（不可跨进程共享）
- 临时文件（视频/音频）在转写完成后自动清理

### 繁转简
- 使用 `opencc-python-reimplemented` 的 `OpenCC('t2s')` 配置
- 在转写完成后对每个 segment text 和 title/desc 统一转换
- 转换在 worker 进程内完成，避免主进程串行瓶颈

### 合集限制
- 小红书合集页面（`/collection/item/{id}`）的笔记列表**不含 xsec_token**
- 直接访问 `/explore/{id}?xsec_source=pc_collection` 会返回 404（error_code=300031）
- 合集笔记点击后跳转 `/discovery/item/{id}` 页面空白
- **解决方案**：从作者主页找到对应笔记点击进入，或请用户直接提供每条笔记的分享链接
