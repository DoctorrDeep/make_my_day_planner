from datetime import datetime, timedelta

minute_blocks = [[0, 15], [15, 30], [30, 45], [45, 59]]


def round_timeblocks(list_of_timeblocks: list) -> list:
    """
    This function will take the first free timeslot (since its based on NOW)
    and break it into 2 parts. the break point will be the nearest 15 minutes.
    The returned list will have at most 1 extra timeblock

    Input
    list_of_timeblocks: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:35:00+01:00', '2019-12-20T10:00:00+01:00'],
                    ['2019-12-20T10:00:00+01:00', '2019-12-20T12:13:00+01:00']
                ]

    Output
    round_timeblocks: list of list of 2 timestamps (each formatted as described above)
        Example: [
                    ['2019-12-20T09:35:00+01:00', '2019-12-20T09:45:00+01:00'],
                    ['2019-12-20T09:45:00+01:00', '2019-12-20T10:00:00+01:00'],
                    ['2019-12-20T10:00:00+01:00', '2019-12-20T12:13:00+01:00']
                ]

    Doctest
    >>> round_timeblocks([['2019-12-20T09:35:00+01:00', '2019-12-20T10:00:00+01:00'], ['2019-12-20T10:00:00+01:00', '2019-12-20T12:13:00+01:00']])
    [['2019-12-20T09:35:00+01:00', '2019-12-20T09:45:00+01:00'], ['2019-12-20T09:45:00+01:00', '2019-12-20T10:00:00+01:00'], ['2019-12-20T10:00:00+01:00', '2019-12-20T12:13:00+01:00']]
    """

    if len(list_of_timeblocks) == 0:
        return list_of_timeblocks

    round_timeblocks = list_of_timeblocks[1:]
    first_timeblock = list_of_timeblocks[0]
    first_timestamp = first_timeblock[0]

    minute_of_timestamp = datetime.fromisoformat(first_timestamp).minute
    hour_of_timestamp = datetime.fromisoformat(first_timestamp).hour

    if hour_of_timestamp == 23:
        return list_of_timeblocks

    block_index = None
    new_minute = None

    for i, block in enumerate(minute_blocks):
        if minute_of_timestamp >= block[0] and minute_of_timestamp <= block[1]:
            block_index = i

    temp_time = datetime.fromisoformat(first_timestamp)
    try:
        new_minute = minute_blocks[block_index + 1][0]
        break_point = temp_time.replace(minute=new_minute, second=0, microsecond=0)
    except IndexError:
        break_point = temp_time.replace(minute=0, second=0, microsecond=0) + timedelta(
            hours=1
        )

    break_point_string = break_point.isoformat()

    new_timeblocks = [
        [first_timeblock[0], break_point_string],
        [break_point_string, first_timeblock[1]],
    ]
    new_timeblocks.reverse()

    for i in new_timeblocks:
        round_timeblocks.insert(0, i)

    return round_timeblocks
