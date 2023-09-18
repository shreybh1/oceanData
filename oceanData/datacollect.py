import earthaccess
import xarray as xr
import sys
import numpy as np
import numpy.ma as ma
import os
import requests 
from requests.auth import HTTPBasicAuth
from urllib.request import urlretrieve


class search_params:
    """
    Class to define search parameters for each access search data function.
    """

    # args receives unlimited no. of arguments as an array
    def __init__(self, **kwargs):
        """
        Initialisation function to set search parameters, and if these are not given then default values are used.

        Args:
            start_date (str): date to start search in format YYYY-MM-DD
            start_time (str): time to start search in format HH:MM:SS
            end_date (str): date to finish search in format YYYY-MM-DD
            end_time (str): time to finish search in format HH:MM:SS
            bounding_box (array): selection of lat/long in format (lower_left_lon, lower_left_lat , upper_right_lon, upper_right_lat)

        Returns:
            search_params object containing search parameters
        """

        # access args index values, otherwise set default values as example
        if kwargs:
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
    Function to search earth access data for MODIS satellite data using search params data

    Args:
        kwargs: search parameters that are passed into search_data function such as start date, end date, bounding box etc.

    Returns:
        results(URL) : results from earth access search API
    """

    # set default times if not already specified.
    earthAccess_data = search_params(**kwargs)

    results = earthaccess.search_data(
        short_name="MODIS_A-JPL-L2P-v2019.0",
        cloud_hosted=True,
        temporal=(
            f"{earthAccess_data.start_date}T{earthAccess_data.start_time}",
            f"{earthAccess_data.end_date}T{earthAccess_data.end_time}",
        ),
        bounding_box=earthAccess_data.bounding_box,
        count=1,
    )

    if len(results) == 0:
        print("No results found")
        sys.exit(0)

    return results


def stream_data(results):
    """
    Function to stream data into xr object using results from earth access search API

    Args:
        results(URLs): results from earth access search API

    Returns:
        ds(xr object): xr object containing dataset
    """

    fileset = earthaccess.open(results)

    print(f" Using {type(fileset[0])} filesystem")

    # open dataset streaming object with h5netcdf engine
    ds = xr.open_mfdataset(fileset, chunks={}, engine="h5netcdf")

    return ds


def data_cleanup(ds):
    """
    Function to clean up data by removing NaN values from dataset

    Args:
        ds(xr object): xr object containing dataset

    Returns:
        ds_cleaned(xr object): xr object containing cleaned dataset
    """
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
    ds_cleaned["lon_cleaned"] = lon_cleaned
    ds_cleaned["lat_cleaned"] = lat_cleaned
    ds_cleaned["sst_cleaned"] = sst_cleaned
    ds_cleaned["time_coverage_start"] = ds.time_coverage_start

    return ds_cleaned

def download_data(result): 
    """
    Function to download URL data to the local folder and open the file using an xr object using results from earth access search API

    Args:
        results(List): results from earth access search API

    Returns:
        ds(xr object): xr object containing dataset
    """

    # download data to local folder
    # files = earthaccess.download(result, "local_folder")
    output = f"{os.getcwd()}/local_folder"
    
    # get authorisation details from .netrc file 
    import netrc
    secrets = netrc.netrc()
    username, account, password = secrets.authenticators("urs.earthdata.nasa.gov")

    # for each element in result, download the file and open using xarray  
    for x in result:
        str_result = str(x)
        # get Data url from list
        url = str_result.split("Data: ")[1][2:-2]

        # get filename from url 
        filename = f"{output}/{url.split('/')[-1]}" 
        
        if(os.path.isfile(filename)!=True):
            print("Saving under ", filename)
            # res=requests.get(url , auth=HTTPBasicAuth(username, password))
            # open(filename, 'wb').write(res.content)
            # call wget on bash using python 
            os.system("wget " + "-P data/" + " --user=" + username + " --password=" + password + " "+ url )

        # test for file
        assert os.path.isfile(filename) == True
        # open file using xarray
        stream = xr.open_dataset(filename)
        # test for stream
        assert stream != None

    return(stream) 
