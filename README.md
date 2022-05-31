# backupcleaner

## clean-backups.py

Tool to cleanup backup directory with daily, weekly and monthly backups.
This tool removes **everything** in the specified directory (not recursively) except files, containing timestamps in the filename that can identified by this tool as fresh backups.

By default, this tool keeps last 7 daily backups, 4 weekly backups (4 last monday backups) and 3 monthly backups (1st day of last 3 months). You can redefine this by command line parameters.

This tool expects timestamps like this: 20220531 (May 31, 2022), but of course, you can redefine this.

```text
usage: clean-backups.py [-h] [-d N] [-w N] [-m N] [-f] PATH

Cleanup old backups

positional arguments:
  PATH               directory path

optional arguments:
  -h, --help         show this help message and exit
  -d N, --daily N    keep N daily backups, default: 7
  -w N, --weekly N   keep N weekly backups, default: 4
  -m N, --monthly N  keep N monthly backups, default: 3
  -f, --force        suppress remove confirmation
  -t FORMAT, --timestamp-format FORMAT
                     format of timestamp, default: %Y%m%d
```

For a complete timestamp format description, see the python strftime() documentation: <https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior>
