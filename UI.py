from tkinter import *
from tkhtmlview import HTMLLabel
import os, time, json
from PIL import Image, ImageTk
import io
from urllib.request import urlopen
class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.data = self.getData()
        self.setupUI()
        self.setTeam()
        self.team=""

    def getData(self):
        with open("data.json", "r") as f:
            return json.load(f)

    def setupUI(self):
        myFont = "Monospace 13"
        self.title("NBA_Viewer")
        self.teamList = Listbox(self, width=25, height=40, font=myFont)
        self.playerList = Listbox(self, width=25, height=20, font=myFont)
        self.teamIMG = HTMLLabel(self, width=25, height=20, font=myFont)
        self.teamDatas = [Label(self, width=25, font=myFont) for i in range(4)]
        self.updateLB = Label(self, text="Update Time: {}".format(self.updateTime()), font=myFont)
        # Teams label
        Label(self, text="Teams", font=myFont).grid(row=0, column=0)
        # Reload button
        Button(self, text="Reload", font=myFont).grid(row=6, column=3, sticky="e")
        Button(self,text="Show Info",font=myFont,command=self.popOutPlayer).grid(row=6,column=1, columnspan=2)
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
        self.team=team
        self.showTeam(team)
        self.setPlayer(team)

    def showTeam(self, team):
        IMG = self.data["teams"][team]["teamData"]["IMG"]
        self.teamIMG.set_html('<img src="{}" width="250" height="200">'.format(IMG))
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

    def popOutPlayer(self):
        pSelection = self.playerList.curselection()
        tSelection = self.teamList.curselection()
        player=self.playerList.get(pSelection[0])
        win =Toplevel()
        win.wm_title(player+"'s Info")
        name = Label(win, text=player) 
        team=Label(win,text=self.team)
        name.pack()
        team.pack()
        infoframe=Frame(win)
        for info in self.data["teams"][self.team]["playerData"][player]["Info"]:
            data=info+":    "+self.data["teams"][self.team]["playerData"][player]["Info"][info]
            keylabel=Label(infoframe,text=data)
            #valuelabel=Label(win)
            keylabel.pack()
            #valuelabel.pack()
        stateframe=Frame(win)
        for state in self.data["teams"][self.team]["playerData"][player]["State"]:
            data=state+":    "+self.data["teams"][self.team]["playerData"][player]["State"][state]
            keylabel=Label(stateframe,text=data)
            #valuelabel=Label(win)
            keylabel.pack()
            #valuelabel.pack()
    
        imageframe=Frame(win) 
        imageframe.pack()
        self.postPlayerImage(self.team,player,imageframe) 
        infoframe.pack(side='right')
        stateframe.pack()
        b = Button(win, text="Okay", command=win.destroy)
        b.pack()   
    def postPlayerImage(self,team,player,frame):
        url=self.data["teams"][team]["playerData"][player]["playerIMG"]
        image_bytes = urlopen(url).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        pil_image = pil_image.resize((450, 350), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(pil_image)
        label = Label(frame, image=tk_image, bg='white')
        label.pack(padx=5, pady=5)


if __name__ == "__main__":
    myApp = MyApp()
    myApp.mainloop()

