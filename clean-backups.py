#!/usr/bin/env python3
"""Backup rotation script"""
from datetime import date, timedelta
import os
import argparse

# Default retention parameters
DEFAULT_DAILY = 7
DEFAULT_WEEKLY = 4
DEFAULT_MONTHLY = 3
DEFAULT_TIMESTAMP_FORMAT = "%Y%m%d"

class BackupFile():
    """
    Manipulations with backup files

    Arguments:
        * retention_daily       - daily renention period
        * retention_weekly      - weekly retention period
        * retention_monthly     - monthly retention perod
        * file_path (optional)  - file path
        * dateformat (optional) - format of timestamps (default is '%Y%m%d')
    """
    def __init__(
        self,
        retention_daily,
        retention_weekly,
        retention_monthly,
        file_path = None,
        dateformat = "%Y%m%d") -> None:

        self.file_path = file_path
        self.daily = retention_daily
        self.weekly = retention_weekly
        self.monthly = retention_monthly
        self.dateformat = dateformat
        curr_date = date.today() # Maybe this will be used to specify date as starting point...
        if self.file_path is None:
            self.file_name = None
        else:
            self.file_name = os.path.basename(self.file_path)
        dates = []
        # Daily
        for i in range(0, self.daily):
            day = curr_date - timedelta(days = i)
            dates.append(day)
        # Weekly
        monday = curr_date - timedelta(days=date.weekday(curr_date))
        for i in range(0,self.weekly):
            day = monday - timedelta( days = (i * 7))
            if day not in dates:
                dates.append(day)
        # Monthly
        day = curr_date.replace(day=1)
        for i in range(0,self.monthly):
            if day not in dates:
                dates.append(day)
            day = (day - timedelta(days=1)).replace(day=1)
        self.dates = dates

    def new_file(
        self,
        file_path,
        retention_daily = None,
        retention_weekly = None,
        retention_monthly = None,
        dateformat = None):
        """
        Create new instance of BackupFile, can be used for retention settings inheritance.
        """

        if retention_daily is None:
            retention_daily = self.daily
        if retention_weekly is None:
            retention_weekly = self.weekly
        if retention_monthly is None:
            retention_monthly = self.monthly
        if dateformat is None:
            dateformat = self.dateformat
        new_file = BackupFile(
            retention_daily,
            retention_weekly,
            retention_monthly,
            file_path,
            dateformat
        )
        return new_file

    def __str__(self):
        val = f"<{self.file_path}>"
        return val

    def need_remove(self):
        """
        Check if file is too old and needs to remove.
        """
        if self.file_name is None:
            need_remove = False
        else:
            need_remove = True
            for single_date in self.dates:
                if single_date.strftime(self.dateformat) in self.file_name:
                    need_remove = False
                    break
        return need_remove

    def remove(self, force_remove = False):
        """
        Remove file

        Arguments:
            * force_remove  - suppress remove confirmation
        """
        print(f"Removing {self}...")
        # Check force option
        if force_remove:
            os.unlink(self.file_path)
        else:
            # Remove interactively
            print("Are you sure? (y/n) ", end="")
            answer = input()
            if answer == "y":
                os.unlink(self.file_path)

    def remove_if_needed(self, force_remove = False):
        """
        Remove file if it's too old.
        """
        if self.need_remove():
            self.remove(force_remove = force_remove)

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
    default = DEFAULT_DAILY,
    metavar = "N",
    help = f"keep N daily backups, default: {DEFAULT_DAILY}"
)
# weekly argument
parser.add_argument(
    "-w", "--weekly",
    type = int,
    default = DEFAULT_WEEKLY,
    metavar = "N",
    help = f"keep N weekly backups, default: {DEFAULT_WEEKLY}"
)
# monthly argument
parser.add_argument(
    "-m", "--monthly",
    type = int,
    default = DEFAULT_MONTHLY,
    metavar = "N",
    help = f"keep N monthly backups, default: {DEFAULT_MONTHLY}"
)
# force removal
parser.add_argument(
    "-f", "--force",
    action="store_true",
    help = "suppress remove confirmation"
)
# timestamp format
parser.add_argument(
    "-t",
    "--timestamp-format",
    type = str,
    default = DEFAULT_TIMESTAMP_FORMAT,
    metavar = "FORMAT",
    help = f"format of timestamp, default: {DEFAULT_TIMESTAMP_FORMAT}".replace(r"%",r"%%")
)
args = parser.parse_args()

daily = args.daily
weekly = args.weekly
monthly = args.monthly
force = args.force
directory = args.path[0]
timestamp_format = args.timestamp_format

# File processing
files = BackupFile(
    retention_daily = daily,
    retention_weekly = weekly,
    retention_monthly = monthly,
    dateformat = timestamp_format
)
# Generate file list with full paths
paths = [
    os.path.join(directory, f) for f in os.listdir(directory)
    if os.path.isfile(os.path.join(directory, f))
]
for path in paths:
    f = files.new_file(path)
    f.remove_if_needed(force_remove = force)
