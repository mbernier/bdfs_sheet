import sys, getopt, os
from modules.config import config_for_testing, config
import modules.base
import modules.cache 
import modules.caches.exception
import modules.caches.flat
import modules.caches.nested
import modules.config
import modules.dataMove
import modules.dataMoves.exception
import modules.dataMoves.originalbdfs_inventory.bdfs_inventory
import modules.dataMoves.originalbdfs_inventory.sarto_inventory
import modules.dataMoves.simple.simple.payroll
import modules.decorator
import modules.decorators.exception
import modules.exception
import modules.helper
import modules.helpers.exception
import modules.logger
import modules.loggers.exception
import modules.sheetProcessor
import modules.sheetProcessors.exception
import modules.sheetProcessors.bdfs_inventory
import modules.spreadsheet
import modules.spreadsheets.destination
import modules.spreadsheets.destinations.bdfs_inventory
import modules.spreadsheets.destinations.originalbdfs_inventory
import modules.spreadsheets.destinations.sarto_inventory
import modules.spreadsheets.destinations.simple_sheet
import modules.spreadsheets.exception
import modules.spreadsheets.source
import modules.spreadsheets.sources.bdfs_inventory
import modules.spreadsheets.sources.originalbdfs_inventory
import modules.spreadsheets.sources.sarto_inventory
import modules.spreadsheets.sources.simple_sheet
import modules.worksheet
import modules.worksheets.exception
import modules.worksheets.bases.doors
import modules.worksheets.bases.sarto_doors
import modules.worksheets.data
import modules.worksheets.destination
import modules.worksheets.destinations.bdfs_inventory
import modules.worksheets.destinations.originalbdfs_inventory
import modules.worksheets.destinations.sarto_inventory
import modules.worksheets.destinations.simple_sheet
import modules.worksheets.source
import modules.worksheets.sources.bdfs_inventory
import modules.worksheets.sources.originalbdfs_inventory
import modules.worksheets.sources.sarto_inventory
import modules.worksheets.sources.simple_sheet

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
# opts, args = getopt.getopt(sys.argv[1:], "chs:w:lvv",["capture=","ignore="])
# captureFound = False

# for opt, arg in opts: 
#     if opt == "--capture" and arg == "tee-sys":
#         captureFound = True

# if False == captureFound:
#     raise Exception("Try running `pytest --capture=tee-sys` instead")


####
#
# double check that our config_for_testing is working, before running
#   otherwise there are tests that will not run properly
#
####
if False == config("debug_decorator_returns"):
    raise Exception("For pytest, make sure the environment in config.ini contains debug_decorator_returns = True")