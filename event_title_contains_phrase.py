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
