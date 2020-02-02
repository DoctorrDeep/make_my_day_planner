from app_scripts.get_free_timeslots import get_free_timeslots

"""
Pytest file for testing.
Run with `pytest` in root of project
"""

"""
If any test fails, drop to the python shell and use the following to execute
tests for a specific time_min

```
from app_scripts.get_free_timeslots import get_free_timeslots
time_min = '2019-12-14T13:00:00+01:00'
time_max = '2019-12-14T23:59:00+01:00'
scheduled_time_blocks = [['2019-12-14T09:00:00+01:00', '2019-12-14T10:00:00+01:00'],
 ['2019-12-14T11:00:00+01:00', '2019-12-14T12:30:00+01:00'],
 ['2019-12-14T11:30:00+01:00', '2019-12-14T12:00:00+01:00'],
 ['2019-12-14T14:00:00+01:00', '2019-12-14T15:00:00+01:00'],
 ['2019-12-14T14:30:00+01:00', '2019-12-14T16:00:00+01:00'],
 ['2019-12-14T17:00:00+01:00', '2019-12-14T18:00:00+01:00'],
 ['2019-12-14T18:00:00+01:00', '2019-12-14T19:00:00+01:00']]
get_free_timeslots(time_min, time_max, scheduled_time_blocks)

```

"""

time_min = "2020-01-09T09:02:58.350498+01:00"
time_max = "2020-01-09T23:59:59+01:00"
scheduled_time_blocks = [
    ["2020-01-09T09:00:00+01:00", "2020-01-09T10:00:00+01:00"],
    ["2020-01-09T10:00:00+01:00", "2020-01-09T11:00:00+01:00"],
    ["2020-01-09T11:00:00+01:00", "2020-01-09T12:00:00+01:00"],
    ["2020-01-09T12:00:00+01:00", "2020-01-09T12:30:00+01:00"],
    ["2020-01-09T13:00:00+01:00", "2020-01-09T14:30:00+01:00"],
]
expected_free_timeblocks = [
    ["2020-01-09T12:30:00+01:00", "2020-01-09T13:00:00+01:00"],
    ["2020-01-09T14:30:00+01:00", "2020-01-09T23:59:59+01:00"],
]
received_free_timeblocks = get_free_timeslots(
    time_min=time_min,
    time_max=time_max,
    scheduled_time_blocks=scheduled_time_blocks,
    debug_mode=True,
)


def test_complex_case_1():
    assert received_free_timeblocks == expected_free_timeblocks
