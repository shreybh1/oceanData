import earthaccess
import xarray as xr
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import datetime as dt   
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy.ma as ma


METHOD='LOCAL'
"""
Function call to retrieve credentials 
"""
auth = earthaccess.login()

class search_params:
    """
    Class to define search parameters for each access search data function. 
    If these parameters are not given, then defaults are set 
    :param: 
    start date - date to start search in format YYYY-MM-DD
    start time - time to start search in format HH:MM:SS 
    end date - date to finish search in format YYYY-MM-DD
    end time - time to finish search in format HH:MM:SS 
    bounding_box - selection of lat/long in format (lower_left_lon, lower_left_lat , upper_right_lon, upper_right_lat)
    """
    # args receives unlimited no. of arguments as an array
    def __init__(self, **kwargs):

        # access args index values, otherwise set default values as example 
        if(kwargs): 
            self.start_date = kwargs["start_date"]
            self.start_time = kwargs["start_time"]
            self.end_date = kwargs["end_date"]
            self.end_time = kwargs["end_time"]
            self.bounding_box = kwargs["bounding_box"]
        else:
            self.start_date = "2020-01-01" 
            self.start_time = "00:00:00" 
            self.end_date = "2020-01-01" 
            self.end_time = "01:00:00"
            self.bounding_box = (-45, -45, 45, 45)

        print("Start date", self.start_date)
        print("End date", self.end_date)
        print("Start time", self.start_time)
        print("End time", self.end_time)
        print("Latitude and longitude selection", self.bounding_box)

    
def get_data(**kwargs): 
    """
    Function to search earth access data for MODIS satellite data 
    using search params data 
    Returns output results in the form of a URL 
    :param kwargs: search parameters that are passed into search_data function such as start date, end date, bounding box etc.
    :return: results from earth access search API
    """

    granules = [] 

    # set default times if not already specified.
    earthAccess_data = search_params(**kwargs)

    results = earthaccess.search_data(
        short_name='MODIS_A-JPL-L2P-v2019.0',
        cloud_hosted=True,
        temporal=(f"{earthAccess_data.start_date}T{earthAccess_data.start_time}", f"{earthAccess_data.end_date}T{earthAccess_data.end_time}"), 
        bounding_box = earthAccess_data.bounding_box, 
        count = 1
    )

    if(len(results) == 0):
        print("No results found")
        sys.exit(0)
        
    return(results)

def stream_data(results):
    """
    Function to stream data into xr object using results from earth access search API
    :param results: results from earth access search API
    :return: xr object containing dataset
    """

    fileset = earthaccess.open(results)

    print(f" Using {type(fileset[0])} filesystem")

    # open dataset streaming object with h5netcdf engine 
    ds = xr.open_mfdataset(fileset, chunks={}, engine='h5netcdf')

    return(ds)


def plotGlobalMap(ds):

    plt.figure(figsize=(20,24))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ds.sea_surface_temperature[0].plot.pcolormesh(
        ax=ax, transform=ccrs.PlateCarree(), y="lat", x="lon", add_colorbar=False
    )
    ax.coastlines()

def data_cleanup(ds): 
    # np arrays 
    lat = np.array(ds.lat) 
    lon = np.array(ds.lon) 
    sst = np.array(ds.sea_surface_temperature[0]) 

    # Remove rows with Nan values.

    # Use np.isnan() to create a mask for rows containing NaN values for latitude 
    nan_lat_mask = np.any(np.isnan(lat), axis=1)

    # Use np.isnan() to create a mask for rows containing NaN values for longitude
    nan_lon_mask = np.any(np.isnan(lon), axis=1)

    # Obtain the combination of these masks to exclude Nan values for both longitude and latitude 
    combined_mask = np.logical_and(nan_lat_mask, nan_lon_mask)

    # Use boolean indexing to exclude rows with NaN values for all arrays 
    lon_cleaned = lon[~combined_mask]
    lat_cleaned = lat[~combined_mask]
    sst_cleaned = sst[~combined_mask] 

    # assign cleaned data to new dataset
    ds_cleaned = {} 
    ds_cleaned['lon_cleaned'] = lon_cleaned
    ds_cleaned['lat_cleaned'] = lat_cleaned
    ds_cleaned['sst_cleaned'] = sst_cleaned
    ds_cleaned['time_coverage_start'] = ds.time_coverage_start
    

    return(ds_cleaned)


def plot_sst_coordinates(ds):
    """
    Plot sea surface temperature on contour plot 
    :param ds object containing xr dataset
    :return: contour plot of sea surface temperature
    """

    # initialise figure 
    fig, ax = plt.subplots(figsize=(15,10))

    # Contour plot with cleaned data 
    contour = plt.contourf(ds['lon_cleaned'], ds['lat_cleaned'], ds['sst_cleaned']) 

    # Add colorbar
    cbar = plt.colorbar(contour, ax=ax, orientation='horizontal')
    cbar.set_label("Sea surface temperature (K)")

    # Annotate plot 
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.title('Sea surface temperature %s' %ds['time_coverage_start'])
    
    # plt.savefig(f'Sea surface temperature {ds.time_coverage_start}') 
    plt.show()


def plot_sst_global(ds):
    # plot map of the world using cartopy 
    # import matplotlib.pyplot as plt
    # import numpy as np
    # import cartopy.crs as ccrs

    # Create a map using PlateCarree projection
    fig, ax = plt.subplots(figsize=(20,14), subplot_kw={"projection": ccrs.PlateCarree()})
    ax.set_global()

    # Add coastline and country borders for context
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, color='lightgray')
    ax.add_feature(cfeature.OCEAN, color='lightblue')

    # Create a filled contour plot
    contour = ax.contourf(ds['lon_cleaned'], ds['lat_cleaned'], ds['sst_cleaned'], levels=20, cmap='viridis')

    # Add colorbar
    cbar = plt.colorbar(contour, ax=ax, orientation='horizontal')
    cbar.set_label("Sea surface temperature (K)")

    # Set a title
    plt.title("SST Plot on a Map of the World")

    fig.tight_layout() 
    # Show the plot
    plt.show()

def sea_surface_temperature(**kwargs):

    # Function to get data from earth access API 
    result = get_data(**kwargs) 

    if(METHOD == 'LOCAL'):
        # download data to local folder
        files = earthaccess.download(result, "local_folder")
        for file in files: 
            stream = xr.open_dataset(f'local_folder/{file}') 

    elif(METHOD == 'STREAM'):
        # stream data directly into dataset 
        stream = stream_data(result)

    data_cleaned = data_cleanup(stream) 

    # plot_sst_coordinates(data_cleaned) 

    plot_sst_global(data_cleaned)


if __name__ == '__main__':
    # by default, the function will use the current date. Iterate backwards by 1 day to get previous day's data. 
    start_date_ = dt.date.today() - dt.timedelta(days = 1)
    # start_date_ = dt.date.today() 
    end_date_ = dt.date.today()
    # obtain current time in format '%Y-%m-%dT%H:%M:%SZ'
    end_time_ = dt.datetime.now().strftime('%H:%M:%S')
    # obtain start time 12h before end time
    start_time_ = (dt.datetime.now() - dt.timedelta(hours = 4)).strftime('%H:%M:%S')   
    sys.exit(sea_surface_temperature(start_date=f"{start_date_}", start_time=start_time_, end_date=f"{end_date_}", end_time=f"{end_time_}",bounding_box=(-45, -45, 45, 45))) 
    # sys.exit(sea_surface_temperature()) 
