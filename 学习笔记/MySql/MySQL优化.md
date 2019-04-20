# MySQL优化

## 优化SQL

### 1. 优化select语句

优化查询的主要考虑因素是：

- 首先检查where子句中的列是否可以添加索引
- 最大限度的减少全表扫描
- 调整MySQL用于缓存的内存区域的大小
- 处理锁的问题，查询的速度可能会受到同时访问表的其他会话的影响
- 使用EXPLAIN调整索引

### 2. where子句

1. 删除不必要的括号

   ```sql
   ((a AND b) AND c OR (((a AND b) AND (c AND d)))) 
   -> 
   (a AND b AND c) OR (a AND b AND c AND d)
   ```

2. 恒定折叠

   ```sql
   (a<b AND b=c) AND a=5
   -> b>5 AND b=c AND a=5
   ```

3. 恒定条件去重

   ```sql
    (b>=5 AND b=5) OR (b=6 AND 5=5) OR (b=7 AND 5=6)
   -> b=5 OR b=6
   ```

4. 尽量使用有索引的字段

5. 手册

   ```http
   https://dev.mysql.com/doc/refman/5.7/en/where-optimization.html
   ```

## 慢查询定位

### 

