import json
import pickle
import pytz
import googleapiclient
from pprint import pprint
from pathlib import Path
from datetime import datetime
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# TODO: Check python version

CLIENT_SECRET = "client_secret"
CREDENTIAL_PICKLE = "calendar_access_credential.p"
DEFAULT_COUNTRY_TIMEZONE = "Europe/Amsterdam"

found_credentials_pickle = Path(".").joinpath(CREDENTIAL_PICKLE).exists()
found_client_secret_json = Path(".").joinpath(f"{CLIENT_SECRET}.json").exists()

calendar_name = None

if found_client_secret_json:
    with open(f"{CLIENT_SECRET}.json", "r") as in_f:
        secrets = json.load(in_f)
        calendar_name = secrets.get("calendar_name")


if calendar_name:
    print(f"Calendar Name is {calendar_name}.")
    print(f"To conitune using {calendar_name} press enter.")
    print(f"Do you want to use a new calendar? Type in new name and press enter.")
else:
    print("Please enter a calendar name and press enter.")

print(f"OR Ctrl + C to exit")

try:
    temp_calendar_name = str(input()).replace(" ", "")
    if len(temp_calendar_name) > 0:
        calendar_name = temp_calendar_name

        with open(f"{CLIENT_SECRET}.json", "w") as ou_f:
            secrets["calendar_name"] = calendar_name
            json.dump(secrets, ou_f, indent=2)

        print(f"Calendar name {calendar_name} has been saved.")
        print("Next time you run make_my_day.py, it will be re-used")

except KeyboardInterrupt:
    print(
        """
      Day of making has ended!
Gee-whiz! A lot got done, huh!
                      Goodbye!
        """
    )
    exit()

if not found_credentials_pickle:

    if not found_client_secret_json:
        print(f"Did not find {CLIENT_SECRET}.json.")
        print("Please follow readme and run me again.")
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
    print("Could not get a calendar name somehow.")
    print("Please inform the author. Aborting run now...")
    exit()

print(f"Timezone is set to {DEFAULT_COUNTRY_TIMEZONE}")
print(f"Do you wish to keep it? [yes|no]. Default yes.")
keep_timezone = str(input("")).replace(" ", "")

if keep_timezone == "no":
    found_good_timezone = False
    while not found_good_timezone:
        user_timezone = str(input("New timezone:")).replace(" ", "")
        if user_timezone in pytz.common_timezones_set:
            print(f"{user_timezone} set!")
            found_good_timezone = True
        else:
            print(f"Did not find {user_timezone} in known timezones.")
else:
    user_timezone = DEFAULT_COUNTRY_TIMEZONE

service = build("calendar", "v3", credentials=credentials)

# TODO: [NTH] Check if the time between `timeMin` and `timeMax`is too less

# ALl events from today in selected calendar

current_time = datetime.now(pytz.timezone(user_timezone))
timeMin = current_time.isoformat()
timeMax = f"{timeMin.split('T')[0]}T23:59:59+{timeMin.split('+')[1]}"
end_day_time = datetime.fromisoformat(timeMax)

try:
    todays_events = (
        service.events()
        .list(
            calendarId=calendar_name,
            timeMin=timeMin,
            timeMax=timeMax,
            orderBy="startTime",
            singleEvents=True,
        )
        .execute()
    )
except googleapiclient.errors.HttpError as err:
    print(f"Could not complete query to google for calendar {calendar_name}.")
    print(f"We got the following response. \n{err._get_reason}")
    print("\nMaybe check the calendar name when entering next time.")
    exit()

# events without summary are usually cancelled, so we filter those events out
sorted_events_with_summaries = sorted(
    [i for i in todays_events["items"] if i.get("summary")],
    key=lambda k: k["start"]["dateTime"],
)

# pprint(sorted_events_with_summaries)

# Used times
print("Events in your calendar between")
print(f"{timeMin} \nand \n{timeMax}\n")

# pprint(sorted_events_with_summaries)

for i in sorted_events_with_summaries:
    my_response_status = "Unknown"
    for attendee in i["attendees"]:
        if attendee.get("self"):
            my_response_status = attendee.get("responseStatus")

    print(f"""
You RSVP status is `{my_response_status}` on event named `{i["summary"]}`
From {i["start"]["dateTime"].split("T")[1].split("+")[0]} till {i["end"]["dateTime"].split("T")[1].split("+")[0]}""")

# TODO: [MUST HAVE] Find unscheduled time from NOW (datetime.now()) till end of day

# TODO: [MUST HAVE] Break up and offer 1 hour chunks of time for user to assign work to (create events about)

# TODO: [MUST HAVE] create the events

# TODO: [MUST HAVE] create events with identifiers so that this code can recognize it

# TODO: [MUST HAVE] if there are events in the rest of the day that were previously made by this code
#      the user should get the option to retain or re-scedule the timeslot
