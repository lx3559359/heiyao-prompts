# 黑曜提示词skill

按角色、作品、底模和权重版本查询已发布的 LoRA 触发词，并编写原装、换装或多人画面的提示词。目录附默认短档、可选头部档和已有的版本注意事项。

## 安装

在你的 Codex 项目根目录运行：

```sh
git clone https://github.com/lx3559359/heiyao-prompts.git .agents/skills/heiyao-prompts
```

打开项目中的 Codex 聊天，调用 `$heiyao-prompts`。例如「用 $heiyao-prompts 查紫灵 v002 的换装提示词」。查询脚本使用 Python 3 标准库。

## 更新

在同一个项目根目录运行：

```sh
git -C .agents/skills/heiyao-prompts pull --ff-only
```

用 ZIP 安装的使用者可通过 [最新 ZIP](https://github.com/lx3559359/heiyao-prompts/archive/refs/heads/main.zip) 更新原目录。目录名称保持 `heiyao-prompts`。如果 Codex 仍显示旧技能，重新启动 Codex。

此仓库提供提示词说明、角色目录及查询工具。使用实际出图功能时请准备对应 LoRA 权重、底模和工作流。黑曜已发布资源可在 [黑曜官网](https://openheiyao.top/) 查看。
