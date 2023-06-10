from __future__ import print_function

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendar:

    def __init__(self):
        # CALID is cal id of league
        if os.path.exists('config.json'):
            with open("config.json", "r") as jsonfile:
                data = json.load(jsonfile)
                self.CALID=data.get("cal_id")
                print("Read successful")
            print(data)
        return

    def AddToGoogleCalendar(self, eventsList):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # if error with token refresh, then delete token.json
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            GoogleCalendar.UpdateCalendar(self,creds,eventsList)

        except HttpError as error:
            print('An error occurred: %s' % error)

    def UpdateCalendar(self, creds,eventsToAdd):
        # clear upcoming events
        service = build('calendar', 'v3', credentials=creds)
        GoogleCalendar.deleteUpcomingEvents(self,creds)

        # add events
        print("Added: ")
        for e in eventsToAdd:
            service.events().insert(calendarId=self.CALID, body=e).execute()
            print(e)
    
    def deleteUpcomingEvents(self,creds):
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=self.CALID, timeMin=now,
                                                #maxResults=20, 
                                                singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])
        print("deleting upcoming events: ")
        for event in events:
            eventID=event.get('id')
            service.events().delete(calendarId=self.CALID, eventId=eventID).execute()
            print(eventID)