from modules.config import config


if False == config("debug_decorator_returns"):
    raise Exception("For pytest, make sure the environment in config.ini contains debug_decorator_returns = True")