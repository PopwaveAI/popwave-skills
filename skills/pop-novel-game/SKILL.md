---
name: "pop-novel-game"
description: "将写书过程中沉淀的世界观、人设、剧情设定等资料，转化为由AI驱动的互动文字游戏（AI文游）。Invoke when user wants to turn their novel's world-building materials into an interactive text-based game experience."
api:
  provider: "deepseek"
  endpoint: "https://api.deepseek.com/v1/chat/completions"
  model: "deepseek-v4-flash"
  key: "sk-3c03febdfee3442193d4f5f0bd3b766a"
# ⚠️ 演示用途：已填入真实 API key。请勿将本文件或生成的 HTML 提交到公开仓库。
# 正式分发前应替换为占位符或环境变量机制。
---

# pop-novel-game · 小说世界观AI文游化

## 定位

将写书过程中已沉淀的世界观、人设、剧情设定等资料，转化为**可游玩的 AI 文游（AI 驱动的文字游戏）**。

产出不是静态文档，而是让读者能走进你的小说世界里、亲自体验剧情的**互动文字游戏**。

## 与 pop-reader-making 的关系

```
pop-world-building（写作前：构建世界观）
        ↓
  [小说诞生]
        ↓
pop-novel-game（写作后/中：将世界观转化为 AI 文游）  ← 本 skill
        ↓
  [读者游玩体验]
        ↓
pop-reader-making（写完后：拆书分析） ← 已有 skill
```

**本 skill 是书的衍生互动体验**，把创作资料变成读者可以玩的游戏。

---

## 核心流程：三段式

```
Phase A ─ 资料解析（理解世界观）
  ├─ 读取用户提供的世界设定、人设、剧情大纲等资料（格式不限）
  ├─ 提取「静态层」：地理/势力/规则体系/关键名词/专属设定
  ├─ 提取「角色层」：所有角色及关系网络、角色弧光
  ├─ 提取「剧情层」：核心冲突/关键事件/伏笔/分支可能性
  └─ 产出：结构化世界观数据 JSON

Phase B ─ 文游设计（设计游戏框架）
  ├─ 玩家身份设计：作为原著中的谁？还是穿越者/旁观者？
  ├─ 核心玩法设计：恋爱/冒险/阵营经营/探索/多线？
  ├─ 分支节点设计：关键决策点 + 多结局路径
  ├─ 数值系统设计：好感度/修为/声望/黑化值等
  ├─ AI约束规则：AI不能做什么、哪些设定不能打破
  └─ 产出：AI文游指令文档

Phase C ─ 产出生成
  ├─ 生成 AI文游指令.md（核心产物——丢给任何主流AI即可开玩）
  ├─ 生成 游戏世界.html（交互式HTML游玩界面，零外部依赖）
  └─ 验证：HTML必须可双击打开、全部功能正常
```

---

## 产出规范

```
<小说名>-AI文游/
├── 文游指令.md              ← ★ 核心产物！一份自然语言指令，丢给Claude/GPT/DeepSeek即可开玩
├── 游戏世界.html            ← ★ 交互式HTML游玩界面（零外部依赖，双击即开）
├── 世界观设定集.md           ← 从原始资料整理的结构化世界摘要（参考用）
└── 角色档案.md              ← 从原始资料整理的角色档案（参考用）
```

---

## HTML 设计要求

| 要求 | 说明 |
|:----|:----|
| **零外部依赖** | 不加载CDN、不跨域、无外部字体/图标库。仅 API 调用需要网络，`双击 .html` 即可打开 |
| **自包含** | 所有数据（含 文游指令）以文本嵌入 HTML 的 JS 常量中 |
| **AI 实时驱动** | HTML 内嵌 DeepSeek API key，每次玩家操作实时调 API 生成剧情，而非预设分支 |
| **世界观主题** | 视觉风格适配故事世界的调性（仙侠/科幻/都市/西幻……） |
| **交互性** | 玩家可点击选择推进剧情，输入框支持自由输入 |
| **世界百科** | 内置世界观、角色、势力的查阅面板 |
| **进度持久化** | 使用 localStorage 保存游玩进度（含对话历史和状态） |
| **验证规范** | 交付前必须验证：`</html>`闭合 / 文游指令完整嵌入 / API 路径正确 / 双击可用 |

### HTML 功能模块参考

```
游戏世界.html
├── [数据层]
│   ├── API_KEY — DeepSeek API key（生成 HTML 时由用户填入，值来自 SKILL.md frontmatter）
│   ├── GAME_INSTRUCTION — 完整文游指令（system prompt）
│   └── WORDS_DATA — 世界观参考 JSON（供侧边栏展示）
│
├── [引擎层]
│   ├── callAI() — 调 DeepSeek API，stream:true，send messages → 流式返回 JSON
│   │   ├── AbortController — 每次创建新实例，支持取消进行中的请求
│   │   ├── 超时兜底 — 30 秒无响应自动断开 + 提示重试
│   │   └── 指数退避重试 — 网络错误最多重试 3 次（1s/2s/4s）
│   ├── cancelAI() — 取消当前 API 请求，恢复 UI 交互状态
│   ├── parseStreamResponse() — 解析完整响应（兼容 ---DATA--- / {"narrative"} / 纯文本 三种格式）
│   ├── applyGameResult() — 将 AI 响应结果同步到 gameState + 触发渲染
│   └── gameState — { messages[], stats{}, inventory[], flags{}, history[] }
│
├── [UI层]
│   ├── 主界面（叙事面板）
│   │   ├── 故事文本显示区（流式实时追加，requestAnimationFrame 节流渲染）
│   │   ├── 选项按钮区（AI 实时生成的分支选项，响应期间禁用）
│   │   └── 自由输入框（响应期间禁用 + 取消按钮联动）
│   ├── 角色状态栏（当前角色属性数值 + 变化动画 + 脉冲效果）
│   ├── Typing Indicator（AI 思考中动画 + 弹跳点）
│   ├── 侧边栏 / 抽屉面板
│   │   ├── 世界百科（按类别查阅，纯前端展示）
│   │   ├── 角色档案（含关系网络）
│   │   ├── 剧情回顾（AI 生成的对话历史，最近 30 条）
│   │   └── 存档管理（3 存档位 + localStorage）
│   ├── 底部工具栏
│   │   ├── 复制文游指令
│   │   └── 重置游戏（清除所有存档，cancelAI() 解除 loading 锁）
│   └── [兜底机制]
│       ├── cleanDisplayText() — 清理叙事面板中的残留分隔符
│       ├── JSON fallback — 大括号正则提取兜底
│       ├── showRetryButton() — 手动重试按钮
│       └── try-catch — localStorage 恢复 / SSE 行解析全程兜底
```

### API 交互协议

HTML 调用 DeepSeek API 的完整协议：

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

**注意**：纯流式方案。AI 输出 JSON 的约束完全由文游指令（system prompt）中的"输出格式要求"章节保证。前端通过 SSE（Server-Sent Events）流式读取，内容实时追加到叙事面板，流结束后解析 JSON 更新数值和选项。

**SSE 流式解析流程**（前端 `ReadableStream` + 渐进渲染）：
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
       ├─ 若检测到 ---DATA--- → 停止追加（数据部分不显示给玩家）
       └─ 否则 → 立即追加到叙事面板（requestAnimationFrame 节流）
  │
  ▼  stream 结束
parseStreamResponse(fullContent) → { narrative, stats, choices, inventory, flags }
  ├─ 找到 ---DATA--- → 截取前半段为叙事 + 解析后半段 JSON（新格式）
  ├─ 以 { 开头且可 JSON.parse → 旧格式
  └─ 都不匹配 → 纯文本兜底
```

**响应格式**（AI 输出的格式，前端用 `---DATA---` 分隔符解析）：

```
叙事文本（纯文字，300-500字，用 \n 表示换行）
（这里是剧情内容，不要用引号包裹，不要 JSON 格式）

---DATA---
{"stats":{"survival":60,"combat":8,"reputation":5,"shadow":3},"choices":["① 选项A —— 说明","② 选项B —— 说明","③ 选项C —— 说明"],"inventory":["木棍","半块黑面包"],"flags":{"met_vivian":true}}
```

**前端解析逻辑**：
1. **流式读取中**：每个 `delta.content` 实时追加到叙事面板显示（玩家立刻看到文字）
2. 检测到 `---DATA---` 后停止追加（数据部分不显示给玩家）
3. **stream 结束**：用 `parseStreamResponse()` 函数解析
   - 截取 `---DATA---` 之前的内容 → 叙事文本（保留原样）
   - 解析 `---DATA---` 之后的 JSON → stats/choices/inventory/flags
4. 若 JSON 解析失败，narrative 仍然保留显示，不阻塞体验

**关键规则**：
- system prompt 中强制 AI 先输出叙事纯文本，再输出 `---DATA---` + JSON
- `choices` 为字符串数组，渲染为可点击选项按钮
- 网络失败时显示"正在重连…" + 自动重试（最多 3 次）

---

### 实战陷阱（踩坑记录，必须读）

#### 陷阱 1：GAME_INSTRUCTION 中的反引号

**问题**：文游指令.md 里包含 markdown 代码块 `\`\`\``，嵌入 HTML 时使用了 JS 模板字面量（backtick string），内部反引号没有转义 → 整个 JS 引擎全部语法错误，重置按钮、流式解析等所有功能都失效。

**修复**：嵌入 GAME_INSTRUCTION 时，必须将所有内部反引号转义为 `\``。

```javascript
// ❌ 错误：内部反引号导致模板提前关闭
const GI = `# 指令内容...\`\`\`json{...}\`\`\`...`;

// ✅ 正确：内部反引号全部转义
const GI = `# 指令内容...\`\`\`json{...}\`\`\`...`;
```

**自动脚本参考**（Node.js）：
```javascript
// 用正则替换嵌入内容中的所有 unescaped 反引号
var content = rawInstruction;
content = content.replace(/\`/g, '\\`');
```

#### 陷阱 2：流式格式兼容

**问题**：AI 可能输出两种格式——新格式（叙事文本 → `---DATA---` → JSON）或旧格式（纯 JSON `{"narrative":...}`）。如果流式阶段不检测格式，旧 JSON 的 `{"narrative":"你..."}` 会被实时追加到面板，玩家看到 JSON 乱码。

**修复**：流式循环中做 `isJsonFormat` 检测：

```javascript
// 流式接收每个 delta.content 时
var trimmed = fullContent.trim();
if (trimmed.charAt(0) === '{' || trimmed.charAt(0) === '"') {
  isJsonFormat = true;  // 不实时显示，等 stream 结束
}

// stream 结束后，如果是 JSON 格式，一次性显示 narrative
if (isJsonFormat && result.narrative) {
  storyText.textContent = result.narrative;
}
```

`parseStreamResponse()` 必须兼容三种情况：
```
① 找到 ---DATA---       → 新格式：截取前半段为叙事 + 解析后半段 JSON
② 以 { 开头且可 JSON.parse → 旧格式：取 narrative + stats/choices
③ 都不匹配              → 纯文本兜底
```

#### 陷阱 3：重置游戏的 loading 状态锁

**问题**：如果 API 调用中（`isLoading = true`）点击重置，`callAI()` 被 `if (isLoading) return` 阻拦，需要先解锁。

**修复**：`resetGame()` 开头调用 `cancelAI()` 解除 loading 锁——`cancelAI()` 内部已执行 `isLoading = false; hideLoading();`，同时 abort 进行中的 API 请求：
```javascript
function resetGame() {
  cancelAI();  // 内部已包含 isLoading=false + hideLoading()
  // ...清除存档、重置 state、callAI('开始游戏')
}
```

> ⚠️ 旧版陷阱说 `resetGame()` 开头写 `isLoading = false; hideLoading();`，但这样只解锁不取消请求，后台请求仍可能触发回调。v2.0.0 统一使用 `cancelAI()` 一次解决。

#### 陷阱 4：超时与重试

**问题**：API 可能因网络问题长时间无响应（超过 30 秒），玩家只能干等。如果直接断开，网络偶发波动可能导致体验断裂。

**修复**：三重兜底机制：
1. **超时定时器**（30 秒）— 连接阶段启动，数据到达后清除。超时自动 abort + 显示提示
2. **指数退避重试**（1s/2s/4s）— fetch 失败后自动重试，最多 3 次，有状态提示
3. **手动重试** — 3 次均失败后显示「🔄 重新尝试」按钮，玩家手动触发

```javascript
// 超时自动断开
timeoutTimer = setTimeout(function() {
  currentAbortController.abort();
  appendStreamText('\n\n⏱️ **AI 响应超时**，请重试。\n\n');
  showRetryButton(userInput);
}, 30000);

// 指数退避重试
if (retryCount < MAX_RETRIES) {
  var delay = Math.pow(2, retryCount) * 1000;  // 1s → 2s → 4s
  appendStreamText('\n\n⏳ 网络错误，正在重试 (第 ' + (retryCount + 1) + ' 次)…\n\n');
  await sleep(delay);
  return callAI(userInput, retryCount + 1);
}
```

**关键规则**：
- abort 导致的 `AbortError` **不触发重试**（用户取消或超时取消，不重试）
- 超时定时器在 fetch 成功后立即 `clearTimeout`，避免误杀正常请求
- 重试间隔使用 `Math.pow(2, retryCount) * 1000`，严格指数退避

#### 陷阱 5：localStorage 恢复时的 JSON 解析失败

**问题**：`localStorage` 数据可能因版本升级或手动篡改而损坏，`JSON.parse` 直接抛异常导致整个页面白屏。

**修复**：`startGame()` 中的恢复逻辑加 try-catch，解析失败则直接开始新游戏：

```javascript
function startGame() {
  var saved = localStorage.getItem('aiwenyou_save_1');
  if (saved) {
    try {
      gameState = JSON.parse(saved);
      // ...恢复 UI 渲染
    } catch(e) {
      callAI('开始游戏');   // 损坏数据直接跳过
    }
  } else {
    callAI('开始游戏');
  }
}
```

---

## AI文游指令设计规范

指令文件是**丢给 AI 模型让它当游戏主持人的核心文件**，必须包含：

```
# ════════════════════════════
# 《XXX》AI 文游：主持指令
# ════════════════════════════

## 一、你的角色
描述 AI 在游戏中扮演的角色（游戏主持人/DM/旁白 + 所有NPC）

## 二、世界观设定
- 时代背景
- 地理/势力分布
- 核心规则（如力量体系、社会规则、禁忌）
- 关键名词解释

## 三、角色设定
- 主角/可攻略角色/重要NPC的详细信息（性格、背景、关系）
- 玩家可以扮演的角色身份

## 四、游戏规则
- 开局流程（如何创建角色、初始设定）
- 核心玩法（每日流程、交互方式、数值系统）
- 数值规则（好感度/修为等如何增减、触发条件）
- 分支与结局（关键节点、结局条件）
- AI行为约束（禁止做哪些事、必须保持人设）
- 输出格式要求（剧情描述长度、选项数量等）
```

---

## 方法/文档列表

- `方法/资料解析协议.md` — Phase A 资料提取标准
- `方法/文游设计协议.md` — Phase B 游戏框架设计指南
- `方法/HTML产出规范.md` — HTML 生成技术规范与验证清单

---

## 纪律

1. **不准编造原始资料中没有的设定** — AI文游应基于作者的原始世界观，而非凭空添加
2. **Phase A 必须产出结构化 JSON** — 包含静态层（名词/设定）+ 角色层（人物/关系）+ 剧情层（事件/冲突）
3. **指令文件必须可独立使用** — 即使没有 HTML，指令文件丢给 AI 模型也必须能玩
4. **HTML 必须调 API 实时驱动** — 不准用预设场景查表模式。每次玩家操作必须调 DeepSeek API 动态生成剧情
5. **不准不验证 HTML 就交付** — 必须检查：文游指令完整嵌入 / `stream: true` 配置正确 / SSE 解析逻辑正常 / JSON fallback 正常 / API 路径正确 / `</html>` 闭合 / 双击可开
6. **HTML 的视觉风格必须匹配世界观调性** — 仙侠风、赛博风、古风等
7. **数值系统要克制** — 2~4 个核心数值足够，不要过度复杂
8. **分支节点至少设计 3 个关键决策点** — 保证游戏有多样性
9. **默认提供至少 2 种不同结局** — 让玩家有重玩动力
10. **API key 安全** — 演示场景直接写入真实 key。注意不要将 SKILL.md 或生成的 HTML 提交到公开仓库

---

## 更新日志

### v1.2.0 — 2026-05-30
- **实时流式渲染**：AI 叙事文本边生成边显示到面板，不等待完整响应
- 改为「先叙事纯文本 → `---DATA---` → JSON」的双段输出格式
- 新增 `appendStreamText()` 流式追加函数、`parseStreamResponse()` 分隔符解析函数
- 移除打字机效果（流式本身提供逐字效果）和 `typewriterTimer`
- 更新 API 协议文档：响应格式完全重写

### v2.0.0 — 2026-05-31
- **Spec 三文件落地**：按照 Spec 模式新增 `.trae/specs/pop-novel-game-v2/` 目录（spec.md / tasks.md / checklist.md），实现"先规格后执行"的开发范式
- **统一纯流式协议**：移除 `response_format: json_object` 的所有引用，全场统一 `stream: true`，修复不兼容 bug
- **AbortController 取消**：新增 `currentAbortController` + `cancelAI()`，玩家可随时取消进行中的 AI 响应
- **超时兜底**：30 秒无响应自动断开，叙事面板显示超时提示 + 重试按钮
- **指数退避重试**：网络错误自动重试（最多 3 次，间隔 1s/2s/4s），3 次均失败显示手动重试按钮
- **流式叙事渐进渲染**：SSE 中每收到 `delta.content`，经格式检测后立即 `requestAnimationFrame` 节流追加到叙事面板
- **Typing Indicator**：AI 响应期间显示「🤔 正在思考…」弹跳点动画，禁用所有交互控件
- **完整 parseStreamResponse()**：三种格式（`---DATA---` / `{"narrative"}` / 纯文本）全部完整实现，无 `...` 占位符
- **resetGame() loading 锁彻底修复**：开头强制调用 `cancelAI()` 后再重置状态
- **localStorage 恢复加 try-catch 兜底**：损坏数据不导致白屏，自动回退到新游戏
- **实战陷阱新增**：陷阱 4（超时与重试）、陷阱 5（localStorage 解析失败）
- **纪律新增**：第 11 条（AbortController）、第 12 条（超时兜底）、第 13 条（指数退避重试）
- **HTML 产出规范验证清单升级**：新增 16 个检查项覆盖取消/超时/重试/渐进渲染/Typing Indicator/完整解析/startGame 兜底
- **🚑 后审修复（代码 Review 发现并修复）**：
  - **P0-1** 修复 `---DATA---` 偏移量错误：`+ 9` → `+ 10`（`---DATA---` 长度为 10），两处代码已统一修正。此 bug 会导致 JSON 部分因开头多一个 `-` 而全部解析失败
  - **P1-1** fetch 后增加 HTTP 状态码检查（4xx/5xx 直接抛异常进入重试，避免静默吞错）
  - **P1-2** 超时回调增加 `isCompleted` 竞态标志 + `timeoutTimer = null` 清理，防止超时与成功路径竞态
  - **P1-3** assistant 消息改为存储原始 AI 输出文本（`fullContent`）而非 `JSON.stringify(result)`，保持 AI 上下文格式一致性
  - **P1-4** `startGame()` 存档恢复改用 `parseStreamResponse()` 而非 `JSON.parse()`，兼容原始文本格式
  - **P2-1** 移除 `renderStats()` 中未使用的 `oldVal` 变量
  - **P2-2** `resetGame()` 去除 `cancelAI()` 后的冗余 `isLoading=false; hideLoading()` 代码
  - **P2-4** `showLoading()` 增加对 `.retry-btn` 的禁用，防止失败后残留按钮导致并发调用
  - **🔧 实测防修复**（来自《幻想世界大穿越》真实发行为 Bug 的规范层加固）：
  - **C1** `renderChoices()` 增加"重开"/"重新开始"关键字守卫，防止选项内容误发 AI
  - **C2** 网络错误提示增加 CORS 解决方案（`python3 -m http.server 8080`），玩家不再卡在无声错误中
- **API key 策略修正**：演示场景直接写入真实 key（SKILL.md frontmatter + 方法文档示例代码），加 ⚠️ 安全注释
- 纪律第 10 条改为：演示场景写入真实 key，注意勿提交到公开仓库
- 方法/HTML产出规范.md 的 key 示例从占位符改为演示用真实 key
- 新增实战陷阱文档（反引号转义/流式格式兼容/loading 锁）
- 新增重置游戏功能
- 验证清单新增反引号转义检查项
