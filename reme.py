#!/usr/local/bin/python3
# Make a new reminder via terminal script for next Friday
# args: <reminder>
# some part used from https://gist.github.com/renfredxh/7836327

import subprocess
import sys
from datetime import datetime # timedelta

# A apple script that creates a new reminder given a name

OSASCRIPT = ('<<END\n'
'on nextWeekday(wd)\n'
'	set today to current date\n'
'	set twd to weekday of today\n'
'	if twd is wd then\n'
'		set d to 7\n'
'	else\n'
'		set d to (7 + (wd - twd)) mod 7\n'
'	end if\n'
'	return today + (d * days)\n'
'end nextWeekday\n'
'on run argv\n'
'	set nextFriday to nextWeekday(Friday)\n'
'	tell application "Reminders"\n'
'		set newLable to argv as string\n'
'		set myList to list "Do."\n'
'		tell myList\n'
'			set newReminder to make new reminder\n'
'			set name of newReminder to newLable\n'
'			set allday due date of newReminder to nextFriday\n'
'		end tell\n'
'	end tell\n'
'end run\n'
'END')

#to find the next friday is python no apple script to increase execusion speed
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead) #4 is Friday


def reminder(name):
    # Execute applescript via shell to create a new reminder.
    command = 'osascript - "{n}" {osa}'.format(n=name, osa=OSASCRIPT)
    with open('/dev/null', 'w') as devnull:
        status = subprocess.call(command, shell=True, stdout=devnull)
    return status

def main():
    name = sys.argv[1]

    status = reminder(name)

    if status == 0:
        print("New Reminder:\n", name)
    else:
        print("Error occured")

if __name__ == "__main__":
    main()
