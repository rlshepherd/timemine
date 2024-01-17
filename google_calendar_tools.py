# google_calendar_tools.py

"""
Google Calendar Tools Module.

This module provides functions to interact with Google Calendar API.
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def search_events_with_phrase(credentials, calendar_id, phrase, time_min=None, time_max=None):
    """
    Search for events in a Google Calendar containing a specific phrase.

    :param credentials: Google API credentials
    :param calendar_id: ID of the calendar to search
    :param phrase: Phrase to search for in events
    :param time_min: Minimum time for events (datetime object, optional)
    :param time_max: Maximum time for events (datetime object, optional)
    :return: List of events containing the phrase
    """
    service = build('calendar', 'v3', credentials=credentials)

    if time_min is None:
        time_min = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    if time_max is None:
        time_max = (datetime.utcnow() + timedelta(weeks=4)).isoformat() + 'Z'

    events_result = service.events().list(calendarId=calendar_id,
                                          timeMin=time_min,
                                          timeMax=time_max,
                                          singleEvents=True,
                                          orderBy='startTime').execute()

    events = events_result.get('items', [])

    matching_events = []
    for event in events:
        if phrase.lower() in event.get('summary', '').lower():
            matching_events.append(event)

    return matching_events

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os.path

# Define the SCOPES (if these change, you need to delete the token.pickle file)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def fetch_calendar_data():
    """
    Fetches the summary and ID of each calendar in the user's Google Calendar account and returns them in a list.

    This function first checks for the presence of a 'token.pickle' file to use stored credentials.
    If the file is not found or the credentials are invalid, it initiates a login flow to obtain new credentials,
    which are then saved for future use. It then builds a Google Calendar API service with these credentials and
    retrieves the list of calendars.

    Note: 
    - The user must have a 'YOUR_CREDENTIALS_FILE.json' file with the required Google API credentials.
    - The SCOPES variable determines the level of access the application will have. If this is changed, 
      the 'token.pickle' file should be deleted to re-initiate the authentication flow.

    No parameters are needed for this function.
    
    Returns:
        List of tuples, each containing the summary and ID of a calendar.
    """
    
    creds = None
    # Check if token.pickle file exists which stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'YOUR_CREDENTIALS_FILE.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the calendar service
    service = build('calendar', 'v3', credentials=creds)
    
    # Initialize a list to store calendar data
    calendar_data = []
    
    # Fetch calendar data
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            # Append summary and ID as a tuple to the list
            calendar_data.append((calendar_list_entry['summary'], calendar_list_entry['id']))
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    return calendar_data
