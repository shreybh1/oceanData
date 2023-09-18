oceanData
---------
The oceanData module searches the MODIS satellite data to obtain sea surface temperature using user specified search parameters which calls the NASA earthaccess package. 
The py files are in [oceanData](oceanData) folder. 
The repository uses a [scheduler](scheduler.py) to obtain the plots for specified intervals. 

## Create a new environment package for earthaccess
### Conda installation
The scripts need conda environments to run the packages.
```
# Earth access module for the NASA earth access package  
conda install -c conda-forge earthaccess

# xarray package for data analysis
conda install -c anaconda xarray

# open blas package may be required for MAC users 
conda install openblas 

# h5netcdf for xarray 
conda install -c conda-forge h5netcdf
conda install dask 

# plotting using matplotlib
conda install matplotlib 

# job scheduling using apscheduler 
conda install -c anaconda apscheduler 
```
Alternatively, [env.yml](env.yml) can be used to build the conda environment to
run the scripts using the following command. 

```
conda env create -f env.yml 
```

### Pip installation
Pip can also be used to setup the environment for this module using the [setup file](setup.py). 

```
pip install . 
```

## Create access file providing your credentials to use earth access 
Access token can be created using earthdata website using this [link](https://www.earthdata.nasa.gov/learn/use-data).  
```
touch ~/.netrc 
echo "machine urs.earthdata.nasa.gov" >> ~/.netrc 
echo "	login <enter username>" >> ~/.netrc
echo "	password <enter password>" >> ~/.netrc 
```

## Documentation 
[GH pages](https://sb15895.github.io/oceanData/) is used to host documentation.

Alternatively, mkdocs can be used to host the documents locally using the following pages. 
```
mkdocs build 
mkdocs serve 
```

## Quick start
[scheduler.py](scheduler.py) is the main file containing the scheduler which then calls the [sst](sst.py) function for default interval of 1 hour. 
```
python3 scheduler.py  
```
A test flag can be added which calls the [sst](sst.py) once, to verify if the plot function is working as expected. 
```
python3 scheduler.py test 
```

### offline global maps 
For offline map generation, a [script](cartopydata.sh) can be called which will download and unzip the cartopy files for the minimum downloading requirements. 
```
sudo bash cartopydata.sh 
```