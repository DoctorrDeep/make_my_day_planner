from pprint import pprint


def print_time_data(
        helptext: str, timedata=[], debug_mode: bool = False, override_debug: bool = False
):
    """
    This will print results in a nice format.
    In future it can also use logging if the need arises.

    Doctest
    >>> print_time_data("Try this", [1,2,3])

    """

    if debug_mode or override_debug:
        print("\n", helptext)
        pprint(timedata)
