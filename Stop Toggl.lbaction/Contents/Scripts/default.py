#!/usr/bin/env python
#
# LaunchBar Action Script for Stoping Running Toggl Entry.
#

# %%
from base64 import b64encode
from datetime import timedelta
from urllib.error import URLError

import requests

# %%
# Fill your API token
TOKEN = '<Your API Token>'

HEADERS = {
    'content-type':
    'application/json',
    'Authorization':
    'Basic %s' % b64encode(f"{TOKEN}:api_token".encode()).decode("ascii")
}

# %%
# Get current running entry.
try:
    current_resp = requests.get(
        'https://api.track.toggl.com/api/v9/me/time_entries/current',
        headers=HEADERS)
    current_entry = current_resp.json()

    # if there's entry running, the stop it.
    if current_entry is not None:
        workspace_id = current_entry['workspace_id']
        time_entry_id = current_entry['id']

        stopped_resp = requests.patch(
            (f'https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/'
             f'time_entries/{time_entry_id}/stop'),
            headers=HEADERS)
        stopped_entry = stopped_resp.json()

        duration_str = str(timedelta(0, stopped_entry['duration']))
        desc = stopped_entry['description']

        print(f'Stopped {desc}, Have Run {duration_str}.')
    # If no running entry, return.
    else:
        print('No Time Entry Runnig Now.')

except URLError:
    print("Internet Error: Can't connent internet.")
