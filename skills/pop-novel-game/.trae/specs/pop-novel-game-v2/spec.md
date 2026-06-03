# pop-novel-game v2 升级 — 产品需求文档

## Overview

对 pop-novel-game 技能进行一次完整性升级。核心方向：修复当前方法文档中 `stream: true` 与 `response_format: json_object` 不兼容的 bug，引入完整的流式输出 + 动态渲染 UX 设计（AbortController 取消、超时兜底、指数退避重试、动态叙事面板渐进渲染），统一三份方法文档的代码规范，并新增 Spec 三文件作为项目规范底座。

目标用户：pop 技能的使用者（小说作者/世界观创作者）及其所面对的终端玩家。

## Goals

- **G1** 修复方法文档中 `stream: true` 与 `response_format: json_object` 的互斥 bug，统一改为纯流式方案
- **G2** 新增 AbortController 机制，支持玩家在 AI 响应过程中取消请求
- **G3** 新增超时兜底（30 秒无响应自动断开 + 提示重试）
- **G4** 新增指数退避重试策略（最多 3 次，间隔 1s/2s/4s）
- **G5** 实现流式叙事文本渐进渲染：AI 边生成边显示到面板，不等完整响应
- **G6** 新增 loading 智能体"思考中"动画（Typing Indicator）
- **G7** 统一三份方法文档中的代码示例，消除不一致
- **G8** 创建 Spec 三文件（spec.md / tasks.md / checklist.md）作为项目规范底座

## Non-Goals (Out of Scope)

- 不修改 Phase A（资料解析协议）的 JSON 产出结构
- 不修改 Phase B（文游设计协议）的游戏框架设计方法论
- 不修改 SKILL.md 中的三段式核心流程
- 不引入外部依赖（零外部库原则不变）
- 不做真实 API 接入测试（文档级规范升级）

## Background & Context

### 当前架构

pop-novel-game 是 pop 技能体系中负责「小说世界观 → AI 文游」转化的技能。核心流程为三段式：
- Phase A：资料解析 → 结构化世界观 JSON
- Phase B：文游设计 → AI 主持指令
- Phase C：HTML 产出生成 → 交互式 HTML

HTML 产出依赖 DeepSeek API 的流式（`stream: true`）能力实现实时叙事生成。

### 当前问题

1. **方法文档代码不一致**：`方法/HTML产出规范.md` 第 69 行示例代码使用了 `response_format: { type: 'json_object' }`，而后文又使用了 `stream: true`。DeepSeek API 规定两者不可同时使用，现有文档会导致生成的 HTML 在流式模式下解析失败。
2. **缺少取消机制**：玩家无法取消正在生成的 AI 响应，导致误操作时需等待完整响应。
3. **缺少超时兜底**：API 可能因网络问题长时间无响应，无超时断开机制。
4. **缺少重试策略**：网络错误后玩家需手动重试，体验差。
5. **流式渲染不完整**：代码模板中的 `parseStreamResponse()` 有 `...` 占位符未完整实现。

## Functional Requirements

### FR-1: 统一流式协议
所有代码示例统一使用 `stream: true`，彻底移除 `response_format: json_object`。AI 输出格式约束改为由文游指令（system prompt）中的"输出格式要求"章节保证。

### FR-2: AbortController 取消机制
在 `callAI()` 中创建 `AbortController` 实例，挂载到全局 `currentAbortController`。提供 `cancelAI()` 函数，外部可随时取消正在进行的 API 请求。调用取消时自动恢复 UI 交互状态。

### FR-3: 超时兜底
`callAI()` 内部设置 30 秒超时定时器。超时后自动调用 `abortController.abort()`，在叙事面板显示"⏱️ AI 响应超时，请重试"，并提供重试按钮。

### FR-4: 指数退避重试
API 网络错误时自动重试，最多 3 次。重试间隔依次为 1 秒、2 秒、4 秒。每次重试前在面板状态栏提示"正在重试 (第 N 次)…"。3 次均失败后显示最终错误信息 + 重试按钮。

### FR-5: 流式叙事渐进渲染
SSE 流中每收到一个 `delta.content`，立即追加到叙事面板显示区域，不等完整流结束。流式阶段同时做格式检测：
- 若内容以 `{` 或 `"` 开头（旧 JSON 格式），暂停追加，等流结束后一次性显示
- 检测到 `---DATA---` 分隔符后，停止追加（数据部分不显示给玩家）
- 流结束后用 `parseStreamResponse()` 解析完整内容

### FR-6: Loading 状态与 Typing Indicator
AI 响应期间显示「🤔 正在思考…」的 Typing Indicator 动画，禁用所有输入控件（选项按钮 + 自由输入框）。响应结束后恢复控件可用状态。

### FR-7: 动态叙事面板
叙事面板支持自动滚动到底部。使用 `requestAnimationFrame` 节流渲染，避免大量 delta 块导致的性能抖动。

## Non-Functional Requirements

- **NFR-1** 代码模板中的核心逻辑行数不超过 600 行
- **NFR-2** 所有示例代码具有可直接复制使用的完整性（无 `...` 占位符）
- **NFR-3** 零外部依赖原则不变
- **NFR-4** 与现有 HTML 输出兼容，存量 HTML 无需修改即可继续使用

## Constraints

- 所有代码示例必须使用纯 JavaScript（ES6+），无 TypeScript / 框架
- 所有 CSS 必须内联在 HTML 中
- API 协议必须兼容 DeepSeek Chat Completions API

## Assumptions

- 浏览器环境支持 `ReadableStream`、`AbortController`、`fetch`（现代浏览器均支持）
- API key 演示场景直接嵌入（安全警告已在 SKILL.md 中标注）
- `localStorage` 可用且容量足够（< 5MB）

## Acceptance Criteria

### AC-1: stream: true 统一
**Given** 读者查看 HTML 产出规范中的 API 调用示例  
**When** 检查 `body` 中的参数  
**Then** 所有示例都使用 `"stream": true`，不存在 `response_format` 字段  
**Verification**: programmatic

### AC-2: AbortController 可用
**Given** 玩家在 AI 响应过程中点击取消按钮  
**When** `abort()` 被调用  
**Then** fetch 请求被中断，UI 恢复交互状态，叙事面板没有残留内容  
**Verification**: programmatic

### AC-3: 超时自动断开
**Given** API 超过 30 秒未返回任何数据  
**When** 超时定时器触发  
**Then** 自动调用 `abortController.abort()`，显示超时提示 + 重试按钮  
**Verification**: programmatic

### AC-4: 指数退避重试
**Given** 网络请求失败（非 abort 导致的失败）  
**When** 重试逻辑执行  
**Then** 依次间隔 1s/2s/4s 重试，最多 3 次，每次有状态提示  
**Verification**: programmatic

### AC-5: 叙事文本渐进渲染
**Given** AI 响应以流式返回叙事文本  
**When** SSE 每收到一个 `delta.content`  
**Then** 内容立即追加到叙事面板（非 JSON 格式且未到 `---DATA---`）  
**Verification**: programmatic

### AC-6: 解析函数完整实现
**Given** 查看 `parseStreamResponse()` 函数  
**When** 逐行阅读  
**Then** 所有三种格式（`---DATA---` / `{"narrative"}` / 纯文本）均有完整实现，无 `...` 占位符  
**Verification**: human-judgment

## Open Questions

- 是否需要引入 SSE 心跳检测？当前通过超时机制兜底，暂不引入
- 30 秒超时是否合适？可根据实际 API 延迟情况在后续迭代中调整
