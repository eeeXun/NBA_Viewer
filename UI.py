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
        self.playerList = Listbox(self, width=25, height=20, font=myFont)
        self.teamIMG = HTMLLabel(self, width=20, height=20, font=myFont)
        self.teamDatas = [Label(self, width=25, font=myFont) for i in range(4)]
        self.updateLB = Label(self, text="Update Time: {}".format(self.updateTime()), font=myFont)
        # Teams label
        Label(self, text="Teams", font=myFont).grid(row=0, column=0)
        # Reload button
        Button(self, text="Reload", font=myFont).grid(row=0, column=3, sticky="e")
        self.teamList.grid(row=1, column=0, rowspan=5)
        self.teamIMG.grid(row=1, column=1, rowspan=4)
        for i in range(4):
            self.teamDatas[i].grid(row=i+1, column=2)
        self.playerList.grid(row=5, column=1, columnspan=2)
        self.updateLB.grid(row=6)

    def updateTime(self):
        return time.ctime(os.path.getmtime("data.json"))

    def setTeam(self):
        self.teamList.insert(END, *self.data["teams"].keys())
        self.teamList.bind("<<ListboxSelect>>", self.teamSelected)

    def teamSelected(self, event):
        selection = self.teamList.curselection()
        team = self.teamList.get(selection)
        self.showTeam(team)
        self.setPlayer(team)

    def showTeam(self, team):
        IMG = self.data["teams"][team]["teamData"]["IMG"]
        self.teamIMG.set_html('<img src="{}" width="200" height="200">'.format(IMG))
        dataSet= ["PPG", "RPG", "APG", "OPPG"]
        for i in range(4):
            self.teamDatas[i].config(text=
                                     dataSet[i]
                                     + ": "
                                     + self.data["teams"][team]["teamData"][dataSet[i]])

    def setPlayer(self, team):
        players = self.data["teams"][team]["playerData"].keys()
        self.playerList.delete(0, END)
        self.playerList.insert(END, *players)

if __name__ == "__main__":
    myApp = MyApp()
    myApp.mainloop()
