#!/usr/bin/env python3
from calendar import week
from datetime import date, timedelta
import os
import argparse

# Default retention parameters
default_daily = 7
default_weekly = 4
default_monthly = 3

class backupFile():
    def __init__(self, daily, weekly, monthly, path = None, dateformat = "%Y%m%d") -> None:
        self.path = path
        self.daily = daily
        self.weekly = weekly
        self.monthly = monthly
        self.dateformat = dateformat
        curr_date = date.today() # Maybe this will be used to specify date as starting point...
        if self.path == None:
            self.filename = None
        else:
            self.filename = os.path.basename(path)
        dates = []

        # Daily
        for i in range(0, daily):
            day = curr_date - timedelta(days = i)
            dates.append(day)
        # Weekly
        monday = curr_date - timedelta(days=date.weekday(curr_date))
        for i in range(0,weekly):
            day = monday - timedelta( days = (i * 7))
            if day not in dates:
                dates.append(day)
        # Monthly
        day = curr_date.replace(day=1)
        for i in range(0,monthly):
            if day not in dates:
                dates.append(day)
            day = (day - timedelta(days=1)).replace(day=1)
        self.dates = dates

    def newFile(self, path, daily = None, weekly = None, monthly = None, dateformat = None):
        if daily == None: daily = self.daily
        if weekly == None: weekly = self.weekly
        if monthly == None: monthly = self.monthly
        if dateformat == None: dateformat = self.dateformat
        newfile = backupFile(daily, weekly, monthly, path)
        return(newfile)

    def __str__(self):
        val = "<{path}>".format(
            path = self.path,
        )
        return(val)

    def needRemove(self):
        if self.filename == None:
            need_remove = False
        else:
            need_remove = True
            for date in self.dates:
                if date.strftime(self.dateformat) in self.filename:
                    need_remove = False
                    break
        return(need_remove)
    
    def remove(self, force = False):
        print("Removing {file}...".format(file = self))
        # Check force option
        if force:
            os.unlink(self.path)
        else:
            # Remove interactively
            print("Are you sure? (y/n) ", end="")
            answer = input()
            if answer == "y":
                os.unlink(self.path)
    
    def removeIfNeeded(self, force = False):
        if self.needRemove():
            self.remove(force = force)

# Argument parser
parser = argparse.ArgumentParser(description="Cleanup old backups")
# path argument
parser.add_argument(
    "path",
    metavar = "PATH",
    type = str,
    nargs = 1,
    help = "directory path"
)
# daily argument
parser.add_argument(
    "-d", "--daily",
    type = int,
    default = default_daily,
    metavar = "N",
    help = "keep N daily backups, default: {default_daily}".format(
        default_daily = default_daily
    )
)
# weekly argument
parser.add_argument(
    "-w", "--weekly",
    type = int,
    default = default_weekly,
    metavar = "N",
    help = "keep N weekly backups, default: {default_weekly}".format(
        default_weekly = default_weekly
    )
)
# monthly argument
parser.add_argument(
    "-m", "--monthly",
    type = int,
    default = default_monthly,
    metavar = "N",
    help = "keep N monthly backups, default: {default_monthly}".format(
        default_monthly = default_monthly
    )
)
# force removal
parser.add_argument(
    "-f", "--force",
    action="store_true",
    help = "suppress remove confirmation"
)
args = parser.parse_args()

daily = args.daily
weekly = args.weekly
monthly = args.monthly
force = args.force
directory = args.path[0]

# File processing
files = backupFile(daily = daily, weekly = weekly, monthly = monthly)
# Generate file list with full paths
paths = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
for path in paths:
    f = files.newFile(path)
    f.removeIfNeeded(force = force)