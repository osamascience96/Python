from datetime import date
from datetime import datetime
from math import ceil

def get_calculated_time_detail(starttime, endtime):
    # remaining time
    timeleft = datetime(endtime.year, endtime.month, endtime.day) - datetime.now()
    hour = ceil(timeleft.seconds / 3600)
    minutes = ceil(timeleft.seconds / 60)

    return {"days": timeleft.days, "hour": hour, "minutes": minutes, "seconds": timeleft.seconds, "milliseconds": timeleft.microseconds, "total_hours_left": (timeleft.days * 24) + hour, "total_minutes_left": (timeleft.days * (24 * 60)) + minutes, "total_seconds_left": (timeleft.days * (24 * 60 * 60)) + timeleft.seconds, "total_millis_left": (timeleft.days * (24 * 60 * 60 * 1000)) + timeleft.microseconds, "total_weeks_left": ceil(timeleft.days / 7), "total_jummah_remaining": ceil(timeleft.days / 7)};

if __name__ == "__main__":
    time_obj = get_calculated_time_detail(date.today(), date(2021, 12, 25));
    print(time_obj);