"""
求水仙花数

水仙花数: 三位数。数字 个 十 百 位的幂相加等于本身的数。例如 1*1*1+5*5*5+3*3*3=153

"""

# 1. 获取这个数的个十百位
num = input('请输入一个三位数: ')

if int(num) > 999 or int(num) < 100:
    print('不支持的数字')
nums = [int(i) for i in num]
print('个十百为分别为: ', nums)

# 2. 分别计算每个数的幂值并相加
sum_mi = 0
for i in nums:
    sum_mi += i * i * i

# 3. 判断输入的数是否等于相加的幂
if sum_mi == int(num):
    print("该数为水仙花数")
else:
    print('该数不是水仙花数')
