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
   
    
    def __init__(self, patientName, fileNameEntries, fileNameTreatments):
        self.patientName = patientName; 
        self.readFromFile = 1; 
        self.patientName = patientName;
        self.datafile_entries = fileNameEntries; #self.patientName + '\\' + 'response_entries.json'; 
        self.datafile_treatments = fileNameTreatments; 
        #self.datafile_treatments = self.patientName + '\\' + 'response_treatments.json';
        
        self.dfEntries = pd.DataFrame();
        self.dfTreatments = pd.DataFrame();
        
        self.dfCGM   = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec']);
        self.dfBolus = pd.DataFrame(columns=['dateTime', 'bolus'])
        self.dfCarbs = pd.DataFrame(columns=['dateTime', 'carbs'])
        self.dfBasal = pd.DataFrame(columns=['dateTime', 'basalRate', 'deltaTimeSec'])
        
        self.readData();
        self.createCGMStructure(); 
        self.createInsulinStructure();
        
        self.numDayNight = self.fixData(); # Remove to that only whole day/nigth periods are in data series.
        
    def readData(self):
        if self.readFromFile == 1: 
                    
            entries = [];
            entries = json.load(open(self.datafile_entries, encoding="utf8"))

            treatments = [];
            treatments = json.load(open(self.datafile_treatments, encoding="utf8"));
        
            self.dfEntries = pd.DataFrame.from_dict(entries);
            self.dfTreatments = pd.DataFrame.from_dict(treatments);
            
            print('Reading files: ' + self.datafile_entries + ' and '+ self.datafile_treatments +' for ' + self.patientName)
            print('Entry size: ' + str(len(entries)))
            print('Treatment size: ' + str(len(treatments)))
            print('Remove Treatments without timestamp')
            
            self.idxToRemove = self.dfTreatments['timestamp'].isnull();
            self.dfTreatments = self.dfTreatments[~self.idxToRemove]; # Remove all rows with timestamp = nan
            self.dfTreatments.reset_index(inplace = True)
            
            #self.idxNanRate = self.dfTreatments['rate'].isnull(); # Det här tilldelar alla kolumne
            #self.dfTreatments[self.idxNanRate] = 0; 
        return self.dfEntries, self.dfTreatments
     
    def createInsulinStructure(self):     
          self.dfInsulin = pd.DataFrame(columns=['dateTime', 'bolus', 'rate', 'deltaTimeSec'])
          
          self.dfInsulin['rate'] = self.dfTreatments['rate']
          
          " Create bolus rows for all Correction and meal boluses "
          # TODO: Double check if this also includes the micro boluses
          for jj in range(0,len(self.dfInsulin['dateTime'])):
              if self.dfTreatments['eventType'][jj] == 'Correction Bolus' :
                  self.dfInsulin['bolus'][jj] = self.dfTreatments['insulin'][jj]
              elif self.dfTreatments['eventType'][jj] == 'Meal Bolus' :
                  if np.isnan(self.dfTreatments['insulin'][jj]) :
                      self.dfInsulin['bolus'][jj] = 0
                  else:
                      self.dfInsulin['bolus'][jj] = self.dfTreatments['insulin'][jj]
              else: 
                  self.dfInsulin['bolus'][jj] = 0;     
          
          " Calculate deltatimeSec for each row "
          tempOld = dt.time(0);
          for ii in range(0,len(self.dfTreatments['timestamp'])):
            try: 
                temp = dt.datetime.strptime(self.dfTreatments['timestamp'][ii], '%Y-%m-%dT%H:%M:%S%fZ');
            except:
                print(self.dfEntries['dateString'])
                print('ii: ' + str(ii))
                temp = 0;
                temp = dt.datetime.strptime('2019-11-01T22:04:25.814+0100', '%Y-%m-%dT%H:%M:%S.%fZ');
            self.dfInsulin['dateTime'][ii]  = temp;
            if ii == 0:
                print('hej')
            else:
                sec = tempOld - temp;
                self.dfInsulin['deltaTimeSec'][ii] = sec.total_seconds();
            tempOld = temp; 
          
          #self.idxRate = ~self.dfTemp.isin([0])
          idxRateNan = self.dfInsulin['rate'].isna()
          self.dfInsulin['rate'][idxRateNan] = 0
           
          idx = list();  
          for ii in range(0,len(self.dfInsulin['rate'])):
              if self.dfInsulin['rate'][ii] == 0:
                  idx.append(ii);
              else:
                  rateNow = self.dfInsulin['rate'][ii];
                  while len(idx) > 0: 
                      self.dfInsulin['rate'][idx.pop()] = rateNow; 
                  idx = list();     
              
          return self.dfInsulin;
   
    def createCGMStructure(self):
        self.dfCGM = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTimeSec'])
        self.dfCGM['cgm'] = self.dfEntries['sgv']
        
        if len(self.dfEntries['sgv']) != len(self.dfEntries['dateString']):
            print('Error in createCGMStructure')
            return
        
        tempOld = dt.time(0);
        for ii in range(0,len(self.dfEntries['dateString'])):
            try: 
                temp = dt.datetime.strptime(self.dfEntries['dateString'][ii], '%Y-%m-%dT%H:%M:%S.%fZ');
            except:
                print(self.dfEntries['dateString'])
                print('ii: ' + str(ii))
                temp = 0;
                temp = dt.datetime.strptime('2019-11-01T22:04:25.814+0100', '%Y-%m-%dT%H:%M:%S.%fZ');
            self.dfCGM['dateTime'][ii]  = temp;
            if ii == 0:
                print('inget')
            else:
                sec = tempOld - temp;
                self.dfCGM['deltaTimeSec'][ii] = sec.total_seconds();
            tempOld = temp; 
            
        return self.dfCGM
        
    def fixData(self): 
        # Putsa till data så att det endast är hela dygn med.    
        numDayNight = 2;  
        return numDayNight; 
    
    def createCarbStructure(self):
        
        idx = np.isfinite(self.dfTreatments['carbs']);
        
        self.dfCarbs['carbs'] = np.array(self.dfTreatments['carbs'][idx]);

        dateTemp = np.array(self.dfTreatments['timestamp'][idx]);   
        counter = 0;
        for jj in dateTemp:
            self.dfCarbs['dateTime'][counter] = dt.datetime.strptime(jj, '%Y-%m-%dT%H:%M:%SZ');
            counter = counter + 1;
        #tempNext = dt.datetime.strptime(self.dfTreatments['timestamp'][1], '%Y-%m-%dT%H:%M:%SZ');
        temp = dt.datetime.strptime(self.dfTreatments['timestamp'][0], '%Y-%m-%dT%H:%M:%SZ');
        for ii in range(1,len(self.dfBasal['deltaTimeSec'])):    
            #tempNext = self.dfBasal['dateTime'][ii-1] - self.dfBasal['dateTime'][ii];
            sec = self.dfBasal['dateTime'][ii-1] - self.dfBasal['dateTime'][ii];
            #sec = temp - tempNext;
            self.dfBasal['deltaTimeSec'][ii] = sec.total_seconds();
            #temp = tempNext; 
            