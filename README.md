# Create a new environment package for earthaccess
The scripts need conda environments to run the pachages.
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
Alternatively, [buildenv.sh](buildenv.sh) can be used to build the conda environment to run the scripts. 

# Create access file providing your credentials to use earth access 
Access token can be created using earthdata website using this [link](https://www.earthdata.nasa.gov/learn/use-data).  
```
	touch ~/.netrc 
	echo "machine urs.earthdata.nasa.gov" >> ~/.netrc 
	echo "	login <enter username>" >> ~/.netrc
	echo "	password <enter password>" >> ~/.netrc 
```

# Documentation 
[GH pages](https://sb15895.github.io/oceanData/) is used to host documentation.

Alternatively, mkdocs can be used to host the documents locally using the following pages. 
```
	mkdocs build 
	mkdocs serve 
```