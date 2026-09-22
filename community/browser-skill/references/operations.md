# 命令与操作细则

在做浏览器任务、或要确认某条命令的参数形式时读本文件。

## 命令清单（完整）

```text
session start|stop|list   browsers   status   doctor   update   logs
navigate   navigate-back   navigate-forward   reload   wait-for-navigation   wait-ms
observe   snapshot   get-html   screenshot   console   network
click   hover   wheel   scroll-to   focus   blur   fill   select   press   evaluate
tab list|create|close|select|borrow|return   window resize   emulate
upload   download   request-help   record start|stop
```

清单以外的命令一律不要自己发明。参数用 `bsk <命令...> --help` 查，不要猜。

容易写错的参数形式：

```text
bsk fill <ref> --value <文本>          bsk select <ref> --value <选项值>
bsk screenshot --out <路径>            bsk emulate --device <设备预设id>
bsk upload <ref> --file <路径>         bsk download <ref> --out <路径>
```

- `select` 匹配选项的 `value` 属性，不是可见文字。
- 设备预设 id 是小写连字符形式，例如 `iphone-14`。
- `console` 和 `network` 只给有界、只读的调试证据。
- `emulate` 把视口、UA、触摸覆盖到单个标签页，新标签页不继承；用 `--off` 恢复真实环境。
- `evaluate` 是最后手段：`observe` 加正常交互做不成时才用。带 `--json` 时看 `.ok`，JavaScript 抛异常也可能因为 RPC 成功而返回退出码 0。任何情况下不许用它读存储、cookie、鉴权数据。
- `record` 录制用户操作供回放。用前先读 `bsk record start --help`；银行、SSO、密码管理器等敏感页面一律不录。

## 观测与元素引用

- `scroll-to <ref或选择器>` 把元素及其所在 frame 滚进可视区。结果给的是顶层视口 CSS 像素下、经祖先裁剪后的可见 border-box 范围。
- 部分可见算成功；隐藏或完全被裁剪的目标会以 `permission_denied` 加 `data.reason=element_not_visible` 失败。它不检测是否被其他元素遮挡。
- 指定标签页或等待上限：`bsk scroll-to @e3 --session <id> --tab-id 42 --timeout 5s`。
- `wheel --delta-y -120` 在视口中心发送原生滚轮输入；可加 ref 或选择器（会先滚进可视区）。两个轴接受带符号数字，默认都是零，至少一个非零。结果回显的是输入，不是实际滚动距离，之后要 observe 看页面反应。
- `focus <ref>` 主动聚焦，`blur <ref>` 取消聚焦并报告原本是否聚焦。焦点触发的界面状态用这两个。
- 优先用新的 `@eN` ref，少用 CSS 选择器。CSS 选择器只搜主文档；iframe 和 shadow root 内的目标要用新 ref。
- 观测会把纯悬停才出现的表面标成 `@e1 button "Products" [hover first: Shoes | Bags]`。列出的只是标签名，不是可用 ref：先 hover 触发器，再 observe，然后点展开项自己的 ref。不要点触发器本身，除非用户要的就是触发器动作。`[has-submenu]` 和 `[expanded]` 标的是同类触发器，同样不列出隐藏项。
- `observe` 不会自己悬停页面。确认预期存在却缺失、又没有 marker 指向触发器时，用一次 `--probe-hover`：这正是纯 CSS 悬停菜单在此处的样子。它会悬停一批可能的触发器，花几秒并触碰真实页面；已知是哪个元素藏着菜单后，`bsk hover <ref>` 更省更准。

读页升级顺序，按需往上走：

1. `observe`：常规语义理解、文本、控件和 ref。
2. `observe --probe-hover`：预期控件缺失且无 marker 时用一次。
3. `snapshot`：需要更严格的静态无障碍树时。
4. `get-html`：需要精确标记或语义视图给不出的隐藏元数据时。
5. `screenshot`：需要版式、样式、canvas、图片或视觉证据时。

不要为了找普通控件就先抓原始 HTML 或截图。需要交互时，先用观测拿到新 ref 再动手。

## Canvas 与观测续读

- `observe` 可能在相关控件附近放 `@eN canvas [visual:screenshot]`。名字是可选的，不要从相邻标签推断 canvas 里的表格标题或控件。
- 视觉 ref 支持 `screenshot --ref`；按点点击还需要它的 `capture_id` 和图像坐标。视觉 ref 不支持 fill、hover 或取 HTML。
- 首次 observe 返回的是文字不是图。用周边语义判断要不要截 canvas。
- 当前会话收不到也看不懂图片时，告诉用户 canvas 内容无法解读，请切换到支持图像的模型，同时继续用已有语义信息推进。
- 默认不设 token 上限。显式给 `--max-tokens` 时，观测可能返回 `next_cursor` 和 `@more`。继续读要先用当前 ref，再 `bsk observe --cursor <token> --session <id>`：每次响应都会替换 ref 表，上一页的 ref 不能再用。内容还没读完就顺着 cursor 读，不要反复读同一段开头。
- 续读读的是同一份已捕获的观测，不刷新、不悬停页面。不要和改深度或悬停探测混用。新的 observe 或 snapshot 会替换续读；页面身份变了就重新 observe。
- 截图执行时会核对当前目标身份和几何，允许 canvas 重绘，但不冻结像素。
- canvas 截图可能返回 `capture_id`。要点击图里认出的点，用 `bsk click eN --capture <id> --image-x <x> --image-y <y> --session <id>`，坐标用原始 PNG 像素（返回的宽高），不是缩放后的显示坐标或视口坐标。
- capture 一次性有效，两分钟后失效，被同一 ref 的新截图或新的观测、续读取代也会失效。遇到 `capture_unavailable`，看图但要点就重新 observe 加 screenshot。点击次数 1/2、按键和修饰键都支持。
- 点完要 observe 或截图确认结果，展开出来的控件用 DOM ref。点击执行成功不等于业务成功。canvas 重绘允许，但身份、几何或命中目标变了会被拒。`effect_state=unknown` 时先查清再换新 capture 重试。不要从可按点点击推断出支持单元格编辑、输入法、拖拽或悬停。

## 自动化开关（用户在扩展弹窗里设置）

| 借用前确认 | 允许请求人工协助 | 实际行为 |
|:--|:--|:--|
| 开 | 开 | 借用需要确认；求助正常弹窗 |
| 开 | 关 | 借用需要确认；求助返回 disabled |
| 关 | 开 | 借用免确认；求助正常弹窗 |
| 关 | 关 | 借用免确认；求助返回 disabled |

- 用户在扩展里保存的设置对所有会话有最终决定权，对已有会话和新建会话都生效。
- 关掉借用确认会放行待确认的请求；关掉协助会把等待中的求助结束为 `disabled`。重开开关后，后续操作恢复对应行为，包括用旧参数 `--unattended` 建的会话。
- 已完成的借用不会撤销，已结束的求助不会重新弹出。
- 允许协助只代表 `request-help` 可用，不代表每个浏览器操作都要先请求许可。任务授权和宿主审批仍然有效。
- `session start --json` 和 `session list --json` 返回浏览器实际的 `interaction` 策略。
- 偏好读取失败时，后台保留已有有效值；还没有有效值时按两项都开处理，不回写默认值，也不阻止新建会话。浏览器未连接时返回连接错误，不会根据命令行参数或环境变量在本地伪造成 `disabled`。

## 标签借用

- 常规页面写入只影响 Agent Window 的标签页。要操作用户的标签页，先 `bsk tab list --scope user --session <id>`，再 `bsk tab borrow <tab-id>`。
- 相关步骤做完立刻 `bsk tab return <tab-id>`。停会话时也会归还借用的标签页。
- 不编造 tab id，不把个人标签页跨不相关的任务一直占着。
- `tab borrow --timeout 120s` 只改确认等待时长（默认 60s），不决定是否需要确认。自定义等待需要 daemon 和扩展都支持协议 1.2 以上。
- 同一会话里重复请求已完成的借用会返回原有结果。挂起的、被拒的、确认超时的请求都不要重复请求，也不要换别的浏览器工具绕过。`reason` 是 `borrow_outcome_unknown` 时，先查标签页和会话状态，标签页可能已经移过去了。

## 人工求助

- 协助开启时（默认），登录、验证码、OTP、支付确认、同意或其他只能由人完成的步骤用 `bsk request-help`。提示写准，能指具体控件就带新的 `--target` ref 或选择器。只有页面有明确稳定的成功信号时才用完成判据。
- `outcome` 取值 `continued`、`completed`、`cancelled`、`timed_out`、`disabled`（`navigated` 已废弃，永远不要当成完成信号）。
- 人工接手后，只有 `continued` 或 `completed` 才继续。`cancelled` 视为拒绝，`timed_out` 视为受阻，这两个不要重复发起。控制权回来后先 observe 再用 ref。
- 协助被关掉时，不要调 `request-help`。若仍收到 `disabled`，说明没有任何人工动作被确认：重新 observe 继续推进，不要仅因为求助不可用就把步骤判为受阻。
- 关掉协助不增加任何授权，任务授权和宿主限制照旧。
- 用当前页面、已有登录态、已授权的凭据或验证码完成当前步骤。任务授权和宿主规则允许时，有图像理解能力的模型可以截图并尝试图形验证。手机扫码、人脸验证、拿不到的短信验证码可能仍然受阻；纯文本模型也可能解不了纯图验证码。
- 一次尝试失败后重新 observe，换可行路径再试。不要在同一失败上循环，也不要重复一个结果未知的动作。只有缺必需信息或能力、或可行路径都用尽时才报受阻，同时继续做能独立完成的部分。不要为了绕开这些限制去重开协助开关或换浏览器后端。

## 截图

```sh
bsk screenshot --session <id> --out viewport.png
bsk screenshot --session <id> --ref @e3 --out element.png
bsk screenshot --session <id> --full-page --out page.png
bsk screenshot --session <id> --full-page --timeout 5m --out page.png
```

- 不带 `--ref` 也不带 `--full-page` 时只截可见视口。`--full-page` 与 `--ref` 互斥。
- 整页模式从页顶滚到页底，跟随滚动中加载的内容，结束后恢复原始位置和样式。
- 整页截图属于页面输入：用 Agent Window 里已选中、受会话控制的标签页（先新建或借用），保持视口稳定，尊重用户中断。`--tab-id` 指定标签页但不选中它。
- Chrome 内部页、扩展商店、嵌套滚动容器和虚拟列表不支持自动整页。
- 默认采集与编码超时两分钟，长页面加 `--timeout 5m`。支持 Ctrl-C 取消，结束后恢复原始滚动位置。
