# -*- coding: utf-8 -*-
"""
@author: dpriley1                               [ Dan Riley, NASA MSFC, ER12 ]
Created on Tue Jun 17 14:41:06 2025

@Description: Setting up an ADVANCED (i.e. uses INTERMEDIATE METHODS) example
              config/settings file architecture


    WHY USE INTERMEDIATE METHODS (e.g. get_path, get_setting, get_engine_param)
    INSTEAD OF DIRECTLY ACCESSING VALUES IN main.py?

    1. Incorporation of Error Handling
    2. Convenience/Readability (method access a little bit shorter).    # mehhhhh
    3. Future Flexibility
        Maybe you decide later to add validation or **unit conversion**


"""
#%%
import os
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigManager:
    def __init__(self, config_file='config.yaml'):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            print(f"Warning: Config file {self.config_file} not found!")
            return {}

    def save_config(self):
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML not installed")
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config_data, f, default_flow_style=False)

    def set(self, section, key, value):
        """Set a configuration value and optionally save"""
        if section not in self.config_data:
            self.config_data[section] = {}
        self.config_data[section][key] = value

    def set_and_save(self, section, key, value):
        """Set a value and immediately save to file"""
        self.set(section, key, value)
        self.save_config()
        print(f"Updated {section}.{key} = {value} and saved to {self.config_file}")

    def get_path(self, key):
        """Get a file path from the config"""
        return self.config_data['paths'][key]

    def get_setting(self, key):
        """Get a setting value"""
        return self.config_data['settings'][key]

    def get_engine_param(self, key):
        """Get an engine parameter"""
        return self.config_data['engine_parameters'][key]

# Create a global instance that your scripts can import
config = ConfigManager()