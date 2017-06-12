#!/usr/bin/python3

from datetime import datetime
from datetime import timedelta
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY, MO, TU, WE, TH, FR, SA, SU


class Event:
    """basic input of a Schedule"""

    def __init__(self, title, description, start, duration, repeating = None):
        """Build an event.

        title -- short string identifying the event
        description -- string describing the event in detail
        start -- datetime.datetime of the event's activation
        duration -- datetime.timedelta as long as one occurrence of that event
        repeating -- dateutil.rrule.rrule for recurring events (None if unique)
        """
        self._title = title
        self._description = description
        self._start = start
        self._duration = duration
        self._repeating = repeating

    def __repr__(self):
        """Give the event's string representation."""
        return """otto.Event("{0}", "{1}", {2}, {3}, {4})""".format(self._title, self._description, repr(self._start), repr(self._duration), 'dateutil.rrule.rrulestr("{}")'.format(self._repeating) if self._repeating != None else "None")

    def __str__(self):
        """Give the event's user-friendly string representation"""
        return """Event "{0}" ("{1}")
Start date: {2};
Duration: {3};
{4}""".format(self._title, self._description, self._start, self._duration, "Unique." if self._repeating == None else "Repeating:\n{}".format(self._repeating))


class Task (Event):
    """basic unit of a user's work to fit in a Schedule"""

    def __init__(self, title, description, start, duration, priority, due, repeating = None):
        """Build a task

        title -- short string identifying the event
        description -- string describing the event in detail
        start -- datetime.datetime of the event's activation
        duration -- datetime.timedelta as long as one occurrence of that event
        priority -- integer representing the importance of the task
        due -- datetime.datetime before when the task has to be done
        repeating -- dateutil.rrule.rrule for recurring events (None if unique)
        """
        super(Task, self).__init__(title, description, start, duration, repeating)
        self._priority = priority
        self._due = due

    def __repr__(self):
        """Give string representation of the task."""
        return """otto.Task("{0}", "{1}", {2}, {3}, {4}, {5}, {6})""".format(self._title, self._description, repr(self._start), repr(self._duration), self._priority, self._due, "rrulestr({})".format(self._repeating) if self._repeating != None else "None")

    def __str__(self):
        """Give user-friendly string representation of the task."""
        return """Task "{0}" ("{1}")
Start date: {2};
Duration: {3};
Priority: {4};
Due date: {5};
{6}""".format(self._title, self._description, self._start, self._duration, self._priority, self._due, "Unique." if self._repeating == None else "Repeating:\n{}".format(self._repeating))


class Occurrence:
    """Occurrence of an Event inside a Schedule"""

    def __init__(self, event, start, duration):
        """Build an Occurrence.

        event -- Event the Occurrence is an instance of
        start -- datetime.datetime of when the Occurrence starts
        duration -- datetime.timedelta length of the Occurrence
        """
        self._event = event
        self._start = start
        self._duration = duration
    def __repr__(self):
        """Give string representation of the Occurrence."""
        return "otto.Occurrence({0}, {1}, {2})".format(repr(self._event), repr(self._start), repr(self._duration))


class Schedule:
    """Auto-organizing Schedule"""

    def __init__(self, events, tasks, start=None):
        """Build a Schedule.

        events -- list of events sorted by start date
        tasks -- list of tasks sorted by start date
        start -- datetime.datetime of beginning of the Schedule (default to the earliest event of the list)
        """
        #events_, tasks_ = sorted(events, key=lambda e: e.start), sorted(tasks, key=lambda t: t.start)
        self._start = start if start != None else events[0]._start
        self._timeline = list()
        #finding the due date of the last task
        self._end = tasks[0]._due
        for t in tasks[1:]:
            if t._due > self._end:
                self._end = t._due
        for e in events: self._add_event(e)

    def __repr__(self):
        """Give the string representation of the timeline's content"""
        return "list({0})".format(",\n".join(repr(o) for o in self._timeline))

    def __str__(self):
        """Give the user-friendly string representation of the Schedule"""
        return '\n'.join("from {0} to {1}: {2}".format(o._start, o._start + o._duration, o._event._title) for o in self._timeline)


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

    def get_free_time(self,after, before=None):
        """Return a datetime.timedelta of the free time between two dates in this schedule.

        after -- datetime.datetime after which looking for free time
        before -- datetime.datetime before which looking for free time
        """
        if before == None: before = self._end
        #time to invest overall minus free time after "before"
        if before < self._end:
            return self.get_free_time(start, self._end) - self.get_free_time(end, self._end)
        free_time = timedelta(0)
        for i, occ in enumerate(self._timeline):
            if occ._start+occ._duration >= after:
                if i < len(self._timeline)-1:
                    free_time += (self._timeline[i+1]._start - (occ._start+occ._duration)) if (self._timeline[i+1]._start > occ._start+occ._duration) else timedelta(0)
                else:
                    free_time += before - (occ._start+occ._duration) if before > occ._start+occ._duration else timedelta(0)
        return free_time

#tests
if __name__ == "__main__":
    sleepEvent = Event("Sleeping", "Daily sleep", datetime(2016,1,1,20,0,0), timedelta(0,8*60*60), rrule(DAILY, dtstart=datetime(2016,1,1,20,0,0)))
    singleEvent = Event("Birthday", "random birthday", datetime(2017, 6, 29, 10, 0, 0), timedelta(1), None)
    firstTask = Task("First task", "This is my first task", datetime(2017,5,31,13,37), timedelta(0,5*60), 57, datetime(2017,6,6,12))
    print(sleepEvent)
    print(singleEvent)
    print(firstTask)
    aSchedule = Schedule([sleepEvent, singleEvent], [firstTask], datetime(2017,6,1,20))
    print(str(aSchedule))
    print(aSchedule.get_free_time(datetime(2017,6,1, 21)))
