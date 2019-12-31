from pprint import pprint


def print_time_data(
    helptext: str, timestr, debug_mode: bool = False, override_debug: bool = False
):

    if debug_mode or override_debug:
        print("\n", helptext)
        pprint(timestr)
