@[TOC](NVIM常用配置解析)

## 设置VIM共享系统剪切板

如果我们想复制粘贴VIM外部的文本时，就需要使用如下命令实现VIM与系统剪切板的共享：

(1) Vimscript指令：

```vimscript
set clipboard=unnamed
```

(2) Luascript

```lua
vim.cmd('set clipboard=unnamed')
```