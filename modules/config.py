import configparser
config_obj = configparser.ConfigParser()
config_obj.read("config.ini")

#get the settings that determine the current environment
#to make the code use production, set environment = production in the config.ini
current_config = config_obj["current"]

# get the environment that we care about right now
config = config_obj[current_config["environment"]]