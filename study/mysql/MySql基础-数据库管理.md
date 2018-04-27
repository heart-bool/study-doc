数据库管理

   1.1 库级别的SQL语句

        · 选定数据库: use 用来选择使用一个默认的数据库,
            例如 use TEST;
            当然在用户权限允许的情况下直接使用数据库名称也可以直接访问该库下的数据表
            databaseName.tableName
            例如 TEST.user 表示访问 TEST 数据库中的 user 表, 不过一般我们不会这么做.

        · 创建数据库
            create database db_name;
            前提条件是, 数据库的名字是合法的,不能是已经存在的.创建数据库时,MySQL 会在它的数据库目录创建一个与该数据库名字相同的子目录,
            这个新的目录被称为数据库的子目录.并且服务器还会在里面创建一个db.opt文件用来保存数据库的属性

            完整语法
            create database 1[IF NOT EXISTS] db_name 2[CHARACTER SET charset] 3[COLLATE collation]
                1: 如果被创建的数据库已存在时会报错, 该选项表示只在数据库不存在时才执行创建
                2：默认情况下服务器级别的字符集和排序方式将成为新建数据库的默认字符集,如果只给出了 3 中的排序方式
                    则意味着使用 COLLATE 的名字的开头部分确定字符集
                3：指定数据库字符集排序方式

        · 查看现有数据库的定义
            show create database db_name;
                +----------+-----------------------------------------------------------------+
                | Database | Create Database                                                 |
                +----------+-----------------------------------------------------------------+
                | test     | CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET latin1 */ |
                +----------+-----------------------------------------------------------------+

        · 删除数据库
            drop database db_name;
            删除数据库时需要注意:
            如果 drop database 失效, 通常是因为数据库子目录还包含一些与数据库无关的对象和文件. 而 drop database 不会删除这类文件,在这种情况下,就必须手动的删除该数据库子目录,
            然后再执行 drop database

        · 更改数据库属性
            alert database 1[IF NOT EXISTS] db_name 2[CHARACTER SET charset] 3[COLLATE collation]

   1.2 表操作

        · 存储引擎(storage engine)
            MySQL 支持多种存储引擎, 也被称作`数据表处理器`
            +--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
            | Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
            +--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
            | InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
            | MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
            | MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
            | BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
            | MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
            | CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
            | ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
            | PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
            | FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
            +--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
            注 以上信息由 show engine 指令得出.
            书中的理论太多, 这里只列出两个MyISAM 和 InnoDB 的介绍
            1. MyISAM
                MyISAM 是MySQL 默认使用的存储引擎. 当然这是在你没有把服务器配置成其他默认引擎的情况下.
                主要提供的功能
                    键压缩功能. 它使用某种键压缩算法来保存连续的 相似的 字符串索引值. 另外, MyISAM 还可以压缩相似的数值索引值, 因为数值都是使用高位字节优先的方式保存的
                    低位字节的检索效率非常高, 所以高位字节很容易被压缩.
                    激活数值压缩的方法: 在创建MyISAM数据表时使用 pack_keys=1 的选项.

                    与其他存储引擎相比 MyISAM 为 自增(AUTO_INCREATMENT) 数据列提供了更多的功能.
                    每个MyIASM 数据表都有一个标志 服务器或者myisam程序在检查MyISAM数据表时会对这个标志进行设置. MyISAM还有一个标志来表明该数据表在上次使用后是不是被正常的关闭了。
                    当服务器宕机时，这个标志可以用来判断数据表是否需要检查和修复。 指令--> --myusam-recover. 这会让服务器每次打开一个 MyISAM 数据表时自动检查该数据表的标志并进行必要的数据表修复处理

                    支持全文索引， 但是需要通过 FULLTEXT 索引来实现
                    支持空间数据类型和 SPARIAL 索引

            2. InnoDB
                支持事务
                在系统崩溃后可以自动恢复
                外键和引用完整性支持  包括递归式删除和更新
                数据行级别的锁定和多版本共存，有比较好的并发性能
                存储引擎会把数据表集中存储在一共享的表空间里，而不会像大多数其他存储引擎那样为不同的数据表创建不同的文件。表空间就像是一个虚拟的文件系统管理所有的InnoDB数据表的内容，
                这样做的好处就是数据表的长度就可以超过文件系统对各个文件的最大长度的限制。

        · 创建表
            create table table_name {
                name    varchar(20),
                birth   data not null,
                weight  int,
                sex     enum('F','M')
            }
        · 删除表
            drop table table_name
        · 修改表
                修改表信息

                1.修改表名
                    alter table test_a rename to sys_app;
                2.修改表注释
                    alter table sys_application comment '系统信息表';

                修改字段信息
                1.修改字段类型和注释
                    alter table sys_application  modify column app_name varchar(20) COMMENT '应用的名称';
                2.修改字段类型
                    alter table sys_application  modify column app_name text;
                3.单独修改字段注释
                    目前没发现有单独修改字段注释的命令语句。
                4.设置字段允许为空
                    alter table sys_application  modify column description varchar(255) null COMMENT '应用描述';
                5.增加一个字段，设好数据类型，且不为空，添加注释
                    alert table sys_application add `url` varchar(255) not null comment '应用访问地址';
                6.增加主键
                    alter table t_app add aid int(5) not null ,add primary key (aid);
                7.增加自增主键
                    alter table t_app add aid int(5) not null auto_increment ,add primary key (aid);
                8.修改为自增主键
                    alter table t_app  modify column aid int(5) auto_increment ;
                9.修改字段名字(要重新指定该字段的类型)
                    alter table t_app change name app_name varchar(20) not null;
                10.删除字段
                    alter table t_app drop aid;
                11.在某个字段后增加字段
                    alter table `t_app` add column gateway_id int  not null default 0 AFTER `aid`； #(在哪个字段后面添加)
                12.调整字段顺序
                    alter table t_app  change gateway_id gateway_id int not null after aid ; #(注意gateway_id出现了2次)

   1.3 获取数据库元数据

        · show
            1. 列出服务器所有的数据库
                show databases;
            2. 查看给定数据库的创建信息
                show create database db_name;
            3. 查看数据库中的数据表列表
                show tables;
            4. 查看数据表的创建信息
                show create table table_name;
            5. 查看数据表中的索引
                show index from table_name;
            6. 查看数据表中的列
                show columns from table_name
            7. 查看数据库的数据表描述性信息
                show table status 或者 show table status from table_name;


























