#!/usr/bin/python3

from datetime import datetime
from datetime import timedelta

class Event:
    def __init__(self, title_, description_, start_, duration_, repeating_ = None):
        self.title = title_
        self.description = description_
        self.start = start_
        self.duration = duration_
        self.repeating = repeating_

class Task (Event):
    def __init__(self, title_, description_, start_, duration_, priority_, due_, repeating_ = None):
        super(Task, self).__init__(title_, description_, start_, duration_, repeating_)
        self.priority = priority_
        self.due = due_

class Schedule:
    def __init__(self, events):
        self.timeline = list()

#tests
if __name__ == "__main__":
    a = Event("First event", "This is my first event", datetime.now(), timedelta(0,3600))

    print("""Event "{0}": {1};
start: {2};
duration: {3}.""".format(a.title, a.description, str(a.start), str(a.duration)))
    b = Task("First task", "This is my first task", datetime(2017,5,31,13,37), timedelta(0,5*60), 57, datetime(2017,6,6,12))
    print("""Task "{0}": {1};
start: {2};
duration: {3};
priority: {4};
due date: {5}.""".format(b.title, b.description, str(b.start), str(b.duration), b.priority, str(b.due)))
