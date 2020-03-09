#!/bin/sh
#
# LaunchBar Action Script
#

system_profiler SPPowerDataType | grep "Cycle Count" | awk '{print $3}'
