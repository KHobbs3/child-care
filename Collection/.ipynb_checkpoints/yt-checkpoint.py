#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# ##### Yukon Territories
#  
# Retrieved from: https://yukon.ca/en/education-and-schools/early-childhood-learning-and-programs/find-child-care-yukoners#day-care-centres
#
# Robots.txt: https://yukon.ca/robots.txt
#
# User-agent: *
#
# Crawl-delay: 10s

# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

headers = {'User-Agent': 'Statistics Canada bot created by Kaitlyn Hobbs (kaitlyn.hobbs@statcan.gc.ca)'}


# %% [markdown]
# ##### Log file:

# %%
logfile = open('yt.log', 'a')
logfile.write('{} yt.py execution by Kaitlyn Hobbs.\n'.format(datetime.now()))

# %% [markdown]
# ##### Execute Scrape:

# %%
domain = "https://yukon.ca/en/education-and-schools/early-childhood-learning-and-programs/find-child-care-yukoners"
suffix = ['#day-care-centres', '#family-day-homes', '#communities']

name = []
ages = []
address = []
phone = []
source_type = []

for suf in suffix:
    # Connect
    r = requests.get(domain + suf, headers=headers)
    s = BeautifulSoup(r.text)

    # Log
    logfile.write('    {} Connected to {}.\n'.format(datetime.now(), domain + suf))

    # Collect
    childcare = s.find_all('h3')
    for n in childcare:
        name.append(n.text)

    for fac in s.find_all('div', {'class': 'field-item even'}):
        for child in fac.findChildren("li" , recursive=True):
            if "Address" in child.text:
                address.append(child.text)
            if "Licenced" in child.text.split(": ")[1]:
                ages.append(child.text)
            if "Phone" in child.text:
                phone.append(child.text)
            source_type.append(suf.replace('#', '').replace('-', ' '))

    # Log & sleep
    logfile.write('    {} Collected information.\n'.format(datetime.now())
    time.sleep(10)

# %% [markdown]
# ##### Consolidate, Clean & Export:

# %%
yk = pd.DataFrame({
    'name' : name, 'address' : address,
    'age': age, 'phone': phone,
    'source_type': source_type
                  })

# Encoding:
ykcols = ['name', 'address', 'age', 'phone', 'source_type']
for y in ykcols:
    yk[y] = yk[y].str.encode('ascii', 'ignore').str.decode('ascii')
    
# TODO:


# %%
yk.to_csv('data/YT-childcare.csv')

# Log & close
logfile.write("{} Fin.\n\n".format(datetime.now()))
logfile.close()
