from __future__ import unicode_literals
import json
import os
from datetime import datetime

from oauth2client import client, tools, file


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def auth_headers():
    """
    Gets valid user credentials from storage.

    :return: Header for requests authorized request
    :rtype: dict
    """
    credential_dir = os.path.join(os.path.expanduser('~'), '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(
        credential_dir, 'calendar-python-quickstart.json')

    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        tools.run_flow(flow, store, None)
        print 'Storing credentials to ' + credential_path

    with open(credential_path, 'r') as f:
        auth = json.loads(f.read())

    utc = datetime.strptime(auth.get('token_expiry'), '%Y-%m-%dT%H:%M:%SZ')
    if utc < datetime.utcnow():
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        tools.run_flow(flow, store, None)

    with open(credential_path, 'r') as f:
        auth = json.loads(f.read())

    return {
        'Authorization': 'Bearer ' + auth['token_response']['access_token']}