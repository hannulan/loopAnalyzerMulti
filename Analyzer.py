# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:38:19 2019

@author: hannulan
"""
import numpy as np
import datetime as dt
import help_func

class Analyzer: 
    patientName = ''; 
    
    ## Limits:
    # range, tirLevel
    # target, titLevel
    # hypoLevel1, rangeHypoLevel1
    # hypoLevel2
    # hyperLevel1
    # hyperLevel2
    
    tirLevel = [18*x for x in [3.9, 10]]; 
    titLevel = [18*x for x in [4,8]]# [4*18, 8*18]; # Pythons way for 18*[4,8]; 
    
    rangeHypoLevel1  = [18*x for x in [3.0, 3.8]] # [3.0, 3.8];
    rangeHypoLevel2  = [rangeHypoLevel1[0]];
    
    rangeHyperLevel1 = [18*x for x in [10, 13.9]] #[10*18,13.9*18];
    rangeHyperLevel2 = [rangeHyperLevel1[1]];
    
    #
    #  hypoL2  |  hypoL1    |    range         |  hyperL1    |  hyperL2
    # ---------|------------|-----------|------|-------------|------------- 
    # ----------------------|  target   |----------------------------------
    #
    
    ## Time limits:
    nightTime        = [dt.time(2,0,0), dt.time(7,0,0)];
    nightTimeMinute  = [nightTime[0].minute + nightTime[0].hour*60, nightTime[1].minute + nightTime[1].hour*60]
    dayTime          = [dt.time(7,0,0), dt.time(23,59,59)];
    dayTimeMinute    = [dayTime[0].minute + dayTime[0].hour*60, dayTime[1].minute + dayTime[1].hour*60]
    
    # | idxDay2 |            |                     idxDay2               |  
    #           |  idxNight  |                     idxDay                |
    # |---------|------------|-------------------------------------------|
    # 0         2            7                                          24
    
    ## Idx, based on time limits: 
    idxNight = [];
    idxDay  = [];
    idxDay2 = [];
    
    ## Values to calculate: 
    tir = 0; 
    tit = 0;
    tihypoLevel1Value  = 0; 
    tihypoLevel2Value  = 0; 
    tihyperLevel1Value = 0; 
    tihyperLevel2Value = 0; 
    
    cgmSD   = 0; 
    cgmSCV  = 0; 
    cgmPGS  = 0; 
    cgmMAGE = 0; 
    
    cgmSDDag  = 0; 
    cgmSDNatt = 0; 

    tihypoNightLevel2Value = 0; 
    tihypoDayLevel2Value = 0; 
    
    tihypoNightLevel1Value = 0; 
    tihypoDayLevel1Value = 0; 
    
    tirNatt = 0; 
    tirDag = 0; 
    
    tdd = 0; 
    
    
    def __init__(self, patientName, dfCGM):
        self.patientName = patientName;
        self.dfCGM = dfCGM; 
        # Calc idx night and day
        self.idxNight, self.idxDay, self.idxDay2 = self.findIdxNightDay();
        self.dfCGMNight = dfCGM.iloc[self.idxNight];
        self.dfCGMDay   = dfCGM.iloc[self.idxDay];
        self.dfCGMDay2  = dfCGM.iloc[self.idxDay2];
  
    def calcAllCGM(self):
        
        
        self.tir = self.calcTimeInXNew(self.dfCGM, self.tirLevel, '[]')  # [3.9 10]
        self.tit = self.calcTimeInXNew(self.dfCGM, self.titLevel, '[]') # [4 8]
        self.tihyperLevel1Value = self.calcTimeInXNew(self.dfCGM, self.rangeHyperLevel1, '[]');                                                # ]10 13.9] 
        self.tihyperLevel2Value = self.calcTimeInXNew(self.dfCGM, self.rangeHyperLevel2, ']...'); # ]13.9 ...
        
        self.tihypoLevel1Value      = self.calcTimeInXNew(self.dfCGM, self.rangeHypoLevel1, '[]'); # [3.0 3.8]
        self.tihypoLevel2Value      = self.calcTimeInXNew(self.dfCGM, self.rangeHypoLevel2, '...['); # ... 3.0[
        
        self.tihypoNightLevel1Value = self.calcTimeInXNew(self.dfCGMNight, self.rangeHypoLevel1, '[]'); # [3.0 3.8]
        self.tihypoNightLevel2Value = self.calcTimeInXNew(self.dfCGMNight, self.rangeHypoLevel2, '...['); # ... 3.0[
        
        self.tihypoDayLevel1Value   = self.calcTimeInXNew(self.dfCGMDay, self.rangeHypoLevel1, '[]'); # [3.0 3.8]
        self.tihypoDayLevel2Value   = self.calcTimeInXNew(self.dfCGMDay, self.rangeHypoLevel2, '...['); # ... 3.0[
        
        self.tirNightValue          = self.calcTimeInXNew(self.dfCGMNight, self.tirLevel, '[]')  # [3.9 10]
        self.tirDayValue            = self.calcTimeInXNew(self.dfCGMDay,   self.tirLevel, '[]')  # [3.9 10]
        
        self.titNightValue          = self.calcTimeInXNew(self.dfCGMDay, self.titLevel, '[]') # [4 8]
        self.tirNightValue          = self.calcTimeInXNew(self.dfCGMDay, self.tirLevel, '[]') # [4 8]
    
        cgmMean, cgmSD, cgmSCV = self.calcCGMVariation(self.dfCGM);
        self.cgmMean = round(cgmMean, 4);
        self.cgmSD   = round(cgmSD, 4); 
        self.cgmSCV  = round(cgmSCV, 4); 
        self.cgmPGS  = 0; 
        self.cgmMAGE = 0; 
        
        #cgmMean, cgmSD, cgmSCV = self.calcCGMVariation(self.dfCGMDay);
        #self.cgmSDDay  = cgmSD; 
        #cgmMean, cgmSD, cgmSCV = self.calcCGMVariation(self.dfCGMNight);
        #self.cgmSDNight = cgmSD; 

        return 1; 
    
    def findIdxNightDay(self):
        ii = 0; 
        minutes  = [[] for i in range(len(self.dfCGM))]; 
        idxNightTemp = [0 for i in range(len(self.dfCGM))]; 
        idxDayTemp   = [0 for i in range(len(self.dfCGM))]; 
        idxDay2Temp  = [0 for i in range(len(self.dfCGM))]; 
        
        while ii < len(self.dfCGM):
            self.dfCGM['dateTime'][ii]    
            minutes[ii]  = self.dfCGM['dateTime'][ii].minute + self.dfCGM['dateTime'][ii].hour*60;
            if self.nightTimeMinute[0] < minutes[ii] & minutes[ii] < self.nightTimeMinute[1]: 
                idxNightTemp[ii] = 1
                idxDay2Temp[ii]   = 0
            else: 
                idxNightTemp[ii] = 0
                idxDay2Temp[ii]   = 1
            
            if self.dayTimeMinute[0] < minutes[ii] & minutes[ii] < self.dayTimeMinute[1]:
                idxDayTemp[ii]   = 1
            ii = ii + 1;
            
        idxNight = np.argwhere(idxNightTemp).flatten().tolist();
        idxDay   = np.argwhere(idxDayTemp).flatten().tolist();
        idxDay2  = np.argwhere(idxDay2Temp).flatten().tolist();
            
        return idxNight, idxDay, idxDay2    
   
    def calcAllInsulin(self):
        self.tdd = 0; 
        
    def writeAll(self):
        ## Write result in text format to a file:     
        file_object  = open(self.patientName + '.csv', "w+") 
        file_object.write('Patient name; ' + self.patientName + '\n');
        file_object.write('tir; ' + str(self.tir) + ';\n');
        file_object.write('tit; ' + str(self.tit) + ';\n');
        
        file_object.write('tihyperLevel1; ' + str(self.tihyperLevel1Value) + ';\n');
        file_object.write('tihyperLevel2; ' + str(self.tihyperLevel2Value) + ';\n');
        file_object.write('tihypoLevel1;  ' + str(self.tihypoLevel1Value) + ';\n');
        file_object.write('tihypoLevel2;  ' + str(self.tihypoLevel2Value) + ';\n\n');
        
        file_object.write('cgmMean; ' + str(self.cgmMean)   + ';\n');
        file_object.write('cgmSD;   ' + str(self.cgmSD)   + ';\n');
        file_object.write('cgmSCV;  ' + str(self.cgmSCV)  + ';\n\n');
        
        file_object.write('cgmSDDay;   ' + str(self.cgmSDDay)   + ';\n');
        file_object.write('cgmSDNight; ' + str(self.cgmSDNight) + ';\n\n');
        
        file_object.write('cgmPGS;  ' + str(self.cgmPGS)  + ';\n');
        file_object.write('cgmMAGE; ' + str(self.cgmMAGE) + ';\n\n');
        
        file_object.write('tihypoDagLevel1; ' + str(self.tihypoDayLevel1Value) + ';\n');
        file_object.write('tihypoDagLevel2; ' + str(self.tihypoDayLevel2Value) + ';\n');
        file_object.write('tihypoNattLevel1;  ' + str(self.tihypoNightLevel1Value) + ';\n');
        file_object.write('tihypoNattLevel2;  ' + str(self.tihypoNightLevel2Value) + ';\n\n');
        
        file_object.write('tirDag;  ' + str(self.tirDag) + ';\n');
        file_object.write('tirNatt; ' + str(self.tirNatt) + ';\n');
        file_object.write('tdd; ' + str(self.tdd) + ';\n');
        file_object.close()

# PGS
# MAGE (medelamplitud hos glukosexkursioner)
        
# Standarddevition, cgm, dagtid
# Standarddevition, cgm, natt (2-7)

# Antal basaljusteringar
# Förhållande basal/bolus
# Antal bolusar

# Vikt/totalt     
#
# Ätna kolhydrater (?). Loggade
    def calcPGS(self, dfCGM):
        print('calcPGS')
        
    def calcCGMVariation(self, df):
        stdCGM  = np.std(df['cgm'], ddof=1)/18;
        meanCGM = np.mean(df['cgm'])/18;
        cgmSCV = stdCGM/meanCGM;
        
        return meanCGM, stdCGM, cgmSCV 
    
    def calcTimeInXNew(self, dfCGM, xRange, mode):
        # This functions calculation percentage of time in range. 
        # TODO: Remove time slots that are larger than 5 minutes
        # idxInRange    = (dfCGM['cgm'] <=  xRange[1]) & (dfCGM['cgm'] >=  xRange[0])
        
        if not dfCGM.empty: #operator.not_(dfCGM.empty):
            if mode == '[]':
                idxInRange    = (xRange[0] <= dfCGM['cgm']) & (dfCGM['cgm'] <=  xRange[1]); 
            elif mode == ']]':
                idxInRange    = (xRange[0] <  dfCGM['cgm']) & (dfCGM['cgm'] <=  xRange[1]) 
            elif mode == '...[':
                idxInRange    = (dfCGM['cgm'] <  xRange[0]) 
            elif mode == ']...':
                idxInRange    = (dfCGM['cgm'] > xRange[0]) 
            else:
                idxInRange = [];
            totTime = sum(dfCGM['deltaTime'][1:len(dfCGM)])
            tix    = sum(dfCGM['deltaTime'][1:len(dfCGM)][idxInRange])/totTime;
            tix = round(tix, 4); 
        else:
            tix = 0; 
            
        return tix

    
    
    
    
    ## Old stuff below:
    def calcTimeInX(self, dfCGM, xRange):
        # This functions calculation percentage of time in range. 
        # TODO: Remove time slots that are larger than 5 minutes
        idxAboveRange = dfCGM['cgm'] > xRange[1];
        idxBelowRange = dfCGM['cgm'] < xRange[0];
        idxInRange    = (dfCGM['cgm'] <=  xRange[1]) & (dfCGM['cgm'] >=  xRange[0])
        
        totTime = sum(dfCGM['deltaTime'][1:len(dfCGM)])
        
        timeAboveRange_per = sum(dfCGM['deltaTime'][1:len(dfCGM)][idxAboveRange])/totTime;
        timeBelowRange_per = sum(dfCGM['deltaTime'][1:len(dfCGM)][idxBelowRange])/totTime;
        timeInRange_per    = sum(dfCGM['deltaTime'][1:len(dfCGM)][idxInRange])/totTime;
        return timeAboveRange_per, timeBelowRange_per, timeInRange_per
    def basalBolusPercentage(self, dfBasal, dfBolus):
        # Thie function...
        
        totBolus = sum(dfBolus['bolus']);
        N = len(dfBasal);
        totBasal = sum(dfBasal['basalRate'][1:N]*dfBasal['deltaTime'][1:N]/3600);
        tot = totBolus + totBasal; 
        basalPercentage = totBasal/tot; 
        bolusPercentage = totBolus/tot; 
        
        return basalPercentage, bolusPercentage, tot