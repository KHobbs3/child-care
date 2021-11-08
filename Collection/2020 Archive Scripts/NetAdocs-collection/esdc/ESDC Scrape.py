#!/usr/bin/env python
# coding: utf-8

# ### List of designated educational institutions
# 
# Retrieved from: https://www.canada.ca/en/employment-social-development/programs/designated-schools.html
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import random


# Set up:

opts = Options()
opts.add_argument("user-agent=kt v 1.0")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)

headers = {
    'User-Agent': 'kt 1.0',
    'From': 'khobbs3@uwo.ca'
}


# ---
# 
# Get links to each province table:
r = requests.get('https://www.canada.ca/en/employment-social-development/programs/designated-schools.html', headers=headers)
s = BeautifulSoup(r.text)

links = []
tab = s.find_all('h2')[4].next_sibling.next_sibling
for t in tab.find_all('a'):
    if t.text == 'International List of designated educational institutions':
        pass
    else:
        links.append(t['href'])


# ---
# Selenium click to view all and scrape:
# 
# <mark>NOTE: no data for 'NU',</mark>

links_no_NU = []
for l in links:
    if links[7] != l:
        links_no_NU.append(l)

province = ['AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'ON', 'PE', 'QU', 'SK', 'YU']



for prov, url in zip(province, links_no_NU):
    # TRACK PROGRESS
    print(prov, url)
    driver.get(url)
    
    # SEE ALL
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wb-auto-4_length"]/label/select/option[3]'))).click()
    
    # MAKE DF
    new = pd.read_html(driver.page_source)
    new = new[0]
    new.to_csv('data/education/{}-education.csv'.format(prov))
    
    # SLOW
    time.sleep(random.uniform(2,8))
    
driver.close()

