#!/bin/sh
#
# LaunchBar Action Script to Get Battery Percentage
#
pmset -g batt | grep -o "[0-9]\{1,3\}%"
