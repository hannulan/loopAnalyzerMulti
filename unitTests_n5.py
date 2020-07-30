# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 19:53:38 2020

@author: hannu
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

tf = 'testFiles/treatments_n5.json'
ef_n1 = 'testFiles/entriesEXNy.json'
name = 'Daniel'
timeCGMStableMin = 20; 

reader_n1 = Reader.Reader(name, ef_n1, tf, timeCGMStableMin);
#analyzer = Analyzer.Analyzer(name, reader.numDayNight, reader.dfCGM, reader.dfInsulin, timeCGMStableMin); 

lenDfCGMCorrect_n1 = 1121; 
firstDateCorrect_n1 = dt.date(2020,7, 8)
lastDateCorrect_n1 =  dt.date(2020,7, 11)
booleanWholeDayNight_correct_n1 = True; 
numDayNightCorrect_n1 = 4; 
lendfInsulinCorrect_n1 = 727; "Vet ej exakt varde men det ska vara 731 eller mindre. Mindre är nog för att den sorterar bort en del av andra anledningar än de vanliga. Men hur många tar den bort egentligen?"


lenDfCGMTest_n1 = len( reader_n1.dfCGM['dateTime'])
lastDateTest_n1 = reader_n1.dfCGM['dateTime'][1].date()
firstDateTest_n1 = reader_n1.dfCGM['dateTime'][lenDfCGMTest_n1-1].date()
booleanWholeDayNight_test_n1 = reader_n1.booleanWholeDayNight;
numDayNight_test_n1 = reader_n1.numDayNight; 
lendfInsulinTest_n1 = len( reader_n1.dfInsulin['dateTime'])

ef_n2    = 'testFiles/entriesEXNy_v2.json'
reader_n2 = Reader.Reader(name, ef_n2, tf, timeCGMStableMin);

lenDfCGMCorrect_n2 = 1118; 
firstDateCorrect_n2 = dt.date(2020,7, 8)
lastDateCorrect_n2 =  dt.date(2020,7, 11)
booleanWholeDayNight_correct_n2 = True; 
numDayNightCorrect_n2 = 4; 

lenDfCGMTest_n2 = len( reader_n2.dfCGM['dateTime'])
lastDateTest_n2 = reader_n2.dfCGM['dateTime'][1].date()
firstDateTest_n2 = reader_n2.dfCGM['dateTime'][lenDfCGMTest_n2-1].date()
booleanWholeDayNight_test_n2 = reader_n2.booleanWholeDayNight;
numDayNight_test_n2 = reader_n2.numDayNight; 

ef_n3    = 'testFiles/entries1_time.json'
name = 'Daniel'
timeCGMStableMin = 20; 
reader_n3 = Reader.Reader(name, ef_n3, tf, timeCGMStableMin);
booleanWholeDayNight_correct_n3 = False; 
booleanWholeDayNight_test_n3 = reader_n3.booleanWholeDayNight;
numDayNightCorrect_n3 = 2; 
numDayNight_test_n3 = reader_n3.numDayNight; 


nFault5 = 0; 

if lenDfCGMCorrect_n1 == lenDfCGMTest_n1:
    print('Length test 1:     OK')
else: 
    print('Length test 1:    NOK')
    nFault5 = nFault5 +1; 
    
if firstDateCorrect_n1 == firstDateTest_n1:
    print('First date test 1:     OK')
else:
    print('First date test 1:    NOK')
    nFault5 = nFault5 +1;
    
if lastDateCorrect_n1 == lastDateTest_n1:
    print('Last date test 1:     OK')
else:
    print('Last date test 1:    NOK')
    nFault5 = nFault5 +1; 

if booleanWholeDayNight_correct_n1 == booleanWholeDayNight_test_n1:
    print('booleanWholeDayNight date test 1:     OK')
else:
     print('booleanWholeDayNight date test 1:   NOK')
     nFault5 = nFault5 +1; 
     
if numDayNightCorrect_n1 == numDayNight_test_n1:
    print('NumDayNight  test 1:     OK')
else:
     print('numDayNight  test 1:   NOK')
     nFault5 = nFault5 +1; 
    
if lendfInsulinCorrect_n1 == lendfInsulinTest_n1:
    print('len dfInsulin  test 1:     OK')
else:
     print('len dfInsulin test 1:   NOK')
     nFault5 = nFault5 +1;    
    
if lenDfCGMCorrect_n2 == lenDfCGMTest_n2:
    print('Length test 2:     OK')
else: 
    print('Length test 2:    NOK')
    nFault5 = nFault5 +1; 
    
if firstDateCorrect_n2 == firstDateTest_n2:
    print('First date test 2:     OK')
else:
    print('First date test 2:    NOK')
    nFault5 = nFault5 +1;
    
if lastDateCorrect_n2 == lastDateTest_n2:
    print('Last date test 2:     OK')
else:
    print('Last date test 2:    NOK')
    nFault5 = nFault5 +1; 
    
if booleanWholeDayNight_correct_n2 == booleanWholeDayNight_test_n2:
    print('booleanWholeDayNight date test 2:     OK')
else:
     print('booleanWholeDayNight date test 2:   NOK')
     nFault5 = nFault5 +1; 
    
if numDayNightCorrect_n2 == numDayNight_test_n2:
    print('NumDayNight  test 2:     OK')
else:
     print('numDayNight  test 2:   NOK')
     nFault5 = nFault5 +1; 
          
if booleanWholeDayNight_correct_n3 == booleanWholeDayNight_test_n3:
    print('booleanWholeDayNight date test 3:     OK')
else:
     print('booleanWholeDayNight date test 3:   NOK')
     nFault5 = nFault5 +1; 
     
if numDayNightCorrect_n3 == numDayNight_test_n3:
    print('NumDayNight  test 3:     OK')
else:
     print('numDayNight  test 3:   NOK')
     nFault5 = nFault5 +1; 
     
if nFault5 == 0: 
    print('unitTest 5:       OK')
else: 
    print('unitTest 5:       NOK')