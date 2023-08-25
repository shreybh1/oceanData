# Create a new environment package for earthaccess
## Earth access module for the NASA earth access package  
	conda install -c conda-forge earthaccess
## xarray package for data analysis
	conda install -c anaconda xarray
## open blas package may be required for MAC users 
	conda install openblas 
## h5netcdf for xarray 
	conda install -c conda-forge h5netcdf
	conda install dask 
## plotting using matplotlib
	conda install matplotlib 

# Create access file providing your credentials to use earth access 
	touch ~/.netrc 
	echo "machine urs.earthdata.nasa.gov" >> ~/.netrc 
	echo "	login <enter username>" >> ~/.netrc
	echo "	password <enter password>" >> ~/.netrc 

