from tkinter import Tk
from calculate_time import get_calculated_time_detail

def timeinterface(start_time, end_time):
    root = Tk()
    
    root.iconbitmap('clock.ico')
    root.title("Time Count down")
    root.geometry('500x500')
    
    # get calculated datetime
    calculated_datetime = get_calculated_time_detail(starttime=start_time, endtime=end_time)

    root.mainloop()