from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.

class GoogleCalendar():
    #Connecting google calendar to book borrowing library
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.SCOPES)
            creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                 pickle.dump(creds, token)
        self.service = build('calendar', 'v3', credentials=creds)
   
   
    def borrow_book(self, date, summary, description, eventID):
        #Borrowed book recording details and setting details for event
        event = {
        'id':'',
        'summary': 'Returned',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'date': '',
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'date': '',
            'timeZone': 'Australia/Melbourne',
        },
        }
        event['summary'] = summary
        event['description'] = description
        event['start']['date'] = date
        event['end']['date'] = date
        event['id'] = eventID
        event = self.service.events().insert(calendarId='primary', body=event).execute()
    
    def return_book(self, eventID):
        #Book returned on calendar
        self.service.events().delete(calendarId='primary', eventId=eventID).execute()

