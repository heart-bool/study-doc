"""
字符验证码
"""
import random


def generate_code(_check_len):
    all_str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    code = ''
    for _ in range(_check_len):
        code += all_str[random.randint(0, all_str.__len__() - 1)]

    return code


if __name__ == '__main__':

    while True:
        _check_len = int(input("请输入验证码长度: "))
        if _check_len == 0:
            print('game over')
            break
        code = generate_code(_check_len)
        print(code)
