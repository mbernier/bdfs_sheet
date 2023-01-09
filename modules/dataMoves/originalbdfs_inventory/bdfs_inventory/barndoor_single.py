from airium import Airium

from modules.decorator import Debugger
from modules.dataMove import DataMove
from pydantic import validate_arguments

class Sarto_Inventory_BDFS_BarnDoor_Single(DataMove):
    """Processes data from the Sarto Spreadsheet, barndoor_single worksheet over to the 
        BDFS Inventory sheet, which is a staging for bringin the data to Shopify
    """
    sourceClassPath = "sarto_inventory.Sarto_Inventory_Spreadsheet_Source"
    sourceWorksheetName = "barndoor_single"

    destinationClassPath = "bdfs_inventory.bdfs_inventories.barndoor_single.Bdfs_Inventory_BarnDoor_Single_Worksheet_Destination"
    destinationWorksheetName = ["barndoor_single"]

    destinationShopifyBase = 'https://barndoors.forsale/'

    @Debugger
    @validate_arguments
    def mapFields_barndoor_single(self, sourceData:dict): 
        """Handles the field level mapping from the Sarto inventory to what we need for BDFS Shopify"""

        # 'Type'
        sourceData['Type'] = 'Barn Door'

        # Item Count: 'Number of Doors' 
        sourceData['Item Count'] = sourceData['Type']

        # image URLs, up to 10 of them
        for counter in range(1,11):
            imageKey = f"Image {counter}"
            
            imageUrl = ""
            if imageKey in sourceData:
                imageUrl = sourceData[imageKey]
            
            imageSeo = "" # @todo define this
            
            sourceData[f"{imageKey} URL"] = imageUrl
            sourceData[f"{imageKey} SEO"] = imageSeo

        # 'Vendor'
        sourceData['Vendor Name'] = "Sarto Doors"
        
        # Vendor URL
        sourceData['Vendor URL'] = "https://unitedporte.us"

        # Vendor Identifier
        sourceData['Vendor Unique ID'] = sourceData['URL_key']
		
        # 'Vendor SKU'
        sourceData['Vendor SKU'] = sourceData['SKU']

		# 'Vendor Model Name
        sourceData['Vendor Model'] = sourceData['Model']

        # 'Shipping Cost'
        sourceData['Shipping Cost'] = 180
        
        # 'Shipping Method'
        sourceData['Shipping Method'] = "Vendor Delivered, 3rd Party Shippers"
        
        # 'Discount'
        sourceData['Discount'] = self.destinationWorksheet.data.discount

        # Has Glass - already in the sourceData
        #sourceData['Has Glass'] 
        
        # Glass Lites
        sourceData['Glass Lites'] = sourceData['Lites']

        # Already included in the source
        # sourceData['Has Hardware']
        # sourceData['Hardware Type']
        # sourceData['Hardware Color']

        # Items from here need all the other data defined first, so that they can be built
        # from the data above

        # 'Title'
        sourceData['Title'] = self.prepTitle(sourceData.copy())

        # 'SEO Title'
        sourceData['SEO Title'] = self.prepSeoTitle(sourceData.copy())

        # Description
        sourceData['Description'] = self.prepDescription(sourceData.copy())

    	# 'Shopify Handle'
        sourceData = self.prepShopifyHandle(sourceData.copy())

        # 'Shopify URL'
        sourceData['Shopify URL'] = f"{self.destinationShopifyBase}{sourceData['Shopify Handle']}"

		# 'Tags'
        sourceData = self.prepTags(sourceData.copy())

        # @todo need to find a way to signal which fields always get syncd from the destination
        # instead of forcing passing these over and having to dedupe later, if an expected field is not included in the sourceData:
        #   - if data is in destination, replace with destination version 
        #   - if data is NOT in destination, replace with equiv to None for that destination

		# 'Publish To Store'
        sourceData['Publish To Store'] = '' #The sarto data cannot tell us whether to publish, this will be syncd from elsewhere

		# 'Publish To Google'
        sourceData['Publish To Google'] = '' #The sarto data cannot tell us whether to publish, this will be syncd from elsewhere

		# 'Publish to Pinterest'
        sourceData['Publish To Pinterest'] = '' #The sarto data cannot tell us whether to publish, this will be syncd from elsewhere

		# 'Publish To Facebook & Instagram'
        sourceData['Publish To Facebook & Instagram'] = '' #The sarto data cannot tell us whether to publish, this will be syncd from elsewhere

		# 'Publish to Microsoft'
        sourceData['Publish To Microsoft'] = '' #The sarto data cannot tell us whether to publish, this will be syncd from elsewhere

		# 'Publish to Shop'
        sourceData['Publish To Shop'] = '' #The sarto data cannot tell us whether to publish, this will be syncd from elsewhere

        return sourceData
    



    def prepSeoTitle(self, data):
        # ['URL', 'URL_key', 'Title', 'Type', 
        # 'Has Glass', 'Glass Finish', 'Lites', 
        # 'Color', 'Finish',
        # 'Hardware Type', 'Hardware Color', 'Hardware', 
        # 'SKU', 'Model',
        # 'Materials', 'Door Thickness', 'Pre-drilled For Hardware',
        # 'Image 1 URL', 'Image 2 URL', 'Image 3 URL', 'Image 4 URL', 'Image 5 URL', 
        # 'Image 6 URL', 'Image 7 URL', 'Image 8 URL', 'Image 9 URL', 'Image 10 URL', 
        # 'Description', 'Shipping', 'Discount']

        """Builds the SEO Title from the other data provided"""
        pass

    def prepDescription(self, data):
        # ['URL', 'URL_key', 'Title', 'Type', 
        # 'Has Glass', 'Glass Finish', 'Lites', 
        # 'Color', 'Finish',
        # 'Hardware Type', 'Hardware Color', 'Hardware', 
        # 'SKU', 'Model',
        # 'Materials', 'Door Thickness', 'Pre-drilled For Hardware',
        # 'Image 1 URL', 'Image 2 URL', 'Image 3 URL', 'Image 4 URL', 'Image 5 URL', 
        # 'Image 6 URL', 'Image 7 URL', 'Image 8 URL', 'Image 9 URL', 'Image 10 URL', 
        # 'Description', 'Shipping', 'Discount']

        """Builds the Description from the other data in a standardized way"""
        
        a = Airium()

        with a.div():
            
            # Intro Paragraph
            with a.p():
                a('These Barn Doors are sized to match most interior door openings, for closets, bathrooms, and bedrooms.')

            a.br()

            # About This Door
            with a.p():
                with a.h2():
                    a('About this door:')
                with a.ul():
                    with a.li():
                        a('')
            
            # What's included
            with a.p():
                with a.h2():
                    a('Included: ')
                with a.ul():
                    with a.li():
                        a('Door')
                    with a.li():
                        a('Slide Rail')
                    with a.li():
                        a('Wheels')
                    with a.li():
                        a('Floor Guide (Plastic Fin)')
            with a.p():
                a('paragraph')



        output = str(a)  # casting to string extracts the value
        # or directly to UTF-8 encoded bytes:
        html_bytes = bytes(a)  # casting to bytes is a shortcut to str(a).encode('utf-8')


        """This barn door is the perfect size for any interior door such as bedrooms, closets, bathrooms.

            This door is manufactured from a single piece of wood, providing a strong core and sturdy construction that will last a long time.

            What's included: Door, Slide Rail, Wheels, and Floor Guide

            Specifications
            Finish: Veneer
            Materials: Solid MDF
            Door Thickness: 1 3/5"
            Glass: Frosted Glass
            Pre-drilled for hardware: No
            Includes
            Door
            Hardware:
            Rail with predrilled holes
            Hangers with wheels
            Door stops
            Floor guide
            Mounting screws

            SOUND ATTENUATION

            Get up to 30% noise reduction over standard doors due to the door's 1-3/5" thickness.

            Environmentally Friendly

            Premium decorative films are made from polypropylene. These films provide an outstanding painted surface look and feel. The doors are free from solvents, formaldehyde, and the Premium films are environmentally friendly. Our high quality surfaces makes it clean super easy and provide resistance against mechanical stress and chemicals."""


    def prepShopifyHandle(self, data):
        # ['URL', 'URL_key', 'Title', 'Type', 
        # 'Has Glass', 'Glass Finish', 'Lites', 
        # 'Color', 'Finish',
        # 'Hardware Type', 'Hardware Color', 'Hardware', 
        # 'SKU', 'Model',
        # 'Materials', 'Door Thickness', 'Pre-drilled For Hardware',
        # 'Image 1 URL', 'Image 2 URL', 'Image 3 URL', 'Image 4 URL', 'Image 5 URL', 
        # 'Image 6 URL', 'Image 7 URL', 'Image 8 URL', 'Image 9 URL', 'Image 10 URL', 
        # 'Description', 'Shipping', 'Discount']

        pass

    def prepTags(self, data):
        # ['URL', 'URL_key', 'Title', 'Type', 
        # 'Has Glass', 'Glass Finish', 'Lites', 
        # 'Color', 'Finish',
        # 'Hardware Type', 'Hardware Color', 'Hardware', 
        # 'SKU', 'Model',
        # 'Materials', 'Door Thickness', 'Pre-drilled For Hardware',
        # 'Image 1 URL', 'Image 2 URL', 'Image 3 URL', 'Image 4 URL', 'Image 5 URL', 
        # 'Image 6 URL', 'Image 7 URL', 'Image 8 URL', 'Image 9 URL', 'Image 10 URL', 
        # 'Description', 'Shipping', 'Discount']

        pass