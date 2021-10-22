from datetime import date
import tkinter as tk
from tkcalendar import Calendar
from time_interface import timeinterface


root = tk.Tk()

def select_date():
    # current date
    current_date = date.today()
    # date selcted from calendar
    selected_date = cal.get_date()
    sel_date_array = selected_date.split('-')
    selected_date = date(int(sel_date_array[0]), int(sel_date_array[1]), int(sel_date_array[2]))

    if(selected_date > current_date):
        # display the time interface
        timeinterface(current_date, selected_date)

        # close the current window
        exit()
    else:
        error_label.config(text="Selected Date must not be Previous days or the current date")

root.iconbitmap('clock.ico')
root.title("Time Count down")
root.geometry('500x500')

# show the calendar
date_select_label = tk.Label(root, text="Select final Date")
date_select_label.pack(pady=20)
cal = Calendar(root, selectmode="day", date_pattern='yyyy-mm-dd')
cal.pack(pady=20)

tk_button = tk.Button(text="Select Date", command=select_date)
tk_button.pack(pady=20)

error_label = tk.Label(root, text="", fg="red")
error_label.pack(pady=20)

# enter widgets here
root.mainloop()