#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
#
# ### Manitoba Child Care
# Retrieved from: https://childcaresearch.gov.mb.ca
#
# Robots: not found.
#
# <mark> N.B. (From website) * We have not published the names and addresses of Family and Group Facilities for security reasons. Please contact these facilities for further information including their location. </mark>

# %%
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
from datetime import datetime


# %% [markdown]
# ##### Log file:

# %%
logfile = open('mb.log', 'a')
logfile.write('{} mb.py execution by Kaitlyn Hobbs.\n'.format(datetime.now()))

# %%
# os.system("java -jar /usr/local/bin/selenium-server-standalone-3.141.59.jar")
opts = Options()
opts.add_argument("user-agent=Statistics Canada bot created by Kaitlyn Hobbs (kaitlyn.hobbs@statcan.gc.ca)")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)


# %% [markdown]
# ##### Functions:

# %%
def scrollToBottom():
    """
    Scrolls to bottom of page with endless scrolling.
    Detects when page height does not change after scroll.
    https://stackoverflow.com/questions/63647849/scroll-to-the-end-of-the-infinite-loading-page-using-selenium-python
    """
    # Get scroll height after first time page load
    counter = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Log scroll
        logfile.write('{} Scroll to bottom of page.\n'.format(datetime.now()))
        
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Scrolled {} times.".format(counter))
            break
    
        counter += 1
        last_height = new_height
        
        


# %% [markdown]
# ##### Execute Scrape:
# <mark> Subject to modification after testing.</mark>

# %%
domain = 'https://childcaresearch.gov.mb.ca'
driver.get(domain)
logfile.write('{} Connected to {}.\n'.format(datetime.now(), domain))

scrollToBottom()

elems = driver.find_elements_by_class_name("child-care-facility")
links = [elem.get_attribute('href') for elem in elems]

# %%
# Navigate through links to each facility page to find detailed information:
name = []
source_type = []
phone = []
email = []
address = []
infant = []
toddler = []
schoolage = []

for l in links:
    driver.get(domain + l)
    logfile.write('{} Navigated to {}.\n'.format(datetime.now(), domain + l))
    
    # Grab elements
    logfile.write('{} Collecting data for: {}.\n'.format(datetime.now(), 
                  driver.find_element_by_class_name("child-care-facility-name").text))
    name.append(driver.find_element_by_class_name("child-care-facility-name").text)
    source_type.append(driver.find_element_by_class_name("child-care-facility-type").text)
    phone.append(driver.find_element_by_class_name("child-care-facility-phone-number").text)
    email.append(driver.find_element_by_class_name("child-care-facility-email").text)
    address.append(driver.find_element_by_class_name("child-care-facility-address").text)
    
    # Only relevant ages are visible text -- note for cleaning
    infant.append(driver.find_element_by_class_name("allow0to2").text)
    toddler.append(driver.find_element_by_class_name("allow2to6").text)
    schoolage.append(driver.find_element_by_class_name("allow6to12").text)
    
    # Wait between urls
    time.sleep(random.randint(5,15))


# %%
driver.close()

# %% [markdown]
# ##### Consolidate, Clean & Export:

# %%
#TODO


# %%
df.to_csv("data/MB-childcare.csv")

# Log & close
logfile.write("{} Fin.\n\n".format(datetime.now()))
logfile.close()

