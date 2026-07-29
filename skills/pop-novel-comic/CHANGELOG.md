# CHANGELOG

## v1.1.0 | 2026-07-29

### 修复（格式保真）
- **根因**：Seedream API 返回的 URL 资源实际为 JPEG（magic bytes `FF D8 FF`），但 `generate_storyboard.py` 以 `.png` 命名保存，导致扩展名与实际格式不符
- **现象**：浏览器做 MIME sniffing 能兼容显示，但 popwave webview（nosniff 模式）按扩展名校验 MIME，判定为图片损坏
- **修复**：新增 `ensure_png_format()` 函数，在图片下载后自动检测 magic bytes，若为 JPEG 内容则用 Pillow 转码为真 PNG
- **同步修复**：`pop-novel-visual/scripts/generate.py` 的 `download_file` 和 `save_base64_image` 两条路径（新增 `ensure_format_integrity()` 函数）
- **新增铁律5**：下载后格式保真

## v1.0.0 | 2026-07-29

### 新增
- 初始版本，基于 R15 测试验证的网文章节转漫画管线
- 2 步结构：Step 1 章节解构+分镜脚本+门禁A，Step 2 角色定妆+分镜生成+HTML组装
- 复用 pop-novel-visual 的 Seedream API 脚本（`scripts/generate.py`）和提示词指南（`references/seedream-prompt-guide.md`）
- 新增 `scripts/generate_storyboard.py` 批量分镜生成脚本
- 新增 `templates/comic-page.tpl.html` HTML 漫画页模板
- 新增 `references/storyboard-guide.md` 分镜脚本指南

### 验证数据（R15 测试）
- 9 次 API 调用（1 角色定妆 + 8 分镜），100% 成功率
- 单格画面质量 9/10，角色一致性 75%，风格统一 9/10
- 总耗时 ~3 分钟（串行），并行可压缩到 ~30 秒
