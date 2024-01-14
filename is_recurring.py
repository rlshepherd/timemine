import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')

# Initialize the API service
service = build('calendar', 'v3', credentials=creds)

# Retrieve events
events_result = service.events().list(calendarId='primary').execute()
events = events_result.get('items', [])

# Check for recurrence
for event in events:
    if 'recurrence' in event:
        print(f"Event {event['summary']} is recurring.")
    else:
        print(f"Event {event['summary']} is not recurring.")