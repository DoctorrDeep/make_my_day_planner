import copy
from datetime import datetime

from app_scripts.get_next_available_open_timeset import get_next_available_open_timeset
from app_scripts.print_time_data import print_time_data
from app_scripts.validate_update_timestamp import validate_update_timestamp


def get_free_timeslots(
        time_min: str, time_max: str, scheduled_time_blocks: list, debug_mode: bool = False
) -> list:
    """
    This function will take a timerange (from time_min to time_max) and blocks of
    busy times (scheduled_time_blocks). To calculate the free time inbetween as
    blocks(list_of_free_timesets) in the same format as the busy times.

    Input:
    - time_min: isoformat timestamp string. Example "2019-10-20T12:20:00.000+01:00"
    - time_max: isoformat timestamp string. Example "2019-10-20T15:50:00.000+01:00"
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

    Doctest
    >>> get_free_timeslots('2019-10-20T12:00:00.000+01:00', '2019-10-20T14:00:00.000+01:00', [['2019-10-20T13:00:00.000+01:00', '2019-10-20T14:00:00.000+01:00']])
    [['2019-10-20T12:00:00.000+01:00', '2019-10-20T13:00:00.000+01:00']]

    """
    reached_end_of_day = False
    beginning_of_free_time = time_min
    list_of_free_timesets = []
    next_free_timeset = None
    previous_result = []
    list_of_scheduled_timesets = copy.deepcopy(scheduled_time_blocks)

    while not reached_end_of_day:

        print_time_data(
            "Get free timeslot: (while loop) Next free timestamp",
            beginning_of_free_time,
            debug_mode,
        )
        print_time_data(
            "Get free timeslot: (while loop) Blocked time",
            list_of_scheduled_timesets,
            debug_mode,
        )
        print_time_data(
            "Get free timeslot: (while loop) List of free time",
            list_of_free_timesets,
            debug_mode,
        )

        free_timeset_results = get_next_available_open_timeset(
            beginning_of_free_time, list_of_scheduled_timesets, debug_mode
        )

        if free_timeset_results["reached_end_of_list"] and (
                free_timeset_results["next_free_timeset"] is None
        ):
            next_free_timeset = [beginning_of_free_time, time_max]
        elif (
                free_timeset_results["reached_end_of_list"]
                and free_timeset_results["next_free_timeset"] != []
        ):
            next_free_timeset = free_timeset_results["next_free_timeset"]
            free_timeset_results["reached_end_of_list"] = False

        if free_timeset_results["reached_end_of_list"]:
            print_time_data(
                "Get free timeslot: (while loop) Reached End of Day: Next free timeset",
                next_free_timeset,
                debug_mode,
            )
            reached_end_of_day = True
            if not free_timeset_results.get("next_free_timeset"):
                next_free_timeset = validate_update_timestamp(
                    next_free_timeset, list_of_scheduled_timesets, debug_mode
                )
        else:
            next_free_timeset = free_timeset_results["next_free_timeset"]

        if next_free_timeset not in list_of_free_timesets:
            duration_of_timeset = (
                datetime.fromisoformat(next_free_timeset[1])
                - datetime.fromisoformat(next_free_timeset[0])
            ).total_seconds()
            if duration_of_timeset >= 1:
                list_of_free_timesets.append(next_free_timeset)
        else:
            if previous_result == next_free_timeset:
                reached_end_of_day = True
                print_time_data(
                    "Get free timeslot: (while loop) Force closing loop because inf: Next free timeset",
                    next_free_timeset,
                    debug_mode,
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
        "Get free timeslot: Final List of free timesets",
        list_of_free_timesets,
        debug_mode,
    )

    return list_of_free_timesets
