# 自用命令

## 启动所有容器

```shell
sudo docker start $(sudo docker ps -a | awk '{ print $1}' | tail -n +2)
```

## 关闭所有容器

```shell
sudo docker stop $(sudo docker ps -a | awk '{ print $1}' | tail -n +2)
```

## Dockerfile

```shell
```

## python



## opengauss

### 单机

```shell
sudo docker run \
	--name opengauss \
	--privileged=true \
	-d \
	-e GS_PASSWORD=Gaussdb@123 \
	-p 54320:5432 \
	enmotech/opengauss

# 默认用户名 gaussdb
# 默认用户密码 Gaussdb@123
```

### 主从复制

1. 拉取容器镜像

2. 运行脚本create_master_slave.sh，按照提示输入所需参数，或者直接使用默认值，即可自动创建openGauss一主一备架构的两个容器。

```shell
#!/bin/bash -e
# Parameters
#!/bin/bash

#set OG_SUBNET,GS_PASSWORD,MASTER_IP,SLAVE_1_IP,MASTER_HOST_PORT,MASTER_LOCAL_PORT,SLAVE_1_HOST_PORT,SLAVE_1_LOCAL_PORT,MASTER_NODENAME,SLAVE_NODENAME

read -p "Please input OG_SUBNET (容器所在网段) [172.11.0.0/24]: " OG_SUBNET
OG_SUBNET=${OG_SUBNET:-172.11.0.0/24}
echo "OG_SUBNET set $OG_SUBNET"

read -p "Please input GS_PASSWORD (定义数据库密码)[Gaussdb@123]: " GS_PASSWORD
GS_PASSWORD=${GS_PASSWORD:-Gaussdb@123}
echo "GS_PASSWORD set $GS_PASSWORD"

read -p "Please input MASTER_IP (主库IP)[172.11.0.101]: " MASTER_IP
MASTER_IP=${MASTER_IP:-172.11.0.101}
echo "MASTER_IP set $MASTER_IP"

read -p "Please input SLAVE_1_IP (备库IP)[172.11.0.102]: " SLAVE_1_IP
SLAVE_1_IP=${SLAVE_1_IP:-172.11.0.102}
echo "SLAVE_1_IP set $SLAVE_1_IP"

read -p "Please input MASTER_HOST_PORT (主库数据库服务端口)[54325]: " MASTER_HOST_PORT
MASTER_HOST_PORT=${MASTER_HOST_PORT:-54325}
echo "MASTER_HOST_PORT set $MASTER_HOST_PORT"

read -p "Please input MASTER_LOCAL_PORT (主库通信端口)[54326]: " MASTER_LOCAL_PORT
MASTER_LOCAL_PORT=${MASTER_LOCAL_PORT:-54326}
echo "MASTER_LOCAL_PORT set $MASTER_LOCAL_PORT"

read -p "Please input SLAVE_1_HOST_PORT (备库数据库服务端口)[54327]: " SLAVE_1_HOST_PORT
SLAVE_1_HOST_PORT=${SLAVE_1_HOST_PORT:-54327}
echo "SLAVE_1_HOST_PORT set $SLAVE_1_HOST_PORT"

read -p "Please input SLAVE_1_LOCAL_PORT (备库通信端口)[54328]: " SLAVE_1_LOCAL_PORT
SLAVE_1_LOCAL_PORT=${SLAVE_1_LOCAL_PORT:-54328}
echo "SLAVE_1_LOCAL_PORT set $SLAVE_1_LOCAL_PORT"

read -p "Please input MASTER_NODENAME [opengauss_master]: " MASTER_NODENAME
MASTER_NODENAME=${MASTER_NODENAME:-opengauss_master}
echo "MASTER_NODENAME set $MASTER_NODENAME"

read -p "Please input SLAVE_NODENAME [opengauss_slave1]: " SLAVE_NODENAME
SLAVE_NODENAME=${SLAVE_NODENAME:-opengauss_slave1}
echo "SLAVE_NODENAME set $SLAVE_NODENAME"

read -p "Please input openGauss VERSION [1.1.0]: " VERSION
VERSION=${VERSION:-1.1.0}
echo "openGauss VERSION set $VERSION"

echo "starting  "

docker network create --subnet=$OG_SUBNET opengaussnetwork \
|| {
  echo ""
  echo "ERROR: OpenGauss Database Network was NOT successfully created."
  echo "HINT: opengaussnetwork Maybe Already Exsist Please Execute 'docker network rm opengaussnetwork' "
  exit 1
}
echo "OpenGauss Database Network Created."

docker run \
	--network opengaussnetwork \
	--ip $MASTER_IP \
	--privileged=true \
	--name $MASTER_NODENAME \
	-v opengauss_cluster_master:/var/lib/opengauss \
	-h $MASTER_NODENAME \
	-p $MASTER_HOST_PORT:$MASTER_HOST_PORT \
	-d \
	-e GS_PORT=$MASTER_HOST_PORT \
	-e OG_SUBNET=$OG_SUBNET \
	-e GS_PASSWORD=$GS_PASSWORD \
	-e NODE_NAME=$MASTER_NODENAME \
	-e REPL_CONN_INFO="replconninfo1 = 'localhost=$MASTER_IP localport=$MASTER_LOCAL_PORT localservice=$MASTER_HOST_PORT remotehost=$SLAVE_1_IP remoteport=$SLAVE_1_LOCAL_PORT remoteservice=$SLAVE_1_HOST_PORT'\n" \
	enmotech/opengauss:$VERSION -M primary \
|| {
  echo ""
  echo "ERROR: OpenGauss Database Master Docker Container was NOT successfully created."
  exit 1
}
echo "OpenGauss Database Master Docker Container created."

sleep 30s

docker run \
	--network opengaussnetwork \
	--ip $SLAVE_1_IP \
	--privileged=true \
	--name $SLAVE_NODENAME \
	-h $SLAVE_NODENAME \
	-p $SLAVE_1_HOST_PORT:$SLAVE_1_HOST_PORT \
	-d \
	-e GS_PORT=$SLAVE_1_HOST_PORT \
	-e OG_SUBNET=$OG_SUBNET \
	-e GS_PASSWORD=$GS_PASSWORD \
	-e NODE_NAME=$SLAVE_NODENAME \
	-e REPL_CONN_INFO="replconninfo1 = 'localhost=$SLAVE_1_IP localport=$SLAVE_1_LOCAL_PORT localservice=$SLAVE_1_HOST_PORT remotehost=$MASTER_IP remoteport=$MASTER_LOCAL_PORT remoteservice=$MASTER_HOST_PORT'\n" \
	enmotech/opengauss:$VERSION -M standby \
|| {
  echo ""
  echo "ERROR: OpenGauss Database Slave1 Docker Container was NOT successfully created."
  exit 1
}
echo "OpenGauss Database Slave1 Docker Container created."
```

# MySQL

```shell
sudo docker run \
	--name mysql56 \
	-e MYSQL_ROOT_PASSWORD=MySQL@123 \
	-p 33061:3306 \
	-d \
	mysql:5.6

# 默认用户名 postgres
# 默认用户密码 MySQL@123
```



## Postgres

### 单机

```shell
sudo docker run \
	--name postgres13 \
	-e POSTGRES_PASSWORD=Postgres@123 \
	-p 54321:5432 \
	-d \
	postgres:13

# 默认用户名 postgres
# 默认用户密码 Postgres@123

# 这边不映射端口貌似没法连接
```

### 集群

```shell
# 定义docker存储volume的默认位置
export v_path=/var/lib/docker/volumes

# 若存在同名则删除
sudo docker rm -f postgres_master
sudo docker rm -f postgres_slave1
sudo docker rm -f postgres_slave2
sudo rm -rf $v_path/postgres_cluster_master/_data
sudo rm -rf $v_path/postgres_cluster_slave1
sudo rm -rf $v_path/postgres_cluster_slave2
sudo mkdir -p $v_path/postgres_cluster_master/_data/_data
sudo mkdir -p $v_path/postgres_cluster_slave1/_data
sudo mkdir -p $v_path/postgres_cluster_slave2/_data
```

```shell
# 创建容器
sudo docker run \
	--name postgres_master \
	--privileged=true \
	#--restart=always \
	-p 54301:5432 \
    -e POSTGRES_PASSWORD=Postgres@123 \
    -v postgres_cluster_master:/var/lib/postgresql/data \
    -d postgres:13
    
sudo docker run \
	--name postgres_slave1 \
	--privileged=true \
	#--restart=always \
	-p 54302:5432 \
	-e POSTGRES_PASSWORD=Postgres@123 \
	-v postgres_cluster_slave1:/var/lib/postgresql/data \
	-d postgres:13
	
sudo docker run \
	--name postgres_slave2 \
	--privileged=true \
	#--restart=always \
	-p 54303:5432 \
	-e POSTGRES_PASSWORD=Postgres@123 \
	-v postgres_cluster_slave2:/var/lib/postgresql/data \
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
sudo sed -i '$ahost replication replica 172.17.0.3/32 md5' $v_path/postgres_cluster_master/_data/pg_hba.conf
sudo sed -i '$ahost replication replica 172.17.0.4/32 md5' $v_path/postgres_cluster_master/_data/pg_hba.conf
sudo sed -i '$ahost replication replica 172.17.0.5/32 md5' $v_path/postgres_cluster_master/_data/pg_hba.conf

# 在主库的目录下，修改postgresql.conf 文件
sudo sed -i '$alisten_addresses = '\''*'\''' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$amax_connections = 100' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$aarchive_mode = on' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$aarchive_command = '\''cp %p /var/lib/postgresql/data/pg_archive/%f'\''' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$wal_level = 100' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$awal_level = replica' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$awal_keep_size = 1000' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$awal_sender_timeout = 60s' $v_path/postgres_cluster_master/_data/postgresql.conf

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
pg_basebackup -h 172.17.0.3 -p 5432 -U replica -Fp -Xs -Pv -R -D /var/lib/postgresql/data-bak
# 输入密码123456

# 退出容器
exit

# 复制
sudo rm -rf /tmp/postgres/data_bak/
sudo docker cp postgres_master:/var/lib/postgresql/data-bak /tmp/postgres/data_bak

# 增加参数
sudo sed -i '$aprimary_conninfo = '\''host=172.17.0.3 port=54ls32 user=replica password=123456'\''' /tmp/postgres/data_bak/postgresql.conf
sudo sed -i '$arecovery_target_timeline = latest' /tmp/postgres/data_bak/postgresql.conf
sudo sed -i '$amax_connections = 120 # 大于等于主节点' /tmp/postgres/data_bak/postgresql.conf
sudo sed -i '$ahot_standby = on' /tmp/postgres/data_bak/postgresql.conf
sudo sed -i '$amax_standby_streaming_delay = 30s' /tmp/postgres/data_bak/postgresql.conf
sudo sed -i '$awal_receiver_status_interval = 10s' /tmp/postgres/data_bak/postgresql.conf
sudo sed -i '$ahot_standby_feedback = on' /tmp/postgres/data_bak/postgresql.conf
```
```shell
# extra 

# 主库开启日志  不开日志可忽略
sudo sed -i '$alogging_collector = on' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$alog_directory = '\''log'\''' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$alog_filename = '\''postgresql-%Y-%m-%d_%H%M%S.log'\''' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo sed -i '$alog_file_mode = 0600' $v_path/postgres_cluster_master/_data/postgresql.conf
sudo docker restart postgres_master
```
```shell
# 配置从库1

# 停止容器
sudo docker stop postgres_slave1

sudo rm -rf $v_path/postgres_cluster_slave1/
sudo mkdir -p $v_path/postgres_cluster_slave1/
sudo cp -r /tmp/postgres/data_bak $v_path/postgres_cluster_slave1/_data

# 重新启动数据库
sudo docker start postgres_slave1
```
```shell
# 配置主库2

# 停止容器
sudo docker stop postgres_slave2

sudo rm -rf $v_path/postgres_cluster_slave2/
sudo mkdir -p $v_path/postgres_cluster_slave2/
sudo cp -r /tmp/postgres/data_bak $v_path/postgres_cluster_slave2/_data

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

## portainer

```shell
sudo docker pull portainer/portainer-ce

sudo docker run \
	--name portainer \
	-d \
	-p 8088:9000 \
	--restart=always \
	-v /var/run/docker.sock:/var/run/docker.sock \
	--privileged=true \
	portainer/portainer-ce
```

