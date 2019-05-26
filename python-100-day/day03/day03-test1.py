"""
分支结构 <if> 的使用
注意点: Python 中没有用大括号来构造代码块，而是使用缩进的方式来设置代码的层次结构（有点类似yaml文件格式）。
        如果在if条件成立时需要有多行执行语句的时候，只需要保持多行语句具有相同的缩进就可以了。
"""

# 基本使用方式
userName = input("请输入用户名: ")
password = input("请输入密码: ")
if userName == 'wangfeng' and password == '123456':
    print("身份验证成功")
else:
    print('身份验证失败')

# 嵌套使用方式
x = 10
y = 20
if x < 10:
    print("x > 10")
else:
    if x > y:
        print("x > y")
    else:
        print("x < y")