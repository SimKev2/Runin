from __future__ import unicode_literals

import json
from collections import defaultdict
from datetime import datetime, timedelta
from os import path

from google_calendar.api import events


def event_group(start_date, end_date):
    """
    Groups events from user's calendars by day.

    :param start_date:
    :type start_date: str in "Year-Month-Day" format
    :param end_date:
    :type end_date: str in "Year-Month-Day" format
    :return: All events on calendar for each day between dates (inclusive)
    :rtype: dict of events.CalendarEvent objects
    """
    start_date += 'T00:00:00Z'
    end_date += 'T23:59:59Z'

    all_events = []
    for cal in events.calendars():
        c_events = events.get_events(cal, start_date, end_date)
        all_events.extend([events.CalendarEvent(e) for e in c_events if e.get(
                'startTime') is not None])

    day_schedule = defaultdict(list)
    for cal_e in sorted(all_events, key=lambda x: x.day):
        day_schedule[cal_e.day].append(cal_e)

    return day_schedule


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
    times_dict = defaultdict(list)
    for date, cal_events in cal_schedule.items():
        for e in cal_events:
            times_dict[date].extend([
                ('start', e.start_time), ('end', e.end_time)])

    counter = 0
    free = defaultdict(list)
    for date, times in times_dict.items():
        for time in sorted(
                times, key=lambda x: x[1].strftime("%Y-%m-%dT%H:%M:%S")):

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
            0, ('start', datetime(int(d[0:4]), int(d[5:7]), int(d[-2:]), 7, 50)))
        end.append((
            'end', datetime(int(d[0:4]), int(d[5:7]), int(d[-2:]), 22)))
        for i, k in zip(end[0::2], end[1::2]):
            free_events[d].append(events.CalendarEvent({
                'startTime': i[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'endTime': k[1].strftime("%Y-%m-%dT%H:%M:%S"),
                'summary': None}))

    return free_events


def main(training_file):
    with open(training_file, 'r') as f:
        contents = json.loads(f.read())

    free_spots = free_time(event_group(
        contents.get('startDate'), contents.get('endDate')))

    running_schedule = []
    running_events = contents.get('events')
    for r_e in running_events:
        for f in free_spots.get(r_e.get('date')):
            run_duration = timedelta(seconds=(r_e.get('distance') * 660))
            if f.duration >= run_duration:
                running_schedule.append(events.CalendarEvent({
                    'startTime': f.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'endTime': (f.start_time + run_duration).strftime(
                        "%Y-%m-%dT%H:%M:%S"),
                    'summary': r_e.get('name')}))
                break

    for r in running_schedule:
        print r.summary
        print r.start_time
        print r.end_time
        print
        events.create_event(r)


if __name__ == '__main__':
    main(path.join(path.dirname(path.realpath(__file__)), 'plan.json'))
