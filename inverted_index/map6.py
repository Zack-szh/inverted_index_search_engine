#!/usr/bin/env python3
"""Map 6."""

import sys


for line in sys.stdin:
    line = line.strip()
    content = line.split()

    term = content[0]
    idf = content[1]
    the_rest = content[2:]

    info = {}

    for i in range(0, len(the_rest), 3):
        doc_id = the_rest[i]
        tf = the_rest[i + 1]
        normalization_factor = the_rest[i + 2]
        segment = int(doc_id) % 3
        if segment not in info:
            info[segment] = []
        info[segment].append((doc_id, tf, normalization_factor))

    for segment, value in info.items():
        sorted_values = sorted(value, key=lambda item: item[0])
        output = " ".join(
            f"{doc_id} {tf} {normalization_factor}"
            for doc_id, tf, normalization_factor in sorted_values
        )
        print(f"{segment}\t{term} {idf} {output}")
