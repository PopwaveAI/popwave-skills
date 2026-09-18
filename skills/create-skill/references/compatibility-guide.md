# 依赖与兼容

纯提示词与参考资料无需附加运行依赖。需要脚本或外部工具时，在 skill.json 中加入按实际需要填写的 dependencies：

```json
{
  "dependencies": {
    "commands": ["python3"],
    "env": ["SERVICE_TOKEN"],
    "platforms": ["darwin", "win32", "linux"],
    "files": ["scripts/convert.py"]
  }
}
```

commands 是必需的 PATH 命令名，不能是完整 shell 指令或带参数的字符串；env 仅列必需变量名，不包含值；platforms 是支持的 Node 平台名，无限制时省略；files 列出必须存在的包内相对文件。没有依赖时省略 dependencies，不复制示例中的虚构依赖。

客户端只检查声明，不会自动安装命令或设置变量。仅声明已知真实要求，未验证的依赖应在交付说明中指出。脚本保持跨平台或声明平台限制，不硬编码用户本机目录。

allowed-tools、model、MCP、插件或 permissions 元数据不授予运行权限，也不改变客户端当前模型。第三方专属工具无法直接使用时，说明限制或按用户目标采用客户端已支持的能力，不虚构工具。

正常示例应覆盖主要功能；边界示例可用缺失输入或缺少依赖，说明如何提示用户补充。结构检查不等于脚本执行成功。
