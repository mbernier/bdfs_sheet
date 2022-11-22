# bdfs_sheet
Working with the BDFS spreadsheet - pulling and pushing data, using the sheets as a database

# Setup
1. Create your python environment, this is special per environment so you gotta figure this out
2. Get your credentials for OAuth for google sheets: https://docs.gspread.org/en/latest/oauth2.html#
3. You may need Matt to setup credentials for you and provide the access file, just ask him

# Running the script
To run the script (replacing `python3` with the appropriate python command for your environment):
```python3 run.py```


What this functionality can do:
1. Take in command line arguments for:
	a. listing all worksheets
	b. passing in specific worksheet names (but doing nothing with them)
	c. Overriding the default spreadsheet ID
2. Setup the Spreadsheet object
3. Get the available worksheets
4. Output the worksheet names to the console

To Add:
1. Parsing through the information in the sheet
	a. Throw errors when the data is incorrect or weird
	b. Build the handle
	c. Build the title
	d. Template for the content
	e. Look for other calculations that are in the spreadsheet and program them in
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
	a. Store the data in a shopify-data cache that mirrors the spreadsheet data cache
	b. compare to the data in the spreadsheet and determine the differences
	c. Take in command line information about what to update?
6. Ability to push Shopify data over the API
	a. Cache data -> API object processor
	b. Make the API call with the whole object, or just the changes? 
