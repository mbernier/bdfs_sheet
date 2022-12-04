import configparser
config_obj = configparser.ConfigParser()
config_obj.read("config.ini")

#get the settings that determine the current environment
#to make the code use production, set environment = production in the config.ini
current_config = config_obj["current"]

# set up the defaults first
config = config_obj["DEFAULT"]

# merge in the environment we care about
config = config_obj[current_config["environment"]]

# config["debug_decorator_returns"] = config.getboolean("debug_decorator_returns")
# config["debug_validations"] = config.getboolean("debug_validations")
# config["output_to_console"] = config.getboolean("output_to_console")