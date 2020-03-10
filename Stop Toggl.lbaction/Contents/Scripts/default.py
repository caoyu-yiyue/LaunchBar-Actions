#!/usr/bin/env python
#
# LaunchBar Action Script
#
from toggl.TogglPy import Toggl
from requests import HTTPError
import datetime

# %%
toggl = Toggl()
# fill your own E-Mail and Password.
toggl.setAuthCredentials('<EMAIL>', '<PASSWORD>')

# %%
try:
    currentTimer = toggl.currentRunningTimeEntry()
    if currentTimer['data'] is None:
        print('No Time Entry Runnig Now.')
    else:
        stoppedEntry = toggl.stopTimeEntry(currentTimer['data']['id'])['data']
        duration_str = str(datetime.timedelta(0, stoppedEntry['duration']))
        print('Stopped: {}, Have Run {}.'.format(stoppedEntry['description'],
                                                 duration_str))
except HTTPError as e:
    print(e)
