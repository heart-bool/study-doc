"""
    静态方法
    静态方法在python中和Java中的概念一致，属于类方法。

"""
from math import sqrt


class Triangle(object):

    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    @staticmethod
    def valid(a, b, c):
        return a + b > c and b + c > a and a + c > b

    def perimeter(self):
        return self._a + self._b + self._c

    def area(self):
        f = self.perimeter() / 2
        return sqrt(f * (f - self._a) * (f - self._b) * (f - self._c))


def main():
    a, b, c = 3, 3, 3
    if Triangle.valid(a, b, c):
        t = Triangle(a, b, c)
        print(t.perimeter())
        print(t.area())
    else:
        print("无法构成三角形")


if __name__ == '__main__':
    main()
