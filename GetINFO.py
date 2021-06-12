from selenium import webdriver
import os, json, time

class Fetch:
    def __init__(self):
        if not os.path.exists("data.json"):
            self.data = {}
            self.start()

    def start(self):
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
        teams = self.browser.find_elements_by_class_name("TeamFigure_tfMainLink__mH93D.Anchor_external__Mh-vB.Anchor_complexLink__2NtkO")
        self.data["teams"] = {team.text: {"teamData": {}, "playerData": {}} for team in teams}
        print(self.data)
        profiles = self.browser.find_elements_by_link_text("Profile")
        pLinks = [i.get_attribute("href") for i in profiles]
        self.getTeamDatas(pLinks)

    def getTeamDatas(self, links):
        for link in links:
            self.browser.get(link)
            teamName = " ".join(self.browser.find_element_by_class_name("TeamHeader_name__1i3fv")
                                .text.split())
            teamINFO = self.browser.find_elements_by_class_name("TeamHeader_rankValue__1pj3i")
            dataColumn = ["PPG", "RPG", "APG", "OPPG"]
            for i in range(4):
                self.data["teams"][teamName]["teamData"][dataColumn[i]] = teamINFO[i].text
            time.sleep(1)
            print(teamName)

    def writeData(self):
        with open("data.json", "w") as f:
            json.dump(self.data, f)

    def end(self):
        self.browser.close()

if __name__ == "__main__":
    Fetch()
