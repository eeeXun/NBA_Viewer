from tkinter import *
from tkhtmlview import HTMLLabel
import os, time, json

class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.data = self.getData()
        self.setupUI()
        self.setTeam()

    def getData(self):
        with open("data.json", "r") as f:
            return json.load(f)

    def setupUI(self):
        myFont = "Monospace 13"
        self.teamList = Listbox(self, width=25, height=40, font=myFont)
        self.playerList = Listbox(self, height=20, font=myFont)
        self.displayArea = HTMLLabel(self, height=20, font=myFont)
        # Teams label
        Label(self, text="Teams", font=myFont).grid(row=0, column=0)
        # Reload button
        Button(self, text="Reload", font=myFont).grid(row=0, column=2, sticky="e")
        # Time of data created
        Label(self, text="Update Time: {}".format(self.updateTime()), font=myFont).grid(row=3)
        self.teamList.grid(row=1, column=0, rowspan=2)
        self.playerList.grid(row=2, column=2)
        self.displayArea.grid(row=1, column=2)

    def updateTime(self):
        return time.ctime(os.path.getmtime("data.json"))

    def setTeam(self):
        self.teamList.insert(END, *self.data["teams"].keys())
        self.teamList.bind("<<ListboxSelect>>", self.teamSelected)

    def teamSelected(self, event):
        selection = self.teamList.curselection()
        team = self.teamList.get(selection)
        self.teamDisplay(team)

    def teamDisplay(self, team):
        IMG = self.data["teams"][team]["teamData"]["IMG"]
        self.displayArea.set_html('<img src="{}" width="200" height="200">'.format(IMG))

if __name__ == "__main__":
    myApp = MyApp()
    myApp.mainloop()
