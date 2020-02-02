import copy
from datetime import datetime, timedelta

from app_scripts.print_time_data import print_time_data

MIN_TIMEBLOCK_DURATION = 600


def break_up_free_timeblocks(
    free_timeblocks_list: list, block_size: int = 3600, debug_mode: bool = False
) -> list:
    """
    This function will hop through a list of timeblocks provided as input and
    break them into smaller timeblocks of a designated size. The size defaults
    to one hour and can be changed. It is set in seconds.
    Any times smaller than 10 minutes will be omitted from the final list

    Input
    free_timeblocks_list: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                    ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
                ]

    Output
    plannable_timeblocks_list: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T14:45:00+01:00', '2019-12-20T18:45:00+01:00'],
                    ['2019-12-20T17:00:00+01:00', '2019-12-20T17:45:00+01:00']
                ]

    Doctest
    >>> break_up_free_timeblocks([['2019-12-20T14:45:00+01:00', '2019-12-20T16:45:00+01:00']], 3600)
    [['2019-12-20T14:45:00+01:00', '2019-12-20T15:45:00+01:00'], ['2019-12-20T15:45:00+01:00', '2019-12-20T16:45:00+01:00']]
    """

    if MIN_TIMEBLOCK_DURATION >= block_size:
        print_time_data("Could not process since min block duration is ")
        return free_timeblocks_list

    plannable_timeblocks_list = []
    temp_timeblocks_list = []

    for timeblock in free_timeblocks_list:

        reached_end_of_timeblock = False
        start_time = datetime.fromisoformat(timeblock[0])
        end_time = datetime.fromisoformat(timeblock[1])

        while not reached_end_of_timeblock:

            temp_end_time = start_time + timedelta(seconds=block_size)

            if temp_end_time < end_time:
                temp_timeblocks_list.append(
                    [start_time.isoformat(), temp_end_time.isoformat()]
                )
                start_time = copy.deepcopy(temp_end_time)
            else:
                temp_timeblocks_list.append(
                    [start_time.isoformat(), end_time.isoformat()]
                )
                reached_end_of_timeblock = True

        print_time_data("Big timeblock", timeblock, debug_mode)
        print_time_data("Broken timeblock", temp_timeblocks_list, debug_mode)

    for timeblock in temp_timeblocks_list:
        duration_of_timeblock = (
            datetime.fromisoformat(timeblock[1]) - datetime.fromisoformat(timeblock[0])
        ).total_seconds()

        if duration_of_timeblock >= MIN_TIMEBLOCK_DURATION:
            plannable_timeblocks_list.append(timeblock)

    if debug_mode:
        drop_in_number = len(temp_timeblocks_list) - len(plannable_timeblocks_list)
        print_time_data(
            f"{str(drop_in_number)} lesser timeblocks due to small durations"
        )

    return plannable_timeblocks_list
