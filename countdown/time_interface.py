from tkinter import Button, Label, Tk
from calculate_time import get_calculated_time_detail
from interval import setInterval


# set the labels values repeatedly
def setLabelDateTime(label1, label2, label3, label4, label5, label6, label7, start_time, end_time):
    # get calculated datetime
    calculated_datetime = get_calculated_time_detail(starttime=start_time, endtime=end_time)
    label1.config(text=f"Remaining days: {calculated_datetime['days']} days.")
    label2.config(text=f"Remaining Hours: {calculated_datetime['hour']} hours, Remaining Minutes: {calculated_datetime['minutes']} minutes.")
    label3.config(text=f"Remaining Seconds: {calculated_datetime['seconds']} seconds, Remaining Milliseconds: {calculated_datetime['milliseconds']} milliseconds")
    label4.config(text=f"Total Hours Left: {calculated_datetime['total_hours_left']} hours, Total Minutes Left: {calculated_datetime['total_minutes_left']} minutes")
    label5.config(text=f"Total Seconds Left: {calculated_datetime['total_seconds_left']} seconds, Total Milliseconds Left: {calculated_datetime['total_millis_left']} millis")
    label6.config(text=f"Weeks Left: {calculated_datetime['total_weeks_left']}")
    label7.config(text=f"Total Jummah Left: {calculated_datetime['total_jummah_remaining']}")



def timeinterface(start_time, end_time):
    root = Tk()
    
    root.iconbitmap('clock.ico')
    root.title("Time Count down")
    root.geometry('500x500')
    
    # get calculated datetime
    calculated_datetime = get_calculated_time_detail(starttime=start_time, endtime=end_time)

    label_1 = Label(root, text=f"Remaining days: {calculated_datetime['days']} days.", font="sans")
    label_1.pack(padx=10, pady=20)

    label_2 = Label(root, text=f"Remaining Hours: {calculated_datetime['hour']} hours, Remaining Minutes: {calculated_datetime['minutes']} minutes.", font="sans")
    label_2.pack(padx=10, pady=20)

    label_3 = Label(root, text=f"Remaining Seconds: {calculated_datetime['seconds']} seconds, Remaining Milliseconds: {calculated_datetime['milliseconds']} milliseconds", font="sans")
    label_3.pack(padx=10, pady=20)

    label_4 = Label(root, text=f"Total Hours Left: {calculated_datetime['total_hours_left']} hours, Total Minutes Left: {calculated_datetime['total_minutes_left']} minutes", font="sans")
    label_4.pack(padx=10, pady=10)

    label_5 = Label(root, text=f"Total Seconds Left: {calculated_datetime['total_seconds_left']} seconds, Total Milliseconds Left: {calculated_datetime['total_millis_left']} millis", font="sans")
    label_5.pack(padx=10, pady=10)

    label_6 = Label(root, text=f"Weeks Left: {calculated_datetime['total_weeks_left']}", font="sans")
    label_6.pack(padx=10, pady=10)

    label_7 = Label(root, text=f"Total Jummah Left: {calculated_datetime['total_jummah_remaining']}", font="sans")
    label_7.pack(padx=10, pady=10)

    btn_func = Button(root, text="Set Interval", font="sans")
    btn_func.pack(padx=10, pady=10)

    root.mainloop()