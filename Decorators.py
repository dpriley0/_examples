# -*- coding: utf-8 -*-
"""
@author: dpriley1                               [ Dan Riley, NASA MSFC, ER12 ]
Created on Tue May 27 16:38:02 2025

@Description:

"""
#%%
def my_decorator(func):
    def wrapper():
        print("Before the function is called")
        func()
        print("After the function is called")
    return wrapper


def say_hello_world():
    print("Hello World!")

x = my_decorator(say_hello_world)

x()