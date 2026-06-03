# pop-novel-game v2 升级 — 任务分解

## Task 1: 创建 Spec 三文件
- 创建 `spec.md`（需求规格）
- 创建 `tasks.md`（任务分解）
- 创建 `checklist.md`（验证清单）
- **完成标准**：三文件齐全，内容覆盖 v2 升级所有维度

## Task 2: 修复 HTML产出规范.md 中 stream/response_format 不一致
- 移除第 69 行附近代码示例中的 `response_format: { type: 'json_object' }`
- 统一改为 `"stream": true`
- 在文末验证清单中新增"不包含 response_format"检查项
- 确保讲解文字与代码示例一致
- **依赖**: 无
- **完成标准**：全文搜索不到 `response_format` 字段，所有示例使用 `stream: true`

## Task 3: 实现 AbortController 取消机制（HTML产出规范）
- 在核心引擎框架中新增全局 `let currentAbortController = null;`
- `callAI()` 中每次创建新 `new AbortController()` 并挂载
- `fetch()` 的第二个参数传入 `{ signal: currentAbortController.signal }`
- 新增 `cancelAI()` 函数：`currentAbortController?.abort()`
- 新增 UI 取消按钮/逻辑
- abort 后 `isLoading = false; hideLoading();`
- **依赖**: Task 2
- **完成标准**：代码示例中包含完整的 AbortController 创建/挂载/取消/清理逻辑

## Task 4: 实现超时兜底机制（HTML产出规范）
- `callAI()` 中调用 `fetch` 之前启动 `setTimeout(fn, 30000)`
- 超时后调用 `abortController.abort()`
- 超时后在叙事面板显示"⏱️ AI 响应超时" + 重试按钮
- 超时变量全局化，可在正常结束时 clearTimeout
- **依赖**: Task 3
- **完成标准**：代码示例中包含超时定时器创建/清理/超时处理完整逻辑

## Task 5: 实现指数退避重试策略（HTML产出规范）
- `callAI()` 中包裹重试循环（最多 3 次）
- catch 块中判断：非 abort 错误则重试
- 每次重试间隔 1s/2s/4s（使用 `await sleep(delay)`）
- 重试前更新 UI 提示"正在重试 (第 N 次)…"
- 3 次均失败后显示最终错误 + 手动重试按钮
- **依赖**: Task 4
- **完成标准**：代码示例中包含完整的重试循环逻辑

## Task 6: 实现流式叙事渐进渲染（HTML产出规范）
- SSE 循环中每收到 `delta.content` 立即追加到 `storyText` 元素
- 追加前做格式检测：`isJsonFormat` / `dataSectionReached` 判断
- 非 JSON 且未到 `---DATA---` 的内容才追加
- 追加后调用 `scrollToBottom()`
- 使用 `requestAnimationFrame` 节流渲染
- **依赖**: Task 2
- **完成标准**：SSE 解析循环中包含完整的格式检测 + 渐进追加 + 滚动逻辑

## Task 7: 实现 Loading / Typing Indicator（HTML产出规范）
- 新增 Typing Indicator UI（`<div class="typing-indicator">🤔 正在思考…</div>`）
- `showLoading()` / `hideLoading()` 函数
- showLoading 时：显示 indicator + 禁用选项按钮 + 禁用输入框 + 显示取消按钮
- hideLoading 时：隐藏 indicator + 启用控件 + 隐藏取消按钮
- CSS 中添加弹跳点动画
- **依赖**: Task 6
- **完成标准**：代码示例中包含完整的 loading 状态管理函数 + UI 控件 + 样式

## Task 8: 升级 SKILL.md — 统一流式协议 + 新增 UX 规范
- 更新"API 交互协议"章节，移除所有 `response_format` 痕迹
- 在"HTML 功能模块参考"中新增 AbortController / 超时 / 重试 / Typing Indicator 的模块图
- 在"实战陷阱"中新增"超时与重试"章节
- 更新核心流程 SSE 解析图，加入渐进渲染描述
- **依赖**: Tasks 2-7
- **完成标准**：SKILL.md 中的 API 协议、模块参考、陷阱记录与 HTML产出规范.md 完全一致

## Task 9: 统一验证
- 全文搜索 `response_format`，确认已全部移除
- 确认 `parseStreamResponse()` 无 `...` 占位符
- 确认三份文档的一致性
- 确认 SKILL.md 更新日志已添加 v2.0.0 条目
- **依赖**: Tasks 2-8
- **完成标准**：checklist.md 中所有检查项通过

---

## Task Dependencies
- Task 1 无依赖
- Task 2 无依赖
- Task 3 依赖 Task 2
- Task 4 依赖 Task 3
- Task 5 依赖 Task 4
- Task 6 依赖 Task 2
- Task 7 依赖 Task 6
- Task 8 依赖 Tasks 2-7
- Task 9 依赖 Tasks 2-8

可以并行的任务：Task 2 与 Task 1 可以并行；Task 6 与 Tasks 3/4/5 可以并行（它们修改的是不同函数）。
