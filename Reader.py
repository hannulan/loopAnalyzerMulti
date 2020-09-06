# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:47:31 2019

@author: hannulan
"""
from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya

import datetime as dt

class Reader: 
   
    
    def __init__(self, patientName, fileNameEntries, fileNameTreatments, timeCGMStableMin, timeStrTreatments = 'timestamp',
                 runSimple = False, dfCGMIn = False, dfInsulinIn = False, numDayNightIn = 0, booleanWholeDayNightIn = True):
        self.patientName = patientName; 
            
        if (runSimple == False): 
            self.readFromFile = 1; 
            self.patientName = patientName;
            self.datafile_entries = fileNameEntries; #self.patientName + '\\' + 'response_entries.json'; 
            self.datafile_treatments = fileNameTreatments; 
            
            self.timeCGMStableSec = timeCGMStableMin*60;
            #self.datafile_treatments = self.patientName + '\\' + 'response_treatments.json';
            
            self.dfEntries = pd.DataFrame();
            self.dfTreatments = pd.DataFrame();
            
            self.dfCGM   = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec']);
            self.dfInsulin = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'deltaTimeSec'])
    
            #self.dfBolus = pd.DataFrame(columns=['dateTime', 'bolus'])
            #self.dfCarbs = pd.DataFrame(columns=['dateTime', 'carbs'])
            #self.dfBasal = pd.DataFrame(columns=['dateTime', 'basalRate', 'deltaTimeSec'])
            
            self.dfEntries, self.dfTreatments, timeStampStr = self.readData(self.datafile_entries, self.datafile_treatments, timeStrTreatments);
            self.dfCGM = self.createCGMStructure(self.dfEntries); 
            self.dfInsulin = self.createInsulinStructure(self.dfTreatments, timeStampStr);
            
            print('size dfCGM: ' + str(len(self.dfCGM)))
            print('size dfInsulin: ' + str(len(self.dfInsulin)))
    
            self.numDayNight, self.booleanWholeDayNight, self.dfCGM, self.dfInsulin = self.fixData(); # Remove to that only whole day/nigth periods are in data series.
            print('size dfCGM, efter fix: ' + str(len(self.dfCGM)))
            print('size dfInsulin, efter fix: ' + str(len(self.dfInsulin)))
        else:
            self.readFromFile = 1; 
            #self.datafile_entries = fileNameEntries; #self.patientName + '\\' + 'response_entries.json'; 
            #self.datafile_treatments = fileNameTreatments; 
            
            self.timeCGMStableSec = timeCGMStableMin*60;
            
            self.dfEntries = pd.DataFrame();
            self.dfTreatments = pd.DataFrame();
            
            self.dfCGM     = dfCGMIn; 
            self.dfInsulin = dfInsulinIn; 
            
            print('size dfCGM: ' + str(len(self.dfCGM)))
            print('size dfInsulin: ' + str(len(self.dfInsulin)))
    
            self.numDayNight = numDayNightIn; 
            self.booleanWholeDayNight = booleanWholeDayNightIn;
            print('size dfCGM, efter fix: ' + str(len(self.dfCGM)))
            print('size dfInsulin, efter fix: ' + str(len(self.dfInsulin))) 
            
   
    
    def readData(self, datafile_entries, datafile_treatments, timeStrTreatments):
        # Read data from json files (datafiles_entries and datafile_treatments)
        # timeStrT is the time string 
        if self.readFromFile == 1: 
                    
            entries = [];
            entries = json.load(open(datafile_entries, encoding="utf8"))

            treatments = [];
            treatments = json.load(open(datafile_treatments, encoding="utf8"));
        
            dfE = pd.DataFrame.from_dict(entries);
            dfT = pd.DataFrame.from_dict(treatments);
            
            print('Reading files: ' + datafile_entries + ' and '+ datafile_treatments +' for ' + self.patientName)
            print('Entry size: ' + str(len(entries)))
            print('Treatment size: ' + str(len(treatments)))
            
            print('Treatment Pandas size: ' + str(len(dfT)))
            print('Entry Pandas size size: ' + str(len(dfE)))

            # try: 
            #     idxToRemove = dfT['timestamp'].isnull();
            #     timeStampStr = 'timestamp'
            # except: 
            #     idxToRemove = dfT['created_at'].isnull();
            #     timeStampStr = 'created_at'
               
            idxToRemove = dfT[timeStrTreatments].isnull();
            timeStampStr =  timeStrTreatments;   
            dfT = dfT[~idxToRemove]; # Remove all rows with timestamp = nan
            dfT.reset_index(inplace = True)
            
            print('Treatment size after remove: ' + str(len(dfT)))

        return dfE, dfT, timeStampStr
     
    def createInsulinStructure(self, dfT, timeStampStr):     
          dfIns = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'carbs', 'deltaTimeSec'])
          dfIns['rate'] = dfT['rate']
          dfIns['carbs'] = dfT['carbs']
          
          " Create bolus rows for all Correction and meal boluses "
          # TODO: Double check if this also includes the micro boluses
          for jj in range(0,len(dfIns['dateTime'])):
              if dfT['eventType'][jj] == 'Correction Bolus' :
                  dfIns['bolus'][jj] = dfT['insulin'][jj]
              elif dfT['eventType'][jj] == 'Meal Bolus' :
                  if np.isnan(dfT['insulin'][jj]) :
                      dfIns['bolus'][jj] = 0
                  else:
                      dfIns['bolus'][jj] = dfT['insulin'][jj]
              else: 
                  dfIns['bolus'][jj] = 0;     
          
          " Calculate deltatimeSec for each row "
          tempOld = dt.time(0);
          for ii in range(0,len(dfT[timeStampStr])):
            try: 
                temp = dt.datetime.strptime(dfT[timeStampStr][ii], '%Y-%m-%dT%H:%M:%S%fZ');
            except:
                #print('ii: ' + str(ii))
                temp = 0;
                #temp = dt.datetime.strptime('2019-11-01T22:04:25.+0100', '%Y-%m-%dT%H:%M:%S.%fZ');
                try:
                    temp = dt.datetime.strptime(dfT[timeStampStr][ii], '%Y-%m-%dT%H:%M:%S.%fZ');
                except: 
                    temp = dt.datetime.strptime(dfT['created_at'][ii], '%Y-%m-%dT%H:%M:%S.%fZ');

            dfIns['dateTime'][ii]  = temp;
            if ii == 0:
                dfIns['deltaTimeSec'][ii] = 0;
            else:
                sec = tempOld - temp;
                dfIns['deltaTimeSec'][ii] = sec.total_seconds();
            tempOld = temp; 
          " Done with deltaTimeSec " 
           
          # Assign all carbs that are nan to 0
          idxCarbsNan = dfIns['carbs'].isna()
          dfIns['carbs'][idxCarbsNan] = 0
           
          idx = list();  
          # for ii in range(0,len(dfIns['rate'])):
          #     if dfIns['rate'][ii] == 0:
          #         idx.append(ii);
          #     else:
          #         rateNow = dfIns['rate'][ii];
          #         while len(idx) > 0: 
          #             dfIns['rate'][idx.pop()] = rateNow; 
          #         idx = list();  
          
          ii = len(dfIns['rate']) - 1; 
          rateNow = None; 
          nanVector = dfIns['rate'].isna()          
          while ii >= 0 : 
              if nanVector[ii] == True :
                  dfIns['rate'][ii] = rateNow;   
              else:
                  rateNow = dfIns['rate'][ii];
              ii = ii -1;    
              
          return dfIns;
   
    def createCGMStructure(self, dfE):
        self.dfCGM = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec'])
        self.dfCGM['cgm'] = dfE['sgv']
        
        if len(dfE['sgv']) != len(dfE['dateString']):
            print('Error in createCGMStructure')
            return
        
        tempOld = dt.time(0);
        for ii in range(0,len(dfE['dateString'])):
            
            try: 
                temp = dt.datetime.strptime(dfE['dateString'][ii], '%Y-%m-%dT%H:%M:%S.%fZ');
            except:
                #print('ii: '  + str(ii))
                temp = 0;
                #print(dfE['dateString'][ii-1])
                #print(dfE['dateString'][ii])
                temp = dt.datetime.strptime(dfE['dateString'][ii], '%Y-%m-%dT%H:%M:%S.%f+0100');
                #temp = dt.datetime.strptime('2019-11-01T22:04:25.814+0100', '%Y-%m-%dT%H:%M:%S.%fZ');
            self.dfCGM['dateTime'][ii]  = temp;
            if ii == 0:
                #print('inget')
                j = 0; 
            else:
                sec = tempOld - temp;
                self.dfCGM['deltaTimeSec'][ii] = sec.total_seconds();
            tempOld = temp; 
            
        return self.dfCGM
        
    def fixData(self): 
        # Find whole day/night (dygn) and remove other part of data
        # Both for CGM and Insulin
        
        startIdxCGM, stopIdxCGM = self.findWholeDayNight(self.dfCGM, self.timeCGMStableSec);   
                        
        # Find out if at least one whole dayNight has been found for CGM data
        # If not, return all data
        if startIdxCGM <= stopIdxCGM:
            # No whole daynights detected
            booleanOnlyWholeDayNight = False;
            startIdxCGM = len(self.dfCGM['dateTime'])-1;
            stopIdxCGM  = 0; 
        elif startIdxCGM == -1 or stopIdxCGM == -1:
            booleanOnlyWholeDayNight = False;
            startIdxCGM = len(self.dfCGM['dateTime'])-1;
            stopIdxCGM  = 0; 
        else: 
            booleanOnlyWholeDayNight = True;

        stopD  = self.dfCGM['dateTime'].iloc[stopIdxCGM];
        startD = self.dfCGM['dateTime'].iloc[startIdxCGM];
        
        diffDate = stopD - startD; 
        numDayNight = diffDate.days + 1;  
        
        newCGM = self.dfCGM.iloc[stopIdxCGM:startIdxCGM+1];
        newCGM = newCGM.reset_index();
        
        idx2 = (self.dfInsulin['dateTime'] >= startD) & (self.dfInsulin['dateTime'] <= stopD)
        newInsulin = self.dfInsulin[idx2];
        newInsulin = newInsulin.reset_index()
        
        # Find all index where (date >= startDate) & (date <= stopDate)
        # Remove this code because it is not tested. Will probably work   
        # idx = (self.dfCGM['dateTime'] >= self.startDate) & (self.dfCGM['dateTime'] <= self.stopDate)
        # self.dfCGM = self.dfCGM[idx];
        # self.dfCGM.reset_index(inplace = True) 
        # idx2 = (self.dfInsulin['dateTime'] >= self.startDate) & (self.dfInsulin['dateTime'] <= self.stopDate)
        # self.dfInsulin = self.dfInsulin[idx2];
        # self.dfInsulin.reset_index(inplace = True)
        
        return numDayNight, booleanOnlyWholeDayNight, newCGM, newInsulin; 
    
    def findWholeDayNight(self, df, limm):
        ### findWholeDayNight(df, limit)
        # Find first index of first whole day
        # And last index of last whole day/night
        # return said indexes
        
        startIdx = -1; 
        stopIdx  = -1; 
        timeComp = 23*60*60 + 59*60 + 59 - limm;
        loopCount = 0; 
        ll = len(df['dateTime']);
        while loopCount < ll: 
            # Find last time-point where time of day is right before midnight
            # "right before" means maximum timeCGMStableSec before midnight
            tt = df['dateTime'][loopCount].time();
            timeTemp = tt.hour*60*60 + tt.minute*60 + tt.second; 
            if timeTemp > timeComp:
                # Hittat rätt
                stopIdx = loopCount;
                break
            loopCount = loopCount + 1; 
            
        loopCount = len(df['dateTime']) - 1;     
        while loopCount >= 0:
            # Find first time-point where time of day is right after midnight
            # "rigth after" means maximum timeCGMStableSec after midnight
            tt = df['dateTime'][loopCount].time();
            timeTemp = tt.hour*60*60 + tt.minute*60 + tt.second;
            if timeTemp < limm:
                startIdx = loopCount;
                break
            loopCount = loopCount - 1; 
        
        return startIdx, stopIdx
    
    # def createCarbStructure(self):
        
    #     idx = np.isfinite(self.dfTreatments['carbs']);
        
    #     self.dfCarbs['carbs'] = np.array(self.dfTreatments['carbs'][idx]);

    #     dateTemp = np.array(self.dfTreatments['timestamp'][idx]);   
    #     counter = 0;
    #     for jj in dateTemp:
    #         self.dfCarbs['dateTime'][counter] = dt.datetime.strptime(jj, '%Y-%m-%dT%H:%M:%SZ');
    #         counter = counter + 1;
    #     #tempNext = dt.datetime.strptime(self.dfTreatments['timestamp'][1], '%Y-%m-%dT%H:%M:%SZ');
    #     temp = dt.datetime.strptime(self.dfTreatments['timestamp'][0], '%Y-%m-%dT%H:%M:%SZ');
    #     for ii in range(1,len(self.dfBasal['deltaTimeSec'])):    
    #         #tempNext = self.dfBasal['dateTime'][ii-1] - self.dfBasal['dateTime'][ii];
    #         sec = self.dfBasal['dateTime'][ii-1] - self.dfBasal['dateTime'][ii];
    #         #sec = temp - tempNext;
    #         self.dfBasal['deltaTimeSec'][ii] = sec.total_seconds();
    #         #temp = tempNext; 
            