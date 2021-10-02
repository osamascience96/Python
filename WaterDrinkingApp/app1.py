# Code Taken from Code with Harry
# Water Schedular Application that sleeps the computer for the given time
# And then invoking the notification after the sleep syncronization is finished

import time
from plyer import notification

if __name__ == "__main__":
    while True:
        notification.notify(
            title = "Please Drink Water Now",
            message = "Please Drink Water, as it is important for you",
            app_icon = "icon.ico",
            timeout = 12
        )
        time.sleep(6)
