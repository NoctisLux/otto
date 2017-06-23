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
{4}""".format(self._title, self._description, self._start, self._duoration, "Unique." if self._repeating == None else "Repeating:\n{}".format(self._repeating))


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
        return """otto.Task("{0}", "{1}", {2}, {3}, {4}, {5}, {6})""".format(self._title, self._description, repr(self._start), repr(self._duration), self._priority, repr(self._due), 'dateutil.rrule.rrulestr("{}")'.format(self._repeating) if self._repeating != None else "None")

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
        #in case we want to sort it: events_, tasks_ = sorted(events, key=lambda e: e.start), sorted(tasks, key=lambda t: t.start)

        self._start = start if start != None else events[0]._start
        self._timeline = list()
        
        #finding the due date of the last task
        self._end = tasks[0]._due
        for t in tasks[1:]:
            if t._due > self._end:
                self._end = t._due
        for e in events: self._add_event(e)

        #truncating the part of the timeline before start
        if self._timeline[0]._start < self.start:
            tronc = 0
            for i, o in enumerate(self._timeline):
                if o._start + o._duration <= self.start:
                    tronc = i #identify where the start is;
            del self._timeline[:i+1] #remove what ends before;
            for o in self._timeline: #and shave what starts before.
                if o._start < self._start:
                    o._duration -= (self._start - o._start)
                    o._start = self._start
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

    def get_free_intervals(after, before=None):
        """Return a list of tuples (datetime.datetime, datetime.datetime) representing the intervals of free time of this schedule.

        after -- datetime.datetime after which looking for free time
        before -- datetime.datetime before which looking for free time
        """
        intervals = list()
        #entire list of intervals
        for i, occ in enumerate(self._timeline):
                if i < len(self._timeline)-1:
                    if occ._start+occ._duration < self_timeline[i+1]._start:
                        intervals.append(tuple((occ._start+occ._duration, self_timeline[i+1]._start))) 
                else:
                    if before > occ._start+occ._duration:
                        intervals.append(tuple((occ._start+occ._duration, before)))
        
        #cutting before start and after end
        for i, t in enumerate(intervals):
            if t[1] <= after:
                trimstart = i
            elif trimend != None and t[0] >= before:
                trimend = i
        del intervals[:trimstart+1]
        del intervals[trimend+1:]

        #trimming first and last if needed
        if intervals[0][0] > after and intervals[0][1] < after:
            intervals.insert(1, tuple((after, intervals[0][1])))
            del intervals[0]
        if intervals[-1][1] > before and intervals[-1][0] < before:
            intervals.append(tuple((intervals[-1][0], before)))
            del intervals[-2]

        return intervals

#tests
if __name__ == "__main__":
    print(str(Task("a task", "description of it", datetime.now(), timedelta(0,360), 99, datetime.now()+timedelta(1), rrule(DAILY, dtstart=datetime.now()))))
