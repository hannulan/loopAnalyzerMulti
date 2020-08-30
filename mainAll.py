#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:22:59 2020

@author: mattiasbrannstrom
"""

from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya


import datetime as dt
import Reader
import Analyzer

timeCGMStableMin = 20; 


## All entry-files: 
petraBengtsonEntry    = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PetraBangtsson/InlamningFinal/PetraEntries_v2.json'
paulJaniakEntry       = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PaulJaniak/InlamningFinal/entriesPaul2.json'

claraHogstramEntry    = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/ClaraHogstrom/InlamningFinal/ClaraEntries.json'
ceciliaSommerfeld     = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/CeciliaSommerfeld/InlamningFinal/ceciliaEntries_v2.json'

ingridSvenssonEntry   = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/IngridSvensson/InlamningFinal/Ingridentries_v3.json'
danielJohanssonEntry1 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanilEntries_forstaOmgangen.json'
danielJohanssonEntry2 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/danielEntries_andraOmgangen.json'


## All treatment-files: 
petraT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PetraBangtsson/InlamningFinal/PetraTreatments.json'
paulT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PaulJaniak/InlamningFinal/treatmentsPaul3.json'

claraT   = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/ClaraHogstrom/InlamningFinal/ClaraTreatments.json'
ceciliaT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/CeciliaSommerfeld/InlamningFinal/ceciliatreatments_v2.json'

ingridT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/IngridSvensson/InlamningFinal/IngridTreatments_v4.json'

daniel1T = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments1011-1211_forstaOmgangen.json'
daniel2T = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments0111-0311_andraOmgangen.json'

pd.set_option('mode.chained_assignment', None)

## All readers: 
readerPetra = Reader.Reader('Petra', petraBengtsonEntry, petraT,  timeCGMStableMin);

readerPaul   = Reader.Reader('Paul', paulJaniakEntry, paulT,  timeCGMStableMin, 'created_at');
readerClara   = Reader.Reader('Clara', claraHogstramEntry, claraT,  timeCGMStableMin);
readerCecilia = Reader.Reader('Cecilia', ceciliaSommerfeld, ceciliaT,  timeCGMStableMin);

readerIngrid  = Reader.Reader('Ingrid', ingridSvenssonEntry, ingridT,  timeCGMStableMin);
readerDaniel1 = Reader.Reader('Daniel1', danielJohanssonEntry1, daniel1T,  timeCGMStableMin);
readerDaniel2 = Reader.Reader('Daniel2', danielJohanssonEntry2, daniel2T,  timeCGMStableMin);


## All analyzers:
analyzerPetra = Analyzer.analyzer('Petra', readerPetra)
analyzerPaul = Analyzer.analyzer('Paul', readerPaul)
analyzerClara = Analyzer.analyzer('Clara', readerClara)
analyzerCecilia = Analyzer.analyzer('Cecilia', readerCecilia)
analyzerIngrid = Analyzer.analyzer('Ingrid', readerIngrid)


readerPaul.createInsulinStructure(readerPaul.dfTreatements, timeStampStr)


reader_v = [readerPetra, readerPaul, readerClara, readerCecilia, readerIngrid, readerDaniel1, readerDaniel2];
name_v   = ['Petra', 'Paul', 'Clara', 'Cecilia', 'Ingrid', 'Daniel1', 'Daniel2'];
ii_v =  [0, 1, 2, 3, 4, 5, 6];
for ii in [0]:
    print('Read file from: ' + name_v[ii])
    reader_v[ii].readData(); 
    if ii != 1:
        reader_v[ii].createCGMStructure();
    input("Press Enter to continue...")
    
    
    
## All Analyzers:
    
## Petra
ii = 0; 
dfCGM   = reader_v[ii].dfCGM;   
#analyzer = Analyzer.Analyzer(name_v[ii], dfCGM); 
#analyzer.calcAllCGM(); 
#analyzer.writeAllCGM();

#timeAboveRange_per, timeBelowRange_per, timeInRange_per = analyzer.calcTimeInRange(dfCGM)
#timeAboveTarget_per, timeBelowTarget_per, timeInTarget_per = analyzer.calcTimeInTarget(dfCGM)

#stdCGM = analyzer.calcStdCGM(dfCGM);

