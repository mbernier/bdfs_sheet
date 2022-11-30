# Summary
We will use this code to simplify our world more than the original script. The problem with the original script is that is relied on manual intervention, where we had to download and re-upload data using the importing functionality of Shopify.

This code will rely on the Google Sheet called [BDFS Inventory](https://docs.google.com/spreadsheets/d/1RyODmeydoIlMO75xa5wIxHRxqnZWRkDcxWZyp6fK-H8/edit#gid=891609024) as the source of truth for the data. Rather than an amazon database (mostly for cost reasons at the moment) being able to swap this out at a later time is part of the reason for the Object Oriented code, that makes it much easier in the future than making changes to the manager code or the CSV logic I wrote previously.

From there, we will be able to pull the data and do things with it as needed (such as update multiple Shopify sites, update Juniper wholesale system, etc)

This will eventually scale to allow us to do the same for Doors.Forsale, including all of the doors that UnitedPorte provides. If we get another vendor, we can write similar scripts that will allow us to pull data and push it to the systems we care about.

We can then look into options for order processing as well.

## Where we're going
1. Pull the data from Google Sheets for BarnDoors
2. Pull data from BarnDoors.ForSale
3. Update Shopify when the spreadsheet data is newer than Shopify
4. Update/Generate the Juniper spreadsheet
5. Take Juniper live with wholesale doors on their network
6. Import all the doors to Doors.ForSale from UnitedPorte
7. Process and update the spreadsheet for all the doors on Doors.ForSale
8. Sync doors with Spreadsheet and DFS

# Setup
1. Create your python environment
2. Run `pip install -r requirements.txt`
    a. if you run into issues with pycairo, make sure to look at this [Stackoverflow comment](https://stackoverflow.com/a/61164149) for suggestions on how to fix
3. Get your credentials for OAuth for google sheets: https://docs.gspread.org/en/latest/oauth2.html#
4. You may need Matt to setup credentials for you and provide the access file, just ask him
5. If you're running sublime text (vscode is better), then you may want to have sublime [auto-replace tabs with spaces](https://coderwall.com/p/zvyg7a/convert-tabs-to-spaces-on-file-save) Suggest: set this on User prefs notin the `.sublime-project` file, for some reason it seems to work better that way

# Running the script
To run the script (replacing `python3` with the appropriate python command for your environment):
```python3 run.py```
You will need to include parameters for the script to run properly, otherwise it will not do anything.
```python3 run.py -h``` will give you more information
This was setup to allow for multiple functions to be possible, without changing the code or multiple run files


# What this functionality can do today (updated as changes are made):
*run.py*
- Calls the `Processor` functionality that we care about

*sheetProcessor*
Conductor code that allows specific functionality to be run against a sheet. Take in command line arguments and then calls the Spreadsheet functionality, support for:
    a. Listing all worksheets
    b. Passing in specific worksheet names (but doing nothing with them)
    c. Overriding the default spreadsheet ID
    d. Outputting all the worksheets names to the console

Relevant Files
- modules/sheetProcessor.py - Base Conductor
- modules/sheetProcessors/bdfs_inventory.py - configuration for BDFS
- modules/sheetProcessors/exception.py


*spreadsheet*
Wrapper for core google spreadsheets. If you want to do something for a specific spreadsheet or style of sheet, then extend this class into the specific class.
Provides functionality that allows for:
    a. Listing all worksheets
    b. Passing in specific worksheet names
    c. Outputting all the worksheet names to the console
Relevant Files:
- modules/spreadsheet.py - Base class for handling a google spreadsheet, wraps gspread
- modules/spreadsheets/bdfs_inventory.py - BDFS spreadsheet specifics
- modules/spreadsheets/exception.py - defined an exception so we can see what code threw an error


*worksheet*
Wrapper for a specific worksheet in a google sheet. Pulls all the rows data from the worksheet and stores it in a data store. Current Data Store: Nested Cache

Relevant Files:
- modules/worksheet.py - Base class for a google spreadsheet worksheet (a tab)
- modules/worksheets/bdfs_inventory.py - specifics for the BDFS inventory worksheets
- modules/worksheets/exception.py
- modules/worksheets/data.py - Worksheet Data class, wraps the NestedCache functionality to create a local copy of the data in the worksheet 

*validation*
Method and field validation code
Will validate features of parameters, is employed by decorators

*decorators*
@ methods that can be specified before a method call, to add functionality

Decorators:
    - debug - will call a logger method to add information about the method that is decorated 
    - validator - takes in some information to validate the parameters of the method

Relevant Files
- modules/decorator.py
- modules/decorators/exception.py

*helpers*
Shared methods in a Helper class that are used in multiple places to reduce duplication of code and standardize some specific actions.

Relevant Files
- modules/helper.py - Helper class with many shared static methods
- modules/helpers/exception.py

*caches*
- similar to an in-memory database, without all the features. 
- this functionality creates a controlled in memory storage
- allows storing rows of data and accessing the data by row, headername, or index
- keeps a copy of the data by header or index in each row
- index data has information about the headers and vice versa
- setters will make sure that the data is written/updated in both places

Relevant Files:
- modules/cache.py - roughly an abstract class
- modules/caches/flat.py - a wrapper for accessing and getting data from a dict
- modules/caches/nested.py - a list of flatCaches, pushes the parallel index/header data and manages accessing/writing it

*logger*
Wrapper for logging functionality, making it easier to pass information to the logger. 
Extending Logger or BaseClass will get you the logging methods in your class

Relevant Files
- modules/logger.py

*BaseClass*
Originally, this had the logging functionality, but that was broken out. Now this has a couple of helper methods wrapped up that were used in various places, but doesn't do much else.

*DataStore*
Was the first pass at WorksheetData and NestedCache, when the data was being used in the sheet and not locally. This is still here, because there is functionality that may be reusable, post refactor towards local data processing

## To Add:
0. Validations
    a. Add return data validation?
1. Parsing through the information in the sheet - in a Shopify generic (NOT DOOR SPECIFIC) way
    *DECIDE:* how do we want the information organized in the spreadsheet? Should it be organized by the categories that are in Shopify? Should there be a categorization mapping and a products table - referenced so that we can go back and forth? This needs to be figured out, as the structure can determine many things in the future. Right now, the spreadsheet is organized by door type.
    a. Throw errors when the data is incorrect or weird
    b. Build the handle
    c. Build the title
    d. Template for the content
    e. Look for other calculations that are in the spreadsheet and program them in
    f. Add functionality that ALWAYS updates the "update_date" field in the spreadsheet and relies on this for doing updates to Shopify or third parties
2. Configuration
    a. Retail pricing percentage
    b. Wholesale pricing percentage
3. Class for Spreadsheet object
    a. Pass in a listing item's data and all variations
    b. Calculate display price based on our price (just like the spreadsheet, without using the spreadsheet calculations)
    c. Store the data in a spreadsheet-data cache
4. Wholesale (Juniper) object - Need to be able to write to the Juniper spreadsheet
    //data is attached here https://mail.google.com/mail/u/0/#inbox/KtbxLzFrMSGKMkfHHTZlrlGDrSgMBLJjpL
    a. Update the descriptions using our template
    b. Update the pricing based on configuration
    c. Output a new Juniper file
5. Ability to pull Shopify data over the API
    a. Can we pull a subset of data from the website (like doors not updated in last 14 days?)
    b. Store the data in a shopify-data cache that mirrors the spreadsheet data cache
    c. compare to the data in the spreadsheet and determine the differences
    d. Take in command line information about what to update?
6. Ability to push Shopify data over the API
    a. Cache data -> API object processor
    b. Make the API call with the whole object, or just the changes?
7. Versioning of the sheet - storing locally in a database
    a. requires a way to pull the sheet version into memory to be used like the sheet
    b. Needs a way to go back and forth between versions
    c. Maybe a way to show the diffs?
    d. Possible to record the actions taken? remove empties, added columns, added rows, removed rows, updated data?
8. Consider moving the validators to another class object with static methods, allowing them to be used elsewhere too?
9. Hit the sarto inventory page to pull everything, update the main spreadsheet with inventory, and update the websites with inventory - so we can pull products up/down as inventory changes
