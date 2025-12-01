#!/usr/bin/env python3
"""
Template reducer version.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    """Sum counts for each (term, doc_id) pair and print."""
    total = 0
    term, doc_id = key.split("\t", 1)

    for line in group:
        parts = line.rstrip("\n").split("\t")
        _, _, value = parts
        total += int(value)

    print(f"{term}\t{doc_id}\t{total}")


def keyfunc(line):
    """
    Return the key from a TAB-delimited (term, doc_id, count) line.

    Key = 'term (tab) doc_id'
    """
    parts = line.split("\t")
    if len(parts) < 2:
        return ""
    return f"{parts[0]}\t{parts[1]}"


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
