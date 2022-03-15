#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# #### Northwest Territories Child Care
# Retrieved from: https://www.ece.gov.nt.ca/en/childcare?page=4
#  
# Robots.txt: https://www.ece.gov.nt.ca/robots.txt
#  
# User-agent: *
#  
# Crawl-delay: 10s

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
logfile = open('nt.log', 'a')
logfile.write('{} nt.py execution by Kaitlyn Hobbs.\n'.format(datetime.now()))

# %% [markdown]
#
#
# ##### Execute scrape:
# <mark> Slow script below </mark>

# %%
name = []
address = []
location = []
status = []
contact = []
phone = []
links = set()

# Connection
url = 'https://www.ece.gov.nt.ca/en/childcare'
r = requests.get(url, headers=headers)
s = BeautifulSoup(r.text)

# Log
logfile.write('{} Connected to {}.\n'.format(datetime.now(), url))

# Collect information
tables = s.find_all('td')
for td in tables:
    try:
        links.add(td.findChild()['href'])
    except TypeError:
        pass

# %%
# Crawl through each facility link and scrape information
crawl = 'https://www.ece.gov.nt.ca'

# First page - because the domain name does not change
counter = 1
for l in links:
    print("{} of {} links".format(counter, len(links)))
    # Connect
    r = requests.get(crawl+l)
    s = BeautifulSoup(r.text)
    
    # Log
    logfile.write('{} Connected to {}.\n'.format(datetime.now(), crawl+l))
    
    # Collect data
    name.append(s.find('h1', {'id':'page-title'}).text)
    
    if s.find('div', {'class':'field field-name-field-address field-type-text field-label-above'}):
        address.append(s.find('div', {'class':'field field-name-field-address field-type-text field-label-above'}).findChild().findNext().text)
    else:
        address.append("none")
        
    if s.find('div', {'class':"field field-name-field-status field-type-list-text field-label-inline clearfix"}):
        status.append(s.find('div', {'class':"field field-name-field-status field-type-list-text field-label-inline clearfix"}).findChild().findNext().text)
    else:
        status.append("none")
        
    if s.find_all('div', {'class':'field field-name-field-location field-type-taxonomy-term-reference field-label-hidden'}):
        location.append(s.find('div', {'class':'field field-name-field-location field-type-taxonomy-term-reference field-label-hidden'}).findChild().text)
    else:
        location.append("none")
        
    if s.find_all('div', {'class':'field field-name-field-contact-name field-type-text field-label-inline clearfix'}):
        contact.append(s.find('div', {'class':'field field-name-field-contact-name field-type-text field-label-inline clearfix'}).findChild().findNext().text)
    else:
        contact.append("none")

    if s.find_all('div', {'class':'field field-name-field-company-phones field-type-multifield field-label-above'}):
        phone.append(s.find('div', {'class':'field field-name-field-company-phones field-type-multifield field-label-above'}).findChild().findNext().text)
    else:
        phone.append("none")
        
    # Log & Sleep
    time.sleep(5)
    logfile.write('{} Collected information.\n'.format(datetime.now()))
    
    counter +=1


# %%
# Remaining pages - iterate through each listed facility link
domain = "https://www.ece.gov.nt.ca/en/childcare?page="
pagelinks = set()

for i in range(1,5):
    print("Page {} of 5".format(i))
    # Connect
    r = requests.get(domain + str(i), headers = headers)
    s = BeautifulSoup(r.text)
    
    # Log
    logfile.write('{} Connected to {}.\n'.format(datetime.now(), crawl+l))
    
    # Collect
    column = s.find_all('td', {'class':'views-field views-field-title active'})
    for c in column:
        pagelinks.add(c.find('a')['href'])

    counter = 1
    for p in pagelinks:
        print("{} of {} links".format(counter, len(pagelinks)))
        # Connect - 2
        r = requests.get(crawl+p)
        s = BeautifulSoup(r.text)
        
        # Log - 2
        logfile.write('    {} Connected to {}.\n'.format(datetime.now(), crawl+p))
    
        # Collect - 2
        name.append(s.find('h1', {'id':'page-title'}).text)

        if s.find('div', {'class':'field field-name-field-address field-type-text field-label-above'}):
            address.append(s.find('div', {'class':'field field-name-field-address field-type-text field-label-above'}).findChild().findNext().text)
        else:
            address.append("none")

        if s.find('div', {'class':"field field-name-field-status field-type-list-text field-label-inline clearfix"}):
            status.append(s.find('div', {'class':"field field-name-field-status field-type-list-text field-label-inline clearfix"}).findChild().findNext().text)
        else:
            status.append("none")

        if s.find_all('div', {'class':'field field-name-field-location field-type-taxonomy-term-reference field-label-hidden'}):
            location.append(s.find('div', {'class':'field field-name-field-location field-type-taxonomy-term-reference field-label-hidden'}).findChild().text)
        else:
            location.append("none")

        if s.find_all('div', {'class':'field field-name-field-contact-name field-type-text field-label-inline clearfix'}):
            contact.append(s.find('div', {'class':'field field-name-field-contact-name field-type-text field-label-inline clearfix'}).findChild().findNext().text)
        else:
            contact.append("none")

        if s.find_all('div', {'class':'field field-name-field-company-phones field-type-multifield field-label-above'}):
            phone.append(s.find('div', {'class':'field field-name-field-company-phones field-type-multifield field-label-above'}).findChild().findNext().text)
        else:
            phone.append("none")
            
        counter +=1
            
        # Log & Sleep
        time.sleep(5)
        logfile.write('    {} Collected information.\n'.format(datetime.now()))

# %% [markdown]
# ##### Consolidate, Clean & Export:

# %%
final = pd.DataFrame({'facility_name':name, 'address':address, 
                      'city':location, 'status':status, 
                      'contact':contact, "phone":phone})

# Text formatting:
final.phone.replace("[Telephone]","", inplace = True, regex=True)
final.phone = final.phone.str.strip()
final.phone = final.phone.str.replace('Fax', ' Fax: ')
final.phone = final.phone.str.replace('WbsitYWCANW.ca', '')
final.phone = final.phone.str.replace('P', 'P: ')

# Encoding:
cols = ['facility_name', 'address', 'city', 'status', 'contact', 'phone']
for c in cols:
    final[c] = final[c].str.encode('ascii', 'ignore').str.decode('ascii')

final.to_csv('data/NT-childcare.csv')

# Log & close
logfile.write("{} Fin.\n\n".format(datetime.now()))
logfile.close()

