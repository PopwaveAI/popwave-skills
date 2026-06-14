# Cursor Remote SSH 断线修复方案

## 问题现象

使用 Cursor 通过 Remote SSH 连接远程服务器时，频繁出现 "taking longer than expected" 提示，随后连接断开，需要手动重连。尤其在空闲一段时间后更容易发生。

## 根本原因

- SSH 连接在空闲时被中间网络设备（路由器/防火墙/NAT）超时断开
- Cursor 的默认 SSH 超时和重连配置不够积极
- 没有 keep-alive 心跳包来维持连接活跃

---

## 修复步骤

### 第一步：修改 SSH 客户端配置

编辑文件 `~/.ssh/config`（Windows 路径为 `C:\Users\你的用户名\.ssh\config`），在文件最顶部添加：

```
# Global SSH keep-alive settings for Cursor
Host *
    ServerAliveInterval 15
    ServerAliveCountMax 3
    TCPKeepAlive yes
    ConnectionAttempts 3
    ConnectTimeout 10
```

#### 参数说明

| 参数 | 值 | 作用 |
|------|-----|------|
| ServerAliveInterval | 15 | 每 15 秒发送一个心跳包，防止连接被中间设备断开 |
| ServerAliveCountMax | 3 | 连续 3 次心跳无响应才判定断线（即 45 秒无响应） |
| TCPKeepAlive | yes | 启用 TCP 层面的 keep-alive |
| ConnectionAttempts | 3 | 连接失败时自动重试 3 次 |
| ConnectTimeout | 10 | 单次连接超时 10 秒（更快发现连接问题） |

---

### 第二步：修改 Cursor 设置

打开 Cursor 的 settings.json（快捷键 `Ctrl+Shift+P` → 搜索 "Open User Settings JSON"），添加以下配置：

```json
{
    "remote.SSH.connectTimeout": 30,
    "remote.SSH.maxReconnectionAttempts": 10,
    "remote.SSH.useLocalServer": true,
    "remote.SSH.showLoginTerminal": true,
    "remote.SSH.enableDynamicForwarding": false
}
```

#### 参数说明

| 参数 | 值 | 作用 |
|------|-----|------|
| remote.SSH.connectTimeout | 30 | SSH 连接超时设为 30 秒，比默认值更快检测到断线 |
| remote.SSH.maxReconnectionAttempts | 10 | 断线后自动重连最多 10 次 |
| remote.SSH.useLocalServer | true | 使用本地服务器模式，减少对远程连接的依赖 |
| remote.SSH.showLoginTerminal | true | 显示登录终端，方便排查连接问题 |
| remote.SSH.enableDynamicForwarding | false | 关闭动态转发，减少连接复杂度和潜在的超时点 |

---

### 第三步（可选）：服务器端配置

如果你有服务器的管理员权限，编辑 `/etc/ssh/sshd_config`，添加：

```
ClientAliveInterval 15
ClientAliveCountMax 3
TCPKeepAlive yes
```

然后重启 SSH 服务：

```bash
sudo systemctl restart sshd
```

---

## 原理总结

### 修复前
```
Cursor ←→ SSH连接（空闲超时）←→ 服务器
→ 中间设备静默断开连接 → Cursor 不知道 → "taking longer than expected"
```

### 修复后
```
Cursor ←→ SSH连接（每15秒心跳）←→ 服务器
→ 心跳保活，中间设备不会断开
→ 万一真断了，45秒内检测到 → 自动重连最多10次
```

---

## 注意事项

1. **ServerAliveInterval 设为 15 秒比较激进**，如果网络环境稳定可以改为 30-60 秒
2. **这些设置对所有 SSH 连接生效**（Host *），如果只想针对特定服务器，把 * 改为具体的 Host
3. **修改 `~/.ssh/config` 后无需重启**，下次连接自动生效
4. **修改 Cursor settings.json 后建议重启 Cursor**

---

## 验证配置是否生效

修改配置后，重新连接 SSH，然后可以通过以下命令验证：

```bash
# 在 SSH 连接的终端中运行，查看当前连接的配置
ssh -G 你的主机名 | grep -E "(alive|timeout)"
```

如果看到 `serveraliveinterval 15`，说明配置已生效。
