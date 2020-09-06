# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:54:16 2020

@author: hannu
"""


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
dfCGM = reader2.dfCGM; 
dfInsulin = reader2.dfInsulin; 

reader2Simple  = Reader.Reader(patientName = name, fileNameEntries = ef, fileNameTreatments = tf2, 
                               timeCGMStableMin = timeCGMStableMin, timeStrTreatments = 'timestamp',
                               runSimple = True, dfCGMIn = dfCGM, dfInsulinIn = dfInsulin, 
                               numDayNightIn = 1, booleanWholeDayNightIn = True);

analyzer2 = Analyzer.Analyzer(name, reader2Simple) #.numDayNight,  reader2.booleanWholeDayNight, reader2.dfCGM, reader2.dfInsulin, timeCGMStableMin); 

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


nFaultN5 = 0; 
if tddCorrect == tddTest: 
    print('TDD calc:                      OK')
else: 
    print('TDD calc:                     NOK')
    nFaultN5 = nFaultN5 +1; 
    
if nFaultN5 == 0:
    print('--- testcase n3, basal and bolus:     OK')
else: 
    print('--- testcase n3, basal and bolus:     NOK')


# TODO: Double check if dfBolus also includes the micro boluses