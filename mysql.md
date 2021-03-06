# 待分类

## ！！MySQL 哪些情况会锁表

# 面试题

## 优化

**MySQL 数据库作发布系统的存储，一天五万条以上的增量，预计运维三年,怎么优化？**

```
（1）设计良好的数据库结构，允许部分数据冗余，尽量避免 join 查询，提高效率。
（2）选择合适的表字段数据类型和存储引擎，适当的添加索引。
（3）MySQL 库主从读写分离。
（4）找规律分表，减少单表中的数据量提高查询速度。
（5）添加缓存机制，比如 memcached，apc 等。
（6）不经常改动的页面，生成静态页面。
（7）书写高效率的 SQL。比如 SELECT * FROM TABEL 改为 SELECT field_1, field_2, field_3 FROM TABLE.
```



# MySQL理论

## MySQL整体逻辑架构

![Center](https://img-blog.csdn.net/20150514221010295?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvY3ltbV9saXU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

**第一层，即最上一层**，所包含的服务并不是MySQL所独有的技术。它们都是服务于C/S程序或者是这些程序所需要的 ：连接处理，身份验证，安全性等等。

**第二层值得关注**。这是MySQL的核心部分。通常叫做 SQL Layer。在  MySQL据库系统处理底层数据之前的所有工作都是在这一层完成的，包括权限判断， sql解析，行计划优化， query cache  的处理以及所有内置的函数(如日期,时间,数学运算,加密)等等。各个存储引擎提供的功能都集中在这一层，如存储过程，触发器，视 图等。

**第三层包括了存储引擎**。通常叫做StorEngine Layer  ，也就是底层数据存取操作实现部分，由多种存储引擎共同组成。它们负责存储和获取所有存储在MySQL中的数据。就像Linux众多的文件系统  一样。每个存储引擎都有自己的优点和缺陷。服务器是通过存储引擎API来与它们交互的。这个接口隐藏  了各个存储引擎不同的地方。对于查询层尽可能的透明。这个API包含了很多底层的操作。如开始一个事物，或者取出有特定主键的行。存储引擎不能解析SQL，互相之间也不能通信。仅仅是简单的响应服务器 的请求。

## mysql逻辑分层

client  ==>连接层 ==>服务层==>引擎层==>存储层 server

![](./img/2021-12-20_09-50.png)

| 名称   | 注释                                                         |
| ------ | ------------------------------------------------------------ |
| client |                                                              |
| 连接层 | 提供与客户端连接的服务                                       |
| 服务层 | 1.提供各种用户使用的接口(增删改查),sql解析<br/>	sql的解析过程比如:<br/>	from ... on ... where ... group by  ... having ... select ... order by ... limit<br/>2.提供SQL优化器(MySQL Query Optimizer),重写查询,决定表的读取顺序,选择合适的索引<br/>	mysql的hint关键字有很多比如:SQL_NO_CACHE FORCE_INDEX SQL_BUFFER_RESULT |
| 引擎层 | innoDB和MyISAM<br/>innoDB:事务优先(适合高并发修改操作;行锁)<br/><br/>MyISAM:读性能优先<br/>show engines;查询支持哪些引擎<br/><br/>查看当前默认的引擎 show variables like '%storage_engine%';default_storage_engine |
| 存储层 |                                                              |

## MySQL的引擎

### Mysql 中 MyISAM 和 InnoDB 的区别有哪些？

#### 区别

InnoDB支持事务，MyISAM不支持

对于InnoDB每一条SQL语言都默认封装成事务，自动提交，这样会影响速度，所以最好把多条SQL语言放在begin和commit之间，组成一个事务；

InnoDB支持外键，而MyISAM不支持。对一个包含外键的InnoDB表转为MYISAM会失败；

InnoDB是聚集索引，数据文件是和索引绑在一起的，必须要有主键，通过主键索引效率很高。

但是辅助索引需要两次查询，先查询到主键，然后再通过主键查询到数据。因此主键不应该过大，因为主键太大，其他索引也都会很大。

而MyISAM是非聚集索引，数据文件是分离的，索引保存的是数据文件的指针。主键索引和辅助索引是独立的。

InnoDB不保存表的具体行数，执行select count(*) from table时需要全表扫描。而MyISAM用一个变量保存了整个表的行数，执行上述语句时只需要读出该变量即可，速度很快；

Innodb不支持全文索引，而MyISAM支持全文索引，查询效率上MyISAM要高；

#### 如何选择

是否要支持事务，如果要请选择innodb，如果不需要可以考虑MyISAM；

如果表中绝大多数都只是读查询，可以考虑MyISAM，如果既有读写也挺频繁，请使用InnoDB

系统奔溃后，MyISAM恢复起来更困难，能否接受；

MySQL5.5版本开始Innodb已经成为Mysql的默认引擎(之前是MyISAM)，说明其优势是有目共睹的，如果你不知道用什么，那就用InnoDB，至少不会差。

### MyISAM

#### MyISAM 表格将在哪里存储，并且还提供其存储格式？

每个 MyISAM 表格以三种格式存储在磁盘上：

（1）·“.frm”文件存储表定义

（2）·数据文件具有“.MYD”（MYData）扩展名

（3）索引文件具有“.MYI”（MYIndex）扩展名

### InnoDB

####  mysql聚簇索引和非聚簇索引的区别

##### **1) 聚集索引**

表数据按照索引的顺序来存储的，也就是说索引项的顺序与表中记录的物理顺序一致。对于聚集索引，叶子结点即存储了真实的数据行，不再有另外单独的数据页。 在一张表上最多只能创建一个聚集索引，因为真实数据的物理顺序只能有一种。

##### **2) 非聚集索引**

表数据存储顺序与索引顺序无关。对于非聚集索引，叶结点包含索引字段值及指向数据页数据行的逻辑指针，其行数量与数据表行数据量一致。

总结一下：聚集索引是一种稀疏索引，数据页上一级的索引页存储的是页指针，而不是行指针。而对于非聚集索引，则是密集索引，在数据页的上一级索引页它为每一个数据行存储一条索引记录。

## 索引

### key和index的区别

1. key 是数据库的物理结构，它包含两层意义和作用，一是约束（偏重于约束和规范数据库的结构完整性），二是索引（辅助查询用的）。包括primary key, unique key, foreign key 等
2. index是数据库的物理结构，它只是辅助查询的，它创建时会在另外的表空间（mysql中的innodb表空间）以一个类似目录的结构存储。索引要分类的话，分为前缀索引、全文本索引等；



### B树与B+树

#### B树

每个节点都存储key和data，所有节点组成这棵树，并且叶子节点指针为null。

![](https://img-blog.csdnimg.cn/20190705082348947.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3podXlhbmxpbjA5,size_16,color_FFFFFF,t_70)

#### B+树

**只有叶子节点存储data**，叶子节点包含了这棵树的**所有键值**，叶子节点不存储指针。

![](https://img-blog.csdnimg.cn/20190705082430929.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3podXlhbmxpbjA5,size_16,color_FFFFFF,t_70)

后来，在B+树上增加了**顺序访问指针**，也就是每个叶子节点增加一个指向相邻叶子节点的指针，这样一棵树成了数据库系统实现索引的首选数据结构。

存储数据量：假设一个key占10个字节，可以存入4千万+。

一般情况下，3-4层的B+树支持千万级别索引。

### 为什么使用数据索引能提高效率

1. 数据索引的存储是有序的
2. 在有序的情况下，通过索引查询一个数据是无需遍历索引记录的
3. 极端情况下，数据索引的查询效率为二分法查询效率，趋近于 log2(N)

### 索引下推

（index condition pushdown ）简称ICP，在**Mysql5.6**的版本上推出，用于优化查询。

在不使用ICP的情况下，在使用**非主键索引（又叫普通索引或者二级索引）**进行查询时，存储引擎通过索引检索到数据，然后返回给MySQL服务器，服务器然后判断数据是否符合条件 。

在使用ICP的情况下，如果存在某些被索引的列的判断条件时，MySQL服务器将这一部分判断条件传递给存储引擎，然后由存储引擎通过判断索引是否符合MySQL服务器传递的条件，只有当索引符合条件时才会将数据检索出来返回给MySQL服务器 。

**索引条件下推优化可以减少存储引擎查询基础表的次数，也可以减少MySQL服务器从存储引擎接收数据的次数**。 

#### Mysql5.6之前的版本

- 5.6之前的版本是没有索引下推这个优化的，因此执行的过程如下图：

![img](./img/16401639821.png)

会忽略age这个字段，直接通过name进行查询，在(name,age)这课树上查找到了两个结果，id分别为2,1，然后拿着取到的id值一次次的回表查询，因此这个过程需要**回表两次**。

#### Mysql5.6及之后版本

- 5.6版本添加了索引下推这个优化，执行的过程如下图：

![img](./img/16401639402.png)

- InnoDB并没有忽略age这个字段，而是在索引内部就判断了age是否等于20，对于不等于20的记录直接跳过，因此在(name,age)这棵索引树中只匹配到了一个记录，此时拿着这个id去主键索引树中回表查询全部数据，这个过程只需要**回表一次**。

## 锁

### Mysql中的锁

| 锁     | 开销               | 加锁效率 | 死锁     | 锁定粒度           | 锁冲突概率 | 并发度 |
| ------ | ------------------ | -------- | -------- | ------------------ | ---------- | ------ |
| 表级锁 | 小                 | 快       | 不会出现 | 大                 | 最高       | 最低   |
| 行级锁 | 大                 | 慢       | 会出现   | 最小               | 最低       | 最高   |
| 页面锁 | 界于表锁和行锁之间 | -        | 会出现   | 界于表锁和行锁之间 | -          | 一般   |

# MySQL数据类型

## 字符串

注：MySQL中utf8并不是真正的UTF-8,真正的UTF-8占用4个字节的空间，对应在mysql中是utf8mb4编码。

### char与varchar

#### 介绍

char使用固定长度的空间进行存储，char(4)存储4个字符，根据编码方式的不同占用不同的字节。

varchar保存可变长度的字符串，使用额外的一个或两个字节存储字符串长度。

#### 对比

对于**经常改变的值**，char优于varchar，原因是固定长度的行不容易产生碎片。

对于**很短的列**，char优于varchar，原因是varchar需要额外一个或两个字节存储字符串的长度。

char和varchar后面如果**有空格**，char会自动去掉空格后存储，varchar虽然不会去掉空格，但在进行字符串比较时，会去掉空格进行比较。 

# MySQL函数

## 序号函数

### rank()

并列排序，会**跳过重复**序号

### dense_rank()

并列排序，**不会跳过重复**序号

### row_number()

顺序排序，不跳过任何一个序号，就是**行号**

> `select`
>     `id,`
>     `name,`
>     `rank() over(order by score desc) rank,`
>     `row_number() over(order by score desc) row_number,`
>     `dense_rank() over(order by score desc) dense_rank`
> `from students;`
>
> `--------------------------------- 结果 ------------------------------------`
> `+----+----------+-------+------+------------+------------+`
> `| id | name     | score | rank | row_number | dense_rank |`
> `+----+----------+-------+------+------------+------------+`
> `|  1 | zhangsan |   100 |    1 |          1 |          1 |`
> `|  3 | wangwu   |   100 |    1 |          2 |          1 |`
> `|  2 | lisi     |    99 |    3 |          3 |          2 |`
> `|  5 | pjf      |    99 |    3 |          4 |          2 |`
> `|  6 | wzm      |    96 |    5 |          5 |          3 |`
> `|  4 | trx      |    90 |    6 |          6 |          4 |`

## NOW()和 CURRENT_DATE()有什么区别？ 

NOW()命令用于显示当前年份，月份，日期，小时，分钟和秒。

CURRENT_DATE()仅显示当前年份，月份和日期。

# MySQL优化

## 锁的优化策略

（1）读写分离

（2）分段加锁

（3）减少锁持有的时间

（4）多个线程尽量以相同的顺序去获取资源

不能将锁的粒度过于细化，不然可能会出现线程的加锁和释放次数过多，反而效率不如一次加一把大锁。

## 优化MySQL顺序

最好是按照以下顺序优化：

1. SQL语句及索引的优化
2. 数据库表结构的优化
3. 系统配置的优化
4. 硬件的优化

## MySQL慢查询该如何优化

1. 检查是否走了索引，如果没有则优化SQL利用索引
2. 检查所利用的索引，是否是最优索引
3. 检查所查字段是否都是必须的
4. 检查表中数据是否过多，是否应该进行分库分表了
5. 检查数据库实例所在机器的性能配置，是否太低，是否可以适当增加资源

## 索引优化

### 索引优化的时候需要注意什么

1.索引字段要尽可能少的占用存储空间

2.在满足业务系统的需求内，尽可能自增

3.索引字段尽可能不要为null

4.选择索引的时候，索引内容的重复值要尽可能少（大于80%）

5.只给常用字段添加索引

6.尽量避免索引失效

7.索引字段不要频繁修改

### 什么情况下应不建或少建索引

1、表记录太少

2、经常插入、删除、修改的表

3、数据重复且分布平均的表字段，假如一个表有10万行记录，有一个字段A只有T和F两种值，且每个值的分布概率大约为50%，那么对这种表A字段建索引一般不会提高数据库的查询速度。

4、经常和主字段一块查询但主字段索引值比较多的表字段



## Mysql语句执行顺序

1. from
2. on
3. join
4. where
5. group by
6. having
7. select
8. distinct
9. union
10. order by

### 案例

存在如下表格orders：

![img](./img/Center)

注：下面所有语句符合语法顺序(也不可能不符合，因为会报错^_^)，只分析其执行顺序：(join和on属于多表查询，放在最后展示)

#### 语句一

```
select a.Customer

from orders a

where a.Customer='Bush' or a.Customer = 'Adams'
```

分析一：首先是from语句找到表格，然后根据where得到符合条件的记录，最后select出需要的字段，结果如下：



![img](./img/2Center)

#### 语句二groupby

groupby要和聚合函数一起使用



```
select a.Customer,sum(a.OrderPrice)

from orders a

where a.Customer='Bush' or a.Customer = 'Adams'

group by a.Customer
```

分析二：在from，where执行后，执行group by，同时也根据group by的字段，执行sum这个聚合函数。这样的话得到的记录对group by的字段来说是不重复的，结果如下：
![img](./img/9Center)



#### 语句三having



```
select a.Customer,sum(a.OrderPrice)

from orders a

where a.Customer='Bush' or a.Customer = 'Adams'

group by a.Customer

having sum(a.OrderPrice) > 2000
```

分析三：由于where是在group之前执行，那么如何对group by的结果进行筛选，就用到了having，结果如下：



![img](./img/4Center)

#### 语句四distinct

（为测试，先把数据库中Adams那条记录的OrderPrice改为3000）



```
select distinct sum(a.OrderPrice)

from orders a

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 1700
```

分析四：将得到一条记录（没有distinct，将会是两条同样的记录）：



![img](./img/8Center)

#### 语句五union

完全是对select的结果进行合并（默认去掉重复的记录）：



```
select distinct sum(a.OrderPrice) As Order1

from orders a

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 1500

union

select distinct sum(a.OrderPrice) As Order1

from orders a

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 2000
```

分Ubuntu 添加打印机析五：默认去掉重复记录（想保留重复记录使用union all），结果如下：



![img](./img/32Center)

#### 语句六order by



```
select distinct sum(a.OrderPrice) As order1

from orders a

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 1500

union

select distinct sum(a.OrderPrice) As order1

from orders a

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 2000

order by order1


```

分析：升序排序，结果如下：



![img](./img/3Center)

#### 语句七limit



```
select distinct sum(a.OrderPrice) As order1

from orders a

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 1500

union

select distinct sum(a.OrderPrice) As order1

from orders a

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 2000

order by order1

limit 1
```

分析七：取出结果中的前1条记录，结果如下：



![img](./img/23Center)

#### 语句八

（上面基本讲完，下面是join 和 on)

`
select distinct sum(a.OrderPrice) As order1,sum(d.OrderPrice) As order2

from orders a

left join (select c.* from Orders c) d  

on a.O_Id = d.O_Id

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 1500

union

select distinct sum(a.OrderPrice) As order1,sum(e.OrderPrice) As order2

from orders a

left join (select c.* from Orders c) e  

on a.O_Id = e.O_Id

where a.Customer='Bush' or a.Customer = 'Adams' or a.Customer = 'Carter'

group by a.Customer

having sum(a.OrderPrice) > 2000

order by order1

limit 1
`

分析八：上述语句其实join on就是多连接了一张表，而且是两张一样的表，都是Orders。 执行过程是，在执行from关键字之后根据on指定的条件，把left join指定的表格数据附在from指定的表格后面，然后再执行where字句。



注：

1)使用distinct要写在所有要查询字段的前面，后面有几个字段，就代表修饰几个字段，而不是紧随distinct的字段；

2)group by执行后(有聚合函数)，group by后面的字段在结果中一定是唯一的，也就不需要针对这个字段用distinct；



## explain语法

在日常工作中，我们会有时会开慢查询去记录一些执行时间比较久的SQL语句，找出这些SQL语句并不意味着完事了，些时我们常常用到explain这个命令来查看一个这些SQL语句的执行计划，查看该SQL语句有没有使用上了索引，有没有做全表扫描，这都可以通过explain命令来查看。所以我们深入了解MySQL的基于开销的优化器，还可以获得很多可能被优化器考虑到的访问策略的细节，以及当运行SQL语句时哪种策略预计会被优化器采用。

```
-- 实际SQL，查找用户名为Jefabc的员工
select * from emp where name = 'Jefabc';
-- 查看SQL是否使用索引，前面加上explain即可
explain select * from emp where name = 'Jefabc';
```

![img](./img/512541-20180803142201303-545775900.png)

expain出来的信息有10列，分别是id、select_type、table、type、possible_keys、key、key_len、ref、rows、Extra

**概要描述：**

| explain中的列名 | 解释                     |
| --------------- | ------------------------ |
| id              | 选择标识符               |
| select_type     | 查询的类型               |
| table           | 输出结果集的表           |
| partitions      | 匹配的分区               |
| type            | 表的连接类型             |
| possible_keys   | 查询时，可能使用的索引   |
| key             | 实际使用的索引           |
| key_len         | 索引字段的长度           |
| ref             | 列与索引的比较           |
| rows            | 扫描出的行数(估算的行数) |
| filtered        | 按表条件过滤的行百分比   |
| Extra           | 执行情况的描述和说明     |

**下面对这些字段出现的可能进行解释：**

### 一、 **id**

SELECT识别符。这是SELECT的查询序列号

 **我的理解是SQL执行的顺序的标识，SQL从大到小的执行**

1. id相同时，执行顺序由上至下

2. 如果是子查询，id的序号会递增，id值越大优先级越高，越先被执行

3. id如果相同，可以认为是一组，从上往下顺序执行；在所有组中，id值越大，优先级越高，越先执行

```
-- 查看在研发部并且名字以Jef开头的员工，经典查询
explain select e.no, e.name from emp e left join dept d on e.dept_no = d.no where e.name like 'Jef%' and d.name = '研发部';
```

![img](./img/512541-20180803143413064-173136748.png)



### **二、select_type**

 ***示查询中每个select子句的类型***

(1) SIMPLE(简单SELECT，不使用UNION或子查询等)

(2) PRIMARY(子查询中最外层查询，查询中若包含任何复杂的子部分，最外层的select被标记为PRIMARY)

(3) UNION(UNION中的第二个或后面的SELECT语句)

(4) DEPENDENT UNION(UNION中的第二个或后面的SELECT语句，取决于外面的查询)

(5) UNION RESULT(UNION的结果，union语句中第二个select开始后面所有select)

(6) SUBQUERY(子查询中的第一个SELECT，结果不依赖于外部查询)

(7) DEPENDENT SUBQUERY(子查询中的第一个SELECT，依赖于外部查询)

(8) DERIVED(派生表的SELECT, FROM子句的子查询)

(9) UNCACHEABLE SUBQUERY(一个子查询的结果不能被缓存，必须重新评估外链接的第一行)



### **三、table**

显示这一步所访问数据库中表名称（显示这一行的数据是关于哪张表的），有时不是真实的表名字，可能是简称，例如上面的e，d，也可能是第几步执行的结果的简称



### **四、type**

对表访问方式，表示MySQL在表中找到所需行的方式，又称“访问类型”。

**常用的类型有**： ALL、index、range、 ref、eq_ref、const、system、NULL（从左到右，性能从差到好）

#### ALL

Full Table Scan， MySQL将遍历全表以找到匹配的行

#### index

 Full Index Scan，index与ALL区别为index类型只遍历索引树

#### range

只检索给定范围的行，使用一个索引来选择行

#### ref

表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值

#### eq_ref

类似ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用primary key或者 unique key作为关联条件

#### const、system

当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量，system是const类型的特例，当查询的表只有一行的情况下，使用system

#### NULL

MySQL在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。



### **五、possible_keys**

指出MySQL能使用哪个索引在表中找到记录，查询涉及到的字段上若存在索引，则该索引将被列出，但不一定被查询使用（该查询可以利用的索引，如果没有任何索引显示 null）

该列完全独立于EXPLAIN输出所示的表的次序。这意味着在possible_keys中的某些键实际上不能按生成的表次序使用。
如果该列是NULL，则没有相关的索引。在这种情况下，可以通过检查WHERE子句看是否它引用某些列或适合索引的列来提高你的查询性能。如果是这样，创造一个适当的索引并且再次用EXPLAIN检查查询



### **六、Key**

key列显示MySQL实际决定使用的键（索引），必然包含在possible_keys中

如果没有选择索引，键是NULL。要想强制MySQL使用或忽视possible_keys列中的索引，在查询中使用FORCE INDEX、USE INDEX或者IGNORE INDEX。



### **七、key_len**

表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度（key_len显示的值为索引字段的最大可能长度，并非实际使用长度，即key_len是根据表定义计算而得，不是通过表内检索出的）

不损失精确性的情况下，长度越短越好



### **八、ref**

列与索引的比较，表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值



### **九、rows**

 估算出结果集行数，表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数



### **十、Extra**

该列包含MySQL解决查询的详细信息,有以下几种情况：

Using where:不用读取表中所有信息，仅通过索引就可以获取所需数据，这发生在对表的全部的请求列都是同一个索引的部分的时候，表示mysql服务器将在存储引擎检索行后再进行过滤

Using temporary：表示MySQL需要使用临时表来存储结果集，常见于排序和分组查询，常见 group by ; order by

Using filesort：当Query中包含 order by 操作，而且无法利用索引完成的排序操作称为“文件排序”

```
-- 测试Extra的filesort
explain select * from emp order by name;
```

Using join buffer：改值强调了在获取连接条件时没有使用索引，并且需要连接缓冲区来存储中间结果。如果出现了这个值，那应该注意，根据查询的具体情况可能需要添加索引来改进能。

Impossible where：这个值强调了where语句会导致没有符合条件的行（通过收集统计信息不可能存在结果）。

Select tables optimized away：这个值意味着仅通过使用索引，优化器可能仅从聚合函数结果中返回一行

No tables used：Query语句中使用from dual 或不含任何from子句

```
-- explain select now() from dual;
```

## SQL语句优化举例

#### 1.where、order by 列上建立索引

对查询进行优化，应尽量避免全表扫描，首先应考虑在 where 及 order by 涉及的列上建立索引。

#### 2.避免在 where 中使用!=或<>操作符

应尽量避免在 where 子句中使用!=或<>操作符，否则将引擎放弃使用索引而进行全表扫描。

#### 3.避免在 where 中进行 null 值判断

应尽量避免在 where 子句中对字段进行 null 值判断，否则将导致引擎放弃使用索引而进行全表扫描，如：

select id from t where num is null

可以在num上设置默认值0，确保表中num列没有null值，然后这样查询：

select id from t where num=0

#### 4.避免在 where 中使用 or

应尽量避免在 where 子句中使用 or 来连接条件，否则将导致引擎放弃使用索引而进行全表扫描，如：

select id from t where num=10 or num=20

可以这样查询：

select id from t where num=10

union all

select id from t where num=20

#### 5.like注意事项

下面的查询也将导致全表扫描：

select id from t where name like '%abc%'

若要提高效率，可以考虑全文检索。

#### 6.慎用in 和 not in

in 和 not in 也要慎用，否则会导致全表扫描，如：

select id from t where num in(1,2,3)

对于连续的数值，能用 between 就不要用 in 了：

select id from t where num between 1 and 3

#### 7.避免在where 中使用参数

如果在 where 子句中使用参数，也会导致全表扫描。因为SQL只有在运行时才会解析局部变量，但优化程序不能将访问计划的选择推迟到运行时；它必须在编译时进行选择。然而，如果在编译时建立访问计划，变量的值还是未知的，因而无法作为索引选择的输入项。如下面语句将进行全表扫描：

select id from t where num=@num

可以改为强制查询使用索引：

select id from t with(index(索引名)) where num=@num

#### 8.避免在 where 中写表达式

应尽量避免在 where 子句中对字段进行表达式操作，这将导致引擎放弃使用索引而进行全表扫描。如：

select id from t where num/2=100

应改为:

select id from t where num=100*2

#### 9.避免在where中对使用函数

应尽量避免在where子句中对字段进行函数操作，这将导致引擎放弃使用索引而进行全表扫描。如：

select id from t where substring(name,1,3)='abc'--name以abc开头的id

select id from t where datediff(day,createdate,'2005-11-30')=0--'2005-11-30'生成的id

应改为:

select id from t where name like 'abc%'

select id from t where createdate>='2005-11-30' and createdate<'2005-12-1'

#### 10.NULL

不要在 where 子句中的“=”左边进行函数、算术运算或其他表达式运算，否则系统将可能无法正确使用索引。

#### 11.复合索引最左匹配原则

在使用索引字段作为条件时，如果该索引是复合索引，那么必须使用到该索引中的第一个字段作为条件时才能保证系统使用该索引，否则该索引将不会被使用，并且应尽可能的让字段顺序与索引顺序相一致。

#### 12.不要写一些没有意义的查询

不要写一些没有意义的查询，如需要生成一个空表结构：

select col1,col2 into #t from t where 1=0

这类代码不会返回任何结果集，但是会消耗系统资源的，应改成这样：

create table #t(...)

#### 13.用 exists 代替 in

很多时候用 exists 代替 in 是一个好的选择：

select num from a where num in(select num from b)

用下面的语句替换：

select num from a where exists(select 1 from b where num=a.num)

#### 14.索引列中不能有大量数据重复

并不是所有索引对查询都有效，SQL是根据表中数据来进行查询优化的，当索引列有大量数据重复时，SQL查询可能不会去利用索引，如一表中有字段sex，male、female几乎各一半，那么即使在sex上建了索引也对查询效率起不了作用。

#### 15.索引降低 insert 、 update 的效率

索引并不是越多越好，索引固然可以提高相应的 select 的效率，但同时也降低了 insert 及 update 的效率，因为 insert 或 update 时有可能会重建索引，所以怎系统配置的优化样建索引需要慎重考虑，视具体情况而定。一个表的索引数最好不要超过6个，若太多则应考虑一些不常使用到的列上建的索引是否有必要。

#### 16.避免更新 clustered 索引数据列

应尽可能的避免更新 clustered 索引数据列，因为 clustered 索引数据列的顺序就是表记录的物理存储顺序，一旦该列值改变将导致整个表记录的顺序的调整，会耗费相当大的资源。若应用系统需要频繁更新 clustered 索引数据列，那么需要考虑是否应将该索引建为 clustered 索引。

#### 17.尽量使用数字型字段

尽量使用数字型字段，若只含数值信息的字段尽量不要设计为字符型，这会降低查询和连接的性能，并会增加存储开销。这是因为引擎在处理查询和连接时会逐个比较字符串中每一个字符，而对于数字型而言只需要比较一次就够了。

#### 18.尽可能的使用 varchar/nvarchar 代替 char/nchar

尽可能的使用 varchar/nvarchar 代替 char/nchar ，因为首先变长字段存储空间小，可以节省存储空间，其次对于查询来说，在一个相对较小的字段内搜索效率显然要高些。

#### 19.用具体的字段列表代替“*”

任何地方都不要使用 select * from t ，用具体的字段列表代替“*”，不要返回用不到的任何字段。

#### 20.使用表变量来代替临时表

尽量使用表变量来代替临时表。如果表变量包含大量数据，请注意索引非常有限（只有主键索引）。

#### 21.避免频繁创建和删除临时表

避免频繁创建和删除临时表，以减少系统表资源的消耗。

#### 22.NULL

临时表并不是不可使用，适当地使用它们可以使某些例程更有效，例如，当需要重复引用大型表或常用表中的某个数据集时。但是，对于一次性事件，最好使用导出表。

#### 23.NULL

在新建**临时表**时，如果一次性插入数据量很大，那么可以使用 select into 代替 create table，避免造成大量 log ，以提高速度；如果数据量不大，为了缓和系统表的资源，应先create table，然后insert。

#### 24.NULL

如果使用到了临时表，在存储过程的最后务必将所有的临时表显式删除，先 truncate table ，然后 drop table ，这样可以避免系统表的较长时间锁定。系统配置的优化

#### 25.避免使用游标

尽量避免使用游标，因为游标的效率较差，如果游标操作的数据超过1万行，那么就应该考虑改写。

#### 26.NULL

使用基于游标的方法或临时表方法之前，应先寻找基于集的解决方案来解决问题，基于集的方法通常更有效。

#### 27.NULL

与临时表一样，游标并不是不可使用。对小型数据集使用 FAST_FORWARD 游标通常要优于其他逐行处理方法，尤其是在必须引用几个表才能获得所需的数据时。在结果集中包括“合计”的例程通常要比使用游标执行的速度快。如果开发时间允许，基于游标的方法和基于集的方法都可以尝试一下，看哪一种方法的效果更好。

#### 28.NULL

在所有的存储过程和触发器的开始处设置 SET NOCOUNT ON ，在结束时设置 SET NOCOUNT OFF 。无需在执行存储过程和触发器的每个语句后向客户端发送 DONE_IN_PROC 消息。

#### 29.避免向客户端返回大数据量

尽量避免向客户端返回大数据量，若数据量过大，应该考虑相应需求是否合理。

#### 30.避免大事务操作

尽量避免大事务操作，提高系统并发能力。

## 为什么用自增列作为主键

**在满足业务系统的情况下，尽可能选择自增**

1、如果我们定义了主键(PRIMARY KEY)，那么InnoDB会选择主键作为聚集索引。

如果没有显式定义主键，则InnoDB会选择第一个不包含有NULL值的唯一索引作为主键索引。

如果也没有这样的唯一索引，则InnoDB会选择内置6字节长的ROWID作为隐含的聚集索引(ROWID随着行记录的写入而主键递增，这个ROWID不像ORACLE的ROWID那样可引用，是隐含的)。

2、数据记录本身被存于主索引（一颗B+Tree）的叶子节点上，这就要求同一个叶子节点内（大小为一个内存页或磁盘页）的各条数据记录按主键顺序存放

因此每当有一条新的记录插入时，MySQL会根据其主键将其插入适当的节点和位置，如果页面达到装载因子（InnoDB默认为15/16），则开辟一个新的页（节点）

3、如果表使用自增主键，那么每次插入新的记录，记录就会顺序添加到当前索引节点的后续位置，当一页写满，就会自动开辟一个新的页

4、如果使用非自增主键（如果身份证号或学号等），由于每次插入主键的值近似于随机，因此每次新纪录都要被插到现有索引页得中间某个位置

此时MySQL不得不为了将新记录插到合适位置而移动数据，甚至目标页面可能已经被回写到磁盘上而从缓存中清掉，此时又要从磁盘上读回来，这增加了很多开销

同时频繁的移动、分页操作造成了大量的碎片，得到了不够紧凑的索引结构，后续不得不通过OPTIMIZE TABLE来重建表并优化填充页面。

## 分区分表

**推荐sharingsphere**

### 表分区有什么好处

1、**存储更多数据**。分区表的数据可以分布在不同的物理设备上，从而高效地利用多个硬件设备。和单个磁盘或者文件系统相比，可以存储更多数据

2、**优化查询**。在where语句中包含分区条件时，可以只扫描一个或多个分区表来提高查询效率；涉及sum和count语句时，也可以在多个分区上并行处理，最后汇总结果。

3、**分区表更容易维护**。例如：想批量删除大量数据可以清除整个分区。

4、**避免某些特殊的瓶颈**，例如InnoDB的单个索引的互斥访问，ext3问价你系统的inode锁竞争等。

### 分区表的限制因素

1. 一个表最多只能有1024个分区
2. MySQL5.1中，分区表达式必须是整数，或者返回整数的表达式。在MySQL5.5中提供了非整数表达式分区的支持。
3. 如果分区字段中有主键或者唯一索引的列，那么多有主键列和唯一索引列都必须包含进来。即：分区字段要么不包含主键或者索引列，要么包含全部主键和索引列。
4. 分区表中无法使用外键约束
5. MySQL的分区适用于一个表的所有数据和索引，不能只对表数据分区而不对索引分区，也不能只对索引分区而不对表分区，也不能只对表的一部分数据分区。

### MySQL支持的分区类型

1. **RANGE分区**： 这种模式允许将数据划分不同范围。例如可以将一个表通过年份划分成若干个分区
2. **LIST分区**： 这种模式允许系统通过预定义的列表的值来对数据进行分割。按照List中的值分区，与RANGE的区别是，range分区的区间范围值是连续的。
3. **HASH分区** ：这中模式允许通过对表的一个或多个列的Hash Key进行计算，最后通过这个Hash码不同数值对应的数据区域进行分区。例如可以建立一个对表主键进行分区的表。
4. **KEY分区** ：上面Hash模式的一种延伸，这里的Hash Key是MySQL系统产生的。

### Mysql分表和分区的区别、分库分表介绍与区别

#### 一、什么是mysql分表，分区

什么是分表，从表面意思上看呢，就是把一张表分成N多个小表

什么是分区，分区呢就是把一张表的数据分成N多个区块，这些区块可以在同一个磁盘上，也可以在不同的磁盘上

#### 二、mysql分表和分区有什么区别呢 

1、实现方式上

- mysql的分表是真正的分表，一张表分成很多表后，每一个小表都是完整的一张表，都对应三个文件，一个.MYD数据文件，.MYI索引文件，.frm表结构
- 分区不一样，一张大表进行分区后，他还是一张表，不会变成二张表，但是他存放数据的区块变多了。

2、提高性能上

- 分表重点是存取数据时，如何提高mysql并发能力上；
- 而分区呢，如何突破磁盘的读写能力，从而达到提高mysql性能的目的。

3、实现的难易度上

1、分表的方法有很多，用merge来分表，是最简单的一种方式。这种方式根分区难易度差不多，并且对程序代码来说可以做到透明的。如果是用其他分表方式就比分区麻烦了。
2、分区实现是比较简单的，建立分区表，根建平常的表没什么区别，并且对开代码端来说是透明的。

#### 三、mysql分表和分区有什么联系呢

1，都能提高mysql的性高，在高并发状态下都有一个良好的表面。

2，分表和分区不矛盾，可以相互配合的，对于那些大访问量，并且表数据比较多的表，我们可以采取分表和分区结合的方式（如果merge这种分表方式，不能和分区配合的话，可以用其他的分表试），访问量不大，但是表数据很多的表，我们可以采取分区的方式等。

#### 四、 分库分表存在的问题。

1、事务问题。

在执行分库分表之后，由于数据存储到了不同的库上，数据库事务管理出现了困难。如果依赖数据库本身的分布式事务管理功能去执行事务，将付出高昂的性能代价；如果由应用程序去协助控制，形成程序逻辑上的事务，又会造成编程方面的负担。

2、跨库跨表的join问题。

在执行了分库分表之后，难以避免会将原本逻辑关联性很强的数据划分到不同的表、不同的库上，这时，表的关联操作将受到限制，我们无法join位于不同分库的表，也无法join分表粒度不同的表，结果原本一次查询能够完成的业务，可能需要多次查询才能完成。

3、额外的数据管理负担和数据运算压力。

额外的数据管理负担，最显而易见的就是数据的定位问题和数据的增删改查的重复执行问题，这些都可以通过应用程序解决，但必然引起额外的逻辑运算，例如，对于一个记录用户成绩的用户数据表userTable，业务要求查出成绩最好的100位，在进行分表之前，只需一个order by语句就可以搞定，但是在进行分表之后，将需要n个order  by语句，分别查出每一个分表的前100名用户数据，然后再对这些数据进行合并计算，才能得出结果。

## MVCC

读不加锁，读写不冲突。在读多写少的OLTP应用中，读写不冲突是非常重要的，极大的增加了系统的并发性能，现阶段几乎所有的RDBMS，都支持了MVCC。

1. LBCC：Lock-Based Concurrency Control，基于锁的并发控制

2. MVCC：Multi-Version Concurrency Control

   基于多版本的并发控制协议。纯粹基于锁的并发机制并发量低，MVCC是在基于锁的并发控制上的改进，主要是在读操作上提高了并发量。

### 读操作的分类

1. **快照读 (snapshot read)**：读取的是记录的可见版本 (有可能是历史版本)，不用加锁（共享读锁s锁也不加，所以不会阻塞其他事务的写）
2. **当前读 (current read)**：读取的是记录的最新版本，并且，当前读返回的记录，都会加上锁，保证其他事务不会再并发修改这条记录

## 主从复制

### 主（Master）从（Slave）复制的工作过程

1） 在每个事务更新数据完成之前，master 在二进制日志记录这些改变。写入二进制日志完成后，master 通知存储引擎提交事务。

2） Slave 将 master 的 binary log 复制到其中继日志。首先 slave 开始一个工作线程（I/O），I/O 线程在 master 上打开一个普通的连接，然后开始 binlog dump process。binlog dump process 从 master 的二进制日志中读取事件，如果已经跟上 master，它会睡眠并等待 master 产生新的事件，I/O 线程将这些事件写入中继日志。

3） Sql slave thread（sql 从线程）处理该过程的最后一步，sql 线程从中继日志读取事件，并重放其中的事件而更新 slave 数据，使其与 master 中的数据一致，只要该线程与 I/O 线程保持一致，中继日志通常会位于 os 缓存中，所以中继日志的开销很小。

![img](https://img-blog.csdnimg.cn/20200304161751676.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMzOTQ1MjQ2,size_16,color_FFFFFF,t_70)

### 主从复制的几种方式

    同步复制: master 的变化，必须等待 slave-1,slave-2,…,slave-n 完成后才能返回。 这样，显然不可取，也不是 MySQL 复制的默认设置。比如，在 WEB 前端页面上，用户增加了条记录，需要等待很长时间。
    
    异步复制:如同 AJAX 请求一样。master 只需要完成自己的数据库操作即可。至于 slaves 是否收到二进制日志，是否完成操作，不用关心，MySQL 的默认设置。
    
    半同步复制:master 只保证 slaves 中的一个操作成功，就返回，其他 slave 不管。 这个功能，是由 google 为 MySQL 引入的。

随着应用的日益增长，读操作很多，我们可以扩展 slave，但是如果 master 满足不了写操作了，怎么办呢？

可以分库【垂直拆分】，分表【水平拆分】。

### ！！MTS

## 读写分离

**推荐sharingsphere**

读写分离就是在主服务器上修改，数据会同步到从服务器，从服务器只能提供读取数据，不能写入，实现备份的同时也实现了数据库性能的优化，以及提升了服务器安全。

在这里插入图片描述

前较为常见的 Mysql 读写分离分为以下两种：

### 基于程序代码内部实现

在代码中根据 select 、insert 进行路由分类，这类方法也是目前生产环境下应用最广泛的。优点是性能较好，因为程序在代码中实现，不需要增加额外的硬件开支，缺点是需要开发人员来实现，运维人员无从下手。

### 基于中间代理层实现

代理一般介于应用服务器和数据库服务器之间，代理数据库服务器接收到应用服务器的请求后根据判断后转发到，后端数据库，有以下代表性的程序。

    mysql_proxy。mysql_proxy 是 Mysql 的一个开源项目，通过其自带的 lua 脚本进行 sql 判断。

不是所有的应用都能够在基于程序代码中实现读写分离，像一些大型的 java 应用，如果在程序代码中实现读写分离对代码的改动就较大，所以，像这种应用一般会考虑使用代理层来实现。
