#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:14:55 2020

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

# Setting for everyone:
timeCGMStableMin = 20; 


# Beräkning av GVP

treatmentsFile = 'testFiles/treatments2.json'
entriesFile    = 'testFiles/entries1_time.json'
name = 'Daniel'
timeCGMStableMin = 20; 

readerTest = Reader.Reader(name, entriesFile, treatmentsFile, timeCGMStableMin);
analyzer   = Analyzer.Analyzer(name, readerTest.numDayNight, readerTest.dfCGM, readerTest.dfInsulin, timeCGMStableMin); 

#dfCGM = pd.DataFrame(data60); 
dfCGM = readerTest.dfCGM

############## Berakna GVP #######################
deltaCGM = -np.diff(dfCGM['cgm'])

N = len(dfCGM['deltaTimeSec']);

LAll = np.square(dfCGM['deltaTimeSec'][1:N]/60) + np.square(deltaCGM)
LAll = LAll.to_numpy();
LAll = np.sqrt(np.double(LAll));

idx  = dfCGM['deltaTimeSec'] < timeCGMStableMin*60 

L = sum(LAll[idx[1:N]])  # LAll has one element less than dfCGM and hence idx. Due to diff calc of cgm-values

L0All = dfCGM['deltaTimeSec'][1:N]/60
L0 = sum(L0All[idx])

GVP = (L/L0 - 1);
############## END Berakna GVP #######################


############### Beräkna PGS    #########################
GVP = round(GVP, 4)
MG = analyzer.cgmMean*18
PTIR = analyzer.tir; 

logF = analyzer.logisticFunc
counter = analyzer.counter

numWeek = analyzer.numDayNight/7; 
N_54 = counter(dfCGM['cgm'], 54)/numWeek
N_70 = counter(dfCGM['cgm'], 70)/numWeek - N_54; 

F_54 = 0.5 + 4.5*(1 - np.exp(-0.81093*N_54));

if N_70 <= 7.65:
    F_70 = 0.5714*N_70 + 0.625; 
else:
    F_70 = 5;


# Tested N_54 = 2 and 6 
# Tested N_70 = 4 and 6
# Result as plots in reference
# Result:  4.1111107267264435 4.965316895174042
# Result: 2.9106 4.0534

# Tested GVP = 0.40, 0.80 and 1.20
# Result as plots in reference
# Result:  3.0073720738402177 7.037526804202406 9.418170307425285    

# Tested PTIR = 0.1 0.5 0.9
# Result: 9.79357349339474, 6.430987434173073, 1.4639979055645385
# Result as in reference
    
# Tested MG = 50 90 110 190 240
# Result: 9.327081158011563, 2.052595742987335,  1.2302228345542954
#         9.565776416313424, 9.99540476009064

F_GVP  = 1 + 9*logF(100*GVP, 0.049, 65.47)
F_PTIR = 1 + 9*logF(100*PTIR, -0.0833, 55.04)
F_MG   = 1 + 9*logF(MG, -0.1139, 72.08) + 9*logF(MG, 0.09195, 157.57)

PGS = F_54 + F_70 + F_GVP + F_PTIR + F_MG; 

print('F_54: ' + str(F_54) + '\n')
print('F_70: ' + str(F_70) + '\n')
print('F_GVP: ' + str(F_GVP) + '\n')
print('F_PTIR: ' + str(F_PTIR) + '\n')
print('F_MG: ' + str(F_MG) + '\n')
PGSround = round(PGS, 4);
############### END Beräkna PGS    #########################
#reader.createInsulinStructure();

# self.dfTreatments.columns
# Index(['_id', 'amount', 'created_at', 'eventType', 'duration', 'timestamp',
#        'enteredBy', 'rate', 'absolute', 'temp', 'utcOffset', 'carbs',
#        'insulin', 'programmed', 'type', 'unabsorbed', 'reason',
#        'insulinNeedsScaleFactor', 'remoteAddress', 'absorptionTime',
#        'foodType'],
#       dtype='object')

# self.dfTreatments.eventType.unique()
# array(['Temp Basal', 'Correction Bolus', 'Temporary Override',
#        'Sensor Start', 'Meal Bolus', 'Resume Pump', 'Suspend Pump', nan],
#       dtype=object)

# All bolus events: 'Correction Bolus' and 'Meal Bolus'