#!/usr/bin/env python
# coding: utf-8

# ### Creates a database of cities in Canada, primarily for MB, SK, and NB.
# 
# Formatted as: `city 2-letter prov, Canada`

# In[1]:


prov_abbrev = {
              "Alberta": "AB",
              "British Columbia": "BC",
              "Saskatchewan": "SK",
              "Manitoba": "MB",
              "Ontario": "ON",
              "Quebec": "QC",
              "Newfoundland And Labrador": "NL",
              "New Brunswick": "NB",
              "Nova Scotia": "NS",
              "Northwest Territories": "NT",
              "Nunavut": "NU",
              "Prince Edward Island": "PE",
              "Yukon Territory": "YT"}

def complete_address(x):
    """Converts full province name to abbreviated in the reference set.
    Returns full address with changes intended for improved parsing efficacy."""
    for k in prov_abbrev.keys():
        try:
            mach = re.search(k, x)[0]
            return x.replace(mach, prov_abbrev[mach])
        except TypeError:
            pass
    return x


# In[2]:


import pandas as pd
import os
import re

os.chdir('output/childcare/merged/')

# import data
df=pd.read_csv('childcare-merged.csv')
df['source_full_address'] = df['full_address']

# grab list of all cities and provinces used in GoDayCare.com facilities
godc_prov = df.loc[df.provider == 'GoDayCare.com'].province.astype(str).to_list()
godc_cit = df.loc[df.provider == 'GoDayCare.com'].city.astype(str).to_list()

# create unique set of city - province concatenations to reference in full_address for removal
citprovCA = set()
for c,p in zip(godc_cit, godc_prov):
    citprovCA.add("{} {}, {}".format(c,p, "Canada"))
    
reference = set()
for v in citprovCA:
    reference.add(complete_address(v))


# In[3]:


os.getcwd()


# Update reference set with additional cities in MB and SK using NRCAN's list of geographical names databases

# In[4]:


os.chdir('../parsed/references')

mb_names = pd.read_csv('cgn_mb_csv_eng-filtered.csv')
sk_names = pd.read_csv('cgn_sk_csv_eng-filtered.csv')

tempMB = mb_names['Geographical Name'].to_list()
tempSK = sk_names['Geographical Name'].to_list()


for m,s in zip(tempMB, tempSK):
    reference.add("{} MB, Canada".format(m))
    reference.add("{} SK, Canada".format(s))


# Update reference set with manually observed cities in data

# In[9]:


# Manitoba
reference.add('St Andrews MB, Canada')
reference.add('Shilo  MB, Canada')
reference.add('St.Malo MB, Canada')
reference.add('St. Jean-Baptiste MB, Canada')
reference.add('Landmark  MB, Canada')
reference.add('Elm Creek  MB, Canada')
reference.add('St. Francois Xavier MB, Canada')
reference.add('Ste Anne  MB, Canada')
reference.add('LaBroquerie MB, Canada')
reference.add('Ile Des Chenes MB, Canada')
reference.add('St. Pierre Jolys MB, Canada')
reference.add('Binscarth  MB, Canada')
reference.add('Pine Falls MB, Canada')
reference.add('Oak Bluff  MB, Canada')
reference.add('Lockport  MB, Canada')
reference.add('Swan River MB, Canada')
reference.add('Ste. Agathe MB, Canada')
reference.add('The Pas MB, Canada')
reference.add('Thompson MB, Canada')
reference.add('Lake MB, Canada')
reference.add('Virden MB, Canada')
reference.add('Stony Mountain MB, Canada')
reference.add('Gladstone  MB, Canada')
reference.add('Sanford MB, Canada')
reference.add('Brandon MB, Canada')
reference.add('Winkler MB, Canada')
reference.add('Adolphe MB, Canada')
reference.add('St Paul MB, Canada')
reference.add('Winnipeg  MB, Canada')
reference.add('Winnpeg  MB, Canada')
reference.add('Headingley  MB, Canada')
reference.add('St Claude MB, Canada')
reference.add('Ste Rose Du Lac MB, Canada')
reference.add('St Francois Xavier MB, Canada')
reference.add('St Jean Baptiste MB, Canada')
reference.add('StMalo MB, Canada')
reference.add('St Jean Baptiste MB, Canada')
reference.add('Grunthal  MB, Canada')
reference.add('Ebb & Flow MB, Canada')
reference.add('Ste Agathe MB, Canada')
reference.add('St Georges MB, Canada')
reference.add('St Pierre Jolys MB, Canada')
reference.add('St Laurent MB, Canada')
reference.add('Carooman MB, Canada')
reference.add('St Eustache MB, Canada')


# Saskatchewan
reference.add('Stoughton SK., Canada')
reference.add('Saskatoon SK SK, Canada')
reference.add('Saskatoon Sask, Canada')
reference.add('Bellevue SK, Canada')
reference.add('Prince Albert SK S6V OM9, Canada')
reference.add('Lanigan SK SOK 2M0, Canada')
reference.add('Ile a la Crosse SK, Canada')
reference.add('Theordore SK, Canada')
reference.add('Emerald Park SK, Canada')
reference.add('Fort QuAppelle SK, Canada')
reference.add('Louis SK, Canada')
reference.add('Whitecap SK, Canada')
reference.add('Rosthern SK, Canada')
reference.add('Wakaw SK, Canada')
reference.add('Lake Lenore SK, Canada')
reference.add('Shellbrook SK, Canada')
reference.add('LeRoy SK, Canada')
reference.add('Wilkie SK, Canada')
reference.add('Watson SK, Canada')
reference.add('Strasbourg SK, Canada')
reference.add('Unity SK, Canada')
reference.add('Edam SK, Canada')
reference.add('Stewart Valley SK, Canada')
reference.add('Cabri SK, Canada')
reference.add('Success SK, Canada')
reference.add('Kelliher SK, Canada')
reference.add('Nipawin SK, Canada')
reference.add('Hazlet SK, Canada')
reference.add('Porcupine Plain SK, Canada')
reference.add('Porcupine Plain SK, Canada')
reference.add('Ituna SK, Canada')
reference.add('Paradise Hill SK, Canada')
reference.add('Meadow Lake SK, Canada')
reference.add('Fort Qu\'appelle SK, Canada')
reference.add('Gravelbourg SK, Canada')
reference.add('McLean SK, Canada')
reference.add('Gull Lake SK, Canada')
reference.add('Lafleche SK, Canada')
reference.add('Indian Head SK, Canada')
reference.add('Limerick SK, Canada')
reference.add('Stoughton SK, Canada')
reference.add('Sturgis SK, Canada')
reference.add('Canora SK, Canada')
reference.add('Ferland SK, Canada')
reference.add('Hudson Bay SK, Canada')
reference.add('Wolseley SK, Canada')
reference.add('Montmartre SK, Canada')
reference.add('Ogema SK, Canada')
reference.add('Pangman SK, Canada')
reference.add('Grenfell SK, Canada')
reference.add('Pelly SK, Canada')
reference.add('Kamsack SK, Canada')
reference.add('Saltcoats SK, Canada')
reference.add('Radville SK, Canada')
reference.add('La Ronge SK, Canada')
reference.add('Esterhazy SK, Canada')
reference.add('Kipling SK, Canada')
reference.add('Consul SK, Canada')
reference.add('Pinehouse SK, Canada')
reference.add('Wapella SK, Canada')
reference.add('Rocanville SK, Canada')
reference.add('Creighton SK, Canada')
reference.add('Oxbow SK, Canada')
reference.add('Carnduff SK, Canada')
reference.add('La Loche SK, Canada')
reference.add('Warooman SK, Canada')
reference.add('Southey SK, Canada')
reference.add('Qu\'Appelle SK, Canada')

# NB
reference.add('Saint-Basile NB, Canada')
reference.add('Cap-Pel NB, Canada')
reference.add('Hanwell NB, Canada')
reference.add('Saint-Isidore NB, Canada')
reference.add('Saint-Jacques NB, Canada')
reference.add('Douglas NB, Canada')
reference.add('Grand Barachois NB, Canada')
reference.add('Sainte Marie Saint Raphal NB, Canada')
reference.add('Kingston NB, Canada')
reference.add('Centreville NB, Canada')
reference.add('Harvey Station NB, Canada')
reference.add('Charlotte Co NB, Canada')
reference.add('Sheila NB, Canada')
reference.add('Steeves Mountain NB, Canada')
reference.add('Saint Joseph de Madawaska NB, Canada')
reference.add('Saint Jacques NB, Canada')
reference.add('Kedgwick NB, Canada')
reference.add('Hillsborough NB, Canada')
reference.add('Shediac Cape NB, Canada')
reference.add('Grand Sault/Grand Falls NB, Canada')
reference.add('Drummond NB, Canada')
reference.add('dsl de Drummond NB, Canada')
reference.add('Saint Irene NB, Canada')
reference.add('Keswick Ridge NB, Canada')
reference.add('Nashwaak Village NB, Canada')
reference.add('Stephen NB, Canada')
reference.add('Andover NB, Canada')
reference.add('Noonan NB, Canada')
reference.add('Saint Basile NB, Canada')
reference.add('Robertville NB, Canada')

reference.add('Westfield NB, Canada')
reference.add('Grand Bay Westfield NB, Canada')

reference.add('Robertville NB, Canada')
reference.add('Bedell NB, Canada')
reference.add('Burtts Corner NB, Canada')
reference.add('Richibucto Road NB, Canada')
reference.add('St Stephen NB, Canada')
reference.add('Blacks Harbour NB, Canada')
reference.add('Saint Andr NB, Canada')
reference.add('Waasis NB, Canada')
reference.add('Saint Lonard NB, Canada')
reference.add('Riverside Albert NB, Canada')
reference.add('Elsipogtog First Nation NB, Canada')
reference.add('Richibucto Road NB, Canada')
reference.add('Noonan NB, Canada')
reference.add('Perth Andover NB, Canada')
reference.add('Saint Antoine NB, Canada')
reference.add('Petit Rocher NB, Canada')
reference.add('Saint Quentin NB, Canada')
reference.add('Nguac NB, Canada')
reference.add('St Simon NB, Canada')
reference.add('Grande Digue NB, Canada')
reference.add('Sainte Anne de Madawaska NB, Canada')
reference.add('Petite Lamque NB, Canada')
reference.add('Lamque NB, Canada')##
reference.add('Saint Basile NB, Canada')
reference.add('Eel River Crossing NB, Canada')
reference.add('Dundee NB, Canada')
reference.add('Cap Pel NB, Canada')
reference.add('Sainte Marie de Kent NB, Canada')
reference.add('Saint Franois de Madawaska NB, Canada')
reference.add('Pointe Brle NB, Canada')##
reference.add('Saint Isidore NB, Canada')
reference.add('DSL de Grand Sault/Falls NB, Canada')
reference.add('Pointe Sapin NB, Canada')
reference.add('Geary NB, Canada')
reference.add('Val d\'Amour NB, Canada')
reference.add('Pont Landry NB, Canada')
reference.add('Scoudouc NB, Canada')
reference.add('Sainte Rose NB, Canada')
reference.add('Le Goulet NB, Canada')
reference.add('Verte NB, Canada')
reference.add('Lincoln NB, Canada')
reference.add('Burton NB, Canada')
reference.add('Wilsons Beach NB, Canada')
reference.add('Kingsclear First Nation NB, Canada')
reference.add('Sunny Corner NB, Canada')
reference.add('Saint Louis De Kent NB, Canada')
reference.add('Sainte Anne de Kent NB, Canada')
reference.add('Shediac Bridge NB, Canada')
reference.add('Grande Anse NB, Canada')
reference.add('Sainte Anne Gloucester Co NB, Canada')
reference.add('Baie Sainte Anne NB, Canada')
reference.add('Rivire La Truite NB, Canada')
reference.add('Dorchester NB, Canada')
reference.add('Sunny Corner NB, Canada')
reference.add('Roachville NB, Canada')
reference.add('Madawaska Maliseet First Nation NB, Canada')
reference.add('Hainesville NB, Canada')

reference.add('Sunbury NB, Canada')
reference.add('Waterville Sunbury NB, Canada')

reference.add('Debec NB, Canada')
reference.add('Mactaquac NB, Canada')
reference.add('Saint Andrews NB, Canada')
reference.add('Riverbank NB, Canada')
reference.add('Bath NB, Canada')
reference.add('Pine Glen NB, Canada')
reference.add('Apohaqui NB, Canada')
reference.add('Gagetown NB, Canada')
reference.add('Plaster Rock NB, Canada')
reference.add('St George NB, Canada')
reference.add('Tracadie Beach NB, Canada')

############# NB lameque --> lamque???, pointe brule --> point brle ??

# QC
reference.add('Quèbec Qc, Canada')
reference.add('Quèbec QC, Canada')
reference.add('Ste Genevieve QC, Canada')
reference.add('Notre Dame du Bon Conseil QC, Canada')
reference.add('Trois Rivières QC, Canada')

# NL
reference.add('Grand Falls Windsor NL, Canada')

# ON
reference.add('Clarence-rockland ON, Canada')
reference.add('Sharon east gwillimbury ON, Canada')
reference.add('Woodbridge ON, Canada')

# BC
reference.add('Lantzville Lantzville BC, Canada')
reference.add('Richmond Richmond BC, Canada')
reference.add('Burnaby BC, Canada')


# In[10]:


ref = pd.DataFrame([r for r in reference], columns=["cityprov"])
ref.replace({'\.': ''}, regex = True, inplace = True)
ref.replace({'-': ' '}, regex = True, inplace = True)
ref.to_csv('reference.csv')


# In[ ]:




