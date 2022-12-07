#get the settings that determine the current environment
#to make the code use production, set environment = production in the config.ini

import configparser
config_obj = configparser.ConfigParser()
config_obj.read("config.ini")

# merge in the environment we care about
def config(field=None, current=None):

    environment = config_obj["current"].get('environment')
    config = config_obj[environment]

    if None != field:        
        return config_convert_bool(config, field)
    return config

def config_convert_bool(config, field):
    
    info = config[field]

    if info in ("True", "False"):
        return config.getboolean(field)
    else:
        return info

def config_for_testing():
    config_obj.set('current', 'environment', 'verbose_debug')