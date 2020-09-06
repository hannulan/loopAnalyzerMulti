# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:38:19 2019

@author: hannulan
"""
import numpy as np
import datetime as dt


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
    titLevel = [18*x for x in [4, 8]]# [4*18, 8*18]; # Pythons way for 18*[4,8]; 
    
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
    cgmGVP  = 0; 
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
    
    
    def __init__(self, patientName, reader):
        self.patientName = patientName;
        self.numDayNight = reader.numDayNight; 
        self.dfCGM       = reader.dfCGM; 
        self.dfInsulin   = reader.dfInsulin; 
        self.booleanWholeDayNight = reader.booleanWholeDayNight; 
        
        # Calc idx night and day
        self.idxNight, self.idxDay, self.idxDay2 = self.findIdxNightDay();
        self.dfCGMNight = self.dfCGM.iloc[self.idxNight];
        self.dfCGMDay   = self.dfCGM.iloc[self.idxDay];
        self.dfCGMDay2  = self.dfCGM.iloc[self.idxDay2];

        self.timeCGMStableSec = reader.timeCGMStableSec;
        
        self.calcAllCGM(); 
        
        self.tdd = self.calcAllInsulin(self.dfInsulin, self.booleanWholeDayNight)
  
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
        self.cgmMean = cgmMean;
        self.cgmSD   = cgmSD; 
        self.cgmSCV  = cgmSCV;
        
        self.cgmGVP = self.calcGVP(self.dfCGM);
        
        self.cgmPGS  = self.calcPGS(self.dfCGM, self.cgmGVP, self.cgmMean*18, self.tir, self.numDayNight); 
        self.cgmMAGE = 0; 
        
        # Calculate cgm values for day and nights
        cgmMean, cgmSD, cgmSCV = self.calcCGMVariation(self.dfCGMDay);
        self.cgmSDDay  = cgmSD; 
        cgmMean, cgmSD, cgmSCV = self.calcCGMVariation(self.dfCGMNight);
        self.cgmSDNight = cgmSD; 

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
   
    def calcAllInsulin(self, dfInsulin, booleanWholeDayNight):
        sumBolus  = np.sum(dfInsulin['bolus']); 
        basal     = dfInsulin['rate'];
        timeHours = dfInsulin['deltaTimeSec']/60/60;
        sumBasal  = np.sum(basal*timeHours); 
        
        if booleanWholeDayNight:
            tdd = round((sumBasal+sumBolus)/self.numDayNight, 4); 
        else: 
            tdd = -1; 
            
        return tdd;  
        
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
        file_object.write('TDD genomsnitt; ' + str(self.tdd) + ';\n');
        file_object.close()

    def calcPGS(self, dfCGM, GVP, MG, PTIR, numDayNight):
        
        # PGS: 
        # the glycemic variability, GVP
        # mean glucose,
        # percent time in range (70–180mg/dL),
        # and incidence of hypoglycemic episodes per week deﬁned separately as 
        # the number of episodes per week <= 54mg/dL and 
        # the number of episodes < 70mg/dL and >= 55mg/dL. 
        # Reference: https://pubmed.ncbi.nlm.nih.gov/28585873/
                
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
                
        numWeek = numDayNight/7; 
        N_54 = self.counter(dfCGM['cgm'], 54)/numWeek
        N_70 = self.counter(dfCGM['cgm'], 70)/numWeek - N_54; 
        
        F_54 = 0.5 + 4.5*(1 - np.exp(-0.81093*N_54));
        
        if N_70 <= 7.65:
            F_70 = 0.5714*N_70 + 0.625; 
        else:
            F_70 = 5;

        
        F_GVP  = 1 + 9*self.logisticFunc(100*GVP, 0.049, 65.47)
        F_PTIR = 1 + 9*self.logisticFunc(100*PTIR, -0.0833, 55.04)
        F_MG   = 1 + 9*self.logisticFunc(MG, -0.1139, 72.08) + 9*self.logisticFunc(MG, 0.09195, 157.57)
        
        PGS = F_54 + F_70 + F_GVP + F_PTIR + F_MG; 
        if GVP == -1:
            PGS = -1
            
        PGS = round(PGS, 4);

        return PGS
    
    def logisticFunc(self, x, steepness, offset):
        # Calc logistic function, https://en.wikipedia.org/wiki/Logistic_function
        # steepness = k in wikipedia article
        # offset = x0 in wikipedia article

        return 1/(1+np.exp(-steepness*(x-offset)))
    
    def counter(self, cgm, limit):
        flag = False; 
        count = 0; 
        hyst = 9; 
        for ii in range(0, len(cgm)):
            if cgm[ii] < limit and flag == False:
                count = count + 1;
                flag = True
            elif cgm[ii] >= (limit + hyst):
                flag = False
         
        return count
        
    
    def calcGVP(self, dfCGM):
        # Calculate GVP, Glucose variability percentage, based om mg/dL and time in minutes
        # Reference: https://pubmed.ncbi.nlm.nih.gov/29227755/
        # IMPORTANT TO USE CORRECT UNITS!
        # Time: [minute]
        # cgm: [mg/dL]

        # L = sum{sqrt(dt_i^2 + dcgm_i^2)}          L = sum{sqrt(dx_i^2 + dy_i^2)}
        # L0 = sum{dt_i}                            L0 = sum{dx_i}
        # GVP = (L/L0 - 1)*100
        
        # L0 = sum{dt_i}                            L0 = sum{dx_i}
        # GVP = (L/L0 - 1)*100
        
        # L = sum{sqrt(dt_i^2 + dcgm_i^2)}
        # L = sum(sqrt{deltaTimeSec/60^2 + dcgm_mg_dL^2})
        
        deltaCGM = -np.diff(dfCGM['cgm'])
        
        N = len(dfCGM['deltaTimeSec']);
        
        LAll = np.square(dfCGM['deltaTimeSec'][1:N]/60) + np.square(deltaCGM)
        LAll = LAll.to_numpy();
        LAll = np.sqrt(np.double(LAll));
        
        idx  = dfCGM['deltaTimeSec'] < self.timeCGMStableSec
        
        L = sum(LAll[idx[1:N]])  # LAll has one element less than dfCGM and hence idx. Due to diff calc of cgm-values
        
        L0All = dfCGM['deltaTimeSec'][1:N]/60
        
        L0 = sum(L0All[idx])
        
        if L0 == 0:
            GVP = -1
        else: 
            GVP = (L/L0 - 1);
        
        GVP = round(GVP, 4);
        return GVP
        
    def calcCGMVariation(self, df):
        stdCGM  = round(np.std(df['cgm'], ddof=1)/18, 4);
        meanCGM = round(np.mean(df['cgm'])/18, 4);
        cgmSCV  = round(stdCGM/meanCGM, 4);
        
        return meanCGM, stdCGM, cgmSCV 
    
    def calcTimeInXNew(self, dfCGM, xRange, mode):
        # This functions calculation percentage of time in range. 
        # TODO: Remove time slots that are larger than 5 minutes
        # TODO: Remove some self. which is there for debugging
        # idxInRange    = (dfCGM['cgm'] <=  xRange[1]) & (dfCGM['cgm'] >=  xRange[0])
        
        if not dfCGM.empty: #operator.not_(dfCGM.empty):
            if mode == '[]':
                idxInRange    = (xRange[0] <= dfCGM['cgm']) & (dfCGM['cgm'] <=  xRange[1]) 
            elif mode == ']]':
                idxInRange    = (xRange[0] <  dfCGM['cgm']) & (dfCGM['cgm'] <=  xRange[1]) 
            elif mode == '...[':
                idxInRange    = (dfCGM['cgm'] <  xRange[0]) 
            elif mode == ']...':
                idxInRange    = (dfCGM['cgm'] > xRange[0]) 
            else:
                idxInRange = [];
            
            delta = dfCGM['deltaTimeSec'];
            delta.iloc[0] = 0; # Set deltaTime for the first (last) sample to zero since it is unknown. 
            deltaNew = np.minimum(delta,self. timeCGMStableSec)
            totTime = sum(deltaNew);
            
            tix = sum(np.minimum(deltaNew[idxInRange], self.timeCGMStableSec))/totTime;
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
        
        totTime = sum(dfCGM['deltaTimeSec'][1:len(dfCGM)])
        
        timeAboveRange_per = sum(dfCGM['deltaTimeSec'][1:len(dfCGM)][idxAboveRange])/totTime;
        timeBelowRange_per = sum(dfCGM['deltaTimeSec'][1:len(dfCGM)][idxBelowRange])/totTime;
        timeInRange_per    = sum(dfCGM['deltaTimeSec'][1:len(dfCGM)][idxInRange])/totTime;
        return timeAboveRange_per, timeBelowRange_per, timeInRange_per
    def basalBolusPercentage(self, dfBasal, dfBolus):
        # Thie function...
        
        totBolus = sum(dfBolus['bolus']);
        N = len(dfBasal);
        totBasal = sum(dfBasal['basalRate'][1:N]*dfBasal['deltaTimeSec'][1:N]/3600);
        tot = totBolus + totBasal; 
        basalPercentage = totBasal/tot; 
        bolusPercentage = totBolus/tot; 
        
        return basalPercentage, bolusPercentage, tot