from google.oauth2 import service_account
from googleapiclient.discovery import build

# Authenticate with Google Calendar using your credentials
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = service_account.Credentials.from_service_account_file('path_to_your_client_secret_json_file.json', scopes=SCOPES)

# Create the Google Calendar API service
calendar_service = build('calendar', 'v3', credentials=creds)

# Define the calendar IDs for the two calendars you want to check
calendar_id_1 = 'your_calendar_id_1@example.com'
calendar_id_2 = 'your_calendar_id_2@example.com'

# Function to check for overlapping events
def is_overlap(event1, event2):
    start1 = event1['start'].get('dateTime', event1['start'].get('date'))
    end1 = event1['end'].get('dateTime', event1['end'].get('date'))
    start2 = event2['start'].get('dateTime', event2['start'].get('date'))
    end2 = event2['end'].get('dateTime', event2['end'].get('date'))

    return start1 < end2 and end1 > start2

# Fetch events from both calendars
events_calendar_1 = calendar_service.events().list(calendarId=calendar_id_1).execute()
events_calendar_2 = calendar_service.events().list(calendarId=calendar_id_2).execute()

events_list_1 = events_calendar_1.get('items', [])
events_list_2 = events_calendar_2.get('items', [])

# Check for overlapping events between the two calendars
for event1 in events_list_1:
    for event2 in events_list_2:
        if is_overlap(event1, event2):
            print(f"Overlap found between '{event1['summary']}' in Calendar 1 and '{event2['summary']}' in Calendar 2")