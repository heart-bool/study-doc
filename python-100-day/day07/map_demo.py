"""
字典：类似于java中的map。属于可变的容器，以键值对形式存储数据，可以存储任何对象。
"""


def main():
    # 定义map
    map1 = {1: 'a', 2: 'b', 3: 'c'}
    print(map1)
    # 以建取值
    print(map1[1])
    print(map1.get(2))

    # 获取不存在的key，可以指定默认值，不指定时则返回None
    print(map1.get(4))
    print(map1.get(4, 'd'))
    # 添加
    # map1.update('4'= 'd')
    # print(map1.items())

    # 更新
    map1[2] = 'D'
    print(map1)

    # 遍历
    for key in map1:
        print(key, ':', map1[key])

    # 删除指定key元素
    map1.pop(1)
    print(map1)

    # 删除最后一个元素
    map1.popitem()
    print(map1)


if __name__ == '__main__':
    main()
