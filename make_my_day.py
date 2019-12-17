import pickle
from pprint import pprint
from pathlib import Path
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET = "client_secret"
CREDENTIAL_PICKLE = "calendar_access_credential.p"

# TODO: Check python version

found_credentials_pickle = Path(".").joinpath(CREDENTIAL_PICKLE).exists()

if not found_credentials_pickle:

    scopes = ["https://www.googleapis.com/auth/calendar"]
    flow = InstalledAppFlow.from_client_secrets_file(
        f"{CLIENT_SECRET}.json", scopes=scopes
    )
    credentials = flow.run_console()

    with open(CREDENTIAL_PICKLE, "wb") as f:
        pickle.dump(credentials, f)

with open(CREDENTIAL_PICKLE, "rb") as f:
    credentials = pickle.load(f)


service = build("calendar", "v3", credentials=credentials)


# TODO: Automatically GET todays date and construct `timeMin` and `timeMax`

# ALl events from today
todays_events = (
    service.events()
    .list(
        calendarId="ambar@plotwise.com",
        timeMin="2019-12-17T00:00:00+01:00",
        timeMax="2019-12-18T00:00:00+01:00",
    )
    .execute()
)

# events without summary are usually cancelled, so we filter those events out
sorted_events_with_summaries = sorted(
    [i for i in todays_events["items"] if i.get("summary")],
    key=lambda k: k["start"]["dateTime"],
)

# TODO: Mention whether you are attending event or not
# Used times
print("events in your calendar")
pprint([[i["start"]["dateTime"], i["summary"]] for i in sorted_events_with_summaries])

# TODO: Find unscheduled time from NOW (datetime.now())

# TODO: Break up and offer 1 hour chunks of time for user to assign work to (create events about)

# TODO: create the events

# TODO: create events with identifiers so that this code can recognize it

# TODO: if there are events in the rest of the day that were previously made by this code
#      the user should get the option to retain or re-scedule the timeslot
