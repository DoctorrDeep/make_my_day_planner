class BaseA(object):
    """
    hello A
    """
    def __init__(self, x, y):
        self.x = x  # self.__dict__["x"] = x
        self.y = y

    def sum(self):
        return self.x + self.y


class B(BaseA):
    pass



class BaseTimeSlot(object):

    def __init__(self, min_time, max_time):
        if min_time > max_time:
            min_time, max_time = max_time, min_time
        self.min_time = min_time
        self.max_time = max_time

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.min_time == other.min_time and self.max_time == other.max_time

    def __ne__(self, other):
        return not (self == other)

    def overlapping(self, other):
        return not (self.min_time >= other.max_time or self.max_time < other.min_time)


class Calendar(BaseTimeSlot):

    def __init__(self, owner, name, events, **kwargs):
        super().__init__(**kwargs)
        self.owner = owner
        self.name = name
        self.events = events

    def __len__(self):
        return len(self.events)

    def __iter__(self):
        return iter(self.events)

    def __contains__(self, item):
        return item in self.events

    def fits(self, event):
        pass



class Event(BaseTimeSlot):

    def __init__(self, min_time, max_time, status="attending"):
        super().__init__(min_time=min_time, max_time=max_time)
        self.status = status

    def __contains__(self, other):
        return self.min_time <= other < self.max_time

    def __str__(self):
        return f"{self.__class__.__name__}(min_time={self.min_time}, max_time={self.max_time}, status={self.status})"


if __name__ == "__main__":
    event = Event(0, 1, "happy")
    e1 = Event(2, 5)
    e2 = Event(3, 4)
    print(e1.overlapping(e2))
    print(3.5 in e1)
    e = Event(2,1)
    print(e.__dict__)

    print(e1 == e2)
    print(e1 != e2)

    cal = Calendar(min_time=0, max_time=24, owner=None, name="yes", events=[e, e1, e2])
    print(len(cal))
    min_times = [c.min_time for c in cal]
    print(min_times)
    print(e in cal)


