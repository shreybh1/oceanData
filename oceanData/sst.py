import earthaccess
from oceanData import *
import xarray as xr
import os 

def sst(**kwargs):
    """
    Main function that calls all other functions to retrieve and plot sea surface temperature data

    Args:
        kwargs: search parameters that are passed into search_data function such as start date, end date, bounding box etc.

    Returns:
        plots of sea surface temperature data
    """

    METHOD = "LOCAL"
    """
    Variable to define method of data retrieval.

    Args:
        LOCAL: download data to local folder
        STREAM: stream data directly into dataset
    """

    auth = earthaccess.login() # Function call to retrieve credentials using the .netrc file 


    # Function to get data from earth access API
    result = get_data(**kwargs)

    if METHOD == "LOCAL":
        # download data to local folder
        files = earthaccess.download(result, "local_folder")
        for file in files:
            # test for file 
            assert os.path.isfile(f"local_folder/{file}") == True
            # open file using xarray 
            stream = xr.open_dataset(f"local_folder/{file}")
            # test for stream
            assert stream!=None

    elif METHOD == "STREAM":
        # stream data directly into dataset
        stream = stream_data(result)
        assert stream!=None

    data_cleaned = data_cleanup(stream)

    # make directory plots if not already created 
    if not os.path.exists('Plots'):
        os.makedirs('Plots')

    plot_sst_coordinates(data_cleaned)

    plot_sst_global(data_cleaned)
