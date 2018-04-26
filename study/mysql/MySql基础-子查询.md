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
        3. 行子查询：返回的结果集是一行 N 列。
        4. 表子查询：返回的结果集是 N 行 N 列。

     按位置分类

