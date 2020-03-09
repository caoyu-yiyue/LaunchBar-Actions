#!/usr/bin/env python
#
# LaunchBar Action Script
#
import json
import sh
import re

try:
    result = str(
        sh.egrep(sh.ioreg('-r', '-l', '-n', 'AppleHSBluetoothDevice'),
                 r'"BatteryPercent" = |^  \|   "Bluetooth Product Name" = '))
except sh.ErrorReturnCode:
    print('None Bluetooth Connecting.')
    quit()

names = [
    match.group(1) for match in re.finditer(r'Product Name" = "(.+?)"', result)
]
BatteryPercent_nums = [
    match.group(1) for match in re.finditer(r'Percent" = (\d+)', result)
]

name_percent_pairs = [
    name + " : " + bp + "%" for name in names for bp in BatteryPercent_nums
]

items = []
for pair in name_percent_pairs:
    item = {}
    item['title'] = pair
    items.append(item)

print(json.dumps(items))
