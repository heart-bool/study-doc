# MySQL存储引擎

## 简介

在MySQL中，支持多种类型的存储引擎。如下:

- InnoDB
- MyISAM
- MEMORY
- CSV
- ARCHIVE
- BLACKHOLE
- MERGE
- FEDERATED

### 查询存储引擎

1. SHOW ENGINES 命令

   1. ```sql
      SHOW ENGINES;
      ```

2. 查询 INFOMATION_SCHEMA.ENGINES

   1. ```sql
       SELECT * FROM INFORMATION_SCHEMA.ENGINES;
       ```

## InnoDB

### 简介

`InnoDB`是一种平衡高可靠性和高性能的存储引擎。在MySQL 5.7 中，`InnoDB`是默认的存储引擎。除非在配置了其他存储引擎的情况下，默认创建的表都将使用`InnoDB`存储引擎

### InnoDB的主要优势

- 具有事务的功能
- 支持行级锁来提高并发性能，支持表的并发读写
- 每个InnoDB表都有一个聚簇索引的主键索引
- 外键支持

![image-20190402181301082](/Users/bool/Library/Application Support/typora-user-images/image-20190402181301082.png)

### 使用InnoDB表的好处

- 提供自动的崩溃恢复。当服务器宕机之后，InnoDB崩溃恢复会自动完成在崩溃之前提交的所有更改，并撤销所有未提交的更改
- 提供自维护的缓存池，包括数据表，索引
- 提供数据校验机制。如果数据在磁盘或内存中被损坏，校验机制会在使用之前提醒我们伪造数据
- 自动优化主键列
- 插入更新删除等操作通过更改缓存的自动机制来进行优化。
- 对巨型表查询时，当访问表中相同的行时，称为自适应哈希索引会接管以使这些查找更快，就像它们来自哈希表一样
- 支持压缩表和相关联的索引
- 创建和删除索引时，对性能和可用性的影响很小
- 截断表的效率较高

这里只列出一部分，具体参看

```http
https://dev.mysql.com/doc/refman/5.7/en/innodb-benefits.html
```

### InnoDB最佳实践

- 指定主键，主键查询的速度很高
- 指定外键，可以提高连接查询的效率
- 关闭自动提交。每秒承诺数百次会限制性能（受存储设备写入速度的限制）。

详细请查询

```http
https://dev.mysql.com/doc/refman/5.7/en/innodb-best-practices.html
```

MySQL 官方手册

```http
https://dev.mysql.com/doc/refman/5.7/en/
```

## MYISAM

## 锁 

- MYISAM 只支持表级锁，不支持行级锁

- InnoDB 默认行锁，也支持表级锁

#### 锁的分类

- 按锁的粒度划分，可分为表级锁，行级锁，页级锁
- 按锁级别划分，可分为共享锁，排它锁
- 按加锁方式划分，可分为自动锁，显式锁
- 按操作划分，可分为DML锁，DDL锁
- 按所用方式划分，可分为乐观锁，悲观锁

















































