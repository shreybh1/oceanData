import earthaccess
import xarray as xr
import sys 
import numpy as np 
import matplotlib.pyplot as plt

"""
Function call to retrieve credentials 
"""
auth = earthaccess.login()

"""
Class to define search parameters for each access search data function. 
If these parameters are not given, then defaults are set 
Inputs:
start date - date to start search in format YYYY-MM-DD
start time - time to start search in format HH:MM:SS 
end date - date to finish search in format YYYY-MM-DD
end time - time to finish search in format HH:MM:SS 
bounding_box - selection of lat/long in format (lower_left_lon, lower_left_lat , upper_right_lon, upper_right_lat)
"""
class search_params:
    # args receives unlimited no. of arguments as an array
    def __init__(self, **kwargs):

        # access args index values, otherwise set default values as example 
        if(kwargs): 
            self.start_date = kwargs["start_date"]
            self.start_time = kwargs["start_time"]
            self.end_date = kwargs["end_date"]
            self.end_time = kwargs["end_time"]
            print(kwargs["bounding_box"])
            self.bounding_box = kwargs["bounding_box"]
        else:
            self.start_date = "2020-01-01" 
            self.start_time = "00:00:00" 
            self.end_date = "2020-01-01" 
            self.end_time = "01:00:00"

        print("Start date", self.start_date)
        print("End date", self.end_date)
        print("Start time", self.start_time)
        print("End time", self.end_time)
        print("Latitude and longitude selection", self.bounding_box)

    
"""
Function to search earth access data for MODIS satellite data 
using search params data 
Returns output results in the form of a URL 
"""
def get_data(**kwargs): 

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

    if len(results)>0:
        granules.append(results[0])
    
    print("Total granules:", len(granules))

    return(granules)

"""
Function to stream data into xr object using results from earth access search API
"""
def stream_data(results):

    fileset = earthaccess.open(results)

    print(f" Using {type(fileset[0])} filesystem")

    # open dataset streaming object with h5netcdf engine 
    ds = xr.open_mfdataset(fileset, chunks={}, engine='h5netcdf')

    return(ds)

"""
Plot sea surface temperature on contour plot 
"""
def plot_sst(ds):

    plt.figure(figsize=(15,7))

    z = ds['sea_surface_temperature'][0] 
    y = ds['lat'] 
    x = ds['lon']  

    # Contour plot 
    contourplot = plt.contourf( x,y,z,levels=50)
    cbar = plt.colorbar(contourplot)

    # Annotate plot 
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.title('Sea surface temperature %s' %ds.time_coverage_start)
    plt.show() 

def sea_surface_temperature(**kwargs):

    """
    Function to get data from earth access API 
    """
    result = get_data(**kwargs) 

    """
    stream data directly into dataset 
    """
    stream = stream_data(result)

    """
    Plot sea surface temperature     
    """
    plot_sst(stream)


if __name__ == '__main__':
    sys.exit(sea_surface_temperature(start_date="2020-01-01", start_time="00:00:10", end_date="2020-01-02", end_time="01:00:00",bounding_box=(-45, -45, 45, 45))) 
