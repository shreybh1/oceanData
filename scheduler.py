from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import datetime as dt
from oceanData import * 


def plot_maps():
    """
    Calls sst function with current date and time
    """

    # by default, the function will use the current date. Iterate backwards by 1 day to get previous day's data.
    start_date_ = dt.date.today() - dt.timedelta(days=1)
    # start_date_ = dt.date.today()
    end_date_ = dt.date.today()
    # obtain current time in format '%Y-%m-%dT%H:%M:%SZ'
    end_time_ = dt.datetime.now().strftime("%H:%M:%S")
    # obtain start time 12h before end time
    start_time_ = (dt.datetime.now() - dt.timedelta(hours=4)).strftime("%H:%M:%S")
    sst(
        start_date=f"{start_date_}",
        start_time=start_time_,
        end_date=f"{end_date_}",
        end_time=f"{end_time_}",
        bounding_box=(-45, -45, 45, 45),
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        """
        Test plot maps function if argument "test" is passed
        """
        print("Running one instance of plot_maps")
        plot_maps() 

    else: 
        """
        Main function that calls plot_maps function for interval of 4 hours
        """
        scheduler = BlockingScheduler()
        scheduler.add_job(plot_maps, "interval", minutes=5)
        scheduler.start()

