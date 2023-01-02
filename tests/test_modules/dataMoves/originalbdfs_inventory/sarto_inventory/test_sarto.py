from collections import OrderedDict
import pytest
from modules.dataMoves.originalbdfs_inventory.sarto_inventory.sarto import Originalbdfs_Inventory_To_Sarto_Inventory

obj = Originalbdfs_Inventory_To_Sarto_Inventory()

worksheetName='slabs_single'
slabSourceData=OrderedDict([("Generate (add an 'x' for the one you want to generate", '114'), ('Inspect/Clean CSV before Import?', '-'), ('Confirmed 08/21', 'x'), ('Published', 'FALSE'), ('Title', 'Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('NoHeaderFound_5', '44.00'), ('Handle', 'white-solid-3-panel-wood-single-barn-door-slab'), ('Type', 'Single'), ('On BDFS', 'Yes'), ('Vendor', 'Sartodoors'), ('Glass', 'No'), ('Glass Lites', 'No'), ('Color', 'White'), ('Hardware', 'Slab'), ('SKU', 'sartodoors_2661_single_white_slab'), ('Tags', 'Barn Door, Single Barn Door, White, No Hardware, No Glass, sartodoors-2661'), ('original SKU or Sarto Title', 'sarto_2661-single-white18"x80"_slab'), ('Sarto SKU', '2661'), ('_3309_single_matte-white_frosted-glass_stainless-rail', 'Lucia_2661_single_white_slab_1.jpg'), ('Image 1 URL', 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2661_Single_White_slab_1.jpg?v=1637605012'), ('Image 1 SEO', 'Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 2 URL', 'https://unitedporte.us/media/catalog/product/cache/d263df706a409d1ef4cb15ae72241da3/c/d/cdn.shopify.com_s_files_1_1655_9629_files_design_1.jpg_v_1576676778_14.jpg'), ('Image 2 SEO', 'Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 3 URL', 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Felicia_3309_Single_Matte-White_Frosted_glass_black_rail_3_d6499017-c0d0-4243-90fa-19f172829f55.jpg'), ('Image 3 SEO', 'Barn Door Rail Hanging Instructions for Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 4 URL', 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2555_Single_White_clear-glass_black-rail_4.jpg'), ('Image 4 SEO', 'Internal Construction of Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 5 URL', ''), ('Image 5 SEO', ''), ('UnitedPorte URL', 'https://unitedporte.us/3-panel-slab-barn-door-lucia-2661-white-silk-sturdy-finished-wooden-kitchen-pantry-shaker-doors-pocket-closet-sliding'), ('Price Updated Date', ''), ('Cost: 18" x 80"', '346.40'), ('Cost: 24" x 80"', '356.80'), ('Cost: 28" x 80"', '356.80'), ('Cost: 30" x 80"', '356.80'), ('Cost: 32" x 80"', '356.80'), ('Cost: 36" x 80"', '356.80'), ('Cost: 42" x 80"', '356.80'), ('Cost: 18" x 84"', '386.40'), ('Cost: 24" x 84"', '386.40'), ('Cost: 28" x 84"', '386.40'), ('Cost: 30" x 84"', '386.40'), ('Cost: 32" x 84"', '386.40'), ('Cost: 36" x 84"', '386.40'), ('Cost: 42" x 84"', '445.60'), ('Cost: 18" x 96"', '505.60'), ('Cost: 24" x 96"', '505.60'), ('Cost: 28" x 96"', '505.60'), ('Cost: 30" x 96"', '505.60'), ('Cost: 32" x 96"', '505.60'), ('Cost: 36" x 96"', '505.60'), ('Cost: 42" x 96"', '635.20'), ('NoHeaderFound_52', ''), ('Price:18" x 80"', '666.61'), ('Price:24" x 80"', '679.30'), ('Price:28" x 80"', '679.30'), ('Price:30" x 80"', '679.30'), ('Price:32" x 80"', '679.30'), ('Price:36" x 80"', '679.30'), ('Price:42" x 80"', '679.30'), ('Price:18" x 84"', '715.41'), ('Price:24" x 84"', '715.41'), ('Price:28" x 84"', '715.41'), ('Price:30" x 84"', '715.41'), ('Price:32" x 84"', '715.41'), ('Price:36" x 84"', '715.41'), ('Price:42" x 84"', '787.63'), ('Price:18" x 96"', '860.83'), ('Price:24" x 96"', '860.83'), ('Price:28" x 96"', '860.83'), ('Price:30" x 96"', '860.83'), ('Price:32" x 96"', '860.83'), ('Price:36" x 96"', '860.83'), ('Price:42" x 96"', '1,018.94'), ('NoHeaderFound_74', ''), ('Profits:18" x 80"', '140.21'), ('Profits:24" x 80"', '142.50'), ('Profits:28" x 80"', '142.50'), ('Profits:30" x 80"', '142.50'), ('Profits:32" x 80"', '142.50'), ('Profits:36" x 80"', '142.50'), ('Profits:42" x 80"', '142.50'), ('Profits:18" x 84"', '149.01'), ('Profits:24" x 84"', '149.01'), ('Profits:28" x 84"', '149.01'), ('Profits:30" x 84"', '149.01'), ('Profits:32" x 84"', '149.01'), ('Profits:36" x 84"', '149.01'), ('Profits:42" x 84"', '162.03'), ('Profits:18" x 96"', '175.23'), ("Generate (add an 'x' for the one you want to generate_update_timestamp", 1672532165.7651799), ('Inspect/Clean CSV before Import?_update_timestamp', 1672532165.7661812), ('Confirmed 08/21_update_timestamp', 1672532165.767204), ('Published_update_timestamp', 1672532165.7683241), ('Title_update_timestamp', 1672532165.7693), ('NoHeaderFound_5_update_timestamp', 1672532165.77032), ('Handle_update_timestamp', 1672532165.771223), ('Type_update_timestamp', 1672532165.772272), ('On BDFS_update_timestamp', 1672532165.773196), ('Vendor_update_timestamp', 1672532165.774108), ('Glass_update_timestamp', 1672532165.7750258), ('Glass Lites_update_timestamp', 1672532165.7759821), ('Color_update_timestamp', 1672532165.776893), ('Hardware_update_timestamp', 1672532165.777795), ('SKU_update_timestamp', 1672532165.7787478), ('Tags_update_timestamp', 1672532165.7799911), ('original SKU or Sarto Title_update_timestamp', 1672532165.781122), ('Sarto SKU_update_timestamp', 1672532165.782059), ('_3309_single_matte-white_frosted-glass_stainless-rail_update_timestamp', 1672532165.782975), ('Image 1 URL_update_timestamp', 1672532165.7838879), ('Image 1 SEO_update_timestamp', 1672532165.7849889), ('Image 2 URL_update_timestamp', 1672532165.78592), ('Image 2 SEO_update_timestamp', 1672532165.786835), ('Image 3 URL_update_timestamp', 1672532165.787743), ('Image 3 SEO_update_timestamp', 1672532165.788647), ('Image 4 URL_update_timestamp', 1672532165.789557), ('Image 4 SEO_update_timestamp', 1672532165.7904582), ('Image 5 URL_update_timestamp', 1672532165.791359), ('Image 5 SEO_update_timestamp', 1672532165.7922518), ('UnitedPorte URL_update_timestamp', 1672532165.7931478), ('Price Updated Date_update_timestamp', 1672532165.794044), ('Cost: 18" x 80"_update_timestamp', 1672532165.79498), ('Cost: 24" x 80"_update_timestamp', 1672532165.796053), ('Cost: 28" x 80"_update_timestamp', 1672532165.796967), ('Cost: 30" x 80"_update_timestamp', 1672532165.797877), ('Cost: 32" x 80"_update_timestamp', 1672532165.7988439), ('Cost: 36" x 80"_update_timestamp', 1672532165.7997599), ('Cost: 42" x 80"_update_timestamp', 1672532165.800679), ('Cost: 18" x 84"_update_timestamp', 1672532165.80159), ('Cost: 24" x 84"_update_timestamp', 1672532165.802654), ('Cost: 28" x 84"_update_timestamp', 1672532165.80357), ('Cost: 30" x 84"_update_timestamp', 1672532165.804471), ('Cost: 32" x 84"_update_timestamp', 1672532165.805388), ('Cost: 36" x 84"_update_timestamp', 1672532165.806389), ('Cost: 42" x 84"_update_timestamp', 1672532165.807648), ('Cost: 18" x 96"_update_timestamp', 1672532165.808565), ('Cost: 24" x 96"_update_timestamp', 1672532165.809471), ('Cost: 28" x 96"_update_timestamp', 1672532165.810375), ('Cost: 30" x 96"_update_timestamp', 1672532165.811279), ('Cost: 32" x 96"_update_timestamp', 1672532165.812192), ('Cost: 36" x 96"_update_timestamp', 1672532165.813349), ('Cost: 42" x 96"_update_timestamp', 1672532165.8143628), ('NoHeaderFound_52_update_timestamp', 1672532165.815286), ('Price:18" x 80"_update_timestamp', 1672532165.816191), ('Price:24" x 80"_update_timestamp', 1672532165.8171031), ('Price:28" x 80"_update_timestamp', 1672532165.8182452), ('Price:30" x 80"_update_timestamp', 1672532165.81916), ('Price:32" x 80"_update_timestamp', 1672532165.820074), ('Price:36" x 80"_update_timestamp', 1672532165.820987), ('Price:42" x 80"_update_timestamp', 1672532165.821895), ('Price:18" x 84"_update_timestamp', 1672532165.822804), ('Price:24" x 84"_update_timestamp', 1672532165.8237078), ('Price:28" x 84"_update_timestamp', 1672532165.824621), ('Price:30" x 84"_update_timestamp', 1672532165.825517), ('Price:32" x 84"_update_timestamp', 1672532165.826416), ('Price:36" x 84"_update_timestamp', 1672532165.8273191), ('Price:42" x 84"_update_timestamp', 1672532165.828238), ('Price:18" x 96"_update_timestamp', 1672532165.829278), ('Price:24" x 96"_update_timestamp', 1672532165.8301911), ('Price:28" x 96"_update_timestamp', 1672532165.831101), ('Price:30" x 96"_update_timestamp', 1672532165.832015), ('Price:32" x 96"_update_timestamp', 1672532165.8329191), ('Price:36" x 96"_update_timestamp', 1672532165.833833), ('Price:42" x 96"_update_timestamp', 1672532165.83474), ('NoHeaderFound_74_update_timestamp', 1672532165.835646), ('Profits:18" x 80"_update_timestamp', 1672532165.836548), ('Profits:24" x 80"_update_timestamp', 1672532165.837448), ('Profits:28" x 80"_update_timestamp', 1672532165.83835), ('Profits:30" x 80"_update_timestamp', 1672532165.8392582), ('Profits:32" x 80"_update_timestamp', 1672532165.840163), ('Profits:36" x 80"_update_timestamp', 1672532165.841063), ('Profits:42" x 80"_update_timestamp', 1672532165.841965), ('Profits:18" x 84"_update_timestamp', 1672532165.842865), ('Profits:24" x 84"_update_timestamp', 1672532165.843769), ('Profits:28" x 84"_update_timestamp', 1672532165.844696), ('Profits:30" x 84"_update_timestamp', 1672532165.8456051), ('Profits:32" x 84"_update_timestamp', 1672532165.8465128), ('Profits:36" x 84"_update_timestamp', 1672532165.847424), ('Profits:42" x 84"_update_timestamp', 1672532165.848334), ('Profits:18" x 96"_update_timestamp', 1672532165.8496928), ('update_timestamp', 1672532165.8489978)])
notSlabSourceData=OrderedDict([("Generate (add an 'x' for the one you want to generate", '114'), ('Inspect/Clean CSV before Import?', '-'), ('Confirmed 08/21', 'x'), ('Published', 'FALSE'), ('Title', 'Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('NoHeaderFound_5', '44.00'), ('Handle', 'white-solid-3-panel-wood-single-barn-door-slab'), ('Type', 'Single'), ('On BDFS', 'Yes'), ('Vendor', 'Sartodoors'), ('Glass', 'Frosted'), ('Glass Lites', '12 Lites'), ('Color', 'White'), ('Hardware', 'Black'), ('SKU', 'sartodoors_2661_single_white_slab'), ('Tags', 'Barn Door, Single Barn Door, White, No Hardware, No Glass, sartodoors-2661'), ('original SKU or Sarto Title', 'sarto_2661-single-white18"x80"_slab'), ('Sarto SKU', '2661'), ('_3309_single_matte-white_frosted-glass_stainless-rail', 'Lucia_2661_single_white_slab_1.jpg'), ('Image 1 URL', 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2661_Single_White_slab_1.jpg?v=1637605012'), ('Image 1 SEO', 'Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 2 URL', 'https://unitedporte.us/media/catalog/product/cache/d263df706a409d1ef4cb15ae72241da3/c/d/cdn.shopify.com_s_files_1_1655_9629_files_design_1.jpg_v_1576676778_14.jpg'), ('Image 2 SEO', 'Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 3 URL', 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Felicia_3309_Single_Matte-White_Frosted_glass_black_rail_3_d6499017-c0d0-4243-90fa-19f172829f55.jpg'), ('Image 3 SEO', 'Barn Door Rail Hanging Instructions for Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 4 URL', 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2555_Single_White_clear-glass_black-rail_4.jpg'), ('Image 4 SEO', 'Internal Construction of Lucia 2661 White Silk 3 Panel Barn Door Slab'), ('Image 5 URL', ''), ('Image 5 SEO', ''), ('UnitedPorte URL', 'https://unitedporte.us/3-panel-slab-barn-door-lucia-2661-white-silk-sturdy-finished-wooden-kitchen-pantry-shaker-doors-pocket-closet-sliding-purple-whatever'), ('Price Updated Date', ''), ('Cost: 18" x 80"', '346.40'), ('Cost: 24" x 80"', '356.80'), ('Cost: 28" x 80"', '356.80'), ('Cost: 30" x 80"', '356.80'), ('Cost: 32" x 80"', '356.80'), ('Cost: 36" x 80"', '356.80'), ('Cost: 42" x 80"', '356.80'), ('Cost: 18" x 84"', '386.40'), ('Cost: 24" x 84"', '386.40'), ('Cost: 28" x 84"', '386.40'), ('Cost: 30" x 84"', '386.40'), ('Cost: 32" x 84"', '386.40'), ('Cost: 36" x 84"', '386.40'), ('Cost: 42" x 84"', '445.60'), ('Cost: 18" x 96"', '505.60'), ('Cost: 24" x 96"', '505.60'), ('Cost: 28" x 96"', '505.60'), ('Cost: 30" x 96"', '505.60'), ('Cost: 32" x 96"', '505.60'), ('Cost: 36" x 96"', '505.60'), ('Cost: 42" x 96"', '635.20'), ('NoHeaderFound_52', ''), ('Price:18" x 80"', '666.61'), ('Price:24" x 80"', '679.30'), ('Price:28" x 80"', '679.30'), ('Price:30" x 80"', '679.30'), ('Price:32" x 80"', '679.30'), ('Price:36" x 80"', '679.30'), ('Price:42" x 80"', '679.30'), ('Price:18" x 84"', '715.41'), ('Price:24" x 84"', '715.41'), ('Price:28" x 84"', '715.41'), ('Price:30" x 84"', '715.41'), ('Price:32" x 84"', '715.41'), ('Price:36" x 84"', '715.41'), ('Price:42" x 84"', '787.63'), ('Price:18" x 96"', '860.83'), ('Price:24" x 96"', '860.83'), ('Price:28" x 96"', '860.83'), ('Price:30" x 96"', '860.83'), ('Price:32" x 96"', '860.83'), ('Price:36" x 96"', '860.83'), ('Price:42" x 96"', '1,018.94'), ('NoHeaderFound_74', ''), ('Profits:18" x 80"', '140.21'), ('Profits:24" x 80"', '142.50'), ('Profits:28" x 80"', '142.50'), ('Profits:30" x 80"', '142.50'), ('Profits:32" x 80"', '142.50'), ('Profits:36" x 80"', '142.50'), ('Profits:42" x 80"', '142.50'), ('Profits:18" x 84"', '149.01'), ('Profits:24" x 84"', '149.01'), ('Profits:28" x 84"', '149.01'), ('Profits:30" x 84"', '149.01'), ('Profits:32" x 84"', '149.01'), ('Profits:36" x 84"', '149.01'), ('Profits:42" x 84"', '162.03'), ('Profits:18" x 96"', '175.23'), ("Generate (add an 'x' for the one you want to generate_update_timestamp", 1672532165.7651799), ('Inspect/Clean CSV before Import?_update_timestamp', 1672532165.7661812), ('Confirmed 08/21_update_timestamp', 1672532165.767204), ('Published_update_timestamp', 1672532165.7683241), ('Title_update_timestamp', 1672532165.7693), ('NoHeaderFound_5_update_timestamp', 1672532165.77032), ('Handle_update_timestamp', 1672532165.771223), ('Type_update_timestamp', 1672532165.772272), ('On BDFS_update_timestamp', 1672532165.773196), ('Vendor_update_timestamp', 1672532165.774108), ('Glass_update_timestamp', 1672532165.7750258), ('Glass Lites_update_timestamp', 1672532165.7759821), ('Color_update_timestamp', 1672532165.776893), ('Hardware_update_timestamp', 1672532165.777795), ('SKU_update_timestamp', 1672532165.7787478), ('Tags_update_timestamp', 1672532165.7799911), ('original SKU or Sarto Title_update_timestamp', 1672532165.781122), ('Sarto SKU_update_timestamp', 1672532165.782059), ('_3309_single_matte-white_frosted-glass_stainless-rail_update_timestamp', 1672532165.782975), ('Image 1 URL_update_timestamp', 1672532165.7838879), ('Image 1 SEO_update_timestamp', 1672532165.7849889), ('Image 2 URL_update_timestamp', 1672532165.78592), ('Image 2 SEO_update_timestamp', 1672532165.786835), ('Image 3 URL_update_timestamp', 1672532165.787743), ('Image 3 SEO_update_timestamp', 1672532165.788647), ('Image 4 URL_update_timestamp', 1672532165.789557), ('Image 4 SEO_update_timestamp', 1672532165.7904582), ('Image 5 URL_update_timestamp', 1672532165.791359), ('Image 5 SEO_update_timestamp', 1672532165.7922518), ('UnitedPorte URL_update_timestamp', 1672532165.7931478), ('Price Updated Date_update_timestamp', 1672532165.794044), ('Cost: 18" x 80"_update_timestamp', 1672532165.79498), ('Cost: 24" x 80"_update_timestamp', 1672532165.796053), ('Cost: 28" x 80"_update_timestamp', 1672532165.796967), ('Cost: 30" x 80"_update_timestamp', 1672532165.797877), ('Cost: 32" x 80"_update_timestamp', 1672532165.7988439), ('Cost: 36" x 80"_update_timestamp', 1672532165.7997599), ('Cost: 42" x 80"_update_timestamp', 1672532165.800679), ('Cost: 18" x 84"_update_timestamp', 1672532165.80159), ('Cost: 24" x 84"_update_timestamp', 1672532165.802654), ('Cost: 28" x 84"_update_timestamp', 1672532165.80357), ('Cost: 30" x 84"_update_timestamp', 1672532165.804471), ('Cost: 32" x 84"_update_timestamp', 1672532165.805388), ('Cost: 36" x 84"_update_timestamp', 1672532165.806389), ('Cost: 42" x 84"_update_timestamp', 1672532165.807648), ('Cost: 18" x 96"_update_timestamp', 1672532165.808565), ('Cost: 24" x 96"_update_timestamp', 1672532165.809471), ('Cost: 28" x 96"_update_timestamp', 1672532165.810375), ('Cost: 30" x 96"_update_timestamp', 1672532165.811279), ('Cost: 32" x 96"_update_timestamp', 1672532165.812192), ('Cost: 36" x 96"_update_timestamp', 1672532165.813349), ('Cost: 42" x 96"_update_timestamp', 1672532165.8143628), ('NoHeaderFound_52_update_timestamp', 1672532165.815286), ('Price:18" x 80"_update_timestamp', 1672532165.816191), ('Price:24" x 80"_update_timestamp', 1672532165.8171031), ('Price:28" x 80"_update_timestamp', 1672532165.8182452), ('Price:30" x 80"_update_timestamp', 1672532165.81916), ('Price:32" x 80"_update_timestamp', 1672532165.820074), ('Price:36" x 80"_update_timestamp', 1672532165.820987), ('Price:42" x 80"_update_timestamp', 1672532165.821895), ('Price:18" x 84"_update_timestamp', 1672532165.822804), ('Price:24" x 84"_update_timestamp', 1672532165.8237078), ('Price:28" x 84"_update_timestamp', 1672532165.824621), ('Price:30" x 84"_update_timestamp', 1672532165.825517), ('Price:32" x 84"_update_timestamp', 1672532165.826416), ('Price:36" x 84"_update_timestamp', 1672532165.8273191), ('Price:42" x 84"_update_timestamp', 1672532165.828238), ('Price:18" x 96"_update_timestamp', 1672532165.829278), ('Price:24" x 96"_update_timestamp', 1672532165.8301911), ('Price:28" x 96"_update_timestamp', 1672532165.831101), ('Price:30" x 96"_update_timestamp', 1672532165.832015), ('Price:32" x 96"_update_timestamp', 1672532165.8329191), ('Price:36" x 96"_update_timestamp', 1672532165.833833), ('Price:42" x 96"_update_timestamp', 1672532165.83474), ('NoHeaderFound_74_update_timestamp', 1672532165.835646), ('Profits:18" x 80"_update_timestamp', 1672532165.836548), ('Profits:24" x 80"_update_timestamp', 1672532165.837448), ('Profits:28" x 80"_update_timestamp', 1672532165.83835), ('Profits:30" x 80"_update_timestamp', 1672532165.8392582), ('Profits:32" x 80"_update_timestamp', 1672532165.840163), ('Profits:36" x 80"_update_timestamp', 1672532165.841063), ('Profits:42" x 80"_update_timestamp', 1672532165.841965), ('Profits:18" x 84"_update_timestamp', 1672532165.842865), ('Profits:24" x 84"_update_timestamp', 1672532165.843769), ('Profits:28" x 84"_update_timestamp', 1672532165.844696), ('Profits:30" x 84"_update_timestamp', 1672532165.8456051), ('Profits:32" x 84"_update_timestamp', 1672532165.8465128), ('Profits:36" x 84"_update_timestamp', 1672532165.847424), ('Profits:42" x 84"_update_timestamp', 1672532165.848334), ('Profits:18" x 96"_update_timestamp', 1672532165.8496928), ('update_timestamp', 1672532165.8489978)])

def test_doorFields():
    outputData = obj.doorFields(worksheetName, slabSourceData.copy())
    expectedCols = obj.destinationWorksheets[worksheetName].getExpectedColumns()
    outputKeys = outputData.keys()
    assert len(outputData) > len(expectedCols)
    for expectedCol in expectedCols:
        assert expectedCol in outputKeys
    assert outputData['Discount'] == 0.3
    # ('Price:30" x 80"', '679.30')
    assert float(outputData['Price:30" x 80"']) == 679.30
    expectedCost = float(outputData['Price:30" x 80"']) * (1 - outputData['Discount'])
    assert outputData['Cost: 30"x80"'] == expectedCost


def test_cleanPriceKey():
    result = obj.cleanPriceKey('Cost: 18" x 80"')
    assert result == 'Price:18" x 80"'


def test_calculatePrice():
    testSource = {'Cost: 18" x 80"': 10000, 'Price:18" x 80"': 100, 'Discount': 0.25}
    # Note - this will NOT use the value in sourceData['Discount'] it will use
    # what is set on the destination class
    price = obj.calculatePrice('Cost: 18" x 80"', worksheetName, testSource)
    assert price == 70.00


def test_calculatePrice_with_symbols():
    testSource = {'Cost: 18" x 80"': 10000, 'Price:18" x 80"': '$1,000.00', 'Discount': 0.25}
    # Note - this will NOT use the value in sourceData['Discount'] it will use
    # what is set on the destination class
    price = obj.calculatePrice('Cost: 18" x 80"', worksheetName, testSource)
    assert price == 700.00


def test_calculatePrice_with_blank_price():
    testSource = {'Cost: 18" x 80"': 10000, 'Price:18" x 80"': '', 'Discount': 0.25}
    # Note - this will NOT use the value in sourceData['Discount'] it will use
    # what is set on the destination class
    price = obj.calculatePrice('Cost: 18" x 80"', worksheetName, testSource)
    assert price == ''


def test_prepUrl():
    outputUrl = obj.prepUrl(slabSourceData.copy())
    assert outputUrl == slabSourceData['UnitedPorte URL']

def test_prepUrlKey():
    # URL looks like this
    # https://unitedporte.us/3-panel-slab-barn-door-lucia-2661-white-silk-sturdy-finished-wooden-kitchen-pantry-shaker-doors-pocket-closet-sliding
    source = slabSourceData.copy()
    source['URL'] = obj.prepUrl(source)
    output = obj.prepUrlKey(source)
    assert output == "3-panel-slab-barn-door-lucia-2661-white-silk-sturdy-finished-wooden-kitchen-pantry-shaker-doors-pocket-closet-sliding"

def test_prepUrlKey_no_url():
    sourceCopy = slabSourceData.copy()
    sourceCopy['URL'] = ""
    assert None == obj.prepUrlKey(sourceCopy)
    assert obj.skipItem[obj.sourceWorksheetName] == True
    obj.skipItem[obj.sourceWorksheetName] = False


def test_prepModel():
    output = obj.prepModel(slabSourceData.copy())
    assert "Lucia 2661" == output

def test_prepModel_no_title():
    sourceCopy = slabSourceData.copy()
    sourceCopy['Title'] = ""
    assert None == obj.prepModel(sourceCopy)
    assert obj.skipItem[obj.sourceWorksheetName] == True
    obj.skipItem[obj.sourceWorksheetName] = False

def test_prepImages():
    data = obj.prepImages(slabSourceData)
    keys = slabSourceData.keys()
    assert "Image 1 URL" in keys
    assert "Image 2 URL" in keys
    assert "Image 3 URL" in keys
    assert "Image 4 URL" in keys
    assert "Image 5 URL" in keys
    assert "Image 6 URL" in keys
    assert "Image 7 URL" in keys
    assert "Image 8 URL" in keys
    assert "Image 9 URL" in keys
    assert "Image 10 URL" in keys
    assert data['Image 1 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2661_Single_White_slab_1.jpg?v=1637605012'
    assert data['Image 2 URL'] == 'https://unitedporte.us/media/catalog/product/cache/d263df706a409d1ef4cb15ae72241da3/c/d/cdn.shopify.com_s_files_1_1655_9629_files_design_1.jpg_v_1576676778_14.jpg'
    assert data['Image 3 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Felicia_3309_Single_Matte-White_Frosted_glass_black_rail_3_d6499017-c0d0-4243-90fa-19f172829f55.jpg'
    assert data['Image 4 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2555_Single_White_clear-glass_black-rail_4.jpg'
    assert data['Image 5 URL'] == ''
    assert data['Image 6 URL'] == ''
    assert data['Image 7 URL'] == ''
    assert data['Image 8 URL'] == ''
    assert data['Image 9 URL'] == ''
    assert data['Image 10 URL'] == ''

def test_prepDescription_none():
    assert "" == obj.prepDescription(slabSourceData.copy())
    
def test_prepDescription_isset():
    source = slabSourceData.copy()
    source['Description'] = "lorem ipsum"
    assert "lorem ipsum" == obj.prepDescription(source)

def test_prepGlass_no_glass():
    data = obj.prepGlass({"Glass": "No"})
    assert data['Has Glass'] == "No"
    assert data['Glass Finish'] == "None"

def test_prepGlass_has_glass():
    data = obj.prepGlass({"Glass": "Frosted"})
    assert data['Has Glass'] == "Yes"
    assert data['Glass Finish'] == "Frosted"

def test_prepHardware_slab():
    sourceData = obj.prepHardware(slabSourceData.copy())
    assert sourceData['Hardware Type'] == "None"
    assert sourceData['Hardware Color'] == "None"
    assert sourceData['Hardware'] == "None"

def test_prepHardware_not_slab():
    sourceData = obj.prepHardware(notSlabSourceData.copy())
    assert sourceData['Hardware Type'] == "Rail"
    assert sourceData['Hardware Color'] == notSlabSourceData['Hardware']
    assert sourceData['Hardware'] == f"{notSlabSourceData['Hardware']} Rail with predrilled holes, {notSlabSourceData['Hardware']} Hangers with wheels, Door stops, Plastic Fin Floor guide, and Mounting screws"

def test_lites():
    assert obj.prepLites(notSlabSourceData.copy()) == '12'


def test_mapFields_barndoor_single():
    obj.skipItem['barndoor_single'] = False
    outputData = obj.mapFields_barndoor_single(notSlabSourceData.copy())
    assert obj.skipItem['barndoor_single'] == False

    assert outputData['Hardware Type'] == "Rail"
    assert outputData['Hardware Color'] == notSlabSourceData['Hardware']
    assert outputData['Hardware'] == f"{notSlabSourceData['Hardware']} Rail with predrilled holes, {notSlabSourceData['Hardware']} Hangers with wheels, Door stops, Plastic Fin Floor guide, and Mounting screws"
    assert outputData['Has Glass'] == "Yes"
    assert outputData['Glass Finish'] == "Frosted"
    assert outputData['Description'] == ""
    assert outputData['URL'] == notSlabSourceData['UnitedPorte URL']
    assert outputData['URL_key'] == "3-panel-slab-barn-door-lucia-2661-white-silk-sturdy-finished-wooden-kitchen-pantry-shaker-doors-pocket-closet-sliding-purple-whatever"
    assert outputData['Model'] == "Lucia 2661"
    assert outputData['Image 1 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2661_Single_White_slab_1.jpg?v=1637605012'
    assert outputData['Image 2 URL'] == 'https://unitedporte.us/media/catalog/product/cache/d263df706a409d1ef4cb15ae72241da3/c/d/cdn.shopify.com_s_files_1_1655_9629_files_design_1.jpg_v_1576676778_14.jpg'
    assert outputData['Image 3 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Felicia_3309_Single_Matte-White_Frosted_glass_black_rail_3_d6499017-c0d0-4243-90fa-19f172829f55.jpg'
    assert outputData['Image 4 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2555_Single_White_clear-glass_black-rail_4.jpg'
    assert outputData['Image 5 URL'] == ''
    assert outputData['Image 6 URL'] == ''
    assert outputData['Image 7 URL'] == ''
    assert outputData['Image 8 URL'] == ''
    assert outputData['Image 9 URL'] == ''
    assert outputData['Image 10 URL'] == ''
    assert outputData['Lites'] == '12'

def test_mapFields_barndoor_single_isSlab():
    obj.skipItem['barndoor_single'] = False
    outputData = obj.mapFields_barndoor_single(slabSourceData.copy())
    assert obj.skipItem['barndoor_single'] == True


def test_mapFields_slabs_single():
    obj.skipItem['slabs_single'] = False
    outputData = obj.mapFields_slabs_single(notSlabSourceData.copy())
    assert obj.skipItem['slabs_single'] == True

def test_mapFields_slabs_single_notSlab():
    obj.skipItem['slabs_single'] = False
    outputData = obj.mapFields_slabs_single(slabSourceData.copy())
    assert obj.skipItem['slabs_single'] == False
    
    assert outputData['Hardware Type'] == "None"
    assert outputData['Hardware Color'] == "None"
    assert outputData['Hardware'] == "None"
    assert outputData['Description'] == ""
    assert outputData['Has Glass'] == "No"
    assert outputData['Glass Finish'] == "None"
    assert outputData['URL'] == slabSourceData['UnitedPorte URL']
    assert outputData['URL_key'] == "3-panel-slab-barn-door-lucia-2661-white-silk-sturdy-finished-wooden-kitchen-pantry-shaker-doors-pocket-closet-sliding"
    assert outputData['Model'] == "Lucia 2661"
    assert outputData['Image 1 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2661_Single_White_slab_1.jpg?v=1637605012'
    assert outputData['Image 2 URL'] == 'https://unitedporte.us/media/catalog/product/cache/d263df706a409d1ef4cb15ae72241da3/c/d/cdn.shopify.com_s_files_1_1655_9629_files_design_1.jpg_v_1576676778_14.jpg'
    assert outputData['Image 3 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Felicia_3309_Single_Matte-White_Frosted_glass_black_rail_3_d6499017-c0d0-4243-90fa-19f172829f55.jpg'
    assert outputData['Image 4 URL'] == 'https://cdn.shopify.com/s/files/1/0555/3176/5931/files/Lucia_2555_Single_White_clear-glass_black-rail_4.jpg'
    assert outputData['Image 5 URL'] == ''
    assert outputData['Image 6 URL'] == ''
    assert outputData['Image 7 URL'] == ''
    assert outputData['Image 8 URL'] == ''
    assert outputData['Image 9 URL'] == ''
    assert outputData['Image 10 URL'] == ''
    assert outputData['Lites'] == 'No'