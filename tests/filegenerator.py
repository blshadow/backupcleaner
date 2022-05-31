#!/usr/bin/env python3
"""
Generate files for tests.
"""
import argparse
from datetime import date, timedelta
from pathlib import Path
import os

DEFAULT_NUMBER_OF_FILES = 200
DEFAULT_PREFIX = "testfile-"
DEFAULT_SUFFIX = ".bak"

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
# number of files
parser.add_argument(
    "-n", "--number-of-files",
    type = int,
    default = DEFAULT_NUMBER_OF_FILES,
    metavar = "N",
    help = f"generate N files, default: {DEFAULT_NUMBER_OF_FILES}"
)
# prefix argument
parser.add_argument(
    "-p", "--prefix",
    type = str,
    default = DEFAULT_PREFIX,
    metavar = "PREFIX",
    help = f"use PREFIX as file name prefix, default: {DEFAULT_PREFIX}"
)
# suffix argument
parser.add_argument(
    "-s", "--suffix",
    type = str,
    default = DEFAULT_SUFFIX,
    metavar = "SUFFIX",
    help = f"use SUFFIX as file name suffix, default: {DEFAULT_SUFFIX}"
)
args = parser.parse_args()
path = args.path[0]
number_of_files = args.number_of_files
prefix = args.prefix
suffix = args.suffix

for i in range(number_of_files):
    timestamp = (date.today() - timedelta(days=i)).strftime("%Y%m%d")
    filename = f"{prefix}{timestamp}{suffix}"
    Path(os.path.join(path, filename)).touch()
    