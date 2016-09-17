from __future__ import unicode_literals

import requests

from . import authorization

CALENDAR_API_URL = 'https://www.googleapis.com/calendar/v3'


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


def create_event(calendar_id, event, auth=None):
    """
    Create an event on the specified calendar.

    :param calendar_id: Id of the calendar to create event on.
    :type calendar_id: str
    :param event: Information about the event to create.
    :type event: dict
    :param auth: Authentication header for the calendar. Defaults to None.
        Will authenticate user if None.
    :type auth: dict
    :return: Response from event POST.
    :rtype: requests.Response
    """
    raise NotImplementedError()
