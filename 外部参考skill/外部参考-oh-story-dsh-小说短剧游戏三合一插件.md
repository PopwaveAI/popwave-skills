# oh-story-dsh：小说/短剧/游戏三合一创作插件

> 采源：微信公众号「PROMPT ENGINEERING SQUAD（Prompt 工程队）」
> 原文链接：https://mp.weixin.qq.com/s/y6h26u63FQuewd8xgqiawQ
> 抓取日期：2026-09-05
> 项目地址：github.com/zenstory-ai/oh-story-dsh

---

写小说、拍短剧、做互动游戏，这三件事原本要用三套工具、开三个窗口来回倒腾。GitHub 上有个叫 **oh-story-dsh** 的开源插件，把这三条创作流水线装进了 DeepSeek 出的开源 Agent 工作台 DeepSeek Harness（DSH）里——左边是文件树和编辑器，右边是 AI 对话，写完小说让它改游戏，全程不换窗口。

小说工作台：文件树、编辑器、AI 对话三栏联动

## 一个插件，三张工作台

插件来自 zenstory-ai 组织，8 月 19 日建仓，10 天拿下 222 星，MIT 协议，昨天还在提交更新。它本身是个「聚合器」：把三个开源创作项目的方法库打包进 DSH——写小说的 **Oh Story**、做短剧的 **Drama Skills**、把小说改成互动游戏的 **NovelToGame**。DSH 负责 Agent、会话、模型和权限，插件负责创作流程，顶部 Tab 随时切换三张工作台。

### 能力目录

| 工作台 | 版本 | 规模 | 入口 |
|---|---|---|---|
| 小说 | Oh Story 0.7.8 | 13 个 Skills + 7 个专业 Roles | /story |
| 短剧 | Drama Skills 0.6.1 | 10 个 Skills | /short-drama |
| 游戏 | NovelToGame 0.3.0 | 7 个 Skills | /novel-to-game quick |

## 小说工作台：从选题到去 AI 味

覆盖长篇、短篇、选题、扫榜、拆文、导入、审稿、去 AI 味和封面全流程。AI 调用工具改文件时，编辑器会实时定位到目标文件，边生成边看；点 Chat 里提到的文件名，文件树直接跳过去，不用手动翻目录。

## 短剧工作台：每集五份文档，一份真相

每集维护最多五份可读 Markdown：**剧本、视觉设定、分镜、图片提示词、视频提示词**。「生产」视图把这些文档投影成镜头板、素材板和成片顺序，重复 ID、悬空引用就地标红，不另建第二份真相。配套关系画布可拖拽整理角色、场景、道具的视觉关系；媒体库自动汇总各集生成的图片和视频成果。

媒体生成内置 GPT Image 2、Seedance、MiniMax Music 的可选适配——账号和 API Key 由 DSH 统一管理，插件不碰凭据。

## 游戏面板：边聊边试玩

游戏模式是两列布局：左边是隔离运行的实时游戏预览，右边保留完整 AI 对话。AI 改完代码生成 **build/app/** 后自动进入项目列表，刷新、全屏、试玩都不用离开对话。仓库内置《金瓶梅 · 风月总账》完整可玩构建，装完就能验证输入、核心循环和结局流程。

游戏面板窄屏两列布局

## 上手门槛

需要 Node.js 24+，两条命令装完（npx -y @deepseek-ai/dsh@0.1.1-rc.1 plugin --profile web add @oh-story/dsh@0.1.4，然后 npx -y @deepseek-ai/dsh@0.1.1-rc.1 web），默认开在本机 3080 端口。模型在「设置 → 模型」里填 API Key，或提前设好 DEEPSEEK_API_KEY 环境变量。

## 实事求是说

- 需要 Node.js 24+ 和 DSH 基础，纯小白有一定上手门槛
- 图片/视频/音乐生成依赖第三方 API，费用走自己的账号
- 项目 8 月中才建仓，版本 0.1.x，功能还在快速迭代期

---

关注「Prompt 工程队」，每天拆解一个拿来就能用的 AI 工具
