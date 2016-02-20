#!/usr/bin/env bash

# If you want to start `systray.py` upon boot,
# then call this launcher script.
# If you call `systray.py` upon boot, it'll
# be called too early and very likely you'll
# get an error that the system tray is missing.

sleep 30    # giving some time for the system tray to come up

HERE=`dirname $0`
cd $HERE
./systray.py
