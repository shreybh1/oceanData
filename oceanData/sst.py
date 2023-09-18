import earthaccess
import os 
from oceanData import *

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

    auth = (
        earthaccess.login()
    )  # Function call to retrieve credentials using the .netrc file

    # Function to get data from earth access API
    result = get_data(**kwargs)

    if METHOD == "LOCAL":
        # download data into the local directory 
        stream = download_data(result)

    elif METHOD == "STREAM":
        # stream data directly into dataset
        stream = stream_data(result)
        assert stream != None

    data_cleaned = data_cleanup(stream)

    # make directory plots if not already created
    if not os.path.exists("Plots"):
        os.makedirs("Plots")

    if kwargs["plot_type"] == "global" or kwargs["plot_type"] == "Global" or kwargs["plot_type"] == "GLOBAL" or kwargs["plot_type"] == "g" or kwargs["plot_type"] == "G":
    # if plot type argument global is passed, plot sea surface temperature on global coordinates
        plot_sst_global(data_cleaned)
    else: 
    # if plot type argument local is passed, plot sea surface temperature on local coordinates
        plot_sst_coordinates(data_cleaned)
