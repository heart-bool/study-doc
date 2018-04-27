事务
    概念

    事务是作为一个不可分割的逻辑单元而被执行的一组SQL语句, 在执行的过程中, 如果某一步骤出错, 则会执行回滚操作.

    事务的特性(ACID原则), 是 Atomic(原子性) Consistent(稳定性) Isolated(隔离性) Durable(可靠性)
        原子性: 要么全部成功, 要么全部失败.
        稳定性: 数据库在事务执行之前和执行完毕之后都必须是稳定的.
        隔离性: 不同的事务之间不应该互相影响.
        持久性: 如果事务被执行成功, 它的影响将永久性的记录到数据库中.

    语法 start transaction; [需要执行的操作] commit;

    事务的保存点
        MySQL事务能够对一个事务进行部分回滚. 但是需要在事务过程中使用 savepoit 语句来设置一些称为保存点的标记.

        create table t (i int) engine=innodb;
        start transaction;
        insert into t values(1);
        savepoint my_savepoint;
        insert into t values(2);
        roback to savepoint my_savepoint;
        insert into t values(3);
        savepoint my_savepoint;
        commit;
        执行完成上面的SQL语句 在数据表中只会看到一条记录 roback to savepoint 表示回滚到某一个保存点

    事务的隔离性
