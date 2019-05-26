"""
    字符串：字符序列，定义与Java中基本一致。在Python中，下标从1开始
"""

def main():
    str1 = 'hello, world!'
    # 通过len()获取字符串的长度
    print(len(str1))
    # 获取首字母大写的拷贝
    print(str1.capitalize())
    # 全大写
    print(str1.upper())
    # 查找字符串，存在返回指定值的位置，否则返回-1
    print(str1.find('wo'))
    print(str1.find('no'))
    # str.index类似于 find 但是在找不到指定字符将会报错
    # print(str1.index('wo'))
    # print(str1.index('no'))
    # 检查字符串是否以指定字符开头，返回 True/False
    print(str1.startswith("he"))
    print(str1.startswith("He"))
    # 检查字符串是否以指定字符结尾，返回 True/False
    print(str1.endswith("d!"))
    print(str1.endswith("rlD"))
    # 将字符串以指定的宽度居中并在两边填充指定的字符
    print(str1.center(50, '*'))
    # 将字符串以指定的宽度靠右并在两边填充指定的字符
    print(str1.rjust(50, '*'))
    # 将字符串以指定的宽度靠左并在两边填充指定的字符
    print(str1.ljust(50, '*'))
    str2 = 'abc123456'
    # 从字符串中取出指定位置的字符
    print(str2[2])
    # 字符串切片（从指定的开始下标到指定的结束下标，包括开始下标不包括结束下标，类似Java的indexOf()）
    print(str2[2:5])
    # 从下标2开始截取之后所有的字符
    print(str2[2:])
    # 跳跃截取 从指定下标的倍数值截取
    print(str2[2::2])
    # 反转字符串
    print(str2[::-1])
    # 反向截取
    print(str2[-3:-1])
    # 检查字符串是否由数字组成
    print(str2.isdigit())
    print(str2.isalnum())
    print(str2.isalpha())
    print(str2.isdecimal())
    print(str2.isidentifier())
    print(str2.islower())
    print(str2.isnumeric())
    print(str2.isprintable())
    print(str2.isspace())
    print(str2.istitle())
    print(str2.isupper())

if __name__ == '__main__':
    main()
