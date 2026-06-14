/**
 * qa/kimi-client.js — Kimi K2.5 API 客户端
 *
 * 职责：给一个 base64 图片 + 评估 Prompt → 返回 Kimi 的视觉分析文本
 *
 * 用法：
 *   const { analyzeImage } = require('./kimi-client.js');
 *   const result = await analyzeImage(base64String, 'image/jpeg');
 *   console.log(result.text);
 */

// ─── Kimi API 配置 ─────────────────────────────────────────
const QA_CONFIG = {
  API_KEY: process.env.KIMI_API_KEY || '',
  BASE_URL: 'https://api.moonshot.cn/v1',
  MODEL: 'kimi-k2.5',
  TIMEOUT: 120000,
  SCREENSHOT: { fullPage: true, type: 'jpeg', quality: 85 },
  QA_PROMPT: `你是一个专业的 HTML 视觉设计师。我会给你一张 HTML 页面的截图，请严格评估。

## 第一部分：文字分析（供人阅读）
从以下维度逐项简短分析，先给总体评分（1-10分）：

1. **整体布局与结构** — 布局是否合理？有无溢出/不对齐？间距一致性？
2. **文字可读性** — 字号是否合适？对比度是否足够？
3. **色彩与风格** — 配色是否协调？是否有高级感？
4. **内容密度** — 信息密度合理？拥挤还是稀疏？
5. **改进建议** — 按优先级列出最多3条可操作的CSS/布局修改建议。

## 第二部分：修复指令（供主 Agent 自动执行）

请在你回复的最后，输出一个 JSON 块，格式如下。这个 JSON 是给另一个 AI（DeepSeek）读的，它需要知道**改哪个文件、改哪个选择器、改成什么值**。

\`\`\`json
{
  "patches": [
    {
      "priority": "P0/P1/P2",
      "type": "layout|typography|color|density|interaction",
      "skeleton_id": "骨架ID（如 abyss/dossier/social 等）",
      "selector": "CSS选择器字符串",
      "issue": "问题描述（简洁的一句话）",
      "cssOverrides": {
        "属性名": "属性值"
      },
      "reason": "为什么要这样改"
    }
  ]
}
\`\`\`

### 规则：
- **P0** = 严重影响可读性或功能，必须修
- **P1** = 影响体验但可用，建议修
- **P2** = 锦上添花，可修可不修
- 每个 patches 条目必须有明确的 **selector** 和 **cssOverrides**
- cssOverrides 中只列出要覆盖的属性，不要写完整样式
- **skeleton_id** 从以下选择：abyss, purple-orb, dossier, social, xianxia-sect, family-tree, card-deck, status-board, narrative, canvas-map, galaxy, d3-galaxy
- 如果没有发现问题，patches 可以为空数组

我的最终目标是：这个 HTML 是小说世界观/角色/剧情的视觉化展示，
应该让读者一眼就被吸引，愿意深入阅读。`,
};

/**
 * 发送一张截图给 Kimi K2.5 做视觉分析
 */
async function analyzeImage(base64Image, mimeType, customPrompt, opts = {}) {
  const {
    timeout = QA_CONFIG.TIMEOUT,
    model = QA_CONFIG.MODEL,
  } = opts;

  const imageUrl = `data:${mimeType};base64,${base64Image}`;
  const prompt = customPrompt || QA_CONFIG.QA_PROMPT;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(`${QA_CONFIG.BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${QA_CONFIG.API_KEY}`,
      },
      body: JSON.stringify({
        model,
        messages: [
          {
            role: 'system',
            content: '你是 Kimi，由 Moonshot AI 提供的人工智能助手。你擅长视觉设计评估，能够从截图分析 HTML 页面的视觉质量并给出改进建议。',
          },
          {
            role: 'user',
            content: [
              { type: 'image_url', image_url: { url: imageUrl } },
              { type: 'text', text: prompt },
            ],
          },
        ],
        // kimi-k2.5 强制 temperature=1.0（思考模式），不可手动指定
        // 参考：https://platform.moonshot.cn/docs/guide/use-kimi-vision-model
        max_tokens: 4096,
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const errorBody = await response.text().catch(() => '');
      throw new Error(`Kimi API 错误 ${response.status}: ${errorBody.slice(0, 200)}`);
    }

    const data = await response.json();
    const text = data.choices?.[0]?.message?.content || '';
    const usage = data.usage || {};

    // 尝试从回复中提取评分
    let score = null;
    const scoreMatch = text.match(/(\d+)(?:\s*\/\s*10|分)/);
    if (scoreMatch) score = parseInt(scoreMatch[1], 10);

    return { text, score, usage, model };

  } finally {
    clearTimeout(timer);
  }
}

async function analyzeBatch(images, onProgress) {
  const results = [];
  for (let i = 0; i < images.length; i++) {
    const img = images[i];
    if (onProgress) onProgress(i + 1, images.length, img.htmlPath);

    const result = await analyzeImage(img.base64, img.mimeType);
    results.push({
      htmlPath: img.htmlPath,
      skeletonId: img.skeletonId,
      text: result.text,
      score: result.score,
      usage: result.usage,
      model: result.model,
    });

    // 为避免限流，每轮间隔 2 秒
    if (i < images.length - 1) {
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  return results;
}

module.exports = { analyzeImage, analyzeBatch, QA_CONFIG };
