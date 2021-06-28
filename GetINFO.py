from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from cairosvg import svg2png
import os, json

class Fetch:
    def __init__(self):
        if not os.path.exists("data.json"):
            self.data = {}
            self.badGateway = "An error (502 Bad Gateway) has occurred in response to this request."
            self.start()

    def start(self):
        if not os.path.exists("./teamPic"):
            os.mkdir("./teamPic")
        self.setBrowser()
        self.getTeams()
        self.writeData()
        self.end()

    def setBrowser(self):
        with open("drivePath.txt", "r") as f:
            self.drivePath = f.read()[:-1]
        options = webdriver.ChromeOptions()
        options.add_argument("-headless")
        self.browser = webdriver.Chrome(executable_path=self.drivePath,
                                        options=options)

    def getTeams(self):
        url = "https://www.nba.com/teams"
        self.browser.get(url)
        self.data["teams"] = {}
        bsObj = BeautifulSoup(self.browser.page_source, "html.parser")
        teamsInfo = bsObj.findAll("div", {"class": "TeamFigure_tf__2RSkP"})
        for teamInfo in teamsInfo:
            teamName = teamInfo.find("a", {"class": "TeamFigure_tfMainLink__mH93D Anchor_external__Mh-vB Anchor_complexLink__2NtkO"}).get_text()
            profile = teamInfo.find("a", {"class": "TeamFigureLink_teamFigureLink__3uOct Anchor_complexLink__2NtkO"})["href"]
            profileLink = urljoin(url, profile)
            self.data["teams"][teamName] = {"teamData":{}, "playerData": {}}
            self.getTeamDatas(teamName, profileLink)

    def getTeamDatas(self, teamName, link):
        self.browser.get(link)
        if self.browser.find_element_by_tag_name("body").text == self.badGateway:
            self.getTeamDatas(teamName, link)
        else:
            teamINFO = self.browser.find_elements_by_class_name("TeamHeader_rankValue__1pj3i")
            dataColumn = ["PPG", "RPG", "APG", "OPPG"]
            for i in range(4):
                self.data["teams"][teamName]["teamData"][dataColumn[i]] = teamINFO[i].text
            imgURL = self.browser.find_element_by_class_name("TeamHeader_teamLogoBW__QkK7w.TeamLogo_logo__1CmT9").get_attribute("src")
            imgPath = "./teamPic/{}.png".format(teamName)
            svg2png(url=imgURL, write_to=imgPath)
            self.data["teams"][teamName]["teamData"]["IMG"] = imgPath

    def writeData(self):
        with open("data.json", "w") as f:
            json.dump(self.data, f)

    def end(self):
        self.browser.close()

if __name__ == "__main__":
    Fetch()
