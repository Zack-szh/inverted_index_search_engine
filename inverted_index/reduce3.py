#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math


def reduce_one_group(key, group):
    """Reduce one group."""
    with open("total_document_count.txt", encoding="utf-8") as file:
        n = file.readline().strip()
        n = int(n)

    doc_info = []
    for line in group:
        line = line.strip()

        stuff = line.split("\t")

        doc_id = stuff[1]
        tf = int(stuff[2])
        doc_info.append((doc_id, tf))

    if not doc_info:
        return

    n_k = len(doc_info)

    idf = math.log10(n / n_k)

    for doc_id, tf in sorted(doc_info, key=lambda item: item[0]):
        print(f"{doc_id}\t{key}\t{tf}\t{idf}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
