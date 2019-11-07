"""
面向对象进阶
"""


class Person(object):
    """
        1. @property装饰器：
            相当于java中定义getter和setter方法

        2. __slots__：
            限定自定义对象只能绑定某些属性。该限定只对当前类有效，对子类不起作用。
                如下，限定Person类只能绑定'_name', '_age', '_gender'这三个属性，绑定 gender1时，将会报错

        3. 静态方法和类方法：
            和java中的概念基本一致，只是语法上的区别
            Python中定义静态方法的方式为使用 @staticmethod 装饰器。
    """
    __slots__ = ('_name', '_age', '_gender')

    # def __init__(self, name, age, gender1):
    #     self._name = name
    #     self._age = age
    #     # AttributeError: 'Person' object has no attribute '_gender1'
    #     self._gender1 = gender1

    def __init__(self, name, age, gender):
        self._name = name
        self._age = age
        self._gender = gender

    @staticmethod
    def play():
        print('这是一个静态方法')

    def eat(self):
        print('这是一个类方法')

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age


def main():
    per = Person("wangfeng", 20, 1)
    per.age = 21

    print(per.name)
    print(per.age)

    Person.play()
    per.eat()


if __name__ == '__main__':
    main()
