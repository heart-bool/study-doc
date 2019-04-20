#!/usr/bin/env python3
# -*- coding: utf-8 -*-
list = [1, 2, 3, 4, 5, 6]
for item in list:
    print(item)

sum = 0
for item in list:
    sum = sum + item
print(sum)

sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)

L = ['Bart', 'Lisa', 'Adam']
for item in L:
    print("hello", item)