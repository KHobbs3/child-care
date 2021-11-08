#!/usr/bin/env python
# coding: utf-8

# **IN:** deduplicated and standard CSVs for each province
# 
# **OUT:** one merged file to be parsed




import pandas as pd
import os
import glob
import re
import numpy as np


#### Deduplicated output files

os.chdir('/Users/kt/Documents/work/STATCAN/ODECF/Wrangling-ODECF/output/childcare/deduplicated')
files = glob.glob('*.csv')


dedup = []
l = []
for f in files:
        dedup.append(pd.read_csv(f))
        full = pd.concat(dedup)
        l.append(len(pd.read_csv(f)))


#### Standardized output files

os.chdir('/Users/kt/.config/opentabulate.con/data/output')
std_files = []

for c in glob.glob('*.csv'):
    if c not in files:
        std_files.append(c)
        l.append(len(pd.read_csv(c)))


for s in std_files:
    if "street_number" in pd.read_csv(s).columns:
        print(s)

std = []
for s in std_files:
    std.append(pd.read_csv(s))
    full2 = pd.concat(std)


master = pd.concat([full, full2])#.drop(columns = 'Unnamed: 0')

# export
master.to_csv('/Users/kt/Documents/work/STATCAN/ODECF/Wrangling-ODECF/output/childcare/merged/childcare-merged.csv', encoding = "utf-8-sig")

