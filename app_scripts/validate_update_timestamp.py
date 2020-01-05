import copy
from datetime import datetime
from app_scripts.print_time_data import print_time_data
from app_scripts.validate_update_timeset import validate_update_timeset


def validate_update_timestamp(
    a_timeset: list, list_of_timesets: list, debug_mode: bool = False
) -> list:
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

    Doctest
    >>> validate_update_timestamp(['2019-12-20T09:30:00+01:00', '2019-12-20T11:45:00+01:00'],[['2019-12-20T11:30:00+01:00', '2019-12-20T11:45:00+01:00']])
    ['2019-12-20T09:30:00+01:00', '2019-12-20T11:30:00+01:00']
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

            print_time_data(f"{a_timeset}\n\tChanged to:", temp_timeset, debug_mode)

        if datetime.fromisoformat(temp_timeset[1]) > datetime.fromisoformat(
            timeset[0]
        ) and datetime.fromisoformat(temp_timeset[1]) <= datetime.fromisoformat(
            timeset[1]
        ):
            new_timeset = validate_update_timeset([temp_timeset[0], timeset[0]])
            temp_timeset = new_timeset

            print_time_data(f"{a_timeset}\n\tChanged to:", temp_timeset, debug_mode)

    print_time_data(
        "validate update timestamp, Received Timeset:", a_timeset, debug_mode
    )
    print_time_data(
        "validate update timestamp, Received List:", list_of_timesets, debug_mode
    )
    print_time_data("validate update timestamp, New Timeset:", new_timeset, debug_mode)

    return new_timeset
