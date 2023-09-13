import earthaccess
import xarray as xr
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import datetime as dt   
import cartopy.crs as ccrs

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

def plot_sst(ds):
    """
    Plot sea surface temperature on contour plot 
    :param ds object containing xr dataset
    :return: contour plot of sea surface temperature
    """

    plt.figure(figsize=(15,7))

    z = ds['sea_surface_temperature'][0] 
    y = ds['lat'] 
    x = ds['lon'] 

    # Contour plot 
    contourplot = plt.contourf( x,y,z,levels=100)
    cbar = plt.colorbar(contourplot)

    # Annotate plot 
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.title('Sea surface temperature %s' %ds.time_coverage_start)
    # plt.show() 
    plt.savefig(f'Sea surface temperature {ds.time_coverage_start}') 

def plotGlobalMap(ds):

    plt.figure(figsize=(20,24))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ds.sea_surface_temperature[0].plot.pcolormesh(
        ax=ax, transform=ccrs.PlateCarree(), y="lat", x="lon", add_colorbar=False
    )
    ax.coastlines()

def sea_surface_temperature(**kwargs):

    # Function to get data from earth access API 
    result = get_data(**kwargs) 

    if(METHOD == 'LOCAL'):
        # download data to local folder
        files = earthaccess.download(result, "local_folder")
        stream = xr.open_dataset(files) 
    elif(METHOD == 'STREAM'):
        # stream data directly into dataset 
        stream = stream_data(result)

    stream.sea_surface_temperature[0].plot() # lat and lon are coordinates but they do not function well for current data 


if __name__ == '__main__':
    # by default, the function will use the current date. Iterate backwards by 1 day to get previous day's data. 
    start_date_ = dt.date.today() - dt.timedelta(days = 1)
    # start_date_ = dt.date.today() 
    end_date_ = dt.date.today()
    # obtain current time in format '%Y-%m-%dT%H:%M:%SZ'
    end_time_ = dt.datetime.now().strftime('%H:%M:%S')
    # obtain start time 12h before end time
    start_time_ = (dt.datetime.now() - dt.timedelta(hours = 4)).strftime('%H:%M:%S')   
    # sys.exit(sea_surface_temperature(start_date=f"{start_date_}", start_time=start_time_, end_date=f"{end_date_}", end_time=f"{end_time_}",bounding_box=(-45, -45, 45, 45))) 
    sys.exit(sea_surface_temperature()) 
