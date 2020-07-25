#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:25:47 2020

@author: mattiasbrannstrom
"""



from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya


import datetime as dt
import Reader
import Analyzer

import help_func

treatmentsFile = 'treatments2.json'
entriesFile    = 'entries1_time.json'
name = 'Daniel'
timeCGMStableMin = 20; 

readerTest = Reader.Reader(name, entriesFile, treatmentsFile, timeCGMStableMin);
analyzer = Analyzer.Analyzer(name, readerTest.numDayNight, readerTest.dfCGM, readerTest.dfInsulin, timeCGMStableMin); 

analyzerTime = Analyzer.Analyzer(name, readerTest.numDayNight, readerTest.dfCGM, readerTest.dfInsulin, timeCGMStableMin); 

#Analyzer.Analyzer(name, readerTest.dfCGM); 
analyzerTime.calcAllCGM(); 


## Correct values: 
idxDay_correct = [0, 1, 2, 3, 4, 5]; 
idxNight_correct = [10, 11, 12, 13]; 

## Checks:
nFault2 = 0; 
if analyzerTime.idxDay == idxDay_correct: 
    print('idxDay:      OK')
else: 
    print('idxDay:      NOK')
    nFault2 = nFault2 + 1; 

if analyzerTime.idxNight == idxNight_correct: 
    print('idxNight:    OK')
else: 
    print('idxNight:    NOK')
    nFault2 = nFault2 + 1; 
   
if nFault2 == 0: 
    print("No fault detected --- OK")