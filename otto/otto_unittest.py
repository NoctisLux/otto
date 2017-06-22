#!/usr/bin/python3

import unittest

from datetime import datetime, timedelta
from dateutil.rrule import rrule, YEARLY, DAILY, MO, TU, WE, TH, FR, SA, SU
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

    def test_repr_unique(self):
        an_event = Event("Hammer time",
                         "no description",
                         datetime(2017, 5, 5, 8, 20, 37),
                         timedelta(0,300))
        self.assertEqual(repr(an_event),
                         """otto.Event("Hammer time", "no description", datetime.datetime(2017, 5, 5, 8, 20, 37), datetime.timedelta(0, 300), None)""")

    def test_repr_repeating(self):
        an_event = Event("Djinn's birthday",
                         "Holding a memorial ceremony",
                         datetime(1998, 8, 17),
                         timedelta(1),
                         rrule(YEARLY, dtstart=datetime(1998,8,17))
                    )
        self.assertEqual(repr(an_event),
                         """otto.Event("Djinn's birthday", "Holding a memorial ceremony", datetime.datetime(1998, 8, 17, 0, 0), datetime.timedelta(1), dateutil.rrule.rrulestr("DTSTART:19980817T000000\nFREQ=YEARLY"))""")

    def test_str_unique(self):
        an_event = Event("Hammer time",
                         "no description",
                         datetime(2017, 5, 5, 8, 20, 37),
                         timedelta(0,300))
        self.assertEqual(str(an_event),
                         """Event "Hammer time" ("no description")
Start date: 2017-05-05 08:20:37;
Duration: 0:05:00;
Unique.""")

    def test_str_repeating(self):
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

    def test_wrongduration(self):
        with self.assertRaises(ValueError, msg="Duration is inferior to datetime.timedelta(0)"):
            an_event = Event("negative time!!!", "no description", datetime(2017,5,5), timedelta(0,-1))


class TestTaskMethods (unittest.TestCase):

    def test_init(self):
        some_task = Task("computer maintenance",
                         "keeping it all neat and working",
                         datetime(2016,1,1),
                         timedelta(0,1200),
                         20,
                         datetime(2016,1,2,12),
                         rrule(DAILY, dtstart=datetime(2016,1,1))
        )
        self.assertEqual(some_task._title, "computer maintenance")
        self.assertEqual(some_task._description, "keeping it all neat and working")
        self.assertEqual(some_task._start, datetime(2016,1,1))
        self.assertEqual(some_task._duration, timedelta(0,1200))
        self.assertEqual(some_task._priority, 20)
        self.assertEqual(some_task._due, datetime(2016,1,2,12))
        self.assertEqual(str(some_task._repeating),
                         "DTSTART:20160101T000000\nFREQ=DAILY")

    def test_init_default(self):
        some_task = Task("debugging",
                         "debug this one unit test",
                         datetime(2017,6,17,12,50,0),
                         timedelta(0,300),
                         70,
                         datetime(2020,1,1))
        self.assertEqual(some_task._title, "debugging")
        self.assertEqual(some_task._description, "debug this one unit test")
        self.assertEqual(some_task._start, datetime(2017,6,17,12,50,0))
        self.assertEqual(some_task._duration, timedelta(0,300))
        self.assertEqual(some_task._priority, 70)
        self.assertEqual(some_task._due, datetime(2020,1,1))

    def test_repr_unique(self):
        some_task = Task("debugging",
                         "debug this one unit test",
                         datetime(2017,6,17,12,50,0),
                         timedelta(0,300),
                         70,
                         datetime(2020,1,1),
                         None)
        self.assertEqual(repr(some_task),
                         """otto.Task("debugging", "debug this one unit test", datetime.datetime(2017, 6, 17, 12, 50), datetime.timedelta(0, 300), 70, datetime.datetime(2020, 1, 1, 0, 0), None)""")

    def test_repr_repeating(self):
        some_task = Task("computer maintenance",
                         "keeping it all neat and working",
                         datetime(2016,1,1),
                         timedelta(0,1200),
                         20,
                         datetime(2016,1,2,12),
                         rrule(DAILY, dtstart=datetime(2016,1,1))
        )
        self.assertEqual(repr(some_task),
                         """otto.Task("computer maintenance", "keeping it all neat and working", datetime.datetime(2016, 1, 1, 0, 0), datetime.timedelta(0, 1200), 20, datetime.datetime(2016, 1, 2, 12, 0), dateutil.rrule.rrulestr("DTSTART:20160101T000000\nFREQ=DAILY"))""")

    def test_str_unique(self):
        some_task = Task("debugging",
                         "debug this one unit test",
                         datetime(2017,6,17,12,50,0),
                         timedelta(0,300),
                         70,
                         datetime(2020,1,1),
                         None)
        self.assertEqual(str(some_task),
                         """Task "debugging" ("debug this one unit test")
Start date: 2017-06-17 12:50:00;
Duration: 0:05:00;
Priority: 70;
Due date: 2020-01-01 00:00:00;
Unique.""")

    def test_str_repeating(self):
        some_task = Task("computer maintenance",
                         "keeping it all neat and working",
                         datetime(2016,1,1),
                         timedelta(0,1200),
                         20,
                         datetime(2016,1,2,12),
                         rrule(DAILY, dtstart=datetime(2016,1,1))
        )
        self.assertEqual(str(some_task),
                         """Task "computer maintenance" ("keeping it all neat and working")
Start date: 2016-01-01 00:00:00;
Duration: 0:20:00;
Priority: 20;
Due date: 2016-01-02 12:00:00;
Repeating:
DTSTART:20160101T000000
FREQ=DAILY""")

    def test_priority(self):
        with self.assertRaises(ValueError, msg="Priority is inferior to 0"):
            a = Task("low priority", "priority so low, procrastinating is more productive", datetime(2017,5,2), timedelta(0,17), -5, datetime(2017,5,3))
        with self.assertRaises(ValueError, msg="Priority is superior to 99"):
            a = Task("high priority", "priority so high, it's already too late", datetime(2017,5,2), timedelta(0,17), 100, datetime(2017,5,3))

    def test_due(self):
        with self.assertRaises(ValueError, msg="The task is due before it starts"):
            a = Task("invalid due date", "had to be finished the day before you'll start", datetime(2017,5,2), timedelta(0,1200), 45, datetime(2017,5,1))
        with self.assertRaises(ValueError, msg="The task is due before it can finish"):
            a = Task("other invalid due date", "have to bend time to finish it in time", datetime(2017,5,2,8), timedelta(0,1200), 50, datetime(2017,5,2,8,15))

class TestOccurrenceMethods (unittest.TestCase):

    def test_init(self):
        an_occurrence = Occurrence(Event("t", "d", datetime(2017,2,28), timedelta(0,1800)), datetime(2017,2,28), timedelta(0,1800))
        self.assertEqual(an_occurrence._start, datetime(2017,2,28))
        self.assertEqual(an_occurrence._duration, timedelta(0,1800))
        self.assertEqual(repr(an_occurrence._event),
                         """otto.Event("t", "d", datetime.datetime(2017, 2, 28, 0, 0), datetime.timedelta(0, 1800), None)""")

    def test_repr(self):
        an_occurrence = Occurrence(Event("t", "d", datetime(2017,2,28), timedelta(0,1800)), datetime(2017,2,28), timedelta(0,1800))
        self.assertEqual(repr(an_occurrence),
                         """otto.Occurrence(otto.Event("t", "d", datetime.datetime(2017, 2, 28, 0, 0), datetime.timedelta(0, 1800), None), datetime.datetime(2017, 2, 28, 0, 0), datetime.timedelta(0, 1800))""")

class TestScheduleMethods (unittest.TestCase):

    def setup(self):
        self.events_list = {
            Event("Daily sleep", "sleep is important!", datetime(2000, 1, 1, 0, 0), timedelta(0, 28800), rrule(DAILY, dtstart=datetime(2000, 1, 1, 21, 0, 0), byweekday={MO, TU, WE, TH, SU})),
            Event("Weekend sleep", "sleep is even better!", datetime(2000, 1, 1, 0, 0), timedelta(0,28800), rrule(DAILY, dtstart=datetime(2000, 1, 1, 23, 0, 0), byweekday={FR, SA})),
            Event("resting", "not working", datetime(2000, 1, 1, 0, 0), timedelta(0, 43200), rrule(DAILY, dtstart=datetime(2000, 1, 1, 12, 0, 0), byweekday={WE, SU})),
            Event("marriage", "out for the day", datetime(2016, 3, 4, 0, 0, 0), timedelta(1), None)}
        self.tasks_list = {
            Task("eating", "a good meal!", datetime(2016, 2, 22, 0, 0, 0), timedelta(0, 5400), 90, datetime(2016, 2, 22, 21, 0, 0), rrule(DAILY, dtstart=datetime(2016, 2, 22, 12, 0, 0))),
            Task("", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Marjana Tereza", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Aditya Sorcha", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Bohdan Petronella", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Wealdmær Amiran", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Monica Ebba", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Rakel Johnathan", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Constance Rajendra", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Melissa Thomas", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Aurea Slàine", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Mateus Sevinc", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Eliza Aamir", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Candidus Ælfwig", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Hovo Gena", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Mamoun Darayavahush", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Dagny Emmanuhel", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Laraine Olavi", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Theo Cyra", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Tarquinius Edna", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Narangerel Frīdrihs", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Siavash Lina", "2h-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,7200), 70, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Santos Patterson", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Tommye Norsworthy", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Olene Creager", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Jayna Lockard", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Marlon Remigio", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Lael Saam", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Kylee Cusick", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Kyong Parkman", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Deena Mcevoy", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Vertie Dymond", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Katrice Hildreth", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Maryjane Beshears", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Katherine Marro", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Sherrill Zylstra", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Melony Villagrana", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Lynnette Forst", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Angie Anzaldua", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Freida Lingenfelter", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Esmeralda Delosantos", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Reynaldo Stirling", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Nicolasa Kendrick", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Malika Spore", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Donnetta Piersall", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Lloyd Travis", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Regenia Volker", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Ernestina Truehart", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Paulette Pautz", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Rochelle Luck", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Alec Sabia", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Eloy Byram", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Agustina Schuller", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Gracia Willimas", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Sasha Capone", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Celeste Wakeland", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Miki Carrithers", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Cherelle Nowakowski", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Floretta Lazaro", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Elin Baugher", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Dalton Haake", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Felicia Stimage", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Rosaria Shand", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Loralee Mansker", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Hilma Lovering", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Crissy Almanza", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Eleanor Manjarrez", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Kathline Apperson", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Willetta Dobrowolski", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Sade Lovett", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Silvia Mahony", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0)),
            Task("Armida Bobo", "20min-long medical appointment", datetime(2016, 2, 22, 0, 0, 0), timedelta(0,1200), 50, datetime(2016, 3, 6, 0, 0, 0))}

    def test_init(self):
        pass

    def test_init_default(self):
        pass

    def test_repr(self):
        pass

    def test_str(self):
        pass

    def test_freetime_simple(self):
        pass                      

    def test_freetime_intervals(self):
        pass
if __name__ == "__main__":
    unittest.main()
