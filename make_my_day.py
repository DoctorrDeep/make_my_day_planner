import json
import pickle
import copy
import pytz
import sys
import googleapiclient
from pprint import pprint
from pathlib import Path
from datetime import datetime

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from app_scripts.validate_update_timeset import validate_update_timeset

try:
    # TODO: [NTH] improve assert since the code breaks due to
    #       typehints before it can execute this following check.
    assert sys.version_info >= (3, 7)
except AssertionError:
    print("Please user Python 3.7 and above.")
    print("Aborting this run.")
    exit()

DEBUG_MODE = False
CLIENT_SECRET = "client_secret"
CREDENTIAL_PICKLE = "calendar_access_credential.p"
DEFAULT_COUNTRY_TIMEZONE = "Europe/Amsterdam"


def print_time_data(helptext: str, timestr, override_debug: bool = False):

    if DEBUG_MODE or override_debug:
        print("\n", helptext)
        pprint(timestr)


def validate_update_timestamp(a_timeset: list, list_of_timesets: list) -> list:
    """
    This function will hop throught a list of events provided as input and
    check till whether a given timeset(start and end) lies inside any of the
    events(1 event = 1 timeset) provided in the input.
    If it lies inside, or overlaps, an event or multiple events, then a new
    timeset will be created.

    Input
    a_timeset: list of 2 isoformat timestamp strings.
        Example: ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00']
    list_of_timesets: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                    ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
                ]

    Output
    new_timeset: list of 2 isoformat timestamp strings.
        Example: ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00']
    """

    temp_timeset = copy.deepcopy(a_timeset)
    new_timeset = copy.deepcopy(a_timeset)

    for timeset in list_of_timesets:

        if datetime.fromisoformat(temp_timeset[0]) >= datetime.fromisoformat(
            timeset[0]
        ) and datetime.fromisoformat(temp_timeset[0]) < datetime.fromisoformat(
            timeset[1]
        ):
            new_timeset = validate_update_timeset([timeset[1], temp_timeset[1]])
            temp_timeset = new_timeset

            print_time_data(f"{a_timeset}\n\tChanged to:", temp_timeset)

        if datetime.fromisoformat(temp_timeset[1]) > datetime.fromisoformat(
            timeset[0]
        ) and datetime.fromisoformat(temp_timeset[1]) <= datetime.fromisoformat(
            timeset[1]
        ):
            new_timeset = validate_update_timeset([temp_timeset[0], timeset[0]])
            temp_timeset = new_timeset

            print_time_data(f"{a_timeset}\n\tChanged to:", temp_timeset)

    print_time_data("validate update timestamp, Received Timeset:", a_timeset)
    print_time_data("validate update timestamp, Received List:", list_of_timesets)
    print_time_data("validate update timestamp, New Timeset:", new_timeset)

    return new_timeset


def get_next_avialable_open_timeset(a_timestamp: str, list_of_timesets: list) -> dict:
    """
    This function will hop throught a list of events provided as input and
    check till when there is free time based on one initial timestamp also
    provided in the input.

    Input
    a_timestamp: isoformat timestamp string. Example "2019-10-20T12:20:00.00+01:00"
    list_of_timesets: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                    ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
                ]

    Output
    dictionary:
        next_free_timeset: list of 2 isoformat timestamp strings
        reached_end_of_list: Boolean
    """

    results = {"next_free_timeset": None, "reached_end_of_list": True}

    sorted_list_of_timesets = sorted(list_of_timesets, key=lambda k: k[0])

    filtered_list_of_timesets = []
    for timeset in sorted_list_of_timesets:
        if datetime.fromisoformat(a_timestamp) <= datetime.fromisoformat(timeset[1]):
            filtered_list_of_timesets.append(timeset)

    if filtered_list_of_timesets != sorted_list_of_timesets:
        print_time_data(
            "Next available_timeset: filtering effect from:", sorted_list_of_timesets
        )
        print_time_data(
            "Next available_timeset: filtering effect to:", filtered_list_of_timesets
        )

    # the last timeset triggers some actions. However if the last is also the first
    #     i.e. list of 1 timeset, then its too early to set off the trigger
    index_of_last_timeset = (len(filtered_list_of_timesets) - 1) or 1

    temp_timestamp = a_timestamp

    for timeset_index, timeset in enumerate(filtered_list_of_timesets):
        if datetime.fromisoformat(timeset[0]) > datetime.fromisoformat(temp_timestamp):

            results["next_free_timeset"] = [temp_timestamp, timeset[0]]
            if timeset_index != index_of_last_timeset:
                results["reached_end_of_list"] = False

            print_time_data(
                "Next available_timeset: Going to break: current timeset", timeset
            )
            print_time_data(
                "Next available_timeset: Going to break: timestamp", temp_timestamp
            )
            print_time_data("Next available_timeset: Going to break: results", results)
            break

        temp_timestamp = timeset[1]

    # Check if the found timeset has a startTime
    # inside another timeset
    if results["next_free_timeset"]:
        temp_timeset = validate_update_timestamp(
            results["next_free_timeset"], filtered_list_of_timesets
        )
        results["next_free_timeset"] = temp_timeset

    print_time_data("Next available_timeset: Final results", results)

    return results


def get_free_timeslots(timeMin: str, timeMax: str, scheduled_time_blocks: list) -> list:
    """
    This function will take a timerange (from timeMin to timeMax) and blocks of
    busy times (scheduled_time_blocks). To calculate the free time inbetween as
    blocks(list_of_free_timesets) in the same format as teh busy times.

    Input:
    - timeMin: isoformat timestamp string. Example "2019-10-20T12:20:00.00+01:00"
    - timeMax: isoformat timestamp string. Example "2019-10-20T15:50:00.00+01:00"
    - scheduled_time_blocks: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                    ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
                ]

    Output:
    - list_of_free_timesets: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                    ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
                ]
    """
    reached_end_of_day = False
    beginning_of_free_time = timeMin
    list_of_free_timesets = []
    previous_result = []
    list_of_scheduled_timesets = copy.deepcopy(scheduled_time_blocks)

    while not reached_end_of_day:

        print_time_data(
            "Get free timeslot: (while loop) Next free timestamp",
            beginning_of_free_time,
        )
        print_time_data(
            "Get free timeslot: (while loop) Blocked time", list_of_scheduled_timesets
        )
        print_time_data(
            "Get free timeslot: (while loop) List of free time", list_of_free_timesets
        )

        free_timeset_results = get_next_avialable_open_timeset(
            beginning_of_free_time, list_of_scheduled_timesets
        )

        if free_timeset_results["reached_end_of_list"]:
            next_free_timeset = [beginning_of_free_time, timeMax]
            print_time_data(
                "Get free timeslot: (while loop) Reached End of Day: Next free timeset",
                next_free_timeset,
            )
            reached_end_of_day = True
            if not free_timeset_results.get("next_free_timeset"):
                next_free_timeset = validate_update_timestamp(
                    next_free_timeset, list_of_scheduled_timesets
                )
        else:
            next_free_timeset = free_timeset_results["next_free_timeset"]

        if next_free_timeset not in list_of_free_timesets:
            list_of_free_timesets.append(next_free_timeset)
        else:
            if previous_result == next_free_timeset:
                reached_end_of_day = True
                print_time_data(
                    "Get free timeslot: (while loop) Force closing loop because inf: Next free timeset",
                    next_free_timeset,
                )

        beginning_of_free_time = next_free_timeset[1]
        previous_result = next_free_timeset

        new_list_of_scheduled_timesets = []
        for timeset in list_of_scheduled_timesets:
            if datetime.fromisoformat(next_free_timeset[1]) < datetime.fromisoformat(
                timeset[1]
            ):
                new_list_of_scheduled_timesets.append(timeset)
        list_of_scheduled_timesets = new_list_of_scheduled_timesets

    print_time_data(
        "Get free timeslot: Final List of free timesets", list_of_free_timesets
    )

    return list_of_free_timesets


def setup() -> dict:
    """
    The following actions will be carried out
    - oauth with google calendar
    - set timezone of user
    - fetch todays events

    It will return the following in dictionary form:
    - timeMin: isoformat timestamp string
    - timeMax: isoformat timestamp string
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

    # TODO: [NTH] Check if the time between `timeMin` and `timeMax`is too less

    # ALl events from today in selected calendar

    current_time = datetime.now(pytz.timezone(user_timezone))
    timeMin = current_time.isoformat()
    timeMax = f"{timeMin.split('T')[0]}T23:59:59+{timeMin.split('+')[1]}"

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

    print("Events in your calendar between")
    print(f"{timeMin} \nand \n{timeMax}\n")

    # Events being attended
    attending_events = []

    # pprint(sorted_events_with_summaries)

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

    return {
        "scheduled_time_blocks": scheduled_time_blocks,
        "timeMin": timeMin,
        "timeMax": timeMax,
    }


if __name__ == "__main__":

    time_data_dict = setup()

    timeMin = time_data_dict["timeMin"]
    timeMax = time_data_dict["timeMax"]
    scheduled_time_blocks = time_data_dict["scheduled_time_blocks"]

    free_timeblocks = get_free_timeslots(timeMin, timeMax, scheduled_time_blocks)

    print_time_data("Final result: Current time ", timeMin, True)
    print_time_data("Final result: Blocked time ", scheduled_time_blocks, True)
    print_time_data("Final result: Free time ", free_timeblocks, True)

# TODO: [MUST HAVE] Break up and offer 1 hour chunks of time for user to assign work to (create events about)

# TODO: [MUST HAVE] create the events

# TODO: [MUST HAVE] create events with identifiers so that this code can recognize it

# TODO: [MUST HAVE] if there are events in the rest of the day that were previously made by this code
#      the user should get the option to retain or re-scedule the timeslot
