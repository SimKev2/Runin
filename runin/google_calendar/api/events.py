from __future__ import unicode_literals
import json

import requests
from dateutil import parser

import authorization

CALENDAR_API_URL = 'https://www.googleapis.com/calendar/v3'


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
        """The day the event is on i.e. 2016-09-19"""
        return str(self.start_time.date())

    @property
    def duration(self):
        """The length of the CalendarEvent"""
        return self.end_time - self.start_time


def calendars():
    """
    Authorize a user and retrieve all ids of calendars they own.

    :return: All calendar ids of a user.
    :rtype: list of str
    """
    auth = authorization.auth_headers()
    calendars = requests.get(
        CALENDAR_API_URL + '/users/me/calendarList',
        headers=auth).json()

    calendar_ids = []
    for c in calendars.get('items'):
        calendar_ids.append(c.get('id'))

    return calendar_ids


def get_events(calendar_id, start_time, end_time, auth=None):
    """
    Retrieve all events from calendar_id between specified dates.

    Example event format:
      {
        "summary": "Eat lunch with Kevin"
        "startTime": "2016-09-19T12:00:00Z"
        "endTime":  "2016-09-19T13:00:00Z"
      }

    :param calendar_id: Id of the calendar to get events from.
    :type calendar_id: str
    :param start_time: Lower bound for event end time.
    :type start_time: str in UTC ISO format. i.e. '2016-09-20T13:00:00Z'
        datetime.utcnow().isoformat() + 'Z'
    :param end_time: Upper bound for event start time.
    :type end_time: str in UTC ISO format. i.e. '2016-09-20T14:00:00Z'
    :param auth: Authentication header for the calendar. Defaults to None.
        Will authenticate user if None.
    :type auth: dict
    :return: Events in json format.
    :rtype: list of dict
    """
    if not auth:
        auth = authorization.auth_headers()

    try:
        resp = requests.get(
            CALENDAR_API_URL + '/calendars/{}/events'
            '?timeMin={}&timeMax={}&singleEvents=true'.format(
                calendar_id, start_time, end_time),
            headers=auth)

        if resp.status_code != 200:
            print 'Error retrieving event from calendar ' + calendar_id
            print resp.content
            return []

        events = []
        for i in resp.json().get('items', []):
            events.append({
                'summary': i.get('summary'),
                'startTime': i.get('start').get('dateTime'),
                'endTime': i.get('end').get('dateTime')})

        return events

    except Exception as e:
        print e.message


def create_event(event, auth=None):
    """
    Create an event on the primary calendar.

    :param event: Information about the event to create.
    :type event: processing.CalendarEvent
    :param auth: Authentication header for the calendar. Defaults to None.
        Will authenticate user if None.
    :type auth: dict
    :return: Response from event POST.
    :rtype: requests.Response
    """
    if not auth:
        auth = authorization.auth_headers()

    g_event = {
        'end': {
            'dateTime': event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Chicago'},
        'start': {
            'dateTime': event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Chicago'},
        'summary': event.summary}

    headers = {'Content-Type': 'application/json'}
    headers.update(auth)
    resp = requests.post(
        CALENDAR_API_URL + '/calendars/primary/events',
        data=json.dumps(g_event),
        headers=headers)

    return resp

if __name__ == '__main__':
    create_event(CalendarEvent({
        'startTime': '2016-09-17T19:00:00-5:00',
        'endTime': '2016-09-17T20:00:00-5:00',
        'summary': 'Run 2 Miles'}))
