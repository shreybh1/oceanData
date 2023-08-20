# STAC API client 
from pystac_client import Client
# other STAC packages 
import json

from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension

def dataExtract():

    """read catalog for Sentinel 3""" 
    root_catalog = Catalog.from_file('https://stac.adamplatform.eu/catalog.json') 

    # describe catalog, takes a long time to describe"
    # root_catalog.describe()

    # print high level descriptions of catalog 
    # print(f"ID: {root_catalog.id}")
    # print(f"Title: {root_catalog.title or 'N/A'}")
    # print(f"Description: {root_catalog.description or 'N/A'}")

    # collections = list(root_catalog.get_collections())

    # print(f"Number of collections: {len(collections)}")
    # print("Collections IDs:")
    # for collection in collections:
    #     print(f"- {collection.id}")

    # items 
    # items = list(root_catalog.get_all_items())

    # print(f"Number of items: {len(items)}")
    # for item in items:
    #     print(f"- {item.id}")

    # item = root_catalog.get_item("S3A_OL_2_WFR____NTC", recursive=True)

    # exit() 

    # file structure Sentinel 3 
    # MMM_II_L_TTTTTT_yyyymmddThhmmss_YYYYMMDDTHHMMSS_YYYYMMDDTHHMMSS_[instance ID]_GGG_[class ID].SEN3
    """Water temperature dataset""" 
    file = 'S3B_OL_2_WFR____20210304T012346_20210304T012646_20210305T141533_0179_049_359_3060_MAR_O_NT_003_A865.tif' 
    # file = 'S3A_SL_2_LST____20200512T095859_20200512T100159_20200513T145209_0179_058_136_2880_LN2_O_NT_004_LST.tif'
    return(file)