from app_scripts.break_up_free_timeblocks import break_up_free_timeblocks

time_s_p = ["2019-12-14T", ":00+01:00"]


def test_break_up_free_timeblocks_single_timeblock_cases_1():
    free_timeslots_raw = [["08:00", "10:00"]]

    expected_plannable_timeblocks_raw = [["08:00", "09:00"], ["09:00", "10:00"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_2():
    free_timeslots_raw = [["08:00", "09:30"]]

    expected_plannable_timeblocks_raw = [["08:00", "09:00"], ["09:00", "09:30"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_3():
    free_timeslots_raw = [["08:00", "08:30"]]

    expected_plannable_timeblocks_raw = [["08:00", "08:30"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_4():
    free_timeslots_raw = [["08:00", "09:00"]]

    expected_plannable_timeblocks_raw = [["08:00", "09:00"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_5():
    free_timeslots_raw = [["08:00", "08:05"]]

    expected_plannable_timeblocks = []

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_6():
    free_timeslots_raw = [["08:00", "08:55"]]

    expected_plannable_timeblocks_raw = [["08:00", "08:55"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_7():
    free_timeslots_raw = [["08:00", "09:05"]]

    expected_plannable_timeblocks_raw = [["08:00", "09:00"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_8():
    free_timeslots_raw = [["08:00", "09:11"]]

    expected_plannable_timeblocks_raw = [["08:00", "09:00"], ["09:00", "09:11"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks


def test_break_up_free_timeblocks_single_timeblock_cases_9():
    free_timeslots_raw = [["08:00", "09:10"]]

    expected_plannable_timeblocks_raw = [["08:00", "09:00"], ["09:00", "09:10"]]

    free_timeslots = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in free_timeslots_raw
    ]

    expected_plannable_timeblocks = [
        [f"{time_s_p[0]}{i[0]}{time_s_p[1]}", f"{time_s_p[0]}{i[1]}{time_s_p[1]}"]
        for i in expected_plannable_timeblocks_raw
    ]

    calculated_free_timeslots = break_up_free_timeblocks(free_timeslots)
    assert calculated_free_timeslots == expected_plannable_timeblocks
