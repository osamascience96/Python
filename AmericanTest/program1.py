from tkinter import *
from tkinter.messagebox import showinfo

class WidgetDemo():

    def __init__(self):
        window = Tk()
        window.title("Widgets Demo!")
        frame1 = Frame(window)
        frame1.pack()

        button1 = Button(window, text = "Button", command = self.processButton)
        button1.pack(side = 'top')
        window.mainloop()
    
    def processButton(self):
        showinfo(title="Wizard", message="Welcome")
    

win = WidgetDemo()