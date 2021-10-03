from datetime import date

from plyer.facades import notification
from MyIpAddress import getmyipaddr
from IPLocation import GetIpBasedLocation
from AzanApi import GetAzanTimings
from Time import Get24HourFormat
from plyer import notification

# init the gloabl azan variable
global_azan_timings_obj = None;

# init the global time array
global_time_array = {};

if __name__ == "__main__":
    # get the current ip address of the user
    ipaddress_obj = getmyipaddr();
    
    if(ipaddress_obj is not None):
        location_obj = GetIpBasedLocation(ipaddress_obj['ip']);
        if(location_obj is not None):
            if(location_obj["status"] == "success"):
                lat = location_obj["lat"];
                long = location_obj["lon"];
                # get the current month and year
                todays_date = date.today();
                date = todays_date.day;
                month = todays_date.month;
                year = todays_date.year;

                azan_obj = GetAzanTimings(lat, long, date, month, year)
                global_azan_timings_obj = azan_obj['timings']
            else:
                print("No Data found...")
                print("Program Ends...")
        else:
            print("The system cannot get your Location based on Your Ip Address")
            print("Program Ends...")
    else:
        print("The system cannot get your Ip Address")
        print("Program Ends...")


    # write the program that generates the notification based on the azan timings object
    if(global_azan_timings_obj is not None):
        for key, value in global_azan_timings_obj.items():
            # get the time in 24 hour format
            time = value.split()[0]
            # set the value to the time array
            # convert the time to milliseconds
            global_time_array[key] = time
    else:
        print("No Result Found")

    
    if(len(global_time_array) > 0):
        while True:
            for key, value in global_time_array.items():
                # compare the time
                currenttime = Get24HourFormat()
                if(value == currenttime):
                    notification.notify(
                        title = "Time for {prayer_name}".format(prayer_name = key),
                        message = "Please get up for {prayer_name}, it is important for your success".format(prayer_name = key),
                        app_icon = "icon.ico",
                        timeout = 12
                    )
    else:
        print("No Prayer Found");