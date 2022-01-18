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
sudo docker run --name mysql56 -e MYSQL_ROOT_PASSWORD=MySQL@123 -p 33061:3306 -d mysql:5.6

# 默认用户名 postgres
# 默认用户密码 MySQL@123
```



## Postgres

### 单机

```shell
sudo docker run --name postgres13 -e POSTGRES_PASSWORD=Postgres@123 -p 54321:5432 -d postgres:13

# 默认用户名 postgres
# 默认用户密码 Postgres@123

# 这边不映射端口貌似没法连接
```

### 集群

```shell
# 若存在同名则删除
sudo docker rm -f postgres_master
sudo docker rm -f postgres_slave1
sudo docker rm -f postgres_slave2
sudo rm -rf /tmp/postgres_cluster/
```

```shell
# 创建容器
sudo docker run \
	--name postgres_master \
	--privileged=true \
	--restart=always \
	-p 54301:5432 \
    -e POSTGRES_PASSWORD=Postgres@123 \
    -v /tmp/postgres_cluster/postgres_master:/var/lib/postgresql/data \
    -d postgres:13
    
sudo docker run \
	--name postgres_slave1 \
	--privileged=true \
	--restart=always \
	-p 54302:5432 \
	-e POSTGRES_PASSWORD=Postgres@123 \
	-v /tmp/postgres_cluster/postgres_slave1:/var/lib/postgresql/data \
	-d postgres:13
	
sudo docker run \
	--name postgres_slave2 \
	--privileged=true \
	--restart=always \
	-p 54303:5432 \
	-e POSTGRES_PASSWORD=Postgres@123 \
	-v /tmp/postgres_cluster/postgres_slave2:/var/lib/postgresql/data \
	-d postgres:13
```

```shell
# 获取三个数据库的ip地址
sudo docker inspect postgres_master |grep IPAddress
sudo docker inspect postgres_slave1 |grep IPAddress
sudo docker inspect postgres_slave2 |grep IPAddress
```

```shell
# 配置主库

# 需要注意替换IP
# 配置主库，将从库的ip地址添加到pg_hba.conf
sudo sed -i '$ahost replication replica 172.17.0.2/32 md5' /tmp/postgres_cluster/postgres_master/pg_hba.conf
sudo sed -i '$ahost replication replica 172.17.0.4/32 md5' /tmp/postgres_cluster/postgres_master/pg_hba.conf
sudo sed -i '$ahost replication replica 172.17.0.5/32 md5' /tmp/postgres_cluster/postgres_master/pg_hba.conf

# 在主库的目录下，修改postgresql.conf 文件
sudo sed -i '$alisten_addresses = '\''*'\''' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$amax_connections = 100' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$aarchive_mode = on' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$aarchive_command = '\''cp %p /var/lib/postgresql/data/pg_archive/%f'\''' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$wal_level = 100' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$awal_level = replica' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$awal_keep_size = 1000' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$awal_sender_timeout = 60s' /tmp/postgres_cluster/postgres_master/postgresql.conf

# 重启主库
sudo docker restart postgres_master
```

```shell
# 导出主库配置

sudo docker exec -it postgres_master bash

# 进入数据库配置
psql -U postgres

CREATE ROLE replica login replication encrypted password '123456';
CREATE DATABASE replica;

# 退出数据库
\q

# 制作备份
pg_basebackup -h 172.17.0.2 -p 5432 -U replica -Fp -Xs -Pv -R -D /var/lib/postgresql/data-bak

# 退出容器
exit

# 复制
sudo rm -rf /tmp/postgres_cluster/data-bak/
sudo docker cp postgres_master:/var/lib/postgresql/data-bak /tmp/postgres_cluster/

# 增加参数
sudo sed -i '$aprimary_conninfo = '\''host=172.17.0.2 port=5432 user=replica password=123456'\''' /tmp/postgres_cluster/data-bak/postgresql.conf
sudo sed -i '$arecovery_target_timeline = latest' /tmp/postgres_cluster/data-bak/postgresql.conf
sudo sed -i '$amax_connections = 120 # 大于等于主节点' /tmp/postgres_cluster/data-bak/postgresql.conf
sudo sed -i '$ahot_standby = on' /tmp/postgres_cluster/data-bak/postgresql.conf
sudo sed -i '$amax_standby_streaming_delay = 30s' /tmp/postgres_cluster/data-bak/postgresql.conf
sudo sed -i '$awal_receiver_status_interval = 10s' /tmp/postgres_cluster/data-bak/postgresql.conf
sudo sed -i '$ahot_standby_feedback = on' /tmp/postgres_cluster/data-bak/postgresql.conf
```
```shell
# extra 

# 主库开启日志  不开日志可忽略
sudo sed -i '$alogging_collector = on' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$alog_directory = '\''log'\''' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$alog_filename = '\''postgresql-%Y-%m-%d_%H%M%S.log'\''' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo sed -i '$alog_file_mode = 0600' /tmp/postgres_cluster/postgres_master/postgresql.conf
sudo docker restart postgres_master
```
```shell
# 配置从库1

# 停止容器
sudo docker stop postgres_slave1

sudo rm -rf /tmp/postgres_cluster/postgres_slave1/
sudo cp -r /tmp/postgres_cluster/data-bak /tmp/postgres_cluster/postgres_slave1/

# 重新启动数据库
sudo docker start postgres_slave1
```
```shell
# 配置主库2

# 停止容器
sudo docker stop postgres_slave2

sudo rm -rf /tmp/postgres_cluster/postgres_slave2/
sudo cp -r /tmp/postgres_cluster/data-bak /tmp/postgres_cluster/postgres_slave2/

# 重新启动数据库
sudo docker start postgres_slave2
```

```shell
# 测试从库连接

# 进入主库
sudo docker exec -it postgres_master bash

psql -U postgres

select client_addr,sync_state from pg_stat_replication;

CREATE USER pguser WITH PASSWORD 'pguser123';
CREATE DATABASE testdb OWNER pguser;

\c testdb pguser;
CREATE TABLE jk(id int,name varchar(20));
INSERT INTO jk(id,name) VALUES(1,'jj');
INSERT INTO jk(id,name) VALUES(2,'jk');
```

