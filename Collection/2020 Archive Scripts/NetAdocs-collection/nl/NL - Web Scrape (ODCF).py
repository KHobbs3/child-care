#!/usr/bin/env python
# coding: utf-8

# #### Newfoundland
# <mark> Scraped </mark> from: https://www.childcare.gov.nl.ca/public/ccr/childcare?apply_table_filters=1&keyword=
# 
# java -jar /usr/local/bin/selenium-server-standalone-3.141.59.jar

import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import time
import random
from bs4 import BeautifulSoup


opts = Options()
opts.add_argument("user-agent=kt v 1.0")


driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)


my_url = 'https://www.childcare.gov.nl.ca/public/ccr/childcare/?apply_table_filters=1&keyword=&childcare-p=YTozOntzOjc6ImtleXdvcmQiO047czoxMDoicGFnaW5hdGlvbiI7aToxO3M6MTM6InJvd3NfcGVyX3BhZ2UiO2k6MTAwMDA7fQ%3D%3D'
driver.get(my_url)


nl = pd.read_html(driver.page_source)[0]


# *Crawl & scrape for postal codes*
s = BeautifulSoup(driver.page_source)
cells = s.find_all('td')

domain = 'https://www.childcare.gov.nl.ca'
links = set()

for c in cells:
    if c.getText() == 'Details':
        links.add(domain + c.findChild('a')['href'])


pc = []
phone = []
mailing = []
hours = []
days = []
months = []
i = 1

for l in links:
    print(i)
    
    driver.get(l)
    res = driver.page_source
    soup = BeautifulSoup(res)
    
    try:
        pc.append(soup.find('dd', {"id" : "form-field-display-value-form-field-element-text-addr_postal"}).text)
    except AttributeError:
        pc.append("none")
        
    try:
        phone.append(soup.find('dd', {"id" : "form-field-display-value-form-field-element-text-telephone"}).text)
    except AttributeError:
        phone.append("none")
        
    try:
        mailing.append(soup.find('dd', {"id" : "form-field-display-value-form-field-element-textarea-addr_mailing"}).text)
    except AttributeError:
        mailing.append("none")
    
    try:
        hours.append(soup.find('dd', {"id" : "form-field-display-value-form-field-element-textarea-hours_of_operation"}).text)
    except AttributeError:
        hours.append("none")
        
    try:
        days.append(soup.find('dd', {"id" : "form-field-display-value-form-field-element-textarea-days_of_operation"}).text)
    except AttributeError:
        days.append("none")
        
    try:
        months.append(soup.find('dd', {"id" : "form-field-display-value-form-field-element-textarea-weeks_of_operation"}).text)
    except AttributeError:
        months.append("none")
        
    i += 1
        
    time.sleep(random.uniform(2,6))

driver.close()


nl['postal_code'] = pc
nl['phone'] = phone
nl['mailing_address'] = mailing
nl['hours_operation'] = hours
nl['days_operation'] = days
nl['months_operation'] = months


nl.mailing_address = nl.mailing_address.str.replace('\n', ' ', regex=True)
nl.mailing_address = nl.mailing_address.str.replace('\t', ' ', regex=True)


nl.drop(columns = "Unnamed: 6", inplace = True)

nl.info()
nl.tail()


nl.to_csv('data/childcare/NL-childcare.csv')



