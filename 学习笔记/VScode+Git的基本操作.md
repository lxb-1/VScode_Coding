
## VScode+Git的基本操作
### 如何在Github创建仓库
首先需要注册Github账号，并创建仓库。然后，
### 如何将VScode项目上传到github仓库

在VScode下面的的bash终端如下如所示：
<div align=center><img src="../Figures/VScode终端.png"></div>


输入如下几个命令就可以实现将VScode中的代码推送到自己的Github仓库中了。

```bash
git add .               # 将项目下的所有文件放入暂存区
git commit -m "note"    # 提交到本地仓库
git push                # 提交到远程仓库github上
```

> **注意**：这里我已经配置好了该项目与我的github远程仓库lxb-1/VScode_Coding的git链接配置（如下图所示），所以对这该项目可以直接使用上面三条指令直接上传到lxb-1/VScode_Coding的远程仓库中。如果想上传到别的仓库，我们还需要进行新的配置，配置文件信息在使用git init命令后，自动在项目文件下的.git/config文件中创建。


<div align=center><img src="../Figures/项目git配置信息.png"></div>
