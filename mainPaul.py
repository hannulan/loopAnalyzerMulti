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
    #fileNameE = '..\Data_fran_deltagare\PaulJaniak\Inlamning1\saukacgm2.herokuapp.com 2019-09-16 - 2019-12-16.json'; 
    #fileNameE = '..\Data_fran_deltagare\IngridSvensson\Inlamning1\entries.json'; 
    
    fileNameE = '..\\Data_fran_deltagare\\DanielJohansson\\Inlamning1\\entries.json'; 
    #fileNameE = '.\Aksel\\test.json'
    #fileNameE = '.\Aksel\\response_entries.json';
    fileNameT = fileNameE; 
    reader = Reader.Reader('Paul', fileNameE, fileNameT);
    reader.readData(); 
    
    reader.createCGMStructure();
    #reader.createCarbStructure();
    #reader.createBolusStructure(); 
    #reader.createBasalRateStructure(); 

    
analyzer = Analyzer.Analyzer('Paul');

# Find all in range

dfCGM   = reader.dfCGM; # Detta är två samma värdne, inte kopior!
#dfBolus = akselReader.dfBolus;
#dfBasal = akselReader.dfBasal;

timeAboveRange_per, timeBelowRange_per, timeInRange_per = analyzer.calcTimeInRange(dfCGM)
timeAboveTarget_per, timeBelowTarget_per, timeInTarget_per = analyzer.calcTimeInTarget(dfCGM)

stdCGM = analyzer.calcStdCGM(dfCGM);

#basalPercentage, bolusPercentage, tot = analyzer.basalBolusPercentage(dfBasal, dfBolus)


## Print all result to the command prompt: 
print('Patient name: ' + 'Paul');

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


#print('------------- Insulin  -------------')
#print('Total delivery:   ' + str(tot))
#print('Basal percentage: ' + str(basalPercentage))
#print('Bolus percentage: ' + str(bolusPercentage))

## Todo:
print('Show MARD')
print('Show PGS')
print('Show GVI')


