#!/usr/bin/env python
# coding: utf-8

# ### Alberta
# 
# Retrieved from: https://open.alberta.ca/opendata/childcareinformation


import numpy as np
import pandas as pd


ab = pd.read_csv('https://open.alberta.ca/dataset/e4ecb4fa-28b5-4abb-8c32-b2a76d2a6ee0/resource/e89a46f3-e4ec-41a3-8086-026a2c14e24c/download/open-data-portal-202003.csv')



ab.to_csv('data/childcare/AB-childcare.csv', encoding = "utf-8")


