# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 22:53:07 2021

@author: hannu
"""

from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya

import csv 
import datetime as dt

import Reader
import Analyzer
import ReaderMedtronic

## Ladda spydata fil först: 
# fn = 'C:\Users\hannu\Dropbox\Diassist_OpenAPS_study\Data_fran_deltagare\Resultat\DIY/diy_11.spydata


cc =['name', 'tir', 'tit', 'tihyperLevel1', 'tihyperLevel2', 'tihypoLevel1', 'tihypoLevel2', 'cgmMean', 'cgmSD', 'cgmSCV', 'cgmSDDay', 'cgmSDNight', 'tihypoDagLevel1', 'tihypoDagLevel2', 'tihypoNattLevel1', 'tihypoNattLevel2', 'tirDag', 'tirNatt', 'tdd', 'antal_dagar']
   

dataList = list();
for nn in range(0, len(analyzerList)):
    data1 = analyzerList[nn].getResult()
    data = data1[0]
    dataList.append(data)


df = pd.DataFrame(dataList, columns = cc)
df.to_csv('allDIY.csv', sep = ';', decimal= ",")
