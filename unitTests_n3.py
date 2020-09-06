# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:54:16 2020

@author: hannu
"""


" Testa basal och bolus strukturerna "
" Testa även TDD "

from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya


import datetime as dt
import Reader
import Analyzer


timeCGMStableMin = 20; 


## Test creation of dfInsulin
# Testa längden
# Testa att första deltaTimeSec är 0
# Kolla att rate är korrekt

# Eventtypes: Temp Basal

ef = 'testFiles/entries_ex_caspian.json';
name = 'Daniel2'
tf = 'testFiles/treatments_ex_nightscoutcaspian_forN3.json'

reader  = Reader.Reader(name, ef, tf, timeCGMStableMin, 'timestamp');
dfInsulinLength_correct = 0


tf2 = 'testFiles/treatments_ex_nightscoutcaspian_forN3_2.json'
reader2  = Reader.Reader(name, ef, tf2, timeCGMStableMin, 'timestamp');
analyzer2 = Analyzer.Analyzer(name, reader2) #.numDayNight,  reader2.booleanWholeDayNight, reader2.dfCGM, reader2.dfInsulin, timeCGMStableMin); 

dfInsulinTest = reader2.dfInsulin; 
length_dfInsulin_test = len(dfInsulinTest)
length_dfTreatments_test = len(reader2.dfTreatments)
tddTest = analyzer2.tdd

# readData removes Sensor start due to timestamp is nan
length_dfTreatments_correct = 16; 
length_dfInsulin_correct = 16; 
tddCorrectBolus = 0.05 + 0.05 + 0.55 + 0.75 + 0.7 + 0.6; 

rateTemp = np.array([0.00, 0.00, 0.95, 0.95, 0.95, 0.95, 0.95, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.30, 0.30, np.nan])
rateTemp[len(rateTemp)-1] = 0; 
dTTemp   = np.array([0, 3900.1, 3899.9, 3900, 2700, 3900.1, 3899.9, 3900, 2700, 3900.1, 3899.9, 3900, 2700, 3900.1, 3899.9, 3900])
dTTemp   = dTTemp/60/60; 
tddCorrectBasal = sum(rateTemp*dTTemp);

tddCorrect = round(tddCorrectBasal + tddCorrectBolus, 4);

dataCorrect = {
'dateTime':
[dt.datetime(2019,10,12,20,55,39),
dt.datetime(2019,10,12,19,50,38),
dt.datetime(2019,10,12,18,45,39),
dt.datetime(2019,10,12,17,40,39),
dt.datetime(2019,10,12,16,55,39),
dt.datetime(2019,10,12,15,50,38),
dt.datetime(2019,10,12,14,45,39),
dt.datetime(2019,10,12,13,40,39),
dt.datetime(2019,10,12,12,55,39),
dt.datetime(2019,10,12,11,50,38),
dt.datetime(2019,10,12,10,45,39),
dt.datetime(2019,10,12, 9,40,39),
dt.datetime(2019,10,12, 8,55,39),
dt.datetime(2019,10,12, 7,50,38),
dt.datetime(2019,10,12, 6,45,39),
dt.datetime(2019,10,12, 5,40,39)
],
'bolus': [ 0,
 0,
0.05,
0.05,
 0,
0.55,
 0,
 0,
0.75,
 0,
 0,
 0,
 0,
0.70,
 0,
0.60],
'rate': [
0.00,
0.00,
0.95,
0.95,
0.95,
0.95,
0.95,
0.45,
0.45,
0.45,
0.45,
0.45,
0.45,
0.30,
0.30,
 np.nan
],
'carbs': [
     0,
 0,
20.0,
 0,
 0,
 0,
 0,
 0,
 0,
30.0,
 0,
 0,
 0,
 0,
 0,
25.0 
],
 'deltaTimeSec': [ # Do not check this
    0,
 390,
 389,
 390,
     0,
 390,
 389,
 390,
     0,
 390,
 389,
 390,
     0,
 390,
 389,
 390]    
 };

dfInsulinCorrect = pd.DataFrame(dataCorrect); 

nFaultN3 = 0; 

if length_dfTreatments_correct == length_dfTreatments_test:
    print('length of dfTreatments:     OK')
else: 
    print('length of dfTreatments:     NOK')
    nFaultN3 = nFaultN3 + 1; 

if length_dfInsulin_correct == length_dfInsulin_test:
    print('length of dfInsulin:        OK')
else: 
    print('length of dfInsulin:        NOK')
    nFaultN3 = nFaultN3 + 1; 
     
if sum(dfInsulinTest['bolus'] == dfInsulinCorrect['bolus']) == length_dfInsulin_correct: 
    print('dfInsulin[bolus] is:        OK')
else:
     print('dfInsulin[bolus] is:      NOK')
     nFaultN3 = nFaultN3 + 1;
 
if sum(dfInsulinTest['carbs'] == dfInsulinCorrect['carbs']) == length_dfInsulin_correct: 
    print('dfInsulin[carbs] is:        OK')
else:
     print('dfInsulin[carbs] is:      NOK')
     nFaultN3 = nFaultN3 + 1;
     
if sum(dfInsulinTest['rate'].isna() == dfInsulinCorrect['rate'].isna()) ==  length_dfInsulin_correct: # Check that values and nan's are correct
    # Replace Nans with zeros:
    insulinCorrectNew = np.array(dfInsulinCorrect['rate']); 
    idx = np.isnan(insulinCorrectNew)
    insulinCorrectNew[idx] = 0;

    insulinTestNew = np.array( dfInsulinTest['rate']); 
    idx = np.isnan(insulinTestNew)
    insulinTestNew[idx] = 0;
    
    if sum(insulinTestNew == insulinCorrectNew) == length_dfInsulin_correct: 
        print('dfInsulin[rate]  is:        OK')
    else: 
        print('dfInsulin[rate]  is:       NOK')
        nFaultN3 = nFaultN3 + 1;
else:
     print('dfInsulin[rate]  is:       NOK')
     nFaultN3 = nFaultN3 + 1;

if tddCorrect == tddTest: 
    print('TDD calc:                      OK')
else: 
    print('TDD calc:                     NOK')
    nFaultN3 = nFaultN3 + 1;     
    
if nFaultN3 == 0:
    print('--- testcase n3, basal and bolus:     OK')
else: 
    print('--- testcase n3, basal and bolus:     NOK')


# TODO: Double check if dfBolus also includes the micro boluses