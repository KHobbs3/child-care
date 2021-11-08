#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd


# ### Ontario
# Retrieved from: https://data.ontario.ca/dataset/licensed-child-care-facilities-in-ontario


on = pd.read_excel('https://data.ontario.ca/dataset/7efd8b4b-cc63-4337-a551-c940a346605b/resource/d2144297-fc60-4472-b954-e577d1f1a3fb/download/child_care_facilities_open_data_feb2020.xlsx')
ondict = pd.read_excel('https://files.ontario.ca/lccf_-_data_dictionary_en_fr.xlsx')

on.to_csv('data/childcare/ON-childcare.csv', encoding = "utf-8")
ondict.to_csv('data/childcare/ON-childcare-dictionary.csv', encoding = "utf-8")

