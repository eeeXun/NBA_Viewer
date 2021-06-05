from tkinter import *
import os, time

class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):
        self.geometry("400x400")
        Label(self, text="Update Time: {}".format(self.dataTime())).pack(side=BOTTOM)
        Button(self, text="yellow", command=lambda:self.change("yellow")).pack(side=LEFT)
        Button(self, text="blue", command=lambda:self.change("blue")).pack(side=LEFT)
    def dataTime(self):
        return time.ctime(os.path.getmtime("data.json"))
    def change(self, color):
        self.config(bg=color)

if __name__ == "__main__":
    myApp = MyApp()
    myApp.mainloop()
