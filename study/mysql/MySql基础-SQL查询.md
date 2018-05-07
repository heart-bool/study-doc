子查询

    就是将一条 select 语句用括号括起来嵌入另一个select语句.

子查询分为如下几类：

    按结果分类


        1. 标量子查询：返回单一值的标量，最简单的形式。
            是指子查询返回的是单一值的标量，如一个数字或一个字符串，也是子查询中最简单的返回形式。
            可以使用 = > < >= <= <> 这些操作符对子查询的标量结果进行比较，通常子查询的位置在比较式的右侧
            示例： 　　
            SELECT * FROM article WHERE uid = (SELECT uid FROM user WHERE status=1 ORDER BY uid DESC LIMIT 1)
            SELECT * FROM t1 WHERE column1 = (SELECT MAX(column2) FROM t2)
            SELECT * FROM article AS t WHERE 2 = (SELECT COUNT(*) FROM article WHERE article.uid = t.uid)

        2. 列子查询：返回的结果集是 N 行一列。
        3. 行子查询：返回的结果可以是多行多列(一行多列)
        4. 表子查询：子查询返回的结果是多行多列的二维表: 子查询返回的结果是当做二维表来使用


    按位置分类
        from 子查询. 子查询在from之后
            select * from (select * from table_name) s
        where 子查询. 子查询在where之后
            select * from table_name where id = (select id from table_name where id < 10)
        exists 子查询. 用来判断某些条件是否满足(跨表), exists是接在where之后: exists返回的结果只有0和1.
    IN 和 NOT IN
        用途是检索一个给定的比较值是否存在或排除一个特定的结果集中. 如下表
        +-----+--------+-----+
        | sid | sname  | cid |
        +-----+--------+-----+
        |   1 | 张三   |   1 |
        |   2 | 李四   |   1 |
        |   3 | 王五   |   1 |
        |   4 | 阿大撒 |   2 |
        |   5 | 速度   |   2 |
        |   6 | 爱的   |   2 |
        |   7 | 风骚的 |   3 |
        |   8 | 企鹅   |   3 |
        |   9 | 实打实 |   3 |
        +-----+--------+-----+
        查询除了 cid=1 以外的所有同学
        select * from student where cid not in(1)
        查询 cid=1 的所有同学
        select * from student where cid in(1)
        注 以上sql只做演示, 在实际使用中, 可以直接使用 cid = 1 或 cid != 1 来实现

联合查询

    将多次查询出来的结果及进行合并或拼接操作. 所有参与联合查询的select 语句字段数必须保持一致, 只要求字段一样, 跟数据类型无关

    select ... union [ALL DISINCT] select ...

    ALL         表示保留所有的结果集
    DISINCT     表示去掉所有的重复行 默认行为

    案例
        1. 查询同一张表,但是需求不同: 如查询学生信息, 男生身高升序, 女生身高降序.

        2. 多表查询: 多张表的结构是完全一样的,保存的数据(结构)也是一样的.

    注意
        在联合查询中 order by 不能直接使用,需要对查询语句使用括号才行；另外，要orderby生效: 必须搭配limit: limit使用限定的最大数即可.

连接查询


    将多张表进行记录的链接, 按照在表中指定的条件进行数据的拼接.

    分类
        内连接
            CROSS JOIN：
            SELECT * FROM class CROSS JOIN student where class.cid = student.cid

            INNER JOIN：和 CROSS JOIN 相似
            SELECT * FROM class INNER JOIN student where class.cid = student.cid

        外连接
            左关联: 左表为主表, 当左表的数据行没有匹配到右表的数据行时, 依然会显示出来.
            使用方式: 左表 left jion on  右表 条件
            例: SELECT * FROM student left join class ON student.cid = class.cid

            右关联: 右表为主表, 当右表的数据行没有匹配到左表的数据行时, 依然会显示出来.
            使用方式: 右表 right jion on 左表 条件
            例: SELECT * FROM student right join class ON student.cid = class.cid

视图

    视图是一种虚拟的数据表, 本身并不包含真正的数据. 但是它使用真正的数据或其他视图所定义出来的假数据表, 通常可以简化查询.

    创建视图
    	CREATE VIEW 视图名(列1，列2...) AS SELECT (列1，列2...) FROM ...;
    使用视图
        当成表使用就好
    修改视图
        CREATE OR REPLACE VIEW 视图名 AS SELECT [...] FROM [...];
    查看数据库已有视图
        SHOW TABLES [like...];（可以使用模糊查找）
    查看视图详情
        DESC 视图名或者SHOW FIELDS FROM 视图名
    视图条件限制
        [WITH CHECK OPTION]

























