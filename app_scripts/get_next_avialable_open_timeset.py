from datetime import datetime
from app_scripts.print_time_data import print_time_data
from app_scripts.validate_update_timestamp import validate_update_timestamp


def get_next_avialable_open_timeset(
    a_timestamp: str, list_of_timesets: list, debug_mode: bool = False
) -> dict:
    """
    This function will hop throught a list of events provided as input and
    check till when there is free time based on one initial timestamp also
    provided in the input.
    If it has not found the free time at the end of the list then it informs
    that the end of the list has been reached

    Input
    a_timestamp: isoformat timestamp string. Example "2019-10-20T12:20:00.000+01:00"
    list_of_timesets: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                    ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
                ]

    Output
    dictionary:
        next_free_timeset: list of 2 isoformat timestamp strings
            Example: ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00']
        reached_end_of_list: Boolean

    Doctest
    >>> get_next_avialable_open_timeset('2019-10-20T12:20:00.000+01:00', [['2019-12-20T19:30:00+01:00', '2019-12-20T19:45:00+01:00']])
    {'next_free_timeset': ['2019-10-20T12:20:00.000+01:00', '2019-12-20T19:30:00+01:00'], 'reached_end_of_list': False}
    """

    results = {"next_free_timeset": None, "reached_end_of_list": True}

    sorted_list_of_timesets = sorted(list_of_timesets, key=lambda k: k[0])

    filtered_list_of_timesets = []
    for timeset in sorted_list_of_timesets:
        if datetime.fromisoformat(a_timestamp) <= datetime.fromisoformat(timeset[1]):
            filtered_list_of_timesets.append(timeset)

    if filtered_list_of_timesets != sorted_list_of_timesets:
        print_time_data(
            "Next available_timeset: filtering effect from:",
            sorted_list_of_timesets,
            debug_mode,
        )
        print_time_data(
            "Next available_timeset: filtering effect to:",
            filtered_list_of_timesets,
            debug_mode,
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
                "Next available_timeset: Going to break: current timeset",
                timeset,
                debug_mode,
            )
            print_time_data(
                "Next available_timeset: Going to break: timestamp",
                temp_timestamp,
                debug_mode,
            )
            print_time_data(
                "Next available_timeset: Going to break: results", results, debug_mode
            )
            break

        temp_timestamp = timeset[1]

    # Check if the found timeset has a startTime
    # inside another timeset
    if results["next_free_timeset"]:
        temp_timeset = validate_update_timestamp(
            results["next_free_timeset"], filtered_list_of_timesets, debug_mode
        )
        results["next_free_timeset"] = temp_timeset

    print_time_data("Next available_timeset: Final results", results, debug_mode)

    return results
