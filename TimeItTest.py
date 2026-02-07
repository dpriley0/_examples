# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 15:41:09 2025

@author: dpriley1
"""

import timeit

# Using list comprehension
list_time = timeit.timeit("[x**2 for x in range(1000)]", number=1000)

# Using map with lambda
map_time = timeit.timeit("list(map(lambda x: x**2, range(1000)))", number=1000)

print(f"List comprehension time: {list_time} seconds")
print(f"Map time: {map_time} seconds")
