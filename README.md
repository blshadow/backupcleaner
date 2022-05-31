# backupcleaner

Tool to cleanup backup directory with daily, weekly and monthly backups.

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
