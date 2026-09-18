---
name: browser-skill
description: "用 bsk CLI 驱动用户已登录的 Chromium 浏览器：打开并读取页面、填表点击、走完流程、抓取数据、验证已部署页面、整页长截图。含首次安装配置与排障步骤。当用户要操作自己已登录的网站，或需要整页长截图时使用。"
version: "1.0.0"
author: "Popwave"
---

# 浏览器操控（BrowserSkill）

用 `bsk` 命令驱动用户真实的 Chromium 浏览器。自动化跑在独立的 Agent Window 里，复用用户已有的登录态和 cookie，用户自己的窗口不受影响。

## 什么时候用

- 用户要打开、读取、总结某个网页。
- 用户要在自己已登录的网站上填表、点击、走完一段流程、抓取列表或表格数据。
- 用户要验证一个已部署页面的表现，或回归验证某个改动的界面。
- 用户要整页长截图。

以下情况不要用：任务里没有浏览器；用户只要一份安装说明（直接给步骤，不跑任务）；用户要自己从扩展商店装扩展（这步只能用户点）。

## 三条铁律

1. 不提取凭据、cookie、token 或任何密钥。`evaluate` 不许碰登录态、浏览器存储、鉴权数据。
2. 不用 `sudo` 安装或提权。浏览器扩展由用户自己在扩展商店安装。
3. 没读到页面就不许报成功。报成功要给读到的页面内容或截图路径。

## 先判断装没装

按顺序判一次，命中就往下走：

- `bsk --version` 有版本号：CLI 已就绪，跳到「任务生命周期」。
- 命令找不到：读 [安装与排障](references/setup.md) 走安装。
- `bsk doctor` 有 `fail` 行：读 [安装与排障](references/setup.md) 的排障段，按 hint 修一次再重跑。
- `bsk doctor` 只有 `extension connected` 失败：让用户装扩展并确认连上，见 [安装与排障](references/setup.md)。

`doctor` 通过不代表技能已装（未装会显示 `N/A`），技能发现要单独验。

## 任务生命周期

每个浏览器任务独占一个有界会话，三步固定：

```text
1. bsk session start --json          # 记下返回的 session id
2. bsk <命令> --session <id>         # 会话内每条命令都带这个 id
3. bsk session stop <id>             # 成功路径和报错路径都要跑
```

- 目标达成就立刻停会话，不要靠空闲超时清理。
- 清理动作是 `bsk session stop`，不是 `bsk daemon stop` 或 `daemon restart`。daemon 要常驻复用。
- 接了多个浏览器时先 `bsk browsers`，再用 `bsk session start --browser <id或标签>` 指定。
- 不需要抢用户焦点时，在 start 那条命令上加 `--no-focus`。它不是其他命令的参数。

## 观测、操作、再观测

默认循环：

```text
bsk navigate <url> --session <id>
bsk observe --session <id>
bsk click|fill|select|press ... --session <id>
bsk observe --session <id>          # 导航后或 DOM 有明显变化后
```

- 优先用新取到的 `@eN` ref。导航会让 ref 失效，DOM 大改也可能让 ref 过期；下一次操作前重新 observe。
- 读页按需升级，不要一上来就抓 HTML 或截图：`observe` → 预期控件缺失且没有 marker 提示时用一次 `observe --probe-hover` → `snapshot` → `get-html` → `screenshot`。
- 成功可见后不要再点击、刷新、跳转、切标签或做多余检查。
- 悬停菜单的观测只给标签名不给可用 ref：先 hover 触发器，再 observe，然后点展开项自己的 ref。
- 只从命令清单里选命令，不要自己发明；参数用 `bsk <命令> --help` 查，不要猜。

命令清单、易错参数形式与细则见 [命令与操作细则](references/operations.md)。

## 操作用户标签页要先借用

```text
bsk tab list --scope user --session <id>
bsk tab borrow <tab-id> --session <id>
bsk tab return <tab-id> --session <id>    # 相关步骤做完立刻还
```

- 不编造 tab id，不把用户的标签页跨任务长期占用。
- 借用是否需要确认，由扩展里保存的「借用前确认」开关决定。`--timeout` 只改确认等待时长（默认 60s），不决定是否需要确认。
- 已完成的借用重复请求会返回原结果；挂起、被拒、超时的请求不要重试，也不要换别的浏览器工具绕过。

## 需要人出手时

登录、验证码、短信验证码、支付确认、同意弹窗这类只有人能做的步骤，用 `bsk request-help`，给准确提示，能指控件就带 `--target`。

| outcome | 处理 |
|:--|:--|
| `continued` / `completed` | 继续。控制权回来后先 observe 再操作 |
| `cancelled` | 视为用户拒绝，不重复发起 |
| `timed_out` | 视为受阻，不重复发起 |
| `disabled` | 没人接手。重新 observe，用现有登录态和已授权输入继续自主完成 |

扩展里关掉「允许请求人工协助」时，不要调 `request-help`，也不要改开关或换浏览器后端绕过。`disabled` 只说明没人接手，不代表任务完成或受阻。

## 长截图

```sh
bsk screenshot --session <id> --full-page --out page.png
bsk screenshot --session <id> --full-page --timeout 5m --out page.png
```

- 不带 `--ref` 也不带 `--full-page` 时只截视口；`--full-page` 与 `--ref` 互斥。
- 整页截图会滚动页面：用 Agent Window 里受会话控制的标签页，保持视口稳定，尊重用户中断。
- 默认采集与编码超时两分钟，长页面加 `--timeout 5m`。支持 Ctrl-C 取消，结束后恢复原始滚动位置。
- Chrome 内部页、扩展商店、嵌套滚动容器和虚拟列表不支持自动整页。

## 汇报

- 成功：一句话说清读了哪个页面、完成了哪一步，有截图就附路径，并确认会话已停。
- 受阻：说清哪部分已就绪、哪步没验证、缺什么才能继续。没验证的步骤不许说成完成。

---

来源：本技能按腾讯 [BrowserSkill](https://github.com/Tencent/BrowserSkill)（MIT 协议）的官方说明整理。运行时自带的 `browser-skill` 技能由 `bsk install-skill` 管理并自动更新，与本包各自独立。
