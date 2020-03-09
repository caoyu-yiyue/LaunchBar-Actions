#!/usr/bin/env python
#
# LaunchBar Action Script
#
import subprocess as sp
import re

my_command = ["pmset", "-g", "batt"]
content = sp.check_output(my_command).decode('utf-8')
batteryPercent = re.search(r'\d{1,3}\%', content).group(0)
print(batteryPercent)
