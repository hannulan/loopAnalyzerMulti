# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:13:16 2021

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

fn = 'temp_medtronic.csv';

df = pd.DataFrame();

dfRead = pd.read_csv(fn,  sep=';', header = 6);
dfCGM   = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec']);
dfInsulin = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'deltaTimeSec'])

index = dfRead['Index'].to_list()
time = dfRead['Time'].to_list()
date = dfRead['Date'].to_list()
cgm  = dfRead['Sensor Glucose (mmol/L)']
bolus = dfRead['Bolus Volume Delivered (U)']
rate = dfRead['Basal Rate (U/h)']

firstBool = True
dateTimeListInsulin = list(); 



bolusList = list();
rateList = list();
deltaTimeSecListInsulin = list();
#### Insluin ####

#for jj in range(0, len(tt)-1):
firstIndexInsulin = 0; 
for jj in range(0, len(date)-1):
#for jj in range(len(date)-1-1, -1, -1):    
    #print("jj: " + str(jj)  
    try:
        dateTimeString = str(date[jj]) + ' ' + str(time[jj]);
        #print("dateTimeString: " + dateTimeString)
        tempDateTime = dt.datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S"); 
        dateTimeListInsulin.append(tempDateTime)
        if jj == 0:
            deltaTimeSec = 0;
            lastTime = tempDateTime;
        else:
            deltaTimeSecTemp = lastTime - tempDateTime; 
            deltaTimeSec = deltaTimeSecTemp.total_seconds()
            lastTime = tempDateTime; 
        deltaTimeSecListInsulin.append(deltaTimeSec)
        bolusString = str(bolus[jj])
        bolusFloat = float(bolusString.replace(',', '.'))
        bolusList.append(bolusFloat)
        
        rateString = str(rate[jj])
        rateFloat = float(rateString.replace(',', '.'))
        rateList.append(rateFloat)
    except:    
        print("jj: " + str(jj))
        nextPart = jj
        break
    
# Remove nan in bolus list and replace with 0
# Add basal rate (in U/hour) to every row
# Does not change any order
lastIndexInsulin = nextPart - 1;
rateCurrent = 0; 
for rr in range(lastIndexInsulin, firstIndexInsulin-1, -1):
    if bolusList[rr] > 0:
        bb = 2;
    else:
        bolusList[rr] = 0; 
        
    if rateList[rr] > -1:
        rateCurrent = rateList[rr]
    else:
        rateList[rr] = rateCurrent;
        
nextPart = nextPart + 3
countNan = 0
cgmList = list(); 
dateTimeListCGM = list(); 
deltaTimeSecList = list();

for kk in range(nextPart, len(date)-1):
    try:

        dateTimeString = str(date[kk]) + ' ' + str(time[kk]);
        #print("dateTimeString: " + dateTimeString)
        tempDateTime = dt.datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S"); 
        if kk == nextPart:
            deltaTimeSec = 0;
            lastTime = tempDateTime;
        else:
            deltaTimeSecTemp = lastTime - tempDateTime; 
            deltaTimeSec = deltaTimeSecTemp.total_seconds()
            lastTime = tempDateTime; 
        sensorString = str(cgm[kk])
        sensorString = sensorString.replace(',', '.')
        sensorFloat = 18*float(sensorString);
        
        if sensorFloat > 0:
            dateTimeListCGM.append(tempDateTime)
            cgmList.append(sensorFloat)
            deltaTimeSecList.append(deltaTimeSec)
        else:
            countNan = countNan +1; 
        
    except:
        print("kk: " + str(kk))
        break
        ff = 1

dfCGM   = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec']);
dfInsulin = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'deltaTimeSec'])
dfInsulin['dateTime'] = dateTimeListInsulin
dfInsulin['bolus'] = bolusList
dfInsulin['rate'] = rateList
dfInsulin['deltaTimeSec'] = deltaTimeSecListInsulin

dfCGM['dateTime'] = dateTimeListCGM
dfCGM['cgm'] = cgmList
dfCGM['deltaTimeSec'] = deltaTimeSecList