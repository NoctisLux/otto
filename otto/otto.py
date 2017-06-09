#!/usr/bin/python3

from datetime import datetime
from datetime import timedelta
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY, MO, TU, WE, TH, FR, SA, SU


class Event:

    def __init__(self, title, description, start, duration, repeating = None):
        self._title = title
        self._description = description
        self._start = start
        self._duration = duration
        self._repeating = repeating

    def __repr__(self):
        return """otto.Event("{0}", "{1}", {2}, {3}, {4})""".format(self._title, self._description, repr(self._start), repr(self._duration), "rrulestr({})".format(self._repeating) if self._repeating != None else "None")

    def __str__(self):
        return """Event "{0}" ("{1}")
Start date: {2};
Duration: {3};
{4}""".format(self._title, self._description, self._start, self._duration, "Unique." if self._repeating == None else "Repeating:\n{}".format(self._repeating))


class Task (Event):

    def __init__(self, title, description, start, duration, priority, due, repeating = None):
        super(Task, self).__init__(title, description, start, duration, repeating)
        self._priority = priority
        self._due = due

    def __repr__(self):
        return """otto.Task("{0}", "{1}", {2}, {3}, {4}, {5}, {6})""".format(self._title, self._description, repr(self._start), repr(self._duration), self._priority, self._due, "rrulestr({})".format(self._repeating) if self._repeating != None else "None")

    def __str__(self):
        return """Task "{0}" ("{1}")
Start date: {2};
Duration: {3};
Priority: {4};
Due date: {5};
{6}""".format(self._title, self._description, self._start, self._duration, self._priority, self._due, "Unique." if self._repeating == None else "Repeating:\n{}".format(self._repeating))


class Occurrence:

    def __init__(self, event, start, duration):
        self._event = event
        self._start = start
        self._duration = duration
    def __repr__(self):
        return "otto.Occurrence({0}, {1}, {2})".format(repr(self._event), repr(self._start), repr(self._duration))


class Schedule:

    def __init__(self, events, tasks, start=None):
        #events_, tasks_ = sorted(events, key=lambda e: e.start), sorted(tasks, key=lambda t: t.start)
        self._start = start if start != None else events[0]._start
        self._timeline = list()
        #finding the due date of the last task
        self._end = tasks[0]._due
        for t in tasks[1:]:
            if t._due > self._end:
                self._end = t._due
        for e in events: self._add_event(e)

    def _add_event(self, event):
        if event._repeating == None:
            self._add_occ(Occurrence(event, event._start, event._duration))
        else:
            #will probably be better with rrule.replace()
            for d in event._repeating.between(self._start, self._end, inc=True):
                self._add_occ(Occurrence(event, d, event._duration))

    def _add_occ(self, occ):
        self._timeline.append(occ)
        self._timeline.sort(key=lambda o: o._start)

#tests
if __name__ == "__main__":
    sleepEvent = Event("Sleeping", "Daily sleep", datetime(2016,1,1,20,0,0), timedelta(0,8*60*60), rrule(DAILY, dtstart=datetime(2016,1,1,20,0,0)))
    singleEvent = Event("Birthday", "random birthday", datetime(2017, 6, 29, 10, 0, 0), timedelta(0, 10*60*60), None)
    firstTask = Task("First task", "This is my first task", datetime(2017,5,31,13,37), timedelta(0,5*60), 57, datetime(2017,6,6,12))
    print(sleepEvent)
    print(singleEvent)
    print(firstTask)
    aSchedule = Schedule([sleepEvent, singleEvent], [firstTask], datetime(2017,6,1,20))
