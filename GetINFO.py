from selenium import webdriver
import os, json

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
        info = self.browser.find_elements_by_class_name("TeamFigure_tfMainLink__mH93D.Anchor_external__Mh-vB.Anchor_complexLink__2NtkO")
        self.data["teams"] = dict.fromkeys([i.text for i in info])
    def writeData(self):
        with open("data.json", "w") as f:
            json.dump(self.data, f)
    def end(self):
        self.browser.close()

if __name__ == "__main__":
    Fetch()
