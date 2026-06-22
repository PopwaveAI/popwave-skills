---
name: tool-download-webnovel
description: 当用户提供授权的网文/小说 TXT/ZIP 直链、本地文本文件，或要求“直链下载/导入/转码/校验小说 TXT 供 pop-decon 使用”时启用。主路径是直链下载；只处理用户有权使用的来源，不绕过登录/付费/提取码/反爬限制，不逐章抓取受保护网站。
---

# tool-download-webnovel · 授权直链下载与校验

> **定位：** 走“直链下载 → 转 UTF-8 → 校验 → 交付路径”的单线流程，把授权文本来源处理成可被 `pop-decon` 消费的 TXT。
> **核心边界：** 可以下载用户提供或明确授权的 TXT/ZIP 直链；不把盗版站、侵权转载站设为优先来源，不绕过访问控制，不逐章抓取受保护内容。

## 速查表

| 场景 | 动作 | 输出 |
|:-----|:-----|:-----|
| 用户给 http(s) TXT/ZIP 直链 | 直接下载、解压、转码、校验 | `D:\popwave-skills\downloads\{书名}.txt` |
| 用户给本地 TXT/ZIP 文件 | 用脚本复制/解压、转码、校验 | `D:\popwave-skills\downloads\{书名}.txt` |
| 用户只给书名 | 可建议合法来源类型；不要以盗版/侵权站为目标检索 | 无文件 |
| 网盘需登录/提取码/人工下载 | 不绕过；请用户手动下载后提供本地文件 | 无文件或等待用户文件 |

## 质量红线

| 红线 | 处理 |
|:-----|:-----|
| 以盗版站、侵权转载站为优先来源 | 禁止；改为要求授权直链或本地文件 |
| 绕过登录、付费、提取码、反爬、DRM | 禁止；请用户手动处理 |
| 逐章抓取受保护小说站 | 禁止；不做爬虫 |
| 下载后粘贴全文 | 禁止；只给路径、大小、编码、短预览 |
| 未验证就交付 | 禁止；必须检查大小、编码、HTML/错误页、可读性 |

## 执行流程

### Step 1：确认来源

读 `steps/step-1-source.md`。

**必须确认：**
- 用户提供的是授权直链 URL 或本地文件。
- 来源可以直接下载/复制，不需要登录、破解、绕过限制。
- 书名或输出文件名明确。

### Step 2：下载/导入并转码

读 `steps/step-2-download.md`。

优先用脚本：

```powershell
python skills\tool-download-webnovel\scripts\download_text.py "SOURCE" --title "书名"
```

可选参数：

```powershell
--output-dir "D:\popwave-skills\downloads"
--min-bytes 102400
```

### Step 3：验证并交付

读 `steps/step-3-verify.md`。

最终只回复：
- 保存路径
- 文件大小
- 检测到的原编码
- 前 100-120 字预览
- 是否可交给 `pop-decon`

## 异常处理

| 情况 | 动作 |
|:-----|:-----|
| 只有书名没有来源 | 说明需要授权直链/本地文件，不以盗版站为目标检索 |
| URL 下载到 HTML/404/网盘页 | 标记失败，不保存为最终 TXT |
| 文件小于阈值 | 标记可能不完整；如是短篇/样章，用户确认后可降低 `--min-bytes` |
| 编码不是 UTF-8 | 脚本自动尝试 `utf-8/gb18030/gbk/big5` 并保存 UTF-8 |
| ZIP 内多文本 | 默认取最大 `.txt/.md`；如不对，请用户指定文件 |
| RAR/7z | 不自动处理；请用户解压后提供 TXT 或 ZIP |

## 文件职责

| 文件 | 用途 |
|:-----|:-----|
| `scripts/download_text.py` | 下载/复制授权来源，解压 ZIP，转 UTF-8，基础校验 |
| `steps/step-1-source.md` | 来源确认与版权边界 |
| `steps/step-2-download.md` | 下载/导入命令 |
| `steps/step-3-verify.md` | 交付前验证 |

## 版本

v3.0.1 | 2026-06-22 | 明确恢复“直链下载”为主路径，同时保留授权与反绕过边界 → [CHANGELOG.md](CHANGELOG.md)
