# 项目规则 / pop 工作流

## 文件写入可靠性（实测教训 2026-09-09 固化 · Edit 禁令 2026-09-11 解除）

实测教训（2026-09-09）：`Edit` 工具在本环境曾"返回成功但内容未写进磁盘"，且用默认编码的 `Select-String` 回读会被乱码哄骗，造成"以为写上了"的假象。
结论（2026-09-11 老板拍板）：**解除"禁止 Edit"限制，Edit 可直接用于文档修改，不许为绕 Edit 写临时脚本**；但教训保留——**任何改动落盘后必须 UTF-8 回读校验关键字符串**，不校验=不知道真没真写上。

### 修改方式（Edit 与 Write 都可用）

- **Edit 用于小段修改**：直接改目标段落。为绕 Edit 写临时脚本=过度工程，禁止。
- **Write 用于全量重写/新建**：Write 前必须先 Read 当前完整内容（在旧内容上叠加改动，避免覆盖用户手动改过的部分；若只改某一小段，先读全文件再照抄其余部分）。
- 复杂批量改动（如多文件同步版本号）可以用脚本一次跑完，但脚本用完即删，不留仓库。

### 落盘必校验（防呆，不算绕）

- **改完必须用 PowerShell `-Encoding UTF8` 回读校验**，检出本次改动独有的关键字符串，确认磁盘上真实存在才算完成。
- 禁止用默认编码的 `Select-String` 或只信工具返回的"成功"回执——它们都会被编码/回执骗到。
- 删除文件前先确认路径正确，删除后验证目标确实不存在。
- 修改文档后向用户汇报时，写清绝对路径 + 确认文件编码为 UTF-8，避免"我以为改了 X，其实 Y"或"打开乱码误以为没改"的错位。本目录下文档统一放 `新流程探索\sop文档\`。

### 验证命令（PowerShell，必须用 UTF-8 编码）

```powershell
$c = Get-Content -Path "文件绝对路径" -Raw -Encoding UTF8
$c.Contains("本次改动独有的关键字符串")   # True = 落盘成功；False = 写入失败，重写
```

## skill 双位置同步纪律（老板拍板，2026-09-11 固化）

**以后所有 skill 改动一律主写 D 盘，再同步 C 盘，禁止反方向。** 2026-09-11 实测教训：改动直接落在 C 盘 remote-skills，导致 D 盘 git 仓库长期落后（lantern 还是旧版七件套），最后靠手动展平同步才追平——反方向写 = 仓库失真。

### 两个位置

| 位置 | 路径 | 角色 | 结构 |
|:--|:--|:--|:--|
| D 盘 | `D:\popwave-skills\skills\{skill}\` | **主写位置**（git 仓库源） | 扁平结构（SKILL.md 直接在下） |
| C 盘 | `C:\Users\AWMPRO\AppData\Roaming\popwave\remote-skills\{skill}\{版本目录}\` | 应用生效位置（同步目标） | 版本目录结构（`1.0.0/`、`1.1.0/`，版本目录 = skill.json 的 version 字段） |

### 执行规则

- **写改动**：直接写 D 盘 `D:\popwave-skills\skills\{skill}\`，改完按仓库流程提交 git。

- **同步 C 盘**：改动落盘后必须把该 skill 的 D 盘内容递归复制到 C 盘对应版本目录（覆盖旧文件）——`Copy-Item -Path "D:\popwave-skills\skills\{skill}\*" -Destination "C:\Users\AWMPRO\AppData\Roaming\popwave\remote-skills\{skill}\{版本目录}\" -Recurse -Force`。C 盘版本目录不存在则先建（目录名照 skill.json 的 version 字段）。

- **同步后校验**：用上面的 UTF-8 回读命令，在 **C 盘**文件里检出本次改动独有的关键字符串，确认 C 盘真实生效。

- **新建 skill**：先建 D 盘 `skills\{skill}\`，再同步 C 盘建版本目录。删除 skill：D 盘删除 + 提交 git，C 盘对应目录一并删除。

- **C 盘是只读参照**：C 盘文件只用于确认应用加载到新版本，不在 C 盘上改内容。

### 一句话纪律

**改 D 盘 → 提交 git → 同步 C 盘 → UTF-8 校验 C 盘。** 顺序不可倒，缺同步 = 应用还在跑旧版。

## API 默认模型（老板拍板，2026-09-12 固化）

**所有走 API 的任务一律默认用 `deepseek-flash`，没有当次特别强调不许换 pro。**

适用：批量跑稿、盲评打分、评审、任何脚本调 API 的活。

- 换模型只有一种情况：老板当次明确指定。指定了就写进当次产出文件，方便回溯。
- 依据：这把 key 下 `/models` 实测只有 `deepseek-flash` 和 `deepseek-v4-pro`。实测 flash 单次 7-16 秒，pro 要 45-160 秒；pro 的思考量还会吃满输出额度，出现过正文 0 字的空转（`finish_reason=length`，`reasoning_tokens` 正好等于 `max_tokens`）。
