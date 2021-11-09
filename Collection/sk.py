#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# #### Saskatchewan Child Care
# Retrieved from: https://www.saskatchewan.ca/residents/family-and-social-support/child-care/find-a-child-care-provider-in-my-community
#  
# Robots.txt: Not found.
#
# Ref: https://datascience.stackexchange.com/questions/11730/how-to-scrape-a-website-with-a-searchbar/11734

# %%
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.auth import AuthBase
import time
from datetime import datetime

headers = {'User-Agent': 'Statistics Canada bot created by Kaitlyn Hobbs (kaitlyn.hobbs@statcan.gc.ca)'}


# %% [markdown]
# ##### Log file:

# %%
logfile = open('sk.log', 'a')
logfile.write('{} sk.py execution by Kaitlyn Hobbs.\n'.format(datetime.now()))

# %% [markdown]
# ##### Execute Scrape:

# %%
details = []
name = []
address = []
phone = []

domain = 'https://www.saskatchewan.ca/residents/family-and-social-support/child-care/find-a-child-care-provider-in-my-community?searchRadius=1000&userLong=-106.666667&userLat=52.133333&page='
for i in range(1,59):
    # Connect
    r = requests.get(domain+str(i), headers=headers)
    s = BeautifulSoup(r.text)
    
    # Log
    logfile.write('    {} Connected to {}.\n'.format(datetime.now(), domain+str(i)))
    
    # Collect
    centres=s.find('div', {'class':'map-result'}).find_all('li')
    
    for c in centres:
        details.append(c.text.split('\n')[1])
        name.append(c.text.split('\n')[2])
        address.append(c.text.split('\n')[3])
        phone.append(c.text.split('\n')[4].split('|')[0])
    
    # Log & Sleep
    logfile.write('    {} Collected information.\n'.format(datetime.now()))
    time.sleep(5)

# %% [markdown]
# ##### Consolidate, Clean & Export:

# %%
# Create DF, Text formatting:
df = pd.DataFrame({'facility_name': name, 'full_address': address, 'phone': phone, 'details': details})
df.facility_name.replace('[\\r]','', regex=True, inplace = True)

# Whitespaces:
rmvws = ['facility_name', 'full_address', 'phone', 'details']
for r in rmvws:
    df[r] = df[r].str.strip()
    
# Encoding:
df.full_address = df.full_address.str.encode('ascii', 'ignore').str.decode('ascii')
df.facility_name = df.facility_name.str.encode('ascii', 'ignore').str.decode('ascii')
    
df.to_csv('data/SK-childcare.csv')

# Log & close
logfile.write("{} Fin.\n\n".format(datetime.now()))
logfile.close()

