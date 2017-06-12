#!/usr/bin/python3

import unittest

from datetime import datetime, timedelta
from dateutil.rrule import rrule, YEARLY
from otto import Event, Task, Occurrence, Schedule


class TestEventMethods(unittest.TestCase):
    def test_init_full(self):
        an_event = Event("Djinn's birthday",
                         "Holding a memorial ceremony",
                         datetime(1998, 8, 17),
                         timedelta(1),
                         rrule(YEARLY, dtstart=datetime(1998,8,17))
                    )
        self.assertEqual(an_event._title, "Djinn's birthday")
        self.assertEqual(an_event._description, "Holding a memorial ceremony")
        self.assertEqual(an_event._start, datetime(1998, 8, 17))
        self.assertEqual(an_event._duration, timedelta(0,24*3600))
        self.assertEqual(str(an_event._repeating),
                         str(rrule(YEARLY, dtstart=datetime(1998,8,17))))
        #comparing strings because two rrule objects are considered distinct

    def test_init_default(self):
        an_event = Event("busy",
                         "no description",
                         datetime(2009, 3, 28),
                         timedelta(0,7200))
        self.assertEqual(an_event._repeating, None)

    def test_repr(self):
        an_event = Event("Djinn's birthday",
                         "Holding a memorial ceremony",
                         datetime(1998, 8, 17),
                         timedelta(1),
                         rrule(YEARLY, dtstart=datetime(1998,8,17))
                    )
        self.assertEqual(repr(an_event),
                         """otto.Event("Djinn's birthday", "Holding a memorial ceremony", datetime.datetime(1998, 8, 17, 0, 0), datetime.timedelta(1), dateutil.rrule.rrulestr("DTSTART:19980817T000000\nFREQ=YEARLY"))""")

    def test_str(self):
        an_event = Event("Djinn's birthday",
                         "Holding a memorial ceremony",
                         datetime(1998, 8, 17),
                         timedelta(1),
                         rrule(YEARLY, dtstart=datetime(1998,8,17))
                    )
        self.assertEqual(str(an_event),
                         """Event "Djinn's birthday" ("Holding a memorial ceremony")
Start date: 1998-08-17 00:00:00;
Duration: 1 day, 0:00:00;
Repeating:
DTSTART:19980817T000000
FREQ=YEARLY""")

if __name__ == "__main__":
    unittest.main()
