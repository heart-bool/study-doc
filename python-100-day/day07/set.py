"""
set集合: 和java中的set差不多。元素不能重复。Python中的set提供更多更便利的操作，求交集、并集、差集等

"""


def main():
    # 定义set 由于set不能有重复元素 故set1只会存在 1，2，3，4，5
    set1 = {1, 2, 3, 4, 1, 4, 5, 2}
    print(set1)
    # 获取长度
    print(len(set1))
    # 生成集合
    set1 = {x for x in range(1, 10)}
    print(set1)
    set2 = set(range(1, 5))
    print(set2)

    # 删除元素
    set1.discard(5)
    print("set1 1=", set1)
    set1.discard(10)
    print('set1 2=', set1)
    # 使用remove函数删除元素
    set1.remove(1)
    print('set1 3=', set1)
    print('----')
    # 使用remove函数删除元素 当元素不存在时会报错 KeyError
    # set1.remove(10)
    # print('set1 remove=', set1)
    # 集合的交集、并集、差集、对称差运算
    print("set1 =", set1)
    print("set2 =", set2)

    # 本来以为list也支持这些操作，但是报错
    # set1  = list(set1)
    # set2  = list(set2)

    print('----交集----')
    print('&', set1 & set2)
    print('intersection', set1.intersection(set2))
    print('----并集----')
    print('|', set1 | set2)
    print('union', set1.union(set2))
    print('----差集----')
    print('-', set1 - set2)
    print('difference', set1.difference(set2))
    print('----对称差----')
    print('^', set1 ^ set2)
    print('symmetric_difference', set1.symmetric_difference(set2))

    # 判断子集和超集
    set2.discard(1)
    print(set2)
    print('----判断子集----')
    print(set2 <= set1)
    print('----判断超集----')
    print(set1 >= set2)

if __name__ == '__main__':
    main()
