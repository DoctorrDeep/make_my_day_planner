from app_scripts.round_timeblocks import round_timeblocks

time_s_p = ["2019-12-14T", "+01:00"]
max_time = f"23:59:59"


def test_round_timeblocks_cases_1():
    free_timeslots_raw = [["08:00:00", "12:00:00"], ["12:00:00", max_time]]

    expected_rounded_timeblocks_raw = [
        ["08:00:00", "08:15:00"],
        ["08:15:00", "12:00:00"],
        ["12:00:00", max_time],
    ]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_2():
    free_timeslots_raw = [["08:00:15", "12:00:00"], ["12:00:00", max_time]]

    expected_rounded_timeblocks_raw = [
        ["08:00:15", "08:15:00"],
        ["08:15:00", "12:00:00"],
        ["12:00:00", max_time],
    ]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_3():
    free_timeslots_raw = [["08:15:00", max_time]]

    expected_rounded_timeblocks_raw = [["08:15:00", "08:30:00"], ["08:30:00", max_time]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_4():
    free_timeslots_raw = [["08:15:15", max_time]]

    expected_rounded_timeblocks_raw = [["08:15:15", "08:30:00"], ["08:30:00", max_time]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_5():
    free_timeslots_raw = [["08:30:00", max_time]]

    expected_rounded_timeblocks_raw = [["08:30:00", "08:45:00"], ["08:45:00", max_time]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_6():
    free_timeslots_raw = [["08:30:50", max_time]]

    expected_rounded_timeblocks_raw = [["08:30:50", "08:45:00"], ["08:45:00", max_time]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_7():
    free_timeslots_raw = [["08:45:00", max_time]]

    expected_rounded_timeblocks_raw = [["08:45:00", "09:00:00"], ["09:00:00", max_time]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_8():
    free_timeslots_raw = [["08:45:45", max_time]]

    expected_rounded_timeblocks_raw = [["08:45:45", "09:00:00"], ["09:00:00", max_time]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks


def test_round_timeblocks_cases_9():
    free_timeslots_raw = [["23:10:00", max_time]]

    expected_rounded_timeblocks_raw = [["23:10:00", max_time]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_rounded_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_rounded_timeblocks_raw
    ]

    calculated_rounded_timeslots = round_timeblocks(free_timeslots)
    assert calculated_rounded_timeslots == expected_rounded_timeblocks
