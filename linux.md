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

## 常用命令（待整理）

Linux 下命令有哪几种可使用的通配符？

```
“？”可替代单个字符。
“*”可替代任意多个字符。
方括号“[charset]”可替代 charset 集中的任何单个字符，如[a-z]，[abABC]
```

用什么命令对一个文件的内容进行统计？(行号、单词数、字节数)

```
wc 命令 - c 统计字节数 - l 统计行数 - w 统计字数
```

Grep 命令有什么用？如何忽略大小写？如何查找不含该串的行?

```

```

Linux 中进程有哪几种状态？在 ps 显示出来的信息中，分别用什么符号表示的？

```
（1）、不可中断状态：进程处于睡眠状态，但是此刻进程是不可中断的。不可中断， 指进程不响应异步信号。
（2）、暂停状态/跟踪状态：向进程发送一个 SIGSTOP 信号，它就会因响应该信号 而进入 TASK_STOPPED 状态;当进程正在被跟踪时，它处于 TASK_TRACED 这个特殊的状态。
“正在被跟踪”指的是进程暂停下来，等待跟踪它的进程对它进行操作。
（3）、就绪状态：在 run_queue 队列里的状态
（4）、运行状态：在 run_queue 队列里的状态
（5）、可中断睡眠状态：处于这个状态的进程因为等待某某事件的发生（比如等待 socket 连接、等待信号量），而被挂起
（6）、zombie 状态（僵尸）：父亲没有通过 wait 系列的系统调用会顺便将子进程的尸体（task_struct）也释放掉
（7）、退出状态
```

哪个命令专门用来查看后台任务? 

```
job -l
```

把后台任务调到前台执行使用什么命令?

把停下的后台任务在后台执行起来用什么命令?

```
fg 把后台任务调到前台执行

bg 把停下的后台任务在后台执行起来
```

怎么查看系统支持的所有信号？

```
kill -l
```

使用什么命令查看磁盘使用空间？空闲空间呢?

```
df -hl
```

使用什么命令查看网络是否连通?

```
netstat
```

查看各类环境变量用什么命令?

```
env
```

通过什么命令查找执行命令?

```
which 查找系统PATH目录下的可执行文件
whereis 查二进制文件、说明文档，源文件等
```

怎么对命令进行取别名？

```
alias la='ls -a'
```

du 和 df 的定义，以及区别？

```
du 显示目录或文件的大小
df 显示每个<文件>所在的文件系统的信息，默认是显示所有文件系统。

du 命令是用户级的程序，它不考虑 Meta Data，而 df 命令则查看文件系统的磁盘分配图并考虑 Meta Data。
du 命令只查看文件系统的部分情况，而 df 命令获得真正的文件系统数据。 

```

你的系统目前有许多正在运行的任务，在不重启机器的条件下，有什么方法可以把所有正在运行的进程移除呢？

```
使用linux命令 disown -r 可以将所有正在运行的进程移除。
```

bash shell 中的hash 命令有什么作用？

```
linux命令’hash’管理着一个内置的哈希表，记录了已执行过的命令的完整路径, 用该命令可以打印出你所使用过的命令以及执行的次数。

[root@localhost ~]# hash
hits command
2 /bin/ls
2 /bin/su
```

# 