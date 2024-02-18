import datetime as dt
import os.path
import psutil

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
def create_event(service, start_time, end_time, color):
    event = {
            "summary": "Chrome",
            # "location": "Somewhere Online",
            "description": "Being productive",
            "colorId": color,
            "start": {
                "dateTime": start_time,
                "timeZone": "US/Central"
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "US/Central"
            }
            # "recurrence": ["RRULE:FREQ=DAILY;COUNT=3"],
            # "attendees": [
            #     {"email": "oburhankhan@gmail.com"},
            #     {"email": "somethingstupid@jfkdjfal.com"}
            # ]
        }
    try:
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event['htmlLink']}")
    except HttpError as error:
        print(f"Error creating event: {error}")
    
def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh.token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        chrome_process_name = 'chrome.exe'
        while True:
            chrome_running = any(process.name() == chrome_process_name for process in psutil.process_iter())
            if chrome_running:
                start_time = dt.datetime.utcnow().isoformat() + 'Z'
                while any(process.name() == chrome_process_name for process in psutil.process_iter()):
                    pass

                end_time = dt.datetime.utcnow().isoformat() + 'Z'
                create_event(service, start_time, end_time, 6)

    except HttpError as error:
        print("An error occurred!:", error)

if __name__ == "__main__":
    main()

