import copy

from datetime import datetime


def validate_update_timeset(a_timeset: list) -> list:
    """
    Check if the timeset supplied makes sense.
    - whether they are in correct order (time should increase from 1 to 2)
    - correct the order
    - if they are the same then make sure that they have a 1 microsecond time diff

    Input
    a_timeset: list of 2 isoformat timestamp strings.
        Example: ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00']
    Output
    a_timeset: list of 2 isoformat timestamp strings.
        Example: ['2019-12-20T09:30:00+01:00', '2019-12-20T09:45:00+01:00']
    """

    new_timeset = copy.deepcopy(a_timeset)

    if datetime.fromisoformat(a_timeset[1]) <= datetime.fromisoformat(a_timeset[0]):
        new_timeset = [
            a_timeset[0],
            (
                datetime.fromisoformat(a_timeset[0]) + timedelta(microseconds=1)
            ).isoformat(),
        ]

    return new_timeset
