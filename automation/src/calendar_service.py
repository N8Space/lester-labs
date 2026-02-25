from googleapiclient.discovery import build
import datetime
import pytz

class CalendarService:
    def __init__(self, credentials, timezone='America/Chicago'):
        self.service = build('calendar', 'v3', credentials=credentials)
        self.timezone = pytz.timezone(timezone)

    def get_todays_events(self):
        """Returns a list of events for the current day in the user's timezone."""
        try:
            # Get 'now' in the user's timezone
            now_user = datetime.datetime.now(self.timezone)
            
            # Start of Day (User Time)
            start_of_day_user = now_user.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # End of Day (User Time)
            # Fetch for the next 24 hours essentially, or just until end of today.
            # Let's go until end of today + slight buffer or just next 24h.
            # User requirement: "current day's calendar items".
            # So from 00:00 today to 23:59 today.
            end_of_day_user = start_of_day_user + datetime.timedelta(days=1)
            
            # Convert to UTC ISO format for API
            time_min = start_of_day_user.astimezone(pytz.utc).isoformat()
            time_max = end_of_day_user.astimezone(pytz.utc).isoformat()
            
            # print(f"  [Debug] Fetching calendar from {time_min} to {time_max} (UTC)")

            events_result = self.service.events().list(
                calendarId='primary', 
                timeMin=time_min,
                timeMax=time_max,
                maxResults=50, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
            
        except Exception as e:
            print(f"Calendar Error: {e}")
            return []
