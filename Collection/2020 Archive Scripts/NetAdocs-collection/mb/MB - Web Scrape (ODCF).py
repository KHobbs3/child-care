#!/usr/bin/env python
# coding: utf-8

# ## Manitoba - Childcare Scrape
# Retrieved from: https://direct3.gov.mb.ca/86256AF2006B7D4F/Map?OpenForm&AGE=Infant,PreSchool,Nursery,SchoolAge&FAC=Group,Center,Nursery&OPN=Weekdays,Weekends,Evenings,Overnight&VAC=No&MAP=Manitoba&LANG=1

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random



headers = {
    'User-Agent': 'kt 1.0',
    'From': 'khobbs3@uwo.ca'
}


ages = ['Infant', 'Preschool', 'Nursery', 'School Age']
opn = ['Weekdays', 'Weekends', 'Evenings', 'Overnight']



domain = 'https://direct3.gov.mb.ca/daycare/fs/fs.nsf/'


# <mark> slow script ahead!!! </mark>

# initialize variables
url = 'https://direct3.gov.mb.ca/86256AF2006B7D4F/FacilityList?OpenForm&START=1&COUNT=1000&AGE={}&FAC=Group,%20Center,%20Nursery&OPN={}&VAC=No&MAP=Manitoba&AREA=CENTRAL,EASTMAN,INTERLAKE,NORMAN,PARKLAND,THOMPSON,WESTMAN,Brandon,R2_WPG&VIEW=P&LANG=1&ADV=No'
names = list()
links = list()


for a in ages:
    for o in opn:
        print(a, o)
        # change the url to iter through all age and opn options
        req = requests.get(url.format(a, o), headers=headers)
        soup = BeautifulSoup(req.text)
        
        tables = soup.find_all('table')
        
        # get names and request.get links to description pages. Scrape each facility
        for l in tables[3].find_all('a'):
            names.append(l.text)
            links.append(domain+l['href'])
        
            # wait
            time.sleep(random.uniform(1,4))
            
            



output = []
out_links = []

# remove duplicates except for those that are Family or Group Child  Care Home *
# duplicates identified on account of duplicate page links

for x,l in zip(names, links):
    if l not in out_links:
        output.append(x)
        out_links.append(l)
    if x == 'Family or Group Child  Care Home *':
        output.append(x)
        out_links.append(l)



output = []
out_links = []

# remove duplicates except for those that are Family or Group Child  Care Home *

for x,l in zip(names, links):
    if x not in output:
        output.append(x)
        out_links.append(l)
    if x == 'Family or Group Child  Care Home *':
        output.append(x)
        out_links.append(l)



print("before:", len(names), len(links))
print("after:", len(output), len(out_links))


domain = 'https://direct3.gov.mb.ca'
mb = {}

for l,i in zip(out_links,range(1,len(out_links)+1)):
    print('{} of {}'.format(i, len(out_links)))
    
    r = requests.get(l, headers = headers)
    s = BeautifulSoup(r.text)

    # scrape info
    table = s.find_all('table')[1]
    vals = table.select('td:nth-of-type(2)')
    kys = table.select('td:nth-of-type(1)')

    # make dict
    for k,v in zip(kys, vals):
        if k.text in mb.keys():
            mb[k.text].append(v.text)
        else:
            mb[k.text] = [v.text]

    # fill missing info
    if not any("Address" in k.text for k in kys):
        if "Address:" in mb.keys():
            mb["Address:"].append("None")
        else:
            mb["Address:"] = ["None"]
    else:
        pass

    if not any("Legal Name" in k.text for k in kys):
        if "Legal Name: " in mb.keys():
            mb["Legal Name: "].append("Family or Group Child  Care Home *")
        else:
            mb["Legal Name: "] = ["None"]
    else:
        pass

   

    # wait
    time.sleep(random.uniform(1,4))



for k,v in mb.items():
    print(k, len(v))


# Drop unneccessary key with missing values
mb.pop("Facility Director:")

MB = pd.DataFrame(mb)

# Check if all regions are there, if not add missing regions
MB.groupby('Region').describe()

#------------------------------------------------------
# MISSING REGIONS
#------------------------------------------------------
# Brandon
# ---

url2 ='https://direct3.gov.mb.ca/86256AF2006B7D4F/FacilityList?OpenForm&START=1&COUNT=1000&AGE={}&FAC=Group,%20%20Center,%20%20Nursery&OPN={}&VAC=No&MAP=Brandon&AREA=BRANDON%20CENTRAL,BRANDON%20EAST,BRANDON%20WEST,NORTH%20HILL&VIEW=P&LANG=1&ADV=No'

names_brandon = list()
links_brandon = list()


for a in ages:
    for o in opn:
        print("BRANDON", a, o)
        # change the url to iter through all age and opn options
        req2 = requests.get(url2.format(a, o), headers=headers)
        soup2 = BeautifulSoup(req2.text)
        
        tables = soup2.find_all('table')
        
        # get names and request.get links to description pages. Scrape each facility
        for l in tables[3].find_all('a'):
            names_brandon.append(l.text)
            links_brandon.append(domain+l['href'])
        
            # wait
            time.sleep(random.uniform(1,4))



output2 = []
out_links2 = []

# remove duplicates except for those that are Family or Group Child  Care Home *

for x,l in zip(names_brandon, links_brandon):
    if l not in out_links2:
        output2.append(x)
        out_links2.append(l)
    if x == 'Family or Group Child  Care Home *':
        output2.append(x)
        out_links2.append(l)


domain = 'https://direct3.gov.mb.ca'
brandon = {}

for l,i in zip(out_links2,range(1,len(out_links2)+1)):
    print('BR - {} of {}'.format(i, len(out_links2)))
    
    r2 = requests.get(l, headers = headers)
    s2 = BeautifulSoup(r2.text)

    # scrape info
    table = s2.find_all('table')[1]
    vals = table.select('td:nth-of-type(2)')
    kys = table.select('td:nth-of-type(1)')

    # make dict
    for k,v in zip(kys, vals):
        if k.text in brandon.keys():
            brandon[k.text].append(v.text)
        else:
            brandon[k.text] = [v.text]

    # fill missing info
    if not any("Address" in k.text for k in kys):
        if "Address:" in brandon.keys():
            brandon["Address:"].append("None")
        else:
            brandon["Address:"] = ["None"]
    else:
        pass

    if not any("Legal Name" in k.text for k in kys):
        if "Legal Name: " in brandon.keys():
            brandon["Legal Name: "].append("Family or Group Child  Care Home *")
        else:
            brandon["Legal Name: "] = ["None"]
    else:
        pass

   

    # wait
    time.sleep(random.uniform(1,4))



brandon.pop('Facility Director:')


# Winnipeg
# --------

url3 ='https://direct3.gov.mb.ca/86256AF2006B7D4F/FacilityList?OpenForm&START=1&COUNT=1000&AGE={}&FAC=Group,%20%20Center,%20%20Nursery&OPN={}&VAC=No&MAP=Winnipeg&AREA=ASSINIBOINE%20SOUTH,DOWNTOWN,FORT%20GARRY,INKSTER,POINT%20DOUGLAS,RIVER%20EAST,RIVER%20HEIGHTS,SEVEN%20OAKS,ST.BONIFACE,ST.JAMES%20ASSINIBOINE,ST.VITAL,TRANSCONA&VIEW=P&LANG=1&ADV=No'

names_winnipeg = list()
links_winnipeg = list()


for a in ages:
    for o in opn:
        print("WINNIPEG", a, o)
        # change the url to iter through all age and opn options
        req3 = requests.get(url3.format(a, o), headers=headers)
        soup3 = BeautifulSoup(req3.text)
        
        tables = soup3.find_all('table')
        
        # get names and request.get links to description pages. Scrape each facility
        for l in tables[3].find_all('a'):
            names_winnipeg.append(l.text)
            links_winnipeg.append(domain+l['href'])
        
            # wait
            time.sleep(random.uniform(1,4))


output3 = []
out_links3 = []

# remove duplicates except for those that are Family or Group Child  Care Home *

for x,l in zip(names_winnipeg, links_winnipeg):
    if l not in out_links3:
        output3.append(x)
        out_links3.append(l)
    if x == 'Family or Group Child  Care Home *':
        output3.append(x)
        out_links3.append(l)



domain = 'https://direct3.gov.mb.ca'
winnipeg = {}


for l,i in zip(out_links3,range(176,len(out_links3)+1)):
    print('wpg - {} of {}'.format(i, len(out_links3)))
    
    r3 = requests.get(l, headers = headers)
    s3 = BeautifulSoup(r3.text)

    # scrape info
    table = s3.find_all('table')[1]
    vals = table.select('td:nth-of-type(2)')
    kys = table.select('td:nth-of-type(1)')

    # make dict
    for k,v in zip(kys, vals):
        if k.text in winnipeg.keys():
            winnipeg[k.text].append(v.text)
        else:
            winnipeg[k.text] = [v.text]

    # fill missing info
    if not any("Address" in k.text for k in kys):
        if "Address:" in winnipeg.keys():
            winnipeg["Address:"].append("None")
        else:
            winnipeg["Address:"] = ["None"]
    else:
        pass

    if not any("Legal Name" in k.text for k in kys):
        if "Legal Name: " in winnipeg.keys():
            winnipeg["Legal Name: "].append("Family or Group Child  Care Home *")
        else:
            winnipeg["Legal Name: "] = ["None"]
    else:
        pass

   

    # wait
    time.sleep(random.uniform(1,4))



for k,v in winnipeg.items():
    print(k, len(v))



winnipeg.pop('Facility Director:')


# Merge, clean, export:
br = pd.DataFrame(brandon)
wp = pd.DataFrame(winnipeg)
MB_all = pd.concat([br,wp,MB])

MB_all.columns = ['Facility Number', 'Phone', 'Region', 'Area', 'Neighourhood', 'School Division', 'Type of Facility', 
                     'Age Type', 'Facility Open On', 'Total Child Care Spaces', 'Address', 'Legal Name']

MB_all['Legal Name'].replace({"None" : "Family or Group Child  Care Home *"}, inplace = True)

MB_all.Address = MB_all.Address.replace("\n", " ", regex = True)

MB_all.to_csv("data/childcare/MB-childcare.csv")


# <mark> N.B. * We have not published the names and addresses of Family and Group Facilities for security reasons. Please contact these facilities for further information including their location </mark>
