import earthaccess
import xarray as xr

auth = earthaccess.login()


from pprint import pprint

def findDatasetname(): 
    # We'll get 4 collections that match with our keywords
    collections = earthaccess.search_datasets(
        keyword = "SEA SURFACE TEMPERATURE MODIS",
        cloud_hosted = True,
        count = 4
    )
    for collection in collections[0:4]:
        # pprint(collection.summary())
        print(pprint(collection.summary()), collection.abstract(), "\n", collection["umm"]["DOI"], "\n\n")

# results = earthaccess.search_data(
#     short_name='MODIS_A-JPL-L2P-v2019.0',
#     cloud_hosted=True,
#     bounding_box=(-10, 20, -5, 25),
#     temporal=("2020-02", "2020-03"),
#     count=1
# )

granules = earthaccess.search_data(
    short_name='MODIS_A-JPL-L2P-v2019.0',
    cloud_hosted=True,
    bounding_box=(-10, 20, -5, 25),
    temporal=("2020-02-01", "2020-02-02"),
    count = 1
)


print(len(granules))


# the collection is cloud hosted, but we can access it out of AWS with the regular HTTPS URL
# granules[0].data_links(access="out_of_region")
# granules[0].data_links(access="direct")

fileset = earthaccess.open(granules)

print(f" Using {type(fileset[0])} filesystem")

ds = xr.open_mfdataset(fileset, chunks={}, engine='h5netcdf')

print(ds)

# ds.SLA.where((ds.SLA>=0) & (ds.SLA < 10)).std('Time').plot(figsize=(14,6), x='Longitude', y='Latitude')

# files = earthaccess.open(results)

# ds = xr.open_mfdataset(files)