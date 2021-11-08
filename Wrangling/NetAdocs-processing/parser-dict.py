#!/usr/bin/env python
# coding: utf-8

# #### Address cleaning

# **IN:** cleaned file
# **OUT:** parsed file


from postal.parser import parse_address
import pandas as pd
import os
import re

df = pd.read_csv('../childcare-to-parse.csv', encoding = 'utf-8')

#### Part 2: Full address parsing

df.full_address = df.full_address.astype(str)
parsed = df.full_address.map(parse_address)


# initialize empty dictionary with set keys
keys = set()
for p in parsed:
        for v,k in p:
            keys.add(k)
            
parsed_dict = {k: [] for k in keys} 
parsed_dict

# convert set to list of all unique keys for reference
keylst = [k for k in keys]

# initialize master dictionary for parser output
master = {k: [] for k in keys} 

for p in parsed:
    # make a dict of all the keys and values in each address parse
    currentkeys = []
    
    # separate the parsed tuple and add to list
    for v,k in p:
        currentkeys.append(k)
    
    # initialize dictionary for current address parse bits
    current = {k: [] for k in currentkeys} 
    
    # complete current dictionary
    for v,k in p:
        current[k] = v
        
    # iter through all the possible keys in master dict, which need to be of equal length
    for masterkey in keylst:
        # if theres the dict key in current address, retrieve the value and append it to our master dict
        if masterkey in current.keys():
            master[masterkey].append(current[masterkey])

        # else, append a space holder
        else:
            master[masterkey].append('')


# check they are all the same length
for k,v in master.items():
    print(k, len(v))

master_df = pd.DataFrame(master)

# fill parsed data in the childcare dataframe
df['unit'] = master_df.unit
df.street_name.fillna(value = master_df.road, inplace = True)
df.street_number.fillna(value = master_df.house_number, inplace = True)
df.street_number.fillna(value = master_df.postcode, inplace = True)
df.unit.fillna(value = master_df.level, inplace = True)


# Export 5% sample for verification
# df[['name', 'source_full_address', 'full_address', 'street_number', 'street_name', 'unit', 'city', 'province', 'provider']].sample(int(len(df)*0.05)).to_csv("../childcare-0.05-percent.csv", encoding = "utf-8-sig")

# Export
df.to_csv('../childcare-parsed.csv', encoding = 'utf-8')
