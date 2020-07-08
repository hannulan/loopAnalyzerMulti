# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:40:46 2019

@author: hannulan
"""

from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya


import datetime as dt
datafile_entries = './response_entries.json'; 
datafile_treatments = 'response_treatments.json';

#io = StringIO(datafile_response);

#json.load(io)
#json.load(datafile_response);

# https://www.programiz.com/python-programming/json

#file = open(datafile_response);

# NOK:
#dd = dict
#dd = json.load(file)

#ss = str
#ss = json.load(file)


# Från mitt nightscout: 

# Från Davids dotter. 
respTr = requests.get('https://whooze.herokuapp.com/api/v1/treatments')
if respTr == 200: 
    print('ok')
else:
    print('nok')
    
dfTreatmentsDavid = pd.DataFrame.from_dict(respTr.json());

respEn = requests.get('https://whooze.herokuapp.com/api/v1/entries')
if respEn == 200: 
    print('ok')
else:
    print('nok')
#dfResponseDavid = pd.DataFrame.from_dict(respEn.json());

# Fran Henriks filer:  
entries = [];
entries = json.load(open(datafile_entries))

treatments = [];
treatments = json.load(open(datafile_treatments));

# Get treatments from Nightscout account instead: 
# I webläsare: https://whooze.herokuapp.com/api/v1/treatments

# Find all timestamp in treatments: 

for ii in range(0, 2): #len(treatments)-1):
    print(ii)
    print(treatments[ii]['timestamp'])
    
dfEntries = pd.DataFrame.from_dict(entries)
dfTreatments = pd.DataFrame.from_dict(treatments)


dfCGM = pd.DataFrame(columns=['dateTime', 'cgm'])
dfCGM['cgm']


dfCGM['cgm'] = dfEntries['sgv'] 

tt = '2019-04-10T11:15:31.000Z'

tr = '2019-04-10 11:15:31.000'
date_time_obj = dt.datetime.strptime(tr, '%Y-%m-%d %H:%M:%S.%f')


#date_time_obj = dt.datetime.strptime(tt, '%Y-%m-%d %H:%M:%S.%f')
#date_time_obj = dt.datetime.strptime(tt, '%Y-%m-%dT%H:%M:%S.%fZ')

for ii in range(len(dfEntries['dateString'])):
    dfCGM['dateTime'] = dt.datetime.strptime(dfEntries['dateString'][ii], '%Y-%m-%dT%H:%M:%S.%fZ')


# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
#print(data)

my_dict = {"one": 1, "two": 2, "three": 3}
my_dict["one"] # return 1

print('hej') 
2019,4,12,
tt= dt.datetime(2019,4,12,13,59,57)- dt.datetime(2019,4,12,13,55,31)

