# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 23:39:07 2021

@author: Mattias Brännström
"""
from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
import datetime as dt
import csv 

class ReaderMedtronic: 
   
    
    def __init__(self, patientName,fn, headerLine = 6, dateFormat = "%Y-%m-%d %H:%M:%S", insulinOffset = 0,  dfCGMIn = False, dfInsulinIn = False):
        self.patientName = patientName; 
        self.dateFormat = dateFormat;
        self.insulinOffset = insulinOffset
        self.dfCGM = dfCGMIn; 
        self.dfInsulin = dfInsulinIn
        self.numDayNight = 1
        self.booleanWholeDayNight = True
        self.timeCGMStableSec = 20*60;
        self.dfCGM, self.dfInsulin = self.read(fn, headerLine);
        
    def read(self, fn, headerLine):
        
        df = pd.DataFrame();
        
        dfRead = pd.read_csv(fn,  sep=';', header = headerLine);
        dfCGM   = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec']);
        dfInsulin = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'deltaTimeSec'])
        
        #index = dfRead['Index'].to_list()
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
            #print("jj: " + str(jj))  
            #try:
            
            if type(date[jj]) == str and not(date[jj].__contains__('MiniMed')):
                dateTimeString = str(date[jj]) + ' ' + str(time[jj]);
                #print("dateTimeString: " + dateTimeString)
                tempDateTime = dt.datetime.strptime(dateTimeString, self.dateFormat); 
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
            else:
            # except:    
                print("jj: " + str(jj))
                nextPart = jj
                break
            
        # Remove nan in bolus list and replace with 0
        # Add basal rate (in U/hour) to every row
        # Does not change any order
        lastIndexInsulin = nextPart - 1 + self.insulinOffset;
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
                tempDateTime = dt.datetime.strptime(dateTimeString, self.dateFormat); 
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
        
        return dfCGM, dfInsulin