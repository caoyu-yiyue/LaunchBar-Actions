#!/usr/bin/env python
#
# LaunchBar Action Script
#
from toggl.TogglPy import Toggl
from requests import HTTPError
# import os

# %%
toggl = Toggl()
# fill your own E-Mail and Password.
toggl.setAuthCredentials('<EMAIL>', '<PASSWORD>')

# %%
my_entries = toggl.request('https://www.toggl.com/api/v8/time_entries')


def find_last_not_break(history_time_entries: list):
    last_entry = history_time_entries[-1]
    if last_entry['description'] != 'Pomodoro Break':
        return last_entry
    else:
        return find_last_not_break(history_time_entries[:-1])


last_entry: dict = find_last_not_break(my_entries)

# %%
# chech if now have tasks running.
if last_entry['duration'] < 0:
    # notifi_title = 'Having Running'
    notifi_content = '⚠Now Having Running Task: ' + last_entry['description']
else:
    try:
        pid = last_entry.get('pid', None)
        tid = last_entry.get('tid', None)
        started_entry = toggl.startTimeEntry(
            description=last_entry['description'], pid=pid, tid=tid)
        # notifi_title = 'Continue Toggl Success!'
        notifi_content = '✅Continue Last Entry: ' + started_entry['data'][
            'description']
    except HTTPError as e:
        # notifi_title = 'Continue Toggl Failed'
        notifi_content = '❌' + e.message

print(notifi_content)

# os.system("""
# osascript -e 'display notification "{}" with title "{}"'
# """.format(notifi_title, notifi_content))
