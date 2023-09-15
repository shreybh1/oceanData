from createplots import *
from datacollect import *   

def sst(**kwargs):
    """
    Main function that calls all other functions to retrieve and plot sea surface temperature data

    Args:
        kwargs: search parameters that are passed into search_data function such as start date, end date, bounding box etc.

    Returns:
        plots of sea surface temperature data
    """

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

    plot_sst_coordinates(data_cleaned) 

    plot_sst_global(data_cleaned)