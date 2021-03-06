#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:13:35 2020

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

## Unit tests: 

# Reader: 
# readData
# createCGM

treatmentsFile = 'testFiles/treatments2.json'
entriesFile    = 'testFiles/entries5.json'
name = 'Daniel'
# Datum: 2019-10-11 2019-10-13
numDayNight = 2;
timeCGMStableMin = 20; 


pd.set_option('mode.chained_assignment', None)

daniel1T = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments1011-1211_forstaOmgangen.json'
danielJohanssonEntry1 = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanilEntries_forstaOmgangen.json'


readerTest = Reader.Reader(name, entriesFile, treatmentsFile,  timeCGMStableMin, 'timestamp');
analyzer = Analyzer.Analyzer(name, readerTest);
analyzer.calcAllCGM(); 
#analyzer.calcAllInsulin();
#analyzer.writeAll();

#readerTest.calcAllCGM()

length_correct = 27; 
meanCGM_correct = 9.2572;
stdCGM_correct = 4.5576; 
tir_correct = 0.3846;
tiHyperLevel2Value_correct = 0.2308
tiHypoLevel2Value_corret = 0.0769; 

# Checks
print('\n')
nFault = 0; 

if len(analyzer.dfCGM) == length_correct:
    print('Length  OK: ' + str(len(analyzer.dfCGM)))
else: 
    print('Length NOK: ' + str(len(analyzer.dfCGM)))
    nFault = nFault + 1; 
if analyzer.cgmMean == meanCGM_correct: 
    print('meanCGM OK')
else: 
    print('meanCGM NOK')
    nFault = nFault + 1; 
if analyzer.cgmSD == stdCGM_correct: 
    print('stdCGM  OK')
else: 
    print('stdCGM NOK')
    nFault = nFault + 1; 

if analyzer.tir == tir_correct: 
    print('tir:     OK')
else: 
    print('tir:     NOK')
    nFault = nFault + 1; 
if analyzer.tihyperLevel2Value == tiHyperLevel2Value_correct: 
    print('tihyperLevel2Value:     OK')
else: 
    print('tihyperLevel2Value:     NOK')
    nFault = nFault + 1; 

if analyzer.tihypoLevel2Value == tiHypoLevel2Value_corret:
    print('tiHypoLevel2Value:      OK')
else:
    print('tiHypoLevel2Value:      NOK')
    nFault = nFault + 1; 
    
print('\n')

## Check that all intervalls are correct: 
tirLevel_correct = [18*x for x in [3.9, 10]];
titLevel_correct = [18*x for x in [4, 8]];

rangeHyperLevel1_correct = [18*x for x in [10, 13.9]];
rangeHyperLevel2_correct = [18*13.9];

rangeHypoLevel1_correct = [18*x for x in [3, 3.8]];
rangeHypoLevel2_correct = [18*3];

if analyzer.tirLevel == tirLevel_correct:
    print('tirLevel: OK')
else:
    print('tirLevel: NOK')
    nFault = nFault + 1; 
    
if analyzer.tirLevel == tirLevel_correct:
    print('titLevel: OK')
else:
    print('titLevel: NOK')
    nFault = nFault + 1; 
    
if analyzer.rangeHyperLevel1 == rangeHyperLevel1_correct:
    print('rangeHyperLevel1: OK')
else:
    print('rangeHyperLevel1_correct: NOK')
    nFault = nFault + 1; 
    
if analyzer.rangeHyperLevel2 == rangeHyperLevel2_correct:
    print('rangeHyperLevel2: OK')
else:
    print('rangeHyperLevel2_correct: NOK')
    nFault = nFault + 1; 

if analyzer.rangeHypoLevel1 == rangeHypoLevel1_correct:
    print('rangeHypoLevel1: OK')
else:
    print('rangeHypoLevel1_correct: NOK')
    nFault = nFault + 1; 

if analyzer.rangeHypoLevel2 == rangeHypoLevel2_correct:
    print('rangeHypoLevel2: OK')
else:
    print('rangeHypoLevel2_correct: NOK')
    nFault = nFault + 1; 


if nFault == 0: 
    print("No error detected --- OK")
