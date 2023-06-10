from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import date

class Lolesports:   
    def __init__(self, driver: ChromiumDriver):
        self.driver = driver

    def get_match_teams(self, element: WebElement):
        t1 = element.find_element(By.CLASS_NAME,"team-info")
        t1 = t1.find_element(By.CLASS_NAME,"tricode")
        loc = locate_with(By.CLASS_NAME, "team-info").to_right_of(t1)
        t2 = self.driver.find_element(loc)
        t2 = t2.find_element(By.CLASS_NAME,"tricode")
        return t1.text+" vs "+t2.text
    
    def get_match_time(self, element: WebElement):
        et = element.find_element(By.CLASS_NAME,"EventTime")
        hour = et.find_element(By.CLASS_NAME,"hour").text
        ampm = et.find_element(By.CLASS_NAME,"ampm").text
        return hour + " "+ampm
    
    def get_match_date(self, element: WebElement):
        locator = locate_with(By.CLASS_NAME, "monthday").above(element)
        md = self.driver.find_element(locator,"//span[@class='monthday']")
        return md.text 
    
    def get_match_league(self, element:WebElement):
        info=element.find_element(By.CLASS_NAME,"league")
        leag=info.find_element(By.CLASS_NAME,"name")
        return leag.text
    
    def get_match_length(self, element:WebElement):
        info=element.find_element(By.CLASS_NAME,"league")
        length=info.find_element(By.CLASS_NAME,"strategy").text
        length=length.split()[-1]
        return length

    def get_match_info(self, element: WebElement):
        d = self.get_match_date(element)
        t = self.get_match_time(element)
        teams = self.get_match_teams(element)
        leag=self.get_match_league(element)
        length=self.get_match_length(element)
        return [teams,d+" "+t,leag,length]

    def get_all_match_info(self):
        matchList = self.driver.find_elements(By.CLASS_NAME,"EventMatch")
        l = []
        for match in matchList:
            l.append(self.get_match_info(match))
        return l
    
    # TODO could be optimized
    # Returns a 2D list containing match info
    #   [[teams, day-time, region/event, number of matches],[ ... ]]
    #   format determined by get_match_info()
    def get_upcoming_matches(self):
        matchList = self.driver.find_elements(By.CLASS_NAME,"EventMatch")
        today = datetime.today()
        l = []
        for match in matchList:
            
            matchDate = self.get_match_date(match)
            matchDateList = matchDate.split()
            dt = datetime.strptime(matchDateList[0]+" "+matchDateList[1].zfill(2),"%B %d")
            dt = datetime.today().replace(month=dt.month,day=dt.day)
            
            teams = self.get_match_teams(match)
            if dt >= today and ("TBD" not in teams):
                try:
                    match.find_element(By.CLASS_NAME,"EventTime")
                    # this is here bc live games show on the site 
                    # even if they're stupid and no one wants to watch them. 
                    # and those events crash the get_match_info
                except:
                    continue
                l.append(self.get_match_info(match))
        return l