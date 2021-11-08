#!/usr/bin/env python
# coding: utf-8

# #### Northwest Territories
# Retrieved from: https://www.ece.gov.nt.ca/en/childcare?page=4

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

# for the final df
name = []
address = []
location = []
status = []
contact = []
phone = []


links = set()

r = requests.get('https://www.ece.gov.nt.ca/en/childcare')
s = BeautifulSoup(r.text)
# column = s.find_all('td', {'class':'views-field views-field-title active'})

tables = s.find_all('td')

for td in tables:
    try:
        links.add(td.findChild()['href'])
    except TypeError:
        pass


# <mark> Slow script below </mark>

# crawl through each facility link and scrape information
crawl = 'https://www.ece.gov.nt.ca'

# First page - because the domain name does not change
counter = 1
for l in links:
    print("{} of {} links".format(counter, len(links)))
    r = requests.get(crawl+l)
    s = BeautifulSoup(r.text)
    
    # gather data
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
        
    time.sleep(random.uniform(2,5))
    counter +=1

# # Remaining pages - iterate through each listed facility link
domain = "https://www.ece.gov.nt.ca/en/childcare?page="
pagelinks = set()

for i in range(1,5):
    print("Page {} of 5".format(i))
    r = requests.get(domain + str(i), headers = headers)
    s = BeautifulSoup(r.text)
    
    column = s.find_all('td', {'class':'views-field views-field-title active'})
    for c in column:
        pagelinks.add(c.find('a')['href'])

    counter = 1
    for p in pagelinks:
        print("{} of {} links".format(counter, len(pagelinks)))
        r = requests.get(crawl+p)
        s = BeautifulSoup(r.text)
        
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
            
        time.sleep(random.uniform(2,6))


final = pd.DataFrame({'facility_name':name, 'address':address, 'city':location, 'status':status, 'contact':contact, "phone":phone})
final.phone.replace("[Telephone]","", inplace = True, regex=True)

final.info()
final.head()

final.phone = final.phone.str.strip()
final.phone = final.phone.str.replace('Fax', ' Fax: ')
final.phone = final.phone.str.replace('WbsitYWCANW.ca', '')
final.phone = final.phone.str.replace('P', 'P: ')

cols = ['facility_name', 'address', 'city', 'status', 'contact', 'phone']

for c in cols:
    final[c] = final[c].str.encode('ascii', 'ignore').str.decode('ascii')

final.to_csv('data/childcare/NT-childcare.csv')

