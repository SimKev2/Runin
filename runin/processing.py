from __future__ import unicode_literals
from collections import defaultdict

from dateutil import parser

from google_calendar.api import events


class CalendarEvent(object):
    """
    Object containing information about a calendar event.

    :ivar end_time: Datetime object of event end time
    :ivar start_time: Datetime object of event start time
    :ivar summary: String of the event summary
    """
    def __init__(self, json_event):
        self.end_time = parser.parse(json_event.get('endTime'))
        self.start_time = parser.parse(json_event.get('startTime'))
        self.summary = json_event.get('summary')

    @property
    def day(self):
        """The day the event is on 2016-09-19"""
        return str(self.start_time.date())


def free_time(cal_schedule):
    """
    Find 40+ minute times during the day (7 am - 10 pm) that are unscheduled.

    Free time example return:
    {
      '2016-08-16': [
        ('2016-08-19T07:00:00-5:00', '2016-08-19T09:00:00-5:00'),
        ('2016-08-19T20:00:00-5:00', '2016-08-19T22:00:00-5:00')
      ]
    }

    :param cal_schedule: The events on calendar stored by day.
    :type cal_schedule: dict of CalendarEvent objects
    :return: Free time for each day in cal_schedule
    :rtype: dict
    """
    print cal_schedule


def event_group(start_date, end_date):
    """
    Groups events from user's calendars by day.

    :param start_date:
    :type start_date: str in UTC ISO format
    :param end_date:
    :type end_date: str in UTC ISO format
    :return: All events on calendar for each day between dates (inclusive)
    :rtype: dict of CalendarEvent objects
    """
    all_events = []
    for cal in events.calendars():
        c_events = events.get_events(cal, start_date, end_date)
        all_events.extend([CalendarEvent(e) for e in c_events])

    day_schedule = defaultdict(list)
    for cal_e in sorted(all_events, key=lambda x: x.day):
        day_schedule[cal_e.day].append(cal_e)

    return day_schedule


if __name__ == '__main__':
    event_group('2016-09-17T12:00:00Z', '2016-09-20T00:00:00Z')
