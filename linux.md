## Linux环境变量配置

### 环境变量的分类

用户级别环境变量配置文件：

-  ~/.bashrc 
- ~/.profile 
- ~/.bash_profile（centos7 无）
- /home/非root用户名/.bashrc 

系统级别环境变量配置文件： 

- /etc/bashrc 
- /etc/profile 
- /etc/bash_profile（centos7 无）
- /etc/environment 

### Linux环境变量加载顺序

1. /etc/environment
2. /etc/profile
3. /etc/bashrc
4. ~/.profile
5. ~/.bashrc

#### `/etc/environment`

- 生效时间：新开终端生效，或者手动`source /etc/environment`生效
- 生效期限：永久有效
- 生效范围：对所有用户有效

#### `/etc/profile`

- 生效时间：新开终端生效，或者手动`source /etc/profile`生效
- 生效期限：永久有效
- 生效范围：对所有用户有效

#### `/etc/bash.bashrc`

- 生效时间：新开终端生效，或者手动`source /etc/bashrc`生效
- 生效期限：永久有效
- 生效范围：对所有用户有效

#### `~/.profile`

- 生效时间：使用相同的用户打开新的终端时生效，或者手动`source ~/.bash_profile`生效
- 生效期限：永久有效
- 生效范围：仅对当前用户有效
- 如果没有`~/.bash_profile`文件，则可以编辑`~/.profile`文件或者新建一个

#### `~/.bashrc`

- 生效时间：使用相同的用户打开新的终端时生效，或者手动`source ~/.bashrc`生效
- 生效期限：永久有效
- 生效范围：仅对当前用户有效
- 如果有后续的环境变量加载文件覆盖了`PATH`定义，则可能不生效



## 如何创建eclipse的快捷方式

进入/usr/share/applications文件夹.该文件夹就相当于Windows上的快捷方式。可以用 ls 查看一下都是以.desktop 结尾的文件。

```shell
[Desktop Entry]
Encoding=UTF-8
Name=Eclipse
Comment=Eclipse IDE
Exec=/usr/local/eclipse/eclipse(eclipse存放路径)
Icon=/usr/local/eclipse/icon.xpm(eclipse存放路径)
Terminal=false
Type=Application
Categories=GNOME;Application;Development;
StartupNotify=true
```

## 常用命令

端口查询