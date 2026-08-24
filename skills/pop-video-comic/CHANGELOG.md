# CHANGELOG

## v1.0.0 — 2026-08-24

### steps 5件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step0-collect / step1-understand / step2-script / step3-tts / step4-render 五件全合入 SKILL.md 对应 SOP 步骤节
- **执行模式明确**：Step 0/1（素材收集+读图理解）为只读分析，可派子agent执行并回报、主agent落盘；Step 2 脚本确认闸门起（需老板多轮交互"先脚本后出片"）及 Step 3/4 配音合成，主agent直执
- **内容精炼**：各 step 的流程细节/完成判定/输出格式/脚本命令（tts_generate.py、render_video.py 调用方式、Ken Burns 规则、时长清单.json 结构）全合入 SOP 步骤节；速查表去除 steps/ 引用行
- skill.json version 0.2.0→1.0.0

## v0.2.0 | 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v0.2.0。

## v0.1.0 | 2026-08-06

首版发布：漫画转 PPT 放映式短视频 skill。

### 新增
- 五步管线：Step 0 收集 → Step 1 读图理解 → Step 2 脚本创作【确认闸门】→ Step 3 TTS 配音 → Step 4 渲染合成
- 读图自理解：模型直接读漫画页，图片为主，`页面配置.json` 文字兜底（审查拦截时补全）
- 先脚本后出片：Step 2 产出 `口播脚本.md` 后停下来等老板确认，确认后才配音合成
- 每句口播绑定 page{N}，保证画面与口播/字幕同步
- TTS：edge-tts 免费配音（`scripts/tts_generate.py`），输出分句 mp3 + 时长清单
- 渲染：HTML 排版 + Playwright 截图 + ffmpeg 合成（`scripts/render_video.py`），Ken Burns 推拉 + 字幕 + 可选 BGM

### 铁律
- ❌1 先脚本后出片（Step 2 确认闸门）
- ❌2 读图为主、配置文字兜底
- ❌3 每句口播绑定具体页
- ❌4 视频合成走确定性渲染，不走 AI 视频（Seedance/GenerateVideo）