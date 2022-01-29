#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:22:59 2020

@author: mattiasbrannstrom

Script for reading and analyzing specific files from different patients
Filename specified in the beginning of the file, one Entry and one treatment file
The files are exports from Nightscout

"""
import pickle
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


##
susanE = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/SusanMustafa/samihusseint1d.herokuapp.com_entries.json'
susanT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/SusanMustafa/samihusseint1d.herokuapp.com_treatments.json'
readerSusan = Reader.Reader('Susan', susanE, susanT,  timeCGMStableMin, 'created_at');

mattiasE = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/MattiasSchain/entries_mattiasSchain.json'
mattiasT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/MattiasSchain/treatments_mattiasSchain.json'
readerMattias = Reader.Reader('Mattias', mattiasE, mattiasT,  timeCGMStableMin, 'created_at');

andreasE = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/AndreasBjorklund/entries_andreas.json'
andreasT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/AndreasBjorklund/treatments_andreas.json'
readerAndreas = Reader.Reader('Andreas', andreasE, andreasT,  timeCGMStableMin, 'created_at');

janE = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/JanSturestig/Final/diasigvard.herokuapp.com.json'
janT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/JanSturestig/Final/diasigvardTreatments.json'
readerJan = Reader.Reader('Jan', janE, janT,  timeCGMStableMin, 'created_at');



analyzerSusan = Analyzer.Analyzer('Susan', readerSusan)
analyzerMattias = Analyzer.Analyzer('Mattias', readerMattias)
analyzerAndreas = Analyzer.Analyzer('Andreas', readerAndreas)
analyzerJan = Analyzer.Analyzer('Jan', readerJan)


# henrikSjoE = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/HenrikSjostrand2/henriksjostrand_entries_3months.json'
# henrikSjoT = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/HenrikSjostrand2/henriksjostrand_treatments_3months.json'
# readerHenrikSjo = Reader.Reader('HenrikSjo', henrikSjoE, henrikSjoT,  timeCGMStableMin, 'created_at');
# Henrik har laddat upp csv filer istället för json-filer

danielT              = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanielTreatments_all.json' # Treatment file 1 and 2 put together to one file
danielE              = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/DanielJohansson/InlamningFinal/DanilEntries_all2.json' # Entry file 1 and 2 put together to one file
readerDaniel = Reader.Reader('Daniel', danielE, danielT,  timeCGMStableMin, 'timestamp');
readerDaniel.numDayNight = 118 # Hard coded number of days because the treatment and entry files are put together from two different periods. Not enough to look at last and first date.



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

analyzerDaniel = Analyzer.Analyzer('Daniel', readerDaniel)

analyzerList = list()
analyzerList = [analyzerPetra, analyzerPaul, analyzerClara, analyzerCecilia, analyzerIngrid, analyzerDaniel, analyzerEmma, analyzerHenrik]
for analyzer in analyzerList:
    analyzer.calcAllCGM(); 
        

analyzerList = [analyzerPetra, analyzerPaul, analyzerClara, analyzerCecilia, analyzerIngrid, analyzerDaniel, analyzerEmma, analyzerHenrik, analyzerSusan, analyzerMattias, analyzerAndreas, analyzerJan]
for analyzer in analyzerList:
    analyzer.writeAll(); 
 
    
readerList = [readerPetra, readerPaul, readerClara, readerCecilia, readerIngrid, readerDaniel, readerEmma, readerHenrik, readerSusan, readerMattias, readerAndreas, readerJan]
nameList =  ['petra', 'paul', 'clara', 'cecilia', 'ingrid','daniel', 'emma', 'henrik', 'susan', 'mattias', 'andreas', 'jan']


# Write output files 
analyzerPetra.writeAll()   
analyzerPaul.writeAll()
analyzerClara.writeAll()   
analyzerCecilia.writeAll() 
analyzerIngrid.writeAll()
analyzerDaniel1.writeAll()
analyzerDaniel2.writeAll()
analyzerEmma.writeAll()
analyzerHenrik.writeAll()

analyzerDaniel.writeAll()