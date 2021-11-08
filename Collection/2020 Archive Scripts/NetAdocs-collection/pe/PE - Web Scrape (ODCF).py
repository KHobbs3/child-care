#!/usr/bin/env python
# coding: utf-8

# ### PEI
# Retrieved from: https://peichildcareregistry.com/search.php
# 
# `java -jar /usr/local/bin/selenium-server-standalone-3.141.59.jar`


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

pd.set_option('display.max_columns', 60)
opts = Options()
opts.add_argument("user-agent=kt v 1.0")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)


url = 'https://peichildcareregistry.com/search.php'
driver.get(url)


pe = {}
for i in range(1,9):
    # page iteration
    driver.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[4]/a[{}]'.format(i)).click()
    print("Page {}:".format(i))
    if i in range(8):
        # ie. not the last page
        for num in range(1,11):
            print("{} of 10".format(num))
            box = driver.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1]'.format(num))
            name = box.find_element_by_tag_name('h2').text
            # get rest of information in the childcare facility box
            elemnt = box.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1][text()]'.format(num)).text.split('\n')

            # set up name in pe dictionary
            if 'Name' not in pe.keys():
                pe['Name'] = [name]
            else:
                pe['Name'].append(name)

            # add the rest of the facility info to dictionary
            for i in elemnt[1::]:
                try:
                    if i.split(': ')[0] not in pe.keys():
                        pe[i.split(': ')[0]] = [i.split(': ')[1]]
                    else:
                        pe[i.split(': ')[0]].append(i.split(': ')[1])
                except IndexError:
                    pass
                
        # wait between pages
        time.sleep(random.uniform(1,5))

    if i == 8:
        # last page
        for num in range(1,8):
            print("{} of 7".format(num))
            box = driver.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1]'.format(num))
            name = box.find_element_by_tag_name('h2').text
            # get rest of information in the childcare facility box
            elemnt = box.find_element_by_xpath('/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[{}]/div[1]/div[1][text()]'.format(num)).text.split('\n')

            # add the rest of the facility info to dictionary
            pe['Name'].append(name)
            
            for i in elemnt[1::]:
                try:
                    if i.split(': ')[0] not in pe.keys():
                        pe[i.split(': ')[0]] = [i.split(': ')[1]]
                    else:
                        pe[i.split(': ')[0]].append(i.split(': ')[1])
                except IndexError:
                    pass
                

# last page
# '/html/body/main/section/div/div/div[2]/div/div[3]/div/div/div/div/div[7]'


for k,v in pe.items():
    print(k, len(v))


# Drop unneccessary key with missing values (Centre Accommdates gives hours: part time, seasonal, alternate)
pe.pop("Centre Accommodates")

pd.DataFrame(pe).to_csv('data/childcare/PE-childcare.csv')

pe2.info()

driver.close()

