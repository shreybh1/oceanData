import cartopy.crs as ccrs
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from rasterio.plot import show
from rasterio.enums import Resampling

def waterTemp(data):

    # For convenience I have stored the COG file in the same directory as this notebook.
    # Note you may have given the file a different name.
    """Get data objects from tif file"""

    raster = rasterio.open(data)

    # This will print out a short version of the  meta data associated with this file.
    print(raster.meta)

    # Data visualization units.
    unit = '[ K ]'

    long_name = 'Sentinel-3 Water Surface Temperature'

    # We need to know the geographical extent of the data, this is contained in the raster object.

    bbox = raster.bounds
    extent=[bbox[0],bbox[2],bbox[1],bbox[3]]
    print (bbox)

    """Apply scale factor to plot to reduce the size of the box bounds."""
    upscale_factor = 0.1

    # resample data to target shape
    data = raster.read(
    out_shape=(
        raster.count,
        int(raster.height * upscale_factor),
        int(raster.width * upscale_factor)
            ),
            resampling=Resampling.bilinear
        )

    transform = raster.transform * raster.transform.scale(
    (raster.width / data.shape[-1]),
    (raster.height / data.shape[-2]))

    print('Rescaled size: ',np.shape(data[0,:,:]))

    """Add plot"""
    # Here we set up the parameters needed to display the geographical data correctly.
    fig=plt.figure(figsize=(15, 12))

    # Here we set up a simple Plate Carree geographical projection. This is handled by the Cartopy library.

    ax = plt.axes(projection=ccrs.PlateCarree())

    # The coastline data get downloaded here, there may be a delay the first time you run this notebook.

    ax.coastlines(resolution='10m')
    ax.gridlines()
    ax.set_title(long_name, fontsize=20, pad=20.0, fontweight = 'bold')

    # Here we set the colour map for matplotlib. e.g. 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'jet', also
    # selecting which colour to associate with the NODATA value in the map

    color = cm.jet

    color.set_bad('white')

    #The pixel associated to the NODATA values are masked out.

    data = data.astype(np.float16)
    data[data == -32768.0] = np.nan

    # As the product contains the data in Digital Numbers (DN), it is necessary to calibrate them with the SCALE FACTOR and OFFSET values.
    # These can be retrieved from the extended metadata of the file. 

    scale_factor = 0.0020000001

    offset = 290

    cal_data = scale_factor * data + offset

    img = plt.imshow(cal_data[0,:,:], cmap = color,extent = extent,transform=ccrs.PlateCarree())

    cbar = fig.colorbar(img, ax=ax, orientation='horizontal', fraction=0.04, pad=0.05)
    cbar.set_label(unit, fontsize=16, fontweight = 'bold')
    cbar.ax.tick_params(labelsize=14)

    # plt.savefig('lst.png')
    plt.show()