from tkinter import *
from tkhtmlview import HTMLLabel
import os, time

class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.teamList = Listbox(self, height=40)
        self.playerList = Listbox(self, height=20)
        self.displayArea = HTMLLabel(self, height=20)
        # Teams label
        Label(self, text="Teams").grid(row=0, column=0)
        # Reload button
        Button(self, text="Reload").grid(row=0, column=2, sticky="e")
        # Time of data created
        Label(self, text="Update Time: {}".format(self.dataTime())).grid(row=3)
        self.teamList.grid(row=1, column=0, rowspan=2)
        self.playerList.grid(row=2, column=2)
        self.displayArea.grid(row=1, column=2)

    def dataTime(self):
        return time.ctime(os.path.getmtime("data.json"))

if __name__ == "__main__":
    myApp = MyApp()
    myApp.mainloop()
