scheduler.py creates a scheduler to run the script for an interval of 4 hours by
default. 
This saves the two type of maps, global and coordinate based locally in Plots/
folder. 
```
	python3 scheduler.py 
```
If a test is required for the job, then the test flag can be added which calls
the sst function. 
```
	python3 scheduler.py test 
```
For a simple plot, sst function can be called after importing the oceanData
module. 
```
	sst() # default times and dates 
	sst(start_date=f"{start_date_}", start_time=start_time_,
	end_date=f"{end_date_}", end_time=f"{end_time_}",bounding_box=(-45, -45, 45,
	45)) # sst function with given options 
```
