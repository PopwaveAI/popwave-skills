# HTML 产出规范 · Phase C

## 目标

生成一个**自包含的交互式 HTML**，作为 AI 文游的游玩界面。零外部依赖，双击即可在浏览器中打开。

## 技术选型

| 项目 | 要求 |
|:----|:----|
| **框架** | 纯 HTML + CSS + JavaScript，无框架依赖 |
| **外部资源** | 零外部引用，不使用 CDN、Google Fonts、图标库等。仅 API 调用需要网络 |
| **数据** | 文游指令以 `const GAME_INSTRUCTION` 完整嵌入 HTML。世界观参考数据以 JSON 嵌入 |
| **AI 引擎** | 内嵌 DeepSeek API key（来自 SKILL.md frontmatter），每次玩家操作实时调 API |
| **字体** | 使用系统字体栈（`system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`） |
| **存储** | 使用 `localStorage` 保存游戏进度（含对话历史、stats、inventory、flags） |
| **编码** | UTF-8（`<meta charset="UTF-8">`） |

## HTML 结构规范

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>《书名》AI 文游</title>
  <style>
    /* 所有 CSS 内联 */
  </style>
</head>
<body>
  <!-- HTML 结构 -->

  <script>
    // ═══════ 0. 凭据与数据 ═══════
    const API_KEY = '...';  // 由环境变量或用户输入注入
    const API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';
    const MODEL = 'deepseek-v4-flash';

    // ★ 完整文游指令，作为 system prompt
    const GAME_INSTRUCTION = `...`;

    // 侧边栏展示用的世界观参考数据
    const WORDS_DATA = { ... };

    // ═══════ 1. 游戏状态 ═══════
    let gameState = {
      messages: [{ role: 'system', content: GAME_INSTRUCTION }],
      stats: { survival: 65, combat: 5, reputation: 0, shadow: 0 },
      inventory: [],
      flags: {},
      history: []
    };

    // ═══════ 2. API 调用 ═══════
    async function callAI(userInput) { ... }
    function cancelAI() { ... }

    // ═══════ 3. 渲染逻辑 ═══════
    function renderNarrative(text) { ... }
    function renderStats(stats) { ... }
    function renderChoices(choices) { ... }
    function renderHistory() { ... }
    function renderWorld() { ... }
    function renderCharacters() { ... }

    // ═══════ 4. 交互逻辑 ═══════
    function handleChoice(choiceText) { callAI(choiceText); }
    function handleFreeInput(text) { callAI(text); }

    // ═══════ 5. 启动 ═══════
    // 从 localStorage 恢复或开始新游戏
    // 新游戏: callAI("开始游戏")
  </script>
</body>
</html>
```

## 功能模块

### 1. 叙事主面板（核心）

```
┌──────────────────────────────────┐
│  [角色头像]  角色名   LV.3       │
│  好感度: ████████░░ 72/100      │
├──────────────────────────────────┤
│  你推开那扇门，迎面而来的是一股   │
│  淡淡的花香。                    │
│  「你来了。」她轻声说道。        │
├──────────────────────────────────┤
│  [○] 「有什么事直说吧。」        │
│  [○] 「你的眼睛很美。」          │
│  [○] 沉默不语                    │
│  [○] 💬 自由输入...              │
├──────────────────────────────────┤
│  输入框: ________________ [发送] │
└──────────────────────────────────┘
```

**功能**：
- 故事文本显示区（自动滚动到底部）
- 选项按钮（点击即选择）
- 自由输入框（玩家可自定义操作）
- 打字机效果（可选，逐字展示新文本）

### 2. 角色状态栏

- 显示当前玩家角色的核心数值
- 数值变化时用动画效果提示（如 +5 / -3）
- 鼠标悬停显示数值说明

### 3. 侧边栏（抽屉面板）

```
世界百科                   ───
  ├─ 地理志     [展开 ▾]
  ├─ 势力阵营   [展开 ▾]
  ├─ 关键名词   [展开 ▾]
  └─ 规则体系   [展开 ▾]

角色档案                   ───
  ├─ 所有角色列表
  └─ 角色关系网络

剧情回顾                   ───
  └─ 历史对话/事件日志

存档管理                   ───
  ├─ 存档位 1 [保存] [读取]
  ├─ 存档位 2 [保存] [读取]
  └─ 存档位 3 [保存] [读取]
```

### 4. 底部工具栏

- **复制文游指令** — 一键复制完整的 AI 文游指令到剪贴板
- **存档管理** — 快速存取档
- **设置** — 字体大小、打字机速度等

## 视觉风格

视觉设计必须适配世界观调性：

| 世界观类型 | 配色参考 | 字体风格 | 装饰元素 |
|:----------|:--------|:--------|:--------|
| **仙侠/古风** | 墨黑/朱红/青绿/米白 | 衬线风 | 水墨纹理、印章、卷轴 |
| **科幻/赛博** | 暗紫/霓虹蓝/荧光绿 | 无衬线、科技感 | 发光线条、网格 |
| **西幻/魔幻** | 深蓝/金币/羊皮纸色 | 中世纪风格 | 纹章、符文、羊皮纸 |
| **都市/现代** | 白/灰/品牌色 | 干净简约 | 卡片式、圆角 |
| **暗黑/恐怖** | 纯黑/暗红/灰白 | 粗重衬线 | 血迹、裂纹、模糊 |

**设计原则**：
- 减少不必要的装饰，保持可读性优先
- 适度的 CSS 动画增强体验（如淡入、滑动）
- 响应式设计：适配桌面和移动端

## 游戏引擎核心逻辑（API 实时驱动版）

### 核心流程

```
玩家点击选项 / 输入文字
        │
        ▼
callAI(userInput)
        │
        ├─ 构建 messages = [system(文游指令), ..., assistant(AI上轮回复), user(玩家输入)]
        ├─ POST → https://api.deepseek.com/v1/chat/completions
        │
        ▼
        解析响应 JSON
        ├─ narrative  → 渲染叙事文本（打字机效果）
        ├─ stats      → 更新状态栏（带变化动画）
        ├─ choices    → 渲染选项按钮
        ├─ inventory  → 更新物品栏
        └─ flags      → 更新剧情标记
        │
        ▼
        将 AI 回复追加到 messages
        等待玩家下一次操作
```

### API 交互规范

**请求**（POST `https://api.deepseek.com/v1/chat/completions`）：
```json
{
  "model": "deepseek-v4-flash",
  "messages": [
    {"role": "system", "content": "（完整文游指令）"},
    {"role": "assistant", "content": "上一轮AI的叙事和选项..."},
    {"role": "user", "content": "玩家本次的选择或自由输入"}
  ],
  "temperature": 0.85,
  "max_tokens": 2048,
  "stream": true
}
```

**SSE 流式解析流程**：
```
fetch(stream: true)
  │
  ▼
response.body.getReader()
  │
  ▼  逐块读取
for each chunk:
  ├─ 按 '\n' 分割行
  ├─ 取 'data: ' 前缀后的 JSON
  ├─ 检查 payload === '[DONE]' → 结束
  └─ choices[0].delta.content → 累积到 fullContent
       │
       ▼  实时渐进渲染（格式检测）
       ├─ 若以 { 或 " 开头（旧 JSON 格式）→ 不显示，等流结束
       ├─ 若检测到 ---DATA--- → 停止追加
       └─ 否则 → 立即追加到叙事面板（requestAnimationFrame 节流）
  │
  ▼  stream 结束
parseStreamResponse(fullContent) → { narrative, stats, choices, inventory, flags }
```

**响应格式**：
```
叙事文本（纯文字，300-500字，用 \n 表示换行）

---DATA---
{"stats":{"survival":60,"combat":8,"reputation":5,"shadow":3},"choices":["① 选项A","② 选项B","③ 选项C"],"inventory":["木棍","半块黑面包"],"flags":{"met_vivian":true}}
```

### API 响应解析（三格式兼容）

```javascript
function parseStreamResponse(fullContent) {
  var content = fullContent.trim();
  var result = { narrative: null, stats: null, choices: null, inventory: null, flags: null };

  // ① 新格式：叙事文本 → ---DATA--- → JSON
  var sepIndex = content.indexOf('---DATA---');
  if (sepIndex !== -1) {
    result.narrative = content.substring(0, sepIndex).trim();
    var jsonStr = content.substring(sepIndex + 10).trim();
    try {
      var parsed = JSON.parse(jsonStr);
      result.stats = parsed.stats || null;
      result.choices = parsed.choices || null;
      result.inventory = parsed.inventory || null;
      result.flags = parsed.flags || null;
    } catch(e) { /* 叙事仍有效 */ }
    return result;
  }

  // ② 旧 JSON 格式
  if (content.charAt(0) === '{') {
    try {
      var parsed = JSON.parse(content);
      result.narrative = parsed.narrative || null;
      result.stats = parsed.stats || null;
      result.choices = parsed.choices || null;
      result.inventory = parsed.inventory || null;
      result.flags = parsed.flags || null;
      return result;
    } catch(e) {
      var m = content.match(/\{[\s\S]*\}/);
      if (m) {
        try {
          var parsed2 = JSON.parse(m[0]);
          result.narrative = parsed2.narrative || null;
          result.stats = parsed2.stats || null;
          result.choices = parsed2.choices || null;
          result.inventory = parsed2.inventory || null;
          result.flags = parsed2.flags || null;
          return result;
        } catch(e2) { /* 继续兜底 */ }
      }
    }
  }

  // ③ 兜底：纯文本
  result.narrative = content;
  return result;
}
```

## 实战陷阱

### 陷阱 1：GAME_INSTRUCTION 中的反引号

**问题**：文游指令.md 里包含 markdown 代码块，嵌入 HTML 时使用 JS 模板字面量，内部反引号未转义导致语法错误。

**修复**：嵌入 GAME_INSTRUCTION 前，将所有内部反引号转义为 `\``。

### 陷阱 2：流式格式兼容

**问题**：AI 可能输出新格式（叙事文本 → `---DATA---` → JSON）或旧格式（纯 JSON）。流式阶段不检测格式会导致乱码。

**修复**：流式循环中做 `isJsonFormat` 检测，JSON 格式等 stream 结束后一次性显示。

### 陷阱 3：重置游戏的 loading 状态锁

**问题**：API 调用中点击重置，`callAI()` 被 `if (isLoading) return` 阻拦。

**修复**：`resetGame()` 开头调用 `cancelAI()` 解除 loading 锁。

### 陷阱 4：超时与重试

**问题**：API 可能因网络问题长时间无响应。

**修复**：
1. **超时定时器**（30 秒）— 连接阶段启动，数据到达后清除
2. **指数退避重试**（1s/2s/4s）— fetch 失败后自动重试，最多 3 次
3. **手动重试** — 3 次均失败后显示重试按钮

### 陷阱 5：localStorage 恢复时的 JSON 解析失败

**问题**：`localStorage` 数据可能因版本升级或手动篡改损坏。

**修复**：`try-catch` 包裹恢复逻辑，解析失败直接开始新游戏。

## 验证清单

交付 HTML 前必须逐项检查：

```
□ </html> 正确闭合
□ 零外部 CDN/远程资源引用（除 API 调用外）
□ API_KEY 通过环境变量或交互式提示注入（禁止硬编码）
□ API_ENDPOINT 配置正确
□ stream: true 已设置
□ GAME_INSTRUCTION 完整嵌入
□ GAME_INSTRUCTION 内部反引号已转义
□ SSE 解析逻辑正确
□ parseStreamResponse() 兼容三种格式
□ AbortController 已实现
□ 超时机制（30秒）
□ 指数退避重试（最多3次）
□ localStorage 读/写正常
□ 视觉风格匹配世界观调性
□ 双击可正常打开
□ 自由输入框和选项按钮工作正常
```

## 纪律

1. **必须实时调 API** — 不准用预设场景查表模式
2. **必须验证** — 不验证 HTML 不准交付
3. **零外部依赖（除 API 外）**
4. **代码简洁** — 核心逻辑控制在 500 行以内
5. **Fallback 处理** — 指数退避重试 + 手动重试按钮
6. **不开新窗口** — 所有交互在单页面内完成
7. **API key 安全** — 禁止硬编码在文件中
8. **GAME_INSTRUCTION 必须完整** — 全文嵌入，不截断
9. **GAME_INSTRUCTION 反引号必须转义**
10. **同时支持旧 JSON 和新 ---DATA--- 格式**
11. **AbortController 必须实现**
12. **必须实现超时兜底**
13. **必须实现指数退避重试**
