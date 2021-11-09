#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# #### New Brunswick Child Care
# Retrieved from: https://www.nbed.nb.ca/parentportal/en/search/elc
#
# Robots.txt: https://www.nbed.nb.ca/robots.txt
#  
# User-agent: *  

# %%
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from datetime import datetime


# %%
# os.system("java -jar /usr/local/bin/selenium-server-standalone-3.141.59.jar")

opts = Options()
opts.add_argument("user-agent=Statistics Canada bot created by Kaitlyn Hobbs (kaitlyn.hobbs@statcan.gc.ca)")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)

# %% [markdown]
# ##### Log file:

# %%
logfile = open('nb.log', 'a')
logfile.write('{} nb.py execution by Kaitlyn Hobbs.\n'.format(datetime.now()))


# %% [markdown]
# ##### Functions:

# %%
def get_header(elem):
    """
    Grabs information from header portion of info box.
    """
    kys = ['facility', 'type', 'community', 'language', 'agegroups']

    for k,e in zip(kys, elem.text.split('\n')):
        if k in cc.keys():
            cc[k].append(e)
        else:
            cc[k] = [e]
    logfile.write('{} Collected facility, type, community, language, age group information.\n'.format(datetime.now()))
            
def get_table(elem):
    """
    Grabs information from table portion of info box.
    """
    tabkeys = ['district', 'address', 'operator', 'num_spaces', 'age', 'licence_status']
    for tk, e in zip(tabkeys, elem):
        if tk in cc.keys():
            cc[tk].append(e.text)
        else:
            cc[tk] = [e.text]
    logfile.write('{} Collected district, address, operator, number of spaces, age group information.\n'.format(datetime.now()))
   



# %% [markdown]
# ##### Execute Scrape:
# <mark> Slow script ahead. Subject to modification after testing. </mark>

# %%
url = 'https://www.nbed.nb.ca/parentportal/en/search/elc'
driver.get(url)
logfile.write('{} Connected to {}.\n'.format(datetime.now(), url))


# %%
# Expand all buttons to see information:
elem1 = driver.find_element_by_xpath('//*[@id="SearchFacilities"]')
elem1.click()

# Log & sleep
logfile.write('{} Element clicked.\n'.format(datetime.now()))
time.sleep(5)

for i in range(0, 95):
    # Click through elements
    elem3 = driver.find_element_by_xpath('//*[@id="DLMIRForm"]/div[6]/div')
    elem3.click()
    
    # Log & sleep
    logfile.write('{} Element clicked.\n'.format(datetime.now()))
    time.sleep(5)


# %%
cc = {}

# first bit
for i in range(2,15):
    for ii in range(1, 11):
        print(i, "---" ,ii)
        # Click through elements
        xpath = '/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[{}]/div[{}]'.format(i, ii)
        elem4 = driver.find_element_by_xpath(xpath)
        elem4.click()
        logfile.write('{} Element clicked.\n'.format(datetime.now()))
        get_header(elem4)
        
        # Collect 
        elemt = driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[{}]/div[{}]'.format(i, ii))
        contents = elemt.find_elements_by_class_name('list-unstyled')
        get_table(contents)
        
        # Log & sleep
        logfile.write('{} Table content collected.\n'.format(datetime.now()))
        time.sleep(5)


# %%
# do exception error separately
for i in range(1, 11):
    print("15 ---", i)
    
    # Click through elements
    xpath = '/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[15]/div[{}]'.format(i)
    elem4 = driver.find_element_by_xpath(xpath)
    get_header(elem4)
    elem4.click()
    logfile.write('{} Element clicked.\n'.format(datetime.now()))
    
    # Collect
    elemt = driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[15]/div[{}]'.format(i))
    contents = elemt.find_elements_by_class_name('list-unstyled')
    get_table(contents)
    
    # Log & sleep
    logfile.write('{} Table content collected.\n'.format(datetime.now()))
    time.sleep(5)


# %%
# the rest
for i in range(16,84):
    for ii in range(1,11):
        try:
                print(i, "---" ,ii)
                # Click through elements
                xpath = '/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[{}]/div[{}]'.format(str(i), str(ii))
                elem4 = driver.find_element_by_xpath(xpath)
                elem4.click()
                get_header(elem4)
                
                # Log & sleep
                logfile.write('{} Element clicked.\n'.format(datetime.now()))
                time.sleep(5)
            
                # Collect
                elemt = driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[{}]/div[{}]'.format(i, ii))
                contents = elemt.find_elements_by_class_name('list-unstyled')
                get_table(contents)
                logfile.write('{} Table content collected.\n'.format(datetime.now()))

        except ElementClickInterceptedException:
            print("exception at:", i, "---" ,ii)
            xpath = '/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[{}]/div[{}]/div[{}]/div/div'.format(str(i), str(ii), 1)
            elem4 = driver.find_element_by_xpath(xpath)
            elem4.click()
            get_header(elem4)
            
            # Log & sleep
            logfile.write('{} Element clicked.\n'.format(datetime.now()))
            time.sleep(5)
            
            # get table information
            elemt = driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div[5]/div/div/div[1]/div[{}]/div[1]')
            contents = elemt.find_elements_by_class_name('list-unstyled')
            get_table(contents)
            logfile.write('{} Table content collected.\n'.format(datetime.now()))
            
        if i == 83 and ii == 10:
            # end of list
            break

        # Sleep
        time.sleep(5)


# %% [markdown]
# ##### Consolidate, Clean & Export:


# %%
# Remove language
cc.pop("language")

for k,v in cc.items():
    print(k, len(v))


# Create dataframe and clean
nb = pd.DataFrame(cc)
cols = ['facility', 'type', 'community', 'agegroups', 'district',
       'address/phone', 'operator', 'num_spaces', 'age', 'licence_status']

for c in cols:
    nb[c].iloc[1::] = nb[c].iloc[1::].str[0]
    nb[c] = nb[c].str.encode('ascii', 'ignore').str.decode('ascii')
    
nb['address/phone'].replace({'\n':' '}, regex = True, inplace = True)
nb['age'].replace({'\n':', '}, regex = True, inplace = True)

# Convert to ascii encoding:
cols = nb.columns.to_list()
for c in cols:
    try:
        nb[c] = nb[c].str.encode('ascii', 'ignore').str.decode('ascii')
    except AttributeError:
        pass
    

nb.to_csv('data/NB-childcare.csv')

# Log & close
logfile.write("{} Fin.\n\n".format(datetime.now()))
logfile.close()
