#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:22:59 2020

@author: mattiasbrannstrom

Script for reading and analyzing specific files from different patients
Filename specified in the beginning of the file, one Entry and one treatment file
The files are exports from Nightscout

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


## All tfiles: 
petraT                = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PetraBangtsson/InlamningFinal/PetraTreatments.json'
petraBengtsonEntry    = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PetraBangtsson/InlamningFinal/PetraEntries_v2.json'

paulT                 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PaulJaniak/InlamningFinal/treatmentsPaul3.json'
paulJaniakEntry       = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/PaulJaniak/InlamningFinal/entriesPaul2.json'

claraT                = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/ClaraHogstrom/InlamningFinal/ClaraTreatments.json'
claraHogstramEntry    = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/ClaraHogstrom/InlamningFinal/ClaraEntries.json'

ceciliaT              = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/CeciliaSommerfeld/InlamningFinal/ceciliatreatments_v2.json'
ceciliaSommerfeld     = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/CeciliaSommerfeld/InlamningFinal/ceciliaEntries_v2.json'


ingridT               = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/IngridSvensson/InlamningFinal/IngridTreatments_v4.json'
ingridSvenssonEntry   = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/IngridSvensson/InlamningFinal/Ingridentries_v3.json'

daniel1T              = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments1011-1211_forstaOmgangen.json'
danielJohanssonEntry1 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanilEntries_forstaOmgangen.json'

daniel2T              = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments0111-0311_andraOmgangen.json'
danielJohanssonEntry2 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/danielEntries_andraOmgangen.json'

emmaE = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/EmmaMandroppe/Final/entries.json'
emmaT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/EmmaMandroppe/Final/treatments.json'

henrikE = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/HenrikGrentzelius/entries.json'
henrikT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/HenrikGrentzelius/treatments.json'


pd.set_option('mode.chained_assignment', None)

## Create reading object for all patients
readerPetra = Reader.Reader('Petra', petraBengtsonEntry, petraT,  timeCGMStableMin, 'created_at'); #
readerPaul   = Reader.Reader('Paul', paulJaniakEntry, paulT,  timeCGMStableMin, 'created_at'); # OK

readerClara   = Reader.Reader('Clara', claraHogstramEntry, claraT,  timeCGMStableMin, 'timestamp');
readerCecilia = Reader.Reader('Cecilia', ceciliaSommerfeld, ceciliaT,  timeCGMStableMin, 'created_at'); #
# Varfor bara 20

readerIngrid  = Reader.Reader('Ingrid', ingridSvenssonEntry, ingridT,  timeCGMStableMin, 'created_at'); 
readerDaniel1 = Reader.Reader('Daniel1', danielJohanssonEntry1, daniel1T,  timeCGMStableMin, 'timestamp');
readerDaniel2 = Reader.Reader('Daniel2', danielJohanssonEntry2, daniel2T,  timeCGMStableMin, 'timestamp');

readerEmma = Reader.Reader('Emma', emmaE, emmaT,  timeCGMStableMin, 'created_at');
readerHenrik = Reader.Reader('Henrik', henrikE, henrikT,  timeCGMStableMin, 'created_at');

## Create analyzers for all patients:
analyzerPetra   = Analyzer.Analyzer('Petra', readerPetra)
analyzerPaul    = Analyzer.Analyzer('Paul', readerPaul)
analyzerClara   = Analyzer.Analyzer('Clara', readerClara)
analyzerCecilia = Analyzer.Analyzer('Cecilia', readerCecilia)
analyzerIngrid  = Analyzer.Analyzer('Ingrid', readerIngrid)
analyzerDaniel1 = Analyzer.Analyzer('Daniel1', readerDaniel1)
analyzerDaniel2 = Analyzer.Analyzer('Daniel2', readerDaniel2)
analyzerEmma    = Analyzer.Analyzer('Emma', readerEmma)
analyzerHenrik  = Analyzer.Analyzer('Henrik', readerHenrik)


# Write output files for all patients:
analyzerPetra.writeAll()   
analyzerPaul.writeAll()
analyzerClara.writeAll()   
analyzerCecilia.writeAll() 
analyzerIngrid.writeAll()
analyzerDaniel1.writeAll()
analyzerDaniel2.writeAll()
analyzerEmma.writeAll()
analyzerHenrik.writeAll()
