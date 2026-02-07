# -*- coding: utf-8 -*-
"""
@author: dpriley1                               [ Dan Riley, NASA MSFC, ER12 ]
Created on Tue May 27 12:10:26 2025

@Description: Example class implementation

"""
#%%
class RocketEngine:
    def __init__(self, thrust=100, propellant="RP-1", stages=1, **kwargs):
        self.thrust = thrust
        self.propellant = propellant
        self.stages = stages
        self.extra = kwargs



"""
Use the following syntax to use:

    from scra