"""
函数/模块化/包/变量作用域
    函数：在Python中，使用def关键字来定义函数。命名规则和变量一致。代码6.1
        函数参数：跟Java 等语言有点区别。在Python中并不支持传统的函数的重载。
        在Python中函数的参数可以有默认值，同样可以使用可变参数。参数传递时也不必要按照函数参数定义的顺序。 代码6.2

        Python中可以在函数内部再定义函数，但只能在外层函数调用。代码6.3
    模块化：Python中每一个文件就是一个模块，使用 import 指令导入模块 代码6.4
        模块的名称：默认的，每个*.py文件的*就是该模块的名称。例如 test.py 的模块名称为 test
    包：类似于Java中的包，但在Python中，每一个包中都必须有一个 __init__.py，__init__.py可以是空的，也可以有内容。
        如果目录下没有__init__.py文件，Python会将这个目录当成一个普通的文件夹而不是一个包
    变量作用域：简单介绍，test1中详细介绍
        全局变量：全局变量的定义方式通过模块的 if __name__ == '__main__': 分支中定义的变量 代码6.5.1
            global：通常在需要修改全局变量的时候可以使用global关键字来指明某局部变量来自全局变量 代码6.5.2


"""


# 代码6.1
def defDemo():
    return 0


# 代码6.2
def defDemo2(a=0, b=1, c=2, *args):
    temp = a + b + c
    for i in args:
        temp += i
    return temp


print(defDemo2(3, 4, 5, 6, 7))


# 代码 6.3
def defDemo3():
    print('defDemo3')

    def inner():
        print('defDemo3.inner')

    inner()


defDemo3()

# 代码6.4
# 导包
from day06 import module1
from day06 import module2

# 调用模块函数
module1.test('hello world')
module2.test('bey world')


# 代码6.5.1
def foo():
    b = 'hello'

    def bar():  # Python中可以在函数内部再定义函数
        c = True
        print(a)
        print(b)
        print(c)

    bar()
    # print(c)  # NameError: name 'c' is not defined

# 代码6.5.2
def foo1():
    global a
    a = 200
    print(a)


if __name__ == '__main__':
    a = 100
    # print(b)  # NameError: name 'b' is not defined
    foo()
    foo1()