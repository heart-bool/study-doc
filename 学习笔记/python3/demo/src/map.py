#!/usr/bin/env python3
# -*- coding: utf-8 -*-
map = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', }
val = map.get('a')
print(val)

if 's' in map:
    print('yes')
else:
    print("no")

val = map.get('s', 1)
print(val)