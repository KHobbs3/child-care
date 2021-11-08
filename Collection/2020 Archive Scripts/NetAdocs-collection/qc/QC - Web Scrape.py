#!/usr/bin/env python
# coding: utf-8

# #### Quebec
# Retrieved from: https://www.mfa.gouv.qc.ca/fr/services-de-garde/parents/localisateur/Pages/liste.aspx

import numpy as np
import pandas as pd

import re
import requests
import time
from bs4 import BeautifulSoup


# *Scraper info*

headers = {
    'User-Agent': 'kt 1.0',
    'From': 'khobbs3@uwo.ca'
}

r = requests.get('https://www.mfa.gouv.qc.ca/fr/services-de-garde/parents/localisateur/Pages/liste.aspx', headers = headers)
s = BeautifulSoup(r.text)

domain = 'https://www.mfa.gouv.qc.ca'
cc = []
links = []


childcare = s.find_all('a', {'title':re.compile("Répertoire des services de garde par région administrative —?")})
for centre in childcare:
    cc.append(centre.text)
    links.append(domain + centre['href'])


# Download and concat each link
# * CSV Tab 1: CPE and GARD
# * CSV Tab 2: BC-MF

qc = pd.read_excel(links[0], header = 3, skipfooter = 4)
qc2 = pd.read_excel(links[0], sheet_name = "BC-MF", header = 3, skipfooter = 8)
master = pd.concat([qc, qc2], ignore_index=True)

master.info()

for link,c in zip(links[1::],cc[1::]):
    addme = pd.read_excel(link, header = 3, skipfooter = 4)
    addme2 = pd.read_excel(links[0], sheet_name = "BC-MF", header = 3, skipfooter = 8)
    full = pd.concat([addme, addme2], ignore_index=True)
    master = pd.concat([master, addme], ignore_index=True)


cols = ['Nom de l\'installation', 'Région administrative', 'Adresse',
       'Municipalité', 'Code postal', 'Téléphone', 'Télécopieur',
       'Adresse courriel', 'Type de service de garde',
       'Places totales au permis', 'Places 17 mois ou moins',
       'Place à contribution réduite', 'Territoire couvert',
       'Places totales à l\'agrément', 'Nombre de RSG reconnues']
for c in cols:
    try:
        master[c] = master[c].str.encode('utf-8-sig', 'ignore').str.decode('utf-8-sig')
    except AttributeError:
        print(c)


master.head()
master.to_csv('data/childcare/QC-CPE-GARD-MF.csv', encoding = 'utf-8-sig')
