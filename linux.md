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