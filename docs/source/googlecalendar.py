class GoogleCalendar():
    """The GoogleCalendar class sets up the google calendar with borrow and return dates."""
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
        """Sets date on borrowing a book on the google calendar
        
        :param self: Initiates the self service events
        
        :param date: date grabbing for book borrowing on calendar event

        :param summary: Result of book borrowed in event (Returned/Borrowed)

        :param description: Event description

        :param eventID: sets Event ID on borrowed book in calendar
        """
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
        """Sets date on returning a book on the google calendar"""
        self.service.events().delete(calendarId='primary', eventId=eventID).execute()

