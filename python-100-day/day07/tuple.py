"""
元组：与列表类似，但是元组的元素不能被修改。

    在多线程环境下可以规避线程安全的问题。元组在创建时间和空间占用都优于列表。

"""


def main():
    # 定义元组
    yz = ('wangfeng', 22, '162cm', '四川省南部县')
    print(yz)

    # 获取元组中的元素
    print(yz[0])
    print(yz[1])
    # 遍历
    for x in yz:
        print(x)

    # 尝试修改元组的元素
    # yz[0] = 'bool' TypeError

    # 对引用yz重新赋值后原来的元组将被垃圾回收
    yz = ('bool', 25, '162cm', '四川省南部县')
    print(yz)

    # 将元祖转换成列表
    person = list(yz)
    # 修改列表元素
    person[0] = 'wangfeng'
    print(person)

    # 将列表转换成元组
    yz = tuple(person)
    print(yz)


if __name__ == '__main__':
    main()


