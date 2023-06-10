This project pulls the upcoming match schedule from lolesports and adds it to a google cal. 

INSTALL
add credentials.json as described in the google api quickstart 
add config.json with a calendar id (seeSample)


USE
>> python3 run.py -h
>> python3 run.py 
>> python3 run.py -l lck lpl
>> python3 run.py -l msi
consider using a venv

this script will need to be rerun when more event details are announced. it will delete upcoming events first, then add the upcoming event details. 

UPKEEP
depending on how you've set up your google api stuff, you may need to delete token.json to run successfully. token.json is the generated file after the first run. It may expire after a week

ARCHITECTURE
lolesports.py   uses selenium and processes lolesports website into a 2D list of events and event info. 
                see get_upcoming_matches()
gcal.py         interacts with the google api. updates and deletes events
run.py          gets info from lolesports.py and feeds it to gcal.py
