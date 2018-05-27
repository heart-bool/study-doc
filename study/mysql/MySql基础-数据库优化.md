
对mysql优化时一个综合性的技术，主要包括
1: 表的设计合理化(符合3NF)
2: 添加适当索引(index) [四种: 普通索引、主键索引、唯一索引unique、全文索引]
3: 分表技术(水平分割、垂直分割)
4: 读写[写: update/delete/add]分离
5: 存储过程 [模块化编程，可以提高速度]
6: 对mysql配置优化 [配置最大并发数my.ini, 调整缓存大小 ]
7: mysql服务器硬件升级
8: 定时的去清除不需要的数据,定时进行碎片整理(MyISAM)
9: sql优化

1  什么样的表才是符合3NF (范式)
    1. 3范式

        表的范式，是首先符合1NF, 才能满足2NF , 进一步满足3NF

        1NF: 即表的列的具有原子性,不可再分解，即列的信息，不能分解, 只有数据库是关系型数据库(mysql/oracle/db2/informix/sysbase/sql server)，就自动的满足1NF

        ☞ 数据库的分类
        关系型数据库: mysql/oracle/db2/informix/sysbase/sql server
        非关系型数据库: (特点: 面向对象或者集合)
        NoSql数据库: MongoDB(特点是面向文档)

        2NF: 表中的记录是唯一的, 就满足2NF, 通常我们设计一个主键来实现

        3NF: 即表中不要有冗余数据, 就是说，表的信息，如果能够被推导出来，就不应该单独的设计一个字段来存放.

2  Sql语句本身的优化

    1. 定位慢查询
        修改 MySQL 的默认慢查询时间
            show variables like 'long_query_time';
        设置慢查询时间
            set long_query_time=1;