#!/usr/bin/env python3
"""Sort simple timeline rows by timestamp.

Accepts lines containing an ISO-like timestamp or Unix epoch. Prints unknown
timestamp lines after known timestamp lines.
"""

import argparse
import datetime as dt
import re
import sys


def parse_ts(line):
    epoch = re.search(r"\b(1[0-9]{9}(?:\.[0-9]+)?)\b", line)
    if epoch:
        return float(epoch.group(1))
    iso = re.search(r"\b(20[0-9]{2}-[0-9]{2}-[0-9]{2}[ T][0-9:.+-]+)", line)
    if iso:
        s = iso.group(1).replace("Z", "+00:00")
        try:
            return dt.datetime.fromisoformat(s).timestamp()
        except ValueError:
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", default="-")
    args = ap.parse_args()
    lines = sys.stdin.readlines() if args.file == "-" else open(args.file, errors="replace").readlines()
    keyed = [(parse_ts(line), i, line.rstrip("\n")) for i, line in enumerate(lines)]
    keyed.sort(key=lambda x: (x[0] is None, x[0] or 0, x[1]))
    for ts, _, line in keyed:
        print(line)


if __name__ == "__main__":
    main()

