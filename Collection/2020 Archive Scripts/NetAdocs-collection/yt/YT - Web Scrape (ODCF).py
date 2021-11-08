#!/usr/bin/env python
# coding: utf-8

# #### Yukon Territories
# 
# Retrieved from: https://yukon.ca/en/child-care-information-yukoners

import pandas as pd

import requests
from bs4 import BeautifulSoup

import time
import random

headers = {
    'User-Agent': 'kt 1.0',
    'From': 'khobbs3@uwo.ca'
}


r = requests.get("https://yukon.ca/en/child-care-information-yukoners", headers=headers)
s = BeautifulSoup(r.text)

childcare = s.find_all('p')
childcare = childcare[2:-2]

cc = {
     'name': ['Toy’s FDH'], 
     'address': ['15 Cedar Cres, Y1A 4P2)'],
     'year': ['since 2004'],
     'phone': ['633-6768'],
     'license': ['licensed for 10 children'],
     'age': ['infants and older'],
     'requirements': ['2 year diploma in ECD'],
     'details': ['meals available']
     }

for c in childcare:
    splt = c.text.split(';')
    
    if len(splt) == 6:
        cc['name'].append(splt[0].split(' (')[0])
        cc['address'].append(splt[0].split(' (')[1])
        cc['year'].append(splt[1])
        cc['phone'].append(splt[2])
        cc['license'].append(splt[3])
        cc['age'].append(splt[4])
        cc['requirements'].append(splt[5])
        cc['details'].append("none")
        
    if len(splt) == 7:
        cc['name'].append(splt[0].split(' (')[0])
        cc['address'].append(splt[0].split(' (')[1])
        cc['year'].append(splt[1])
        cc['phone'].append(splt[2])
        cc['license'].append(splt[3])
        cc['age'].append(splt[4])
        cc['requirements'].append(splt[5])
        cc['details'].append(splt[6])
        
    if len(splt) == 5:
        cc['name'].append(splt[0].split(' (')[0])
        cc['address'].append(splt[0].split(' (')[1])
        cc['year'].append("none")
        cc['phone'].append(splt[1])
        cc['license'].append(splt[2])
        cc['age'].append(splt[3])
        cc['requirements'].append(splt[4])
        cc['details'].append("none")


yk = pd.DataFrame(cc)


# Clean cols
ykcols = ['name', 'address', 'year', 'phone', 'license', 'age', 'requirements',
       'details']

for y in ykcols:
    yk[y] = yk[y].str.encode('ascii', 'ignore').str.decode('ascii')

yk.address = yk.address.replace('[\)]', '', regex=True)

# Manually fix random errors
yk.loc[yk.name == 'Montessori Borealis', 'phone'] =  '668-2268'
yk.loc[yk.name == 'Montessori Borealis', 'license'] = 'licensed for 24 children'
yk.loc[yk.name == 'Montessori Borealis', 'age'] = 'pre-school'

yk.loc[yk.name == 'La Garderie du Petit Cheval Blanc School Age Program', 'year'] = "none"
yk.loc[yk.name == 'La Garderie du Petit Cheval Blanc School Age Program', 'phone'] = "633-6566"
yk.loc[yk.name == 'La Garderie du Petit Cheval Blanc School Age Program', 'license'] = "licensed for 45 children"
yk.loc[yk.name == 'La Garderie du Petit Cheval Blanc School Age Program', 'age'] = "kindergarten and school-age, French language only"
yk.loc[yk.name == 'La Garderie du Petit Cheval Blanc School Age Program', 'requirements'] = "training compliant"
yk.loc[yk.name == 'La Garderie du Petit Cheval Blanc School Age Program', 'details'] = "meals available."

yk.head()

yk.to_csv('data/childcare/YT-childcare.csv')

