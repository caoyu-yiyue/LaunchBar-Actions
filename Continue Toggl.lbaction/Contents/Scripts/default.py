#!/usr/local/opt/python@3.10/libexec/bin/python
#
# LaunchBar Action Script For Continue Toggl Track Last Entry.
#

# %%
import os
from base64 import b64encode
from datetime import datetime, timezone
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
# Get time entries' list.

resp = requests.get('https://api.track.toggl.com/api/v9/me/time_entries',
                    headers=HEADERS)
my_entries = resp.json()

# %%
# Get the last but not breaking entry.
for entry in my_entries:
    desc = entry['description']
    if desc != 'Pomodoro Break':
        last_entry = entry
        break
    else:
        continue

# %%
last_desc = last_entry['description']
workspace_id = last_entry['workspace_id']

# Check if the last entry is running.
if last_entry['duration'] < 0:
    notifi_title = 'Having Running'
    notifi_content = '⚠Now Have Running Task: ' + \
        last_desc if not None else 'No description.'

else:
    # Continue the last entry.
    local_now = datetime.now().astimezone()
    utc_now = local_now.astimezone(tz=timezone.utc)
    post_data = {
        'billable': False,
        'created_with': 'LaunchBar Action',
        'description': last_desc,
        'project_id': last_entry['project_id'],
        'task_id': last_entry['task_id'],
        'tags_id': last_entry['tag_ids'],
        'workspace_id': workspace_id,
        'start': utc_now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "duration": int('-' + local_now.strftime('%s')),
        'stop': None
    }

    try:
        started_resp = requests.post(
            ('https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/'
             'time_entries').format(workspace_id=workspace_id),
            json=post_data,
            headers=HEADERS)
        started_entry = started_resp.json()

        started_desc = started_entry['description']
        notifi_title = 'Continue Toggl Success!'
        notifi_content = '✅Continue Last Entry: ' +\
            started_desc if not None else 'No Description'

    except URLError:
        notifi_title = 'Continue Toggl Failed'
        notifi_content = 'Failed to connect Internet.'

# %%
os.system("""
osascript -e 'display notification "{}" with title "{}"'
""".format(notifi_title, notifi_content))
