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
    // ═══════ 0. 凭据与数据（从 Phase A / Phase B 嵌入） ═══════
    const API_KEY = 'sk-3c03febdfee3442193d4f5f0bd3b766a';  // ⚠️ 演示用真实 key
     const API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';
    const MODEL = 'deepseek-v4-flash';

    // ★ 完整文游指令，作为 system prompt
    const GAME_INSTRUCTION = `...`;

    // 侧边栏展示用的世界观参考数据
    const WORDS_DATA = { ... };

    // ═══════ 1. 游戏状态 ═══════
    let gameState = {
      messages: [
        { role: 'system', content: GAME_INSTRUCTION }
      ],
      stats: { survival: 65, combat: 5, reputation: 0, shadow: 0 },
      inventory: [],
      flags: {},
      history: []    // 纯显示用
    };

    // ═══════ 2. API 调用 ═══════
    async function callAI(userInput) {
      const msgs = [...gameState.messages, { role: 'user', content: userInput }];
      const res = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${API_KEY}` },
        body: JSON.stringify({
          model: MODEL,
          messages: msgs,
          temperature: 0.85,
          max_tokens: 2048,
          stream: true
        })
      });
      const data = await res.json();
      const parsed = JSON.parse(data.choices[0].message.content);
      // parsed = { narrative, stats, choices, inventory, flags }
      // 更新 gameState.messages / stats / inventory / flags
      // 更新 history
      // 调用渲染函数
    }

    // ═══════ 3. 渲染逻辑 ═══════
    function renderNarrative(text) { ... }     // 打字机效果
    function renderStats(stats) { ... }        // 进度条 + 动画
    function renderChoices(choices) { ... }    // 选项按钮
    function renderHistory() { ... }           // 剧情回顾
    function renderWorld() { ... }             // 世界百科
    function renderCharacters() { ... }        // 角色档案
    function renderSaveSlots() { ... }         // 存档管理

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
│                                  │
│  你推开那扇门，迎面而来的是一股   │
│  淡淡的花香。房间里的烛光摇曳，   │
│  「你来了。」她轻声说道，眼中有   │
│  着难以言说的复杂情绪。          │
│                                  │
│  —— 她似乎有话要说，却欲言又止。 │
│                                  │
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

HTML 不再维护预设的场景表，而是维护一个**对话消息数组**，每次玩家操作都通过 API 驱动生成剧情。

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

### 关键 JavaScript 代码框架

```javascript
// ════════════════════════════════
// 数据层
// ════════════════════════════════

const API_KEY = 'sk-3c03febdfee3442193d4f5f0bd3b766a';  // ⚠️ 演示用真实 key
const API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';
const MODEL = 'deepseek-v4-flash';

// ★ 完整文游指令作为 system prompt
const GAME_INSTRUCTION = `<从 Phase B 产出的文游指令.md 全文嵌入>`;

// ════════════════════════════════
// 游戏状态
// ════════════════════════════════

let gameState = {
  messages: [
    { role: 'system', content: GAME_INSTRUCTION }
  ],
  stats: { survival: 65, combat: 5, reputation: 0, shadow: 0 },
  inventory: [],
  flags: {},
  history: []    // 纯前端展示用
};

// ════════════════════════════════
// API 调用引擎（流式版）
// ════════════════════════════════

let isLoading = false;
let currentAbortController = null;   // ★ 用于取消进行中的请求
let timeoutTimer = null;             // ★ 超时定时器
const TIMEOUT_MS = 30000;            // 30 秒超时
const MAX_RETRIES = 3;               // 最多重试 3 次

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function cleanDisplayText(text) {
  // 清理叙事面板中的残留分隔符标记
  return text.replace(/---DATA---[\s\S]*$/, '').trim();
}

// 取消当前 AI 响应
function cancelAI() {
  if (currentAbortController) {
    currentAbortController.abort();
    currentAbortController = null;
  }
  if (timeoutTimer) {
    clearTimeout(timeoutTimer);
    timeoutTimer = null;
  }
  isLoading = false;
  hideLoading();
}

// 指数退避重试的主调用函数
async function callAI(userInput, retryCount) {
  if (retryCount === undefined) retryCount = 0;
  if (isLoading && retryCount === 0) return;
  if (retryCount === 0) {
    isLoading = true;
    showLoading();
  }

  const msgs = [...gameState.messages, { role: 'user', content: userInput }];

  // 创建可取消的 AbortController
  currentAbortController = new AbortController();
  const signal = currentAbortController.signal;

  // ★ 竞态防护：请求完成后避免超时回调误触
  var isCompleted = false;

  // 启动超时定时器
  timeoutTimer = setTimeout(function() {
    if (isCompleted) return;
    timeoutTimer = null;
    if (currentAbortController) {
      currentAbortController.abort();
      currentAbortController = null;
    }
    isLoading = false;
    hideLoading();
    appendStreamText('\n\n⏱️ **AI 响应超时**，请重试。\n\n');
    showRetryButton(userInput);
  }, TIMEOUT_MS);

  try {
    const res = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${API_KEY}` },
      body: JSON.stringify({
        model: MODEL,
        messages: msgs,
        temperature: 0.85,
        max_tokens: 2048,
        stream: true
      }),
      signal: signal
    });

    // ★ HTTP 状态码检查：非 2xx 直接抛异常进入重试
    if (!res.ok) {
      var errText = '';
      try { errText = await res.text(); } catch(e) { errText = res.statusText; }
      throw new Error('API Error ' + res.status + ': ' + errText);
    }

    // 清除超时定时器——已成功连接
    if (timeoutTimer) { clearTimeout(timeoutTimer); timeoutTimer = null; }

    // ★ SSE 流式解析 + 渐进渲染
    var reader = res.body.getReader();
    var decoder = new TextDecoder();
    var fullContent = '';
    var buffer = '';
    var isJsonFormat = false;
    var dataSectionReached = false;
    var pendingText = '';
    var rafId = null;

    function flushText() {
      if (pendingText) {
        appendStreamText(pendingText);
        pendingText = '';
      }
      rafId = null;
    }

    while (true) {
      var readResult = await reader.read();
      if (readResult.done) break;
      buffer += decoder.decode(readResult.value, { stream: true });
      var lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (var li = 0; li < lines.length; li++) {
        var t = lines[li].trim();
        if (!t || t.indexOf('data: ') !== 0) continue;
        var payload = t.slice(6);
        if (payload === '[DONE]') continue;
        try {
          var d = JSON.parse(payload);
          var delta = d.choices && d.choices[0] && d.choices[0].delta && d.choices[0].delta.content;
          if (!delta) continue;

          fullContent += delta;

          // 格式检测：旧 JSON 格式不实时显示
          var trimmed = fullContent.trim();
          if (!isJsonFormat && (trimmed.charAt(0) === '{' || trimmed.charAt(0) === '"')) {
            isJsonFormat = true;
          }

          // 检测 ---DATA--- 分隔符
          if (!dataSectionReached && fullContent.indexOf('---DATA---') !== -1) {
            dataSectionReached = true;
          }

          // ★ 渐进渲染：非 JSON 且未到 DATA 段的内容实时追加
          if (!isJsonFormat && !dataSectionReached) {
            pendingText += delta;
            if (!rafId) {
              rafId = requestAnimationFrame(flushText);
            }
          }
        } catch(e) { /* SSE 行解析容错 */ }
      }
    }

    // 确保最后一段渲染完成
    if (rafId) cancelAnimationFrame(rafId);
    flushText();

    // ★ 关闭流后解析完整内容
    var result = parseStreamResponse(fullContent);
    isCompleted = true;  // 成功完成，阻止超时回调误触
    currentAbortController = null;
    isLoading = false;
    hideLoading();

    // 更新游戏状态（传入原始 fullContent 供 messages 存储）
    applyGameResult(result, userInput, fullContent);
    return result;

  } catch (err) {
    // 清除超时定时器
    if (timeoutTimer) { clearTimeout(timeoutTimer); timeoutTimer = null; }
    currentAbortController = null;

    // 用户取消不重试
    if (err.name === 'AbortError') {
      isLoading = false;
      hideLoading();
      return;
    }

    // 指数退避重试
    if (retryCount < MAX_RETRIES) {
      var delay = Math.pow(2, retryCount) * 1000;  // 1s → 2s → 4s
      appendStreamText('\n\n⏳ 网络错误，正在重试 (第 ' + (retryCount + 1) + ' 次)…\n\n');
      await sleep(delay);
      return callAI(userInput, retryCount + 1);
    }

    // 3 次均失败
    isLoading = false;
    hideLoading();
    appendStreamText('\n\n❌ 网络请求失败。\n');
    appendStreamText('[提示: 如果直接双击 HTML 文件打开，浏览器同源策略(CORS)会阻止 API 请求。请在文件夹地址栏输入 cmd，运行: python3 -m http.server 8080，然后在浏览器访问 http://localhost:8080 即可正常游玩]\n\n');
    showRetryButton(userInput);
  }
}

// ★ 完整 parseStreamResponse() — 兼容三种格式，无占位符
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
    } catch(e) {
      // JSON 部分解析失败，纯文本叙事仍有效
    }
    return result;
  }

  // ② 旧格式：{"narrative":"...","stats":{...}}
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
      // JSON 解析失败→尝试大括号正则兜底
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

// 将 AI 响应结果应用到游戏状态（fullContent = 原始 AI 输出文本）
function applyGameResult(result, userInput, fullContent) {
  if (!result) return;

  // 追加到 messages（存储原始 AI 输出，保持上下文格式一致性）
  var assistantContent = fullContent || JSON.stringify(result);
  gameState.messages.push({ role: 'user', content: userInput });
  gameState.messages.push({ role: 'assistant', content: assistantContent });

  // 渲染叙事
  if (result.narrative) {
    renderNarrative(result.narrative);
  }

  // 更新并渲染数值
  if (result.stats) {
    Object.assign(gameState.stats, result.stats);
    renderStats(gameState.stats);
  }

  // 渲染选项
  if (result.choices) {
    renderChoices(result.choices);
  }

  // 更新背包
  if (result.inventory) {
    gameState.inventory = result.inventory;
    renderInventory(gameState.inventory);
  }

  // 更新标记
  if (result.flags) {
    Object.assign(gameState.flags, result.flags);
  }

  // 记录历史（纯前端展示用）
  if (result.narrative) {
    gameState.history.push({
      narrative: result.narrative,
      stats: result.stats ? Object.assign({}, result.stats) : null,
      choices: result.choices ? result.choices.slice() : null,
      timestamp: Date.now()
    });
    if (gameState.history.length > 30) gameState.history.shift();
    renderHistory();
  }
}

// ════════════════════════════════
// 渲染函数
// ════════════════════════════════

function renderNarrative(text) {
  // 将文本追加到叙事面板，自动滚动到底部
  var p = document.createElement('p');
  p.textContent = text;
  storyText.appendChild(p);
  scrollToBottom();
}

function appendStreamText(text) {
  // 流式阶段追加文本到叙事面板（渐进渲染）
  var lastP = storyText.lastElementChild;
  if (!lastP || lastP.tagName !== 'P') {
    lastP = document.createElement('p');
    storyText.appendChild(lastP);
  }
  lastP.textContent += text;
  scrollToBottom();
}

function renderStats(stats) {
  // 更新状态栏数值，播放变化动画
  for (var key in stats) {
    var el = document.getElementById('stat-' + key);
    if (el) {
      var newVal = stats[key];
      el.textContent = newVal;
      // 播放脉冲动画
      el.className = 'stat-value flash';
      setTimeout(function() { el.className = 'stat-value'; }, 600);
    }
  }
}

function renderChoices(choices) {
  // 将字符串数组渲染为可点击按钮（含"重开"关键字守卫）
  var container = document.getElementById('choices-container');
  if (!container) return;
  container.innerHTML = '';
  if (!choices || choices.length === 0) return;
  for (var i = 0; i < choices.length; i++) {
    var btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.textContent = choices[i];
    // ★ 关键字守卫：检测"重开"/"重新开始"→ 调用重置而非 callAI
    btn.onclick = function(text) {
      return function() {
        if (text.indexOf('重开') !== -1 || text.indexOf('重新开始') !== -1) {
          if (typeof resetGame === 'function') { resetGame(); return; }
        }
        callAI(text);
      };
    }(choices[i]);
    container.appendChild(btn);
  }
}

function renderInventory(inventory) {
  var el = document.getElementById('inventory-display');
  if (el) el.textContent = inventory && inventory.length ? inventory.join('、') : '（空）';
}

function renderHistory() {
  // 反向显示最近记录
  var el = document.getElementById('history-list');
  if (!el) return;
  el.innerHTML = '';
  for (var i = gameState.history.length - 1; i >= 0; i--) {
    var item = document.createElement('div');
    item.className = 'history-item';
    item.textContent = gameState.history[i].narrative.substring(0, 80) + '…';
    el.appendChild(item);
  }
}

function showRetryButton(userInput) {
  var container = document.getElementById('choices-container');
  if (!container) return;
  var btn = document.createElement('button');
  btn.className = 'choice-btn retry-btn';
  btn.textContent = '🔄 重新尝试';
  btn.onclick = function() { callAI(userInput); };
  container.appendChild(btn);
}

function scrollToBottom() {
  var panel = document.getElementById('story-panel');
  if (panel) panel.scrollTop = panel.scrollHeight;
}

// ════════════════════════════════
// Loading 状态管理
// ════════════════════════════════

function showLoading() {
  var indicator = document.getElementById('typing-indicator');
  if (indicator) indicator.style.display = 'block';
  // 禁用选项按钮
  var container = document.getElementById('choices-container');
  if (container) {
    var btns = container.querySelectorAll('button');
    for (var i = 0; i < btns.length; i++) btns[i].disabled = true;
  }
  // 禁用重试按钮（上次失败留下的）
  var retryBtns = document.querySelectorAll('.retry-btn');
  for (var r = 0; r < retryBtns.length; r++) retryBtns[r].disabled = true;
  // 禁用输入框
  var input = document.getElementById('free-input');
  if (input) input.disabled = true;
  var sendBtn = document.getElementById('send-btn');
  if (sendBtn) sendBtn.disabled = true;
  // 显示取消按钮
  var cancelBtn = document.getElementById('cancel-btn');
  if (cancelBtn) cancelBtn.style.display = 'inline-block';
}

function hideLoading() {
  var indicator = document.getElementById('typing-indicator');
  if (indicator) indicator.style.display = 'none';
  // 启用选项按钮
  var container = document.getElementById('choices-container');
  if (container) {
    var btns = container.querySelectorAll('button');
    for (var i = 0; i < btns.length; i++) btns[i].disabled = false;
  }
  // 启用输入框
  var input = document.getElementById('free-input');
  if (input) input.disabled = false;
  var sendBtn = document.getElementById('send-btn');
  if (sendBtn) sendBtn.disabled = false;
  // 隐藏取消按钮
  var cancelBtn = document.getElementById('cancel-btn');
  if (cancelBtn) cancelBtn.style.display = 'none';
}

// ════════════════════════════════
// 启动
// ════════════════════════════════

function resetGame() {
  cancelAI();  // cancelAI() 内部已执行 isLoading=false + hideLoading()
  // 清除所有存档
  for (var i = 1; i <= 3; i++) {
    localStorage.removeItem('aiwenyou_save_' + i);
  }
  // 重置状态
  gameState = {
    messages: [{ role: 'system', content: GAME_INSTRUCTION }],
    stats: { survival: 65, combat: 5, reputation: 0, shadow: 0 },
    inventory: [],
    flags: {},
    history: []
  };
  // 清空 UI
  storyText.innerHTML = '';
  document.getElementById('choices-container').innerHTML = '';
  renderStats(gameState.stats);
  renderInventory(gameState.inventory);
  // 开始新游戏
  callAI('开始游戏');
}

function startGame() {
  // 尝试从 localStorage 恢复
  var saved = localStorage.getItem('aiwenyou_save_1');
  if (saved) {
    try {
      var restored = JSON.parse(saved);
      gameState = restored;
      // 恢复 UI 渲染：用 parseStreamResponse 解析原始 AI 输出
      var lastMsg = gameState.messages[gameState.messages.length - 1];
      if (lastMsg && lastMsg.role === 'assistant') {
        var lastResult = parseStreamResponse(lastMsg.content);
        if (lastResult.narrative) renderNarrative(lastResult.narrative);
        if (lastResult.choices) renderChoices(lastResult.choices);
        if (lastResult.stats) renderStats(lastResult.stats);
        if (lastResult.inventory) renderInventory(lastResult.inventory);
      }
    } catch(e) {
      callAI('开始游戏');
    }
  } else {
    callAI('开始游戏');
  }
}

// 页面关闭前自动存档
window.addEventListener('beforeunload', function() {
  localStorage.setItem('aiwenyou_save_1', JSON.stringify(gameState));
});

startGame();
```

### AI 输出格式约束

为了让前端能正确解析，开发者在编写文游指令时必须在指令末尾添加以下**输出格式要求**：

```
## 输出格式要求

为了达到最流畅的游玩体验，你的输出分为两部分：

### 第一部分：叙事文本（纯文字）

直接输出剧情文本，不要加 JSON 包裹，不要加引号。用 \n 表示换行。字数 300-500 字，包含环境描写、对话、事件推进。

### 第二部分：数据 JSON

叙事文本结束后，换行，然后输出：

---DATA---
{"stats":{"survival":数值,"combat":数值,"reputation":数值,"shadow":数值},"choices":["① 选项A —— 说明","② 选项B —— 说明","③ 选项C —— 说明"],"inventory":["物品1","物品2"],"flags":{"flag_name":true}}

要求：
- 前面必须有一行 ---DATA--- 作为分隔
- JSON 必须在一行内，不要格式化/换行
- stats 值域 0-100
- choices 至少 3 个，最多 5 个
```

### 前端解析逻辑（关键）

```
                流式 SSE 接收
                       │
              ┌─────────▼─────────┐
              │ 每收到 delta.content │
              │ 实时 append 到叙事面板 │  ← ★ 玩家立刻看到文字
              └─────────┬─────────┘
                       │
                   检测 content 首字符
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
      以 { 或 " 开头         纯叙事文本
      (旧JSON格式)          (新格式)
            │                     │
      ⏸️ 不显示，等结束     检测 ---DATA---
                                       │
                              ┌────────┴────────┐
                              ▼                 ▼
                           找到 ---DATA---    未找到
                           停止追加到显示     继续追加
                              │                 │
                              └────────┬────────┘
                                       │
                                  stream 结束
                                       │
                              ┌────────▼────────┐
                              │ parseStreamResponse() │
                              ├─ ---DATA--- → 截取前半段+解析后半段JSON
                              ├─ {narrative} → JSON.parse 整体
                              └─ 纯文本 → 兜底显示
                                       │
                              ┌────────▼────────┐
                              │ 更新 stats/choices │
                              │ 更新 inventory/flags│
                              └───────────────────┘
```

### parseStreamResponse() 完整三格式兼容逻辑

```javascript
function parseStreamResponse(fullContent) {
  var content = fullContent.trim();
  var result = { narrative: null, stats: null, choices: null, inventory: null, flags: null };

  // ① 先试 ---DATA--- 新格式（叙事文本 + 分隔符 + JSON）
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
    } catch(e) { /* JSON 部分解析失败，叙事仍有效 */ }
    return result;
  }

  // ② 再试旧 JSON 格式：{"narrative":"...", "stats":{...}}
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
      // JSON 解析失败 → 大括号正则兜底
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

  // ③ 兜底：纯文本（无结构化数据）
  result.narrative = content;
  return result;
}
```

### 流式阶段格式检测

```javascript
// 在 SSE 循环中检测格式类型
var isJsonFormat = false;

// 每收到 delta.content 累积到 fullContent 后：
var trimmed = fullContent.trim();
if (trimmed.charAt(0) === '{' || trimmed.charAt(0) === '"') {
  isJsonFormat = true;  // 旧 JSON 格式，不实时显示
}

// 非 JSON 格式且未到 ---DATA--- 才追加显示
if (!isJsonFormat && !dataSectionReached) {
  appendStreamText(delta.content);
}

// stream 结束后，旧 JSON 格式一次性显示
if (isJsonFormat && result.narrative) {
  storyText.textContent = result.narrative;
}
```

## 实战陷阱（踩坑记录，必须读）

### 陷阱 1：GAME_INSTRUCTION 中的反引号

**问题**：文游指令.md 里包含 markdown 代码块 \`\`\`，嵌入 HTML 时使用 JS 模板字面量（backtick string）`const GAME_INSTRUCTION = \`...\`;`，内部反引号没有转义 → 整个 JS 引擎语法错误，重置按钮、流式解析等全部失效。

**修复**：嵌入 GAME_INSTRUCTION 前，将所有内部反引号转义为 `\\``。

```javascript
// ❌ 错误：内部反引号导致模板提前关闭
const GI = `# 指令...\`\`\`json{...}\`\`\`...`;

// ✅ 正确：内部反引号全部转义
const GI = `# 指令...\`\`\`json{...}\`\`\`...`;
```

**自动转义脚本**（Node.js）：
```javascript
// 嵌入前对文游指令做反引号转义
var content = fs.readFileSync('文游指令.md', 'utf8');
var escaped = content.replace(/\`/g, '\\`');
// 然后把 escaped 嵌入 HTML 的 const GAME_INSTRUCTION = `...`; 中
```

### 陷阱 2：流式格式兼容

AI 可能输出两种格式，`parseStreamResponse()` 和流式阶段必须同时支持：

| AI 输出格式 | 流式过程 | stream 结束后 |
|:-----------|:---------|:--------------|
| **新格式** 叙事文本 → \n\n---DATA---\n{JSON} | ✅ 实时追加文字，检测到分隔符后停止 | 解析 JSON 更新 stats/choices |
| **旧格式** {"narrative":"...","stats":{...}} | ⏸️ 不显示（等全部完成） | 一次性显示 narrative |
| **纯文本** | ✅ 实时追加文字 | 兜底，提供默认 choices |

### 陷阱 3：重置游戏的 loading 状态锁

`resetGame()` 中必须在清理之前设置 `isLoading = false; hideLoading();`，否则 `callAI()` 的 `if (isLoading) return` 会阻拦新游戏启动。

## 验证清单

交付 HTML 前必须逐项检查：

```
□ 文件以 .html 结尾
□ <!DOCTYPE html> 文档开头
□ </html> 正确闭合
□ <meta charset="UTF-8">
□ 零外部 CDN/远程资源引用（除 API 调用外）
□ 所有 src/href 都是相对的或 data: URI
□ API_KEY 常量已正确嵌入（演示场景使用真实 key，注意勿提交到公开仓库）
□ API_ENDPOINT 配置正确（https://api.deepseek.com/v1/chat/completions）
□ MODEL 配置正确（deepseek-v4-flash）
□ stream: true 已设置，全程使用流式输出
□ GAME_INSTRUCTION 完整嵌入了文游指令.md 的全部内容
□ **GAME_INSTRUCTION 内部所有反引号已转义（`\``→ `\\``）** — 否则整个 JS 引擎不会执行
□ SSE 解析逻辑正确（ReadableStream → 分割行 → data: 前缀 → delta.content 累积）
□ 流式阶段有 `isJsonFormat` 检测（防 JSON 显示为乱码）
□ `parseStreamResponse()` 兼容三种格式：---DATA--- / {"narrative"} / 纯文本
□ JSON fallback 解析正常（大括号正则提取兜底）
□ 重置游戏按钮存在且 `resetGame()` 开头强制 `isLoading = false`
□ 文游指令.md 中包含明确的"输出格式要求"章节（补偿无 response_format）
□ JavaScript 控制台无报错
□ 双击 .html 文件可在浏览器打开
□ 页面加载后自动发起 API 调用（callAI('开始游戏')）
□ 选项按钮点击后触发 API 调用
□ 自由输入框提交后触发 API 调用
□ Loading 状态有视觉反馈（禁用按钮 + 提示文字）
□ 视觉风格匹配世界观调性
□ localStorage 读/写正常（含 messages 数组序列化）
□ 存档/读档功能正常
□ 在不同屏幕尺寸下显示正常
□ 复制文游指令功能正常
□ AbortController 已实现：全局 `currentAbortController` 在 `callAI()` 中创建并传入 `signal`
□ 取消按钮存在且点击后调用 `cancelAI()`
□ 超时机制：30 秒无响应自动断开，显示超时提示 + 重试按钮
□ 指数退避重试：最多 3 次，间隔 1s/2s/4s，重试前有状态提示
□ 流式叙事渐进渲染：SSE 期间 `delta.content` 实时追加到叙事面板
□ `requestAnimationFrame` 节流渲染：流式期间使用 raf 控制渲染频率
□ Typing Indicator 存在，AI 响应期间显示「🤔 正在思考…」
□ Loading 状态正确禁用所有交互控件，结束后恢复
□ `parseStreamResponse()` 无 `...` 占位符，三种格式完整实现
□ `resetGame()` 开头强制 `cancelAI()` 解除 loading 锁
□ `startGame()` 的 localStorage 恢复逻辑有 try-catch 兜底
```

## 纪律

1. **必须实时调 API** — 不准用预设场景查表模式。每次玩家操作必须调 DeepSeek API 动态生成
2. **必须验证** — 不验证 HTML 不准交付（按验证清单逐项检查）
3. **零外部依赖（除 API 外）** — 不加载 CDN 字体/图标/库，纯 HTML+CSS+JS
4. **代码简洁** — 核心逻辑控制在 500 行以内，注释清晰
5. **Fallback 处理** — 如果 API 调用失败，自动指数退避重试（最多 3 次，间隔 1s/2s/4s）；3 次均失败后显示重试按钮，玩家可手动重试
6. **不开新窗口** — 不弹出新窗口/新标签，所有交互在单页面内完成
7. **API key 安全** — 演示场景直接写入真实 key。注意不要将本文件或生成的 HTML 提交到公开仓库。
8. **GAME_INSTRUCTION 必须完整** — 文游指令全文嵌入，不要截断或改写
9. **GAME_INSTRUCTION 中的反引号必须转义** — 使用 `content.replace(/\`/g, '\\`')` 预处理后再嵌入模板字面量
10. **必须同时支持旧 JSON 格式和新 ---DATA--- 格式** — `parseStreamResponse()` 三种情况都要处理，流式阶段要用 `isJsonFormat` 检测
11. **AbortController 必须实现** — `callAI()` 每次创建新 `AbortController`，`cancelAI()` 提供取消能力
12. **必须实现超时兜底** — 30 秒无响应自动断开，显示提示 + 重试按钮
13. **必须实现指数退避重试** — 网络错误最多重试 3 次，间隔 1s/2s/4s
