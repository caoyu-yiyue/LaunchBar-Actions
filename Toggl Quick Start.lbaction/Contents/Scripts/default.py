#!/usr/local/opt/python@3.11/libexec/bin/python
#
# LaunchBar Action Script for Start an Untitled Toggl Time Entry.
#

import os
from base64 import b64encode
from datetime import datetime, timezone

import requests

TOKEN = '<Your API Token>'
WORKSPACE_ID = '<Your Workspace ID>'

API = (f'https://api.track.toggl.com/api/v9/workspaces/{WORKSPACE_ID}/'
       'time_entries')
HEADERS = {
    'content-type':
    'application/json',
    'Authorization':
    'Basic %s' % b64encode(f"{TOKEN}:api_token".encode()).decode("ascii")
}


# Function for system notification.
def sys_notification(title: str, message: str) -> None:
    os.system("""
    osascript -e 'display notification "{}" with title "{}"'
    """.format(title, message))


local_now = datetime.now().astimezone()
utc_now = local_now.astimezone(tz=timezone.utc)
post_data = {
    'billable': False,
    'created_with': 'LaunchBar Action',
    'description': '',
    'project_id': None,
    'task_id': None,
    'tags_id': None,
    'workspace_id': WORKSPACE_ID,
    'start': utc_now.strftime('%Y-%m-%dT%H:%M:%SZ'),
    "duration": int('-' + local_now.strftime('%s')),
    'stop': None
}

response = requests.post(API, json=post_data, headers=HEADERS)

if response.status_code == 200:
    notifi_title = 'Start A new Toggl Entry!'
    notifi_content = '✅Quickly started an untitled Toggl time entry.'
else:
    notifi_title = 'Failed to Start Toggl Entry'
    notifi_content = 'Some error occured.'

sys_notification(notifi_title, notifi_content)
