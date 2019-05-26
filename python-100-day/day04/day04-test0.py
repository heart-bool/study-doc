"""
循环结构 for in 和 while

for in:
    语法: for [当前值] in [待循环的列表]:
            // 代码块

while:
    语法: while 条件:
            // 代码块

和 java/C/C++ 一样，Python 中同样有continue和break，并且用法基本一致。

"""

# for in 求1~100的和
sum_for = 0
for x in range(101):
    sum_for += x
print('sum_for =', sum_for)

"""
    range():
    
    range可以产生一个不变的数值序列，这个序列通常用于循环中。
    
    例：
    
    range(1, 100) 可以产生1到99的整数序列
    range(1, 100, 2) 可以产生1到99的基数序列，其中2是步长，即数值序列的增量
"""

# while 求1~100的和
item = 0
sum_while = 0
while item < 101:
    sum_while += item
    item += 1
print('sum_while =', sum_while)

# for in 示例求1~100的奇数和, 在x大于80的情况下结束循环
sum_for_continue = 0
for x in range(101):
    if x % 2 != 0:
        continue
    else:
        sum_for_continue += x

    if x > 80:
        break
print('sum_for_continue =', sum_for_continue)

# while 示例求1~100的奇数和, 在x大于80的情况下结束循环
item_while = 0
sum_while_continue = 0
while item_while < 101:
    item_while += 1
    if item_while % 2 == 0:
        sum_while_continue += item_while
    else:
        continue

    if item_while > 80:
        break

print('sum_while_continue =', sum_while_continue)

# 循环嵌套
for i in range(1, 10):
    for j in range(1, i + 1):
        print('%d*%d=%d' % (i, j, (i * j)), end='\t')
    print()