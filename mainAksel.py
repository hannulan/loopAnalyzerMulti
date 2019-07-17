# -*- coding:
# utf-8 -*-
"""
Created on Mon Jul 15 14:45:08 2019

@author: hannulan
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

if 1:
    # Read data for patient Aksel.
    akselReader = Reader.Reader('.');
    akselReader.readData(); 
    
    akselReader.createCGMStructure();
    akselReader.createCarbStructure();
    akselReader.createBolusStructure(); 
    akselReader.createBasalRateStructure(); 

    
akselAnalyzer = Analyzer.Analyzer('Aksel');

# Find all in range

dfCGM   = akselReader.dfCGM; # Detta är två samma värdne, inte kopior!
dfBolus = akselReader.dfBolus;
dfBasal = akselReader.dfBasal;

timeAboveRange_per, timeBelowRange_per, timeInRange_per = akselAnalyzer.calcTimeInRange(dfCGM)
timeAboveTarget_per, timeBelowTarget_per, timeInTarget_per = akselAnalyzer.calcTimeInTarget(dfCGM)

stdCGM = akselAnalyzer.calcStdCGM(dfCGM);

basalPercentage, bolusPercentage, tot = akselAnalyzer.basalBolusPercentage(dfBasal, dfBolus)


## Print all result to the command prompt: 
print('Patient name: ' + 'Aksel');

print('------------- Time in Range -------------')
print('Time below range: ' + str(timeBelowRange_per))
print('Time in range:    ' + str(timeInRange_per))
print('Time above range: ' + str(timeAboveRange_per))


print('------------- Time in Target -------------')
print('Time below target: ' + str(timeBelowTarget_per))
print('Time in target:    ' + str(timeInTarget_per))
print('Time above target: ' + str(timeAboveTarget_per))

print('------------- Glucose variability -------------')
print('CGM std: ' + str(stdCGM))


print('------------- Insulin  -------------')
print('Total delivery:   ' + str(tot))
print('Basal percentage: ' + str(basalPercentage))
print('Bolus percentage: ' + str(bolusPercentage))

## Todo:
print('Show MARD')
print('Show PGS')
print('Show GVI')


