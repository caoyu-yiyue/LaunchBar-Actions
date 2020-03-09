#!/usr/bin/env python
#
# LaunchBar Action Script
#

import subprocess as sp
import os

# input your Airpods' MAC address here
your_MAC_address = 'your_mac_address'

os.environ['PATH'] += os.pathsep + '/usr/local/bin/'
# print(os.environ['PATH'])

command = ['BluetoothConnector', '-c', your_MAC_address, '--notify']
output = sp.check_output(command)
output = output.decode('utf-8').strip()
print(output)
