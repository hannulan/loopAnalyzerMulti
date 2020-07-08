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
        
        self.dfCGM   = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTime']);
        self.dfBolus = pd.DataFrame(columns=['dateTime', 'bolus'])
        self.dfCarbs = pd.DataFrame(columns=['dateTime', 'carbs'])
        self.dfBasal = pd.DataFrame(columns=['dateTime', 'basalRate', 'deltaTime'])
        self.readData();
        
    def readData(self):
        if self.readFromFile == 1: 
                    
            entries = [];
            entries = json.load(open(self.datafile_entries))

            treatments = [];
            treatments = json.load(open(self.datafile_treatments));
        
            self.dfEntries = pd.DataFrame.from_dict(entries);
            self.dfTreatments = pd.DataFrame.from_dict(treatments);
            
            print('Reading files: ' + self.datafile_entries + ' and '+ self.datafile_treatments +' for ' + self.patientName)
            print('Entry size: ' + str(len(entries)))
            print('Treatment size: ' + str(len(treatments)))
            print('Remove Treatments without timestamp')
            
            idxToRemove = self.dfTreatments['timestamp'].isnull();
            idxToKeep   = idxToRemove; 
            
            #for kk in range(0,len(idxToRemove)):
            #    idxToKeep[kk] = not(idxToRemove[kk])
                
            #self.dfTreatments = self.dfTreatments.iloc[idxToKeep.tolist()] 
           
        return self.dfEntries, self.dfTreatments
    
    def createCGMStructure(self):
        self.dfCGM = pd.DataFrame(columns=['dateTime', 'cgm', 'deltaTime'])
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
                self.dfCGM['deltaTime'][ii] = sec.total_seconds();
            tempOld = temp; 
            
        return self.dfCGM
    
    def createBolusStructure(self):     
        #Bolusself.dfb = pd.DataFrame(columns=['dateTime', 'bolus', 'basal'])
        # dfBolus = ['dateTime', 'bolus'])
        self.dfBolus['dateTime'] = self.dfTreatments['timestamp']
        
        for jj in range(0,len(self.dfBolus['dateTime'])):
            if self.dfTreatments['eventType'][jj] == 'Correction Bolus' :
                self.dfBolus['bolus'][jj] = self.dfTreatments['insulin'][jj]
            elif self.dfTreatments['eventType'][jj] == 'Meal Bolus' :
                 self.dfBolus['bolus'][jj] = self.dfTreatments['insulin'][jj]
            else: 
                 self.dfBolus['bolus'][jj] = 0;
         
        np.sum(self.dfBolus['bolus'])        
                
        return 1;

    def createBasalRateStructure(self):
        # Hitta alla rate != 0 och != Nan
        rateV = self.dfTreatments['rate'].tolist();
        idxNan = np.argwhere(np.isnan(rateV)).flatten();
        for kk in range(0,len(idxNan)):
            rateV[idxNan[kk]] = 0.0; 

        # 
        self.dfBasal['dateTime'] = self.dfTreatments['timestamp'];
        self.dfBasal['basalRate']     = rateV;
        
        return 1; 
    
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
        for ii in range(1,len(self.dfBasal['deltaTime'])):    
            #tempNext = self.dfBasal['dateTime'][ii-1] - self.dfBasal['dateTime'][ii];
            sec = self.dfBasal['dateTime'][ii-1] - self.dfBasal['dateTime'][ii];
            #sec = temp - tempNext;
            self.dfBasal['deltaTime'][ii] = sec.total_seconds();
            #temp = tempNext; 
            