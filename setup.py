import setuptools
from setuptools import setup, find_packages

setup(
    name='oceanData',
    version='1.1',
    author='Shrey Bhardwaj',
    packages=find_packages(),
    install_requires=[
        'earthaccess', 
        'apscheduler',
        'matplotlib',
        'cartopy',
        'h5netcdf',
        'netcdf4', 
        'xarray'
    ],
)