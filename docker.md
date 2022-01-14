# 自用命令

## 启动所有容器

```shell
sudo docker start $(sudo docker ps -a | awk '{ print $1}' | tail -n +2)
```

## 关闭所有容器

```shell
sudo docker stop $(sudo docker ps -a | awk '{ print $1}' | tail -n +2)
```



## opengauss

```shell
sudo docker run --name opengauss --privileged=true -d -e GS_PASSWORD=Gaussdb@123 -p 54320:5432 enmotech/opengauss

# 默认用户名 gaussdb
# 默认用户密码 Gaussdb@123
```

# MySQL

```shell
```



## Postgres

```shell
sudo docker run --name postgres13 -e POSTGRES_PASSWORD=Postgres@123 -p 54321:5432 -d postgres:13

# 默认用户名 postgres
# 默认用户密码 Postgres@123

# 这边不映射端口貌似没法连接
```

