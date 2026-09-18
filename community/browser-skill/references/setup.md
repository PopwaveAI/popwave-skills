# 安装与排障

只在 `bsk --version` 失败、`bsk doctor` 报 `fail`、或扩展未连接时读本文件。装好并连上以后不要再读。

## 运行前提

| 运行项 | 支持情况 |
|:--|:--|
| 操作系统 | macOS（Apple Silicon 和 Intel）、Linux（x64 和 ARM64）、Windows x64 |
| 浏览器 | Chrome 和 Microsoft Edge；其他能加载 Chromium 扩展的浏览器通常可用；Firefox 计划中 |

两个本地组件：`bsk` CLI/daemon 和浏览器扩展。缺任何一半都跑不通。

## 先选连接方式

| 情况 | 走法 |
|:--|:--|
| Agent 和浏览器在同一台电脑 | 按下面四步做 |
| 远程，已有服务或配对链接 | Agent 侧装 CLI 和技能；浏览器侧只装扩展，用配对链接连 |
| 远程，服务端还没搭 | Agent 侧先做第一步和第二步，再搭服务端，然后查连接 |

## 第一步：装 bsk CLI

先跑 `bsk --version`。已有安装且版本旧，走本文件末尾的「更新」段。

macOS / Linux：

```sh
curl -fsSL https://raw.githubusercontent.com/Tencent/BrowserSkill/main/install.sh | sh
export PATH="${BSK_INSTALL_DIR:-$HOME/.local/bin}:$PATH"
bsk --version
```

Windows（PowerShell）：

```powershell
irm https://raw.githubusercontent.com/Tencent/BrowserSkill/main/install.ps1 | iex
bsk --version
```

- Unix 安装脚本改不了调用它的父 shell 的 PATH。后续每次 shell 调用都要重新 export，或直接用装好的绝对路径（默认 `~/.local/bin/bsk`，Windows 是 `~/.local/bin/bsk.exe`）。
- 正在运行的 Agent 可能仍拿着旧 PATH，新终端生效后也要重启 Agent 会话。

## 第二步：把技能装进目标 harness

- DeepSeek Harness（`dsh`）：装 npm 插件，它自带技能和原生 `browser_*` 工具，跳过 `bsk install-skill`。

  ```sh
  dsh plugin --profile web add @wxg-prc-cpg/browser-skill-dsh-plugin
  dsh --profile web
  ```

  插件不自动更新，升级用 `dsh plugin --profile web update @wxg-prc-cpg/browser-skill-dsh-plugin --latest`，升级后重启该 profile。
- 其他 harness：先列 ID 和安装路径，再显式指定。

  ```sh
  bsk install-skill --list --json
  bsk install-skill --harness cursor --json
  ```

  把 `cursor` 换成清单里的 ID。显式 `--harness` 在自动检测失败时也能装。`--yes` 不带 `--harness` 会装进所有检测到的 harness，且一个都没检测到时直接失败。
- 不在清单里的 harness：把官方的 `skill/SKILL.md` 拷进该 harness 的技能目录，命名为 `browser-skill/SKILL.md`。

装完检查结果和目标路径。已存在的文件默认跳过，要看是保留还是用 `--force` 覆盖回自带技能。`--force` 会覆盖现有文件。

## 第三步：跑 bsk doctor

```sh
bsk doctor
```

每条 `fail` 行都会给 hint，照 hint 改一次再重跑一次。新装完只有 `extension connected` 失败是正常的，去做第四步。

- 本地进程身份的 warning 不阻塞浏览器使用。
- `doctor` 通过不代表技能已装（未装显示 `N/A`），技能发现要单独验。
- 路径或权限失败时，用报告里的实际路径去查共享目录和沙盒访问规则，不要猜 `/home/<user>`，也不要删 daemon 文件。

## 第四步：连浏览器扩展

扩展由用户自己装，Agent 不代装：

| 浏览器 | 安装地址 |
|:--|:--|
| Chrome 及其他 Chromium 浏览器 | https://chromewebstore.google.com/detail/hhcmgoofomhgciiibhipgmgkgnoenaoi |
| Microsoft Edge | https://microsoftedge.microsoft.com/addons/detail/browserskill/emacgiaaaiojkkpkddmmdfhmokgmnikg |

- 本机：让用户打开扩展弹窗，打开连接开关，确认端口和本地 daemon 一致，等状态变成已连接。
- 远程：让用户在弹窗里选远程连接，粘贴配对链接并保存。

用户做完后，在 Agent 这台机器上再跑一次 `bsk doctor`。只装扩展或只生成链接都还没建立连接。

## 验证技能被发现与首次使用

确认目标 harness 能列出或调用 `browser-skill`。需要新会话或重启 profile 才能发现的，告诉用户怎么做，并在它真正加载前把这项标为待确认。

首次验证：让技能打开 `https://example.com` 并总结页面。

```sh
bsk session start --no-focus --json     # 记下 session id
bsk navigate https://example.com --session <id>
bsk observe --session <id>
bsk session stop <id>
```

读到页面内容并停掉会话，才算通过。

## 沙盒环境（每条命令后回收后台进程）

宿主侧保住 daemon，沙盒内用共享的 `BSK_HOME` 加 `BSK_AUTO_START=0` 连过去。

- 由用户在正常宿主终端里跑 `BSK_HOME=/绝对共享路径/bsk bsk daemon start`；或由宿主后台任务跑 `bsk daemon start --foreground`，用同一个 `BSK_HOME`。
- 沙盒内每条 `bsk` 命令都带上 `BSK_HOME=/绝对共享路径/bsk BSK_AUTO_START=0`。一次 shell 调用里的 `export` 不会留到下一次。
- 这个目录要双方都能访问，包括它里面的 IPC socket。固定用同一个专用目录，不要每个任务换一个。
- 起 daemon 前先 `bsk status --json` 看有没有现成的可用 daemon。权限错误或超时不等于 daemon 不存在。
- 起不来就让用户在宿主侧起，不要反复重试自动启动、不要猜 home 目录、不要删运行时文件、不要重启共享 daemon。

## 远程连接

服务端跑 Agent、本机跑浏览器：CLI 和 harness 装在服务器上，浏览器那台只需扩展，用内置鉴权服务或兼容网关配对。缺服务端访问权限或 TLS 前提条件时，直接说清缺什么，不要猜着连。

## 更新

```sh
bsk update --yes
```

- 更新前先结束进行中的浏览器任务。
- 这条命令会用默认启动设置重启正在跑的 daemon。若你是用安装脚本替换的二进制，任务结束后再跑 `bsk daemon restart`。
- 自定义端口、宿主托管的沙盒 daemon、远程服务器：在各自的地方先停 daemon，跑 `bsk update --yes --no-restart-daemon`，再用原来的参数和 `BSK_HOME` 起回去。
- Windows 报 staged update 时，等替换完成再查 `bsk --version`。
- 扩展从浏览器商店更新，商店版本可能落后 CLI 版本。用 `bsk --version` 和 `bsk status` 对齐 CLI、daemon、扩展三者版本，再跑 `bsk doctor`。
- 0.3.0 起，`--unattended`、`tab borrow --no-confirm`、`BSK_REQUEST_HELP=off` 不再能绕过确认或关掉求助，改用扩展里的两个开关，见 [命令与操作细则](operations.md)。
