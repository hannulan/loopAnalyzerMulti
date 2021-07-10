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
dfNew   = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec']);


time = dfRead['Time'].to_list()
date = dfRead['Date'].to_list()
cgm  = dfRead['Sensor Glucose (mmol/L)']
bolus = dfRead['Bolus Volume Delivered (U)']
rate = dfRead['Basal Rate (U/h)']

firstBool = True
dateTimeListInsulin = list(); 
dateTimeListCGM = list(); 

cgmList = list(); 
bolusList = list();
rateList = list();

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
        
dfInsulin_v1 = pd.DataFrame(list(zip(dateTimeListInsulin, bolusList, rateList)), 
                columns =['dateTime', 'bolus', 'rate']) 
dfInsulin_v1 = dfInsulin_v1.sort_values('dateTime', ascending=False);
dfInsulin_v1 = dfInsulin_v1.reset_index()

# Calculate time difference between each sample/row
diffTimeListInsulin = list()
diffTimeListInsulin.append(0)  
for ii in range(1,len(dfInsulin_v1)):
    diffTime =  dfInsulin_v1['dateTime'][ii-1] - dfInsulin_v1['dateTime'][ii]
    diffTimeSec = diffTime.seconds
    diffTimeListInsulin.append(diffTimeSec)

dfInsulin_v1['deltaTimeSec'] = diffTimeListInsulin


dfInsulin = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'deltaTimeSec'])
dfInsulin = dfInsulin_v1
dfInsulin = dfInsulin_v1.drop(index = 0); 
dfInsulin = dfInsulin.drop(index = len(dfInsulin))

##### CGM #####
offset = 3; 

print("start cgm: " + str(nextPart + offset - 1))
countNan = 0; 

for kk in range(nextPart + offset-1, len(date)-1):
    try:
        sensorString = str(cgm[kk])
        sensorString = sensorString.replace(',', '.')
        sensorFloat = float(sensorString);
        if sensorFloat > 0:
            dateTimeString = str(date[kk]) + ' ' + str(time[kk]);
            tempDateTime = dt.datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S"); 
            dateTimeListCGM.append(tempDateTime)
            cgmList.append(sensorFloat)
        else:
            countNan = countNan + 1; 
    except:
        ff = 1
     
dfCGM_v1 = pd.DataFrame(list(zip(dateTimeListCGM, cgmList)), 
                columns =['dateTime', 'cgm']) 
dfCGM_v1 = dfCGM_v1.sort_values('dateTime', ascending=False);
dfCGM_v1 = dfCGM_v1.reset_index()

diffTimeList = list()

diffTimeList.append(0)  
for ii in range(1,len(dfCGM_v1)):
    diffTime =  dfCGM_v1['dateTime'][ii-1] - dfCGM_v1['dateTime'][ii]
    diffTimeSec = diffTime.seconds
    diffTimeList.append(diffTimeSec)

dfCGM_v1['deltaTimeSec'] = diffTimeList

dfCGM = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec']);
dfCGM = dfCGM_v1.drop(index = 0); 
  
    
    
# TODO - lista: 

# Läs in insulinvärden


#aa = dt.datetime();
    
#with open(fn, 'r') as file:
#    reader = csv.reader(file)
#    for row in reader:
#        print(row)
        

# temp = dt.datetime.strptime(td[jj] + ' ' + tt[jj], "%Y-%m-%d %H:%M:%S")
# d = {'dateTime': 1, 'cgm': 2, 'deltaTimeSec': 5}
# d = [['tom', 10], ['nick', 15], ['juli', 14]] 

# d2 = [[10, 10, 11], [10,11,12], [14, 13,15]]
# d3 = [[10,16,17]]

# dfTemp2 = pd.DataFrame(d2, columns=['dateTime', 'cgm', 'deltaTimeSec']);
        
# dfTemp3 = pd.DataFrame(d3, columns=['dateTime', 'cgm', 'deltaTimeSec']);


