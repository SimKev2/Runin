from __future__ import unicode_literals

from runin.google_calendar.api import events


def main():
    ids = events.calendars()
    c_events = []
    for i in ids:
        c_events.append(
            events.get_events(i, '2016-09-17T12:00:00Z', '2016-09-20T00:00:00Z'))

    print c_events

if __name__ == '__main__':
    main()
