#!/usr/bin/env python3
"""Map 2."""

import sys
import re


stopwords = []
with open("stopwords.txt", "r", encoding="utf-8") as stopwords_file:
    for line in stopwords_file:
        word = line.strip()
        stopwords.append(word)

for line in sys.stdin:
    line = line.rstrip("\n")
    line = line.partition("\t")
    doc_id = line[0]
    content = line[2]

    tfs = {}

    tokens = re.compile(r"[^a-zA-Z0-9 ]+").sub("", content.casefold()).split()

    for t in tokens:
        if t not in stopwords:
            if t in tfs:
                tfs[t] += 1
            else:
                tfs[t] = 1

    for t, f in tfs.items():
        print(f"{t}\t{doc_id}\t{f}")
