import sys, getopt, os
from modules.config import config_for_testing, config

####
#
# This sets up the config for testing, for the entire pytest run
#   effectively sets the environment to verbose_debug, even if it's set to anything else
#
####
config_for_testing()

####
#
# Make sure we're using the right parameters on pytest
#
####
opts, args = getopt.getopt(sys.argv[1:], "chs:w:lvv",["capture=","ignore="])
captureFound = False

for opt, arg in opts: 
    if opt == "--capture" and arg == "tee-sys":
        captureFound = True

if False == captureFound:
    raise Exception("Try running `pytest --capture=tee-sys` instead")


####
#
# double check that our config_for_testing is working, before running
#   otherwise there are tests that will not run properly
#
####
if False == config("debug_decorator_returns"):
    raise Exception("For pytest, make sure the environment in config.ini contains debug_decorator_returns = True")