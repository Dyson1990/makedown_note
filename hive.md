## 基本概念

### 注意点

1）Hive的数据存储在hdfs上，简单的说hive就是hdfs的简单一种映射，比如：hive的一张表映射hdfs上的一个文件，hive的一个数据库就映射为hdfs上的文件夹

2）Hive是一个计算框架，他是MapReduce的一种封装，实际上他的底层还是MR，Hive就是用人们熟悉的sql对数据进行分析的

3）Hive执行程序是运行在Yarn上的

### 缺点

1．Hive的HQL表达能力有限

（1）迭代式算法无法表达

（2）数据挖掘方面不擅长

2．Hive的效率比较低

（1）Hive自动生成的MapReduce作业，通常情况下不够智能化

（2）Hive调优比较困难，粒度较粗


### hive的架构

![](https://img-blog.csdn.net/20180811111042853?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N0dWRlbnRfX3NvZnR3YXJl/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

### Hive与传统数据库的区别

#### 相似点

Hive和数据库除了拥有类型的查询语言外，无其他相似

#### 不同点

|          | hive                                               | 传统数据库           |
| -------- | -------------------------------------------------- | -------------------- |
| 存储位置 | HDFS                                               | 块设备或本地文件系统 |
| 数据更新 | 不建议对数据改写                                   | 通常需要经常修改     |
| 执行引擎 | MapReduce                                          | 自己的执行引擎       |
| 执行速度 | 延迟高，但数据规模远超过数据库处理能力时，才有优势 | 延迟较低             |
| 数据规模 | 大规模的数据计算                                   | 数据规模较小         |
| 扩展性   | 随Hadoop的扩展性                                   | 扩展有限             |



## 排序（4个BY）

## HIVE调优

### 数据倾斜

### 调优参数

hive.map.aggr

hive.groupby.skewindata

### map side join

### 并行化执行

## 面试题

Hive自定义函数有哪几种

