import json
import pickle
import googleapiclient
from pprint import pprint
from pathlib import Path
from datetime import datetime, timedelta
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# TODO: Check python version

CLIENT_SECRET = "client_secret"
CREDENTIAL_PICKLE = "calendar_access_credential.p"

found_credentials_pickle = Path(".").joinpath(CREDENTIAL_PICKLE).exists()
found_client_secret_json = Path(".").joinpath(f"{CLIENT_SECRET}.json").exists()

calendar_name = None

if found_client_secret_json:
    with open(f"{CLIENT_SECRET}.json", "r") as in_f:
        secrets = json.load(in_f)
        calendar_name = secrets.get("calendar_name")
        print(calendar_name)


if calendar_name:
    print(f"Calendar Name is {calendar_name}.")
    print(f"To conitune using {calendar_name} press enter.")
    print(f"Do you want to use a new calendar? Type in new name and press enter.")
else:
    print("Please enter a calendar name and press enter.")

print(f"Ctrl + C to exit")

try:
    temp_calendar_name = str(input()).replace(" ", "")
    if len(temp_calendar_name) > 0:
        calendar_name = temp_calendar_name

        with open(f"{CLIENT_SECRET}.json", "w") as ou_f:
            secrets["calendar_name"] = calendar_name
            json.dump(secrets, ou_f, indent=2)

        print(f"Calendar name {calendar_name} has been saved.")
        print("Next time you run make_my_day.py, it will be an option to re-use")

except KeyboardInterrupt:
    print(
        """
Day of making-my-day has been ended!
Gee-whiz! A lot got done! Goodbye!
        """
    )
    exit()

if not found_credentials_pickle:

    if not found_client_secret_json:
        print(
            f"Did not find {CLIENT_SECRET}.json. Please follow readme and run me again."
        )
        exit()

    scopes = ["https://www.googleapis.com/auth/calendar"]
    flow = InstalledAppFlow.from_client_secrets_file(
        f"{CLIENT_SECRET}.json", scopes=scopes
    )
    credentials = flow.run_console()

    with open(CREDENTIAL_PICKLE, "wb") as f:
        pickle.dump(credentials, f)

with open(CREDENTIAL_PICKLE, "rb") as f:
    credentials = pickle.load(f)

if not calendar_name:
    print(
        f"Could not get a calendar name somehow. Please inform the author. Aborting run now..."
    )
    exit()

service = build("calendar", "v3", credentials=credentials)

# TODO: Automatically GET todays date and construct `timeMin` and `timeMax`

# ALl events from today in selected calendar

try:
    todays_events = (
        service.events()
        .list(
            calendarId=calendar_name,
            timeMin="2019-12-17T00:00:00+01:00",
            timeMax="2019-12-18T00:00:00+01:00",
            orderBy="startTime",
            singleEvents=True,
        )
        .execute()
    )
except googleapiclient.errors.HttpError as err:
    print(f"Could not complete query to google for calendar {calendar_name}.  ")
    print(f"We got the following response. \n{err._get_reason}")
    print("\nMaybe check the calendar name when entering next time.")
    exit()

# events without summary are usually cancelled, so we filter those events out
sorted_events_with_summaries = sorted(
    [i for i in todays_events["items"] if i.get("summary")],
    key=lambda k: k["start"]["dateTime"],
)

# pprint(sorted_events_with_summaries)

# TODO: Mention whether you are attending event or not
# Used times
print("events in your calendar")
pprint([[i["start"]["dateTime"], i["end"]["dateTime"], i["summary"]] for i in sorted_events_with_summaries])

# TODO: Find unscheduled time from NOW (datetime.now())

# TODO: Break up and offer 1 hour chunks of time for user to assign work to (create events about)

# TODO: create the events

# TODO: create events with identifiers so that this code can recognize it

# TODO: if there are events in the rest of the day that were previously made by this code
#      the user should get the option to retain or re-scedule the timeslot
