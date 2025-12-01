#!/usr/bin/env python3
"""Template reducer."""

import sys
import itertools


def reduce_one_group(partition_id, group):
    """Reduce one partition group: collect and sort its records."""
    records = []

    for line in group:
        line = line.rstrip("\n")
        _, _, value = line.partition("\t")
        if value:
            records.append(value.strip())

    for record in sorted(records, key=lambda item: item.split(" ", 1)[0]):
        print(record)


def keyfunc(line):
    """Extract partition key (partition ID)."""
    return line.partition("\t")[0]


def main():
    """Group rows by partition ID."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
