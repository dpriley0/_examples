# -*- coding: utf-8 -*-
"""
@author: dpriley1                               [ Dan Riley, NASA MSFC, ER12 ]
Created on:                                        Tue Jul 22 09:08:24 2025

@Description:

#    BENCHMARKING syntax:       %timeit -r 5 -n 1000 %run script.py
"""

"""

    REFER TO GROK: https://grok.com/chat/a9cbb53e-135f-405a-8e65-03485052fa46

"""

import eel

# Initialize Eel with the 'web' folder containing frontend files
eel.init('web')

# Start the Eel app, opening index.html in a browser window
eel.start('index.html', size=(800, 600))
