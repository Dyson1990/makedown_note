## 常用系统表

### pg_class

PG_CLASS系统表存储数据库对象信息及其之间的关系。

### pg_database

### pg_namespace

### pg_user

查看DWS数据库中都有哪些用户帐号

### pgxc_thread_wait_status

该视图显示由执行语句产生的线程之间层次调用关系，以及各个线程的阻塞等待状态。该视图常用来定位数据库通信过程中的hang问题，主要用于定位的信息包括：query_id，tlevel，wait_status

### pg_stat_activity

查看目前有哪些帐号在使用数据库

#### 查看连接信息

```sql
SELECT usename,client_addr,application_name,state,waiting,enqueue,pid FROM PG_STAT_ACTIVITY WHERE DATNAME='数据库名称';
```

  通过以下SQL就能确认当前的连接用户、连接地址、连接应用、状态、是否等待锁、排队状态以及线程id。

#### 查看SQL运行信息

```sql
SELECT usename,state,query FROM PG_STAT_ACTIVITY WHERE DATNAME='数据库名称';
```

获取当前用户执行SQL信息

如果state为active，则query列表示当前执行的SQL语句，其他情况则表示为上一个查询语句。

#### 查看耗时较长的语句

```sql
SELECT current_timestamp - query_start as runtime, datname, usename, query FROM PG_STAT_ACTIVITY WHERE state != 'idle' order by 1 desc;
```

查询会返回按执行时间长短从大到小排列的查询语句列表。第一条结果就是当前系统中执行时间最长的查询语句。

#### 查看处于阻塞状态的语句

```sql
SELECT pid, datname, usename, state, query FROM PG_STAT_ACTIVITY WHERE state <> 'idle' and waiting=true;
```

- 大部分场景下，阻塞是因为系统内部锁而导致的，waiting字段才显示为true，此阻塞可在视图pg_stat_activity中体现。
- 在一些少数场景下，例如写文件、定时器等情况的查询阻塞，不会在视图pg_stat_activity中体现。

```sql
SELECT w.query as waiting_query,
w.pid as w_pid,
w.usename as w_user,
l.query as locking_query,
l.pid as l_pid,
l.usename as l_user,
t.schemaname || '.' || t.relname as tablename
from pg_stat_activity w join pg_locks l1 on w.pid = l1.pid
and not l1.granted join pg_locks l2 on l1.relation = l2.relation
and l2.granted join pg_stat_activity l on l2.pid = l.pid join pg_stat_user_tables t on l1.relation = t.relid
where w.waiting;
```

查看阻塞的查询语句及阻塞查询的表、模式信息

该查询返回会话ID、用户信息、查询状态，以及导致阻塞的表、模式信息。

查询到阻塞的表及模式信息后请根据会话ID结束会话。

## 表结构优化

### 行存/列存优劣势

|          | 行存                                     | 列存                                                 |
| -------- | ---------------------------------------- | ---------------------------------------------------- |
| 适用场景 | 数据频繁更新                             | 适用于一次性insert大批量数据                         |
|          | 数据频繁少量插入                         | 统计分析类查询（group ,jion多的场景）                |
| 查询方式 | 点查询（返回记录少，基于索引的简单查询） | 即席查询（查询条件列不确定，行存无法确定索引的场景） |
|          | 增删改较多                               |                                                      |
| 压缩     | 默认不压缩                               | 提供更优的数据压缩比、更好的索引性能，默认压缩       |

### 分布方式

| 策略        | 描述                                                         | 适用场景           |
| ----------- | ------------------------------------------------------------ | ------------------ |
| Replication | 将表中的全量数据在集群的每一个DN实例上保留一份，即每个数据节点都有完整的表数据。 | 小表，维度表       |
| Hash        | 表将表中某一个或几个字段进行hash运算后，生成对应的hash值，通过映射，把数据分布到指定DN。 | 数据量较大的事实表 |

#### Hash分布表选取分布列

1. 列值应比较**离散**，以便数据能够均匀分布到各个DN。例如，考虑选择表的主键为分布列，如在人员信息表中选择身份证号码为分布列。
2. 在满足第一条原则的情况下尽量**不要选取存在常量filter的列**。例如，表dwcjk相关的部分查询中出现dwcjk的列zqdh存在常量的约束(例如zqdh=’000001’)，那么就应当尽量不用zqdh做分布列。
3. 在满足前两条原则的情况，考虑选择查询中的连接条件为分布列，以便Join任务能够下推到DN中执行，且减少DN之间的通信数据量。

### 压缩比

| 压缩级别 | 适用场景                                      |
| -------- | --------------------------------------------- |
| LOW      | 系统CPU使用率高，存储磁盘空间充足。           |
| MIDDLE   | 系统CPU使用率适中，存储磁盘空间不是特别充足。 |
| HIGH     | 系统CPU使用率低，存储磁盘空间不充足。         |

压缩比通过COMPRESSION参数指定，其中列存表取值为：YES/NO/LOW/MIDDLE/HIGH，默认值为LOW。

### 索引

#### 创建索引原则

- 经常执行查询的字段
- 在连接条件上创建索引
- Where子句的过滤条件上
- 经常出现在order by，group by和distinct字段

#### DWS索引支持

- Btree索引：使用一种类似B+树的结构来存储数据的键值，通过这种结构能够快速的查找索引。Btree适合支持比较查询和查询范围。但因为其本身的数据结构，当数据量非常大的时候，每条数据的入库速度会变得越来越慢，占用的内存也会越来越大，严重的影响了入库性能。（适用于行存、列存）
- GIN索引是倒排索引，可以处理包含多个键的值（比如数组）。（适用于行存、列存）
- Gist适用于几何和地理等多维数据类型和集合数据类型。（适用于行存）
- Psort:针对列存表进行局部排序索引。（适用于列存）

### 局部聚簇

局部聚簇（Partial Cluster Key）是列存下的一种技术。这种技术可以通过min/max稀疏索引较快的实现基表扫描的filter过滤。

| 适用条件                                                     |
| ------------------------------------------------------------ |
| 局部聚簇可以指定多列，但是不建议超过2列                      |
| 受基表的简单表达式约束。这种约束一般形如col op const,其中col为列名，op为操作符=，<，>，<=，>=，const为常量值。 |
| 尽量采用选择度比较高（过滤更多数据）的简单表达式的列。       |
| 尽量把选择度比较低的约束列放在局部聚簇中的前面。             |
| 尽量把枚举类型的列放在局部聚簇的前面。                       |

## Toast

### 四种策略

| 策略     | 压缩 | 行外存储 |
| -------- | ---- | -------- |
| PLAIN    | 避免 | 避免     |
| MAIN     | 允许 | 尽量避免 |
| EXTERNA  | 不许 | 允许     |
| EXTENDED | 允许 | 允许     |

### 缺点

对大字段创建索引可能会失败，

## VACUUM

### 针对的问题

#### 空间膨胀

清除废旧元组以及相应的索引。包括提交的事务delete的元组（以及索引）、update的旧版本（以及索引），回滚的事务insert的元组（以及索引）、update的新版本（以及索引）、copy导入的元组（以及索引）。

#### freeze

防止因事务ID回卷问题（Transaction ID wraparound）而导致的宕机，将小于OldestXmin的事务号转化为freeze xid，更新表的relfrozenxid，更新库的relfrozenxid，truncate clog。

#### 更新统计信息

VACUUM analyze时，会更新统计信息，使得优化器能够选择更好的方案执行sql。

## 快照

### 手动创建快照前提条件

- 可用
- 只读
- 非均衡

### 支持重新自定义的参数

恢复快照时以下参数支持重新自定义，其他参数默认与快照中的备份信息保持一致。

- “区域”
- “可用区”
- “节点规格”
- “集群名称”
- “数据库端口”
- “虚拟私有云”
- “子网”
- “安全组”
- “公网访问”
- “企业项目”
- “自动快照”（当配置为“自定义”时）
- “保留天数”（当配置为“自定义”、开关设置为开启时）
- “快照执行周期”（当配置为“自定义”、开关设置为开启时）
- “参数模板”（当配置为“自定义”时）
- “标签”（当配置为“自定义”时）
- “密钥名称”（如果原集群开启了“加密数据库”，当配置为“自定义”时）

## 审计日志

### 关键审计项

| 参数名       | 说明                                       |
| ------------ | ------------------------------------------ |
| 关键审计项   | 记录用户登录成功、登录失败和注销的信息。   |
| （默认启用） | 记录数据库启动、停止、恢复和切换审计信息。 |
|              | 记录用户锁定和解锁功能信息。               |
|              | 记录用户权限授予和权限回收信息。           |
|              | 记录SET操作的审计功能。                    |

### 审计项（8.1.1.100及以上版本）

| 审计操作     | 解释                                                         | 默认状态                                                     |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 用户越权访问 | 表示是否记录用户的越权访问操作                               | 关闭                                                         |
| DQL          | 可选SELECT操作进行审计。                                     |                                                              |
| DML          | 表示是否对数据表的**INSERT**、**UPDATE**和**DELETE**操作进行记录。 （增加**COPY**，**MERGE**选项） | 关闭                                                         |
| DDL          | 表示是否对指定数据库对象的**CREATE**、**DROP**和**ALTER**操作进行记录。 | “DATABASE”、“SCHEMA”和“USER”，“TABLE”、“DATA SOURCE”和“NODE GROUP”默认启用，其他关闭 |
| 其他         | 表示对其他的操作进行记录                                     | TRANSACTION，CURSOR操作，默认启动；                          |
|              |                                                              | VACUUM，ANALYZE，USER FUNCTION，SPECIAL FUNCTION，PREPARE STATEMENT默认关闭； |



## 三权分立

### 默认权限

| 对象名称         | 系统管理员                                         | 安全管理员                                                   | 审计管理员 | 普通用户 |
| ---------------- | -------------------------------------------------- | ------------------------------------------------------------ | ---------- | -------- |
| 表空间           | 对表空间有创建、修改、删除、访问、分配操作的权限。 | 不具有对表空间进行创建、修改、删除、分配的权限，访问需要被赋权。 |            |          |
| 表               | 对所有表有所有的权限。                             | 仅对自己的表有所有的权限，对其他用户的表无权限。             |            |          |
| 索引             | 可以在所有的表上建立索引。                         | 仅可以在自己的表上建立索引。                                 |            |          |
| 模式             | 对所有模式有所有的权限。                           | 仅对自己的模式有所有的权限，对其他用户的模式无权限。         |            |          |
| 函数             | 对所有的函数有所有的权限。                         | 仅对自己的函数有所有的权限，对其他用户放在public这个公共模式下的函数有调用的权限，对其他用户放在其他模式下的函数无权限。 |            |          |
| 自定义视图       | 对所有的视图有所有的权限。                         | 仅对自己的视图有所有的权限，对其他用户的视图无权限。         |            |          |
| 系统表和系统视图 | 可以查看所有系统表和视图。                         | 只可以查看部分系统表和视图。详细请参见[系统表和系统视图](https://support.huaweicloud.com/devg-dws/dws_04_0559.html)。 |            |          |

### 三权分立后的变化

| 对象名称         | 系统管理员                                                   | 安全管理员 | 审计管理员 | 普通用户                   |
| ---------------- | ------------------------------------------------------------ | ---------- | ---------- | -------------------------- |
| 表空间           | 无变化                                                       | 无变化。   |            |                            |
| 表               | 权限缩小。 只对自己的表有所有权限，对其他用户放在属于各自模式下的表无权限。 | 无变化。   |            |                            |
| 索引             | 权限缩小。 只可以在自己的表上建立索引。                      | 无变化。   |            |                            |
| 模式             | 权限缩小。 只对自己的模式有所有的权限，对其他用户的模式无权限。 | 无变化。   |            |                            |
| 函数             | 权限缩小。 只对自己的函数有所有的权限，对其他用户放在属于各自模式下的函数无权限。 | 无变化。   |            |                            |
| 自定义视图       | 权限缩小。 只对自己的视图及其他用户放在public模式下的视图有所有的权限，对其他用户放在属于各自模式下的视图无权限。 | 无变化。   |            |                            |
| 系统表和系统视图 | 无变化。                                                     | 无变化。   | 无变化。   | 无权查看任何系统表和视图。 |

## 测试记录

### 前提

```sql
SET enable_fast_query_shipping = OFF;
```

### sql(where)

```sql

SELECT id, user_id, vote_id, group_id, create_time
FROM public.vote_record_memory
WHERE GROUP_ID = 1
;
```

#### EXPLAIN

```
 id |                   operation                   | E-rows | E-memory | E-width | E-costs 
----+-----------------------------------------------+--------+----------+---------+---------
  1 | ->  Streaming (type: GATHER)                  |  10073 |          |      41 | 3739.33 
  2 |    ->  Bitmap Heap Scan on vote_record_memory |  10073 | 1MB      |      41 | 3322.70 
  3 |       ->  Bitmap Index Scan                   |  10073 | 1MB      |       0 | 29.44   

Predicate Information (identified by plan id)
---------------------------------------------
  2 --Bitmap Heap Scan on vote_record_memory
        Recheck Cond: (group_id = 1)
  3 --Bitmap Index Scan
        Index Cond: (group_id = 1)

  ====== Query Summary =====  
------------------------------
System available mem: 819200KB
Query Max mem: 819200KB
Query estimated mem: 2048KB
```

#### EXPLAIN ANALYSE

```
 id |                   operation                   |     A-time     | A-rows | E-rows |  Peak Memory   | E-memory | A-width | E-width | E-costs 
----+-----------------------------------------------+----------------+--------+--------+----------------+----------+---------+---------+---------
  1 | ->  Streaming (type: GATHER)                  | 16.905         |  10014 |  10073 | 80KB           |          |         |      41 | 3739.33 
  2 |    ->  Bitmap Heap Scan on vote_record_memory | [4.185, 6.058] |  10014 |  10073 | [16KB, 16KB]   | 1MB      |         |      41 | 3322.70 
  3 |       ->  Bitmap Index Scan                   | [0.456, 0.510] |  10014 |  10073 | [167KB, 173KB] | 1MB      |         |       0 | 29.44   

Predicate Information (identified by plan id)
---------------------------------------------
  2 --Bitmap Heap Scan on vote_record_memory
        Recheck Cond: (group_id = 1)
  3 --Bitmap Index Scan
        Index Cond: (group_id = 1)

Memory Information (identified by plan id)
------------------------------------------
Coordinator Query Peak Memory:
        Query Peak Memory: 0MB
Datanode:
        Max Query Peak Memory: 0MB
        Min Query Peak Memory: 0MB

                     User Define Profiling                      
----------------------------------------------------------------
Plan Node id: 1  Track name: coordinator get datanode connection
 (actual time=[0.013, 0.013], calls=[1, 1])

                          ====== Query Summary =====                          
------------------------------------------------------------------------------
Datanode executor start time [dn_6005_6006, dn_6003_6004]: [0.030 ms,0.037 ms]
Datanode executor end time [dn_6001_6002, dn_6005_6006]: [0.038 ms,0.045 ms]
System available mem: 819200KB
Query Max mem: 819200KB
Query estimated mem: 2048KB
Coordinator executor start time: 0.053 ms
Coordinator executor run time: 17.869 ms
Coordinator executor end time: 0.018 ms
Planner runtime: 0.251 ms
Query Id: 217017207043941182
Total runtime: 17.969 ms
```

#### EXPLAIN PERFORMANCE


```
 id |                      operation                       |     A-time     | A-rows | E-rows | E-distinct |  Peak Memory   | E-memory | A-width | E-width | E-costs 
----+------------------------------------------------------+----------------+--------+--------+------------+----------------+----------+---------+---------+---------
  1 | ->  Streaming (type: GATHER)                         | 11.124         |  10014 |  10073 |            | 80KB           |          |         |      41 | 3739.33 
  2 |    ->  Bitmap Heap Scan on public.vote_record_memory | [4.208, 4.343] |  10014 |  10073 |            | [16KB, 16KB]   | 1MB      |         |      41 | 3322.70 
  3 |       ->  Bitmap Index Scan                          | [0.457, 0.475] |  10014 |  10073 |            | [167KB, 173KB] | 1MB      |         |       0 | 29.44   

     Predicate Information (identified by plan id)     
-------------------------------------------------------
  2 --Bitmap Heap Scan on public.vote_record_memory
        Recheck Cond: (vote_record_memory.group_id = 1)
  3 --Bitmap Index Scan
        Index Cond: (vote_record_memory.group_id = 1)

               Memory Information (identified by plan id)               
------------------------------------------------------------------------
Coordinator Query Peak Memory:
        Query Peak Memory: 0MB
DataNode Query Peak Memory
        dn_6001_6002 Query Peak Memory: 0MB
        dn_6003_6004 Query Peak Memory: 0MB
        dn_6005_6006 Query Peak Memory: 0MB
  1 --Streaming (type: GATHER)
        Peak Memory: 80KB, Estimate Memory: 2048MB
  2 --Bitmap Heap Scan on public.vote_record_memory
        dn_6001_6002 Peak Memory: 16KB, Estimate Memory: 1024KB
        dn_6003_6004 Peak Memory: 16KB, Estimate Memory: 1024KB
        dn_6005_6006 Peak Memory: 16KB, Estimate Memory: 1024KB
        dn_6001_6002 Stream Send time: 0.233; Data Serialize time: 3.976
        dn_6003_6004 Stream Send time: 0.241; Data Serialize time: 3.793
        dn_6005_6006 Stream Send time: 0.356; Data Serialize time: 4.037
  3 --Bitmap Index Scan
        dn_6001_6002 Peak Memory: 173KB, Estimate Memory: 1024KB
        dn_6003_6004 Peak Memory: 167KB, Estimate Memory: 1024KB
        dn_6005_6006 Peak Memory: 167KB, Estimate Memory: 1024KB

      Targetlist Information (identified by plan id)       
-----------------------------------------------------------
  1 --Streaming (type: GATHER)
        Output: id, user_id, vote_id, group_id, create_time
        Node/s: All datanodes
  2 --Bitmap Heap Scan on public.vote_record_memory
        Output: id, user_id, vote_id, group_id, create_time
        Distribute Key: id

                    Datanode Information (identified by plan id)                     
-------------------------------------------------------------------------------------
  1 --Streaming (type: GATHER)
        (actual time=3.424..11.124 rows=10014 loops=1)
        (Buffers: 0)
        (CPU: ex c/r=106, ex row=10014, ex cyc=1062118, inc cyc=1062118)
  2 --Bitmap Heap Scan on public.vote_record_memory
        dn_6001_6002 (actual time=0.747..4.304 rows=3413 loops=1) (filter time=0.000)
        dn_6003_6004 (actual time=0.713..4.208 rows=3199 loops=1) (filter time=0.000)
        dn_6005_6006 (actual time=0.734..4.343 rows=3402 loops=1) (filter time=0.000)
        dn_6001_6002 (Buffers: shared hit=2101)
        dn_6003_6004 (Buffers: shared hit=2041)
        dn_6005_6006 (Buffers: shared hit=2057)
        dn_6001_6002 (CPU: ex c/r=106, ex row=3413, ex cyc=364364, inc cyc=411481)
        dn_6003_6004 (CPU: ex c/r=111, ex row=3199, ex cyc=356130, inc cyc=401788)
        dn_6005_6006 (CPU: ex c/r=109, ex row=3402, ex cyc=371836, inc cyc=419388)
  3 --Bitmap Index Scan
        dn_6001_6002 (actual time=0.471..0.471 rows=3413 loops=1)
        dn_6003_6004 (actual time=0.457..0.457 rows=3199 loops=1)
        dn_6005_6006 (actual time=0.475..0.475 rows=3402 loops=1)
        dn_6001_6002 (Buffers: shared hit=12)
        dn_6003_6004 (Buffers: shared hit=12)
        dn_6005_6006 (Buffers: shared hit=12)
        dn_6001_6002 (CPU: ex c/r=13, ex row=3413, ex cyc=47117, inc cyc=47117)
        dn_6003_6004 (CPU: ex c/r=14, ex row=3199, ex cyc=45658, inc cyc=45658)
        dn_6005_6006 (CPU: ex c/r=13, ex row=3402, ex cyc=47552, inc cyc=47552)

                     User Define Profiling                      
----------------------------------------------------------------
Plan Node id: 1  Track name: coordinator get datanode connection
       cn_5001: (time=0.013 total_calls=1 loops=1)

                          ====== Query Summary =====                          
------------------------------------------------------------------------------
Datanode executor start time [dn_6003_6004, dn_6001_6002]: [0.030 ms,0.037 ms]
Datanode executor end time [dn_6001_6002, dn_6003_6004]: [0.038 ms,0.045 ms]
Remote query poll time: 6.203 ms, Deserialze time: 0.000 ms
System available mem: 819200KB
Query Max mem: 819200KB
Query estimated mem: 2048KB
Coordinator executor start time: 0.037 ms
Coordinator executor run time: 12.140 ms
Coordinator executor end time: 0.017 ms
Planner runtime: 0.189 ms
Query Id: 217017207043938643
Total runtime: 12.240 ms
```

### sql(group by)

```sql
SELECT group_id, COUNT(1)
FROM public.vote_record_memory
GROUP BY group_id
;
```



#### EXPLAIN

```
 id |                  operation                  | E-rows  | E-memory | E-width | E-costs 
----+---------------------------------------------+---------+----------+---------+---------
  1 | ->  HashAggregate                           |     100 |          |      12 | 8129.50 
  2 |    ->  Streaming (type: GATHER)             |     300 |          |      12 | 8129.50 
  3 |       ->  HashAggregate                     |     300 | 16MB     |      12 | 8117.00 
  4 |          ->  Seq Scan on vote_record_memory | 1000000 | 1MB      |       4 | 6449.33 

  ====== Query Summary =====  
------------------------------
System available mem: 819200KB
Query Max mem: 819200KB
Query estimated mem: 1034KB
```

#### EXPLAIN ANALYSE

```
 id |                  operation                  |       A-time       | A-rows  | E-rows  | Peak Memory  | E-memory | A-width | E-width | E-costs 
----+---------------------------------------------+--------------------+---------+---------+--------------+----------+---------+---------+---------
  1 | ->  HashAggregate                           | 227.781            |     100 |     100 | 26KB         |          |         |      12 | 8129.50 
  2 |    ->  Streaming (type: GATHER)             | 227.265            |     300 |     300 | 78KB         |          |         |      12 | 8129.50 
  3 |       ->  HashAggregate                     | [224.168, 224.463] |     300 |     300 | [26KB, 26KB] | 16MB     | [20,20] |      12 | 8117.00 
  4 |          ->  Seq Scan on vote_record_memory | [99.104, 102.054]  | 1000000 | 1000000 | [11KB, 11KB] | 1MB      |         |       4 | 6449.33 

Memory Information (identified by plan id)
------------------------------------------
Coordinator Query Peak Memory:
        Query Peak Memory: 0MB
Datanode:
        Max Query Peak Memory: 0MB
        Min Query Peak Memory: 0MB

                     User Define Profiling                      
----------------------------------------------------------------
Plan Node id: 2  Track name: coordinator get datanode connection
 (actual time=[0.018, 0.018], calls=[1, 1])

                          ====== Query Summary =====                          
------------------------------------------------------------------------------
Datanode executor start time [dn_6003_6004, dn_6005_6006]: [0.267 ms,0.299 ms]
Datanode executor end time [dn_6003_6004, dn_6005_6006]: [0.033 ms,0.035 ms]
System available mem: 819200KB
Query Max mem: 819200KB
Query estimated mem: 1034KB
Coordinator executor start time: 0.096 ms
Coordinator executor run time: 227.885 ms
Coordinator executor end time: 0.020 ms
Planner runtime: 0.345 ms
Query Id: 217017207043943627
Total runtime: 228.049 ms
```

#### EXPLAIN PERFORMANCE

```
 id |                     operation                      |       A-time       | A-rows  | E-rows  | E-distinct | Peak Memory  | E-memory | A-width | E-width | E-costs 
----+----------------------------------------------------+--------------------+---------+---------+------------+--------------+----------+---------+---------+---------
  1 | ->  HashAggregate                                  | 236.691            |     100 |     100 |            | 26KB         |          |         |      12 | 8129.50 
  2 |    ->  Streaming (type: GATHER)                    | 236.142            |     300 |     300 |            | 78KB         |          |         |      12 | 8129.50 
  3 |       ->  HashAggregate                            | [231.698, 233.825] |     300 |     300 |            | [26KB, 26KB] | 16MB     | [20,20] |      12 | 8117.00 
  4 |          ->  Seq Scan on public.vote_record_memory | [101.591, 103.650] | 1000000 | 1000000 |            | [11KB, 11KB] | 1MB      |         |       4 | 6449.33 

               Memory Information (identified by plan id)               
------------------------------------------------------------------------
Coordinator Query Peak Memory:
        Query Peak Memory: 0MB
DataNode Query Peak Memory
        dn_6001_6002 Query Peak Memory: 0MB
        dn_6003_6004 Query Peak Memory: 0MB
        dn_6005_6006 Query Peak Memory: 0MB
  1 --HashAggregate
        Peak Memory: 26KB, Estimate Memory: 2048MB, Width: 20
  2 --Streaming (type: GATHER)
        Peak Memory: 78KB, Estimate Memory: 2048MB
  3 --HashAggregate
        dn_6001_6002 Peak Memory: 26KB, Estimate Memory: 16MB, Width: 20
        dn_6003_6004 Peak Memory: 26KB, Estimate Memory: 16MB, Width: 20
        dn_6005_6006 Peak Memory: 26KB, Estimate Memory: 16MB, Width: 20
        dn_6001_6002 Stream Send time: 0.000; Data Serialize time: 0.040
        dn_6003_6004 Stream Send time: 0.000; Data Serialize time: 0.036
        dn_6005_6006 Stream Send time: 0.000; Data Serialize time: 0.036
  4 --Seq Scan on public.vote_record_memory
        dn_6001_6002 Peak Memory: 11KB, Estimate Memory: 1024KB
        dn_6003_6004 Peak Memory: 11KB, Estimate Memory: 1024KB
        dn_6005_6006 Peak Memory: 11KB, Estimate Memory: 1024KB

 Targetlist Information (identified by plan id)  
-------------------------------------------------
  1 --HashAggregate
        Output: group_id, count((count(1)))
        Group By Key: vote_record_memory.group_id
  2 --Streaming (type: GATHER)
        Output: group_id, (count(1))
        Node/s: All datanodes
  3 --HashAggregate
        Output: group_id, count(1)
        Group By Key: vote_record_memory.group_id
  4 --Seq Scan on public.vote_record_memory
        Output: group_id
        Distribute Key: id

                         Datanode Information (identified by plan id)                         
----------------------------------------------------------------------------------------------
  1 --HashAggregate
        (actual time=236.663..236.691 rows=100 loops=1) (projection time=0.031)
        (Buffers: 0)
        (CPU: ex c/r=188, ex row=300, ex cyc=56413, inc cyc=23668690)
  2 --Streaming (type: GATHER)
        (actual time=234.387..236.142 rows=300 loops=1)
        (Buffers: 0)
        (CPU: ex c/r=78707, ex row=300, ex cyc=23612277, inc cyc=23612277)
  3 --HashAggregate
        dn_6001_6002 (actual time=233.516..233.547 rows=100 loops=1) (projection time=18.354)
        dn_6003_6004 (actual time=231.667..231.698 rows=100 loops=1) (projection time=18.545)
        dn_6005_6006 (actual time=233.792..233.825 rows=100 loops=1) (projection time=18.292)
        dn_6001_6002 (Buffers: shared hit=3120)
        dn_6003_6004 (Buffers: shared hit=3119)
        dn_6005_6006 (Buffers: shared hit=3109)
        dn_6001_6002 (CPU: ex c/r=43, ex row=333761, ex cyc=14674178, inc cyc=23353907)
        dn_6003_6004 (CPU: ex c/r=43, ex row=333676, ex cyc=14630224, inc cyc=23169148)
        dn_6005_6006 (CPU: ex c/r=44, ex row=332563, ex cyc=14914017, inc cyc=23381862)
  4 --Seq Scan on public.vote_record_memory
        dn_6001_6002 (actual time=0.012..103.650 rows=333761 loops=1) (projection time=28.200)
        dn_6003_6004 (actual time=0.011..102.026 rows=333676 loops=1) (projection time=27.823)
        dn_6005_6006 (actual time=0.014..101.591 rows=332563 loops=1) (projection time=28.268)
        dn_6001_6002 (Buffers: shared hit=3120)
        dn_6003_6004 (Buffers: shared hit=3119)
        dn_6005_6006 (Buffers: shared hit=3109)
        dn_6001_6002 (CPU: ex c/r=26, ex row=333761, ex cyc=8679729, inc cyc=8679729)
        dn_6003_6004 (CPU: ex c/r=25, ex row=333676, ex cyc=8538924, inc cyc=8538924)
        dn_6005_6006 (CPU: ex c/r=25, ex row=332563, ex cyc=8467845, inc cyc=8467845)

                     User Define Profiling                      
----------------------------------------------------------------
Plan Node id: 2  Track name: coordinator get datanode connection
       cn_5001: (time=0.015 total_calls=1 loops=1)

                          ====== Query Summary =====                          
------------------------------------------------------------------------------
Datanode executor start time [dn_6001_6002, dn_6005_6006]: [0.053 ms,0.057 ms]
Datanode executor end time [dn_6001_6002, dn_6005_6006]: [0.037 ms,0.040 ms]
Remote query poll time: 234.453 ms, Deserialze time: 0.000 ms
System available mem: 819200KB
Query Max mem: 819200KB
Query estimated mem: 1034KB
Coordinator executor start time: 0.088 ms
Coordinator executor run time: 236.783 ms
Coordinator executor end time: 0.017 ms
Planner runtime: 0.375 ms
Query Id: 217017207043944553
Total runtime: 236.964 ms
```

















