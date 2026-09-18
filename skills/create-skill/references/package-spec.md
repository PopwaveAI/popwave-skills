# Popwave 用户技能包

一个目录对应一个技能。根目录包含 SKILL.md 与 skill.json，其他资源用相对路径按需组织。

skill.json 字段：id 使用短的英文小写字母/数字/连字符；displayName 为不超过 100 字符的名称（可中文）；description 为不超过 2,000 字符的用途描述；version 使用 1.0.0 这样的版本号；entry 为 SKILL.md；tags 为简短标签数组。activation.default 为 false。客户端安装后分配独立稳定标识，不使用 name 覆盖已有技能。

SKILL.md 以 YAML frontmatter 开始，包含 name 和 description。正文说明何时使用、所需输入、工作方式、输出和必要边界。资源可位于 references/、templates/、scripts/ 或 assets/。正文可链接到资源，例如 `[评价维度](references/rubric.md)`。

入口不超过 80,000 字符和 1 MiB；单个资源最多 20 MiB；技能最多 2,000 个文件、深度 20 层，累计不超过 200 MiB。避免把大段资料重复写进入口。

不要使用符号链接、硬链接、绝对路径、上级目录跳转或 Windows 不支持的文件名。不要写入 .env、真实私钥、node_modules 或 .git。不要用同一目录容纳多个技能。

修改草稿时保持用途与职责一致。安装和更新由客户端确认流程决定，不能修改 installed.json。
