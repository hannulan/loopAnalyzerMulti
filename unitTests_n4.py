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

import help_func

## Unit tests: 

# Reader: 
# readData
# createCGM

treatmentsFile = 'testFiles/treatments2.json'
entriesNoTL    = 'testFiles/entries10.json'
entriesTL      = 'testFiles/entries11.json'

name = 'Daniel'

dfCGM = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec'])

dfInsulin = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'deltaTimeSec'])

numDayNight = 1;
timeCGMStableMin = 20; 
booleanWholeDayNight= True
    
data100 = {
'dateTime':
[dt.datetime(2019,10,12,20,55,39),
dt.datetime(2019,10,12,19,50,38),
dt.datetime(2019,10,12,18,45,39),
dt.datetime(2019,10,12,17,40,39),
dt.datetime(2019,10,12,16,35,38),
dt.datetime(2019,10,12,15,30,39)],
'cgm': [
156,
 90,
 80,
 75,
 75,
 75],
 'deltaTimeSec': [
    0,
 390,
 389,
 390,
 390,
 389]    
 };
# 100% tir
tirCorrect100 = 1
PGS_correct100 = 14.2031        
GVP_correct100 = 2.0622

dfCGMTL = pd.DataFrame(data100); 
analyzerTL = Analyzer.Analyzer(name, numDayNight, booleanWholeDayNight, dfCGMTL, dfInsulin, timeCGMStableMin); 
tirTest100 = analyzerTL.calcTimeInXNew(dfCGMTL, analyzerTL.tirLevel, '[]')  # [3.9 10]
PGSTest100 = analyzerTL.cgmPGS
GVPTest100 = analyzerTL.cgmGVP

    
data60 = {
'dateTime':
[dt.datetime(2019,10,12,20,55,39),
dt.datetime(2019,10,12,19,50,38),
dt.datetime(2019,10,12,18,45,39),
dt.datetime(2019,10,12,17,40,39),
dt.datetime(2019,10,12,16,35,38),
dt.datetime(2019,10,12,15,30,39)],
'cgm': [
156,
 90,
 80,
 75,
 60,
 60],
 'deltaTimeSec': [
    0,
 390,
 389,
 390,
 390,
 389]    
 };   
    # 60% tir, 1169/1948 
tirCorrect60 = 0.6001
PGS_correct60  = 22.1311
GVP_correct60  = 2.3656

dfCGMTL = pd.DataFrame(data60); 
analyzerTL = Analyzer.Analyzer(name, numDayNight, booleanWholeDayNight, dfCGMTL, dfInsulin, timeCGMStableMin); 
tirTest60 = analyzerTL.calcTimeInXNew(dfCGMTL, analyzerTL.tirLevel, '[]')  # [3.9 10]
PGSTest60 = analyzerTL.cgmPGS
GVPTest60 = analyzerTL.cgmGVP


dataNotInRangeTL = {
'dateTime':
[dt.datetime(2019,10,12,20,55,39),
dt.datetime(2019,10,12,19,50,38),
dt.datetime(2019,10,12,18,45,39),
dt.datetime(2019,10,12,17,40,39),
dt.datetime(2019,10,12,16,35,38),
dt.datetime(2019,10,12,15,30,39)],
'cgm': [
156,
 90,
 80,
 75,
 60,
 60],
 'deltaTimeSec': [
    0,
 390,
 389,
 390,
 390,
 3890]    
 }; 
# 1169/(1169+390+1200) = 1169/2769 = 0.4237
tirCorrectNotInRangeTL = 0.4237;
PGS_correctNotInRangeTL = 25.2278
GVP_correctNotInRangeTL = 2.9558

#readerTL = Reader.Reader(name, entriesTL, treatmentsFile,  timeCGMStableMin);
dfCGMTL = pd.DataFrame(dataNotInRangeTL); 
analyzerTL = Analyzer.Analyzer(name, numDayNight, booleanWholeDayNight, dfCGMTL, dfInsulin, timeCGMStableMin); 
tirTestNotInRangeTL = analyzerTL.calcTimeInXNew(dfCGMTL, analyzerTL.tirLevel, '[]')  # [3.9 10]
PGSTestNotInRangeTL = analyzerTL.cgmPGS
GVPTestNotInRangeTL = analyzerTL.cgmGVP


dataTLAll = {
'dateTime':
[dt.datetime(2019,10,12,20,55,39),
dt.datetime(2019,10,12,19,50,38),
dt.datetime(2019,10,12,18,45,39),
dt.datetime(2019,10,12,17,40,39),
dt.datetime(2019,10,12,16,35,38),
dt.datetime(2019,10,12,15,30,39)],
'cgm': [
156,
 90,
 80,
 75,
 75,
 75],
 'deltaTimeSec': [
    0,
 3901,
 3899,
 3900,
 3901,
 3899]    
 };
tirCorrectTLAll = 1; 
PGS_correctTLAll = -1
GVP_correctTLAll = -1
    
dfCGMTL = pd.DataFrame(dataTLAll); 
analyzerTL = Analyzer.Analyzer(name, numDayNight, booleanWholeDayNight, dfCGMTL, dfInsulin, timeCGMStableMin); 
tirTestTLAll = analyzerTL.calcTimeInXNew(dfCGMTL, analyzerTL.tirLevel, '[]')  # [3.9 10]
PGSTestTLAll = analyzerTL.cgmPGS
GVPTestTLAll = analyzerTL.cgmGVP

dataTL = {
'dateTime':
[dt.datetime(2019,10,12,20,55,39),
dt.datetime(2019,10,12,19,50,38),
dt.datetime(2019,10,12,18,45,39),
dt.datetime(2019,10,12,17,40,39),
dt.datetime(2019,10,12,16,35,38),
dt.datetime(2019,10,12,15,30,39)],
'cgm': [
156,
 90,
 60,
 75,
 75,
 75],
 'deltaTimeSec': [
    0,
 390,
 3899,
 391,
 3901,
 3899]    
 };
    # (390+391+1200+1200)/(390+1200+391+1200+1200) = 3181/4381
tirCorrectTL = 0.7261; 
PGS_correctTL = 20.0333
GVP_correctTL = 5.3514

    
dfCGMTL = pd.DataFrame(dataTL); 
analyzerTL = Analyzer.Analyzer(name, numDayNight, booleanWholeDayNight, dfCGMTL, dfInsulin, timeCGMStableMin); 
tirTestTL = analyzerTL.calcTimeInXNew(dfCGMTL, analyzerTL.tirLevel, '[]')  # [3.9 10]
PGSTestTL = analyzerTL.cgmPGS
GVPTestTL = analyzerTL.cgmGVP

######## Checks ##########
## Checks TIR: 
nFault4 = 0; 
if tirTest100 == tirTest100: 
    print('TIR test 100:          OK')
else: 
    print('TIR test 100: NOK')
    nFault4 = nFault4 + 1; 

if tirTest60 == tirTest60: 
    print('TIR test 60:           OK')
else: 
    print('TIR test 60: NOK')
    nFault4 = nFault4 + 1;
    
if tirTestNotInRangeTL == tirTestNotInRangeTL: 
    print('TIR test NotInRangeTL: OK')
else: 
    print('TIR test NotInRangeTL: NOK')
    nFault4 = nFault4 + 1; 

if tirTestTLAll == tirTestTLAll: 
    print('TIR test TLAll:        OK')
else: 
    print('TIR test TLAll: NOK')
    nFault4 = nFault4 + 1;     
    
if tirTestTL == tirTestTL: 
    print('TIR test TL:           OK')
else: 
    print('TIR test TL: NOK')
    nFault4 = nFault4 + 1; 

## Checks PGS and GVP
nFault4var = 0; 

if PGS_correct100 == PGSTest100 and GVP_correct100 == GVPTest100:
    print('PGS and GVP 100:   OK')
else: 
    nFault4var = nFault4var + 1; 
    print('PGS and GVP 100:  NOK')     

if PGS_correct60 == PGSTest60 and GVP_correct60 == GVPTest60:
    print('PGS and GVP 60:   OK')
else: 
    nFault4var = nFault4var + 1; 
    print('PGS and GVP 60:  NOK')     
    
if PGS_correctNotInRangeTL == PGSTestNotInRangeTL and GVP_correctNotInRangeTL == GVPTestNotInRangeTL:
    print('PGS and GVP NotInRangeTL:   OK')
else: 
    nFault4var = nFault4var + 1; 
    print('PGS and GVP NotInRangeTL:  NOK')     
    
if PGS_correctTLAll == PGSTestTLAll and GVP_correctTLAll == GVPTestTLAll:
    print('PGS and GVP TLAll:   OK')
else: 
    nFault4var = nFault4var + 1; 
    print('PGS and GVP TLALl:  NOK')     

if PGS_correctTL == PGSTestTL and GVP_correctTL == GVPTestTL:
    print('PGS and GVP TL:   OK')
else: 
    nFault4var = nFault4var + 1; 
    print('PGS and GVP TL:  NOK')     

print('\n')
    

if nFault4 == 0:
    print('--- All TimeLim tests are:  OK')
else:
    print('--- All TimeLim tests are: NOK')
    
if nFault4var == 0: 
    print('--- All PGS and GVP values:  OK')
else:
    print('--- All PGS and GVP values: NOK')
