#!/usr/bin/env python
# coding: utf-8

# #### Saskatchewan
# Retrieved from: https://www.saskatchewan.ca/residents/family-and-social-support/child-care/find-a-child-care-provider-in-my-community
# 
# Ref: https://datascience.stackexchange.com/questions/11730/how-to-scrape-a-website-with-a-searchbar/11734

import numpy as np
import pandas as pd

import requests
import time
import random
from bs4 import BeautifulSoup
from requests.auth import AuthBase


headers = {
    'User-Agent': 'kt 1.0',
    'From': 'khobbs3@uwo.ca'
}


details = []
name = []
address = []
phone = []


domain = 'https://www.saskatchewan.ca/residents/family-and-social-support/child-care/find-a-child-care-provider-in-my-community?searchRadius=1000&userLong=-106.666667&userLat=52.133333&page='
for i in range(1,59):
    r = requests.get(domain+str(i), headers=headers)
    s = BeautifulSoup(r.text)
    
    centres=s.find('div', {'class':'map-result'}).find_all('li')
    
    for c in centres:
        details.append(c.text.split('\n')[1])
        name.append(c.text.split('\n')[2])
        address.append(c.text.split('\n')[3])
        phone.append(c.text.split('\n')[4].split('|')[0])
    
    print(domain+str(i), len(name))
    
    time.sleep(random.uniform(5,15))


df = pd.DataFrame({'facility_name':name, 'full_address':address, 'phone':phone, 'details': details})


df.facility_name.replace('[\\r]','', regex=True, inplace = True)

df.info()
df.head()

# Clean Cols
rmvws = ['facility_name', 'full_address', 'phone', 'details']
for r in rmvws:
    df[r] = df[r].str.strip()

df.full_address = df.full_address.str.encode('ascii', 'ignore').str.decode('ascii')
df.facility_name = df.facility_name.str.encode('ascii', 'ignore').str.decode('ascii')


# Export

df.to_csv('data/childcare/SK-childcare.csv')

