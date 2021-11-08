#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import glob
import os


master = pd.read_csv('output/childcare/parsed/childcare-parsed.csv')


# 1--------
# determine number of rows for each of the file prior to deduplication
os.chdir('/Users/kt/.config/opentabulate.con/data/output/')

orig = []
orig_len = []
for c in glob.glob('*.csv'):
    orig.append(c)
    orig_len.append(len(pd.read_csv(c)))

# 2--------
# determine number of rows for each of the deduplicated files
os.chdir('/Users/kt/Documents/work/STATCAN/ODECF/Wrangling-ODECF/output/childcare/deduplicated/')

dedup = []
len_each = []

for c in glob.glob('*.csv'):
    dedup.append(c)
    len_each.append(len(pd.read_csv(c)))
    
# + determine number of rows for each of the standardized (non-duplicated) files
os.chdir('/Users/kt/.config/opentabulate.con/data/output/')

std = []

for c in glob.glob('*.csv'):
    if c not in dedup:
        std.append(c)
        len_each.append(len(pd.read_csv(c)))

print("Rows before deduplication: {}\nRows after deduplication: {}\nRows after merge: {}".format(sum(orig_len), sum(len_each), len(master)))


# 3----------
# orig - deduplicated lengths to determine the expected number of rows removed from each

os.chdir('/Users/kt/Documents/work/STATCAN/ODECF/Wrangling-ODECF/output/childcare/deduplicated/')
for o, ol in zip(orig, orig_len):
        print("{} === before: {}".format(o, ol))


os.chdir('/Users/kt/Documents/work/STATCAN/ODECF/Wrangling-ODECF/output/childcare/deduplicated/')

for d in dedup:
    print("{} === after: {}".format(d, len(pd.read_csv(d))))


ntdiff = 282 - 131
nbdiff = 826-824
abdiff = 17282 - 2918
mbdiff = 2284-1110
qcdiff = 7096-3573
ondiff = 6995-6992
gdcdiff = 3293-3264

diffs = [ntdiff, nbdiff, abdiff, mbdiff, qcdiff, ondiff, gdcdiff]


print("Expected rows removed from deduplication: {}\nRows removed from deduplication: {}\nExpected final row count: {}\nActual final row count: {}".format(sum(diffs), sum(orig_len) - sum(len_each), sum(orig_len)-sum(diffs), len(master)))

