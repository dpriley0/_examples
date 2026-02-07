# -*- coding: utf-8 -*-
"""
@author: dpriley1                               [ Dan Riley, NASA MSFC, ER12 ]
Created on Tue Jun 17 15:27:51 2025

@Description:       ** Intended for DIRECT ACCESS from main.py **
                Strictly loading and error-checking logic below.

"""

#%%
import yaml
import os
import sys

def load_config(config_file='config.yaml'):
    if not os.path.exists(config_file):
        print(f"ERROR: Config file '{config_file}' not found!")
        print(f"Please create {config_file} in the same directory as this script.")
        sys.exit(1)  # Stop the program

    try:
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)

        # Check if the file was empty or invalid
        if config_data is None:
            print(f"ERROR: Config file '{config_file}' is empty or invalid!")
            sys.exit(1)

        return config_data

    except yaml.YAMLError as e:
        print(f"ERROR: Invalid YAML in config file '{config_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not read config file '{config_file}': {e}")
        sys.exit(1)

# Load the config once when this module is imported
config = load_config()