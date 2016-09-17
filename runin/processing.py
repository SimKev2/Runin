from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime

from google_calendar.api import events


def free_time(cal_schedule):
    """
    Find times during the day that are unscheduled.

    Free time example return:
    {
      '2016-08-16': [
        CalendarEvent('2016-08-19T07:00:00-5:00', '2016-08-19T09:00:00-5:00'),
        CalendarEvent('2016-08-19T20:00:00-5:00', '2016-08-19T22:00:00-5:00')
      ]
    }

    TODO: Put more thought into algorithm as it is overly complicated
          but functional currently.

    :param cal_schedule: The events on calendar stored by day.
    :type cal_schedule: dict of events.CalendarEvent objects
    :return: Free time for each day in cal_schedule
    :rtype: dict
    """
    sorted_times = defaultdict(list)
    for date, cal_events in cal_schedule.items():
        for e in cal_events:
            sorted_times[date].extend([
                ('start', e.start_time), ('end', e.end_time)])

    counter = 0
    free = defaultdict(list)
    for date, times in sorted(sorted_times.items(), key=lambda x: x[1]):
        for time in times:
            if time[0] == 'start':
                if counter == 0:
                    free[date].append(('end', time[1]))
                counter += 1

            elif time[0] == 'end':
                if counter == 1:
                    free[date].append(('start', time[1]))
                counter -= 1

    free_events = defaultdict(list)
    for d, end in free.items():
        end.insert(
            0, ('start', datetime(int(d[0:4]), int(d[5:7]), int(d[-2:]))))
        end.append((
            'end', datetime(int(d[0:4]), int(d[5:7]), int(d[-2:]), 23, 59, 59)))
        for i, k in zip(end[0::2], end[1::2]):
            free_events[d].append(events.CalendarEvent({
                'startTime': i[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'endTime': k[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'summary': None}))

    return free_events


def event_group(start_date, end_date):
    """
    Groups events from user's calendars by day.

    :param start_date:
    :type start_date: str in UTC ISO format
    :param end_date:
    :type end_date: str in UTC ISO format
    :return: All events on calendar for each day between dates (inclusive)
    :rtype: dict of events.CalendarEvent objects
    """
    all_events = []
    for cal in events.calendars():
        c_events = events.get_events(cal, start_date, end_date)
        all_events.extend([events.CalendarEvent(e) for e in c_events if e.get(
                'startTime') is not None])

    day_schedule = defaultdict(list)
    for cal_e in sorted(all_events, key=lambda x: x.day):
        day_schedule[cal_e.day].append(cal_e)

    return day_schedule


if __name__ == '__main__':
    print free_time(event_group(
        '2016-09-17T12:00:00Z', '2016-10-26T00:00:00Z'))
