"""
列表list
"""

import sys


def main():
    list1 = [1, 4, 3, 2, 7, 6, 5, 9, 8, 10]
    print(list1)
    list2 = ['hello'] * 5
    print(list2)
    # 获取list长度
    print(len(list1))
    # 获取元素，使用下标的方式
    print(list1[0])
    print(list1[7])
    print(list1[-1])
    # 添加元素
    list1.append(11)
    print(list1)
    # 在指定位置插入新的元素
    list1.insert(1, 20)
    print(list1)
    list1 += [12, 13]
    print(list1)
    # 删除元素，以元素本身为参数
    list1.remove(20)
    print(list1)
    # 删除元素，以下标
    del list1[0]
    print(list1)

    # 切片操作，用法基本和字符串一致
    print(list1[1:4])
    print(list1[1::2])
    print(list1[::-1])

    list2 = ['wang', 'zhang', 'li', 'w', 'ouyang', 'linghuchong']
    # 排序
    # list.sort 会在原有数据上进行排序操作
    # list1.sort(reverse=True)
    # print(list1)
    # sorted 生成新的拷贝不会对原数据产生影响
    print(sorted(list2))
    # 指定排序条件
    print(sorted(list2, key=len))

    # 使用生成式语法创建列表
    list3 = [i for i in range(1, 30)]
    print(list3)
    # 创建列表之后元素就已经准备就绪所以占跟多的内存空间
    list3 = [i + str(j) for i in 'wangfeng' for j in range(3)]
    print(list3)
    print(sys.getsizeof(list3))

    # 请注意下面的代码创建的不是一个列表而是一个生成器对象
    # 通过生成器可以获取到数据但它不占用额外的空间存储数据
    # 每次需要数据的时候就通过内部的运算得到数据(需要花费额外的时间)
    list3 = (i + str(j) for i in 'wangfeng' for j in range(3))
    print(list3)
    print(sys.getsizeof(list3))
    for val in list3:
        print(val)

if __name__ == '__main__':
    main()
