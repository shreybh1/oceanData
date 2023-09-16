import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy.ma as ma

plt.switch_backend("Agg")  # To avoid matplotlib error


def plot_sst_coordinates(ds):
    """
    Plot sea surface temperature on contour plot

    Args:
        ds(xr object): xr object containing dataset

    Returns:
        contour plot of sea surface temperature
    """

    # initialise figure
    fig, ax = plt.subplots(figsize=(15, 10))

    # Contour plot with cleaned data
    contour = plt.contourf(ds["lon_cleaned"], ds["lat_cleaned"], ds["sst_cleaned"])

    # Add colorbar
    cbar = plt.colorbar(contour, ax=ax, orientation="horizontal")
    cbar.set_label("Sea surface temperature (K)")

    # Annotate plot
    plt.ylabel("Latitude")
    plt.xlabel("Longitude")
    plt.title("Sea surface temperature %s" % ds["time_coverage_start"])

    fig.tight_layout() 
    plt.savefig(f'Plots/Sea_surface_temperature_{ds["time_coverage_start"]}')
    # plt.show()


def plot_sst_global(ds):
    """
    Plot sea surface temperature on contour plot on map of the world

    Args:
        ds(xr object): xr object containing dataset

    Returns:
        contour plot of sea surface temperature on map of the world
    """

    # Create a map using PlateCarree projection
    fig, ax = plt.subplots(
        figsize=(20, 14), subplot_kw={"projection": ccrs.PlateCarree()}
    )
    ax.set_global()

    # Add coastline and country borders for context
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAND, color="lightgray")
    ax.add_feature(cfeature.OCEAN, color="lightblue")

    # Create a filled contour plot
    contour = ax.contourf(
        ds["lon_cleaned"],
        ds["lat_cleaned"],
        ds["sst_cleaned"],
        levels=20,
        cmap="viridis",
    )

    # Add colorbar
    cbar = plt.colorbar(contour, ax=ax, orientation="horizontal")
    cbar.set_label("Sea surface temperature (K)")

    # Set a title
    plt.title("SST Plot on a Map of the World")

    fig.tight_layout()
    # Show the plot
    # plt.show()
    plt.savefig(f'Plots/Sea_surface_temperature_global_map_{ds["time_coverage_start"]}')
