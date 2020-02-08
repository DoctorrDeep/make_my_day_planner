import copy
import json
import pickle
import sys
from datetime import datetime
from pathlib import Path

import googleapiclient
import pytz
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from app_scripts.break_up_free_timeblocks import break_up_free_timeblocks
from app_scripts.get_free_timeslots import get_free_timeslots
from app_scripts.print_time_data import print_time_data
from app_scripts.round_timeblocks import round_timeblocks

try:
    # TODO: [NTH] try-except broken since the code breaks due to compiler error
    #       ->invalid syntax before it can execute this following check.
    #       Compiler error on f-strings before runtime error can be caught.
    assert sys.version_info >= (3, 7)
except AssertionError:
    print("Please user Python 3.7 and above.")
    print("Aborting this run.")
    exit()

DEBUG_MODE = False
CLIENT_SECRET = "client_secret"
CREDENTIAL_PICKLE = "calendar_access_credential.p"
DEFAULT_COUNTRY_TIMEZONE = "Europe/Amsterdam"

DEFAULT_DESCRIPTION_PREFIX = "make_my_day_event"

"""
The following actions will be carried out
- oauth with google calendar
- set timezone of user
- fetch todays events

It will create the following in dictionary(time_data_dict) format:
- time_min: isoformat timestamp string
- time_max: isoformat timestamp string
- scheduled_time_blocks: list of todays attending/confirmed events
    start and end times sorted by startTime
    Example: [
                ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
            ]
"""

found_credentials_pickle = Path(".").joinpath(CREDENTIAL_PICKLE).exists()
found_client_secret_json = Path(".").joinpath(f"{CLIENT_SECRET}.json").exists()

calendar_name = None

if found_client_secret_json:
    with open(f"{CLIENT_SECRET}.json", "r") as in_f:
        secrets = json.load(in_f)
        calendar_name = secrets.get("calendar_name")

if calendar_name:
    print(f"Calendar Name is `{calendar_name}`")
    print(f"To conitune using `{calendar_name}` press enter")
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

        print(f"Calendar name `{calendar_name}` has been saved.")
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
        print(f"Did not find `{CLIENT_SECRET}.json`")
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

print(f"Timezone is set to `{DEFAULT_COUNTRY_TIMEZONE}`")
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
            print(f"Did not find `{user_timezone}` in known timezones.")
else:
    user_timezone = DEFAULT_COUNTRY_TIMEZONE

service = build("calendar", "v3", credentials=credentials)

# ALl events from today in selected calendar

current_time = datetime.now(pytz.timezone(user_timezone))
time_min = current_time.isoformat()
time_max = f"{time_min.split('T')[0]}T23:59:59+{time_min.split('+')[1]}"

try:
    todays_events = (
        service.events()
            .list(
            calendarId=calendar_name,
            time_min=time_min,
            time_max=time_max,
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

print("Events in your calendar between")
print(f"{time_min} \nand \n{time_max}\n")

# Fetch all Events being attended by only start and end times
attending_events = []

for i in sorted_events_with_summaries:
    my_response_status = "Unknown"

    if calendar_name in [i["organizer"].get("email"), i["creator"].get("email")]:
        my_response_status = i["status"]
    else:
        for attendee in i["attendees"]:
            if attendee.get("self"):
                my_response_status = attendee.get("responseStatus")

    if my_response_status in ["accepted", "confirmed"]:
        attending_events.append(i)

        print(
            f"""
You RSVP status is `{my_response_status}` on event named `{i["summary"]}`
From {i["start"]["dateTime"].split("T")[1].split("+")[0]} till {i["end"]["dateTime"].split("T")[1].split("+")[0]}"""
        )

scheduled_time_blocks = [
    [i["start"]["dateTime"], i["end"]["dateTime"]] for i in attending_events
]

# Done fetching the attending events. Named them : scheduled_time_blocks
# Now, time to make sense of them i.e. create the blocks of time where "nothing" is scheduled.

time_data_dict = {
    "scheduled_time_blocks": scheduled_time_blocks,
    "time_min": time_min,
    "time_max": time_max,
}

scheduled_time_blocks = time_data_dict["scheduled_time_blocks"]
time_min = time_data_dict["time_min"]
time_max = time_data_dict["time_max"]

free_timeblocks = get_free_timeslots(
    time_min, time_max, scheduled_time_blocks, DEBUG_MODE
)

# Done calculating free time during the day.
# If the first free timeblock is very small (less than 15 mins) then ignore it
# We call this: rounding out the free timeblocks

duration_from_now = (
        datetime.fromisoformat(free_timeblocks[0][0]) - datetime.fromisoformat(time_min)
).total_seconds()
if duration_from_now <= 900:
    rounded_free_timeblocks = round_timeblocks(free_timeblocks)
else:
    rounded_free_timeblocks = free_timeblocks

# Done rounding out the free timeslots
# Now we break up the available time into 1 hour chunks.
# We call this plannable_timeblocks

plannable_timeblocks = break_up_free_timeblocks(
    rounded_free_timeblocks, 3600, DEBUG_MODE
)

print_time_data("Final result: Current time ", time_min, True, True)
print_time_data("Final result: Blocked time ", scheduled_time_blocks, True, True)
print_time_data("Final result: Free time ", rounded_free_timeblocks, True, True)
print_time_data(
    "Final result: Broken up time blocks ", plannable_timeblocks, True, True
)

# We now have the plannable chunks of time through the rest of the day
# Time to create events out of them. The user gets to decide whether or not
# an event needs to be planned into a free time block or kept free.

default_event_details = {
    "summary": "make_my_day event",
    "location": "Delft Station, Delft",
    "description": "",
}

for a_plannable_timeblock in plannable_timeblocks:

    print("\n\nFor timeblock:\n", a_plannable_timeblock)
    print("[Ctrl+C to skip this timeblock]")

    temp_details = copy.deepcopy(default_event_details)

    try:

        for detail in default_event_details.keys():

            temp = str(
                input(f"[Leave empty and press enter to use default]\n{detail}:")
            )
            if temp == "":
                temp = default_event_details[detail]

            temp_details[detail] = temp

        summary = temp_details["summary"]
        location = temp_details["location"]
        description = temp_details["description"]

        event = {
            "summary": summary,
            "location": location,
            "description": f"{DEFAULT_DESCRIPTION_PREFIX}: {description}",
            "start": {"dateTime": a_plannable_timeblock[0], "timeZone": user_timezone},
            "end": {"dateTime": a_plannable_timeblock[1], "timeZone": user_timezone},
        }

        event = service.events().insert(calendarId=calendar_name, body=event).execute()
        # print(f"Event created: {event.get('htmlLink')}")
    except KeyboardInterrupt:
        print("\nSkipping ", a_plannable_timeblock)


# TODO: [MUST HAVE] if there are events in the rest of the day that were previously made by this code
#      the user should get the option to retain or re-scedule the timeslot
