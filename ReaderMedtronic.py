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
        
        self.booleanWholeDayNight = True
        self.timeCGMStableSec = 20*60;
        self.dfCGM, self.dfInsulin = self.read(fn, headerLine);
        first = self.dfCGM.iloc[0].dateTime.date()
        last  = self.dfCGM.iloc[len(self.dfCGM)-1].dateTime.date()
        
        self.dfCGM = self.removeFirstLastDate(self.dfCGM, first, last)
        self.dfInsulin = self.removeFirstLastDate(self.dfInsulin, first, last)
        
        self.dfCGM, self.dfInsulin = self.extractLastNDays();
        first = self.dfCGM.iloc[0].dateTime.date()
        last  = self.dfCGM.iloc[len(self.dfCGM)-1].dateTime.date()
         
        
        self.numDayNight = (first-last).days + 1
        
    def removeFirstLastDate(self, df, first, last):
        numList = list(); 
        for ii in range(0, len(df)):
            dateNow = df.iloc[ii].dateTime.date()
            if (dateNow == first) | (dateNow == last):
                numList.append(ii)
        df = df.drop(index = numList)
        df = df.reset_index()
        return df
        

                
    def calcNumDays(self):
        self.numDayNight = 1
    
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
        
        idxRate = rate == 'RATE UNKNOWN'
        rate[idxRate] = 0
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
        
        ## Second part of file, contains CGM values
        print("Reading second part of the file")
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
    
    def extractLastNDays(self, nDays = 14):
        # Find the last whole day/night (dygn), extract 14 days back and remove the rest of the data
        # Both for CGM and Insulin
        # Call only if numDayNight > 14
     
        stopD  = self.dfCGM['dateTime'].iloc[0]; # Last day in the dataframe
        newStartD = stopD - dt.timedelta(days=nDays); # New start date to extract the last 14 days in the dataframe
       
        idx1 = (self.dfCGM['dateTime'] >= newStartD); # Find all indeces to keep
        startIdxCGM = np.count_nonzero(idx1)-1; # First index for the new start date
       
        newCGM = self.dfCGM.iloc[0:startIdxCGM]; # CGM extracted for 14 days

        idx2 = (self.dfInsulin['dateTime'] >= newStartD) & (self.dfInsulin['dateTime'] <= stopD)
        newInsulin = self.dfInsulin[idx2]; # Insulin extracted for 14 days
       
        return newCGM, newInsulin