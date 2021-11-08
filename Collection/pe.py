#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
#
# #### PEI Child Care
# Retrieved from: https://peichildcareregistry.com/search.php
#  
# Robots.txt: Not found.

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
import random
from tqdm import tqdm_notebook as tqdmn
import folium
from datetime import datetime


# %% [markdown]
# ##### Log file:

# %%
logfile = open('pe.log', 'a')
logfile.write('{} pe.py execution by Kaitlyn Hobbs.\n'.format(datetime.now()))

# %%
# os.system("java -jar /usr/local/bin/selenium-server-standalone-3.141.59.jar")

opts = Options()
opts.add_argument("user-agent=Statistics Canada bot created by Kaitlyn Hobbs (kaitlyn.hobbs@statcan.gc.ca)")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)

# %% [markdown]
# ##### Execute Scrape:

# %%
url = 'https://peichildcareregistry.com/search.php'
driver.get(url)
logfile.write('{} Connected to {}.\n'.format(datetime.now(), url))


# %%
pe = {}
for i in range(1,9):
    # page iteration
    driver.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[4]/a[{}]'.format(i)).click()
    logfile.write('{} Page clicked.\n'.format(datetime.now()))
    
    print("Page {}:".format(i))
    if i in range(8):
        # ie. not the last page
        for num in range(1,11):
            print("{} of 10".format(num))
            box = driver.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1]'.format(num))
            name = box.find_element_by_tag_name('h2').text
            
            # Get rest of information in the childcare facility box
            elemnt = box.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1][text()]'.format(num)).text.split('\n')
            logfile.write('{} Collected information in child care facility box.\n'.format(datetime.now()))
            
            # Set up name in pe dictionary
            if 'Name' not in pe.keys():
                pe['Name'] = [name]
            else:
                pe['Name'].append(name)

            # Add the rest of the facility info to dictionary
            for i in elemnt[1::]:
                try:
                    if i.split(': ')[0] not in pe.keys():
                        pe[i.split(': ')[0]] = [i.split(': ')[1]]
                    else:
                        pe[i.split(': ')[0]].append(i.split(': ')[1])
                except IndexError:
                    pass
                
        # Sleep
        time.sleep(random.randint(5,15))

    if i == 8:
        # Last page
        for num in range(1,8):
            print("{} of 7".format(num))
            box = driver.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1]'.format(num))
            name = box.find_element_by_tag_name('h2').text
            
            # Get rest of information in the childcare facility box
            elemnt = box.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1][text()]'.format(num)).text.split('\n')
            logfile.write('{} Collected information in child care facility box.\n'.format(datetime.now()))
            
            # Add the rest of the facility info to dictionary
            pe['Name'].append(name)
            
            for i in elemnt[1::]:
                try:
                    if i.split(': ')[0] not in pe.keys():
                        pe[i.split(': ')[0]] = [i.split(': ')[1]]
                    else:
                        pe[i.split(': ')[0]].append(i.split(': ')[1])
                except IndexError:
                    pass



# %%
driver.close()

# %% [markdown]
# ##### Clean & Export:

# %%
for k,v in pe.items():
    print(k, len(v))

# Drop unneccessary key with missing values (Centre Accommdates gives hours: part time, seasonal, alternate)
pe.pop("Centre Accommodates")

pd.DataFrame(pe).to_csv('data/PE-childcare.csv')

# Log & close
logfile.write("{} Fin.\n\n".format(datetime.now()))
logfile.close()

