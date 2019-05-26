"""
求完美数

完美数: 所有约数相加等于其本身
"""

num = input('请输入一个数: ')

# 求该数的所有约数和
sum = 0
num = int(num)
for i in range(1, num):
    if num % i == 0:
        sum += i

if int(num) == sum:
    print('yes')
else:
    print('no')