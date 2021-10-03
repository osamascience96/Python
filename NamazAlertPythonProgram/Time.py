import datetime

# get the time in 24 hour format
def Get24HourFormat():
    today = datetime.datetime.now()
    return today.strftime("%H:%M");