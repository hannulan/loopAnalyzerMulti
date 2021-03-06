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

import help_func


## All entry-files: 
petraBengtsonEntry    = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PetraBangtsson/InlamningFinal/PetraEntries_v2.json'
paulJaniakEntry       = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PaulJaniak/InlamningFinal/entriesPaul2.json'

claraHogstramEntry    = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/ClaraHogstrom/InlamningFinal/ClaraEntries.json'
ceciliaSommerfeld     = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/CeciliaSommerfeld/InlamningFinal/ceciliaEntries_v2.json'

ingridSvenssonEntry   = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/IngridSvensson/InlamningFinal/Ingridentries_v3.json'
danielJohanssonEntry1 = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanilEntries_forstaOmgangen.json'
danielJohanssonEntry2 = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/danielEntries_andraOmgangen.json'


## All treatment-files: 
petraT = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PetraBangtsson/InlamningFinal/PetraTreatments.json'
paulT = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PaulJaniak/InlamningFinal/treatmentsPaul3.json'

claraT   = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/ClaraHogstrom/InlamningFinal/ClaraTreatments.json'
ceciliaT = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/CeciliaSommerfeld/InlamningFinal/ceciliatreatments_v2.json'

ingridT = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/IngridSvensson/InlamningFinal/IngridTreatments_v4.json'

daniel1T = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments1011-1211_forstaOmgangen.json'
daniel2T = '/Users/mattiasbrannstrom/Desktop/Hanna/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments0111-0311_andraOmgangen.json'

## All readers: 
readerPetra = Reader.Reader('Petra', petraBengtsonEntry, petraT);

readerPaul   = Reader.Reader('Paul', paulJaniakEntry, paulT);
readerClara   = Reader.Reader('Clara', claraHogstramEntry, claraT);
readerCecilia = Reader.Reader('Cecilia', ceciliaSommerfeld, ceciliaT);

readerIngrid  = Reader.Reader('Ingrid', ingridSvenssonEntry, ingridT);
readerDaniel1 = Reader.Reader('Daniel1', danielJohanssonEntry1, daniel1T);
readerDaniel2 = Reader.Reader('Daniel2', danielJohanssonEntry2, daniel2T);

reader_v = [readerPetra, readerPaul, readerClara, readerCecilia, readerIngrid, readerDaniel1, readerDaniel2];
name_v   = ['Petra', 'Paul', 'Clara', 'Cecilia', 'Ingrid', 'Daniel1', 'Daniel2'];
ii_v =  [0, 1, 2, 3, 4, 5, 6];
for ii in [0]:
    print('Read file from: ' + name_v[ii])
    reader_v[ii].readData(); 
    if ii != 1:
        reader_v[ii].createCGMStructure();
    #input("Press Enter to continue...")
    
    
    
## All Analyzers:
    
## Petra
ii = 0; 
dfCGM   = reader_v[ii].dfCGM;
reader  = reader_v[ii]
# reader_v[ii].createBolusStructure();
# reader_v[ii].createBasalRateStructure();
analyzer = Analyzer.Analyzer(name_v[ii], dfCGM); 
analyzer.calcAllCGM(); 
analyzer.calcAllInsulin();
#analyzer.writeAll();



ef = 'entries_ex_caspian.json';
name = 'Daniel'
tf = 'treatments_ex_nightscoutcaspian.json'


reader = Reader.Reader(name, ef, tf);
reader.createCGMStructure()




#timeAboveRange_per, timeBelowRange_per, timeInRange_per = analyzer.calcTimeInRange(dfCGM)
#timeAboveTarget_per, timeBelowTarget_per, timeInTarget_per = analyzer.calcTimeInTarget(dfCGM)

#stdCGM = analyzer.calcStdCGM(dfCGM);

# print('Patient name: ' + name_v[ii]);

# print('------------- Time in Range -------------')
# print('Time below range: ' + str(timeBelowRange_per))
# print('Time in range:    ' + str(timeInRange_per))
# print('Time above range: ' + str(timeAboveRange_per))


# print('------------- Time in Target -------------')
# print('Time below target: ' + str(timeBelowTarget_per))
# print('Time in target:    ' + str(timeInTarget_per))
# print('Time above target: ' + str(timeAboveTarget_per))

# print('------------- Glucose variability -------------')
# print('CGM std: ' + str(stdCGM))


# ## Write result in text format to a file:     
# file_object  = open('petra2.txt', "w+") 
# file_object.write('Patient name: ' + 'Petra');
# file_object.close()


# file_object.write('------------- Time in Range -------------\n')
# file_object.write('Time below range: ' + str(timeBelowRange_per) + '\n')
# file_object.write('Time in range:    ' + str(timeInRange_per) + '\n')
# file_object.write('Time above range: ' + str(timeAboveRange_per) + '\n')

# file_object.write('------------- Time in Target -------------' + '\n')
# file_object.write('Time below target: ' + str(timeBelowTarget_per) + '\n')
# file_object.write('Time in target:    ' + str(timeInTarget_per) + '\n')
# file_object.write('Time above target: ' + str(timeAboveTarget_per) + '\n')

# file_object.write('------------- Glucose variability -------------' + '\n')
# file_object.write('CGM std: ' + str(stdCGM) + '\n')

    
# file_object.close()

    
    
    