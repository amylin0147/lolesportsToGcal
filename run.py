from selenium import webdriver
#from selenium.webdriver.support import relative_locator
# path to folder for grep - /Users/amylin/Documents/coding/webScraping/venv/lib/python3.11/site-packages/selenium
from lolesports import Lolesports
import datetime
from gcal import GoogleCalendar
import argparse

def main(leags):
    if leags: 
        url = "https://lolesports.com/schedule?leagues="
        for l in leags:
            url+=l
            url+=","
    else:
        print("ERROR: no leags")
        return
    
    driver = webdriver.Chrome()
    driver.get(url)

    lolesportsObj = Lolesports(driver)
    upcomingMatches = lolesportsObj.get_upcoming_matches()
    allEvents=processMatchesForCal(upcomingMatches)
    if not allEvents:
        print("No upcoming matches for "+url) 
        return
    gcal=GoogleCalendar()
    gcal.AddToGoogleCalendar(allEvents)

def processMatchesForCal(upcomingMatches):
    allEvents=[]

    if not upcomingMatches:
        print("No upcoming matches") 
    else:
        now = datetime.datetime.today()
        for matches in upcomingMatches:
            event={}
            event["summary"]=matches[0] + " ("+ matches[2]+", Best of "+matches[3]+")"
            event["start"]={}
            dt=datetime.datetime.strptime(matches[1]+" "+str(now.year),'%B %d %I %p %Y')
            event['start']["dateTime"]=dt.isoformat()
            event['start']['timeZone']='America/New_York'
            event["end"]={}
            length=((int(matches[3]))//2)+1
            event['end']["dateTime"]=(dt+datetime.timedelta(hours=2)).isoformat()
            event['end']['timeZone']='America/New_York'
            allEvents.append(event)
    return allEvents

parser = argparse.ArgumentParser(description='pulls the upcoming match schedule from lolesports and adds it to a google cal. ')
parser.add_argument("-l", action="store", nargs="+",type=str,choices=['lcs','lck','lec','lpl','msi','worlds','all-star'],default=["lck","lpl"],help="filter which regions or events to get matches for")

args = parser.parse_args()
#print("main("+str(args.l)+")")
main(args.l)
