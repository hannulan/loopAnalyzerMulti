# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:38:19 2019

@author: hannulan
"""
import numpy as np
import datetime as dt
import help_func

class Analyzer: 
    targetValue = [4*18, 8*18];
    rangeValue  = [4*18,10*18];
    nightTime   = [dt.time(2,0,0), dt.time(7,0,0)];
    dayTime     = [dt.time(7,0,0), dt.time(23,59,59)];
    
    
    
    def __init__(self, patientName):
        self.PatientName = patientName;
        self.storage = 0;
        
    
    
# PGS
# MAGE (medelamplitud hos glukosexkursioner)
        
# Standarddevition, cgm, dagtid
# Standarddevition, cgm, natt (2-7)

# Antal basaljusteringar
# Förhållande basal/bolus
# Antal bolusar

# Vikt/totalt insulin
#
# Ätna kolhydrater (?). Loggade
    def calcPGS(self, dfCGM):
        print('calcPGS')
        
    def calcStdCGM(self, dfCGM):
        stdCGM = np.std(dfCGM['cgm'])/18;
        return stdCGM
    
    def calcTimeInRange(self, dfCGM):
        # This functions calculation percentage of time in range. 
        timeAboveRange_per, timeBelowRange_per, timeInRange_per = self.calcTimeInX(dfCGM, self.rangeValue);
        
        return timeAboveRange_per, timeBelowRange_per, timeInRange_per

    def calcTimeInTarget(self, dfCGM):
        # This functions calculation percentage of time in range. 
        print("calcTimeInTarget")
        
        timeAboveTarget_per, timeBelowTarget_per, timeInTarget_per = self.calcTimeInX(dfCGM, self.targetValue);
        
        return timeAboveTarget_per, timeBelowTarget_per, timeInTarget_per
    
    
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
    
    def calcMARD_PGS_GVI(self, dfCGM):
        # Calculate MARD, PGS, GVI and returns
        MARD = 0;
        PGC = 0; 
        GVI = 0;
        return MARD, PGC, GVI    
    
    def basalBolusPercentage(self, dfBasal, dfBolus):
        # Thi function...
        
        totBolus = sum(dfBolus['bolus']);
        N = len(dfBasal);
        totBasal = sum(dfBasal['basalRate'][1:N]*dfBasal['deltaTime'][1:N]/3600);
        tot = totBolus + totBasal; 
        basalPercentage = totBasal/tot; 
        bolusPercentage = totBolus/tot; 
        
        return basalPercentage, bolusPercentage, tot