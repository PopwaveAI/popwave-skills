# 13-pop-novel-game v2 升级 — 验证清单

## 文档完整性验证
- [ ] Check 1: `.trae/specs/13-pop-novel-game-v2/spec.md` 存在且内容完整
- [ ] Check 2: `.trae/specs/13-pop-novel-game-v2/tasks.md` 存在且任务分解合理
- [ ] Check 3: `.trae/specs/13-pop-novel-game-v2/checklist.md` 存在且检查项可判定
- [ ] Check 4: 三文件中 spec/AC 与 checklist 检查项有一一映射关系

## stream/response_format 修复验证
- [ ] Check 5: `方法/HTML产出规范.md` 全文不存在 `response_format` 字段
- [ ] Check 6: `方法/HTML产出规范.md` 中所有 API 调用示例使用 `"stream": true`
- [ ] Check 7: `方法/HTML产出规范.md` 中所有包含 API body 的代码块已统一
- [ ] Check 8: `SKILL.md` 全文不存在 `response_format` 字段
- [ ] Check 9: `SKILL.md` 中"注意：stream: true 后无法同时使用 response_format"的表述已移除或变为纯流式说明

## AbortController 取消机制验证
- [ ] Check 10: `方法/HTML产出规范.md` 核心引擎中包含 `let currentAbortController = null;`
- [ ] Check 11: `callAI()` 函数中包含 `new AbortController()` 创建与挂载
- [ ] Check 12: `fetch()` 的 options 中包含 `signal` 参数
- [ ] Check 13: 存在 `cancelAI()` 函数，调用后正确清理状态
- [ ] Check 14: abort 后 `isLoading` 被正确重置为 `false`

## 超时兜底验证
- [ ] Check 15: `callAI()` 中包含 30 秒超时定时器
- [ ] Check 16: 超时后调用 `abortController.abort()`
- [ ] Check 17: 超时后在叙事面板显示提示文字 + 重试按钮
- [ ] Check 18: 正常结束时清理超时定时器

## 指数退避重试验证
- [ ] Check 19: `callAI()` 中包含重试循环（最多 3 次）
- [ ] Check 20: 重试间隔依次为 1s/2s/4s
- [ ] Check 21: 重试前有 UI 状态提示"正在重试 (第 N 次)…"
- [ ] Check 22: 3 次失败后有最终错误信息 + 手动重试按钮
- [ ] Check 23: abort 导致的错误不触发重试

## 流式叙事渐进渲染验证
- [ ] Check 24: SSE 循环中每收到 `delta.content` 立即追加到叙事面板
- [ ] Check 25: 追加前有 `isJsonFormat` 格式检测
- [ ] Check 26: 检测到 `---DATA---` 后停止追加
- [ ] Check 27: 追加后自动滚动到底部
- [ ] Check 28: 使用 `requestAnimationFrame` 节流

## 解析函数完整性验证
- [ ] Check 29: `parseStreamResponse()` 无 `...` 占位符
- [ ] Check 30: 兼容三种格式：`---DATA---` / `{"narrative"}` / 纯文本
- [ ] Check 31: JSON 解析失败时有正则大括号兜底

## Loading / Typing Indicator 验证
- [ ] Check 32: 存在 Typing Indicator UI 元素和 CSS 样式
- [ ] Check 33: `showLoading()` 显示 indicator + 禁用控件 + 显示取消按钮
- [ ] Check 34: `hideLoading()` 隐藏 indicator + 启用控件 + 隐藏取消按钮
- [ ] Check 35: CSS 中有弹跳点动画

## SKILL.md 升级验证
- [ ] Check 36: SKILL.md 更新日志新增 v2.0.0 条目
- [ ] Check 37: SKILL.md API 交互协议与 HTML产出规范.md 一致
- [ ] Check 38: SKILL.md 新增了 AbortController/超时/重试的模块参考图
- [ ] Check 39: SKILL.md 新增了 Typing Indicator 的模块参考

## 整体质量验证
- [ ] Check 40: 所有代码示例可直接复制使用，无 `...` 占位符
- [ ] Check 41: 三份方法文档之间无矛盾/不一致
- [ ] Check 42: `startGame()` 存档恢复使用 `parseStreamResponse()` 而非 `JSON.parse()`，try-catch 兜底
- [ ] Check 43: `renderStats()` 无未使用的变量
- [ ] Check 44: `showLoading()` 禁用了 `.retry-btn`
- [ ] Check 45: `renderChoices()` 含"重开"/"重新开始"关键字守卫（调用 resetGame 而非 callAI）
- [ ] Check 46: 网络错误提示含 CORS 解决方案（python3 -m http.server）
- [ ] Check 47: `resetGame()` 通过 `cancelAI()` 解除 loading 锁，无冗余代码
- [ ] Check 48: 零外部依赖原则在所有文档中一致
