from selenium import webdriver
import time
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import os, json
import time

class Fetch:
    def __init__(self):
        #if not os.path.exists("data.json"):
        self.data = {}
        self.start()
           
    def start(self):
        self.setBrowser()
        self.getTeams()
        #self.writeData()
        self.getPlayer()
        self.end()

    def setBrowser(self):
        with open("drivePath.txt", "r") as f:
            self.drivePath = f.read()[:-1]
        options = webdriver.ChromeOptions()
        #options.add_argument("-headless")
        self.browser = webdriver.Chrome(executable_path=self.drivePath,
                                        options=options)
    
    def getTeams(self):
        url = "https://www.nba.com/teams"
        self.browser.get(url)
        access_buttom=self.browser.find_element_by_id('onetrust-accept-btn-handler')
        access_buttom.click() 
        teams = self.browser.find_elements_by_class_name("TeamFigure_tfMainLink__mH93D.Anchor_external__Mh-vB.Anchor_complexLink__2NtkO")
        self.data["teams"] = {team.text: {"teamData": {}, "playerData": {}} for team in teams}
        print(self.data)
        profiles = self.browser.find_elements_by_link_text("Profile")
        pLinks = [i.get_attribute("href") for i in profiles]
        self.writeData()
        #self.getTeamDatas(pLinks)
    def getTeamDatas(self, links):
        for link in links:
            self.browser.get(link)
            teamName = " ".join(self.browser.find_element_by_class_name("TeamHeader_name__1i3fv")
                                .text.split())
            teamINFO = self.browser.find_elements_by_class_name("TeamHeader_rankValue__1pj3i")
            dataColumn = ["PPG", "RPG", "APG", "OPPG"]
            for i in range(4):
                self.data["teams"][teamName]["teamData"][dataColumn[i]] = teamINFO[i].text
            print(self.data)
    def getPlayer(self):
        with open('data.json', errors='ignore') as jsonfile:
                inputdata=json.load(jsonfile, strict=False)
        team=inputdata["teams"].keys()
        print("OK")
        teamlist=[*team]
        shortname=[]
        for formal in team:
            buff=formal.split(" ")
            shortname.append(buff[len(buff)-1])
        shortname[18]="Trail Blazers"
        url="https://www.nba.com/players"
        self.browser.get(url)
        teamnum=-1
        for i in shortname:
            teamnum+=1
            thisteam=teamlist[teamnum]
            time.sleep(1)
            try:
                find_teams=Select(self.browser.find_element_by_name('TEAM_NAME'))
                playerlinks=[]
                find_teams.select_by_value(i)
                html=self.browser.page_source
                bsobj=BeautifulSoup(html,"html.parser")
                playerlink=bsobj.findAll('a',{'class':'flex items-center t6 Anchor_complexLink__2NtkO'})
                for pl in playerlink:
                    playerlinks.append(pl["href"])
                for plinkss in playerlinks:
                    time.sleep(1)
                    self.browser.get("https://www.nba.com/"+plinkss)
                    html=self.browser.page_source
                    bsobj=BeautifulSoup(html,"html.parser")
                    playerINFO = bsobj.findAll('p',{"class":"PlayerSummary_playerStatValue__3hvQY"})
                    dataColumn = ["PPG", "RPG", "APG", "PIE"]
                    nameofplayer=bsobj.findAll('p',{"class":"PlayerSummary_playerNameText__K7ZXO"})
                    datanum=0
                    #print(self.data["teams"])

                    self.data["teams"][thisteam]["playerData"][nameofplayer[0].get_text()+" "+nameofplayer[1].get_text()]={"Info":{},"State":{}}
                    print(thisteam)
                    self.writeData()
                    # print(self.data["teams"])
                    os.system("pause")
                    self.writeData()
                    for i in playerINFO:
                        self.data["teams"][thisteam]["playerData"][nameofplayer[0].get_text()+nameofplayer[1].get_text()]["State"][dataColumn[datanum]] = i.get_text()  #teamlist=tname 
                        datanum+=1
                    infoOfPlayer=bsobj.findAll('p',{"class":"PlayerSummary_playerInfoValue__mSfou"})
                    infolabel=bsobj.findAll('p',{"class":"PlayerSummary_playerInfoLabel__gBXXP"})
                    infolist=[]
                    for k in infolabel:
                        infolist.append(k.get_text())
                    infonum=0
                    for ii in infoOfPlayer:
                        self.data["teams"][thisteam]["playerData"][nameofplayer[0].get_text()+nameofplayer[1].get_text()]["Info"][infolist[infonum]] = ii.get_text()  #teamlist=tname 
                        infonum+=1
                    print(teamnum)
                    self.writeData()
                self.browser.get(url)
            except StaleElementReferenceException:
                pass
    def writeData(self):
        with open("data.json", "w") as f:
            json.dump(self.data, f)

    def end(self):
        self.browser.close()

if __name__ == "__main__":
    Fetch()
