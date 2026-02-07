# -*- coding: utf-8 -*-
"""
@author: dpriley1                               [ Dan Riley, NASA MSFC, ER12 ]
Created on Tue Jun 17 14:49:15 2025

@Description: Setting up an example config/settings file architecture

"""
#%%
from config_manager import config


def main():
    # Get the paths you need
    input_path = config.get_path('input_data')
    output_path = config.get_path('output_results')

    # Get simulation settings
    max_iterations = config.get_setting('max_iterations')
    debug_mode = config.get_setting('debug_mode')

    # Get engine parameters
    chamber_pressure = config.get_engine_param('chamber_pressure')

    print(f"Reading data from: {input_path}")
    print(f"Chamber pressure: {chamber_pressure} Pa")
    print(f"Debug mode: {debug_mode}")

    # Your existing code here...


if __name__ == "__main__":
    main()





#%%
# To change a config setting on-the-fly
# Change values in memory
config.set('settings', 'max_iterations', 2000)
config.set('paths', 'input_data', '/new/experiment/data')

# Save all changes at once
config.save_config()

# Or change and save immediately
config.set_and_save('settings', 'tolerance', 0.0001)