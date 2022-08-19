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
DEFAULT_DAY_OF_WEEK = 0
DEFAULT_DAY_OF_MONTH = 1


class BackupFile:
    """
    Manipulations with backup files

    Arguments:
        * retention_daily           - daily retention period
        * retention_weekly          - weekly retention period
        * retention_monthly         - monthly retention period
        * retention_day_of_week     - day of week for weekly backups
        * retention_day_of_month    - day of month for monthly backups
        * file_path (optional)      - file path
        * dateformat (optional)     - format of timestamps (default is '%Y%m%d')
    """
    def __init__(
        self,
        retention_daily,
        retention_weekly,
        retention_monthly,
        retention_day_of_week=0,
        retention_day_of_month=1,
        file_path=None,
        dateformat="%Y%m%d"
    ) -> None:
        self.file_path = file_path
        self.daily = retention_daily
        self.weekly = retention_weekly
        self.monthly = retention_monthly
        self.day_of_week = retention_day_of_week
        self.day_of_month = retention_day_of_month
        self.dateformat = dateformat
        curr_date = date.today()  # Maybe this will be used to specify date as starting point...
        if self.file_path is None:
            self.file_name = None
        else:
            self.file_name = os.path.basename(self.file_path)
        dates = []
        # Daily
        for i in range(0, self.daily):
            day = curr_date - timedelta(days=i)
            dates.append(day)
        # Weekly
        weekly_day = curr_date - timedelta(days=date.weekday(curr_date)) + timedelta(days=self.day_of_week)
        if weekly_day > curr_date:
            weekly_day = weekly_day - timedelta(days=7)
        for i in range(0, self.weekly):
            day = weekly_day - timedelta(days=(i*7))
            if day not in dates:
                dates.append(day)
        # Monthly
        day = curr_date.replace(day=self.day_of_month)
        if day > curr_date:
            day = (day.replace(day=1) - timedelta(days=1)).replace(day=self.day_of_month)
        for i in range(0, self.monthly):
            if day not in dates:
                dates.append(day)
            day = (day.replace(day=1) - timedelta(days=1)).replace(day=self.day_of_month)
        self.dates = dates

    def new_file(
        self,
        file_path,
        retention_daily=None,
        retention_weekly=None,
        retention_monthly=None,
        retention_day_of_week=None,
        retention_day_of_month=None,
        dateformat=None
    ):
        """
        Create new instance of BackupFile, can be used for retention settings inheritance.
        """
        if retention_daily is None:
            retention_daily = self.daily
        if retention_weekly is None:
            retention_weekly = self.weekly
        if retention_monthly is None:
            retention_monthly = self.monthly
        if retention_day_of_week is None:
            retention_day_of_week = self.day_of_week
        if retention_day_of_month is None:
            retention_day_of_month = self.day_of_month
        if dateformat is None:
            dateformat = self.dateformat
        new_file = BackupFile(
            retention_daily,
            retention_weekly,
            retention_monthly,
            retention_day_of_week,
            retention_day_of_month,
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

    def remove(self, force_remove=False):
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

    def remove_if_needed(self, force_remove=False):
        """
        Remove file if it's too old.
        """
        if self.need_remove():
            self.remove(force_remove=force_remove)


# Argument parser
parser = argparse.ArgumentParser(
    description="Cleanup old backups",
    epilog="For a complete timestamp format description, see the python strftime() " +
           "documentation: https://docs.python.org/3/library/datetime.html" +
           "#strftime-strptime-behavior"
)
# path argument
parser.add_argument(
    "path",
    metavar="PATH",
    type=str,
    nargs=1,
    help="directory path"
)
# daily argument
parser.add_argument(
    "-d", "--daily",
    type=int,
    default=DEFAULT_DAILY,
    metavar="N",
    help=f"keep N daily backups, default: {DEFAULT_DAILY}"
)
# weekly argument
parser.add_argument(
    "-w", "--weekly",
    type=int,
    default=DEFAULT_WEEKLY,
    metavar="N",
    help=f"keep N weekly backups, default: {DEFAULT_WEEKLY}"
)
# monthly argument
parser.add_argument(
    "-m", "--monthly",
    type=int,
    default=DEFAULT_MONTHLY,
    metavar="N",
    help=f"keep N monthly backups, default: {DEFAULT_MONTHLY}"
)
# day of week for weekly backups
parser.add_argument(
    "--day-of-week",
    type=int,
    default=DEFAULT_DAY_OF_WEEK,
    metavar="N",
    help=f"day of week for weekly backups, 0 for monday, 6 for sunday, default: {DEFAULT_DAY_OF_WEEK}"
)
# day of month for monthly backups
parser.add_argument(
    "--day-of-month",
    type=int,
    default=DEFAULT_DAY_OF_MONTH,
    metavar="N",
    help=f"day of month for monthly backups, dafault: {DEFAULT_DAY_OF_MONTH}"
)
# force removal
parser.add_argument(
    "-f", "--force",
    action="store_true",
    help="suppress remove confirmation"
)
# force removal
parser.add_argument(
    "-r", "--recursive",
    action="store_true",
    help="remove files recursively"
)
# timestamp format
parser.add_argument(
    "-t",
    "--timestamp-format",
    type=str,
    default=DEFAULT_TIMESTAMP_FORMAT,
    metavar="FORMAT",
    help=f"format of timestamp, default: {DEFAULT_TIMESTAMP_FORMAT}".replace(r"%", r"%%")
)
args = parser.parse_args()

daily = args.daily
weekly = args.weekly
monthly = args.monthly
day_of_week = args.day_of_week
day_of_month = args.day_of_month
recursive = args.recursive
force = args.force
directory = args.path[0]
timestamp_format = args.timestamp_format

#
# File processing
#

# Create BackupFile object with retention settings
files = BackupFile(
    retention_daily=daily,
    retention_weekly=weekly,
    retention_monthly=monthly,
    retention_day_of_week=day_of_week,
    retention_day_of_month=day_of_month,
    dateformat=timestamp_format
)
# Walk through subdirectory tree
for root, dirs, filenames in os.walk(directory):
    for filename in filenames:
        f = files.new_file(os.path.join(root, filename))
        f.remove_if_needed(force_remove=force)
    if not recursive:
        break
