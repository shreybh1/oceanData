oceanData.py creates a scheduler to run the script for an interval of 4 hours. 
This saves the two type of maps, global and coordinate based locally. 
```
	python3 oceanData.py 
```
For a simple plot, sst function can be called. 
```
	sst() # default times and dates 
	sst(start_date=f"{start_date_}", start_time=start_time_,
	end_date=f"{end_date_}", end_time=f"{end_time_}",bounding_box=(-45, -45, 45,
	45)) # sst function with given options 
```
